from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import SubscribeSerializer
from api.utils import CustomPaginator


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPaginator

    @action(detail=False)
    def subscriptions(self, request):
        authors_ids = request.user.subscriber.all().values_list(
            'author', flat=True)
        authors = User.objects.filter(id__in=authors_ids)
        page = self.paginate_queryset(authors)
        serializer = SubscribeSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if author != request.user:
                try:
                    Subscription.objects.create(
                        author=author,
                        user=request.user
                    )
                    serializer = SubscribeSerializer(author)
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response(
                        {'Ошибка, подписка уже существует'},
                        status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {'Ошибка, нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST)
        obj = Subscription.objects.filter(user=request.user, author=author)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'Ошибка удаления, подписки не существует'},
            status=status.HTTP_400_BAD_REQUEST)
