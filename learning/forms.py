from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 Bintang'),
        (2, '2 Bintang'),
        (3, '3 Bintang'),
        (4, '4 Bintang'),
        (5, '5 Bintang'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label="Rating"
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label="Komentar",
        required=False
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']