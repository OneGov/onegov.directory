Changelog
---------

- Ignores unavailable fields when processing submissions.
  [href]

0.4.8 (2019-07-23)
~~~~~~~~~~~~~~~~~~~~~

- Automatically increments the directory name if there's a conflict.
  [href]

0.4.7 (2019-04-25)
~~~~~~~~~~~~~~~~~~~~~

- Fixes error when renaming a file field.
  [href]

0.4.6 (2019-04-03)
~~~~~~~~~~~~~~~~~~~~~

- Support latest onegov.search release.
  [href]

0.4.5 (2019-03-22)
~~~~~~~~~~~~~~~~~~~~~

- Uses yamls safe load function.
  [msom]

0.4.4 (2018-09-12)
~~~~~~~~~~~~~~~~~~~~~

- Adds support for text to markdown migration.
  [href]

0.4.3 (2018-09-10)
~~~~~~~~~~~~~~~~~~~~~

- Adds the ability to hide the external directory link.
  [href]

0.4.2 (2018-08-13)
~~~~~~~~~~~~~~~~~~~~~

- Fixes xlsx import failing in certain cases.
  [href]

- Raises an error when metadata.json is missing in an import.
  [href]

0.4.1 (2018-08-10)
~~~~~~~~~~~~~~~~~~~~~

- No longer overwrites the directory name during import if it exists already.
  [href]

- Throws a proper error when a file is missing from an import.
  [href]

- Ensures that only fields which have choices are actually avilable as filters.
  [href]

0.4.0 (2018-06-15)
~~~~~~~~~~~~~~~~~~~~~

- Adds natural sorting with a variant of the alphanum algorithm.
  [href]

0.3.4 (2018-06-06)
~~~~~~~~~~~~~~~~~~~~~

- Adds the ability to configure a thumbnail.
  [href]

0.3.3 (2018-06-05)
~~~~~~~~~~~~~~~~~~~~~

- Improves the quality of the dynamic elasticsarch content.
  [href]

- Adds the directory_id to the elasticsearch properties.
  [href]

- Adds support for meta/content data in the directory import/export.
  [href]

0.3.2 (2018-05-21)
~~~~~~~~~~~~~~~~~~~~~

- Adds the ability to programatically influence the entry collection results.
  [href]

0.3.1 (2018-05-16)
~~~~~~~~~~~~~~~~~~~~~

- Adds the ability to define an external link by pattern on each entry.
  [href]

0.3.0 (2018-05-16)
~~~~~~~~~~~~~~~~~~~~~

- Adds the ability to specify the order direction for directory collections.
  [href]

0.2.2 (2018-04-26)
~~~~~~~~~~~~~~~~~~~~~

- Fixes some migrations not triggering a database update.
  [href]

0.2.1 (2018-02-23)
~~~~~~~~~~~~~~~~~~~~~

- Fixes a serious performance regression.
  [href]

0.2.0 (2018-02-09)
~~~~~~~~~~~~~~~~~~~~~

- Filters values within one category using OR (existing behaviour) and values
  between categories using AND (was OR).
  [href]

0.1.7 (2018-02-06)
~~~~~~~~~~~~~~~~~~~~~

- Fixes entries from other directories being considered as duplicates.
  [href]

0.1.6 (2018-01-24)
~~~~~~~~~~~~~~~~~~~~~

- Fixes number ranges not being validated during migrations.
  [href]

0.1.5 (2018-01-24)
~~~~~~~~~~~~~~~~~~~~~

- Fixes import duplicates not being detected in all instances.
  [href]

- Fixes limit not being applied correctly (off by one).
  [href]

- Adds the ability to provide a callback for each successful entry import.
  [href]

- Fixes a case where an empty image field would result in an error.
  [href]

0.1.4 (2018-01-23)
~~~~~~~~~~~~~~~~~~~~~

- Ensures the imported lat/lon values are proper coordinates.
  [href]

0.1.3 (2018-01-22)
~~~~~~~~~~~~~~~~~~~~~

- Fixes coordinates export.
  [href]

0.1.2 (2018-01-04)
~~~~~~~~~~~~~~~~~~~~~

- Improves the flexibility of the migration helper.
  [href]

- Fixes a case where invalid entries would be added to the directory.
  [href]

0.1.1 (2017-12-29)
~~~~~~~~~~~~~~~~~~~~~

- Throws an error early if an entry with a duplicate name is created.
  [href]

0.1.0 (2017-12-22)
~~~~~~~~~~~~~~~~~~~~~

- Switches to onegov core's custom json module.
  [href]

- Adds support for text to url migration.
  [href]

- Changes the category filter from AND to OR.
  [href]

- Adds support for radio to checkbox migration.
  [href]

0.0.2 (2017-11-30)
~~~~~~~~~~~~~~~~~~~~~

- Fixes required fileinput fields not working.
  [href]

0.0.1 (2017-11-08)
~~~~~~~~~~~~~~~~~~~~~

- Initial Release.
  [href]
