from django.core.cache import cache


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
