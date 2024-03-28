{-| This module is used to represent PushDown Automata -}

module PushDownAutomata where

import Data.Map as Map
import Data.Set as Set

{-| Represents the transition function (delta function) of a
  PushDownAutomata.  The map pairs a tuple of a state, a symbol and a
  stack symbol with a tuple that has the new state and a list of stack
  symbols. The symbol in the first tuple is represented by a list
  because, it can be either an input symbol or the empty string (see
  6.1.2, definition of PDA).
-}
type TransitionFunction state symbol ssymbol
     = Map (state, [symbol], ssymbol) (Set (state, [ssymbol]))

{-| Represents a PushDown Automaton (PDA).  The type can represent a
  deterministic and non-deterministic PDA, with states of type
  @state@, input symbols of type @symbol@ and stack symbols of type
  @ssymbol@.
-}
data PushDownAutomata state symbol ssymbol = PDA
  {
      -- | The set of states.
      states        :: Set state
      -- | The set of input symbols.
    , alphabet      :: Set symbol
      -- | The set of stack symbols
    , stackalphabet :: Set ssymbol
      -- | The Transition Function.
    , delta        :: TransitionFunction state symbol ssymbol
      -- | The initial state.
    , initialState :: state
      -- | The start symbol
    , z0           :: ssymbol
      -- | The set of final or accepting states.
    , acceptState  :: Set state
  }

{-| Adds a transition to the given TransitionFunction.  @(state,
  [symbol], ssymbol, state, [ssymbol])@ is a tuple whose elements
  represent the origin state, the symbol that executes the transition,
  the last symbol of the stack, the final state and the string to
  replace the stack symbol respectively.
-}
addTransition :: (Ord state, Ord symbol, Ord ssymbol) =>
                 (state, [symbol], ssymbol, state, [ssymbol]) ->
                 TransitionFunction state symbol ssymbol ->
                 TransitionFunction state symbol ssymbol
addTransition (q, s, sp, q', y) = Map.insertWith Set.union (q, s, sp)
                                  (Set.singleton (q', y))

-- | Formats how to display instances of PushdownAutomata.
instance (Show state, Show symbol, Show ssymbol) =>
          Show (PushDownAutomata state symbol ssymbol) where
  show (PDA st sy ssy tf is z00 ac) =
       "States:         "   ++ show st ++
       "\nAlphabet:       " ++ show sy ++
       "\nStack Alphabet  " ++ show ssy ++
       "\nDelta:          " ++ show tf ++
       "\nInitial States: " ++ show is ++
       "\nStart symbol    " ++ show z00 ++
       "\nAccept States:  " ++ show ac

------------------------------------------------------------------------------
-- PDA examples

{-| First automaton example. This PDA represents the following language,
  L(pda1) = {ww^r | w in [0, 1]*} with w^r being the reversed
  word. This is Example 6.2 of the textbook.
-}
pda1 :: PushDownAutomata Int Int Int
pda1 = PDA
  { states        = Set.fromList [0, 1, 2]
  , alphabet      = Set.fromList [0, 1]
  , stackalphabet = Set.fromList [0, 1, -1]
  , delta         = delta'
  , initialState  = 0
  , z0            = -1
  , acceptState   = Set.fromList [2]
  }
  where
    delta' :: TransitionFunction Int Int Int
    delta' = addTransition (0, [0], -1, 0, [0, -1]) $
             addTransition (0, [1], -1, 0, [1, -1]) $
             addTransition (0, [0], 0, 0, [0, 0]) $
             addTransition (0, [0], 1, 0, [0, 1]) $
             addTransition (0, [1], 0, 0, [1, 0]) $
             addTransition (0, [1], 1, 0, [1, 1]) $
             addTransition (0, [], -1, 1, [-1]) $
             addTransition (0, [], 0, 1, [0]) $
             addTransition (0, [], 1, 1, [1]) $
             addTransition (1, [0], 0, 1, []) $
             addTransition (1, [1], 1, 1, []) $
             addTransition (1, [], -1, 2, [-1])
             Map.empty

{-| Second automaton example. This PDA represents the following
  language, L(pda2) = {a^nb^n | n >= 1}.
-}
pda2 :: PushDownAutomata Int Char Char
pda2 = PDA
  { states        = Set.fromList [0, 1, 2]
  , alphabet      = Set.fromList ['a', 'b']
  , stackalphabet = Set.fromList ['a', 'b', 'z']
  , delta         = delta'
  , initialState  = 0
  , z0            = 'z'
  , acceptState   = Set.fromList [2]
  }
  where
    delta' :: TransitionFunction Int Char Char
    delta' = addTransition (0, ['a'], 'z', 0, ['a', 'z']) $
             addTransition (0, ['a'], 'a', 0, ['a', 'a']) $
             addTransition (0, ['b'], 'a', 1, []) $
             addTransition (1, ['b'], 'a', 1, []) $
             addTransition (1, [], 'z', 2, ['z'])
             Map.empty

{-| Third automaton example. This PDA represents the following language.
  L(pda3) = {a^(2n)b^(3n) | n >= 1}.
-}
pda3 :: PushDownAutomata Int Char Char
pda3 = PDA
  {  states        = Set.fromList [0, 1, 2, 3, 4]
  , alphabet      = Set.fromList ['a', 'b']
  , stackalphabet = Set.fromList ['a', 'b', 'z']
  , delta         = delta'
  , initialState  = 0
  , z0            = 'z'
  , acceptState   = Set.fromList [4]
  }
  where
    delta' :: TransitionFunction Int Char Char
    delta' = addTransition (0, ['a'], 'z', 1, ['z']) $
             addTransition (1, ['a'], 'z', 2, ['a', 'a', 'a', 'z']) $
             addTransition (1, ['a'], 'a', 2, ['a', 'a', 'a', 'a']) $
             addTransition (2, ['a'], 'a', 1, ['a']) $
             addTransition (2, ['b'], 'a', 3, []) $
             addTransition (3, ['b'], 'a', 3, []) $
             addTransition (3, [], 'z', 4, ['z'])
             Map.empty

