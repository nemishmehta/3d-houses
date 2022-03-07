# Plot 3D Houses in Belgium

As the name suggests, properties based in Belgium (specifically Flanders and Brussels) can be rendered in 3D using this repository. 3D modelling of properties was made possible as a result of open source LiDAR data provided by the Flemish government and information on cadastral plans provided by MinFin.

## Installation

The project has been coded in Python 3.8.10 and can be run on the terminal. Given below are a set of instructions to access the project:

1. Install [Python](https://realpython.com/installing-python/) (if not installed already).
2. Install [geopandas](https://geopandas.org/en/stable/getting_started/install.html), [pandas](https://pandas.pydata.org/docs/getting_started/install.html), [plotly](https://plotly.com/python/getting-started/#installation), [rasterio](https://rasterio.readthedocs.io/en/latest/installation.html) and [requests](https://pypi.org/project/requests/) libraries.
3. Clone the repository to your local machine.
4. Open the terminal on your local machine and navigate to the directory in which the repo has been cloned.
5. Download and extract LiDAR data available under these links - [DSM](https://www.geopunt.be/download?container=dhm-vlaanderen-ii-dsm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DSM,%20raster,%201m) and [DTM](https://www.geopunt.be/download?container=dhm-vlaanderen-ii-dtm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DTM,%20raster,%201m). Alternatively, run the files titled `download_extract_zip_files_dsm.py` and `download_extract_zip_files_dtm.py` to complete this step.
6. Download [Belgium's Cadastral Parcels dataset](https://www.geo.be/catalog/details/tt098dcb-f5c7-49b8-8e0b-7c3811630d85?l=en) and extract it to a folder titled 'Belgium' in the 'data' directory.
7. **Note**: Please ensure there is sufficient disk space available (~90 GB) for files downloaded in steps 5. and 6.

## Usage

1. Type - `python main.py` to run the project.
2. If it doesn't run then try `python3 main.py`.
3. Input an address of your choice. **Note**: Ensure that the address is provided in Flemish.
4. If the address is available in the database, then a 3D render of the property will open in a browser.
5. In addition to the 3D render of the property, its plot surface will also be displayed.

