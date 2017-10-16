from functools import lru_cache
from onegov.core.crypto import random_token
from onegov.core.orm import Base
from onegov.core.orm.mixins import ContentMixin
from onegov.core.orm.mixins import TimestampMixin
from onegov.core.orm.types import UUID
from onegov.core.utils import normalize_for_url, dictionary_to_binary
from onegov.directory.errors import ValidationError
from onegov.directory.migration import DirectoryMigration
from onegov.directory.types import DirectoryConfigurationStorage
from onegov.file import File, FileSet
from onegov.form import flatten_fieldsets, parse_formcode, parse_form
from onegov.search import ORMSearchable
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy.orm import object_session
from sqlalchemy.orm import relationship
from sqlalchemy_utils import observes
from uuid import uuid4


INHERIT = object()


class Directory(Base, ContentMixin, TimestampMixin, ORMSearchable):
    """ A directory of entries that share a common data structure. For example,
    a directory of people, of emergency services or playgrounds.

    """

    __tablename__ = 'directories'

    es_properties = {
        'title': {'type': 'localized'},
        'lead': {'type': 'localized'}
    }

    @property
    def es_public(self):
        return False  # to be overridden downstream

    #: An interal id for references (not public)
    id = Column(UUID, primary_key=True, default=uuid4)

    #: The public, unique name of the directory
    name = Column(Text, nullable=False, unique=True)

    #: The title of the directory
    title = Column(Text, nullable=False)

    #: Describes the directory briefly
    lead = Column(Text, nullable=True)

    #: The normalized title for sorting
    order = Column(Text, nullable=False, index=True)

    #: The polymorphic type of the directory
    type = Column(Text, nullable=True)

    #: The data structure of the contained entries
    structure = Column(Text, nullable=False)

    #: The configuration of the contained entries
    configuration = Column(DirectoryConfigurationStorage, nullable=False)

    __mapper_args__ = {
        'order_by': order,
        'polymorphic_on': type
    }

    entries = relationship(
        'DirectoryEntry',
        order_by='DirectoryEntry.order',
        backref='directory'
    )

    @property
    def entry_cls_name(self):
        return 'DirectoryEntry'

    @property
    def entry_cls(self):
        return self.__class__._decl_class_registry[self.entry_cls_name]

    def add(self, values, type=INHERIT):
        entry = self.entry_cls(
            directory=self,
            type=self.type if type is INHERIT else type
        )

        object_session(self).add(entry)

        return self.update(entry, values, set_name=True)

    def update(self, entry, values, set_name=False):
        session = object_session(self)

        cfg = self.configuration

        entry.title = cfg.extract_title(values)
        entry.lead = cfg.extract_lead(values)
        entry.order = cfg.extract_order(values)
        entry.keywords = cfg.extract_keywords(values)

        if set_name:
            entry.name = normalize_for_url(entry.title)

        basic_fields = tuple(f for f in self.fields if f.type != 'fileinput')
        entry.values = {f.id: values[f.id] for f in basic_fields}

        file_fields = tuple(
            f for f in self.fields if f.type == 'fileinput'
            if values[f.id] is not None
        )
        if file_fields:
            # XXX add the ability to keep a file
            if entry.fileset:
                for f in entry.fileset.files:
                    session.delete(f)
            else:
                entry.fileset = FileSet(title=self.title)

            for field in file_fields:
                if not values[field.id]:
                    continue

                new_file = File(
                    id=random_token(),
                    name=values[field.id]['filename'],
                    reference=dictionary_to_binary(values[field.id])
                )

                entry.fileset.files.append(new_file)
                entry.values[field.id] = values[field.id]
                entry.values[field.id]['id'] = new_file.id
                entry.values[field.id]['data'] = None

        form = self.form_class(data=entry.values)

        if not form.validate():
            raise ValidationError(form.errors)

        if not session._flushing:
            object_session(self).flush()

        return entry

    @observes('title')
    def title_observer(self, title):
        self.order = normalize_for_url(title)
        self.name = self.name or self.order

    @observes('structure', 'configuration')
    def structure_configuration_observer(self, structure, configuration):
        migration = DirectoryMigration(
            directory=self,
            new_structure=structure,
            new_configuration=configuration
        )
        migration.execute()

    @property
    def fields(self):
        return tuple(flatten_fieldsets(parse_formcode(self.structure)))

    @property
    def form_class(self):
        return self.form_class_from_structure(self.structure)

    @lru_cache(maxsize=1)
    def form_class_from_structure(self, structure):
        directory = self

        class DirectoryEntryForm(parse_form(self.structure)):

            def populate_obj(self, obj):
                super().populate_obj(obj)

                directory.update(obj, self.data)

            def process_obj(self, obj):
                super().process_obj(obj)

                for field in directory.fields:
                    form_field = getattr(self, field.id)
                    form_field.data = obj.values.get(field.id)

        return DirectoryEntryForm
