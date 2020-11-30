from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from main.models.expansion_set import ExpansionSet
from main.models.card import Card
from main.models.collection_card import CollectionCard

from main.forms import ChangeCardCountForm, SelectExpSetForm

from main_core.decorators import group_required
from main_core.reusables import get_next_url, get_card_list, is_collection_complete, get_exp_set_id


def index(request):
    sets = ExpansionSet.objects.order_by('-release_date')[:3]

    return render(request, 'main/index.html', context={'sets': sets})


class ExpansionSetListView(ListView):
    template_name = 'main/set_list.html'
    model = ExpansionSet
    context_object_name = 'sets'
    ordering = ['-release_date']
    paginate_by = 2


class ExpansionSetCardListView(ListView):
    template_name = 'main/card_list.html'
    model = Card
    context_object_name = 'cards'
    paginate_by = 8

    def get_queryset(self):
        exp_set = get_object_or_404(ExpansionSet, pk=self.kwargs.get('pk'))
        cards = exp_set.card_set.order_by('hero_class', 'name')

        return cards


class CardDetailView(DetailView):
    model = Card


@group_required(groups=['Regular User'])
def add_card(request, pk):
    card = Card.objects.get(pk=pk)

    if request.method == 'GET':
        form = ChangeCardCountForm()

        context = {
            'form': form,
            'card': card,
        }

        return render(request, 'main/add_card.html', context)
    else:
        form = ChangeCardCountForm(request.POST)

        if form.is_valid():
            user = request.user
            copies_to_add = form.cleaned_data['count']
            result = user.collectioncard_set.filter(card__name=card.name)

            if result:
                collected_card = result[0]
                collected_card.copies += copies_to_add
                collected_card.save()
            else:
                new_card = CollectionCard(card=card, user=user, copies=copies_to_add)
                new_card.save()

            return redirect(get_next_url(request.POST))

        context = {
            'form': form,
            'card': card,
        }

        return render(request, 'main/add_card.html', context)


@group_required(groups=['Regular User'])
def increase_collected_card_count(request, pk):
    card = request.user.collectioncard_set.get(pk=pk)

    if request.method == 'GET':
        form = ChangeCardCountForm()

        context = {
            'form': form,
            'card': card,
        }

        return render(request, 'main/add_copies.html', context)
    else:
        form = ChangeCardCountForm(request.POST)

        if form.is_valid():
            copies_to_add = form.cleaned_data['count']

            card.copies += copies_to_add
            card.save()

            return redirect(get_next_url(request.POST))

        context = {
            'form': form,
            'card': card,
        }

        return render(request, 'main/add_copies.html', context)


@group_required(groups=['Regular User'])
def remove_collected_card_copies(request, pk):
    card = request.user.collectioncard_set.get(pk=pk)

    if request.method == 'GET':
        form = ChangeCardCountForm()

        context = {
            'form': form,
            'card': card,
        }

        return render(request, 'main/remove_copies.html', context)
    else:
        form = ChangeCardCountForm(request.POST)

        if form.is_valid():
            if card.copies < form.cleaned_data['count']:
                form.add_error('count', 'You can not delete more copies than you already own.')

                context = {
                    'form': form,
                    'card': card,
                }

                return render(request, 'main/remove_copies.html', context)

            copies_to_remove = form.cleaned_data['count']
            card.copies -= copies_to_remove

            if card.copies == 0:
                card.delete()
            else:
                card.save()

            return redirect(get_next_url(request.POST))

        context = {
            'form': form,
            'card': card,
        }

        return render(request, 'main/remove_copies.html', context)


@group_required(groups=['Regular User'])
def delete_collection_card(request, pk):
    card = request.user.collectioncard_set.get(pk=pk)

    if request.method == 'GET':
        context = {
            'card': card,
        }

        return render(request, 'main/delete_user_card.html', context)
    else:
        card.delete()
        return redirect(get_next_url(request.POST))


@group_required(groups=['Regular User'])
def user_collection(request):
    user = request.user
    result = get_exp_set_id(request.GET)

    if not result:
        cards = user.collectioncard_set.order_by('card__expansion_set__name', 'card__hero_class', 'card__name')

        paginator = Paginator(cards, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'form': SelectExpSetForm(),
            'exp_set': '',
            'cards': cards,
            'complete': is_collection_complete(user),
            'total_card_count': Card.objects.all().count(),
            'is_paginated': True,
            'page_obj': page_obj,
        }

        return render(request, 'main/user_collection.html', context)
    else:
        exp_set = ExpansionSet.objects.get(pk=result)
        cards = user.collectioncard_set.filter(card__expansion_set=exp_set).order_by('card__hero_class', 'card__name')

        paginator = Paginator(cards, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'form': SelectExpSetForm(),
            'exp_set': exp_set,
            'cards': cards,
            'complete': is_collection_complete(user, expansion=exp_set),
            'exp_set_card_count': Card.objects.filter(expansion_set=exp_set).count(),
            'is_paginated': True,
            'page_obj': page_obj,
        }

        return render(request, 'main/user_collection.html', context)


@group_required(groups=['Regular User'])
def missing_cards_list(request):
    user = request.user
    result = get_exp_set_id(request.GET)

    if not result:
        missing_cards = get_card_list(user)

        paginator = Paginator(missing_cards, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'form': SelectExpSetForm(),
            'exp_set': '',
            'cards': missing_cards,
            'is_paginated': True,
            'page_obj': page_obj,
        }

        return render(request, 'main/missing_cards.html', context)
    else:
        exp_set = ExpansionSet.objects.get(pk=result)
        missing_cards = get_card_list(user, expansion=exp_set)

        paginator = Paginator(missing_cards, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'form': SelectExpSetForm(),
            'exp_set': exp_set,
            'cards': missing_cards,
            'is_paginated': True,
            'page_obj': page_obj,
        }

        return render(request, 'main/missing_cards.html', context)
