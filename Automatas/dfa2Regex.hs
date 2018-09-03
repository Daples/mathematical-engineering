{- | Converts a deterministic finite automaton (DFA) into a regular expression (Regex), using the DFA2Regex function. -}
{-# LANGUAGE ScopedTypeVariables #-}

module Dfa2Regex where 

import Data.Set as Set
import Data.Map as Map
import DFA
import Regex

-- | Checks if a Regex has epsilon.
hasEp :: Regex c -> Bool
hasEp Epsilon = True
hasEp (Star _) = True
hasEp (Dot a b) = hasEp a && hasEp b
hasEp (Plus a b) = hasEp a || hasEp b
hasEp _ = False

-- | Removes epsilon from a Regex, when necessary.
rmEp :: Regex c -> Regex c
rmEp (Plus Epsilon a) = rmEp a
rmEp (Plus a Epsilon) = rmEp a
rmEp (Plus a b) = Plus (rmEp a) (rmEp b)
rmEp a = a

-- | Checks if a Regex is written exactly as another Regex. Does not check equivalence.
equal :: (Show c) => Regex c -> Regex c -> Bool
equal a b = (show' a) == (show' b)

-- | Simplifies the output regex from the given DFA.
simplify :: (Show a) => Regex a -> Regex a
simplify Empty = Empty
simplify Epsilon = Epsilon
simplify (Symbol b) = Symbol b
simplify (Star Empty) = Epsilon
simplify (Star Epsilon) = Epsilon
simplify (Star (Star b)) = simplify (Star b)
simplify (Star b)
  | hasEp b = Star (rmEp b)
  | otherwise = Star (simplify b)
simplify (Dot Empty _) = Empty
simplify (Dot _ Empty) = Empty
simplify (Dot Epsilon c) = simplify c
simplify (Dot b Epsilon) = simplify b
simplify (Dot (Star b) c)
  | hasEp c && equal (rmEp c) b = simplify (Star b)
simplify (Dot c (Star b))
  | hasEp c && equal (rmEp c) b = simplify (Star b)
simplify (Dot b c) = Dot (simplify b) (simplify c)
simplify (Plus Empty c) = simplify c
simplify (Plus b Empty) = simplify b
simplify (Plus b (Dot c d))
  | (equal b c && hasEp d) || (equal b d && hasEp c) = simplify (Dot c d)
simplify (Plus (Dot c d) b)
  | (equal b c && hasEp d) || (equal b d && hasEp c) = simplify (Dot c d)
simplify (Plus c b)
  | equal c Epsilon && hasEp b = simplify b
  | equal b Epsilon && hasEp c = simplify c
  | equal c (Star b) = simplify c
  | equal b (Star c) = simplify b
  | equal c b = simplify c
  | otherwise = Plus (simplify c) (simplify b)

-- | Extracts the set of states of the given DFA.
states :: Ord s => DFA s c -> Set s
states (MkDFA _ d qf) = Set.union (Set.fromList $ Map.keys d) qf

-- | Generates a Regex using all transitions that arrive at a given state.
tran :: Eq s => Map c s -> s -> Regex c
tran map1 j = tran' (Map.assocs map1) j where
tran' :: Eq s => [(c,s)] -> s -> Regex c
tran' [] _ = Empty
tran' (t:ts) j
  | (snd t) == j = Plus (Symbol (fst t)) (tran' ts j)
  | otherwise = tran' ts j

dfa2Regex1 :: forall s c. (Show c) => Ord s => DFA s c -> s -> Regex c
dfa2Regex1 (MkDFA q0 d qf) fin =
      let stat :: Set s
          stat = states (MkDFA q0 d qf)
          beg :: Int
          beg = Set.findIndex q0 stat
          final :: Int
          final = Set.findIndex fin stat
      in dfa2Regex' stat (beg, final) ((length stat) - 1) d where
dfa2Regex' :: forall s c. (Show c) => Ord s => 
              Set s -> (Int, Int) -> Int -> Map s (Map c s) -> Regex c
dfa2Regex' qs (i,j) k d
  | k == -1 && i == j = 
           let i1 :: s
               i1 = Set.elemAt i qs
               tr :: Regex c
               tr = if Map.member i1 d
                    then tran (d ! i1) (Set.elemAt j qs)
                    else Empty
           in simplify (Plus Epsilon tr)
  | k == -1 = let i1 :: s
                  i1 = Set.elemAt i qs
                  tr :: Regex c
                  tr = if Map.member i1 d
                       then tran (d ! i1) (Set.elemAt j qs)
                       else Empty
              in simplify tr
  | otherwise = let rij :: Regex c
                    rij = simplify (dfa2Regex' qs (i,j) (k-1) d)
                    rik :: Regex c
                    rik = simplify (dfa2Regex' qs (i,k) (k-1) d)
                    rkk :: Regex c
                    rkk = simplify (dfa2Regex' qs (k,k) (k-1) d)
                    rkj :: Regex c
                    rkj = simplify (dfa2Regex' qs (k,j) (k-1) d)
                in simplify (Plus rij (Dot rik (Dot (Star rkk) rkj)))

-- | Converts an input DFA into a Regex.
dfa2Regex :: (Show c) => Ord s => DFA s c -> Regex c
dfa2Regex dfa = dfa2Aux dfa (Set.elems (accepting dfa)) where
dfa2Aux :: forall s c. (Show c) => Ord s => DFA s c -> [s] -> Regex c
dfa2Aux _ [] = Empty
dfa2Aux dfa (x : xs) =
        let reg1 :: Regex c
            reg1 = simplify (dfa2Regex1 dfa x)
            reg2 :: Regex c
            reg2 = simplify (dfa2Aux dfa xs)
        in simplify (Plus reg1 reg2)
