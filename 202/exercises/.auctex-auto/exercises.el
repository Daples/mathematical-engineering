(TeX-add-style-hook
 "exercises"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("babel" "english") ("inputenc" "utf8")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art11"
    "babel"
    "geometry"
    "amsmath"
    "amsthm"
    "graphicx"
    "inputenc"
    "subcaption"
    "hyperref"
    "multicol"
    "amssymb"
    "tensor"
    "xparse"
    "mathtools"
    "prftree"
    "float"
    "esvect"
    "enumitem"
    "mathrsfs")
   (TeX-add-symbols
    '("app" 3)
    '("ch" 1)
    '("expp" 1)
    '("pow" 2)
    "N"
    "Z"
    "Q"
    "R"
    "fst"
    "snd"
    "dneq"
    "I"
    "K"
    "ordAlph"
    "termOrd"
    "fl"
    "sk"
    "oldabs"
    "abs"
    "oldnorm"
    "norm")
   (LaTeX-add-labels
    "eq:radius"
    "eq:lb")
   (LaTeX-add-amsthm-newtheorems
    "definition"
    "remark"
    "example"
    "question"
    "theorem")
   (LaTeX-add-xparse-macros
    '("E" "o m")
    '("V" "o m")
    '("P" "o o m")
    '("cx" "o"))
   (LaTeX-add-mathtools-DeclarePairedDelimiters
    '("abs" "")
    '("norm" "")))
 :latex)

