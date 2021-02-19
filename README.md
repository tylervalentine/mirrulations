# Capstone2021

A complete senior capstone project. The project requires use of a Python virtual environment, installation of necessary Python libraries using a requirements file, and installation of the project as an editable module. Additionally, we make use of make in order to run tests.


## Setup

* Create/Activate a virtual environment

  ```
  python3 -m venv .venv
  source .venv/bin/activate
  ```

* Install libraries

  ```
  pip install -r requirements.txt
  ```

* Install source code as a module

  ```
  pip install -e .
  ```


## Run Static Analysis and Tests

Type `make` to run:
Type `make static` for only static tests
Type `make test` for only pytest

* Static analysis using `flake8`, `pycodestyle`, and `pylint`
* Run `pytest` with coverage.  The coverage metric is set to 95%
* Sometimes if `pytest` is installed globally, the virtual environment will use that instead. Simply exit and reenter the virtual environment to resolve this.

## Contributors
* Abdullah Alharbi (alharbia02@moravian.edu)
* Alex Meci (mecia@moravian.edu)
* Ben Coleman (colemanb@moravian.edu)
* Colby Hillman (hillmanc@moravian.edu)
* Emily Heiser (heisere@moravian.edu)
* Francis Severino-Guzman (severinoguzmanf@moravian.edu)
* Jarod Frekot (frekotj@moravian.edu)
* John Lapatchak (lapatchakjrj@moravian.edu)
* Jonah Beers (beersj02@moravian.edu)
* Jorge Aguilar (aguilarj@moravian.edu)
* Juan Giraldo (giraldoj@moravian.edu)
* Kylie Norwood (norwoodk@moravian.edu)
* Larisa Fava (faval@moravian.edu)
* Riley Kirkpatrick (kirkpatrickr@moravian.edu)
* Ryan Ballek (ballekr@moravian.edu)
* Trae Freeman (freemant02@moravian.edu)
* William Brandes (brandesw@moravian.edu)
