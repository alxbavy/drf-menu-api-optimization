from django.db.models import Prefetch
from rest_framework.generics import ListAPIView

from .models import FoodCategory, Food, FoodListSerializer


class FoodListView(ListAPIView):
    serializer_class = FoodListSerializer

    def get_queryset(self):
        prefetch_published_foods = Prefetch(
            'food',
            queryset=Food.objects.filter(is_publish=True)
        )

        queryset = FoodCategory.objects.filter(
            food__is_publish=True
        ).prefetch_related(
            prefetch_published_foods
        ).distinct()

        return queryset
