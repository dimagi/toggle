from couchdbkit import ResourceNotFound
from django.conf import settings
from django.core.cache import cache

from .models import Toggle
from .caching import update_toggle_cache, get_toggle_cache_key, namespaced_item, update_toggle_document_in_cache, \
    get_toggle_document_from_cache


def toggle_enabled(slug, item, check_cache=True, namespace=None):
    """
    Given a toggle and a username, whether the toggle is enabled for that user
    """
    item = namespaced_item(item, namespace)
    cache_key = get_toggle_cache_key(slug, item)
    if check_cache:
        from_cache = cache.get(cache_key)
        if from_cache is not None:
            return from_cache

    if not settings.UNIT_TESTING or getattr(settings, 'DB_ENABLED', True):
        try:
            toggle = None
            if check_cache:
                toggle = get_toggle_document_from_cache(slug)
            if toggle is None:
                toggle = Toggle.get(slug)
            ret = item in toggle.enabled_users
        except ResourceNotFound:
            ret = False
        cache.set(cache_key, ret)
        return ret


def set_toggle(slug, item, enabled, namespace=None):
    """
    Sets a toggle value explicitly. Should only save anything if the value needed to be changed.
    """
    item = namespaced_item(item, namespace)
    if toggle_enabled(slug, item) != enabled:
        try:
            toggle_doc = Toggle.get(slug)
        except ResourceNotFound:
            toggle_doc = Toggle(slug=slug, enabled_users=[])
        if enabled:
            toggle_doc.add(item)
        else:
            toggle_doc.remove(item)

        update_toggle_document_in_cache(slug, toggle_doc)
        update_toggle_cache(slug, item, enabled)
