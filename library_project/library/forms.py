from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model  = Book
        fields = ['title', 'author', 'category', 'description', 'cover', 'year', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year is not None and (year < 0 or year > 2026):
            raise forms.ValidationError('Year must be between 0 and 2026.')
        return year

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Title cannot be empty.')
        return title
