import copy
import itertools

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self.idMap = {}
        self._bestPath = []
        self._bestScore = 0

    def getAllGenre(self):
        return DAO.getAllGenre()

    def buildGraph(self, genere):
        self._graph.clear()
        self.idMap.clear()

        nodes = DAO.getAllNodes(genere)

        for node in nodes:
            self.idMap[node.id] = node

        self._graph.add_nodes_from(nodes)

        self.associaAttoriAFilm(genere)

        self.addEdges()


    def associaAttoriAFilm(self, genere):
        tutti = DAO.getFilmAttore(genere)
        for filmId, attoreId in tutti:
            if filmId in self.idMap:
                film = self.idMap[filmId]
                film.listActor.append(attoreId)

    def addEdges(self):

        for a, b in itertools.combinations(self.getNodes(), 2):
            condivisi = self.calcolaCondivisi(a,b)
            if condivisi == 0:
                continue
            if a.year is None or b.year is None:
                self._graph.add_edge(a, b)
                self._graph.add_edge(b, a)
                continue
            if a.year == b.year :
                self._graph.add_edge(a, b)
                self._graph.add_edge(b, a)
                continue

            if a.year < b.year:
                self._graph.add_edge(a, b)
            else:
                self._graph.add_edge(b, a)

    def calcolaCondivisi(self, u, v):
        condivisi = 0
        for attoreU in u.listActor:
            for attoreV in v.listActor:
                if attoreU == attoreV:
                    condivisi = condivisi + 1
        return condivisi


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getNodes(self):
        return list(self._graph.nodes)

    def getEdges(self):
        return list(self._graph.edges(data=True))


    def CompConn(self):
        components = list(nx.weakly_connected_components(self._graph))
        return components
    # return nx.number_connected_components(self._graph.to_undirected())

    def getFilmMaxArchiOut(self):
        best = 0
        nodeBest = None
        for node in self.getNodes():
            n = len(self._graph.out_edges(node))
            if n > best:
                best = n
                nodeBest = node
        return nodeBest, best

    def bestCompConn(self):
       components = list(nx.weakly_connected_components(self._graph))
       largest = list(max(components, key=len))

       largest.sort(key=lambda x: len(x.listActor), reverse=True)
       return largest, len(largest)


    def getBestPath(self, partenza, n):
        self._bestPath = []
        self._bestScore = -1
        parziale = [partenza]

        i = 0
        compConn = []
        for c in self.CompConn():
            if partenza not in c:
                compConn.append(c)


        self.ricorsione(parziale, n, compConn, i)

        return self._bestPath, self._bestScore


    def ricorsione(self, parziale, n, compConn, i):
        # caso terminale
        if len(parziale) == n:
            score = self.calcolaScore(parziale)
            if score > self._bestScore:
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)
            return

        # caso ricorsivo

        if i >= len(compConn):
            return

        for nodo in compConn[i]:
            parziale.append(nodo)
            self._ricorsione5(parziale, n, compConn, i+1)
            parziale.pop()

    def _ricorsioneR5(self, components, k, parziale, indexComponente):
        # caso base
        if len(parziale) == k:
            val = self._valuta(parziale)
            if val > self._bestVal:
                self._bestVal = val
                self._bestSet = list(parziale)
            return

        # terminazione / pruning
        if indexComponente >= len(components):
            return
        if (len(components) - indexComponente) < (k - len(parziale)):
            return

        componente = components[indexComponente]

        # BRANCH 1: prendo un film da questa componente
        for nodo in componente:
            parziale.append(nodo)
            self._ricorsioneR5(components, k, parziale, indexComponente + 1)
            parziale.pop()

        # BRANCH 2: salto questa componente
        self._ricorsioneR5(components, k, parziale, indexComponente + 1)

    def _valuta(self, parziale):
        return sum(m.avg_rating for m in parziale if m.avg_rating is not None)

    def calcolaScore(self, parziale):
        score = 0
        for node in parziale:
            if node.avg_rating is not None:
                score += node.avg_rating
        return score
