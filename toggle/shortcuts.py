from couchdbkit import ResourceNotFound
from django.core.cache import cache
from .models import Toggle, ENTITY_TYPES


def toggle_enabled(slug, toggle_type, entity, check_cache=True):
    """
    Given a toggle, an entity type, and an entity string, checks whether the toggle is enabled for that entity
    """
    cache_key = 'toggle-{slug}:{toggle_type}:{entity}'.format(slug=slug, toggle_type=toggle_type, entity=entity)
    if check_cache:
        from_cache = cache.get(cache_key)
        if from_cache is not None:
            return from_cache
    try:
        toggle = Toggle.get(slug)
        ret = entity in getattr(toggle, ENTITY_TYPES[toggle_type])
    except ResourceNotFound:
        ret = False
    cache.set(cache_key, ret)
    return ret


def passes_toggle(toggle_slug, request):
    """
    Given a toggle and a request, determines whether the request can pass the toggle
    """
    if hasattr(request, 'domain') and toggle_enabled(toggle_slug, 'domain', request.domain):
        return True
    if hasattr(request, 'user') and toggle_enabled(toggle_slug, 'user', request.user.username):
        return True
    return False