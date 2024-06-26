[![Codacy Badge](https://app.codacy.com/project/badge/Grade/6f230b60870d4048860528a551654f8e)](https://www.codacy.com/gh/danieldeer/amaz3dsim/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=danieldeer/amaz3dsim&amp;utm_campaign=Badge_Grade)
# AMAZ3DSim

AMAZ3DSim is a lightweight python-based 3D network multi-agent simulator. It uses a cell-based congestion model. It calculates risk, battery capacities, travel time and travelled distance of the agents and the loudness the network links experience. AMAZ3DSim is suitable for 3D network optimization tasks.
![AMAZ3DSim simulation of OSM Darmstadt scenario](https://github.com/danieldeer/gifs/blob/master/amaz3dsim-daniel-hirsch.gif)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following dependencies.

```bash
sudo apt install python3.8

pip install click
pip install tkinter
pip install matplotlib
pip install networkx
```

## Usage

To start AMAZ3DSim with default settings
```bash
python3.8 CommandLineInterface.py
```
To open a small help doc listing the parameters of the CommandLineInterface.py
```bash
python3.8 CommandLineInterface.py --help
```
A full command specifies all of the following paramters
```bash
python3.8 CommandLineInterface.py --in-file /path/to/scenario.xml --out-file /path/to/output.xml --config-file /path/to/config.xml --random-mode False
```
If an argument is left out, a standard value is used. 

## Configuration
A fully commented example configuration is available under
```bash
config/config.xml
```
which is also the standard configuration.

## Input interface of the simulator
To simulate your own network, create your own scenario.xml file. A scenario.xml contains the network, the agents and the delivery orders to be fulfilled.

Example scenario.xml files are available in the input folder.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
