from __future__ import unicode_literals
from django.core.cache import cache
from toggle.models import ensure_doc_id_has_toggle_prefix, Toggle


def clear_toggle_cache(slug, item, namespace=None):
    item = namespaced_item(item, namespace)
    cache_key = get_toggle_cache_key(slug, item)
    cache.delete(cache_key)


def update_toggle_cache(slug, item, state, namespace=None):
    cache_key = get_toggle_cache_key(slug, namespaced_item(item, namespace))
    cache.set(cache_key, state)


def get_toggle_cache_key(slug, item):
    return 'toggle-{slug}:{item}'.format(slug=slug, item=item)


def namespaced_item(item, namespace):
    return '{namespace}:{item}'.format(
        namespace=namespace, item=item
    ) if namespace is not None else item


def update_toggle_document_in_cache(toggle_slug, toggle_doc):
    cache_key = get_toggle_document_cache_key(toggle_slug)
    cache.set(cache_key, toggle_doc.to_json())


def get_toggle_document_from_cache(toggle_slug):
    cache_key = get_toggle_document_cache_key(toggle_slug)
    doc = cache.get(cache_key)
    if doc:
        return Toggle.wrap(doc)
    return None


def get_toggle_document_cache_key(toggle_slug):
    return 'toggle-doc:{slug}'.format(slug=ensure_doc_id_has_toggle_prefix(toggle_slug))
