from collections import defaultdict
from dataclasses import replace
from datetime import date, timedelta
from decimal import Decimal

from babel.dates import format_date

from plannings.dataclasses import PlanningRecipeRead, PlanningRepartition
from recipes.dataclasses import RecipeIngredientRead, RecipeIngredientBase


def build_planning_recipe_reads(
        planning_recipes,
) -> list[PlanningRecipeRead]:
    result: list[PlanningRecipeRead] = []

    for planning_recipe in planning_recipes:
        recipe = planning_recipe.recipe

        recipe_ingredients: list[RecipeIngredientRead] = [
            RecipeIngredientRead(
                recipe_ingredient_base=RecipeIngredientBase(insertion_id=ingredient.insertion_id,
                                                            ref_ingredient_id=ingredient.ingredient_id,
                                                            ref_recipe_id=ingredient.recipe_id,
                                                            quantity=ingredient.quantity),
                recipe_name=recipe.name,
                ingredient_name=(
                    ingredient.ingredient.name
                ),
                ingredient_unit=(
                    ingredient.ingredient
                    .ingredient_unit
                    .symbol
                ),
                estimated_cost_per_unit=(
                        ingredient.quantity
                        * ingredient.ingredient.estimated_price
                ),
            )
            for ingredient in recipe.recipe_ingredients.all()
            if ingredient.state > 0
        ]

        result.append(PlanningRecipeRead(planning_recipe=planning_recipe, recipe=recipe,
                                         estimated_cost_price=planning_recipe.estimated_cost_price,
                                         recipe_ingredients=recipe_ingredients)

                      )

    return result


def redistribute_to_repartition(
        start_of_week: date,
        end_of_week: date,
        recipes: list[PlanningRecipeRead],
) -> list[PlanningRepartition]:
    grouped_data: dict[date, list[PlanningRecipeRead]] = defaultdict(list)

    for recipe in recipes:
        planning_date = recipe.planning_recipe.planning_date
        grouped_data[planning_date].append(recipe)

    repartition_list: list[PlanningRepartition] = []
    current_date = start_of_week

    while current_date <= end_of_week:
        planning_recipes = grouped_data.get(current_date, [])

        repartition_list.append(
            PlanningRepartition(
                planning_group_date=current_date,
                day_name=format_date(
                    current_date,
                    format="EEEE",
                    locale="fr_FR",
                ),
                planning_recipes=planning_recipes,
                estimated_cost_price=get_total_estimated_price(
                    planning_recipes
                )
            )
        )

        current_date += timedelta(days=1)

    return repartition_list


def get_total_estimated_price(
        planning_recipes: list[PlanningRecipeRead],
) -> Decimal:
    return sum(
        (
            recipe.estimated_cost_price
            for recipe in planning_recipes
        ),
        Decimal("0"),
    )


def get_total_estimated_price_from_repartitions(
        planning_repartitions: list[PlanningRepartition],
) -> Decimal:
    return sum(
        (
            repartition.estimated_cost_price
            for repartition in planning_repartitions
        ),
        Decimal("0"),
    )


def get_total_ingredients_to_buy(
        planning_repartitions: list[PlanningRepartition],
) -> list[RecipeIngredientRead]:
    ingredients: dict[str, RecipeIngredientRead] = {}

    for repartition in planning_repartitions:
        for planning_recipe in repartition.planning_recipes:
            servings = planning_recipe.planning_recipe.nb_serving

            for ingredient in planning_recipe.recipe_ingredients:
                ingredient_data = ingredient.recipe_ingredient_base

                ingredient_id = ingredient_data.ref_ingredient_id

                if ingredient_id is None:
                    continue

                total_quantity = (
                        ingredient_data.quantity * servings
                )

                total_estimated_price = (
                        ingredient.estimated_cost_per_unit
                        * servings
                )

                if ingredient_id not in ingredients:

                    aggregated_base = replace(
                        ingredient.recipe_ingredient_base,
                        quantity=total_quantity,
                    )

                    aggregated = replace(
                        ingredient,
                        recipe_ingredient_base=aggregated_base,
                        estimated_cost_per_unit=total_estimated_price,
                    )
                    ingredients[ingredient_id] = aggregated

                else:
                    aggregated = ingredients[ingredient_id]

                    aggregated.recipe_ingredient_base.quantity += total_quantity

                    aggregated.estimated_cost_per_unit += total_estimated_price

    return list(ingredients.values())
