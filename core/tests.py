from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import FoodCategory, Food


class FoodApiTests(APITestCase):
    def setUp(self):
        self.cat_published = FoodCategory.objects.create(name_ru="Напитки", order_id=10)
        self.food1 = Food.objects.create(
            category=self.cat_published,
            name_ru="Чай",
            code=1,
            internal_code=100,
            cost=100,
            is_publish=True
        )

        self.food_hidden = Food.objects.create(
            category=self.cat_published,
            name_ru="Скрытый напиток",
            code=2,
            internal_code=200,
            cost=100,
            is_publish=False
        )

        self.cat_hidden = FoodCategory.objects.create(name_ru="Выпечка", order_id=20)
        Food.objects.create(
            category=self.cat_hidden,
            name_ru="Скрытая булка",
            code=3,
            internal_code=300,
            cost=50,
            is_publish=False
        )

        self.cat_empty = FoodCategory.objects.create(name_ru="Пустая", order_id=30)

        self.url = reverse('food-list')

    def test_get_foods_list__valid_request__returns_200_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_foods_list__mixed_published_and_hidden_data__returns_only_published_foods_and_non_empty_categories(self):
        response = self.client.get(self.url)
        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name_ru'], "Напитки")

        foods = data[0]['foods']
        self.assertEqual(len(foods), 1)
        self.assertEqual(foods[0]['name_ru'], "Чай")
        self.assertEqual(foods[0]['internal_code'], 100)

    def test_get_foods_list__food_with_additional_items__returns_internal_codes_in_additional_field(self):
        self.food1.additional.add(self.food1)

        response = self.client.get(self.url)
        data = response.json()

        self.assertIn(100, data[0]['foods'][0]['additional'])

    def test_get_foods_list__no_published_foods_exist__returns_empty_list(self):
        Food.objects.all().update(is_publish=False)
        response = self.client.get(self.url)
        self.assertEqual(len(response.json()), 0)
