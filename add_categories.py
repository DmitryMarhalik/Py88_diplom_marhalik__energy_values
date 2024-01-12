from app_evop.models import Category

categories = {"🐟 Seafoods": "seafoods",
              "🍅 Vegetables, Fruits and Berries": "vegetables-fruits-and-berries",
              "🧈 Butter, Margarine, Edible Fats": "butter-margarine-edible-fats",
              "🥃 Drinks": "drinks",
              "🥚 Eggs, Milk and Dairy": "eggs-milk-and-dairy",
              "🥩 Meat and Sausage Products": "meat-and-sausage-products",
              "🍞 Bakery , Cereals, Pasta": "bakery-cereals-pasta",
              "🍄 Nuts and Mushrooms": "nuts-and-mushrooms",
              "🎂 Confectionery Products": "confectionery-products",
              "🥜 Legumes": "legumes",
              "🍝 Dishes": "dishes",
              "🥗 Salads": "salads"
              }
for category in categories:
    Category.objects.create(name=category, slug=categories[category])
