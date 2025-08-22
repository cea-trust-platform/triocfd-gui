from triogui.ui.widgets.main_app import MainApp


def main():
    main_app = MainApp()
    return main_app.get_app()


def voila():
    import pathlib
    import subprocess

    main_path = pathlib.Path(__file__).parent / ".." / "main.ipynb"
    subprocess.run(["voila", str(main_path.resolve())])
