from django.shortcuts import render
from main.models import ExpansionSet


# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def expansion_set_list(request):
    context = {
        'sets': ExpansionSet.objects.all(),
    }

    return render(request, 'set_list.html', context)


def expansion_card_list(request, pk):
    expansion = ExpansionSet.objects.get(pk=pk)
    cards = expansion.card_set.all()

    context = {
        'expansion': expansion,
        'cards': cards,
    }

    return render(request, 'card_list.html', context)
