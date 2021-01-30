fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n - 2) + fib1
  where fib1 :: Int
        fib1 = fib (n - 1)
