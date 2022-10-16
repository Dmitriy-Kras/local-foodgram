from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .basket import BasketViewSet
from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        BasketViewSet.as_view({'get': 'get_shop_list'})
    ),
    path(
        'recipes/<int:pk>/shopping_cart/',
        BasketViewSet.as_view({'post': 'to_basket', 'delete': 'from_basket'})
    ),
    path('', include(router.urls))
]
