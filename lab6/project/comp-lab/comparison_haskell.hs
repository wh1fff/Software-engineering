-- ЛАБОРАТОРНАЯ РАБОТА 6. HASKELL

module ComparisonHaskell where

import Data.List (sortBy, groupBy)
import Data.Ord (comparing, Down(..))
import Data.Maybe (fromMaybe)

-- модель данных

data User = User
  { userId :: Int
  , userName :: String
  , userEmail :: String
  } deriving (Show, Eq)

data Product = Product
  { productId :: Int
  , productName :: String
  , productPrice :: Double
  , productCategory :: String
  } deriving (Show, Eq)

data OrderItem = OrderItem
  { itemProduct :: Product
  , itemQuantity :: Int
  } deriving (Show, Eq)

data Order = Order
  { orderId :: Int
  , orderUser :: User
  , orderItems :: [OrderItem]
  , orderStatus :: String
  } deriving (Show, Eq)

-- инициализация данных

users :: [User]
users =
  [ User 1 "John Doe" "john@example.com"
  , User 2 "Jane Smith" "jane@example.com"
  , User 3 "Bob Johnson" "bob@example.com"
  ]

products :: [Product]
products =
  [ Product 1 "iPhone" 999.99 "electronics"
  , Product 2 "MacBook" 1999.99 "electronics"
  , Product 3 "T-shirt" 29.99 "clothing"
  , Product 4 "Jeans" 79.99 "clothing"
  , Product 5 "Book" 15.99 "books"
  ]

orders :: [Order]
orders =
  [ Order 1 (users !! 0)
      [ OrderItem (products !! 0) 1
      , OrderItem (products !! 2) 2
      ] "completed"
  , Order 2 (users !! 1)
      [ OrderItem (products !! 1) 1
      ] "pending"
  , Order 3 (users !! 0)
      [ OrderItem (products !! 3) 3
      ] "completed"
  , Order 4 (users !! 2)
      [ OrderItem (products !! 4) 5
      , OrderItem (products !! 2) 1
      ] "pending"
  ]

-- функции обработки

-- расчет стоимости заказа
calculateOrderTotal :: Order -> Double
calculateOrderTotal order =
  sum [productPrice (itemProduct item) * fromIntegral (itemQuantity item) | item <- orderItems order]

-- статус-фильтр
filterOrdersByStatus :: [Order] -> String -> [Order]
filterOrdersByStatus os status = filter (\order -> orderStatus order == status) os

-- топ заказов по цене
getTopExpensiveOrders :: [Order] -> Int -> [Order]
getTopExpensiveOrders os n =
  take n $ sortBy (comparing (Down . calculateOrderTotal)) os

-- скидка
applyDiscount :: Order -> Double -> Order
applyDiscount order discount =
  order { orderItems = map (applyItemDiscount discount) (orderItems order) }
  where
    applyItemDiscount d item =
      item { itemProduct = (itemProduct item)
           { productPrice = productPrice (itemProduct item) * (1 - d) } }

-- группировка по пользователю
groupOrdersByUser :: [Order] -> [(Int, [Order])]
groupOrdersByUser os =
  [ (userId (orderUser (head group)), group)
  | group <- groupBy (\a b -> userId (orderUser a) == userId (orderUser b))
           (sortBy (comparing (userId . orderUser)) os)
  , not (null group)
  ]

-- расходы пользователя
calculateUserSpending :: [Order] -> [(String, Double)]
calculateUserSpending os =
  sortBy (comparing (Down . snd)) $
  [ (userName user, sum [calculateOrderTotal o | o <- userOrders])
  | user <- users
  , let userOrders = filter (\o -> userId (orderUser o) == userId user) os
  , not (null userOrders)
  ]

-- поиск по категориям
findOrdersByCategory :: [Order] -> String -> [Order]
findOrdersByCategory os category =
  filter (\order -> any (\item -> productCategory (itemProduct item) == category) (orderItems order)) os

-- статистика
data Statistics = Statistics
  { stat_total_orders :: Int
  , stat_completed_orders :: Int
  , stat_pending_orders :: Int
  , stat_total_revenue :: Double
  , stat_average_order :: Double
  , stat_max_order :: Double
  , stat_min_order :: Double
  } deriving (Show)

calculateStatistics :: [Order] -> Maybe Statistics
calculateStatistics os
  | null os = Nothing
  | otherwise =
      let totals = map calculateOrderTotal os
          completed = length (filterOrdersByStatus os "completed")
          pending = length (filterOrdersByStatus os "pending")
      in Just Statistics
           { stat_total_orders = length os
           , stat_completed_orders = completed
           , stat_pending_orders = pending
           , stat_total_revenue = sum totals
           , stat_average_order = sum totals / fromIntegral (length totals)
           , stat_max_order = maximum totals
           , stat_min_order = minimum totals
           }

-- принт

printOrder :: Order -> IO ()
printOrder order =
  putStrLn $ "  Order " ++ show (orderId order) ++ ": " ++
             userName (orderUser order) ++ " - $" ++ show (calculateOrderTotal order)

printUserOrder :: User -> [Order] -> IO ()
printUserOrder user userOrders =
  putStrLn $ "  " ++ userName user ++ ": " ++ show (length userOrders) ++ " orders"

printSpending :: (String, Double) -> IO ()
printSpending (name, total) =
  putStrLn $ "  " ++ name ++ ": $" ++ show total

printStatistics :: Statistics -> IO ()
printStatistics stats = do
  putStrLn $ "[OK] Total orders: " ++ show (stat_total_orders stats)
  putStrLn $ "[OK] Completed: " ++ show (stat_completed_orders stats)
  putStrLn $ "[OK] Pending: " ++ show (stat_pending_orders stats)
  putStrLn $ "[OK] Total revenue: $" ++ show (stat_total_revenue stats)
  putStrLn $ "[OK] Average order: $" ++ show (stat_average_order stats)
  putStrLn $ "[OK] Max order: $" ++ show (stat_max_order stats)
  putStrLn $ "[OK] Min order: $" ++ show (stat_min_order stats)

-- main

main :: IO ()
main = do
  putStrLn ""
  putStrLn (replicate 70 '=')
  putStrLn "LAB 6. PART 6 - FUNCTIONAL PROGRAMMING COMPARISON"
  putStrLn "Implementation in HASKELL"
  putStrLn (replicate 70 '=')

  putStrLn ""
  putStrLn (replicate 70 '=')
  putStrLn "[OK] ORDER ANALYSIS (HASKELL)"
  putStrLn (replicate 70 '=')

  -- завершенные заказы
  putStrLn ""
  putStrLn "[*] Completed orders:"
  let completed = filterOrdersByStatus orders "completed"
  mapM_ printOrder completed

  -- общая выручка
  let totalRevenue = sum (map calculateOrderTotal completed)
  putStrLn $ ""
  putStrLn $ "[*] Total revenue (completed): $" ++ show totalRevenue

  -- топ  заказов по цене
  putStrLn ""
  putStrLn "[*] Top 2 most expensive orders:"
  let topOrders = getTopExpensiveOrders orders 2
  mapM_ printOrder topOrders

  -- скидка
  putStrLn ""
  putStrLn "[*] First order with 10% discount:"
  putStrLn $ "  Was: $" ++ show (calculateOrderTotal (head orders))
  let discounted = applyDiscount (head orders) 0.1
  putStrLn $ "  After discount: $" ++ show (calculateOrderTotal discounted)

  -- группировка
  putStrLn ""
  putStrLn "[*] Orders by users:"
  let groupedWithUsers = [(u, os) | u <- users, let os = [o | o <- orders, userId (orderUser o) == userId u], not (null os)]
  mapM_ (\(user, userOrders) -> printUserOrder user userOrders) groupedWithUsers

  -- расходы
  putStrLn ""
  putStrLn "[*] User spending:"
  let spending = calculateUserSpending orders
  mapM_ printSpending spending

  -- по категориям
  putStrLn ""
  putStrLn "[*] Orders with electronics:"
  let electronics = findOrdersByCategory orders "electronics"
  putStrLn $ "  Found: " ++ show (length electronics) ++ " orders"
  mapM_ (\order -> putStrLn $ "    Order " ++ show (orderId order) ++ ": $" ++ show (calculateOrderTotal order)) electronics

  -- статистика
  putStrLn ""
  putStrLn (replicate 70 '=')
  putStrLn "STATISTICS"
  putStrLn (replicate 70 '=')

  case calculateStatistics orders of
    Just stats -> printStatistics stats
    Nothing -> putStrLn "No orders to analyze"

  -- композиция функций
  putStrLn ""
  putStrLn "[*] Operation chain (functional programming):"
  let result = getTopExpensiveOrders
             (map (\o -> applyDiscount o 0.05)
               (filter (\order -> calculateOrderTotal order > 50)
                 (filterOrdersByStatus orders "completed")))
             1
  case result of
    [order] -> putStrLn $ "  Order " ++ show (orderId order) ++ ": $" ++ show (calculateOrderTotal order) ++ " (after discount)"
    _ -> return ()

  putStrLn ""
  putStrLn (replicate 70 '=')
  putStrLn "[OK] ALL OPERATIONS COMPLETED!"
  putStrLn (replicate 70 '=')
  putStrLn ""