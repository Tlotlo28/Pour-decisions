from django.db import migrations


def seed(apps, schema_editor):
    Category = apps.get_model("stories", "Category")
    Companion = apps.get_model("stories", "Companion")

    categories = [
        ("Funny", "funny", "#E8B4B8", "You will laugh. Probably at yourself."),
        ("Weird", "weird", "#6B5B95", "Unexplained. Unhinged. Unforgettable."),
        ("Horrific", "horrific", "#8B1A1A", "Read with the lights on."),
    ]
    for name, slug, color, desc in categories:
        Category.objects.get_or_create(
            slug=slug,
            defaults={"name": name, "color": color, "description": desc},
        )

    companions = [
        ("Alone", True, 0),
        ("Family", False, 1),
        ("Friends", False, 2),
        ("Co-workers", False, 3),
        ("It's complicated", False, 4),
        ("Other", False, 5),
    ]
    for label, exclusive, order in companions:
        Companion.objects.get_or_create(
            label=label, defaults={"is_exclusive": exclusive, "order": order},
        )


def unseed(apps, schema_editor):
    apps.get_model("stories", "Category").objects.all().delete()
    apps.get_model("stories", "Companion").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("stories", "0001_initial"),
    ]
    operations = [
        migrations.RunPython(seed, unseed),
    ]