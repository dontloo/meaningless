-- A complete parser for simple type definitions.
-- Developed for use in COMP3610

-- Clem Baker-Finch

module ParseTypeDefs where

import Data.Char

-- The grammar is suitable for top-down predictive parsing without
-- modification:

-- <Expr> ::= var | <Expr> <Expr> | lambda var dot <Expr>

-- First the abstract syntax, the taget of the parser:

data Expression = Variable String | Abstraction String Expression 
                | Application Expression Expression
                  deriving Show
-- The scanner is straightforward:

data Token = ID String | LPAREN | RPAREN
           | LAMBDA | ARROW
           deriving Eq

scan :: String -> [Token]

scan []           = []
scan ('(':cs)     = LPAREN : scan cs
scan (')':cs)     = RPAREN : scan cs
scan ('-':'>':cs) = ARROW : scan cs
scan ('\\':cs)    = LAMBDA: scan cs
scan input@(c:cs)
  | isSpace c     = scan cs
  | isAlpha c     = checkResWord word : scan afterWord
  | otherwise     = error (c:" : illegal character.")
 4 where
    (word, afterWord) = span isAlphaNum input

checkResWord :: String -> Token
checkResWord other   = ID other

-- The parser takes a sequence of tokens and constructs a parse tree
-- (i.e. a value of TypeDef).  It must also return the sequence of
-- remaining tokens with which to continue the parse.  There will also
-- be a parser corresponding to the syntactic category Simple.

parseAbs :: [Token] -> (Expression, [Token])
parseAbs (LAMBDA:toks) = (Abstraction var expr, toks3) 
  where (ID var:toks1)  = toks
        toks2            = check ARROW toks1
        (expr, toks3)    = parseAbs toks2
parseAbs (toks) = parseApp toks


parseApp :: [Token] -> (Expression, [Token])
parseApp =  parseApp'.parseTerm


parseApp' :: (Expression, [Token]) -> (Expression, [Token])
parseApp' (expr, [])          = (expr, [])
parseApp' (expr, RPAREN:toks) = (expr, RPAREN:toks)
parseApp' (expr, toks)        = (Application expr expr1, toks1) 
  where (expr1, toks1) = parseApp' $ parseTerm toks


parseTerm :: [Token] -> (Expression, [Token])
parseTerm (LPAREN:toks) = (abs, toks2)
  where (abs, toks1) = parseAbs toks
        toks2        = check RPAREN toks1
parseTerm (ID var:toks) = (Variable var, toks)
parseTerm _ = error "Unexpected symbol. (term error)"

-- Check that the next token is the one expected:

check :: Token -> [Token] -> [Token]

check tok []  = error "Unexpected end of input."
check tok (t:ts)
  | tok == t  = ts
  | otherwise = error "Unexpected symbol."

-- Expand a collapsed expression (e.g. \ x y z -> to \ x -> y -> z ->)
expand :: String -> String

expand []       = []
expand ('\\':cs) = expandVar cs
expand ( c :cs) = c : expand cs

expandVar :: String -> String

expandVar []           = error (" : Unexpected symbol. (expasion error)")
expandVar ('-':'>':cs) = expand cs
expandVar input@(c:cs) 
  | isSpace c     = expandVar cs
  | isAlpha c     = "\\ "++word++" -> "++(expandVar afterWord)
  | otherwise     = error (c:" : Unexpected symbol. (expasion error)")
  where
    (word, afterWord) = span isAlphaNum input

-- To parse an entire type definition, simply require all tokens to be
-- consumed.

parse :: String -> Expression
parse input = expr
  where (expr, []) = parseAbs $ scan $ expand $ input












