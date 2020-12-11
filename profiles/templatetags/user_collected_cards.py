from django import template

register = template.Library()


@register.simple_tag
def user_collected_cards(user, card):
    exp_set = card.card.expansion_set
    user_card_count = user.collectioncard_set.filter(card__expansion_set=exp_set).count()
    exp_set_card_count = exp_set.card_count

    return f'{user_card_count}/{exp_set_card_count} cards collected'
