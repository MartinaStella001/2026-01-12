import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAnno1 = None
        self._choiceAnno2 = None

    def fillDDAnno(self):
        anni = self._model.getAllYears()
        for a in anni:
            self._view._ddAnno1.options.append(
                ft.dropdown.Option(data=a, text=a, on_click = self._saveDDAnno1)
            )
            self._view._ddAnno2.options.append(
                ft.dropdown.Option(data=a, text=a, on_click=self._saveDDAnno2)
            )
        self._view.update_page()
    def _saveDDAnno1(self, e):
        self._choiceAnno1 = e.control.data
        print(f"Da : {self._choiceAnno1}")

    def _saveDDAnno2(self, e):
        self._choiceAnno2 = e.control.data
        print(f"A : {self._choiceAnno2}")



    def handleCreaGrafo(self,e):
        if self._choiceAnno1 is None or self._choiceAnno2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Selezionare un anno dal menu", color="red")
            )
            self._view.update_page()
            return
        self._model.creaGrafo(self._choiceAnno1, self._choiceAnno2)
        nodi, archi = self._model.getDettagliGrafo()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato correttamnete", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {nodi}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {archi}")
        )
        self._view.update_page()

    def handleDettagli(self, e):
        best3archi = self._model.best3archi()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Archi di peso maggiore:", color="green")
        )
        for a in best3archi:
            self._view.txt_result.controls.append(
                ft.Text(f"{a[0]} --> {a[1]} ({a[2]} piloti condivisi)")
            )
        compConnesse =self._model.numCompConnesse()
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {compConnesse} componenti connesse", color="green")
        )
        compMax, listaNodiDesc = self._model.getMaxCompConn()
        self._view.txt_result.controls.append(
            ft.Text(f"Componente piu grande ({len(compMax)} nodi)", color="green")
        )
        for n in compMax:
            self._view.txt_result.controls.append(
                ft.Text(n)
            )
        self._view.txt_result.controls.append(
            ft.Text(f"Componente connessa in ordine descresente:", color="green")
        )
        for n in listaNodiDesc:
            self._view.txt_result.controls.append(
                ft.Text(f"{n[0]} (grado={n[1]})")
            )
        self._view.update_page()

    def handleCerca(self, e):

        txtIn = self._view._txtInK.value()
        try:
            intN = int(txtIn)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Inserire un numero intero",color="red")
            )
            self._view.update_page()
            return
        bestpath, bestcost = self._model.getPath(intN, self._choiceAnno1, self._choiceAnno2)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino trovato di peso ottimo {bestcost}", color="green")
        )
        for a in bestpath:
            self._view.txt_result.controls.append(
                ft.Text(a)
            )
        self._view.update_page()


