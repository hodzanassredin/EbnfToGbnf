from lark import Lark, Tree, Token
import sys
# Определение грамматики EBNF в формате Lark
ebnf_grammar = """
    start: rule+
    rule: ID "=" expression "."
    expression: term ("|" term)*
    term: factor+
    factor: ID
          | STRING
          | grouping
          | optional
          | repetition
          | range
    grouping: "(" expression ")"
    optional: "[" expression "]"
    repetition: "{" expression "}"
    ID: /[a-zA-Z_][a-zA-Z0-9_]*/
    STRING: (/"[^"]*"/) | (/'[^']*'/)
    range: STRING "." "." STRING
    %import common.WS
    %ignore WS
"""



def rebuild_expression(expression_node, rule_names, wrap = False):
    terms = []
    for term_node in expression_node.children:
        terms.append(rebuild_term(term_node, rule_names))
    joined = " | ".join(terms)
    return f"({joined})" if wrap else joined

def rebuild_term(term_node, rule_names):
    factors = []
    for factor_node in term_node.children:
        factors.append(rebuild_factor(factor_node, rule_names))
    return " ".join(factors)

def rebuild_optional(node, rule_names):
    expr = rebuild_expression(node.children[0], rule_names, False)
    return f"({expr})?" 

def rebuild_grouping(node, rule_names):
    expr = rebuild_expression(node.children[0], rule_names, False)
    return f"({expr})" 

def rebuild_repetition(node, rule_names):
    expr = rebuild_expression(node.children[0], rule_names, False)
    return f"({expr})*" 

def rebuild_range(node, rule_names):
    return f"[{node.children[0].value.strip('"')}-{node.children[1].value.strip('"')}]" 

def rebuild_factor(factor_node, rule_names):
    result = []
    
    for child in factor_node.children:
        if isinstance(child, Tree):
            if child.data == "optional":
                result.append(rebuild_optional(child,rule_names))
            elif child.data == "grouping":
                result.append(rebuild_grouping(child,rule_names))
            elif child.data == "repetition":
                result.append(rebuild_repetition(child,rule_names))
            elif child.data == "range":
                result.append(rebuild_range(child,rule_names))
            #items.append(rebuild_expression(ch, True))
        elif isinstance(child, Token):
            if child.value in rule_names:
                result.append(child.value)
            elif child.value.startswith("\""):
                result.append(child.value)
            else:
                result.append(f"\"{child.value}\"")
        else:
            print("UPS")
    return "".join(result)

def rebuild_rule(rule_node, rule_names):
    id_node = rule_node.children[0]
    expression_node = rule_node.children[1]
    return f"{id_node.value} ::= {rebuild_expression(expression_node, rule_names)}"

def rebuild_ebnf(tree):
    rule_names = [c.children[0].value for c in tree.children if c.data == 'rule']
    
    result = []
    for child in tree.children:
        if child.data == "rule":
            result.append(rebuild_rule(child, rule_names))
        else:
            result.append(rebuild_expression(child, rule_names))
    return "\n".join(result)

# Создаем парсер
ebnf_parser = Lark(ebnf_grammar, start='start')

def convert(fname):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            parsed = ebnf_parser.parse(content)
            result = rebuild_ebnf(parsed)
            print(result)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: python main.py <file_name>")
    else:
        file_name = sys.argv[1]
        convert(file_name)

