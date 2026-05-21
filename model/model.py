import copy
import itertools
import random

import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []
        self._idMapTeams = None
        self._bestPath = []
        self._bestObjVal = 0

    def getPath(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

    def getPathV2(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        listaVicini = self.getNeighbors(parziale[-1])
        parziale.append(listaVicini[0][0])
        self._ricorsioneV2(parziale)

        return self._bestPath, self._bestObjVal

    def _ricorsione(self, parziale):
         # 1 Verifico se la parziale è migliore del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        # 2 Verifico se posso continuare

        # 3 Faccio la mia ricorsione
        for v in self._grafo.neighbors(parziale[-1]):

            pesoE = self._grafo[parziale[-1]][v]["weight"]
            # Peso arco che mi ha portato dall'ultimo nodo che ho messo in parziale a v

            if self._grafo[parziale[-2]][parziale[-1]]["weight"] > pesoE and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def _ricorsioneV2(self, parziale):
        # 1 Verifico se la parziale è migliore del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        # 2 Verifico se posso continuare

        # 3 Faccio la mia ricorsione
        listaVicini = self.getNeighbors(parziale[-1])

        for v in listaVicini:
            if v[0] not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > v[1]:
                parziale.append(v[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return


        for v in self._grafo.neighbors(parziale[-1]):

            pesoE = self._grafo[parziale[-1]][v]["weight"]
            # Peso arco che mi ha portato dall'ultimo nodo che ho messo in parziale a v

            if self._grafo[parziale[-2]][parziale[-1]]["weight"] > pesoE and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def _score(self, parziale):
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._grafo[parziale[i]][parziale[i+1]]["weight"]

        return score

    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)

       # for u in self._grafo.nodes:
        #    for v in self._grafo.nodes:
         #       if u != v:
          #          self._grafo.add_edge(u, v)

        # Al posto di fare doppio ciclo, posso usare librearia esterna
        myedges = list(itertools.combinations(self._teams, 2))
        self._grafo.add_edges_from(myedges)

        mapSalary = DAO.getSalariesTeam(year, self._idMapTeams)

        for e in self._grafo.edges:
            sal1 = mapSalary[e[0]] #Salario 1 team
            sal2 = mapSalary[e[1]] #Salario 2 team
            peso = sal1 + sal2
            self._grafo[e[0]][e[1]]["weight"] = peso

    def getNeighbors(self, source):
        vicini = self._grafo.neighbors(source)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self._grafo[source][v]["weight"]))

        viciniTuples.sort(key= lambda x: x[1], reverse=True)
        return viciniTuples

    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        self._idMapTeams = {t.ID: t for t in self._teams}
        return self._teams

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getAllYears(self):
        return DAO.getAllYears()

    def getRandomNode(self):
        index = random.randint(0, len(self._teams))
        return self._teams[index]

