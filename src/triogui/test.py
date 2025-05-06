import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")

with app.setup:
    import trioapi as ta
    from widget_dict2 import widgets_obj


@app.cell
def _():
    widgets_obj(ta.get_jdd("upwind_simplified").get("pb"))

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
