# from django.test import TestCase
from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn(
            "No recipes found here.",
            response.content.decode("utf-8"),
        )

        # self.fail('') gera uma falha no teste
        # self.fail('Para que eu termine de digitá-lo')

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse("recipes:home"))
        response_context_recipes = response.context["recipes"]
        content = response.content.decode("utf-8")

        self.assertIn("recipe title", content)
        self.assertIn("10 min", content)
        self.assertIn("5 portions", content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False don't show"""
        self.make_recipe(is_published=False)

        response = self.client.get(reverse("recipes:home"))

        self.assertIn(
            "No recipes found here.",
            response.content.decode("utf-8"),
        )

    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch(qty=8)

        with patch("recipes.views.site.PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:home"))
            recipes = response.context["recipes"]
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(qty=8)

        with patch("recipes.views.site.PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:home") + "?page=12A")
            self.assertEqual(response.context["recipes"].number, 1)
            response = self.client.get(reverse("recipes:home") + "?page=2")
            self.assertEqual(response.context["recipes"].number, 2)
            response = self.client.get(reverse("recipes:home") + "?page=3")
            self.assertEqual(response.context["recipes"].number, 3)
