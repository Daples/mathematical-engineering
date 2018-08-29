import Data.Set as Set
import Data.Map as Map
import DFA 
import Regex

simplify :: Regex a -> Regex a
simplify Empty = Empty
simplify Epsilon = Epsilon
simplify (Symbol a) = Symbol a
simplify (Star Empty) = Epsilon
simplify (Star Epsilon) = Epsilon
simplify (Star (Star b)) = Star (simplify b)
simplify (Star (Plus Epsilon b)) = Star (simplify b)
simplify (Star (Plus b Epsilon)) = Star (simplify b)
simplify (Star a) = Star (simplify a)
simplify (Dot Empty _) = Empty
simplify (Dot _ Empty) = Empty
simplify (Dot Epsilon c) = simplify c
simplify (Dot b Epsilon) = simplify b
simplify (Dot (Symbol b) c) = Dot (Symbol b) (simplify c)
simplify (Dot b (Symbol c)) = Dot (simplify b) (Symbol c)
simplify (Dot b c) = Dot (simplify b) (simplify c)
simplify (Plus Empty c) = simplify c
simplify (Plus b Empty) = simplify b
simplify (Plus Epsilon b) = Plus Epsilon (simplify b)
simplify (Plus b Epsilon) = Plus (simplify b) Epsilon
simplify (Plus (Symbol b) c) = Plus (Symbol b) (simplify c)
simplify (Plus b (Symbol c)) = Plus (simplify b) (Symbol c)
simplify (Plus a b) = Plus (simplify a) (simplify b)

states :: Ord s => DFA s c -> Set s
states dfa = Set.fromList $ Map.keys (delta dfa)
                                         
tran :: Eq s => Map c s -> s -> Regex c
tran map1 j = tran' (Map.assocs map1) j where
tran' :: Eq s => [(c,s)] -> s -> Regex c
tran' [] _ = Empty
tran' (t:ts) j
  | (snd t) == j = Plus (Symbol (fst t)) (tran' ts j)
  | otherwise = tran' ts j

dfa2Regex1 :: Ord s => DFA s c -> s -> Regex c
dfa2Regex1 (MkDFA q0 d qf) fin =
      let stat = states (MkDFA q0 d qf)
          beg = Set.findIndex q0 stat
          final = Set.findIndex fin stat
      in dfa2Regex' stat (beg, final) ((length stat) - 1) d where
dfa2Regex' :: Ord s => Set s -> (Int, Int) -> Int -> Map s (Map c s) -> Regex c
dfa2Regex' qs (i,j) k d
  | k == -1 && i == j = simplify (Plus Epsilon (tran (d ! Set.elemAt i qs) (Set.elemAt j qs)))
  | k == -1 = simplify (tran (d ! Set.elemAt i qs) (Set.elemAt j qs))
  | otherwise = let rij = simplify (dfa2Regex' qs (i,j) (k-1) d)
                    rik = simplify (dfa2Regex' qs (i,k) (k-1) d)
                    rkk = simplify (dfa2Regex' qs (k,k) (k-1) d)
                    rkj = simplify (dfa2Regex' qs (k,j) (k-1) d)
                in simplify (Plus rij (Dot rik (Dot (Star rkk) rkj)))

dfa2Regex :: Ord s => DFA s c -> Regex c
dfa2Regex dfa = dfa2Aux dfa (Set.elems (accepting dfa)) where
dfa2Aux :: Ord s => DFA s c -> [s] -> Regex c
dfa2Aux _ [] = Empty
dfa2Aux dfa (x : xs) =
        let reg1 = simplify (dfa2Regex1 dfa x)
            reg2 = simplify (dfa2Aux dfa xs)
        in simplify (Plus reg1 reg2)

example1 :: DFA Int Int
example1 = trans (1,1,0) .
  trans (1,2,1) .
  trans (2,3,0) .
  trans (2,3,1) .
  trans (3,4,0) .
  trans (3,4,1) .
  trans (4,1,0) .
  trans (4,4,1) .
  accept 2 .
  accept 3 .
  accept 4 $ initDFA 1

example2 :: DFA Int Int
example2 = trans (1,1,0) .
   trans (1,2,1) .
   trans (2,1,0) .
   trans (2,2,1) .
   accept 2 $ initDFA 1

example3 :: DFA Int Int
example3 = trans (1,1,1) .
  trans (1,2,0) .
  trans (2,3,1) .
  trans (2,1,1) .
  trans (3,1,0) .
  trans (3,1,1) .
  accept 3 $ initDFA 1

example4 :: DFA Int Int
example4 = trans (1,1,1) .
  trans (1,2,0) .
  trans (2,1,0) .
  trans (2,3,1) .
  trans (3,3,0) .
  trans (3,3,1) .
  accept 3 $ initDFA 1

main :: IO()
main = print $ (dfa2Regex example4)
