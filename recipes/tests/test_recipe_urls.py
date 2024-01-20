from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class RecipeURLsTest(TestCase):
    def test_recipes_home_url_is_correct(self):
        home_url = reverse("recipes:home")
        self.assertEqual(home_url, "/")

    def test_recipes_category_url_is_correct(self):
        url = reverse("recipes:category", kwargs={"category_id": 1})
        self.assertEqual(url, "/recipes/category/1/")

    def test_recipes_detail_url_is_correct(self):
        url = reverse("recipes:recipe", kwargs={"pk": 1})
        self.assertEqual(url, "/recipes/1/")

    def test_recipe_search_url_is_correct(self):
        url = reverse("recipes:search")
        self.assertEqual(url, "/recipes/search/")

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse("recipes:search") + "?q=teste")
        self.assertTemplateUsed(response, "recipes/pages/search.html")
