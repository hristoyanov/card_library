from django.core.paginator import Paginator

from main.models.card import Card


def get_next_url(params):
    """Tells a view where to redirect to after an action has been made."""

    next_url = params.get('next', '/')
    return next_url if next_url else 'index'


def get_exp_set_id(params):
    """Returns the id of an expansion set selected in a form or returns None if no set has been selected."""

    exp_set_id = params['expansion_set'] if 'expansion_set' in params else None

    if exp_set_id:
        return int(exp_set_id)
    return exp_set_id


def custom_paginator(request, cards, cards_per_page=8):
    """Paginates a view with a default of 8 objects per page."""

    paginator = Paginator(cards, cards_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def get_card_list(user, expansion=None):
    """Returns a collection of the user's missing cards.

    Args:
        user: the currently logged-in user.
        expansion: an ExpansionSet model object.

    Returns:
        If no expansion has been passed:
            First it gets the ids of all user collected cards with 'copies' attribute value greater or equal than 2 -
            (you can use a maximum of 2 copies of a card in a deck, and having 2 copies of a card in your collection
            means that you have collected it). This only applies to cards with rarities other than legendary.

            Then it gets the ids of all user collected LEGENDARY cards without checking the value of the 'copies'
            attribute as you can only have 1 copy of a legendary card in a deck.

            It combines the two collections together using .union method.

            It goes over all Card model objects in the database that are NOT in the collection, orders them and finally
            returns them.

        If an expansion has been passed:
            Follows the exact same steps as above, only for cards from the selected expansion.

    """

    if not expansion:
        user_card_ids = user.collectioncard_set \
            .filter(copies__gte=2) \
            .values_list('card_id', flat=True)

        user_legendary_card_ids = user.collectioncard_set \
            .filter(card__rarity='legendary') \
            .values_list('card_id', flat=True)

        all_user_card_ids = user_card_ids.union(user_legendary_card_ids)

        missing_cards = Card.objects \
            .exclude(id__in=all_user_card_ids) \
            .order_by('hero_class', 'name')

        return missing_cards

    user_set_cards = user.collectioncard_set.filter(card__expansion_set=expansion)
    user_card_ids = user_set_cards \
        .filter(copies__gte=2) \
        .values_list('card_id', flat=True)

    user_legendary_card_ids = user_set_cards \
        .filter(card__rarity='legendary') \
        .values_list('card_id', flat=True)

    all_user_card_ids = user_card_ids.union(user_legendary_card_ids)

    missing_cards = Card.objects \
        .filter(expansion_set=expansion) \
        .exclude(id__in=all_user_card_ids) \
        .order_by('hero_class', 'name')

    return missing_cards


def is_collection_complete(user, expansion=None):
    """Checks if a user collection is complete.

    Args:
        user: the currently logged-in user.
        expansion: an ExpansionSet model object.

    Returns:
        If no expansion has been passed:
            Goes through all cards in the user's collection 'copies' attribute value of at least 2, excluding legendary
            cards.
            Asserts if the count of those cards is equal to the count of all Card objects in the database, excluding
            legendary cards.

            Next, it does the exact same thing for LEGENDARY cards, without checking the values of 'copies' and asserts
            if their count is equal to the count of all legendary cards.

            If both return True, it means that a user's collection is complete and the function returns True.

        If an expansion has been passed:
            Does the exact same thing for cards ONLY from the selected expansion.

    """

    if not expansion:
        non_legendary_cards_complete = user.collectioncard_set \
                                           .exclude(card__rarity='legendary') \
                                           .filter(copies__gte=2) \
                                           .count() == Card.objects.exclude(rarity='legendary').count()

        legendary_cards_complete = user.collectioncard_set \
                                       .filter(card__rarity='legendary') \
                                       .count() == Card.objects.filter(rarity='legendary').count()

        return non_legendary_cards_complete and legendary_cards_complete

    non_legendary_cards_complete = user.collectioncard_set \
                                       .filter(card__expansion_set=expansion) \
                                       .exclude(card__rarity='legendary') \
                                       .filter(copies__gte=2) \
                                       .count() == Card.objects \
                                       .filter(expansion_set=expansion) \
                                       .exclude(rarity='legendary').count()

    legendary_cards_complete = user.collectioncard_set \
                                   .filter(card__expansion_set=expansion) \
                                   .filter(card__rarity='legendary') \
                                   .count() == Card.objects \
                                   .filter(expansion_set=expansion) \
                                   .filter(rarity='legendary') \
                                   .count()

    return non_legendary_cards_complete and legendary_cards_complete
