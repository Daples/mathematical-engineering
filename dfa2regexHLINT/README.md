# Dfa2Regex
Converts a deterministic finite automaton (DFA) into a regular expression
(Regex), using the dfa2Regex function. This program is based on the Transitive Closure Method, which is an recursive algorithm to find regular expressions associated to a deterministic finite automaton.

## Getting Started
### Prerequisites
* **GHCi version 8.4.3** (interactive Glasgow Haskell Compiler environment): if you are in macOS or Windows, please refer [here](https://www.haskell.org/downloads) in order to download GHC. If you are in a linux-based OS, you can easily find and install GHC or Haskell Platform with your favorite package manager. However, in some linux distributions (e.g. Ubuntu 16.04 LTS), GHC might be outdated in the default repositories; in this case, you would have to search online for a stable version of GHC 8.4.3 for your distribution.

* **DFA** and **Regex** modules included with this program, if these modules are not in the same folder as the **DFA2Regex** module, the program will not execute.
### Installation
Just copy **DFA.hs**, **Regex.hs** and **DFA2Regex.hs** in a folder you can easily find from the command line.

## Usage
This program is executed through GHCi in the command line. In order to use the program, you will have to, first, navigate to the folder where **DFA2Regex** is located, which can be done as follows:
```
> cd path/to/DFA2Regex.hs
```
And then run GHCi,
```
> ghci
> [GHCi, version 8.4.3: http://www.haskell.org/ghc/  :? for help
Prelude>
```
Here, you can load the module as follows:
```
Prelude> :l DFA2Regex.hs
```
And then execute the program:
```
*Dfa2Regex> dfa2Regex example1
```
Note that here we are summoning the function **dfa2Regex** with a predefined DFA called **example** and the program prints the regular expression in the command line.

## Built With
* Glasgow Haskell Compiler (GHC), version 8.4.3.
* HLint v1.9.26.
* Haddock version 2.20.0.
* Atom v1.27.2.

## Authors
* Juan S. Cárdenas R.
* David Plazas E.
