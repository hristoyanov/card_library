from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from main.models.card import Card
from main.models.expansion_set import ExpansionSet


def index(request):
    """Renders the landing page with the 3 most recently released expansion sets."""

    sets = ExpansionSet.objects.order_by('-release_date')[:3]

    return render(request, 'main/index.html', context={'sets': sets})


class ExpansionSetListView(ListView):
    """Renders a list view with all expansion sets in the database, 2 per page, starting with the most recent one."""

    template_name = 'main/set_list.html'
    model = ExpansionSet
    context_object_name = 'sets'
    ordering = ['-release_date']
    paginate_by = 2


class ExpansionSetCardListView(ListView):
    """Renders a list view with all cards in an expansion set with 8 cards per page.

    Cards are ordered by hero class and then by name.
    """

    template_name = 'main/card_list.html'
    model = Card
    context_object_name = 'cards'
    paginate_by = 8

    def get_queryset(self):
        exp_set = get_object_or_404(ExpansionSet, pk=self.kwargs.get('pk'))
        cards = exp_set.card_set.order_by('hero_class', 'name')

        return cards


class CardDetailView(DetailView):
    """Renders a detailed look of a specific card."""

    model = Card
