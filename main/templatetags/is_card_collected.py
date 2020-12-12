from django import template

register = template.Library()


@register.simple_tag
def is_card_collected(user, card):
    result = user.collectioncard_set.filter(card=card)

    if result:
        return f'Copies owned: {result[0].copies}'
    return f'Copies owned: 0'
