import Data.Char

pinyinFromNumberMain :: [Char] -> [[Char]]
pinyinFromNumberMain (digit : digits)
    | digit == '0' = (if unitPinyin `elem` ["","Wan","Yi"] then unitPinyin else digitPinyin) : pinyinFromNumberMain digits
    | otherwise    = (digitPinyin ++ unitPinyin) : pinyinFromNumberMain digits
    where digitPinyin = ["Ling","Yi","Er","San","Si","Wu","Liu","Qi","Ba","Jiu"] !! (digitToInt digit)
          unitPinyin  = ["","Shi","Bai","Qian","Wan","Shi","Bai","Qian","Yi"] !! (length digits)

removeLing :: [[Char]] -> [[Char]]
removeLing (fst : snd : pys)
    | fst == "Ling" && (snd `elem` ["Ling","","Wan","Yi"]) = removeLing (snd : pys)
    | otherwise = fst : (removeLing (snd : pys))
removeLing (last : empty) = filter (/="") [last]

pinyinFromNumber num = removeLing (take (length num) (pinyinFromNumberMain num))
