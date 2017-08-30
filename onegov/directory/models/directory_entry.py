from onegov.core.orm import Base
from onegov.core.orm.mixins import ContentMixin
from onegov.core.orm.mixins import TimestampMixin
from onegov.core.orm.types import UUID
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict
from uuid import uuid4


class DirectoryEntry(Base, ContentMixin, TimestampMixin):
    """ A single entry of a directory. """

    __tablename__ = 'directory_entries'

    #: An interal id for references (not public)
    id = Column(UUID, primary_key=True, default=uuid4)

    #: The directory this entry belongs to
    directory_id = Column(ForeignKey('directories.id'), nullable=False)

    #: the polymorphic type of the entry
    type = Column(Text, nullable=True)

    #: The order of the entry in the directory
    order = Column(Text, nullable=False, index=True)

    #: The title of the entry
    title = Column(Text, nullable=False)

    #: Describes the entry briefly
    lead = Column(Text, nullable=True)

    #: All keywords defined for this entry (indexed)
    _keywords = Column(
        MutableDict.as_mutable(HSTORE), nullable=True, name='keywords'
    )

    __mapper_args__ = {
        'order_by': order,
        'polymorphic_on': type
    }

    __table_args__ = (
        Index('inverted_keywords', 'keywords', postgresql_using='gin'),
    )

    @property
    def keywords(self):
        return set(self._keywords.keys()) if self._keywords else set()

    @keywords.setter
    def keywords(self, value):
        self._keywords = {k: '' for k in value} if value else None