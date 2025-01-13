import itertools

def generate_truth_table(expression, variables):
    """Generate a truth table for the given boolean expression."""
    table = []
    for values in itertools.product([False, True], repeat=len(variables)):
        env = dict(zip(variables, values))
        result = eval(expression, {}, env)
        table.append([int(v) for v in values] + [int(result)])
    return table

def print_truth_table(table, variables):
    """Print the truth table."""
    header = variables + ['Result']
    print(' | '.join(header))
    print('-' * (len(header) * 4))
    for row in table:
        print(' | '.join(map(str, row)))

# Example usage
expression = input("Enter a boolean expression: ")
variables = input("Enter the variables separated by commas: ").split(',')
truth_table = generate_truth_table(expression, variables)
print(truth_table)
