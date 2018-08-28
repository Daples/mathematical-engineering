{- | This module serves as an easy way to represent regular expressions. -}
module Regex where

-- | Represents a regular expession with symbols of type @a@
data Regex a =
  -- | The empty language
  Empty
  -- | The empty string
  | Epsilon
  {- | Represents a symbol of type @a@ in the expression.
       E.g. Symbol @a@ = a -}
  | Symbol a
  {- | Kleene closure of a regular expression.
       E.g. Star (Symbol @a@) = a* -}
  | Star (Regex a)
  {- | Union of two regular expressions.
       E.g. Plus (Symbol @a@) (Symbol @b@) = a+b -}
  | Plus (Regex a) (Regex a)
  {- | Concatenation of two regular expressions.
       E.g. Dot (Symbol @a@) (Symbol @b@) = ab -}
  | Dot  (Regex a) (Regex a)

-- | Creates a String that is the infix representation of a Regex
show' :: (Show c) => Regex c -> String
show' Empty = "∅"
show' Epsilon = "ε"
show' (Symbol a) = show a
show' (Star (Symbol a)) = show' (Symbol a) ++ "*"
show' (Star a) = "(" ++ show' a ++ ")*"
show' (Plus a b) = show' a ++ "+" ++ show' b
show' (Dot (Symbol a) (Symbol b)) = show' (Symbol a) ++ show' (Symbol b)
show' (Dot (Star a) (Star b)) = show' (Star a) ++ show' (Star b)
show' (Dot (Symbol a) (Star b)) = show' (Symbol a) ++ show' (Star b)
show' (Dot (Star a) (Symbol b)) = show' (Star a) ++ show' (Symbol b)
show' (Dot (Symbol a) (Dot b c)) = show' (Symbol a) ++ show' (Dot b c)
show' (Dot (Dot a b) (Symbol c)) = show' (Dot a b) ++ show' (Symbol c)
show' (Dot (Star a) (Dot b c)) = show' (Star a) ++ show' (Dot b c)
show' (Dot (Dot a b) (Star c)) = show' (Dot a b) ++ show' (Star c)
show' (Dot (Symbol a) b) = show' (Symbol a) ++ "(" ++ show' b ++ ")"
show' (Dot a (Symbol b)) = "(" ++ show' a ++ ")" ++ show' (Symbol b)
show' (Dot (Star a) b) = show' (Star a) ++ "(" ++ show' b ++ ")"
show' (Dot a (Star b)) = "(" ++ show' a ++ ")" ++ show' (Star b)
show' (Dot (Dot a b) c) = show' (Dot a (Dot b c))
show' (Dot a b) = "(" ++ show' a ++ ")(" ++ show' b ++ ")"

-- | Erases all instances of a Char in a String
erase :: Char -> String -> String
erase _ [] = []
erase c (h:t)
  | c == h = erase c t
  | otherwise = h : erase c t

-- | String with the infix representation of a Regex without quotation marks
instance (Show c) => Show (Regex c) where
  show a = erase '\"' (show' a)
