import json
import re

from pyeda.boolalg.expr import exprvar, OrOp, AndOp, Complement, Variable, expr

expression_variables = {}
document_locations = set()


def read_inverted_index():
    with open('inverted_index.json', 'r') as file:
        data = json.load(file)
    return data


def boolean_search(expression, variables_map, inverted_index):
    global document_locations, expression_variables
    document_locations = {location for locations in inverted_index.values() for location in locations}
    expression_variables = variables_map

    simplified_expr = simplify_expression(expression)
    result_set = iterate_expression(simplified_expr)

    if (len(result_set) > 0):
        print(f"Found {len(result_set)} documents: {result_set}")
    else:
        print("No documents found")


def parse_expression(expression):
    variables = {var: exprvar(var) for var in expression_variables.keys()}
    return eval(expression, variables)


def simplify_expression(expression):
    return expression.simplify()


def find_word_in_docs(word):
    locations = inverted_index.get(expression_variables.get(word))
    if locations is None:
        return set()
    return locations


def iterate_expression(expression):
    if type(expression) is Complement:
        return document_locations.difference(find_word_in_docs(str(expression)[1::]))
    elif type(expression) is OrOp:
        return set().union(*[iterate_expression(child) for child in expression.xs])
    elif type(expression) is AndOp:
        result_set = document_locations
        for child in expression.xs:
            result_set = result_set.intersection(iterate_expression(child))
        return result_set
    elif type(expression) is Variable:
        return find_word_in_docs(str(expression))
    else:
        return set()


def map_query_words(expression):
    words = re.findall(r'[а-яА-ЯёЁ]+', expression)
    latin_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    variables_map = {}
    result = expression

    for i, word in enumerate(words):
        if i < len(latin_alphabet):
            variables_map[latin_alphabet[i]] = word
            result = result.replace(word, latin_alphabet[i])

    return result, variables_map


if __name__ == "__main__":
    inverted_index = read_inverted_index()

    while True:
        user_input = input("Input search expression:\n")
        if user_input.lower() == 'exit':
            exit()

        expression, variables_map = map_query_words(user_input.lower())
        boolean_search(expr(expression), variables_map, inverted_index)
