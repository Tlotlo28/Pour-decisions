from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


def terms(request):
    return render(request, "core/terms.html")


def hall_of_shame(request):
    return render(request, "core/hall_of_shame.html")


def age_gate(request):
    next_url = request.GET.get("next") or request.POST.get("next") or reverse("stories:feed")
    # Only ever redirect to our own site - never an attacker-supplied URL.
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = reverse("stories:feed")

    if request.method == "POST":
        if request.POST.get("confirm") == "yes":
            request.session["age_verified"] = True
            return redirect(next_url)
        return render(request, "core/age_denied.html")

    return render(request, "core/age_gate.html", {"next": next_url})