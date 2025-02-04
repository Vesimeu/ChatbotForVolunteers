from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
    KeyboardButton("Создать мероприятие"),
    KeyboardButton("Редактировать мероприятие"),
    KeyboardButton("Удалить мероприятие"),
    KeyboardButton("Список мероприятий"),
    KeyboardButton("Список организаций"),
    KeyboardButton("Создать организацию"),
    KeyboardButton("Редактировать организацию"),
    KeyboardButton("Удалить организацию"),
)

# Функция для получения нужной клавиатуры
def get_keyboard_for_role(role):
    if role in ["participant", "volunteer"]:
        return participant_keyboard if role == "participant" else volunteer_keyboard
    elif role == "organizer":  # ✅ Теперь организатор получает админские функции
        return organizer_keyboard
    return ReplyKeyboardMarkup(resize_keyboard=True)


