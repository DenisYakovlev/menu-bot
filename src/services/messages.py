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

            TODO: text to menu
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
            Введіть ціну нового меню
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

messageBuilder = MessageBuilder()