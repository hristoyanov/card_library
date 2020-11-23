from django.shortcuts import render, redirect
from main.models.expansion_set import ExpansionSet
from main.models.card import Card
from main.models.collection_card import CollectionCard
from main.forms import ChangeCardCountForm, SelectExpSetForm
from main_core.decorators import group_required


# Create your views here.
from main_core.reusables import get_card_list


def index(request):
    sets = ExpansionSet.objects.order_by('-release_date')[:3]

    return render(request, 'main/index.html', context={'sets': sets})


def expansion_set_list(request):
    context = {
        'sets': ExpansionSet.objects.order_by('-release_date'),
    }

    return render(request, 'main/set_list.html', context)


def expansion_card_list(request, pk):
    expansion = ExpansionSet.objects.get(pk=pk)
    cards = expansion.card_set.order_by('hero_class', 'name')

    context = {
        'expansion': expansion,
        'cards': cards,
    }

    return render(request, 'main/card_list.html', context)


def card_info(request, pk):
    context = {
        'card': Card.objects.get(pk=pk),
    }

    return render(request, 'main/card_info.html', context)


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

            return redirect('card_list', card.expansion_set.id)

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

            return redirect('user_collection')

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

            return redirect('user_collection')

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
        return redirect('user_collection')


@group_required(groups=['Regular User'])
def user_collection(request):
    user = request.user

    if request.method == 'GET':
        context = {
            'form': SelectExpSetForm(),
            'cards': user.collectioncard_set.order_by('card__expansion_set__name', 'card__hero_class', 'card__name'),
        }

        return render(request, 'main/user_collection.html', context)
    else:
        form = SelectExpSetForm(request.POST)

        if form.is_valid():
            exp_set = form.cleaned_data['expansion_set']
            cards = user.collectioncard_set.filter(card__expansion_set=exp_set)

            context = {
                'exp_set': exp_set,
                'cards': cards,
            }

            return render(request, 'main/exp_set_collection.html', context)

        return render(request, 'main/user_collection.html', context={'form': form})


@group_required(groups=['Regular User'])
def missing_cards_list(request):
    user = request.user

    if request.method == 'GET':
        missing_cards = get_card_list(user)

        context = {
            'form': SelectExpSetForm(),
            'cards': missing_cards,
        }

        return render(request, 'main/missing_cards.html', context)
    else:
        form = SelectExpSetForm(request.POST)

        if form.is_valid():
            exp_set = form.cleaned_data['expansion_set']
            missing_cards = get_card_list(user, expansion=exp_set)

            context = {
                'exp_set': exp_set,
                'cards': missing_cards,
            }

            return render(request, 'main/missing_cards_per_set.html', context)

        return render(request, 'main/missing_cards.html', context={'form': form})
