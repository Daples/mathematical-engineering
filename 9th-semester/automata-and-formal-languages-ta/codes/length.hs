myLength :: [Int] -> Int
myLength []       = 0
myLength (x : xs) = 1 + myLength xs
