from z3 import *
import pandas as pd
import itertools
from sympy import symbols, Or, And, Not 
from sympy.logic.boolalg import to_dnf, simplify_logic

# Reading the data
crashes = {(row['Street1'], row['Street2']): row['Crash'] for index, row in pd.read_csv('intersection.csv').iterrows()}
street_details = {row['Street']: [row['HasTraffic'], row['GreenSignal']] for index, row in pd.read_csv('street.csv').iterrows()}
solver = Solver()
x, y = String("a"), String("b")

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

# print(truth_table)

def truth_table_to_boolean(truth_table):
    A, B, C, D = symbols('street1-greensignal street1-hastraffic street2-greensignal street2-hastraffic')
    terms = []

    for row in truth_table:
        if row[-1] == 1:  # Considering only the rows where the output is 1
            term = []
            term.append(A if row[0] == 1 else Not(A))
            term.append(B if row[1] == 1 else Not(B))
            term.append(C if row[2] == 1 else Not(C))
            term.append(D if row[3] == 1 else Not(D))
            terms.append(And(*term))
    
    boolean_expression = Or(*terms)
    simplified_expression = simplify_logic(boolean_expression, form='dnf')
    return simplified_expression

print(truth_table_to_boolean(truth_table))