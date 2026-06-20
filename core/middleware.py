from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode


class AgeGateMiddleware:
    # Paths that should NEVER be gated (admin, the gate itself, assets, legal).
    EXEMPT_PREFIXES = ("/admin", "/age-gate", "/static", "/media", "/house-rules")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        verified = request.session.get("age_verified")
        exempt = any(request.path.startswith(p) for p in self.EXEMPT_PREFIXES)
        if verified or exempt:
            return self.get_response(request)
        gate = reverse("core:age_gate")
        return redirect(f"{gate}?{urlencode({'next': request.get_full_path()})}")