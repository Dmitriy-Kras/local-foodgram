from django.contrib import admin
from django.contrib.auth.models import Group

from .forms import AtLeastOneFormSet
from .models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag

admin.site.unregister(Group)


class IngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    formset = AtLeastOneFormSet


class FavoriteInLine(admin.TabularInline):
    model = Favorite


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite')
    readonly_fields = ('favorite',)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', '^author__username')
    fields = (
        ('name', 'author'),
        'favorite',
        'text', 'tags',
        'cooking_time',
        'image'
    )
    inlines = (IngredientInLine, FavoriteInLine)

    def favorite(self, obj):
        count = obj.following.count()
        return f'{count} в избранном'

    favorite.short_description = 'Кол-во в избранном'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    list_filter = ('name',)
    search_fields = ('^name',)
    fields = (('name', 'measurement_unit'),)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (('name', 'id'))
