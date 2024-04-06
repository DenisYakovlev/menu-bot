from inspect import cleandoc as _


class MessageBuilder():

    def start_welcome(self, first_name: str) -> str:
        return _(
            f"""
            *🎉 Вітаємо, {first_name}! 🎉*

            Ви авторизувалися у застосунку для вибору страв 
            через *меню бота 🍽*

            Редагувати свої дані/робити замовлення можна 
            через інтерфейс нижче ⬇️⬇️⬇️
            """
        )
    
    def start_welcome_back(self, first_name: str) -> str:
        return _(
            f"""
            *🎉 З поверненням, {first_name}! 🎉*

            Ви повернулись до застосунку для вибору страв 
            через *меню бота 🍽*

            Редагувати свої дані/робити замовлення можна 
            через інтерфейс нижче ⬇️⬇️⬇️
            """
        )
    
    def settings(self, phone_number, first_name, last_name, is_manager) -> str:
        return _(
            f"""
            *📇 Особисті дані*

            📞 Номер телефона: *{phone_number if phone_number else "Не вказано"}*
            👤 Ім'я: *{first_name}*
            👥 Прізвище: *{last_name if last_name else "Не вказано"}*
            🧑‍💻 Статус: *{"Менеджер" if is_manager else "Користувач"}*

            *Надайте свій контакт для оновлення даних
            через інтерфейс нижче ⬇️⬇️⬇️*
            """
        )
    
    def settings_status_update(self, is_manager: bool) -> str:
        return _(
            f"""
            *🧑‍💻 Ваш статус оновлено*

            Тепер ви: *{"Менеджер" if is_manager else "Користувач"}*
            """
        )
    
    def settings_from_contact(self) -> str:
        return _(
            f"""
            *✅ Успішно!*

            Ваші дані оновлені згідно наданого контакту
            """
        )
    
    def main_menu(self) -> str:
        return _(
            f"""
            📇 Головне меню
            """
        )
    
    def error(self, error) -> str:
        return _(
            f"""
            *❌ Виникла помилка*

            _{error}_
            """
        )
    
    def menu(self) -> str:
        return _(
            f"""
            *🔖 Меню*

            Ви можете вибрати страви на сьогодні та на завтра
            """
        )
    
    def menu_settings(self) -> str:
        return _(
            f"""
            *⚙️ Налаштування меню*

            TODO: text to menu settings
            """
        )
    
    def menu_create(self) -> str:
        return _(
            f"""
            *🛠 Створення меню*

            На яку дату ви хочете створити меню?
            *Формат: рік-місяць-день*
            """
        )
    
    def menu_create_date_error(self) -> str:
        return _(
            f"""
            Ця дата не підходить по формату
            *Формат: рік-місяць-день*
            """
        )
    
    def menu_create_name(self) -> str:
        return _(
            f"""
            Введіть назву нового меню
            """
        )
    
    def menu_create_success(self, name: str, date: str) -> str:
        return _(
            f"""
            *✅ Успішно!*

            Створенно нове меню:
            📑 Назва: *{name}*
            📅 Дата: *{date}*
            """
        )
    
    def meal_create(self) -> str:
        return _(
            f"""
            *🛠 Створення страви*

            Введіть назву нової страви
            """
        )
    
    def meal_create_price(self) -> str:
        return _(
            f"""
            Введіть ціну нової страви
            """
        )
    
    def meal_create_price_error(self) -> str:
        return _(
            f"""
            Введена ціна не підходить по формату
            """
        )
    
    def meal_create_img_url(self) -> str:
        return _(
            f"""
            Введіть посилання на зображення страви
            Якщо бажаєте використати дефолтне зображення, напишіть '-' (без дужок)
            """
        )
    
    def meal_create_img_url_error(self) -> str:
        return _(
            f"""
            Введене посилання не підходить по формату
            """
        )
    
    def meal_create_type_id(self) -> str:
        return _(
            f"""
            Виберіть тип страви ⬇️⬇️⬇️
            """
        )
    
    def meal_create_success(self, name: str, price: str) -> str:
        return _(
            f"""
            *✅ Успішно!*

            Створена нова страва:
            📑 Назва: *{name}*
            📌 Ціна: *{price}*
            """
        )
    

    def menu_edit(self) -> str:
        return _(
            f"""
            *🔖 Список меню*

            Оберіть меню, яке хочете редактувати
            """
        )
    
    def menu_edit_meals(self, name) -> str:
        return _(
            f"""
            *🔖 Редагування {name}*

            Інформація про все меню ⬇️⬇️⬇️
            """
        )
    
    def add_meal_to_menu(self) -> str:
        return _(
            f"""
            *➕ Додати страви*

            Виберіть страви зі списку ⬇️⬇️⬇️
            """
        )
    
    def choose_menu(self, name: str) -> str:
        return _(
            f"""
            *🔖 {name}*

            Оберіть страви зі списку
            Натисніть на назву страву для перегляду опису
            """
        )
    
    def choose_menu_cancel(self) -> str:
        return _(
            f"""
            *❌ Скасовано*

            Всі ваші внесені дані були видалені 
            """
        )
    
    def choose_menu_meal(self, menu_name: str, meal_name: str, meal_price: str) -> str:
        return _(
            f"""
            *🔖 {menu_name}*

            Інформація про страву:
            📑 Назва: *{meal_name}*
            📌 Ціна: *{meal_price}*
            """
        )
    
    def choose_menu_check(self, total_price: float) -> str:
        return _(
            f"""
            *📝 Чек*

            Перегляньте страви, які ви обрали

            💰 Загальна вартість: {total_price}
            """
        )

messageBuilder = MessageBuilder()