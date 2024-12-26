from z3 import *

#initializing the data
Intersects = {
    ("Broadway", "Liberty St"),
    ("Broadway", "Wall St"),
    ("Broadway", "Whitehall"),
    ("Liberty St", "Broadway"),
    ("Liberty St", "William St"),
    ("Wall St", "Broadway"),
    ("Wall St", "William St"),
    ("Whitehall", "Broadway"),
    ("William St", "Liberty St"),
    ("William St", "Wall St"),
}
HasTraffic = {"Broadway", "Wall St", "William St", "Whitehall"}
GreenSignal = {"Broadway", "Liberty St", "William St", "Whitehall"}

x, y = String("a"), String("b")

solver = Solver()

#defining constraints
intersection_constraint = Or([And(x == a, y == b) for a, b in Intersects])
traffic_constraint = And(
    Or([x == street for street in HasTraffic]),
    Or([y == street for street in HasTraffic]),
)
green_signal_constraint = And(
    Or([x == street for street in GreenSignal]),
    Or([y == street for street in GreenSignal]),
)

# Adding constraints to the solver
solver.add(intersection_constraint)
solver.add(traffic_constraint)
solver.add(green_signal_constraint)

if solver.check() == sat:
    model = solver.model()
    print(f"Crash found at: ({model[x]}, {model[y]})")
else:
    print("No crashes found.")
