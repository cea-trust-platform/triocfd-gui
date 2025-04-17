import marimo

__generated_with = "0.12.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import os

    return mo, os


@app.cell
def _():
    import trioapi as ta

    return (ta,)


@app.cell
def _(mo):
    mo.md("Choose your dataset").center()
    return


@app.cell
def _(mo, os):
    jdds = [f[:-5] for f in os.listdir() if f.endswith(".data")]

    jdd_selectionne = mo.ui.dropdown(jdds)

    jdd_selectionne.center()
    return jdd_selectionne, jdds


@app.cell
def _(jdd_selectionne, ta):
    ds = ta.get_jdd(jdd_selectionne.value)
    return (ds,)


@app.cell
def _(mo):
    mutation_signal, set_mutation_signal = mo.state(False)
    return mutation_signal, set_mutation_signal


@app.cell
def _(mo):
    mo.md("Current scheme discretization").center()
    return


@app.cell
def _(ds, mutation_signal):
    mutation_signal

    current_scheme = str(type(ds.get("sch"))).removeprefix(
        "<class 'trioapi.trustify_gen_pyd."
    )[:-2]
    current_scheme
    return (current_scheme,)


@app.cell
def _(mo):
    mo.md("Change your discretization : ").center()
    return


@app.cell
def _(mo, ta):
    list_of_scheme = ta.get_subclass("Schema_temps_base")
    for i in range(len(list_of_scheme)):
        list_of_scheme[i] = str(list_of_scheme[i]).removeprefix(
            "<class 'trioapi.trustify_gen_pyd."
        )[:-2]
    new_scheme = mo.ui.dropdown(list_of_scheme)

    return i, list_of_scheme, new_scheme


@app.cell
def _(mutation_signal, new_scheme):
    mutation_signal

    new_scheme
    return


@app.cell
def _(change_scheme, mo):
    mo.ui.button(label="Update with new scheme", on_click=lambda _: change_scheme())
    return


@app.cell
def _(ds, new_scheme, set_mutation_signal, ta):
    def change_scheme():
        ta.change_scheme(ds, new_scheme.value)
        set_mutation_signal(True)

    return (change_scheme,)


@app.cell
def _(ds, mutation_signal):
    mutation_signal

    ds._declarations
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
