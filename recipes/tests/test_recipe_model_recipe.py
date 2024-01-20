from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelsTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self, *args, **kwargs):
        recipe = Recipe(
            category=self.make_category(name="Test Default Category"),
            author=self.make_author(username="newuser"),
            title=kwargs.get("title", "Recipe Title"),
            description="Recipe Description",
            slug=kwargs.get("slug", "slug"),
            preparation_time=10,
            preparation_time_unit="Minutos",
            servings=5,
            servings_unit="Porções",
            preparation_steps="Recipe Preparation Steps",
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_title_raises_error_if_title_was_more_than_65_chars(self):
        self.recipe.title = "A" * 70

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand(
        [
            ("title", 65),
            ("description", 165),
            ("preparation_time_unit", 65),
            ("servings_unit", 65),
        ]
    )
    def test_recipe_fields_max_lenght(self, field, max_lenght):
        setattr(self.recipe, field, "A" * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults(slug="abc-12a", title="abc 12a")
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg="Recipe preparation_steps_is_html is not False",
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults(slug="abc-12b", title="abc 12b")
        self.assertFalse(
            recipe.is_published,
            msg="Recipe is_published is not False",
        )

    def test_recipe_string_representation(self):
        self.recipe.title = "Testing representacion"
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual("Testing representacion", self.recipe.__str__())
