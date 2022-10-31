from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):

    help = 'Load data from .csv files'

    def handle(self, *args, **kwds):
        err_msg = 'Возникла ошибка загрузки'
        print('Loading data from .csv file')

        try:
            for row in DictReader(
                open('./data/ingredients.csv', encoding="utf-8")
            ):
                if Ingredient.objects.filter(name=row['name']).exists():
                    continue
                ingredient = Ingredient(
                    name=row['name'], measurement_unit=row['unit'])
                ingredient.save()
        except Exception as error:
            print(f'{err_msg} ингредиентов - {error}')
        else:
            print('ingredients.csv uploaded')

        try:
            for row in DictReader(
                open('./data/tags.csv', encoding="utf-8")
            ):
                tag = Tag(
                    name=row['name'], color=row['color'], slug=row['slug'])
                tag.save()
        except Exception as error:
            print(f'{err_msg} тегов - {error}')
        else:
            print('tags.csv uploaded')
