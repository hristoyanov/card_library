from django.contrib import admin
from main.models.expansion_set import ExpansionSet
from main.models.card import Card
from main.models.collection_card import CollectionCard
from main.models.custom_user import CustomUser

# Register your models here.
admin.site.register(ExpansionSet)
admin.site.register(Card)
admin.site.register(CollectionCard)
admin.site.register(CustomUser)
