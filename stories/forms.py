from django import forms
from .models import Story, Drink
from .validators import validate_mugshot_size

METER_FIELDS = ["chaos_level", "memory_of_event", "regret_level", "lesson_learned"]


class StoryForm(forms.ModelForm):
    # NOT a Story field - we parse this into Drink rows in the view.
    consent = forms.BooleanField(
        required=True,
        error_messages={"required": "You must agree to the House Rules to file a report."},
    )  

    class Meta:
        model = Story
        fields = [
            "subject", "mugshot", "category", "companions",
            "drinks_forgotten", "story_text",
            "chaos_level", "memory_of_event", "regret_level", "lesson_learned",
        ]
        widgets = {
            "companions": forms.CheckboxSelectMultiple,
            "story_text": forms.Textarea(attrs={"rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].initial = "Anonymous"
        self.fields["category"].empty_label = "-- Select one (required) --"
        # Turn the four meters into range sliders (we'll prettify in Part 2).
        for name in METER_FIELDS:
            self.fields[name].widget = forms.NumberInput(
                attrs={"type": "range", "min": 1, "max": 10, "step": 1})
            self.fields[name].initial = 5

    def clean_mugshot(self):
        image = self.cleaned_data.get("mugshot")
        validate_mugshot_size(image)
        return image

    def clean(self):
        cleaned = super().clean()
        companions = cleaned.get("companions")
        if companions:
            exclusive = [c for c in companions if c.is_exclusive]
            if exclusive and len(companions) > 1:
                self.add_error("companions",
                    f"You picked '{exclusive[0].label}' - that means it was just you. "
                    f"You can't also be with other people. Pick a lane.")
        return cleaned