from z3 import *
import pandas as pd
import operator

# Reading the data
crashes = {(row['Street1'], row['Street2']): row['Crash'] for index, row in pd.read_csv('intersection.csv').iterrows()}
street_details = {row['Street']: [row['HasTraffic'], row['GreenSignal']] for index, row in pd.read_csv('street.csv').iterrows()}


truth_table = []

for (street1, street2), crash in crashes.items():
    street1_details = street_details.get(street1, [False, False])
    street2_details = street_details.get(street2, [False, False])
    truth_table.append([
        street1_details[1],  # street1-greensignal
        street1_details[0],  # street1-hastraffic
        street2_details[1],  # street2-greensignal
        street2_details[0],  # street2-hastraffic
        crash                #if-crash
    ])


unary_ops = {
    'NOT': operator.not_
}

binary_ops = {
    'AND': operator.and_,
    'OR': operator.or_,
    'XOR': operator.xor,
    'NAND': lambda a, b: not (a and b),
    'NOR':  lambda a, b: not (a or b)
}

def eval_expr(expr, vals):
    """Evaluate the expression"""
    if isinstance(expr, str):
        return vals[expr]
    if len(expr) == 2:
        op, sub_expr = expr
        return unary_ops[op](eval_expr(sub_expr, vals))
    if len(expr) == 3:
        left, op, right = expr
        return binary_ops[op](eval_expr(left, vals), eval_expr(right, vals))
    return expr

def generate_expressions(vars):
    """Yield all possible boolean expressions over given vars."""
    if len(vars) == 1:
        yield vars[0]
        for uop in unary_ops.keys():
            yield (uop, vars[0])
    else:
        for i in range(1, len(vars)):
            for left_expr in generate_expressions(vars[:i]):
                for right_expr in generate_expressions(vars[i:]):
                    for op in binary_ops.keys():
                        yield (left_expr, op, right_expr)

def find_expressions_for_truth_table(truth_table):
    var_count = len(truth_table[0]) - 1
    variables = [chr(ord('A') + i) for i in range(var_count)]
    for expr in generate_expressions(variables):
        all_match = True
        for row in truth_table:
            vals = dict(zip(variables, row[:var_count]))
            if eval_expr(expr, vals) != row[-1]:
                all_match = False
                break
        if all_match:
            yield expr

def format_expression(expr):
    if isinstance(expr, tuple):
        if len(expr) == 2:
            return f"({expr[0]} {format_expression(expr[1])})"
        else:
            return f"({format_expression(expr[0])} {expr[1]} {format_expression(expr[2])})"
    else:
        return str(expr)
results = list(find_expressions_for_truth_table(truth_table))
for r in results:
    print(format_expression(r))
