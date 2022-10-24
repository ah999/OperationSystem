import pyomo.environ as pyo
import pandas as pd
import numpy as np


class Solver():
    def get_solution(self, date, opRoomsInfo, ops):

        # operations
        # table = [(str(e).split()[1].strip('>'), e.doctor, e.operation_date, e.department_name,
        #           e.operation_duration, e.operation_urgency, e.operation_room) for e in user_entries]
        #

        print(ops)
        print('ops')
        table = [(str(e).split()[1].strip('>'), e.doctor_name, e.patient_id, e.date,
                  e.duration, e.emergency, e.department_id, e.room_id) for e in ops]
        print(table)
        print('table')
        basket = pd.DataFrame(table, columns=[
                              'id', 'doctor', 'patient_id', 'operation_date', 'operation_duration', 'operation_urgency', 'department_name', 'room_id'])
        basket.index = basket['id']
        print(basket)

        # departments
        # table2 =[(str(e).split()[1].strip('>'),e.department_name, e.department_capacity,e.date) for e in departments_info]
        # dep_df=pd.DataFrame(table2, columns=['id','department_name','department_capacity','date'])
        # dep_df.set_index('id')
        # dep_df['department_capacity']=dep_df['department_capacity'].astype(int)

        # operation rooms
        print(opRoomsInfo)
        print('opRoomsInfo')
        table3 = [(str(o).split()[1].strip('>'), o.name,
                   o.capacity, o.date) for o in opRoomsInfo]
        print(table3)
        print('table3')

        op_df = pd.DataFrame(
            table3, columns=['id', 'name', 'capacity', 'date'])
        op_df.set_index('id')
        op_df['capacity'] = op_df['capacity'].astype(int)
        print(op_df)

        mdl = pyo.ConcreteModel()

        mdl.invs = pyo.Set(initialize=list(
            zip(basket.index, basket["department_name"])))
        mdl.bins = pyo.Set(initialize=list(op_df.name))

        mdl.value = pyo.Param(mdl.invs, initialize={(
            row["id"], row["department_name"]): row["operation_urgency"] for i, row in basket.iterrows()})
        mdl.weight = pyo.Param(mdl.invs, initialize={(
            row["id"], row["department_name"]): row["operation_duration"] for i, row in basket.iterrows()})
        mdl.bin_cap = pyo.Param(mdl.bins, initialize={
                                row["name"]: row["capacity"] for i, row in op_df.iterrows()})
        #mdl.dep_cap = pyo.Param(mdl.deps, initialize= {row["department_name"]:row["department_capacity"] for i,row in dep_df.iterrows()}, mutable=True)

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

        # save the output into dictionary
        dic = dict()

        for i in mdl.X:
            if pyo.value(mdl.X[i]) == 1:
                dic[i[0]] = i[2]

        if basket.index.isin(list(dic.keys())).all():
            basket['operation_room'] = basket.index.map(dic)
            return basket

        else:
            return []
