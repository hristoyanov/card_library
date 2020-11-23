from main.models.card import Card


def get_next_url(params):
    next_url = params.get('next', '/')
    return next_url if next_url else 'index'


def get_card_list(user, expansion=None):
    if not expansion:
        user_card_ids = user.collectioncard_set.all().values_list('card_id', flat=True)
        missing_cards = Card.objects \
            .exclude(id__in=user_card_ids) \
            .order_by('expansion_set__name', 'hero_class', 'name')

        return missing_cards

    user_set_cards = user.collectioncard_set.filter(card__expansion_set=expansion)
    user_card_ids = user_set_cards.values_list('card_id', flat=True)
    missing_cards = Card.objects\
        .filter(expansion_set=expansion)\
        .exclude(id__in=user_card_ids)\
        .order_by('hero_class', 'name')

    return missing_cards
