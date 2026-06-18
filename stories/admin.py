from django.contrib import admin
from .models import Category, Companion, Story, Drink, Rating


class DrinkInline(admin.TabularInline):
    model = Drink
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Companion)
class CompanionAdmin(admin.ModelAdmin):
    list_display = ("label", "is_exclusive", "order")
    list_editable = ("order",)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("report_number", "subject", "category", "status", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("subject", "story_text")
    list_editable = ("status",)
    inlines = [DrinkInline]
    filter_horizontal = ("companions",)
    readonly_fields = ("created_at", "updated_at")
    actions = ["approve_stories", "reject_stories"]

    @admin.action(description="Approve selected stories (send to print)")
    def approve_stories(self, request, queryset):
        updated = queryset.update(status=Story.Status.APPROVED)
        self.message_user(request, f"{updated} story(s) sent to print.")

    @admin.action(description="Reject selected stories (spike them)")
    def reject_stories(self, request, queryset):
        updated = queryset.update(status=Story.Status.REJECTED)
        self.message_user(request, f"{updated} story(s) spiked.")


admin.site.register(Rating)