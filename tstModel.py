from model.model import Model

mymodel = Model()
mymodel.getTeamsOfYear(2012)
mymodel.creaGrafo(2012)
nodi, archi = mymodel.getGraphDetails()
print(f"Grafo creato correttamente. Il grafo ha {nodi} e {archi} archi")

v0 = mymodel.getRandomNode()
path, score = mymodel.getPathV2(v0)

print(f"trovata soluzione lunga {len(path)} con somma pesi e archi pari {score}")
for p in path:
    print(p)