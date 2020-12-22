# With help from Joel Grus

from typing import List, NamedTuple, Set, Dict
"""
Each food has an ingredients list
Each ingredient contains allergens
Each allergen is in exactly one ingredient
Each ingredient have zero or one allergen
Allergens aren't always marked
"""

TEST_RAW = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


class Food(NamedTuple):
    ingredients: List[str]
    allergens: List[str]

    @staticmethod
    def parse(line: str) -> 'Food':
        parts = line.split(' (contains ')
        # )
        if len(parts) == 1:
            ingredients = line.split(' ')
            allergens = []
        else:
            ingredients = parts[0].split(' ')
            allergens = parts[1][:-1].split(', ')
        return Food(ingredients, allergens)


class Foods:
    def __init__(self, raw: str) -> None:
        self.foods: List[Food] = [Food.parse(line) for line in raw.splitlines()]

    def get_allergic_candidates(self) -> Dict[str, Set[str]]:
        # for each allergen what could its ingredients be
        candidates: Dict[str, Set[str]] = {}

        for food in self.foods:
            for allergen in food.allergens:
                if allergen not in candidates:
                    candidates[allergen] = set(food.ingredients)
                else:
                    candidates[allergen] = candidates[allergen] & set(food.ingredients)
        return candidates

    def get_non_allergic_ingredients(self) -> List[str]:
        # allergens = {allergen for food in self.foods for allergen in food.allergens}
        ingredients = {ingredient for food in self.foods for ingredient in food.ingredients}

        allergic_candidates = self.get_allergic_candidates()

        allergic_ingredients = set.union(
            *[ingredients for ingredients in allergic_candidates.values()])
        return list(set.difference(ingredients, allergic_ingredients))

    def count_ingredients_occurrences(self, ingredients: List[str]) -> int:
        # part 1
        return sum(1 if ingredient in ingredients else 0 for food in self.foods
                   for ingredient in food.ingredients)

    def identify_allergic_ingredients(self) -> str:
        # part 2
        # ordered alphebetically by their allergen name
        allergic_candidates: Dict[str, Set[str]] = self.get_allergic_candidates()
        identified_ingreds: Dict[str, str] = {}
        while True:
            for allergen, ingred_candidates in allergic_candidates.items():
                if allergen in identified_ingreds:
                    continue
                elif len(ingred_candidates) == 1:
                    # retrieve the identified ingredient from set of candidate
                    identified_ingred = list(ingred_candidates)[0]

                    # add to the identified dictionary
                    identified_ingreds[allergen] = identified_ingred

                    for allergen, candidates in allergic_candidates.items():
                        try:
                            candidates.remove(identified_ingred)
                        except KeyError:
                            pass

            if len(identified_ingreds) == len(allergic_candidates):
                # break if all ingredients identified
                break

        return ','.join(identified_ingreds[allergen] for allergen in sorted(identified_ingreds))


#
# Unit Tests
#

foods = Foods(TEST_RAW)
non_allergic_ingredients = foods.get_non_allergic_ingredients()
num_occurences = foods.count_ingredients_occurrences(non_allergic_ingredients)
assert num_occurences == 5

allergic_candidates = foods.get_allergic_candidates()
print(allergic_candidates)

allergic_ing_str = foods.identify_allergic_ingredients()
assert allergic_ing_str == 'mxmxvkd,sqjhc,fvjkl'
#
# Problem
#

with open('inputs/21.txt') as file:
    RAW = file.read()

foods = Foods(RAW)
non_allergic_ingredients = foods.get_non_allergic_ingredients()
num_occurences = foods.count_ingredients_occurrences(non_allergic_ingredients)
# print(num_occurences)
allergic_candidates = foods.get_allergic_candidates()
print(allergic_candidates)

allergic_ing_str = foods.identify_allergic_ingredients()
print(allergic_ing_str)
