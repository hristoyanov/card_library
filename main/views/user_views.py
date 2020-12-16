from django.shortcuts import render, redirect

from main.forms import ChangeCardCountForm, SelectExpSetForm
from main.models.card import Card
from main.models.collection_card import CollectionCard
from main.models.expansion_set import ExpansionSet
from main_core.decorators import group_required
from main_core.reusables import get_next_url, get_exp_set_id, is_collection_complete, get_card_list


@group_required(groups=['Regular User'])
def add_card(request, pk):
    """Adds a card to the currently logged-in user's collection.

    Returns:
        If the request method is GET:
            renders a form for selecting the amount of copies to be added.

        If the request method is POST:
            If the user already has the card in their collection, increases the copies owned with the amount
            selected in the form and saves the card.

            If the user does not have the card in their collection, creates a new CollectionCard object and sets its
            'copies' attribute value to the one selected in the form.
    """

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
    """Adds extra copies of an already collected card.

    Returns:
        If the request method is GET:
            renders a form for selecting the amount of copies to be added.

        If the request method is POST:
            Increases the value of the card's 'copies' attribute with the amount selected in the form.
    """

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
    """Removes number of copies of an already collected card.

    Returns:
        If the request method is GET:
            renders a form for selecting the amount of copies to be removed.

        If the request method is POST:
            Checks if the amount of copies selected in the form is greater than the owned copies of the card and if it
            is, renders the form again with an error message.

            If the form is valid, reduces copies owned with the amount selected and saves the card.

            If the values are equal (for example: copies owned are 2 and selected amount is 2), deletes the card from
            the user's collection.
    """

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

            return redirect('user_collection')

        context = {
            'form': form,
            'card': card,
        }

        return render(request, 'main/remove_copies.html', context)


@group_required(groups=['Regular User'])
def delete_collection_card(request, pk):
    """Deletes a card from the user's collection."""

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
    """Renders a view either of a user's entire collection or filtered by expansion set.

    For a card to be considered 'collected', the user must have at least 2 copies of it.
    """

    user = request.user
    result = get_exp_set_id(request.GET)

    if not result:
        cards = user.collectioncard_set.order_by('card__expansion_set__name', '-card__hero_class', 'card__mana_cost')

        context = {
            'form': SelectExpSetForm(),
            'exp_set': '',
            'cards': cards,
            'complete': is_collection_complete(user),
            'total_card_count': Card.objects.all().count(),
        }

        return render(request, 'main/user_collection.html', context)
    else:
        exp_set = ExpansionSet.objects.get(pk=result)
        cards = user.collectioncard_set.filter(card__expansion_set=exp_set).order_by('-card__hero_class',
                                                                                     'card__mana_cost')

        context = {
            'form': SelectExpSetForm(initial={'expansion_set': result}),
            'exp_set': exp_set,
            'cards': cards,
            'complete': is_collection_complete(user, expansion=exp_set),
            'exp_set_card_count': exp_set.card_count,
        }

        return render(request, 'main/user_collection.html', context)


@group_required(groups=['Regular User'])
def missing_cards_list(request):
    """Renders a view of all the user's missing cards, or only ones from a specific expansion set.

    Includes cards that the user doesn't have at all as well as ones with less than 2 copies owned.
    """

    user = request.user
    result = get_exp_set_id(request.GET)

    if not result:
        missing_cards = get_card_list(user)

        context = {
            'form': SelectExpSetForm(),
            'exp_set': '',
            'cards': missing_cards,
        }

        return render(request, 'main/missing_cards.html', context)
    else:
        exp_set = ExpansionSet.objects.get(pk=result)
        missing_cards = get_card_list(user, expansion=exp_set)

        context = {
            'form': SelectExpSetForm(initial={'expansion_set': result}),
            'exp_set': exp_set,
            'cards': missing_cards,
        }

        return render(request, 'main/missing_cards.html', context)
