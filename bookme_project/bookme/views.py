from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import BookingType
from .forms import SlotTimeForm


class HomeView(TemplateView):
    template_name = 'bookme/home.html'


class BookingTypeListView(ListView):
    model = BookingType
    # template_name = 'bookme/home.html'


def slottime_add(request):
    return render(request, 'bookme/slottime_create.html',
                  {'form': SlotTimeForm()})