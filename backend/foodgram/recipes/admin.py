from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Basket, Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class IngredientInLine(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    readonly_fields = ('liked',)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', '^author__username')
    fields = (
        ('name', 'author', 'liked'),
        ('text', 'tags'),
        'cooking_time',
        'image'
    )
    inlines = (IngredientInLine,)

    def liked(self, obj):
        count = obj.following.count()
        url = reverse('admin:recipes_favorite_changelist')
        return format_html('<a href="{}">{} в избранном</a>', url, count)

    liked.short_description = 'Кол-во в избранном'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    list_filter = ('name',)
    search_fields = ('^name',)
    fields = (('name', 'measurement_unit'),)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (('name', 'id'))


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
