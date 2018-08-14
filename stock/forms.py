# -*- coding: utf-8 -*-
from django import forms
from .models import StockSection, SectionInfo, StockWatchList


class StockSectionForm(forms.ModelForm):
    class Meta:
        model = StockSection
        fields = ("sectionName", "stockId", "stockName")


class SectionInfoForm(forms.ModelForm):
    class Meta:
        model = SectionInfo
        fields = ("sectionName", "sectionId")

class StockWatchListForm(forms.ModelForm):
    class Meta:
        model = StockWatchList
        fields = ("stockId", "stockName", "priority")    