import System.Environment
import System.IO
import Data.List
import Data.List.Split
import Data.String.Utils
import Text.Regex.TDFA
import Data.CSV

-- Get all of the pages of the mathematicians
getPages :: String -> [String]
getPages str = tail (splitOn "<page>" str)

-- Gets the name of a mathematician, given it's page
getName :: String -> String
getName page = 
        let regName :: String
            regName  = "<title>(.*)</title>"
            name :: String
            name     = (page =~ regName)
            fixName1 :: String
            fixName1 = replace "<title>" "" name
            fixName2 :: String
            fixName2 = replace "</title>" "" fixName1
            in repRegex fixName2 "" "\\((.*)\\)"
            
-- A regular expresion of the InfoBox. As the infobox language isn't regular
-- it helps to find a good aproximation to then continue to search
regexInfoBox :: String
regexInfoBox = 
          let typesInfos :: String
              typesInfos = "(scientist)?(officeholder)?(person)?(academic)?"
              begin :: String
              begin      = "{{[ ]*[Ii]nfobox " ++ typesInfos ++ "[ ]*[\r]?[\n]"
              middle :: String
              middle     = "(\\|(.*)=(.*)[\r]?[\n]?)+"
              in begin ++ middle

-- Gives the index where the substring ends in the string. If the substring
-- isn't at the givens string it returns -1
findSubstring :: String -> String -> Int 
findSubstring sub str = findSubstringAux sub str 0 (length str)

-- Auxiliar function to substring
findSubstringAux :: String -> String -> Int -> Int -> Int
findSubstringAux sub str i lStr
 | i + length sub >= lStr = -1
 | isPrefixOf sub str     = i + length sub - 1
 | otherwise              = findSubstringAux sub (tail str) (i+1) lStr
 
-- Count elements of a alphabet in a string, given a alphabet of symbols.
countElem :: String -> String -> Int
countElem alphabet str = length (findIndices (`elem` alphabet) str)

-- A function that tells whether the given string is key balanced (i.e {})
nestedKeys :: String -> Bool
nestedKeys page = let nOpenKeys :: Int
                      nOpenKeys   = countElem "{" page
                      nOfClosKeys :: Int
                      nOfClosKeys = countElem "}" page
                      in nOpenKeys == nOfClosKeys

-- Given the original page and a substring, it completes the remaining string so
-- it has balanced keys.
getCompleteNestedKeys :: String -> String -> String
getCompleteNestedKeys header page = 
                      let indHead :: Int
                          indHead = findSubstring header page
                          aftHead :: String
                          aftHead = snd (splitAt indHead page)
                          in getCompleteNestedKeysAux aftHead header

-- An auxiliar function to the function above.
getCompleteNestedKeysAux :: String -> String -> String
getCompleteNestedKeysAux [] header 
                     = header
getCompleteNestedKeysAux (x:xs) header
 | nestedKeys header = header
 | otherwise         = getCompleteNestedKeysAux xs (header ++ [x])

-- It replaces all the strings that fit the regex with a given
-- string.
repRegex :: String -> String -> String -> String
repRegex page rep regex =
                let sepClean :: String
                    sepClean = (page =~ regex)
                    in repRegexAux page rep regex sepClean

-- An auxiliar function to repRegex
repRegexAux :: String -> String -> String -> String -> String
repRegexAux page _ _ ""            = page
repRegexAux page rep regex toClean = 
            let cleaned :: String
                cleaned      = replace toClean rep page
                toCleanAgain :: String
                toCleanAgain = (cleaned =~ regex)
                in repRegexAux cleaned rep regex toCleanAgain

-- It returns the complete infobox of a page
getInfoBox :: String -> String
getInfoBox page =
        let infoHead :: String
            infoHead  = (page =~ regexInfoBox)
            uncleaned :: String
            uncleaned = getCompleteNestedKeys infoHead page
            in repRegex uncleaned "" "&lt(.*)&gt;"

--Erases spaces and equal of the rugged form.
cleanSpacEqual :: String -> String
cleanSpacEqual page =
                let clean :: String
                    clean    = (page =~ "=(.*)")
                    toClean :: String
                    toClean  = (clean =~ "=[ ]*")
                    clean2 :: String
                    clean2   = replace toClean "" clean
                    in clean2

-- It cleans a string, such that we only have the value of the given
-- paramater. (e.g. (clean "alma_mater = hola") = "hola")
cleanForm :: String -> String
cleanForm page =
      let clean :: String
          clean    = cleanSpacEqual page
          complete :: String
          complete = getCompleteNestedKeys clean page
          in complete
          
-- It tells if a form has different values for a parameter
variousStudies :: String -> Bool
variousStudies inform 
 | countElem "*" inform >= 2                              = True
 | countElem "|" inform >= 1                              = True
 | countElem "," inform >= 1 && countElem "[" inform >= 1 = True
 | countElem "[" inform > 2                               = True
 | countElem "[" inform == 2 && last(inform) /= ']'       = True
 | otherwise = False
  
-- It extracts the value of a parameter, given the possibility that it could
-- be variousStudies answers.
obtainStudies :: String -> String
obtainStudies inform
 | variousStudies inform = "(Various)"
 | otherwise             = obtainStudiesAux inform

-- Auxiliar to obtainStudies
obtainStudiesAux :: String -> String  
obtainStudiesAux inform
 | isInfixOf "*" inform = let value :: String
                              value  = (inform =~ "\\*(.*)[\r]?[\n]")
                              toErase :: String
                              toErase = (value =~ "\\*[ ]*")
                              in replace toErase "" value
 | otherwise            = let clean1 :: String
                              clean1  = replace "[" "" inform
                              clean2 :: String
                              clean2 = replace "]" "" clean1
                              in clean2
                              
-- Gets the value of a parameter, given that it could be organized in a list
-- or different ways.                           
getInformTypeList :: String -> String -> String
getInformTypeList info regex =
             let head1 :: String
                 head1    = (info =~ regex)
                 infor :: String
                 infor   = getCompleteNestedKeys head1 info
                 cleaned :: String
                 cleaned = cleanForm infor
                 in obtainStudies cleaned

-- Gets the alma mater given a infobox.                             
getAlmaMater :: String -> String
getAlmaMater info = getInformTypeList info "alma[_ ]mater[ ]*=(.*)[\r]?[\n]"

-- Gets the fields given a infobox.
getFields :: String -> String
getFields info = getInformTypeList info "field(s)?[ ]*=(.*)[\r]?[\n]"

-- It transforms a given format of date, to a general one
orderDate :: String -> String
orderDate date = let withoutComma :: String
                     withoutComma = replace "," "" date
                     dates :: [String]
                     dates = (splitOn " " withoutComma)
                     in (dates!!1) ++ " " ++ (dates!!0) ++ " " ++ (dates!!2)


-- It translates a form of date, to a number one.
transDate :: String -> String
transDate date = transDateAux (splitOn " " date)

-- Auxiliar function to the function above.
transDateAux :: [String] -> String
transDateAux dates
 | length dates >= 3 = (dates!!2) ++ "/" ++ (getMonth (dates!!1)) ++ "/" ++ (dates!!0)
 | otherwise = (dates!!0)

-- It transforms month to number
getMonth :: String -> String
getMonth month
 | month == "January"   = "01"
 | month == "February"  = "02"
 | month == "March"     = "03"
 | month == "April"     = "04"
 | month == "May"       = "05"
 | month == "June"      = "06"
 | month == "July"      = "07"
 | month == "August"    = "08"
 | month == "September" = "09"
 | month == "October"   = "10"
 | month == "November"  = "11"
 | month == "December"  = "12"
 | otherwise = "00"

-- Gets date for a given field.
getDate :: String -> String -> String
getDate info regex =
             let form :: String
                 form = (info =~ regex)
                 cleaned :: String
                 cleaned = cleanSpacEqual form
                 in getDateAux cleaned

-- It's an auxiliar function to the get date
getDateAux :: String -> String
getDateAux "" = ""
getDateAux date
 | isInfixOf "{" date && countElem "|" date > 1 = 
                                     let dPipe :: String
                                         dPipe = (date =~ "[0-9]+\\|[0-9]+\\|[0-9]+")
                                         in replace "|" "/" dPipe
 | isInfixOf "{" date                            = 
                                     let unDate :: String
                                         unDate = ((splitOn "|" date)!!1)
                                         cleaned :: String
                                         cleaned = replace "}" "" unDate
                                         in transDate cleaned
                                         
 | isInfixOf "," date                            = 
                                     let ordDate :: String
                                         ordDate = orderDate date
                                         in transDate ordDate
 | length (replace " " "" date) == 4             = replace " " "" date
 | otherwise                                     = transDate date

-- Gets the birth date given it's infobox.
getBDate :: String -> String
getBDate info = getDate info "birth_date[ ]*=(.*)[\r]?[\n]"

-- Gets the death date given it's infobox.
getDDate :: String -> String
getDDate info = getDate info "death_date[ ]*=(.*)[\r]?[\n]"

-- Erases the first spaces found in a string
eraseFstSp :: String -> String
eraseFstSp str = let firstSpaces :: String
                     firstSpaces = (str =~ "[ ]*")
                     in if firstSpaces == ""
                        then str
                        else replace firstSpaces "" str

-- It takes out extra characters that appear at extracting the place                     
cleanPlace :: String -> String
cleanPlace str = let clean1 :: String
                     clean1 = replace "[" "" str
                     clean2 :: String
                     clean2 = replace "}" "" clean1
                     clean3 :: String
                     clean3 = replace ", " "/" clean2
                     clean4 :: String
                     clean4 = replace "," "" clean3
                     clean5 :: String
                     clean5 = replace "]" "" clean4
                     clean6 :: String
                     clean6 = repRegex clean5 "" "\\((.*)\\)"
                     clean7 :: String
                     clean7 = repRegex clean6 "" "(.*)\\|"
                     clean8 :: String
                     clean8 = replace " /" "/" clean7
                     in eraseFstSp clean8

-- Gets a place given it's field.
getPlace :: String -> String -> String
getPlace info regex = let form :: String
                          form = (info =~ regex)
                          cleaned :: String
                          cleaned = cleanSpacEqual form
                          in getPlaceAux cleaned
                          
-- A auxiliar function for the function above.                          
getPlaceAux :: String -> String
getPlaceAux "" = ""
getPlaceAux form
 | countElem "[" form <= 2 || countElem "," form == 1 = cleanPlace form
 | countElem "," form > 1 = let place :: String
                                place = last (splitOn "," form)
                                in cleanPlace place
 | countElem "|" form > 1 = let place :: String
                                place = last (splitOn "|" form)
                                in cleanPlace place
 | otherwise = "(Various)" 

-- Get's the birth place given it's infobox                        
getBPlace :: String -> String
getBPlace info = getPlace info "birth_place[ ]*=(.*)[\r]?[\n]"

-- Get's the death place given it's infobox
getDPlace :: String -> String
getDPlace info = getPlace info "death_place[ ]*=(.*)[\r]?[\n]"


generateMatrix :: [String] -> [[String]]
generateMatrix pages = ["Name", "Birth date", "Death date",
                         "Birth place", "Death place",
                          "Alma mater", "Fields"] : generateMatrixAux pages
                                            
generateMatrixAux :: [String] -> [[String]]
generateMatrixAux [] = []
generateMatrixAux (x:xs) = let name :: String
                               name = getName x
                               info :: String
                               info = getInfoBox x
                               bDate :: String
                               bDate = getBDate info
                               dDate :: String
                               dDate = getDDate info
                               bPlace :: String
                               bPlace = getBPlace info
                               dPlace :: String
                               dPlace = getDPlace info
                               alma :: String
                               alma = getAlmaMater info
                               fields :: String
                               fields = getFields info
                               in [name, bDate, dDate, 
                               bPlace, dPlace, alma, fields] : 
                               generateMatrixAux xs
                            
                          

printList :: (Show a) => [a] -> IO()
printList [] = print "End of array"
printList (x:xs) = do 
 print $ x
 printList xs
 
printListEnum :: [[String]] -> Int -> IO()
printListEnum [] _ = print ""
printListEnum (x:xs) y = do
 let toPrint :: String
     toPrint = (show y) ++ ". [" ++ (strList x)
     in print toPrint
 printListEnum xs (y+1)
 
strList :: [String] ->String
strList [] = "]"
strList (x:xs) = x ++ ", " ++ strList xs
main :: IO()
main = do
 x <- getArgs
 file  <- openFile (x!!0) ReadMode
 fileStr <- hGetContents file
 let matrix :: [[String]]
     matrix = generateMatrix (getPages fileStr)
     in writeFile "infoboxData.csv" (genCsvFile matrix)
 --let infos :: [String]
     --infos = map getInfoBox (getPages fileStr)
     --bDates :: [String]
     --bDates = map getBDate infos
     --in printList bDates
