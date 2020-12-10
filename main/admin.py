from django.contrib import admin

from main.models.class_portrait import ClassPortrait
from main.models.expansion_set import ExpansionSet
from main.models.card import Card
from main.models.collection_card import CollectionCard


class ExpansionSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'card_count', 'release_date')


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'expansion_set')


class CollectionCardAdmin(admin.ModelAdmin):
    list_display = ('card', 'copies', 'user')


admin.site.register(ExpansionSet, ExpansionSetAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(CollectionCard, CollectionCardAdmin)
admin.site.register(ClassPortrait)
