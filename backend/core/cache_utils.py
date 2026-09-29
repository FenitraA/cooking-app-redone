# cache_utils.py
import urllib.parse
from functools import wraps
from django.core.cache import cache
from rest_framework.response import Response


def household_cache(namespace: str, timeout: int = 300):
    """
    Caches a DRF ViewSet action based on the namespace, household_id, and query parameters.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(viewset_instance, request, *args, **kwargs):
            # 1. Safely extract household_id (adjust depending on how your user model is structured)
            household_id = getattr(request.user, 'ref_household_id', 'global')

            # 2. Sort query params to ensure /api/?limit=10&offset=0 matches /api/?offset=0&limit=10
            query_items: list[tuple[str, str]] = sorted(
                request.query_params.items()
            )

            query_string = urllib.parse.urlencode(query_items)

            # 3. Build the cache key: e.g., "ingredients:list:12345:limit=20&name=apple"
            cache_key = f"{namespace}:{household_id}:{query_string}"

            # 4. Check cache
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return Response(cached_data)

            # 5. Execute view if not cached
            response = view_func(viewset_instance, request, *args, **kwargs)

            # 6. Cache the serialized data on success
            if response.status_code == 200:
                cache.set(cache_key, response.data, timeout)

            return response

        return _wrapped_view

    return decorator


def clear_household_cache(namespace: str, household_id: str | int):
    """
    Uses django-redis to wipe all cached entries for a specific namespace and household.
    Requires django-redis as the cache backend.
    """
    pattern = f"{namespace}:{household_id}:*"
    cache.delete_pattern(pattern)