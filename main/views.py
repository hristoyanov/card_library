from django.shortcuts import render, redirect
from main.models.expansion_set import ExpansionSet
from main.models.card import Card
from main.models.collection_card import CollectionCard
from main.models.custom_user import CustomUser
from main.forms import AddCardForm
from main_core.decorators import group_required


# Create your views here.
def index(request):
    return render(request, 'index.html')


def expansion_set_list(request):
    context = {
        'sets': ExpansionSet.objects.order_by('name'),
    }

    return render(request, 'set_list.html', context)


def expansion_card_list(request, pk):
    expansion = ExpansionSet.objects.get(pk=pk)
    cards = expansion.card_set.order_by('hero_class', 'name')

    context = {
        'expansion': expansion,
        'cards': cards,
    }

    return render(request, 'card_list.html', context)


def card_info(request, pk):
    context = {
        'card': Card.objects.get(pk=pk),
    }

    return render(request, 'card_info.html', context)


@group_required(groups=['Regular User'])
def add_card(request, pk):
    card = Card.objects.get(pk=pk)

    if request.method == 'GET':
        form = AddCardForm()

        context = {
            'form': form,
            'card': card,
        }

        return render(request, 'add_card.html', context)
    else:
        form = AddCardForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user']
            copies_to_add = form.cleaned_data['copies_to_add']
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

        return render(request, 'add_card.html', context)


@group_required(groups=['Regular User'])
def custom_user_collection(request, pk):
    user = CustomUser.objects.get(pk=pk)
    cards = user.collectioncard_set.order_by('card__expansion_set__name', 'card__hero_class', 'card__name')

    context = {
        'user': user,
        'cards': cards,
    }

    return render(request, 'user_collection.html', context)
