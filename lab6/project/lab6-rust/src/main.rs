// ЛАБОРАТОРНАЯ РАБОТА 6. RUST И СИСТЕМНОЕ ПРОГРАММИРОВАНИЕ

use std::rc::Rc;
use std::fmt::{Display, Formatter, Result as FmtResult};

// 1. БАЗОВЫЙ СИНТАКСИС И СИСТЕМА ВЛАДЕНИЯ

mod ownership {
    pub fn square(x: i32) -> i32 {
        x * x
    }

    pub fn add(a: i32, b: i32) -> i32 {
        a + b
    }

    pub fn apply_function<F>(f: F, x: i32) -> i32
    where
        F: Fn(i32) -> i32,
    {
        f(x)
    }

    pub fn demonstrate_ownership() {
        println!("\n{}", "=".repeat(70));
        println!("1. БАЗОВЫЙ СИНТАКСИС И СИСТЕМА ВЛАДЕНИЯ");
        println!("{}", "=".repeat(70));

        let s1 = String::from("hello");
        let s2 = s1;
        println!("После перемещения: s2 = {}", s2);

        let s3 = s2.clone();
        println!("После клонирования: s2 = {}, s3 = {}", s2, s3);

        let len = calculate_length(&s3);
        println!("Длина '{}' = {}", s3, len);

        let mut s4 = String::from("hello");
        modify_string(&mut s4);
        println!("После модификации: {}", s4);
    }

    fn calculate_length(s: &String) -> usize {
        s.len()
    }

    fn modify_string(s: &mut String) {
        s.push_str(", world!");
    }

    pub fn multiply(a: i32) -> impl Fn(i32) -> i32 {
        move |b| a * b
    }

    pub fn main() {
        println!("Квадрат 5: {}", square(5));
        println!("Сложение 3 и 4: {}", add(3, 4));
        println!("Применение функции: {}", apply_function(square, 3));

        let double = multiply(2);
        println!("Удвоение 7: {}", double(7));

        demonstrate_ownership();
    }
}

// 2. ИТЕРАТОРЫ И ЗАМЫКАНИЯ

mod iterators_closures {
    #[derive(Debug, Clone)]
    pub struct Product {
        pub id: u32,
        pub name: String,
        pub price: f64,
        pub category: String,
        pub in_stock: bool,
    }

    impl Product {
        pub fn new(id: u32, name: &str, price: f64, category: &str, in_stock: bool) -> Self {
            Product {
                id,
                name: name.to_string(),
                price,
                category: category.to_string(),
                in_stock,
            }
        }
    }

    pub fn demonstrate_iterators() {
        println!("\n{}", "=".repeat(70));
        println!("2. ИТЕРАТОРЫ И ЗАМЫКАНИЯ");
        println!("{}", "=".repeat(70));

        let products = vec![
            Product::new(1, "iPhone", 999.99, "electronics", true),
            Product::new(2, "MacBook", 1999.99, "electronics", false),
            Product::new(3, "T-shirt", 29.99, "clothing", true),
            Product::new(4, "Jeans", 79.99, "clothing", true),
            Product::new(5, "Book", 15.99, "education", false),
        ];

        // Map
        let product_names: Vec<String> = products.iter()
            .map(|p| p.name.clone())
            .collect();
        println!("Названия продуктов: {:?}", product_names);

        // Filter
        let available_products: Vec<&Product> = products.iter()
            .filter(|p| p.in_stock)
            .collect();
        println!("Доступные продукты: {} товаров", available_products.len());

        // Fold
        let total_price: f64 = products.iter()
            .map(|p| p.price)
            .fold(0.0, |acc, price| acc + price);
        println!("Общая стоимость: ${:.2}", total_price);

        // Цепочка преобразований
        let expensive_available: Vec<String> = products
            .iter()
            .filter(|p| p.in_stock && p.price > 50.0)
            .map(|p| p.name.to_uppercase())
            .collect();
        println!("Дорогие доступные товары: {:?}", expensive_available);

        // Замыкания с захватом
        let min_price = 50.0;
        let filtered_products: Vec<&Product> = products
            .iter()
            .filter(|p| p.price >= min_price)
            .collect();
        println!("Товары >= ${}: {} штук", min_price, filtered_products.len());

        // Ленивые итераторы
        let squares: Vec<i32> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            .iter()
            .map(|x| x * x)
            .take(3)
            .collect();
        println!("Квадраты первых 3 чисел: {:?}", squares);
    }

    pub fn process_products<F>(products: &[Product], predicate: F) -> Vec<&Product>
    where
        F: Fn(&Product) -> bool,
    {
        products.iter().filter(|p| predicate(p)).collect()
    }

    pub fn main() {
        demonstrate_iterators();

        let products = vec![
            Product::new(1, "iPhone", 999.99, "electronics", true),
            Product::new(2, "MacBook", 1999.99, "electronics", false),
        ];

        let electronics = process_products(&products, |p| p.category == "electronics");
        println!("Электроника: {} товаров", electronics.len());
    }
}

// 3. АЛГЕБРАИЧЕСКИЕ ТИПЫ ДАННЫХ И PATTERN MATCHING

mod pattern_matching {
    #[derive(Debug, Clone)]
    pub enum PaymentMethod {
        CreditCard { number: String, expiry: String },
        PayPal { email: String },
        Crypto { wallet: String },
    }

    #[derive(Debug, Clone)]
    pub enum OrderStatus {
        Pending,
        Processing,
        Shipped(String),
        Delivered(String),
        Cancelled { reason: String },
    }

    #[derive(Debug, Clone)]
    pub struct Order {
        pub id: u32,
        pub amount: f64,
        pub payment: PaymentMethod,
        pub status: OrderStatus,
    }

    impl Order {
        pub fn new(id: u32, amount: f64, payment: PaymentMethod, status: OrderStatus) -> Self {
            Order { id, amount, payment, status }
        }
    }

    pub fn process_payment(payment: &PaymentMethod) -> String {
        match payment {
            PaymentMethod::CreditCard { number, expiry } => {
                let last_four: String = number.chars().rev().take(4).collect();
                format!("Кредитная карта: ****{} (до {})", last_four, expiry)
            }
            PaymentMethod::PayPal { email } => {
                format!("PayPal: {}", email)
            }
            PaymentMethod::Crypto { wallet } => {
                let shortened: String = wallet.chars().take(10).collect();
                format!("Криптовалюта: {}...", shortened)
            }
        }
    }

    pub fn can_cancel_order(status: &OrderStatus) -> bool {
        match status {
            OrderStatus::Pending | OrderStatus::Processing => true,
            OrderStatus::Shipped(_) | OrderStatus::Delivered(_) | OrderStatus::Cancelled { .. } => false,
        }
    }

    pub fn demonstrate_pattern_matching() {
        println!("\n{}", "=".repeat(70));
        println!("3. PATTERN MATCHING И CASE CLASSES");
        println!("{}", "=".repeat(70));

        let orders = vec![
            Order::new(
                1,
                99.99,
                PaymentMethod::CreditCard {
                    number: "1234567812345678".to_string(),
                    expiry: "12/25".to_string()
                },
                OrderStatus::Pending
            ),
            Order::new(
                2,
                149.99,
                PaymentMethod::PayPal {
                    email: "user@example.com".to_string()
                },
                OrderStatus::Processing
            ),
            Order::new(
                3,
                199.99,
                PaymentMethod::Crypto {
                    wallet: "1A2b3C4d5E6f7G8h9I0j".to_string()
                },
                OrderStatus::Shipped("TRACK123".to_string())
            ),
        ];

        println!("Обработка платежей:");
        for order in &orders {
            let payment_info = process_payment(&order.payment);
            let cancelable = if can_cancel_order(&order.status) {
                "можно отменить"
            } else {
                "нельзя отменить"
            };
            println!("  Заказ {}: {} - {}", order.id, payment_info, cancelable);
        }

        println!("Статусы доставки:");
        for order in &orders {
            if let OrderStatus::Shipped(tracking) = &order.status {
                println!(" Заказ {} отправлен, трекинг: {}", order.id, tracking);
            }

            if let OrderStatus::Delivered(date) = &order.status {
                println!(" Заказ {} доставлен {}", order.id, date);
            }
        }
    }

    pub fn main() {
        demonstrate_pattern_matching();
    }
}

// 4. ОБРАБОТКА ОШИБОК С RESULT И OPTION

mod error_handling {
    use std::collections::HashMap;
    use std::fmt::{Display, Formatter, Result as FmtResult};

    #[derive(Debug, Clone)]
    pub struct User {
        pub id: u32,
        pub name: String,
        pub email: String,
    }

    #[derive(Debug, Clone)]
    pub struct Order {
        pub user_id: u32,
        pub amount: f64,
        pub status: String,
    }

    impl User {
        pub fn new(id: u32, name: &str, email: &str) -> Self {
            User {
                id,
                name: name.to_string(),
                email: email.to_string(),
            }
        }
    }

    pub type UserDatabase = HashMap<u32, User>;

    pub fn find_user(db: &UserDatabase, id: u32) -> Option<User> {
        db.get(&id).cloned()
    }

    pub fn validate_user(user: &User) -> Result<User, String> {
        if user.email.contains('@') {
            Ok(user.clone())
        } else {
            Err(format!("Invalid email for user {}", user.name))
        }
    }

    pub fn process_order(db: &UserDatabase, order: &Order) -> Result<(User, Order), String> {
        let user = find_user(db, order.user_id)
            .ok_or_else(|| format!("User {} not found", order.user_id))?;

        let _validated_user = validate_user(&user)?;

        Ok((user, order.clone()))
    }

    #[derive(Debug)]
    pub enum OrderError {
        UserNotFound(u32),
        InvalidUser(String),
        PaymentFailed(String),
    }

    impl Display for OrderError {
        fn fmt(&self, f: &mut Formatter) -> FmtResult {
            match self {
                OrderError::UserNotFound(id) => write!(f, "User {} not found", id),
                OrderError::InvalidUser(msg) => write!(f, "Invalid user: {}", msg),
                OrderError::PaymentFailed(msg) => write!(f, "Payment failed: {}", msg),
            }
        }
    }

    pub fn demonstrate_error_handling() {
        println!("\n{}", "=".repeat(70));
        println!("4. ОБРАБОТКА ОШИБОК");
        println!("{}", "=".repeat(70));

        let mut user_db = UserDatabase::new();
        user_db.insert(1, User::new(1, "John Doe", "john@example.com"));
        user_db.insert(2, User::new(2, "Jane Smith", "jane@example.com"));
        user_db.insert(3, User::new(3, "Invalid User", "invalid-email"));

        let orders = vec![
            Order { user_id: 1, amount: 99.99, status: "completed".to_string() },
            Order { user_id: 2, amount: 149.99, status: "pending".to_string() },
            Order { user_id: 4, amount: 199.99, status: "shipped".to_string() },
            Order { user_id: 3, amount: 79.99, status: "processing".to_string() },
        ];

        println!("Обработка заказов:");
        for order in &orders {
            match process_order(&user_db, order) {
                Ok((user, order)) => {
                    println!("Успешно обработан заказ для {}: ${:.2}", user.name, order.amount);
                }
                Err(error) => {
                    println!("Ошибка: {}", error);
                }
            }
        }

        let user_1_email = find_user(&user_db, 1)
            .map(|user| user.email)
            .unwrap_or_else(|| "Unknown".to_string());
        println!("Email пользователя 1: {}", user_1_email);

        let result = find_user(&user_db, 1)
            .and_then(|user| validate_user(&user).ok())
            .map(|user| user.name);
        println!("Результат цепочки: {:?}", result);
    }

    pub fn main() {
        demonstrate_error_handling();
    }
}

// 5. ФУНКЦИОНАЛЬНЫЕ СТРУКТУРЫ ДАННЫХ

mod functional_data_structures {
    use std::rc::Rc;

    #[derive(Debug, Clone)]
    pub enum List<T: Clone> {
        Empty,
        Cons(T, Rc<List<T>>),
    }

    impl<T: Clone> List<T> {
        pub fn new() -> Self {
            List::Empty
        }

        pub fn prepend(&self, elem: T) -> Self {
            List::Cons(elem, Rc::new(self.clone()))
        }

        pub fn head(&self) -> Option<&T> {
            match self {
                List::Cons(head, _) => Some(head),
                List::Empty => None,
            }
        }
    }

    #[derive(Debug, Clone)]
    pub struct ImmutablePoint {
        pub x: f64,
        pub y: f64,
    }

    impl ImmutablePoint {
        pub fn new(x: f64, y: f64) -> Self {
            ImmutablePoint { x, y }
        }

        pub fn translate(&self, dx: f64, dy: f64) -> Self {
            ImmutablePoint {
                x: self.x + dx,
                y: self.y + dy,
            }
        }

        pub fn distance(&self, other: &ImmutablePoint) -> f64 {
            ((self.x - other.x).powi(2) + (self.y - other.y).powi(2)).sqrt()
        }
    }

    pub fn demonstrate_functional_structures() {
        println!("\n{}", "=".repeat(70));
        println!("5. ФУНКЦИОНАЛЬНЫЕ СТРУКТУРЫ ДАННЫХ");
        println!("{}", "=".repeat(70));

        let list = List::new()
            .prepend(3)
            .prepend(2)
            .prepend(1);

        println!("Функциональный список создан");

        if let Some(head) = list.head() {
            println!("Голова списка: {}", head);
        }

        let point1 = ImmutablePoint::new(0.0, 0.0);
        let point2 = point1.translate(3.0, 4.0);

        let distance = point1.distance(&point2);
        println!("Расстояние между ({:.1}, {:.1}) и ({:.1}, {:.1}) = {:.2}",
            point1.x, point1.y, point2.x, point2.y, distance);
    }

    pub fn main() {
        demonstrate_functional_structures();
    }
}

// 6. ПРАКТИЧЕСКИЕ ЗАДАНИЯ

mod practical_tasks {
    use crate::iterators_closures::Product;

    pub fn analyze_products(products: &[Product]) -> (f64, usize, Vec<&Product>) {
        let total_price: f64 = products.iter().map(|p| p.price).sum();
        let average_price = if products.is_empty() { 0.0 } else { total_price / products.len() as f64 };

        let available_count = products.iter().filter(|p| p.in_stock).count();

        let expensive: Vec<&Product> = products.iter()
            .filter(|p| p.price > 100.0)
            .collect();

        (average_price, available_count, expensive)
    }

    pub struct Fibonacci {
        current: u64,
        next: u64,
    }

    impl Fibonacci {
        pub fn new() -> Self {
            Fibonacci { current: 0, next: 1 }
        }
    }

    impl Iterator for Fibonacci {
        type Item = u64;

        fn next(&mut self) -> Option<Self::Item> {
            let result = self.current;
            self.current = self.next;
            self.next = result + self.current;
            Some(result)
        }
    }

    pub fn demonstrate_practical_tasks() {
        println!("\n{}", "=".repeat(70));
        println!("6. ПРАКТИЧЕСКИЕ ЗАДАНИЯ");
        println!("{}", "=".repeat(70));

        let products = vec![
            Product::new(1, "iPhone", 999.99, "electronics", true),
            Product::new(2, "Shirt", 29.99, "clothing", true),
            Product::new(3, "MacBook", 1999.99, "electronics", false),
            Product::new(4, "Jeans", 79.99, "clothing", true),
        ];

        let (avg_price, available, expensive) = analyze_products(&products);
        println!("Анализ продуктов:");
        println!("  Средняя цена: ${:.2}", avg_price);
        println!("  Доступных товаров: {}", available);
        println!("  Дорогих товаров (>100): {}", expensive.len());

        println!("Числа Фибоначчи (первые 10):");
        let fib_sequence: Vec<u64> = Fibonacci::new().take(10).collect();
        println!("  {:?}", fib_sequence);
    }

    pub fn main() {
        demonstrate_practical_tasks();
    }
}

// main

fn main() {
    println!("\n{}", " ".repeat(70));
    println!("ЛАБОРАТОРНАЯ РАБОТА 6. RUST + СП");
    println!("{}\n", " ".repeat(70));

    ownership::main();
    iterators_closures::main();
    pattern_matching::main();
    error_handling::main();
    functional_data_structures::main();
    practical_tasks::main();
}
