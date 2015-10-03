from __future__ import absolute_import
from dimagi.ext.couchdbkit import *


TOGGLE_ID_PREFIX = 'hqFeatureToggle'


class Toggle(Document):
    """
    A very simple implementation of a feature toggle. Just a list of items
    attached to a slug.
    """
    slug = StringProperty()
    enabled_users = ListProperty()

    def save(self, **params):
        if ('_id' not in self._doc):
            self._doc['_id'] = generate_toggle_id(self.slug)
        super(Toggle, self).save(**params)

    @classmethod
    def get(cls, docid, rev=None, db=None, dynamic_properties=True):
        docid = ensure_doc_id_has_toggle_prefix(docid)
        return super(Toggle, cls).get(docid, rev=rev, db=db, dynamic_properties=dynamic_properties)

    def add(self, item):
        """
        Adds an item to the toggle. Only saves if necessary.
        """
        if item not in self.enabled_users:
            self.enabled_users.append(item)
            self.save()

    def remove(self, item):
        """
        Removes an item from the toggle. Only saves if necessary.
        """
        if item in self.enabled_users:
            self.enabled_users.remove(item)
            self.save()


def ensure_doc_id_has_toggle_prefix(docid):
    if not docid.startswith(TOGGLE_ID_PREFIX):
        return generate_toggle_id(docid)
    return docid


def generate_toggle_id(slug):
    # use the slug to build the ID to avoid needing couch views
    # and to make looking up in futon easier
    return '{prefix}-{slug}'.format(prefix=TOGGLE_ID_PREFIX, slug=slug)
