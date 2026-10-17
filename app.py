import json
import os
import random







class Dish:

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Ціна повинна бути більшою за 0")
        self._price = value

    def describe(self):
        return f"{self.name} — {self.price} грн"


class MainCourse(Dish):

    def __init__(self, name: str, price: float, weight_g: int):
        super().__init__(name, price)
        self.weight_g = weight_g

    def describe(self):
        return f"{super().describe()} ({self.weight_g}г)"


class Drink(Dish):

    def __init__(self, name: str, price: float, volume_ml: int):
        super().__init__(name, price)
        self.volume_ml = volume_ml

    def describe(self):
        return f"{super().describe()} ({self.volume_ml}мл)"


class Dessert(Dish):

    def __init__(self, name: str, price: float, is_vegan: bool):
        super().__init__(name, price)
        self.is_vegan = is_vegan

    def describe(self):
        vegan_str = " (веганський)" if self.is_vegan else ""
        return f"{super().describe()}{vegan_str}"


class Table:

    def __init__(self, number: int, seats: int):
        self.number = number
        self.seats = seats
        self.is_busy = False

    def occupy(self):
        self.is_busy = True

    def free(self):
        self.is_busy = False










class Restaurant:

    def __init__(self):
        self.dishes = []
        self.tables = [
            Table(1, 2),
            Table(2, 4),
            Table(3, 2),
            Table(4, 6),
            Table(5, 4),
        ]
        self.total_revenue = 0
        self.served_tables = 0
        self.ratings = []

        self.load_menu()

        if self.dishes:
            self.today_special = random.choice(self.dishes)
        else:
            self.today_special = None

    def load_menu(self):
        if not os.path.exists("menu.json"):
            self.dishes = [
                MainCourse("Борщ", 120, 350),
                Drink("Узвар", 40, 250),
                Dessert("Медовик", 90, False),
                Dessert("Фруктовий салат", 80, True),
            ]
            self.save_menu()
            return

        try:
            with open("menu.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.dishes = []
                for item in data:
                    t = item.get("type")
                    if t == "main":
                        self.dishes.append(
                            MainCourse(
                                item["name"], item["price"], item["weight_g"]
                            )
                        )
                    elif t == "drink":
                        self.dishes.append(
                            Drink(
                                item["name"], item["price"], item["volume_ml"]
                            )
                        )
                    elif t == "dessert":
                        self.dishes.append(
                            Dessert(
                                item["name"], item["price"], item["is_vegan"]
                            )
                        )
        except Exception as e:
            print(f"Помилка завантаження меню: {e}")

    def save_menu(self):
        data = []
        for d in self.dishes:
            item = {"name": d.name, "price": d.price}
            if isinstance(d, MainCourse):
                item["type"] = "main"
                item["weight_g"] = d.weight_g
            elif isinstance(d, Drink):
                item["type"] = "drink"
                item["volume_ml"] = d.volume_ml
            elif isinstance(d, Dessert):
                item["type"] = "dessert"
                item["is_vegan"] = d.is_vegan
            data.append(item)

        with open("menu.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def show_menu(self, dishes_to_show=None):
        if dishes_to_show is None:
            dishes_to_show = self.dishes

        if not dishes_to_show:
            print("Меню порожнє.")
            return

        print("\n--- МЕНЮ ---")
        for i, d in enumerate(dishes_to_show, 1):
            star = " *" if d == self.today_special else ""
            print(f"{i}. {d.describe()}{star}")

    def add_dish(self):
        try:
            name = input("Назва: ").strip()
            if not name:
                print("Помилка: Назва не може бути порожньою")
                return

            price = float(input("Ціна: "))
            if price <= 0:
                print("Помилка: Ціна повинна бути більшою за 0")
                return

            print("Тип: 1-Основна, 2-Напій, 3-Десерт")
            t = input("> ").strip()

            if t == "1":
                w = int(input("Вага (г): "))
                if w <= 0:
                    print("Помилка: Вага має бути більшою за 0")
                    return
                dish = MainCourse(name, price, w)
            elif t == "2":
                v = int(input("Об'єм (мл): "))
                if v <= 0:
                    print("Помилка: Об'єм має бути більшим за 0")
                    return
                dish = Drink(name, price, v)
            elif t == "3":
                veg = input("Веганський? (1-Так, 0-Ні): ").strip()
                if veg not in ["0", "1"]:
                    print("Помилка: Введіть 1 або 0")
                    return
                dish = Dessert(name, price, veg == "1")
            else:
                print("Невідомий тип!")
                return

            self.dishes.append(dish)
            self.save_menu()
            print("Страву додано!")

        except ValueError:
            print("Помилка вводу: некоректні дані")

    def show_tables(self):
        print("\n--- СТОЛИКИ ---")
        for t in self.tables:
            status = "Зайнятий" if t.is_busy else "Вільний"
            print(f"Столик №{t.number} ({t.seats} місць) — {status}")

    def seat_guests(self):
        try:
            guests = int(input("Кількість гостей: "))
            if guests <= 0:
                print("Помилка: Кількість гостей має бути більшою за 0")
                return

            for t in self.tables:
                if not t.is_busy and t.seats >= guests:
                    t.occupy()
                    print(f"Гостей посаджено за столик №{t.number}")
                    return
            print("Місць немає")

        except ValueError:
            print("Введіть число!")

    def take_order(self):
        busy_tables = [t for t in self.tables if t.is_busy]
        if not busy_tables:
            print("Немає зайнятих столиків")
            return

        self.show_tables()
        try:
            t_num = int(input("Номер зайнятого столика: "))
            table = next(
                (t for t in busy_tables if t.number == t_num),
                None,
            )

            if not table:
                print("Столик не знайдено або він вільний!")
                return

            self.show_menu()
            order = []
            print("Введіть номери страв (0 для завершення):")

            while True:
                try:
                    idx = int(input("> "))
                    if idx == 0:
                        break
                    if 1 <= idx <= len(self.dishes):
                        order.append(self.dishes[idx - 1])
                    else:
                        print("Некоректний номер страви!")
                except ValueError:
                    print("Введіть число!")

            if not order:
                print("Замовлення порожнє.")
                return

            self.checkout(table, order)

        except ValueError:
            print("Некоректне число!")

    def checkout(self, table, order):
        total = 0
        print(f"\n=== ЧЕК (Столик №{table.number}) ===")

        # Бонус: VIP 5-й столик
        if table.number % 5 == 0:
            print("VIP-бонус: Безкоштовний десерт!")

        for d in order:
            price = d.price
            if d == self.today_special:
                price *= 0.8
                print(f"* {d.name} (Страва дня -20%): {price:.2f} грн")
            else:
                print(f"  {d.name}: {price:.2f} грн")
            total += price

        # Знижки
        if total > 2000:
            total *= 0.90
            print("Знижка 10%")
        elif total > 1000:
            total *= 0.95
            print("Знижка 5%")

        print(f"ВСЬОГО: {total:.2f} грн")

        # Чек у файл
        with open(f"check_{table.number}.txt", "w", encoding="utf-8") as f:
            f.write(f"Чек для столика №{table.number}\nСума: {total:.2f} грн\n")

        # Відгук
        rating = random.randint(1, 5)
        self.ratings.append(rating)
        print(f"Оцінка гостя: {rating}/5")

        self.total_revenue += total
        self.served_tables += 1
        table.free()









def main():
    res = Restaurant()

    while True:
        print("\n===== РЕСТОРАН «Смакота» =====")
        print("1. Показати меню")
        print("2. Додати страву")
        print("3. Показати столики")
        print("4. Посадити гостей")
        print("5. Прийняти замовлення")
        print("6. Фільтр меню (Веганські десерти)")
        print("7. Закрити зміну")
        print("0. Вихід")

        choice = input("> ").strip()

        if choice == "1":
            res.show_menu()
        elif choice == "2":
            res.add_dish()
        elif choice == "3":
            res.show_tables()
        elif choice == "4":
            res.seat_guests()
        elif choice == "5":
            res.take_order()
        elif choice == "6":
            veg_desserts = [
                d for d in res.dishes if isinstance(d, Dessert) and d.is_vegan
            ]
            res.show_menu(veg_desserts)
        elif choice == "7":
            print(f"\nОбслуговувано столиків: {res.served_tables}")
            print(f"Загальна виручка: {res.total_revenue:.2f} грн")
            if res.ratings:
                avg = sum(res.ratings) / len(res.ratings)
                print(f"Середня оцінка: {avg:.2f}")
            break
        elif choice == "0":
            break


if __name__ == "__main__":
    main()