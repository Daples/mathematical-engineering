{- | Serves as way to represent deterministic finite automata. -}
module DFA where

import Data.Map as Map (Map, empty, insertWith, singleton, union)
import Data.Set as Set (Set, empty, insert)

-- | Represents a DFA with states of type @s@ and input symbols of type @c@
data DFA s c = MkDFA
  { -- | A unique initial state
    start         :: s
  , {- | The transition function.
         The outer map stores all transitions available from a state,
         inner maps stores the endpoint of a transition using a given symbol -}
    delta         :: Map s (Map c s)
  , -- | A set of final/accepting states
    accepting     :: Set s
  } deriving Show

-- | Creates a new DFA with a starting state @q0@
initDFA :: s -> DFA s a
initDFA q0 = MkDFA q0 Map.empty Set.empty

-- | Adds a new transition from state @q@ to @q'@ with a symbol @c@ to a DFA
trans :: (Ord s, Ord c) => (s, s, c) -> DFA s c -> DFA s c
trans (q, q', c) (MkDFA q0 ts f) = MkDFA q0 ts' f
  where ts' = Map.insertWith Map.union q (Map.singleton c q') ts

-- | Adds a new accepting state @q@ to a DFA
accept :: (Ord a, Ord s) => s -> DFA s a -> DFA s a
accept q (MkDFA q0 ts fs) = MkDFA q0 ts (Set.insert q fs)

{-| First automaton example. The language of this DFA does not contain any
    words.-}
dfa0 :: DFA Int String
dfa0 = trans (0, 0, "(^o^)/") $
       trans (0, 0, "(-_-)") $
       initDFA 0

{-| Second automaton example. This DFA represents the language that only
  recognizes the empty word. -}
dfa1 :: DFA Int String
dfa1 = trans (0, 1, "(^o^)/") $
       trans (0, 1, "(-_-)") $
       trans (1, 1, "(^o^)/") $
       trans (1, 1, "(-_-)") $
       accept 0 $
       initDFA 0

{-| Third automaton example. This DFA represents the language of the regex
    L(dfa2) = (0 + 1 + 2)*. -}
dfa2 :: DFA Int Int
dfa2 = trans (0, 0, 0) $
       trans (0, 0, 1) $
       trans (0, 0, 2) $
       accept 0 $
       initDFA 0

{-| Last automaton example. This DFA represents the language of the regex
    L(dfa3) = abc(abc)* -}
dfa3 :: DFA Int Char
dfa3 = trans (0, 1, 'a') $ trans (0, 2, 'b') $
       trans (0, 2, 'c') $ trans (1, 2, 'a') $
       trans (1, 3, 'b') $ trans (1, 2, 'c') $
       trans (2, 2, 'a') $ trans (2, 2, 'b') $
       trans (2, 2, 'c') $ trans (3, 2, 'a') $
       trans (3, 2, 'b') $ trans (3, 4, 'c') $
       trans (4, 1, 'a') $ trans (4, 2, 'b') $
       trans (4, 2, 'c') $ accept 4 $ initDFA 0
