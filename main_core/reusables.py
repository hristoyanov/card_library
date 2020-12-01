from main.models.card import Card


def get_next_url(params):
    next_url = params.get('next', '/')
    return next_url if next_url else 'index'


def get_exp_set_id(params):
    exp_set_id = params['expansion_set'] if 'expansion_set' in params else None

    if exp_set_id:
        return int(exp_set_id)
    return exp_set_id


def get_card_list(user, expansion=None):
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
            .order_by('expansion_set__name', 'hero_class', 'name')

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
