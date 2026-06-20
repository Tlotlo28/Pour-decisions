from django.shortcuts import render


def terms(request):
    return render(request, "core/terms.html")


def hall_of_shame(request):
    return render(request, "core/hall_of_shame.html")