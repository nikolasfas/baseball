import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceTeam = None

    def handleCreaGrafo(self, e):
        self._model.creaGrafo(self._view._ddAnno.value)
        n, m = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo creato correttamente. Il grafo è costituito di {n} ed {m} archi")
        )
        self._view.update_page()

    def handleDettagli(self, e):
        if self._choiceTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Attenzione, selezionare un team.", color="red")
            )
            self._view.update_page()
            return


        neighborsTuple = self._model.getNeighbors(self._choiceTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Il nodo {self._choiceTeam} ha {len(neighborsTuple)} vicini.", color="green")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Di seguito una lista ordinata di vicini", color="green")
        )
        for n in neighborsTuple:
            self._view._txt_result.controls.append(
                ft.Text(f"{n[0]} - peso {n[1]}", color="green")
            )
        self._view.update_page()

    def handlePercorso(self, e):
        pass

    def _fillddYears(self):
        years = self._model.getAllYears()

        yearsDD = []
        #for y in years:
        #    yearsDD.append(
        #        ft.dropdown.Option(y)
        #    )

           # Prima cosa è la funzione e la seconda è un iterable
            # Meglio mettere le mappe all'interno di una list
        yearsDD = list(map(lambda x: ft.dropdown.Option(x), years))
        self._view._ddAnno.options = yearsDD
        self._view.update_page()

    def handleYearSelection(self, e):
        # Questo metodo viene chiamato quando qualcuno ha selezionato un anno, deve recuperare
        # tutti i tema che hanno giocato quell'anno, e stamparli nel textfield, ed anche riempire il dropdwon sotto

        if self._view._ddAnno.value:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append(
                ft.Text("Selezionare un anno dal menu.")
            )
        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)

        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(
            ft.Text(f"Per il {self._view._ddAnno.value} sono iscritte al campionato {len(teams)} squadre.")

        )

        for t in teams:
            self._view._txt_result.controls.append(ft.Text(t))
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(data = t,
                                   text = t.name,
                                   on_click=self._readDDTeams)
            )
        self._view.update_page()

    def _readDDTeams(self, e):
        if e.control.data is None:
            self._choiceTeam = None
        else:
            self._choiceTeam = e.control.data
        print(f"Selezionato il team {self._choiceTeam}")

