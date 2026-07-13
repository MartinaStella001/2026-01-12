from model.model import Model

mdl= Model()
mdl.creaGrafo(1991,1995)
nodi, archi = mdl.getDettagliGrafo()
print(f"nodi: {nodi}, archi: {archi}")