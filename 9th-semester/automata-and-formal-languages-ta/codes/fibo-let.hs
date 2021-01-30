fib :: Int -> Int
fib n
  | n == 0 || n == 1 = n
  | otherwise        = let fib1 :: Int
                           fib1 = fib (n - 1)
                       in fib (n - 2) + fib1
