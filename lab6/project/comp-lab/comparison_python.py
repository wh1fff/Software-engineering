# ЛАБОРАТОРНАЯ РАБОТА 6. PYTHON


from dataclasses import dataclass
from typing import List, Optional
from functools import reduce


@dataclass
class User:
# пользователь 

    id: int
    name: str
    email: str


@dataclass
class Product:
# товар в магазине

    id: int
    name: str
    price: float
    category: str


@dataclass
class OrderItem:
# позиция в заказе

    product: Product
    quantity: int


@dataclass
class Order:
    """Заказ пользователя"""

    id: int
    user: User
    items: List[OrderItem]
    status: str


# ИНИЦИАЛИЗАЦИЯ ДАННЫХ

users = [
    User(1, "John Doe", "john@example.com"),
    User(2, "Jane Smith", "jane@example.com"),
    User(3, "Bob Johnson", "bob@example.com"),
]

products = [
    Product(1, "iPhone", 999.99, "electronics"),
    Product(2, "MacBook", 1999.99, "electronics"),
    Product(3, "T-shirt", 29.99, "clothing"),
    Product(4, "Jeans", 79.99, "clothing"),
    Product(5, "Book", 15.99, "books"),
]

orders = [
    Order(
        1,
        users[0],
        [
            OrderItem(products[0], 1),
            OrderItem(products[2], 2),
        ],
        "completed",
    ),
    Order(
        2,
        users[1],
        [
            OrderItem(products[1], 1),
        ],
        "pending",
    ),
    Order(
        3,
        users[0],
        [
            OrderItem(products[3], 3),
        ],
        "completed",
    ),
    Order(
        4,
        users[2],
        [
            OrderItem(products[4], 5),
            OrderItem(products[2], 1),
        ],
        "pending",
    ),
]


# ФУНКЦИОНАЛЬНЫЕ ОПЕРАЦИИ

def calculate_order_total(order: Order) -> float:
# Расчет общей стоимости заказа
    return sum(item.product.price * item.quantity for item in order.items)


def filter_orders_by_status(orders: List[Order], status: str) -> List[Order]:
# Фильтрация заказов по статусу
    return list(filter(lambda order: order.status == status, orders))


def get_top_expensive_orders(orders: List[Order], n: int) -> List[Order]:
# топ дорогих заказов
    return sorted(orders, key=calculate_order_total, reverse=True)[:n]


def apply_discount(order: Order, discount: float) -> Order:
# скидка
    discounted_items = [
        OrderItem(
            Product(
                item.product.id,
                item.product.name,
                item.product.price * (1 - discount),
                item.product.category,
            ),
            item.quantity,
        )
        for item in order.items
    ]
    return Order(order.id, order.user, discounted_items, order.status)


def group_orders_by_user(orders: List[Order]) -> dict:
# группировка по пользователю
    grouped = {}
    for order in orders:
        user_id = order.user.id
        if user_id not in grouped:
            grouped[user_id] = []
        grouped[user_id].append(order)
    return grouped


def calculate_user_spending(orders: List[Order]) -> List[tuple]:
# общие расходы пользователя
    spending = {}
    for order in orders:
        user_name = order.user.name
        if user_name not in spending:
            spending[user_name] = 0
        spending[user_name] += calculate_order_total(order)

    return sorted(spending.items(), key=lambda x: x[1], reverse=True)


def find_orders_by_category(orders: List[Order], category: str) -> List[Order]:
# товары по категории
    result = []
    for order in orders:
        for item in order.items:
            if item.product.category == category:
                result.append(order)
                break
    return result


def calculate_statistics(orders: List[Order]) -> dict:
# статистика
    if not orders:
        return {}

    totals = [calculate_order_total(order) for order in orders]

    return {
        "total_orders": len(orders),
        "completed_orders": len(filter_orders_by_status(orders, "completed")),
        "pending_orders": len(filter_orders_by_status(orders, "pending")),
        "total_revenue": sum(totals),
        "average_order": sum(totals) / len(totals),
        "max_order": max(totals),
        "min_order": min(totals),
    }

# demo

def main():

    print("\n" + " " * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА 6.")
    print("PYTHON\n" + " " * 70)

    print("\n" + "=" * 70)
    print("АНАЛИЗ ЗАКАЗОВ")
    print("=" * 70)

    print("\nЗавершенные заказы:")
    completed = filter_orders_by_status(orders, "completed")
    for order in completed:
        print(
            f"  Заказ {order.id}: {order.user.name} - ${calculate_order_total(order):.2f}"
        )

    total_revenue = sum(calculate_order_total(order) for order in completed)
    print(f"\nОбщая выручка (завершенные): ${total_revenue:.2f}")

    print("\nТоп-2 самых дорогих заказа:")
    top_orders = get_top_expensive_orders(orders, 2)
    for order in top_orders:
        print(f"  Заказ {order.id}: ${calculate_order_total(order):.2f}")

    print("\nПервый заказ со скидкой 10%:")
    print(f"  Было: ${calculate_order_total(orders[0]):.2f}")
    discounted = apply_discount(orders[0], 0.1)
    print(f"  После скидки: ${calculate_order_total(discounted):.2f}")

    print("\nЗаказы по пользователям:")
    grouped = group_orders_by_user(orders)
    for user_id, user_orders in grouped.items():
        user_name = next((u.name for u in users if u.id == user_id), "Unknown")
        print(f"  {user_name}: {len(user_orders)} заказов")

    print("\nОбщие расходы по пользователям:")
    spending = calculate_user_spending(orders)
    for name, total in spending:
        print(f"  {name}: ${total:.2f}")
    print("\nЗаказы с электроникой:")
    electronics_orders = find_orders_by_category(orders, "electronics")
    print(f"Найдено заказов: {len(electronics_orders)}")
    for order in electronics_orders:
        print(f"Заказ {order.id}: ${calculate_order_total(order):.2f}")

    print("\n" + "=" * 70)
    print("СТАТИСТИКА")
    print("=" * 70)

    stats = calculate_statistics(orders)
    print(f"Всего заказов: {stats['total_orders']}")
    print(f"Завершенных: {stats['completed_orders']}")
    print(f"В ожидании: {stats['pending_orders']}")
    print(f"Общая выручка: ${stats['total_revenue']:.2f}")
    print(f"Средний заказ: ${stats['average_order']:.2f}")
    print(f"Максимальный заказ: ${stats['max_order']:.2f}")
    print(f"Минимальный заказ: ${stats['min_order']:.2f}")
    print("\nЦепочка операций (функциональное программирование):")

    expensive_orders = [
        order
        for order in orders
        if order.status == "completed" and calculate_order_total(order) > 50
    ]

    discounted_orders = [apply_discount(order, 0.05) for order in expensive_orders]
    top_result = sorted(discounted_orders, key=calculate_order_total, reverse=True)[:1]

    if top_result:
        order = top_result[0]
        print(f"  Заказ {order.id}: ${calculate_order_total(order):.2f} (после скидки)")

    print("\nАльтернативная композиция")

    step1 = filter(lambda o: o.status == "completed", orders)
    step2 = filter(lambda o: calculate_order_total(o) > 50, step1)
    step3 = map(lambda o: apply_discount(o, 0.05), step2)
    step4 = sorted(step3, key=calculate_order_total, reverse=True)
    step5 = step4[:1] if step4 else []

    if step5:
        order = step5[0]
        print(f"  Результат: Заказ {order.id} - ${calculate_order_total(order):.2f}")

    print("\n" + "=" * 70)
    print("ВСЕ ОПЕРАЦИИ ЗАВЕРШЕНЫ!")
    print("=" * 70 + "\n")

# фп стиль

def functional_style_demo():
    print("\n" + "=" * 70)
    print("ФУНКЦИОНАЛЬНОЕ ПРОГРАММИРОВАНИЕ - PYTHON")
    print("=" * 70)

    print("\nMap - преобразование всех заказов в их стоимости:")
    totals = list(map(calculate_order_total, orders))
    print(f"  {totals}")

    print("\nFilter - только завершенные заказы:")
    completed = list(filter(lambda o: o.status == "completed", orders))
    print(f"  Найдено: {len(completed)} заказов")

    print("\nReduce - сумма всех заказов:")
    total_sum = reduce(lambda acc, order: acc + calculate_order_total(order), orders, 0)
    print(f"  Сумма: ${total_sum:.2f}")

    print("\nList comprehensions (Pythonic ФП):")
    expensive = [o for o in orders if calculate_order_total(o) > 100]
    print(f"Дорогие заказы (>$100): {len(expensive)} штук")

    print("\nКомбинирование операций:")
    result = [
        (o.id, calculate_order_total(o)) for o in orders if o.status == "completed"
    ]
    print(f"Завершенные: {result}")

    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    main()
    functional_style_demo()
