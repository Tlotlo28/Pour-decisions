import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count
from .forms import StoryForm
from .models import Story, Drink, Companion, Category, Rating


def feed(request):
    base = Story.objects.filter(status=Story.Status.APPROVED).select_related("category")
    active = request.GET.get("category")

    featured = None
    if not active:
        # Highest community-rated story (needs at least one reading).
        featured = (base.annotate(avg=Avg("ratings__score"), n=Count("ratings"))
                    .filter(n__gt=0)
                    .order_by("-avg", "-n")
                    .first())
        # No ratings anywhere yet? Fall back to the newest report.
        if featured is None:
            featured = base.order_by("-created_at").first()

    stories = base
    if active:
        stories = stories.filter(category__slug=active)
    elif featured is not None:
        stories = stories.exclude(pk=featured.pk)  # don't show it twice
    stories = stories.order_by("?")

    return render(request, "stories/feed.html", {
        "stories": stories,
        "categories": Category.objects.all(),
        "active": active,
        "featured": featured,
    })


def story_detail(request, pk):
    story = get_object_or_404(
        Story.objects.select_related("category").prefetch_related("companions", "drinks"),
        pk=pk, status=Story.Status.APPROVED,
    )
    user_score = None
    if request.session.session_key:
        rating = story.ratings.filter(session_key=request.session.session_key).first()
        if rating:
            user_score = rating.score
    return render(request, "stories/detail.html", {"story": story, "user_score": user_score})


@require_POST
def rate_story(request, pk):
    story = get_object_or_404(Story, pk=pk, status=Story.Status.APPROVED)
    try:
        score = int(request.POST.get("score", ""))
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "Invalid score."}, status=400)
    if not 1 <= score <= 100:
        return JsonResponse({"ok": False, "error": "Out of range."}, status=400)

    if not request.session.session_key:
        request.session.create()

    Rating.objects.update_or_create(
        story=story, session_key=request.session.session_key,
        defaults={"score": score},
    )
    agg = story.ratings.aggregate(avg=Avg("score"), count=Count("id"))
    average = round(agg["avg"]) if agg["avg"] is not None else None
    return JsonResponse({"ok": True, "average": average, "count": agg["count"]})


def spin(request):
    ids = list(Story.objects.filter(status=Story.Status.APPROVED)
               .values_list("id", flat=True))
    if not ids:
        return redirect("stories:feed")
    return redirect("stories:detail", pk=random.choice(ids))


def submit_story(request):
    submitted_drinks = []
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        submitted_drinks = [d.strip() for d in request.POST.getlist("drink") if d.strip()]
        if form.is_valid():
            story = form.save(commit=False)
            story.status = Story.Status.PENDING
            story.save()
            form.save_m2m()
            if not story.drinks_forgotten:
                for name in submitted_drinks:
                    Drink.objects.create(story=story, name=name[:80])
            return redirect("stories:submitted")
    else:
        form = StoryForm()

    exclusive_ids = Companion.objects.filter(is_exclusive=True).values_list("id", flat=True)
    return render(request, "stories/submit.html", {
        "form": form,
        "submitted_drinks": submitted_drinks,
        "exclusive_ids": ",".join(str(i) for i in exclusive_ids),
    })


def submitted(request):
    return render(request, "stories/submitted.html")