from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура выбора роли
role_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Участник"),
    KeyboardButton("Волонтёр"),
    KeyboardButton("Организатор")
)

# Клавиатуры
participant_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Календарь мероприятий"),
    KeyboardButton("Подписаться на рассылку"),
    KeyboardButton("Информация про эко-организации"),
    KeyboardButton("Оставить отзыв")
)

volunteer_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Календарь мероприятий"),
    KeyboardButton("Подписаться на рассылку"),
    KeyboardButton("Информация про эко-организации"),
    KeyboardButton("Общение с волонтёрами"),
    KeyboardButton("Оставить отзыв")
)

organizer_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Список мероприятий"),
    KeyboardButton("Создать мероприятие"),
    KeyboardButton("Удалить мероприятие"),
    KeyboardButton("Список организаций"),
    KeyboardButton("Создать организацию"),
    KeyboardButton("Удалить организацию"),
)

# Функция для получения нужной клавиатуры
def get_keyboard_for_role(role):
    if role in ["participant", "volunteer"]:
        return participant_keyboard if role == "participant" else volunteer_keyboard
    elif role == "organizer":  # ✅ Теперь организатор получает админские функции
        return organizer_keyboard
    return ReplyKeyboardMarkup(resize_keyboard=True)


