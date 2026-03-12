import datetime
from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Track

FORBIDDEN_WORDS = {'спам', 'запрещено', 'test'}


def validate_no_forbidden_words(value):
    lowered = value.lower()
    for word in FORBIDDEN_WORDS:
        if word in lowered:
            raise ValidationError('Название содержит запрещённые слова.')


class TrackSuggestionForm(forms.Form):
    track_title = forms.CharField(
        label='Название трека',
        max_length=150,
        validators=[validate_no_forbidden_words],
    )
    email = forms.EmailField(label='Ваша почта')
    comment = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea,
        required=False,
        max_length=500,
    )


class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = [
            'title',
            'slug',
            'genre',
            'tags',
            'duration',
            'release_year',
            'play_count',
            'is_published',
            'image',
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }

    def clean_release_year(self):
        year = self.cleaned_data['release_year']
        current_year = datetime.date.today().year
        if year < 1900 or year > current_year:
            raise ValidationError('Год выпуска должен быть в разумных пределах.')
        return year

    def clean_duration(self):
        duration = self.cleaned_data['duration']
        if duration < 30:
            raise ValidationError('Длительность трека должна быть больше 30 секунд.')
        return duration


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Комментарий'}
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Поделитесь впечатлением...'}),
        }

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if not text:
            raise ValidationError('Комментарий не может быть пустым.')
        return text
