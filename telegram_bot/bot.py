import os
import psycopg2
import telebot
import smtplib

from datetime import datetime
from dotenv import load_dotenv
from telebot import types
from collections import Counter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()

connection = psycopg2.connect(user=os.getenv('USER_PSQL'), database="evop",
                              host="127.0.0.1", port="5432", password=os.getenv('PSQL_PASSWORD'))
cursor = connection.cursor()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.from_user.id, "Please, enter your 'Name' and 'E-mail' separated by a space.\n"
                                           "for example:\nmichael your_email@gmail.com")
    bot.register_next_step_handler(message, authentication)


name = None
email = None
user_id = None


def show_menu(message):
    markup = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton("👀 View all products")
    button_2 = types.KeyboardButton("✅ Add a product")
    button_3 = types.KeyboardButton("📝 Enter intake")
    button_4 = types.KeyboardButton("📆 Calculation result")
    markup.add(button_1, button_2, button_3, button_4, row_width=1)
    bot.send_message(message.from_user.id, "Please, choice the operation  ⬇", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def authentication(message):
    try:
        global name, email, user_id
        name, email = message.text.split(" ")
        postgres_insert_query1 = """select auth_user.id from auth_user
                                                            where (auth_user.username = %s and auth_user.email = %s)"""
        cursor.execute(postgres_insert_query1, (name, email))
        user_id = cursor.fetchone()[0]
        if user_id:
            bot.send_message(message.from_user.id, f"Successful authorization, {name}!")
            show_menu(message)
    except Exception:
        bot.send_message(message.from_user.id, "Incorrect input name or e-mail address. "
                                               "Please, enter your name and e-mail separated by a space")
        bot.register_next_step_handler(message, authentication)


@bot.message_handler()
def on_click(message):
    if message.text == "👀 View all products":
        markup = types.ReplyKeyboardMarkup()
        button_1 = types.KeyboardButton("🐟 Seafoods")
        button_2 = types.KeyboardButton("🍅 Vegetables, Fruits and Berries")
        button_3 = types.KeyboardButton("🧈 Butter, Margarine, Edible Fats")
        button_4 = types.KeyboardButton("🥃 Drinks")
        button_5 = types.KeyboardButton("🥚 Eggs, Milk and Dairy")
        button_6 = types.KeyboardButton("🥩 Meat and Sausage Products")
        button_7 = types.KeyboardButton("🍞 Bakery , Cereals, Pasta")
        button_8 = types.KeyboardButton("🍄 Nuts and Mushrooms")
        button_9 = types.KeyboardButton("🎂 Confectionery Products")
        button_10 = types.KeyboardButton("🥜 Legumes")
        button_11 = types.KeyboardButton("🍝 Dishes")
        button_12 = types.KeyboardButton("🥗 Salads")
        button_13 = types.KeyboardButton("↩ Return back")
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8,
                   button_9, button_10, button_11, button_12, button_13, row_width=4)
        bot.send_message(message.from_user.id, "Please, select category of products  ⬇",
                         reply_markup=markup)
        bot.register_next_step_handler(message, on_click_category)
    elif message.text == "✅ Add a product":
        bot.send_message(message.from_user.id, "All categories ⬇")
        postgres_insert_query = """select id, name from app_evop_category order by name"""
        cursor.execute(postgres_insert_query, (message.from_user.id,))
        allcategories_products = cursor.fetchall()
        connection.commit()
        for category in allcategories_products:
            bot.send_message(message.from_user.id, f"{category[1]} ➡ category id: {category[0]}")
        bot.send_message(message.from_user.id,
                         "❗<The entered energy values should be no more than 9999 "
                         "and no more than one digit after the decimal point>\n"
                         "1⃣ 🆔 Select the category id of the product to be added.\n"
                         "2⃣ 📝 And then, enter name of product, barcode, protein, fat, carbohydrate, kcal, "
                         "category id per 100 grams separated by a comma.\n"
                         "3⃣ 🅾 If the barcode is unknown, then enter the digit 0. For example:\n"
                         "Куриный суп по-индийски, 16237272 (or 0), 232.4,3233, 367, 834, 4'  ⬇")
        bot.register_next_step_handler(message, add_product)
    elif message.text == "📝 Enter intake":
        bot.send_message(message.from_user.id, "❗<The entered energy values should be no more than 9999"
                                               " and no more than one digit after the decimal point>\n"
                                               "  Enter your product(the exact name of the product can be found "
                                               "at 'View all product' button🔘)  and product quantity in grams "
                                               "separated by a comma. "
                                               "For example:\n'Помидоры черри, 250'  ⬇")
        bot.register_next_step_handler(message, intake)
    elif message.text == "📆 Calculation result":
        bot.send_message(message.from_user.id, "📅 For what time period to calculate the result? "
                                               "Enter the number of days.  ⬇")
        bot.register_next_step_handler(message, finally_calculation)
    else:
        bot.send_message(message.from_user.id, "Something went wrong")


def on_click_category(message):
    if message.text == '↩ Return back':
        show_menu(message)
    else:
        try:
            keyword = {'🐟 Seafoods': '1', '🍅 Vegetables, Fruits and Berries': '2',
                       '🧈 Butter, Margarine, Edible Fats': '3', '🥃 Drinks': '4', '🥚 Eggs, Milk and Dairy': '5',
                       '🥩 Meat and Sausage Products': '6', '🍞 Bakery , Cereals, Pasta': '7',
                       '🍄 Nuts and Mushrooms': '8', '🎂 Confectionery Products': '9',
                       '🥜 Legumes': '10', '🍝 Dishes': '11', '🥗 Salads': '12'}
            bot.send_message(message.from_user.id, f"{message.text} products: ⬇")
            postgres_insert_query = """select name from app_evop_food 
                                                                where app_evop_food.category_id = %s order by name"""
            cursor.execute(postgres_insert_query, (keyword[message.text],))
            products_in_category = cursor.fetchall()
            connection.commit()
            for name in products_in_category:
                bot.send_message(message.from_user.id, f"{name[0]}")
            show_menu(message)
        except Exception:
            bot.send_message(message.from_user.id, "Something went wrong")
            show_menu(message)


def add_product(message):
    try:
        product_name, bar_code, protein, fat, carbohydrate, kcal, category_id = message.text.split(",")
        bar_code = None if int(bar_code) == 0 else bar_code
        postgres_insert_query = """INSERT INTO app_evop_food (name, bar_code, proteins, fats, 
                                carbohydrates, kcal, be_confirmed, category_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        be_confirmed = "False"
        cursor.execute(postgres_insert_query, (product_name, bar_code, float(protein),
                                               float(fat), float(carbohydrate), float(kcal), be_confirmed, category_id))
        connection.commit()
        bot.send_message(message.from_user.id, "Product added successfully!")

        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(os.getenv('ADMIN_EMAIL'), os.getenv("EMAIL_ADMIN_PASSWORD"))
        text_message = (
            f'from :{name}, e-mail: {email}\nfood: {product_name}\nbar_code: {bar_code}\nproteins: {protein}'
            f'\nfats: {fat}\ncarbohydrates: {carbohydrate}\nkcal: {kcal}\ncategory: {category_id}')
        msg = MIMEMultipart()
        msg["Subject"] = "food from user EVOP-tg-bot 📧"
        msg.attach(MIMEText(text_message, "plain"))
        smtp_server.sendmail(f'{email}', os.getenv('ADMIN_EMAIL'), msg.as_string())
        smtp_server.quit()
    except Exception:
        bot.send_message(message.from_user.id, "Incorrect input product. Please, try again")


def intake(message):
    try:
        product_name, gram = message.text.split(",")
        postgres_insert_query2 = """select app_evop_food.id from app_evop_food where app_evop_food.name = %s"""
        cursor.execute(postgres_insert_query2, (product_name.strip(),))
        food_id = cursor.fetchone()[0]
        current_time = datetime.now()
        postgres_insert_query3 = """INSERT INTO app_evop_intake (user_id, food_id, gram, time) VALUES (%s,%s,%s,%s)"""
        cursor.execute(postgres_insert_query3, (user_id, int(food_id), float(gram), current_time))
        connection.commit()
        bot.send_message(message.from_user.id, "The intake added!")
    except Exception:
        bot.send_message(message.from_user.id, "Incorrect input intake. Please, try again")


def calculation_all_idproducts(message):
    try:
        days = int(message.text)
        postgres_insert_query = f"""select app_evop_intake.food_id from app_evop_intake
         where (time > now() - interval '%s days' and user_id = {user_id})"""
        cursor.execute(postgres_insert_query, (days,))
        return cursor.fetchall()
    except Exception:
        return False


def finally_calculation(message):
    idproducts = calculation_all_idproducts(message)
    all_products, view_all_products, all_energy_values, \
        nice_count_of_product, view_all_products = [], [], [], [], []
    if bool(idproducts):
        for id in idproducts:
            postgres_insert_query = """select name from app_evop_food where id=%s"""
            cursor.execute(postgres_insert_query, id)
            product = cursor.fetchone()
            all_products.append(product)

        for name in all_products:
            view_all_products.append(name[0])
            postgres_insert_query = """select proteins,fats,carbohydrates, kcal from app_evop_food where name=%s"""
            cursor.execute(postgres_insert_query, name)
            energy_values = cursor.fetchone()
            all_energy_values.append(energy_values)

        all_proteins = all_fats = all_carbohydrates = all_kcal = 0
        for el in all_energy_values:
            all_proteins += el[0]
            all_fats += el[1]
            all_carbohydrates += el[2]
            all_kcal += el[3]

        count_of_product = Counter(view_all_products)
        #  сортировка употребленных продуктов по количеству употребления
        #  count_of_product = dict(sorted(count_of_product.items(), key=lambda item: item[1]))
        for k, v in count_of_product.items():
            nice_count_of_product.append(f"{k}->{v} times\n")
        nice_count_of_product = sorted(nice_count_of_product)  # сортировка употребленных продуктов по алфавиту
        result_message = f"You have eaten the following foods:\n{''.join(nice_count_of_product)}\n" \
                         f"Total amount of protein:  {all_proteins} gr,\nfats: {all_fats} gr,\n" \
                         f"carbohydrates: {all_carbohydrates} gr,\nKcal: {all_kcal}"
        bot.send_message(message.from_user.id, result_message)
    elif idproducts == []:
        bot.send_message(message.from_user.id, "You haven't eaten anything during this time")
    else:
        bot.send_message(message.from_user.id, "Incorrect input days. Please, try again")


bot.polling(none_stop=True, interval=0)
