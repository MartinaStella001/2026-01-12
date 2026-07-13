import copy
from cmath import inf

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._costruttori = []
        self._idMapCostruttori = {}
        self._maxV = None
        self._minV = None
        self._bestPath = []
        self._bestCost = inf



    def getAllYears(self):
        return DAO.getAllYears()

    def creaGrafo(self, anno1, anno2):
        self._grafo.clear()
        self._costruttori = DAO.getAllCostruttori(anno1,anno2)
        for c in self._costruttori:
            self._idMapCostruttori[c.constructorId] = c
        self._grafo.add_nodes_from(self._costruttori)
        self._edges = DAO.getAllEdges(anno1,anno2,self._idMapCostruttori)
        for e in self._edges:
            self._grafo.add_edge(e.costruttore1, e.costruttore2, weight=e.numPiloti)


    def getDettagliGrafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def best3archi(self):
        listaArchi = []
        for u,v,data in self._grafo.edges(data=True):
            listaArchi.append((u, v, data["weight"]))
        listaArchi.sort(key=lambda x: x[2], reverse=True)
        return listaArchi[:3]

    def numCompConnesse(self):
        components = list(nx.connected_components(self._grafo))
        return len(components)
    def getMaxCompConn(self):
        components = list(nx.connected_components(self._grafo))
        maxComp = None
        maxLenComp = 0
        for c in components:
            if len(c) > maxLenComp:
                maxLenComp = len(c)
                maxComp = c

        maxCompGrafo = nx.subgraph(self._grafo, maxComp)
        listaNodiGrado = []
        for c in maxCompGrafo:
            grado  = maxCompGrafo.degree(c)
            listaNodiGrado.append((c, grado))
        listaNodiGrado.sort(key=lambda x:x[1], reverse=True)
        return maxComp, listaNodiGrado

    # Si vuole valutare la diversità anagrafica dei "veterani" (piloti più anziani) nelle diverse scuderie. Dato un valore K
    # intero fornito dall'utente, l'obiettivo del programma è di identificare un set di K costruttori distinti tale per cui:
    # a) Ciascun costruttore faccia parte di una componente connessa distinta, ovvero i costruttori selezionati non
    # devono aver mai condiviso piloti tra loro;
    # b) La differenza fra la data di nascita del pilota più anziano che ha corso per ciascun costruttore sia minima. In
    # altre parole, per ogni costruttore si identifichi il "veterano" (il pilota con data di nascita più vecchia che ha
    # corso per quel team nel periodo selezionato), e si minimizzi il range di età tra questi veterani.
    # SUGGERIMENTO: Per risolvere questo punto, una strategia è quella di  scrivere un metodo del DAO che interroghi il
    # db per ottenere la data di nascita (campo dob della tabella drivers) del pilota più anziano che ha corso per una certa
    # scuderia, e di utilizzare tale metodo per riempire il campo “oldest_driver_dob” della classe Constructor proposta nel
    # codice fornito.
    # Si stampino la lista dei K costruttori selezionati, lo scarto di età in giorni, il costruttore con il veterano più giovane e
    # quello con il veterano più anziano.

    def getPath(self, K,anno1,anno2):
        self._bestPath =[]
        self._bestCost = inf
        parziale =[]
        indiceComp = 0
        for c in DAO.getVeteranoFrom(anno1,anno2,self._idMapCostruttori):
            c[0].oldest_driver_dob = c[1]
        components = list(nx.connected_components(self._grafo))
        if len(components) <K:
            return None,0
        self._ricorsione(components,parziale, indiceComp, K)

        return self._bestPath, self._bestCost, self._maxV, self._minV

    def _ricorsione(self, components, parziale, indiceComp, K):
        if len(parziale) == K:
            if self._getRangeMin(parziale) < self._bestCost:
                self._bestPath = copy.deepcopy(parziale)
                self._bestCost = self._getRangeMin(parziale)
            return

        if indiceComp >= len(components):
            return
        if len(parziale) + (len(components)-indiceComp) < K:
            return
        componente = components[indiceComp]
        for c in componente:
            if c not in parziale:
                parziale.append(c)
                self._ricorsione(components, parziale, indiceComp+1, K)
                parziale.pop()
        self._ricorsione(components, parziale, indiceComp+1, K)



    def _getRangeMin(self,parziale):

        listaDateNasciteVet =[]
        for p in parziale:
            listaDateNasciteVet.append((p,p.oldest_driver_dob))

        listaDateNasciteVet.sort(key=lambda x: x[1], reverse=True)
        self._youngestVetCon = listaDateNasciteVet[0][0]
        self._oldestVetCon = listaDateNasciteVet[-1][0]
        return (listaDateNasciteVet[0][1])-(listaDateNasciteVet[-1][1]).days






