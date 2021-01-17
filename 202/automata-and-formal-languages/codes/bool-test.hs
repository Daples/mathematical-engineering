data Bool = True | False

(||) :: Bool -> Bool -> Bool
True  || _ = True
False || x = x

(&&) :: Bool -> Bool -> Bool
False && _  = False
True  && x  = x

not :: Bool -> Bool
not False = True
not _     = False
