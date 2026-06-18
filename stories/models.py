from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Funny / Weird / Horrific. A model (not just choices) so you can
    tweak the color codes live in the admin without touching code."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    color = models.CharField(
        max_length=7,
        default="#000000",
        help_text="Hex color used to tag this category, e.g. #E8B4B8",
    )
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Companion(models.Model):
    """The 'who were you with' options. Names of real people are NOT allowed —
    these are the only choices a user gets."""
    label = models.CharField(max_length=50, unique=True)
    is_exclusive = models.BooleanField(
        default=False,
        help_text="If true (e.g. 'Alone'), picking this disables all the others.",
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "label"]

    def __str__(self):
        return self.label


class Story(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    # --- Identity ---
    subject = models.CharField(
        max_length=60,
        default="Anonymous",
        help_text="Your alias. We strongly suggest NOT using your real name.",
    )
    mugshot = models.ImageField(
        upload_to="mugshots/", blank=True, null=True,
        help_text="Optional. Max 5MB.",
    )

    # --- Classification ---
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="stories",
    )
    companions = models.ManyToManyField(
        Companion, related_name="stories",
        help_text="Who were you with? One or more (or 'Alone').",
    )

    # --- Drinks ---
    drinks_forgotten = models.BooleanField(
        default=False,
        help_text="Check if the subject genuinely cannot remember what they drank.",
    )

    # --- The confession ---
    story_text = models.TextField()

    # --- The four pre-post meters (1-10) ---
    chaos_level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    memory_of_event = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    regret_level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    lesson_learned = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    # --- Moderation + housekeeping ---
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "stories"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.report_number} - {self.subject}"

    @property
    def report_number(self):
        """Computed, not stored: PD-<year>-<zero-padded id>."""
        if not self.pk:
            return "PD-UNFILED"
        return f"PD-{self.created_at.year}-{self.pk:05d}"

    @property
    def average_bac(self):
        """Community Breathalyzer reading (0-100). Use on single objects only."""
        result = self.ratings.aggregate(avg=models.Avg("score"))["avg"]
        return round(result) if result is not None else None


class Drink(models.Model):
    """One drink per row. A story can have as many as the user adds."""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="drinks")
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Rating(models.Model):
    """A single Breathalyzer reading from a visitor (1-100)."""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["story", "session_key"], name="one_rating_per_session")
        ]

    def __str__(self):
        return f"{self.score} on {self.story.report_number}"