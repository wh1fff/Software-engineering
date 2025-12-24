
// ЛАБОРАТОРНАЯ РАБОТА 6. JAVASCRIPT И ФП

// 1. ФУНКЦИИ ВЫСШЕГО ПОРЯДКА И МЕТОДЫ МАССИВОВ

console.log('\n' + '='.repeat(70));
console.log('1. ФУНКЦИИ ВЫСШЕГО ПОРЯДКА И МЕТОДЫ МАССИВОВ');
console.log('='.repeat(70));

const products = [
    { id: 1, name: 'iPhone', price: 999, category: 'electronics', inStock: true },
    { id: 2, name: 'MacBook', price: 1999, category: 'electronics', inStock: false },
    { id: 3, name: 'T-shirt', price: 29, category: 'clothing', inStock: true },
    { id: 4, name: 'Jeans', price: 79, category: 'clothing', inStock: true },
    { id: 5, name: 'Book', price: 15, category: 'education', inStock: false }
];

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Map - преобразование массива
const productNames = products.map(product => product.name);
console.log('Названия продуктов (map):', productNames);

const discountedPrices = products.map(product => ({
    ...product,
    price: product.price * 0.9 // 10% скидка
}));
console.log('Продукты со скидкой (10%):', discountedPrices.slice(0, 2));

// Filter - фильтрация массива
const availableProducts = products.filter(product => product.inStock);
console.log('Доступные продукты (filter):', availableProducts.map(p => p.name));

const expensiveProducts = products.filter(product => product.price > 100);
console.log('Дорогие продукты (> $100):', expensiveProducts.map(p => p.name));

// Reduce - свертка массива
const totalPrice = products.reduce((sum, product) => sum + product.price, 0);
console.log('Общая стоимость всех продуктов:', totalPrice);

const productsByCategory = products.reduce((acc, product) => {
    const category = product.category;
    if (!acc[category]) {
        acc[category] = [];
    }
    acc[category].push(product);
    return acc;
}, {});
console.log('Продукты по категориям:', productsByCategory);

// Цепочка методов (method chaining)
const chainResult = products
    .filter(product => product.inStock)
    .map(product => ({
        name: product.name.toUpperCase(),
        price: product.price
    }))
    .reduce((total, product) => total + product.price, 0);

console.log('Сумма доступных продуктов (цепочка):', chainResult);

// 2. СТРЕЛОЧНЫЕ ФУНКЦИИ И ЗАМЫКАНИЯ

console.log('\n' + '='.repeat(70));
console.log('2. СТРЕЛОЧНЫЕ ФУНКЦИИ И ЗАМЫКАНИЯ');
console.log('='.repeat(70));

// Стрелочные функции разных стилей
const square = x => x * x;
const add = (a, b) => a + b;
const greet = name => `👋 Hello, ${name}!`;

console.log('square(5):', square(5));
console.log('add(3, 4):', add(3, 4));
console.log(greet('John'));

// Замыкания - функция запоминает переменные из окружения
const createCounter = () => {
    let count = 0;
    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count,
        reset: () => { count = 0; return count; }
    };
};

const counter = createCounter();
console.log('\nТест замыканий (счётчик):');
console.log('  increment():', counter.increment()); // 1
console.log('  increment():', counter.increment()); // 2
console.log('  decrement():', counter.decrement()); // 1
console.log('  getCount():', counter.getCount());   // 1

// Каррирование - преобразование функции с несколькими аргументами
const multiply = a => b => a * b;
const double = multiply(2);
const triple = multiply(3);

console.log('\nТест каррирования:');
console.log('  double(5):', double(5));   // 10
console.log('  triple(5):', triple(5));   // 15

// Функциональная композиция
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);

const add5 = x => x + 5;
const multiply3 = x => x * 3;
const subtract10 = x => x - 10;

const composed = compose(subtract10, multiply3, add5);
const piped = pipe(add5, multiply3, subtract10);

console.log('\nТест функциональной композиции:');
console.log('  compose(subtract10, multiply3, add5)(5):', composed(5)); // ((5+5)*3)-10 = 40
console.log('  pipe(add5, multiply3, subtract10)(5):', piped(5));       // ((5+5)*3)-10 = 40

// 3. ИММУТАБЕЛЬНЫЕ ОБНОВЛЕНИЯ И РАБОТА С ОБЪЕКТАМИ

console.log('\n' + '='.repeat(70));
console.log('3. ИММУТАБЕЛЬНЫЕ ОБНОВЛЕНИЯ И РАБОТА С ОБЪЕКТАМИ');
console.log('='.repeat(70));

const user = {
    id: 1,
    name: 'John Doe',
    address: {
        city: 'New York',
        street: '123 Main St',
        coordinates: {
            lat: 40.7128,
            lng: -74.0060
        }
    },
    preferences: {
        theme: 'dark',
        notifications: true
    }
};

const cart = [
    { id: 1, name: 'Product A', quantity: 2 },
    { id: 2, name: 'Product B', quantity: 1 }
];

// Иммутабельное обновление объекта (spread оператор)
const updatedUser = {
    ...user,
    name: 'Jane Doe',
    preferences: {
        ...user.preferences,
        theme: 'light'
    }
};

console.log('Исходный пользователь:', user.name, user.preferences.theme);
console.log('Обновлённый пользователь:', updatedUser.name, updatedUser.preferences.theme);
console.log('Оригинал не изменился:', user.name, user.preferences.theme);

// Иммутабельное добавление в массив
const newCartItem = { id: 3, name: 'Product C', quantity: 1 };
const updatedCart = [...cart, newCartItem];
console.log('\nИсходная корзина (длина):', cart.length);
console.log('Обновлённая корзина (длина):', updatedCart.length);

// Иммутабельное обновление элемента массива
const updatedCartQuantity = cart.map(item =>
    item.id === 1 ? { ...item, quantity: item.quantity + 1 } : item
);
console.log('Обновлено количество Product A:', updatedCartQuantity[0].quantity);
console.log('Оригинал не изменился:', cart[0].quantity);

// Иммутабельное удаление из массива
const filteredCart = cart.filter(item => item.id !== 2);
console.log('Корзина после удаления Product B (длина):', filteredCart.length);


// 4. АСИНХРОННОЕ ФУНКЦИОНАЛЬНОЕ ПРОГРАММИРОВАНИЕ

console.log('\n' + '='.repeat(70));
console.log('4. АСИНХРОННОЕ ФУНКЦИОНАЛЬНОЕ ПРОГРАММИРОВАНИЕ');
console.log('='.repeat(70));

// Симуляция API запроса
const simulateApiCall = (data, delay = 500) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (data) {
                resolve(data);
            } else {
                reject(new Error('No data provided'));
            }
        }, delay);
    });
};

// Функциональная обработка асинхронных операций
const processUserDataAsync = async (userId) => {
    try {
        const user = await simulateApiCall({ id: userId, name: 'John Doe', email: 'john@example.com' });
        const posts = await simulateApiCall([
            { id: 1, content: 'First post about JavaScript' },
            { id: 2, content: 'Learning functional programming' }
        ]);

        return {
            ...user,
            posts: posts.map(post => ({
                ...post,
                excerpt: post.content.substring(0, 30) + '...'
            }))
        };
    } catch (error) {
        console.error('❌ Error processing user data:', error.message);
        throw error;
    }
};

// Тест асинхронной функции
console.log('Тест асинхронной обработки данных:');
processUserDataAsync(1).then(result => {
    console.log('✅ Обработанные данные пользователя:');
    console.log('  Имя:', result.name);
    console.log('  Email:', result.email);
    console.log('  Посты:', result.posts.length);
});

// Композиция асинхронных функций
const asyncPipe = (...fns) => x => fns.reduce(async (acc, fn) => fn(await acc), x);

const validateInput = async (data) => {
    console.log('  ▪ Валидация входных данных...');
    if (!data.email) throw new Error('Email is required');
    return data;
};

const sanitizeData = async (data) => {
    console.log('  ▪ Санитизация данных...');
    return {
        ...data,
        email: data.email.toLowerCase().trim()
    };
};

const saveToDatabase = async (data) => {
    console.log('  ▪ Сохранение в базу данных...');
    return new Promise(resolve => {
        setTimeout(() => {
            resolve({ ...data, id: Math.random(), createdAt: new Date().toISOString() });
        }, 500);
    });
};

const userRegistration = asyncPipe(
    validateInput,
    sanitizeData,
    saveToDatabase
);

// Тест композиции асинхронных функций
console.log('\nТест регистрации пользователя:');
const userData = { email: '  JOHN@EXAMPLE.COM  ', name: 'John' };
userRegistration(userData).then(result => {
    console.log('✅ Пользователь зарегистрирован:');
    console.log('  ID:', result.id.toFixed(4));
    console.log('  Email:', result.email);
    console.log('  Имя:', result.name);
}).catch(error => {
    console.error('❌ Ошибка регистрации:', error.message);
});


// 5. ПРАКТИЧЕСКИЕ ЗАДАНИЯ

console.log('\n' + '='.repeat(70));
console.log('5. ПРАКТИЧЕСКИЕ ЗАДАНИЯ');
console.log('='.repeat(70));

// ЗАДАНИЕ 1: Обработка массива пользователей
console.log('\n--- ЗАДАНИЕ 1: Обработка массива пользователей ---');

const processUsers = (users) => {
    const avgAge = users.reduce((sum, user) => sum + user.age, 0) / users.length;

    const usersByCity = users.reduce((acc, user) => {
        const city = user.city;
        acc[city] = (acc[city] || 0) + 1;
        return acc;
    }, {});

    const activeEmails = users
        .filter(user => user.active)
        .map(user => user.email);

    return {
        averageAge: avgAge.toFixed(1),
        usersByCity,
        activeUserEmails: activeEmails
    };
};

const users = [
    { name: 'John', age: 25, city: 'New York', active: true, email: 'john@example.com' },
    { name: 'Jane', age: 30, city: 'Boston', active: true, email: 'jane@example.com' },
    { name: 'Bob', age: 28, city: 'New York', active: false, email: 'bob@example.com' }
];

const usersAnalysis = processUsers(users);
console.log('Анализ пользователей:');
console.log('  Средний возраст:', usersAnalysis.averageAge);
console.log('  Пользователи по городам:', usersAnalysis.usersByCity);
console.log('  Email активных пользователей:', usersAnalysis.activeUserEmails);

// ЗАДАНИЕ 2: Дебаунсинг функции
console.log('\n--- ЗАДАНИЕ 2: Дебаунсинг функции ---');

const debounce = (func, delay) => {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func(...args);
        }, delay);
    };
};

const searchHandler = (query) => {
    console.log(`  🔍 Поиск по запросу: "${query}"`);
};

const debouncedSearch = debounce(searchHandler, 500);

console.log('Тест дебаунсинга (3 вызова, только последний выполнится):');
debouncedSearch('jav');
debouncedSearch('java');
debouncedSearch('javascript');

setTimeout(() => {
    console.log('(ждём 600ms для выполнения дебаунса...)');
}, 100);

// ЗАДАНИЕ 3: Мемоизация функции
console.log('\n--- ЗАДАНИЕ 3: Мемоизация функции ---');

const memoize = (func) => {
    const cache = new Map();
    return function (...args) {
        const key = JSON.stringify(args);
        if (cache.has(key)) {
            console.log('  💾 Результат из кэша');
            return cache.get(key);
        }
        console.log('  🔄 Вычисление...');
        const result = func(...args);
        cache.set(key, result);
        return result;
    };
};

const fibonacci = (n) => {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
};

const memoizedFib = memoize(fibonacci);

console.log('Тест мемоизации (fibonacci):');
console.log('  fib(5):', memoizedFib(5));
console.log('  fib(5) ещё раз:', memoizedFib(5)); // Будет из кэша


// 6. УТИЛИТЫ И ХЕЛПЕРЫ

console.log('\n' + '='.repeat(70));
console.log('6. УТИЛИТЫ И ХЕЛПЕРЫ');
console.log('='.repeat(70));

// Throttling - выполняет функцию максимум один раз за время delay
const throttle = (func, delay) => {
    let lastCall = 0;
    return function (...args) {
        const now = Date.now();
        if (now - lastCall >= delay) {
            func(...args);
            lastCall = now;
        }
    };
};

// Partial application - зафиксировать некоторые аргументы
const partial = (func, ...args) => {
    return (...moreArgs) => func(...args, ...moreArgs);
};

const addThreeNumbers = (a, b, c) => a + b + c;
const addFiveToTwo = partial(addThreeNumbers, 5, 2);
console.log('Partial application: addFiveToTwo(3) =', addFiveToTwo(3)); // 5+2+3 = 10

// Flip - поменять порядок аргументов
const flip = (func) => {
    return (...args) => func(...args.reverse());
};

const subtract = (a, b) => a - b;
const flippedSubtract = flip(subtract);
console.log('Flip: subtract(10, 3) =', subtract(10, 3)); // 7
console.log('Flip: flippedSubtract(10, 3) =', flippedSubtract(10, 3)); // -7


// demo
console.log('\n' + '='.repeat(70));
console.log('ИТОГОВАЯ ДЕМОНСТРАЦИЯ: КОМБИНИРОВАНИЕ ВСЕХ КОНЦЕПЦИЙ');
console.log('='.repeat(70));

// Комплексный пример: обработка заказов
const orders = [
    { id: 1, userId: 1, items: [{ price: 100 }, { price: 50 }], status: 'delivered' },
    { id: 2, userId: 2, items: [{ price: 200 }], status: 'pending' },
    { id: 3, userId: 1, items: [{ price: 75 }, { price: 25 }, { price: 50 }], status: 'delivered' }
];

// Функциональный pipeline для анализа заказов
const orderAnalytics = orders
    .filter(order => order.status === 'delivered')
    .map(order => ({
        ...order,
        total: order.items.reduce((sum, item) => sum + item.price, 0)
    }))
    .reduce((acc, order) => {
        const user = acc[order.userId] || { totalSpent: 0, orderCount: 0 };
        return {
            ...acc,
            [order.userId]: {
                totalSpent: user.totalSpent + order.total,
                orderCount: user.orderCount + 1
            }
        };
    }, {});

console.log('Аналитика доставленных заказов:');
console.log(orderAnalytics);

console.log('\n' + '='.repeat(70));
console.log('✅ ВСЕ ПРИМЕРЫ ВЫПОЛНЕНЫ УСПЕШНО!');
console.log('='.repeat(70) + '\n');
