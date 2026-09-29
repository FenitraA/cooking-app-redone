import urllib.parse
from functools import wraps
from django.core.cache import cache
from rest_framework.response import Response


def get_household_id(request) -> str:
    return str(request.user.ref_household_id)

def household_cache(namespace: str, timeout: int = 3600):
    """Caches GET responses scoped to namespace and household ID."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(viewset_instance, request, *args, **kwargs):
            household_id = get_household_id(request)
            query_items: list[tuple[str, str]] = sorted(
                request.query_params.items()
            )

            query_string = urllib.parse.urlencode(query_items)

            cache_key = f"{namespace}:{household_id}:{query_string}"

            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return Response(cached_data)

            response = view_func(viewset_instance, request, *args, **kwargs)

            if 200 <= response.status_code < 300:
                cache.set(cache_key, response.data, timeout)

            return response

        return _wrapped_view

    return decorator


def clear_household_cache(namespace: str, household_id: str | int):
    """Wipes all keys matching the namespace pattern for a given household."""
    pattern = f"{namespace}:{household_id}:*"
    cache.delete_pattern(pattern)