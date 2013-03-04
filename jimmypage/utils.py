import functools

from jimmypage.cache import clear_cache

def invalidate_cache(view):
    @functools.wraps(view)
    def _view(request, *args, **kwargs):
        clear_cache()
        return view(request, *args, **kwargs)
    return _view
