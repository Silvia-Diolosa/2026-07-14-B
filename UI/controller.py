import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self.choiceFilm = None

    def fillDD(self):
        generi = self._model.getAllGenre()
        for g in generi:
            self._view._ddGenre.options.append(ft.dropdown.Option(g))


    def handleCreaGrafo(self, e):
        genere = self._view._ddGenre.value
        if genere is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("inserire un genere"))
            return

        self._model.buildGraph(genere)
        nNodi, nArchi = self._model.getGraphDetails()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text("Grafo correttamente creato.", color="green"))
        self._view._txt_result.controls.append(
            ft.Text(f"Nodi: {nNodi}, Archi: {nArchi}"))

        self._view._btnStampaInfo.disabled = False
        self.fillDDFilm()

        self._view.update_page()

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        numCompConn = len(self._model.CompConn())
        self._view._txt_result.controls.append(ft.Text(f"Numero comp conn: {numCompConn}"))

        filmMaxArchiOut, best = self._model.getFilmMaxArchiOut()
        self._view._txt_result.controls.append(ft.Text(f"film maggior numero archi uscenti: {filmMaxArchiOut}: {best} archi"))

        bestCompConn, n = self._model.bestCompConn()
        self._view._txt_result.controls.append(ft.Text(f"la best comp conn ha: {n} archi"))

        for film in bestCompConn:
            self._view._txt_result.controls.append(ft.Text(f"{film.title}, {len(film.listActor)} "))


        self._view.update_page()

    def fillDDFilm(self):
        nodes = self._model.getNodes()
        for node in nodes:
            self._view._ddMovie.options.append(ft.dropdown.Option(data=node,
                                                                 key=node.title,
                                                                 on_click=self.handleChoiceFilm))

    def handleChoiceFilm(self, e):
        self.choiceFilm = e.control.data


    def handleTrovaSelezione(self, e):
        scelta = self.choiceFilm
        if scelta is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Selezionare un valore dal menu."))
            self._view.update_page()
            return

        txt = self._view._txtInN.value

        if txt is None :
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserire un valore."))
            self._view.update_page()
            return

        try:
            val = int(txt)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserire un valore intero."))
            self._view.update_page()
            return

        if val < 1:
            self._view._txt_result.controls.append(
                ft.Text("Inserire un valore intero maggiore di 0."))
            self._view.update_page()
            return

        bestPath, bestScore = self._model.getBestPath(scelta, txt)

        if bestPath == []:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Non ci sono risultati"))
            self._view.update_page()
            return

        a = bestPath.sort(key=lambda x: x.title)
        for film in a:
            self._view._txt_result.controls.append(ft.Text(f"{film.title}, {film.yaer} {len(film.listActor)} "))

        c = len(bestPath)
        self._view._txt_result.controls.append(ft.Text(f"la lunghezza è {c}"))

        d = bestScore
        self._view._txt_result.controls.append(ft.Text(f"la valutazione media complessiva è {d}"))

        self._view.update_page()

    