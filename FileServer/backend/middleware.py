from django.utils.cache import add_never_cache_headers


class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            add_never_cache_headers(response)
        else:
            response["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"

        return response
