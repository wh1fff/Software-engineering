// ЛАБОРАТОРНАЯ РАБОТА 6. JAVASCRIPT

// модель данных

class User {
    constructor(id, name, email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    static new(id, name, email) {
        return new User(id, name, email);
    }
}

class Product {
    constructor(id, name, price, category) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.category = category;
    }

    static new(id, name, price, category) {
        return new Product(id, name, price, category);
    }
}

class OrderItem {
    constructor(product, quantity) {
        this.product = product;
        this.quantity = quantity;
    }

    static new(product, quantity) {
        return new OrderItem(product, quantity);
    }
}

class Order {
    constructor(id, user, items, status) {
        this.id = id;
        this.user = user;
        this.items = items;
        this.status = status;
    }

    static new(id, user, items, status) {
        return new Order(id, user, items, status);
    }
}

// инициализация данных

const users = [
    User.new(1, "John Doe", "john@example.com"),
    User.new(2, "Jane Smith", "jane@example.com"),
    User.new(3, "Bob Johnson", "bob@example.com"),
];

const products = [
    Product.new(1, "iPhone", 999.99, "electronics"),
    Product.new(2, "MacBook", 1999.99, "electronics"),
    Product.new(3, "T-shirt", 29.99, "clothing"),
    Product.new(4, "Jeans", 79.99, "clothing"),
    Product.new(5, "Book", 15.99, "books"),
];

const orders = [
    Order.new(1, users[0], [
        OrderItem.new(products[0], 1),
        OrderItem.new(products[2], 2),
    ], "completed"),
    Order.new(2, users[1], [
        OrderItem.new(products[1], 1),
    ], "pending"),
    Order.new(3, users[0], [
        OrderItem.new(products[3], 3),
    ], "completed"),
    Order.new(4, users[2], [
        OrderItem.new(products[4], 5),
        OrderItem.new(products[2], 1),
    ], "pending"),
];

// функции

// расчет стоимости заказа
const calculateOrderTotal = (order) =>
    order.items.reduce((total, item) => total + (item.product.price * item.quantity), 0);

// статус-фильтр
const filterOrdersByStatus = (orders, status) =>
    orders.filter(order => order.status === status);

// топ заказов по цене
const getTopExpensiveOrders = (orders, n) =>
    [...orders]
        .sort((a, b) => calculateOrderTotal(b) - calculateOrderTotal(a))
        .slice(0, n);

// скидка
const applyDiscount = (order, discount) => ({
    ...order,
    items: order.items.map(item => ({
        ...item,
        product: {
            ...item.product,
            price: item.product.price * (1 - discount)
        }
    }))
});

// группировка по пользователю
const groupOrdersByUser = (orders) =>
    orders.reduce((acc, order) => {
        if (!acc[order.user.id]) {
            acc[order.user.id] = [];
        }
        acc[order.user.id].push(order);
        return acc;
    }, {});

// расходы пользователя
const calculateUserSpending = (orders) => {
    const spending = orders.reduce((acc, order) => {
        const name = order.user.name;
        acc[name] = (acc[name] || 0) + calculateOrderTotal(order);
        return acc;
    }, {});

    return Object.entries(spending)
        .sort(([, a], [, b]) => b - a);
};

// поиск по категориям
const findOrdersByCategory = (orders, category) =>
    orders.filter(order =>
        order.items.some(item => item.product.category === category)
    );

// статистика
const calculateStatistics = (orders) => {
    if (orders.length === 0) return {};

    const totals = orders.map(calculateOrderTotal);

    return {
        total_orders: orders.length,
        completed_orders: filterOrdersByStatus(orders, "completed").length,
        pending_orders: filterOrdersByStatus(orders, "pending").length,
        total_revenue: totals.reduce((a, b) => a + b, 0),
        average_order: totals.reduce((a, b) => a + b, 0) / totals.length,
        max_order: Math.max(...totals),
        min_order: Math.min(...totals),
    };
};

// demo

function main() {
    console.log("\n" + " ".repeat(70));
    console.log("ЛАБОРАТОРНАЯ РАБОТА 6.");
    console.log("JS\n" + " ".repeat(70));

    console.log("\n" + "=".repeat(70));
    console.log("анализ заказов - JS");
    console.log("=".repeat(70));

// завершенные заказы
    console.log("\nЗавершенные заказы:");
    const completed = filterOrdersByStatus(orders, "completed");
    completed.forEach(order => {
        console.log(`  Заказ ${order.id}: ${order.user.name} - $${calculateOrderTotal(order).toFixed(2)}`);
    });

// общая выручка
    const totalRevenue = completed.reduce((sum, order) => sum + calculateOrderTotal(order), 0);
    console.log(`\nОбщая выручка (завершенные): $${totalRevenue.toFixed(2)}`);

// топ заказов по цене
    console.log("\nТоп 2 самых дорогих заказа:");
    const topOrders = getTopExpensiveOrders(orders, 2);
    topOrders.forEach(order => {
        console.log(`Заказ ${order.id}: $${calculateOrderTotal(order).toFixed(2)}`);
    });

// скидка
    console.log("\nПервый заказ со скидкой 10%:");
    console.log(`Было: $${calculateOrderTotal(orders[0]).toFixed(2)}`);
    const discounted = applyDiscount(orders[0], 0.1);
    console.log(`После скидки: $${calculateOrderTotal(discounted).toFixed(2)}`);

// группировка
    console.log("\nЗаказы по пользователям:");
    const grouped = groupOrdersByUser(orders);
    Object.entries(grouped).forEach(([userId, userOrders]) => {
        const userName = users.find(u => u.id == userId)?.name || "Unknown";
        console.log(`  ${userName}: ${userOrders.length} заказов`);
    });

// расходы
    console.log("\nОбщие расходы по пользователям:");
    const spending = calculateUserSpending(orders);
    spending.forEach(([name, total]) => {
        console.log(`  ${name}: $${total.toFixed(2)}`);
    });

// по категориям
    console.log("\nЗаказы с электроникой:");
    const electronics = findOrdersByCategory(orders, "electronics");
    console.log(`Найдено заказов: ${electronics.length}`);
    electronics.forEach(order => {
        console.log(`Заказ ${order.id}: $${calculateOrderTotal(order).toFixed(2)}`);
    });

// статистика
    console.log("\n" + "=".repeat(70));
    console.log("статистика");
    console.log("=".repeat(70));

    const stats = calculateStatistics(orders);
    console.log(`Всего заказов: ${stats.total_orders}`);
    console.log(`Завершенных: ${stats.completed_orders}`);
    console.log(`В ожидании: ${stats.pending_orders}`);
    console.log(`Общая выручка: $${stats.total_revenue.toFixed(2)}`);
    console.log(`Средний заказ: $${stats.average_order.toFixed(2)}`);
    console.log(`Максимальный заказ: $${stats.max_order.toFixed(2)}`);
    console.log(`Минимальный заказ: $${stats.min_order.toFixed(2)}`);

// композиция
    console.log("\nЦепочка операций (функциональное программирование):");
    const expensive = filterOrdersByStatus(orders, "completed")
        .filter(order => calculateOrderTotal(order) > 50);
    const discountedExpensive = expensive.map(o => applyDiscount(o, 0.05));
    const topResult = getTopExpensiveOrders(discountedExpensive, 1);

    if (topResult.length > 0) {
        const order = topResult[0];
        console.log(`  Заказ ${order.id}: $${calculateOrderTotal(order).toFixed(2)} (после скидки)`);
    }

    console.log("\n" + "=".repeat(70));
    console.log(" все операции завершены");
    console.log("=".repeat(70) + "\n");
}

// run

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        User, Product, OrderItem, Order,
        calculateOrderTotal, filterOrdersByStatus, getTopExpensiveOrders,
        applyDiscount, groupOrdersByUser, calculateUserSpending,
        findOrdersByCategory, calculateStatistics
    };
}

main();
