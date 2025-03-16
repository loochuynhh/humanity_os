import re
from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.exempt_urls = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip("/")
            if not any(
                url.match(path) for url in self.exempt_urls
            ) and not path.startswith("admin/"):
                return redirect(self.login_url + "?next=" + request.path)
        response = self.get_response(request)
        return response
