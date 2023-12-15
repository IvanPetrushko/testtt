import requests
from bs4 import BeautifulSoup
import telebot
import threading
import schedule
import time
from telebot import types


BOT_TOKEN = "6947482074:AAGlXyU7kSVLjYe2s_3QKdk9yapDkqeecyo"

CURRENCY_URL = 'https://myfin.by/currency/usd'

BASE_URL = 'http://127.0.0.1:8000'

previous_messages = {}

chat_ids = []

buy_rates = []

current_usd: float = 0

notification_states = {}


def get_chats():
    global chat_ids
    global notification_states

    response = requests.get(f"{BASE_URL}/api/chats")
    if response.status_code == 200:
        data = response.json()

        for chat in data:
            chat_id = chat["chat_id"]
            enable_notification = chat["enable_notification"]

            chat_ids.append(chat_id)
            notification_states[chat_id] = bool(enable_notification)

    else:
        print(f"Ошибка при выполнении запроса. Код ответа: {response.status_code}")


get_chats()


def get_message():
    global previous_messages

    response = requests.get(f"{BASE_URL}/api/message")
    if response.status_code == 200:
        data = response.json()

        if data:
            for chat_id, messages in data.items():
                chat_id = int(chat_id)
                if chat_id not in previous_messages:
                    previous_messages[chat_id] = []

                for message_info in messages:
                    message_id = message_info.get("message_id")
                    if message_id:
                        previous_messages[chat_id].append(message_id)
    else:
        print(f"Ошибка при выполнении запроса. Код ответа: {response.status_code}")


get_message()


def get_phone():
    response = requests.get(f"{BASE_URL}/api/phones")
    if response.status_code == 200:
        data = response.json()

        formatted_data = [(float(phone['price']), phone['name'], phone['memory'], phone['model']) for i, phone in
                          enumerate(data)]

        return formatted_data
    else:
        print(f"Ошибка при выполнении запроса. Код ответа: {response.status_code}")


def store_chat(chat_id, enable_notification):
    data = {"chat_id": chat_id, "enable_notification": enable_notification}
    response = requests.post(f"{BASE_URL}/api/chats/store", json=data)
    if response.status_code == 200:
        print("STORE CHAT SUCCESSFUL")
    else:
        print(f"POST request failed with status code {response.status_code}")


def update_chat(chat_id, enable_notification):
    data = {"enable_notification": enable_notification}
    response = requests.post(f"{BASE_URL}/api/chats/update/{chat_id}", json=data)
    if response.status_code == 200:
        print("UPDATE CHAT SUCCESSFUL")
        print(response.text)
    else:
        print(f"POST request failed with status code {response.status_code}")


def store_message(chat_id, message_id):
    data = {"chat_id": chat_id, "message_id": message_id}
    response = requests.post(f"{BASE_URL}/api/message/store", json=data)
    if response.status_code == 200:
        print("STORE MESSAGE SUCCESSFUL")
    else:
        print(f"POST request failed with status code {response.status_code}")


def delete_message_back(message_id):
    response = requests.post(f"{BASE_URL}/api/message/delete-message/{message_id}")
    if response.status_code == 200:
        print("DELETE MESSAGE SUCCESSFUL")
        print(response.text)
    else:
        print(f"POST request failed with status code {response.status_code}")


def get_device():
    response = requests.get(f"{BASE_URL}/api/device")
    if response.status_code == 200:
        data = response.json()
        product_info = []
        for category, products in data.items():
            product_info.append(f"—————————————————-\n{category}")
            for i, product in enumerate(products):
                if i > 0 and (products[i - 1]['model'] != product['model']):
                    product_info.append("\n")
                product_info.append(f"{product['name']} - {round(product['price'] * current_usd)} р.")
            if category == "💻Air/Pro M1💻":
                product_info.append(
                    "⚠️Кастомные MacBook Pro/Air на М1 с 16 ОЗУ и выше -уточняйте наличие и конфигурации.")
            if category == "💻Pro 14/16’’💻":
                product_info.append("⚠️Кастомные MacBook Pro 14/16’’-уточняйте наличие и конфигурации.")
            if category == "💻Pro 14/16’’ М2💻":
                product_info.append("⚠️Кастомные MacBook Pro 14/16’’-уточняйте наличие и конфигурации.")
            if category == "💻Air/Pro M2💻":
                product_info.append(
                    "⚠️Кастомные MacBook Pro/Air на М2 с 16 ОЗУ и выше -уточняйте наличие и конфигурации.")
        return product_info

    else:
        print(f"Ошибка при выполнении запроса. Код ответа: {response.status_code}")


def send_notification(new_info, chat_id, bot):
    try:
        phone_message = "📲НОВЫЕ ТЕЛЕФОНЫ📲\n(новые, неактивированные, запечатанные устройства Apple)\n—————————————————"

        previous_memory = None
        previous_model = None

        for price, name, memory, model in new_info:
            if previous_model and previous_model != model:
                phone_message += "\n—————————————————-"

            if previous_memory and previous_memory != memory and previous_model and previous_model == model:
                phone_message += "\n"

            phone_message += f"\n{str(name)} - {round(price)} р."

            previous_memory = memory
            previous_model = model

        phone_message += "\n—————————————————-"

        phone_message += '''\nСтандартные версии: физическая + виртуальная сим-карта 
🔒Гарантия 1 год с момента покупки
🎁 Чехол (Silicone Case)+10D Стекло в подарок к каждому телефону
🚚 доставка бесплатная по Гродно  и РБ (в течении суток после заказа)
💰Самые низкие цены
🆕 Новые | запечатанные | неактивированные | оригинальные

‼️ Нашли дешевле? НАПИШИ НАМ и мы сделаем СКИДКУ 🏷‼️
❗️Цены  ИНОГДА могут зависеть от курса рубля, наличия, спроса, как выше, так и ниже❗️

📱8 (029) 2 33 33 02 📲
📨@ReStore_grodno'''

        device = get_device()

        device_message = "💻MacBook💻\n"
        device_message += "\n".join(device)
        device_message += '''\n\n\n🔒Гарантия 1 год с момента покупки.\n
📢 Все планшеты и часы новые и оригинальные.\n
❗️Цены  ИНОГДА могут зависеть от курса рубля, наличия, спроса, как выше, так и ниже❗️

📱8 (029) 2 33 33 02 📲
📨@ReStore_grodno'''

        for msg_id in previous_messages.get(chat_id, []):
            try:
                bot.delete_message(chat_id, msg_id)
                delete_message_back(msg_id)
            except Exception as exception:
                print(f"Error deleting previous message: {exception}")

        phone_msg = bot.send_message(chat_id, phone_message, disable_notification=True)
        store_message(chat_id, phone_msg.message_id)
        device_msg = bot.send_message(chat_id, device_message, disable_notification=True)
        store_message(chat_id, device_msg.message_id)
        previous_messages[chat_id] = [phone_msg.message_id, device_msg.message_id]

        print(f"Notification sent")
    except Exception as exception:
        print(f"Error sending notification: {exception}")


def get_currency_exchange_rate():
    response = requests.get(CURRENCY_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        currency_elements = soup.find_all('tr', class_='currencies-courses__row-main')

        for currency_element in currency_elements:
            td_elements = currency_element.find_all('td', class_='currencies-courses__currency-cell')

            if len(td_elements) >= 2:
                buy_rate = td_elements[1].text.strip()
                buy_rates.append(float(buy_rate.replace(',', '.')))

            if buy_rate and buy_rate != '-':
                buy_rates.append(float(buy_rate))

        max_rate = max(buy_rates)
        return float(max_rate)
    else:
        print(f"Error fetching currency exchange rate: {response.status_code}")
        return None


def get_current_usd():
    global current_usd
    response = requests.get(CURRENCY_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        currency_elements = soup.find_all('tr', class_='currencies-courses__row-main')

        for currency_element in currency_elements:
            td_elements = currency_element.find_all('td', class_='currencies-courses__currency-cell')

            if len(td_elements) >= 2:
                buy_rate = td_elements[1].text.strip()
                buy_rates.append(float(buy_rate.replace(',', '.')))

            if buy_rate and buy_rate != '-':
                buy_rates.append(float(buy_rate))

        max_rate = max(buy_rates)
        current_usd = max_rate
        return float(max_rate)
    else:
        print(f"Error fetching currency exchange rate: {response.status_code}")
        return None


get_current_usd()

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = create_chat_keyboard(message.chat.id)

    chat_id = message.chat.id

    if chat_id not in notification_states:
        notification_states[chat_id] = True

    if chat_id in chat_ids:
        update_chat(chat_id, 1)
        notification_states[chat_id] = True
    else:
        store_chat(chat_id, 1)
        chat_ids.append(chat_id)

    bot.send_message(message.chat.id, 'Вас приветствует магазин @ReStore_grodno, здесь вы будете получать обновленную '
                                      'цену товаров', reply_markup=markup)

    handle_get_price(message)


def create_chat_keyboard(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    get_price_button = types.KeyboardButton("Получить актуальную цену")

    if notification_states.get(chat_id, True):
        item_notification = types.KeyboardButton("Остановить обновление цен")
    else:
        item_notification = types.KeyboardButton("Включить обновление цен")

    markup.add(get_price_button, item_notification)
    return markup


@bot.message_handler(func=lambda message: message.text in ["Остановить обновление цен", "Включить обновление цен"],
                     content_types=['text'])
def handle_toggle_notifications(message):
    chat_id = message.chat.id
    current_state = notification_states.get(chat_id, True)

    if current_state:
        notification_states[chat_id] = False
        update_chat(chat_id, 0)
        markup = create_chat_keyboard(chat_id)
        bot.send_message(chat_id, "🔕 Обновление цен отключено", reply_markup=markup, disable_notification=True)
    else:
        notification_states[chat_id] = True
        update_chat(chat_id, 1)
        markup = create_chat_keyboard(chat_id)
        bot.send_message(chat_id, "🔔 Обновление цен включено", reply_markup=markup, disable_notification=True)


@bot.message_handler(func=lambda message: message.text == 'Выйти из бота', content_types=['text'])
def exit_from_chat(message):
    chat_id = message.chat.id
    current_state = notification_states.get(chat_id, True)

    if current_state:
        notification_states[chat_id] = False
        update_chat(chat_id, 0)
        markup = create_chat_keyboard(chat_id)
        bot.send_message(chat_id, "🔕 Обновление цен отключено", reply_markup=markup, disable_notification=True)
    else:
        notification_states[chat_id] = True
        update_chat(chat_id, 1)
        markup = create_chat_keyboard(chat_id)
        bot.send_message(chat_id, "🔔 Обновление цен включено", reply_markup=markup, disable_notification=True)


@bot.message_handler(func=lambda message: message.text == "Получить актуальную цену", content_types=['text'])
def handle_get_price(message):
    try:
        currency_exchange_rate = get_currency_exchange_rate()
        if currency_exchange_rate is not None:
            currency_exchange_rate = get_currency_exchange_rate()
            if currency_exchange_rate is not None:
                phone = get_phone()

                phone_message = ("📲НОВЫЕ ТЕЛЕФОНЫ📲\n(новые, неактивированные, запечатанные устройства "
                                 "Apple)\n—————————————————")

                previous_memory = None
                previous_model = None

                for price, name, memory, model in phone:
                    if previous_model and previous_model != model:
                        phone_message += "\n—————————————————-"

                    if previous_memory and previous_memory != memory and previous_model and previous_model == model:
                        phone_message += "\n"

                    phone_message += f"\n{str(name)} - {round(price * currency_exchange_rate)} р."

                    previous_memory = memory
                    previous_model = model

                phone_message += "\n—————————————————-"
                phone_message += '''\nСтандартные версии: физическая + виртуальная сим-карта 
🔒Гарантия 1 год с момента покупки 
🎁 Чехол (Silicone Case)+10D Стекло в подарок к каждому телефону
🚚 доставка бесплатная по Гродно  и РБ (в течении суток после заказа)
💰Самые низкие цены
🆕 Новые | запечатанные | неактивированные | оригинальные
    
‼️ Нашли дешевле? НАПИШИ НАМ и мы сделаем СКИДКУ 🏷‼️
❗️Цены  ИНОГДА могут зависеть от курса рубля, наличия, спроса, как выше, так и ниже❗️
    
📱8 (029) 2 33 33 02 📲
📨@ReStore_grodno'''

                device = get_device()

                device_message = "💻MacBook💻\n"
                device_message += "\n".join(device)
                device_message += '''\n\n\n🔒Гарантия 1 год с момента покупки.\n
📢 Все планшеты и часы новые и оригинальные.\n
❗️Цены  ИНОГДА могут зависеть от курса рубля, наличия, спроса, как выше, так и ниже❗️
    
📱8 (029) 2 33 33 02 📲
📨@ReStore_grodno'''

        for msg_id in previous_messages.get(message.chat.id, []):
            try:
                bot.delete_message(message.chat.id, msg_id)
                delete_message_back(msg_id)
            except Exception as exception:
                print(f"Error deleting previous message: {exception}")

        phone_msg = bot.send_message(message.chat.id, phone_message, disable_notification=True)
        store_message(message.chat.id, phone_msg.message_id)
        device_msg = bot.send_message(message.chat.id, device_message, disable_notification=True)
        store_message(message.chat.id, device_msg.message_id)
        previous_messages[message.chat.id] = [phone_msg.message_id, device_msg.message_id]

    except Exception as exception:
        print(f"Error getting current price: {exception}")


def update_prices():
    global current_usd
    try:
        currency_exchange_rate = get_currency_exchange_rate()
        if currency_exchange_rate is not None:
            if 0.3 >= abs(currency_exchange_rate - current_usd):
                print('notification don"t send, but price')
            else:
                product_prices = get_phone()
                new_prices = [(price * currency_exchange_rate, name, memory, model) for price, name, memory, model in
                              product_prices]

                for chat_id in chat_ids:
                    current_usd = currency_exchange_rate
                    if notification_states.get(chat_id, True):
                        send_notification(new_prices, chat_id, bot)
    except Exception as exception:
        print(f"Error updating prices: {exception}")


schedule.every(1).minutes.do(update_prices)


def polling_worker():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as exception:
            print(f"Error in polling worker: {exception}")
            time.sleep(5)


polling_thread = threading.Thread(target=polling_worker)
polling_thread.start()

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(5)
