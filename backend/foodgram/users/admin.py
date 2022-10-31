from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Subscription, User
from recipes.models import Basket


class BasketInLine(admin.TabularInline):
    model = Basket
    fk_name = 'user'
    verbose_name = "рецепт в корзину"


class SubscriptionInLine(admin.TabularInline):
    model = Subscription
    fk_name = 'user'
    verbose_name_plural = 'Подписка на авторов'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'first_name')
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff'
    )
    fieldsets = (
        (_('Personal info'), {
            'fields': (
                'username',
                'first_name',
                'last_name',
                'email',
                'password'
            )
        }),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'user_permissions'
            )
        })
    )
    inlines = (BasketInLine, SubscriptionInLine)
