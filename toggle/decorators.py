from django.http import Http404
from functools import wraps

from toggle import shortcuts


def require_toggle(toggle_slug):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not shortcuts.passes_toggle(toggle_slug, request):
                raise Http404()
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
