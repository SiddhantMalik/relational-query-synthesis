import itertools

def generate_truth_table(expression, variables):
    """Generate a truth table for the given boolean expression."""
    table = []
    for values in itertools.product([False, True], repeat=len(variables)):
        env = dict(zip(variables, values))
        result = eval(expression, {}, env)
        table.append([int(v) for v in values] + [int(result)])
    return table

expression = input("Enter a boolean expression: ")
variables = input("Enter the variables separated by commas: ").split(',')
truth_table = generate_truth_table(expression, variables)
print(truth_table)
