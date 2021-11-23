# timer/forms.py
from django.forms import ModelForm
from timer.models import StoredTimer


class StoredTimerForm(ModelForm):
    class Meta: 
        model = StoredTimer
        fields = '__all__'
