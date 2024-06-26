from ..grammar import Grammar, Terminal
from ..parser import evaluate_parse, create_parser
from ..token import Token
from .automata import nfa_to_dfa
from . import ast


GRAMMAR = Grammar()

# region TERMINALS

pipe = GRAMMAR.add_terminal("|")
star, question = GRAMMAR.add_terminals("* ?")
lparen, rparen = GRAMMAR.add_terminals("( )")
symbol, range_t = GRAMMAR.add_terminals("s -")

# endregion

# region NON TERMINALS

Rgx = GRAMMAR.add_non_terminal("regex", True)
Concats, MoreConcats, MoreUnions = GRAMMAR.add_non_terminals(
    "concats more_concats more_unions"
)
Atom, Range, Quantifier = GRAMMAR.add_non_terminals("atom range qtfier")

# endregion

# region PRODUCTIONS

Rgx %= Concats + MoreUnions, lambda h, s: s[2], None, lambda h, s: s[1]
MoreUnions %= (
    pipe + Concats + MoreUnions,
    lambda h, s: s[3],
    None,
    None,
    lambda h, s: ast.UnionNode(h[0], s[2]),
)
MoreUnions %= GRAMMAR.Epsilon, lambda h, s: h[0]

Concats %= Atom + MoreConcats, lambda h, s: s[2], None, lambda h, s: s[1]
MoreConcats %= (
    Atom + MoreConcats,
    lambda h, s: s[2],
    None,
    lambda h, s: ast.ConcatNode(h[0], s[1]),
)
MoreConcats %= GRAMMAR.Epsilon, lambda h, s: h[0]

Atom %= (
    lparen + Rgx + rparen + Quantifier,
    lambda h, s: s[4],
    None,
    None,
    None,
    lambda h, s: s[2],
)
Atom %= (
    symbol + Range + Quantifier,
    lambda h, s: s[3],
    None,
    lambda h, s: s[1],
    lambda h, s: s[2],
)

Range %= range_t + symbol, lambda h, s: ast.RangeNode(h[0], s[2])
Range %= GRAMMAR.Epsilon, lambda h, s: ast.SymbolNode(h[0])

Quantifier %= (
    star + Quantifier,
    lambda h, s: s[2],
    None,
    lambda h, s: ast.ClosureNode(h[0]),
)
Quantifier %= (
    question + Quantifier,
    lambda h, s: s[2],
    None,
    lambda h, s: ast.UnionNode(h[0], ast.EpsilonNode()),
)
Quantifier %= GRAMMAR.Epsilon, lambda h, s: h[0]


# endregion

parser = create_parser(GRAMMAR)


def regex_tokenizer(text: str, G: Grammar, char_terminal: Terminal):
    tokens: list[Token] = []
    fixed_chars = [t.name for t in G.terminals if t != char_terminal]

    scaping = False
    for char in text:
        if scaping:
            tokens.append(Token(char, char_terminal))
            scaping = False
        elif char == "\\":
            scaping = True
        else:
            tokens.append(
                Token(
                    char, G.symbol_dict[char] if char in fixed_chars else char_terminal
                )
            )

    tokens.append(Token(G.EOF.name, G.EOF))
    return tokens


class Regex:
    def __init__(self, text):
        tokens = regex_tokenizer(text, GRAMMAR, symbol)
        left_parse = parser([token for token in tokens])
        ast = evaluate_parse(left_parse, tokens)
        nfa = ast.evaluate()
        self.automaton = nfa_to_dfa(nfa)

    def __call__(self, text: str):
        return self.automaton.recognize(text)
