import io

from django.conf import settings
from django.db.models import Sum
from django.db.utils import IntegrityError
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.response import Response

from recipes.models import Basket, Recipe, RecipeIngredient
from users.serializers import MiniRecipeSerializer


class BasketViewSet(viewsets.ViewSet):

    def to_basket(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        try:
            Basket.objects.create(user=request.user, recipe=recipe)
            serializer = MiniRecipeSerializer(recipe)
        except IntegrityError:
            return Response(
                {'Ошибка добавления, рецепт уже в корзине'},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def from_basket(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        obj = Basket.objects.filter(user=request.user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'Ошибка удаления, рецепт не в корзине'},
            status=status.HTTP_400_BAD_REQUEST)

    def get_shop_list_old(self, request):
        pdf = io.BytesIO()
        gen_pdf = canvas.Canvas(pdf)
        pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount')).order_by()

        gen_pdf.setFont('Calibri', 20)
        gen_pdf.drawString(200, 800, 'Список покупок:')
        hight_position = 760
        gen_pdf.setFont('Calibri', 14)
        for ingredient in ingredients:
            gen_pdf.drawString(
                100,
                hight_position,
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}.'
            )
            hight_position -= 20

        gen_pdf.showPage()
        gen_pdf.save()
        pdf.seek(0)

        return FileResponse(pdf, as_attachment=True, filename='shop-list.pdf')

    def get_shop_list(self, request):
        path_to_font = str(settings.BASE_DIR) + '/library/calibri.ttf'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shop_list.pdf"')
        pdfmetrics.registerFont(TTFont('dej', path_to_font))
        p = canvas.Canvas(response)

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount')).order_by()

        p.setFont('dej', 20)
        p.drawString(200, 800, 'Список покупок:')
        p.setFont('dej', 14)
        hight_position = 760
        for ingredient in ingredients:
            p.drawString(
                100,
                hight_position,
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}.'
            )
            hight_position -= 20
        p.showPage()
        p.save()
        return response
