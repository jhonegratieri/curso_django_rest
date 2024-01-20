from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class CategoryModelsTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()

    def test_category_string_representation_is_name_fields(self):
        needed = 'Testing representacion category'
        self.category.name = needed
        self.category.full_clean()
        self.category.save()
        self.assertEqual(needed, self.category.__str__())

    def test_recipe_category_model_name_max_lenght_is_65_chars(self):
        self.category.name = 'a' * 70

        with self.assertRaises(ValidationError):
            self.category.full_clean()
