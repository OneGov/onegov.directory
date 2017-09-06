from collections import defaultdict
from onegov.form import flatten_fieldsets, parse_formcode
from onegov.core.utils import normalize_for_url


class DirectoryMigration(object):
    """ Takes a directory and the structure/configuration it should have in
    the future.

    It then migrates the existing directory entries, if possible.

    """

    def __init__(self, directory, new_structure, new_configuration):
        self.directory = directory
        self.new_structure = new_structure
        self.new_configuration = new_configuration
        self.changes = StructuralChanges(
            self.directory.structure,
            self.new_structure
        )

    @property
    def possible(self):
        if not self.directory.entries:
            return True

        if not self.changes:
            return True

        return False

    def execute(self):
        assert self.possible

        for entry in self.directory.entries:
            self.directory.update(entry, **entry.values)

        self.directory.structure = self.new_structure
        self.directory.configuration = self.new_configuration


class StructuralChanges(object):
    """ Tries to detect structural changes between two formcode blocks.

    Can only be trusted if the ``detection_successful`` property is True. If it
    is not, the detection failed because the changes were too great.

    """

    def __init__(self, old_structure, new_structure):
        self.old = {
            f.id: f for f in flatten_fieldsets(parse_formcode(old_structure))
        }
        self.new = {
            f.id: f for f in flatten_fieldsets(parse_formcode(new_structure))
        }

        self.detect_added_fields()
        self.detect_removed_fields()
        self.detect_renamed_fields()  # modifies added/removed fields
        self.detect_changed_fields()

    def __bool__(self):
        return self.added_fields\
            or self.removed_fields\
            or self.renamed_fields\
            or self.changed_fields

    def detect_added_fields(self):
        self.added_fields = [
            f.id for f in self.new.values()
            if f.id not in {f.id for f in self.old.values()}
        ]

    def detect_removed_fields(self):
        self.removed_fields = [
            f.id for f in self.old.values()
            if f.id not in {f.id for f in self.new.values()}
        ]

    def detect_renamed_fields(self):
        # renames are detected aggressively - we rather have an incorrect
        # rename than an add/remove combo. Renames lead to no data loss, while
        # a add/remove combo does.
        self.renamed_fields = {}

        for r in self.removed_fields:
            for a in self.added_fields:
                if self.old[r].type == self.new[a].type:
                    self.renamed_fields[r] = a

        self.added_fields = [
            f for f in self.added_fields if f not in self.renamed_fields]
        self.removed_fields = [
            f for f in self.removed_fields if f not in self.renamed_fields]

    def detect_changed_fields(self):
        self.changed_fields = []

        for old in self.old:
            if old in self.renamed_fields:
                new = self.renamed_fields[old]
            elif old in self.new:
                new = old
            else:
                continue

            if self.old[old].required != self.new[new].required:
                self.changed_fields.append(new)

            elif self.old[old].type != self.new[new].type:
                self.changed_fields.append(new)


def fieldset_signatures(fields):
    fieldsets = defaultdict(list)

    for field in fields:
        normalized_fieldset = normalize_for_url(field.fieldset)
        bare_id = field.id[len(normalized_fieldset) + 1:]

        fieldsets[field.fieldset].append(bare_id)

    signatures = defaultdict(list)

    for fieldset, fields in fieldsets.items():
        signatures['-'.join(fields)].append(fieldset)

    return signatures
