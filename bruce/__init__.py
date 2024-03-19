from .tools.lexer import create_lexer, keyword_row
from . import grammar as g


# region Tokenizer

nonzero_digits = "|".join(str(n) for n in range(1, 10))
letters = "|".join(chr(n) for n in range(ord("a"), ord("z") + 1))
capital_letters = "|".join(chr(n) for n in range(ord("A"), ord("Z") + 1))

lexer = create_lexer(
    # [
    #     keyword_row(g.let),
    #     keyword_row(g.in_k),
    #     keyword_row(g.if_k),
    #     keyword_row(g.else_k),
    #     keyword_row(g.elif_k),
    #     keyword_row(g.for_k),
    #     keyword_row(g.func),
    #     keyword_row(g.type_k),
    #     keyword_row(g.new),
    #     keyword_row(g.inherits),
    #     keyword_row(g.is_k),
    #     keyword_row(g.as_k),
    #     keyword_row(g.protocol),
    #     keyword_row(g.extends),
    #     keyword_row(g.true_k),
    #     keyword_row(g.false_k),
    #     keyword_row(g.plus),
    #     keyword_row(g.minus),
    #     keyword_row(g.times),
    #     keyword_row(g.div),
    #     keyword_row(g.mod),
    #     keyword_row(g.lt),
    #     keyword_row(g.gt),
    #     keyword_row(g.le),
    #     keyword_row(g.ge),
    #     keyword_row(g.eq),
    #     keyword_row(g.neq),
    #     keyword_row(g.concat),
    #     keyword_row(g.concat_space),
    #     keyword_row(g.conj),
    #     keyword_row(g.disj),
    #     keyword_row(g.not_t),
    #     keyword_row(g.lparen),
    #     keyword_row(g.rparen),
    #     keyword_row(g.lbrace),
    #     keyword_row(g.rbrace),
    #     keyword_row(g.lbracket),
    #     keyword_row(g.rbracket),
    #     keyword_row(g.colon),
    #     keyword_row(g.semicolon),
    #     keyword_row(g.dot),
    #     keyword_row(g.comma),
    #     keyword_row(g.then),
    #     keyword_row(g.given),
    #     keyword_row(g.bind),
    #     keyword_row(g.mut),
    #     (g.power, r"\^|\*\*"),
    #     (g.builtin_identifier, r"PI|E|print|base|self|sin|cos|sqrt|log|exp|rand")
    #     (g.type_identifier, f"({capital_letters})(_|{letters}|{capital_letters})*"),
    #     (
    #         g.identifier,
    #         f"({letters}|{capital_letters})(_|{letters}|{capital_letters}|0|{nonzero_digits})*",
    #     ),
    #     (g.number, f"({nonzero_digits})(0|{nonzero_digits})*|0"),
    # ]
    [
        (g.let, r"let"),
        (g.in_k, r"in"),
        (g.if_k, r"if"),
        (g.else_k, r"else"),
        (g.elif_k, r"elif"),
        (g.for_k, r"for"),
        (g.func, r"func"),
        (g.type_k, r"type"),
        (g.new, r"new"),
        (g.inherits, r"inherits"),
        (g.is_k, r"is"),
        (g.as_k, r"as"),
        (g.protocol, r"protocol"),
        (g.extends, r"extends"),
        (g.true_k, r"true"),
        (g.false_k, r"false"),
        (g.plus, r"\+"),
        (g.minus, r"-"),
        (g.times, r"\*"),
        (g.div, r"/"),
        (g.mod, r"%"),
        (g.lt, r"<"),
        (g.gt, r">"),
        (g.le, r"<="),
        (g.ge, r">="),
        (g.eq, r"=="),
        (g.neq, r"!="),
        (g.concat, r"@"),
        (g.concat_space, r"@@"),
        (g.conj, r"&"),
        (g.disj, r"\|"),
        (g.not_t, r"!"),
        (g.lparen, r"\("),
        (g.rparen, r"\)"),
        (g.lbrace, r"\{"),
        (g.rbrace, r"\}"),
        (g.lbracket, r"\["),
        (g.rbracket, r"\]"),
        (g.colon, r":"),
        (g.semicolon, r";"),
        (g.dot, r"\."),
        (g.comma, r","),
        (g.then, r"=>"),
        (g.given, r"\|\|"),
        (g.bind, r"="),
        (g.mut, r":="),
        (g.type_identifier, f"({capital_letters})(_|{letters}|{capital_letters})*"),
        (
            g.identifier,
            f"({letters}|{capital_letters})(_|{letters}|{capital_letters}|0|{nonzero_digits})*",
        ),
        (g.number, f"({nonzero_digits})(0|{nonzero_digits})*|0"),
        ("space", "  *"),
        ("newline", "\n"),
    ],
    g.GRAMMAR.EOF,
)

# endregion
