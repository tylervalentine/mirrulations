# Capstone2021

A client/server application to ownload [`Regulations.gov`](https://www.regulations.gov/).

## Setup

* Create and activate a virtual environment

  ```
  python3 -m venv .venv
  source .venv/bin/activate
  ```

* Install source code as a module

  The project is organized into multiple modules, which must each be installed as "editable"
  (using the `-e` switch on `pip`):

  ```
  pip install -e mirrulations-client
  pip install -e mirrulations-core
  pip install -e mirrulations-dashboard
  pip install -e mirrulations-mocks
  pip install -e mirrulations-work-generator 
  pip install -e mirrulations-work-server
  ```

## Configuration Files

The client and work generator use environment variables to load key values.
You can either set the relevant values as environment variables or create 
a `.env` file in the relevant module:

* `mirrulations-client`
  
  Place the `.env` file in the `mirrclient` folder:
  
  ```
  WORK_SERVER_HOSTNAME=work_server
  WORK_SERVER_PORT=8080
  API_KEY=YOUR_KEY
  ```

* `mirrulation-work-generator`
  
  Place the `.env` file in the `mirrgen` folder:
  
  ```
  API_KEY=YOUR_KEY
  ```

  To get an api key, visit [here](https://open.gsa.gov/api/regulationsgov/). 
  Check [client docs](https://github.com/cs334s21/capstone2021/blob/main/docs/client.md) 
  for more information.
  
## Run Static Analysis and Tests

Type `make` to run all. 

Type `make static` for only static tests.

Type `make test` for only pytest.  Alternatively, run `pytest` in the root of
the project to run all tests.  You can run `pytest` in any of module folders
(e.g. in `mirrulations-client`) to run tests for just that module.  Note that
there are `pytest.ini` files in each module as well as a global `pytest.ini`.

* Static analysis uses `flake8`, `pycodestyle`, and `pylint`
* `pytest` uses a coverage metric of 95%.
* NOTE: Sometimes if `pytest` is installed globally, the virtual environment will use that instead. Simply exit and reenter the virtual environment to resolve this.
  Alternatively, uninstall `pytest` from the global packages (`pip3 uninstall pytest` in new termainal).

## Architecture
The image below shows the overview of the architecture for our system. Right now, the portions in blue are implemented at a basic level. Those in red are the remaining parts we need to connect. Regardless, the image shows the relationship between the working plumbing but also includes the plan over the next few weeks.
![Architecture](Architecture.png)

## Contributors
* Ben Coleman (colemanb@moravian.edu)
* Abdullah Alramyan (abdullaha@moravian.edu)
* Valeria Aguilar (aguilarv@moravian.edu)
* Jack Fineanganofo (fineanganofoj@moravian.edu)
* Richard Glennon (glennonr@moravian.edu)
* Eric Gorski (gorskie@moravian.edu)
* Shane Houghton (houghtons@moravian.edu)
* Benjamin Jones (jonesb04@moravian.edu)
* Matthew Kosack (koasckm@moravian.edu)
* Cory Little (littlec@moravian.edu)
* Michael Marchese (marchesem@moravian.edu)
* Kimberly Miller (millerk10@moravian.edu)
* Mark Morykan (morykanm@moravian.edu)
* Robert Rabinovich (rabinovichr@moravian.edu)
* Maxwell Schuman (schumanm@moravian.edu)
* Elizabeth Vincente (vincentee@moravian.edu)
* Kimberly Wolf (wolfk@moravian.edu)
* Isaac Wood (woodi@moravian.edu)

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
* Trae Freeman (freemant02@moravian.edu)
* William Brandes (brandesw@moravian.edu)
