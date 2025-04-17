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
    mo.md("Current probes list").center()
    return


@app.cell
def _(ds):
    pb = ds.get("pb")
    return (pb,)


@app.cell
def _(mo):
    mutation_signal_probe, set_mutation_signal_probe = mo.state(False)
    return mutation_signal_probe, set_mutation_signal_probe


@app.cell
def _(mutation_signal_probe, pb):
    mutation_signal_probe

    current_probes = pb.postraitement.sondes
    current_probes
    return (current_probes,)


@app.cell
def _(mo):
    mo.md("Add a new probe").center()
    return


@app.cell
def _(mo, mutation_signal_probe):
    mutation_signal_probe

    probe_name = mo.ui.text(label="Name of the probe")
    field_name = mo.ui.text(label="Name of the sample field")
    period = mo.ui.text(label="Period")
    return field_name, period, probe_name


@app.cell
def _(field_name, mo, period, probe_name):
    points_type = mo.ui.dropdown(
        label="Type of points for the probe", options=["Points", "Segment"]
    )
    mo.vstack([probe_name, field_name, period])

    return (points_type,)


@app.cell
def _(points_type):
    points_type
    return


@app.cell
def _(mo):
    get_points, set_points = mo.state([])
    mutation_signal, set_mutation_signal = mo.state(False)
    return get_points, mutation_signal, set_mutation_signal, set_points


@app.cell
def _(mo, mutation_signal):
    mutation_signal

    x_coordinate = mo.ui.text(label="X coordinate")
    y_coordinate = mo.ui.text(label="Y coordinate")
    starting_x_coordinate = mo.ui.text(label="Starting X coordinate")
    starting_y_coordinate = mo.ui.text(label="Starting Y coordinate")
    ending_x_coordinate = mo.ui.text(label="Ending X coordinate")
    ending_y_coordinate = mo.ui.text(label="Ending Y coordinate")
    return (
        ending_x_coordinate,
        ending_y_coordinate,
        starting_x_coordinate,
        starting_y_coordinate,
        x_coordinate,
        y_coordinate,
    )


@app.cell
def _(
    ending_x_coordinate,
    ending_y_coordinate,
    mo,
    points_type,
    set_point,
    set_points,
    starting_x_coordinate,
    starting_y_coordinate,
    x_coordinate,
    y_coordinate,
):
    vstack = mo.vstack(["Choose the type of points"])
    if points_type.value == "Points":
        add_point_button = mo.ui.button(
            label=("Add this point to the list"),
            on_click=lambda _: set_point(
                [float(x_coordinate.value), float(y_coordinate.value)]
            ),
        )
        remove_point_button = mo.ui.button(
            label=("Remove the last point from the list"),
            on_click=lambda _: set_points(lambda v: v[:-1]),
        )
        hstack1 = mo.hstack([x_coordinate, y_coordinate])
        hstack2 = mo.hstack([add_point_button, remove_point_button])
        vstack = mo.vstack([hstack1, hstack2])

    if points_type.value == "Segment":
        number_of_points = mo.ui.number(label="Number of points")
        segment_hstack1 = mo.hstack([starting_x_coordinate, starting_y_coordinate])
        segment_hstack2 = mo.hstack([ending_x_coordinate, ending_y_coordinate])
        vstack = mo.vstack([number_of_points, segment_hstack1, segment_hstack2])

    vstack
    return (
        add_point_button,
        hstack1,
        hstack2,
        number_of_points,
        remove_point_button,
        segment_hstack1,
        segment_hstack2,
        vstack,
    )


@app.cell
def _(get_points, mo, points_type):
    mo.as_html(get_points()) if points_type.value == "Points" else mo.md("")
    return


@app.cell
def _(set_mutation_signal, set_points, x_coordinate, y_coordinate):
    def set_point(coos):
        if x_coordinate.value and y_coordinate.value:
            set_points(lambda v: v + [coos])
        set_mutation_signal(True)

    return (set_point,)


@app.cell
def _(add_probe, mo):
    mo.ui.button(label="Add this probe", on_click=lambda _: add_probe())
    return


@app.cell
def _(
    ending_x_coordinate,
    ending_y_coordinate,
    field_name,
    get_points,
    number_of_points,
    pb,
    period,
    points_type,
    probe_name,
    set_mutation_signal,
    set_mutation_signal_probe,
    starting_x_coordinate,
    starting_y_coordinate,
    ta,
):
    def add_probe():
        if points_type.value == "Segment":
            segment = ta.create_probe_segment(
                number_of_points.value,
                [
                    float(starting_x_coordinate.value),
                    float(starting_y_coordinate.value),
                ],
                [float(ending_x_coordinate.value), float(ending_y_coordinate.value)],
            )
            probe = ta.create_probe(
                probe_name.value, None, field_name.value, float(period.value), segment
            )
        else:
            points = ta.create_probe_points(get_points())
            probe = ta.create_probe(
                probe_name.value, None, field_name.value, float(period.value), points
            )
        ta.add_probe(pb, probe)
        set_mutation_signal_probe(True)
        set_mutation_signal(True)

    return (add_probe,)


@app.cell
def _(mutation_signal_probe, pb):
    mutation_signal_probe

    pb.postraitement.sondes
    return


@app.cell
def _(mo):
    mo.md("Delete a probe").center()
    return


@app.cell
def _(mo, mutation_signal_probe, pb):
    mutation_signal_probe

    probe_to_delete = mo.ui.dropdown(
        {p.nom_sonde: i for i, p in enumerate(pb.postraitement.sondes)}
    )
    probe_to_delete
    return (probe_to_delete,)


@app.cell
def _(del_probe, mo):
    mo.ui.button(label="Delete this probe", on_click=lambda _: del_probe())
    return


@app.cell
def _(current_probes, probe_to_delete, set_mutation_signal_probe):
    def del_probe():
        (current_probes.pop(probe_to_delete.value),)
        set_mutation_signal_probe(True)

    return (del_probe,)


@app.cell
def _(mo):
    mo.md("Modify a probe").center()
    return


@app.cell
def _(mo, mutation_signal_probe, pb):
    mutation_signal_probe

    probe_to_change = mo.ui.dropdown(
        {p.nom_sonde: i for i, p in enumerate(pb.postraitement.sondes)}
    )
    probe_to_change
    return (probe_to_change,)


@app.cell
def _(mo):
    mo.md("""Field to modify""")
    return


@app.cell
def _(mo):
    field_to_change = mo.ui.dropdown(["Field name", "Period", "Points"])
    field_to_change
    return (field_to_change,)


@app.cell
def _(mo):
    field_name_change = mo.ui.text(label="New field name")
    period_change = mo.ui.text(label="New period")
    points_change = mo.ui.text()
    return field_name_change, period_change, points_change


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _(pb, probe_to_change):
    pb.postraitement.sondes[probe_to_change.value]

    return


@app.cell
def _(pb, probe_to_change):
    pb.postraitement.sondes[probe_to_change.value].prd
    return


@app.cell
def _(pb, probe_to_change):
    pb.postraitement.sondes[probe_to_change.value].nom_inco
    return


@app.cell
def _(pb, probe_to_change):
    pb.postraitement.sondes[probe_to_change.value].type
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
