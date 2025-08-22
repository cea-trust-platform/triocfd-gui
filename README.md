# TRIOCFD-GUI

This webui can be used to generate input files for TrioCFD.
To install the webui, follow the instructions below.

## Installation

```bash
source venv/bin/activate  # Activate your virtual environment
pip install git+https://github.com/cea-trust-platform/trustify.git
pip install git+https://github.com/cea-trust-platform/triocfd-api.git
pip install git+https://github.com/cea-trust-platform/triocfd-gui.git
```

## Usage

```bash
source venv/bin/activate  # Activate your virtual environment
triogui
```

Then open your web browser and go to `http://localhost:8866`.


## Development

To contribute to the development of the webui, clone the repository and install
the dependencies in editable mode. This projects uses `uv` in place of `pip` to
manage dependencies.

Please install pre-commit hooks by running:

```bash
pre-commit install
```
