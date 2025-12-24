// ЛАБОРАТОРНАЯ РАБОТА 6. SCALA

object ComparisonScala {

  // Модель данных (Case Classes)
  case class User(id: Int, name: String, email: String)
  case class Product(id: Int, name: String, price: Double, category: String)
  case class OrderItem(product: Product, quantity: Int)
  case class Order(id: Int, user: User, items: List[OrderItem], status: String)

 // Инициализация данных

  val users = List(
    User(1, "John Doe", "john@example.com"),
    User(2, "Jane Smith", "jane@example.com"),
    User(3, "Bob Johnson", "bob@example.com")
  )

  val products = List(
    Product(1, "iPhone", 999.99, "electronics"),
    Product(2, "MacBook", 1999.99, "electronics"),
    Product(3, "T-shirt", 29.99, "clothing"),
    Product(4, "Jeans", 79.99, "clothing"),
    Product(5, "Book", 15.99, "books")
  )

  val orders = List(
    Order(1, users(0), List(
      OrderItem(products(0), 1),
      OrderItem(products(2), 2)
    ), "completed"),
    Order(2, users(1), List(
      OrderItem(products(1), 1)
    ), "pending"),
    Order(3, users(0), List(
      OrderItem(products(3), 3)
    ), "completed"),
    Order(4, users(2), List(
      OrderItem(products(4), 5),
      OrderItem(products(2), 1)
    ), "pending")
  )

 // Функции обработки

  // Расчет стоимости заказа
  def calculateOrderTotal(order: Order): Double =
    order.items.map(item => item.product.price * item.quantity).sum

  // Фильтрация по статусу
  def filterOrdersByStatus(orders: List[Order], status: String): List[Order] =
    orders.filter(_.status == status)

  // топ дорогих заказов
  def getTopExpensiveOrders(orders: List[Order], n: Int): List[Order] =
    orders.sortBy(calculateOrderTotal)(Ordering[Double].reverse).take(n)

  // Применить скидку
  def applyDiscount(order: Order, discount: Double): Order = {
    val discountedItems = order.items.map { item =>
      item.copy(product = item.product.copy(
        price = item.product.price * (1 - discount)
      ))
    }
    order.copy(items = discountedItems)
  }

  // Группировка по пользователям
  def groupOrdersByUser(orders: List[Order]): Map[Int, List[Order]] =
    orders.groupBy(_.user.id)

  // Расходы пользователей
  def calculateUserSpending(orders: List[Order]): List[(String, Double)] = {
    val spending = orders
      .groupBy(_.user.name)
      .mapValues(userOrders => userOrders.map(calculateOrderTotal).sum)
    spending.toList.sortBy(_._2)(Ordering[Double].reverse)
  }

  // Поиск по категориям
  def findOrdersByCategory(orders: List[Order], category: String): List[Order] =
    orders.filter(order =>
      order.items.exists(_.product.category == category)
    )

  // Статистика
  case class Statistics(
    total_orders: Int,
    completed_orders: Int,
    pending_orders: Int,
    total_revenue: Double,
    average_order: Double,
    max_order: Double,
    min_order: Double
  )

  def calculateStatistics(orders: List[Order]): Option[Statistics] = {
    if (orders.isEmpty) None
    else {
      val totals = orders.map(calculateOrderTotal)
      Some(Statistics(
        total_orders = orders.length,
        completed_orders = filterOrdersByStatus(orders, "completed").length,
        pending_orders = filterOrdersByStatus(orders, "pending").length,
        total_revenue = totals.sum,
        average_order = totals.sum / totals.length,
        max_order = totals.max,
        min_order = totals.min
      ))
    }
  }

  // ============================================================================
  // Демонстрация
  // ============================================================================

  def main(args: Array[String]): Unit = {
    println("\n" + " " * 70)
    println("ЛАБОРАТОРНАЯ РАБОТА 6")
    println("SCALA\n" + " " * 70)

    println("\n" + "=" * 70)
    println("АНАЛИЗ ЗАКАЗОВ")
    println("=" * 70)

    // 1. Завершенные заказы
    println("\nЗавершенные заказы:")
    val completed = filterOrdersByStatus(orders, "completed")
    completed.foreach { order =>
      printf("Заказ %d: %s - $%.2f\n", order.id, order.user.name, calculateOrderTotal(order))
    }

    // 2. Общая выручка
    val totalRevenue = completed.map(calculateOrderTotal).sum
    printf("\nОбщая выручка (завершенные): $%.2f\n", totalRevenue)

    // 3. Топ дорогие заказы
    println("\nТоп-2 самых дорогих заказа:")
    val topOrders = getTopExpensiveOrders(orders, 2)
    topOrders.foreach { order =>
      printf("Заказ %d: $%.2f\n", order.id, calculateOrderTotal(order))
    }

    // 4. Скидка
    println("\nПервый заказ со скидкой 10%:")
    printf("  Было: $%.2f\n", calculateOrderTotal(orders.head))
    val discounted = applyDiscount(orders.head, 0.1)
    printf("  После скидки: $%.2f\n", calculateOrderTotal(discounted))

    // 5. Группировка
    println("\nЗаказы по пользователям:")
    val grouped = groupOrdersByUser(orders)
    grouped.foreach { case (userId, userOrders) =>
      val userName = users.find(_.id == userId).map(_.name).getOrElse("Unknown")
      println(s"  $userName: ${userOrders.length} заказов")
    }

    // 6. Расходы
    println("\nОбщие расходы по пользователям:")
    val spending = calculateUserSpending(orders)
    spending.foreach { case (name, total) =>
      printf("  %s: $%.2f\n", name, total)
    }

    // 7. По категориям
    println("\nЗаказы с электроникой:")
    val electronics = findOrdersByCategory(orders, "electronics")
    println(s"  Найдено заказов: ${electronics.length}")
    electronics.foreach { order =>
      printf("    Заказ %d: $%.2f\n", order.id, calculateOrderTotal(order))
    }

    // 8. Статистика
    println("\n" + "=" * 70)
    println("СТАТИСТИКА")
    println("=" * 70)

    calculateStatistics(orders).foreach { stats =>
      println(s"Всего заказов: ${stats.total_orders}")
      println(s"Завершенных: ${stats.completed_orders}")
      println(s"В ожидании: ${stats.pending_orders}")
      printf("Общая выручка: $%.2f\n", stats.total_revenue)
      printf("Средний заказ: $%.2f\n", stats.average_order)
      printf("Максимальный заказ: $%.2f\n", stats.max_order)
      printf("Минимальный заказ: $%.2f\n", stats.min_order)
    }

    println("\nЦепочка операций")
    val result = orders
      .filter(_.status == "completed")
      .filter(order => calculateOrderTotal(order) > 50)
      .map(order => applyDiscount(order, 0.05))
      .sortBy(calculateOrderTotal)(Ordering[Double].reverse)
      .take(1)

    result.foreach { order =>
      printf("  Заказ %d: $%.2f (после скидки)\n", order.id, calculateOrderTotal(order))
    }

    println("\n" + "=" * 70)
    println("ВСЕ ОПЕРАЦИИ ЗАВЕРШЕНЫ!")
    println("=" * 70 + "\n")
  }
}