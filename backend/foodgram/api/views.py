from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .permissions import AdminOwnerOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from .utils import CustomPaginator
from recipes.models import Favorite, Ingredient, Recipe, Tag
from users.serializers import MiniRecipeSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPaginator
    permission_classes = (AdminOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {'Ошибка: рецепт с таким названием уже существует'},
                status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            tags=self.request.data.get('tags'),
            ingredients=self.request.data.get('ingredients')
        )

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
            tags=self.request.data.get('tags'),
            ingredients=self.request.data.get('ingredients')
        )

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            try:
                Favorite.objects.create(user=request.user, recipe=recipe)
                serializer = MiniRecipeSerializer(recipe)
            except IntegrityError:
                return Response(
                    {'Ошибка добавления, рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'Ошибка удаления, рецепт не в избранном'},
            status=status.HTTP_400_BAD_REQUEST)
