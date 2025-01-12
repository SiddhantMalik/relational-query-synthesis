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
        crash
    ])


#commented the ops because earlier it was giving many possible equations
ops = {
    'AND': operator.and_,
    'OR': operator.or_,
    # 'XOR': operator.xor,
    # 'NAND': lambda a, b: not operator.and_(a, b),
    # 'NOR':  lambda a, b: not operator.or_(a, b)
}

def eval_expr(expr, vals):
    """Evaluate the expression"""
    if isinstance(expr, str):
        return vals[expr]
    if len(expr) == 3:
        left, op, right = expr
        return ops[op](eval_expr(left, vals), eval_expr(right, vals))
    return expr  # single literal or bool

def generate_expressions(vars):
    """Yield all possible boolean expressions over given vars."""
    if len(vars) == 1:
        yield vars[0]
    else:
        for i in range(1, len(vars)):
            for left_expr in generate_expressions(vars[:i]):
                for right_expr in generate_expressions(vars[i:]):
                    for op in ops.keys():
                        yield (left_expr, op, right_expr)

def find_expressions_for_truth_table(truth_table):
    var_count = len(truth_table[0]) - 1
    variables = [chr(ord('A') + i) for i in range(var_count)]
    # Validate expressions
    for expr in generate_expressions(variables):
        all_match = True
        for row in truth_table:
            vals = dict(zip(variables, row[:var_count]))
            if eval_expr(expr, vals) != row[-1]:
                all_match = False
                break
        if all_match:
            yield expr

results = list(find_expressions_for_truth_table(truth_table))
for r in results:
    print(r)
