# -*- coding: iso-8859-1 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import SlotTimesGeneration


class SlotTimesGenerationForm(forms.ModelForm):

    class Meta:
        model = SlotTimesGeneration

    def clean(self):
        cleaned_data = super(SlotTimesGenerationForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(_("'end date' field must be greater"
                                          " than 'start_date' field."))
        return cleaned_data