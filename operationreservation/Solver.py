import pyomo.environ as pyo
import pandas as pd

class Solver():
    def get_solution(self, opRoomsInfo, ops):


        table = [(str(e).split()[1].strip('>'),e.id, e.doctor_name, e.patient_id, e.date,
                  e.duration, e.emergency, e.department_id, e.room_id) for e in ops]
        basket = pd.DataFrame(table, columns=[
            'name','id', 'doctor_name', 'patient_id', 'date', 'duration',
            'emergency', 'department_id', 'room_id'])
        basket.index = basket['id']
        basket = basket.drop(columns='name')


        # operation rooms
        table3 = [(str(o).split()[1].strip('>'), o.name,
                   o.capacity, o.date) for o in opRoomsInfo]


        op_df = pd.DataFrame(table3, columns=['id', 'name', 'capacity', 'date'])
        op_df.set_index('id')
        op_df['capacity'] = op_df['capacity'].astype(int)


        mdl = pyo.ConcreteModel()

        mdl.invs = pyo.Set(initialize=list(zip(basket.index, basket["department_id"])))

        mdl.bins = pyo.Set(initialize=list(op_df.name))

        mdl.value = pyo.Param(mdl.invs, initialize={(row["id"], row["department_id"]): row["emergency"] for i, row in basket.iterrows()})

        mdl.weight = pyo.Param(mdl.invs, initialize={(row["id"], row["department_id"]): row["duration"] for i, row in basket.iterrows()})

        mdl.bin_cap = pyo.Param(mdl.bins, initialize={row["name"]: row["capacity"] for i, row in op_df.iterrows()})
        print('mdl')
        print(mdl)

        # vars
        # the amount from invoice i in bin j
        mdl.X = pyo.Var(mdl.invs, mdl.bins, within=pyo.Binary)

        ### Objective ###
        mdl.OBJ = pyo.Objective(expr=sum(
            mdl.X[i, b]*mdl.value[i] for i in mdl.invs for b in mdl.bins), sense=pyo.maximize)

        # don't overstuff bin
        def bin_limit(self, b):
            return sum(mdl.X[i, b]*mdl.weight[i] for i in mdl.invs) <= mdl.bin_cap[b]
        mdl.bin_limit = pyo.Constraint(mdl.bins, rule=bin_limit)

        # one_item can be only in a single op room.
        def one_item(self, i, d):
            return sum(mdl.X[i, d, b] for b in mdl.bins) <= 1
        mdl.one_item = pyo.Constraint(mdl.invs, rule=one_item)

        # solve it...
        solver = pyo.SolverFactory('glpk')
        results = solver.solve(mdl)
        print(results)
        print(mdl)

        # save the output into dictionary
        dic = dict()

        for i in mdl.X:
            if pyo.value(mdl.X[i]) == 1:
                dic[i[0]] = i[2]

        if basket.index.isin(list(dic.keys())).all():
            basket['room_id'] = basket.index.map(dic)
            basket=basket.drop(columns='id')
            print(type(basket))
            print(basket)
            return basket

        else:
            return []
