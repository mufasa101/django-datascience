from django import forms
CHART_CHOICES=(
    ('bar','Bar chart'),
    ('pie','Pie chart'),
    ('line','Line chart'),
)
GROUP_CHOICES=(
    ('date','date'),
    ('transactions','Transactions'),
)
class SearchForm(forms.Form):
    date_from=forms.DateField(, required=True)
    date_to=forms.DateField(, required=True)
    chart_type=forms.ChoiceField(, choices=[CHART_CHOICES], required=True)
    group_type=forms.ChoiceField(, choices=[GROUP_CHOICES], required=True)
    
    