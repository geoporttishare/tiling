<img src="https://github.com/geoportti/Logos/blob/master/geoportti_logo_300px.png">

# tiling

A simple Python package to help dealing with spatial data that is split into
regular tiles.

The package contains a generic tiling class `Block` that alone is not useful. The class
`TM35Block` extends the generic class. It implements one
[tiling](https://www.maanmittauslaitos.fi/sites/maanmittauslaitos.fi/files/old/TM35-lehtijako.pdf) used in many
data sets in the National Land Survey of Finland.

## Installation

Probably the easiest way to install the package is to use virtual environment.
You can create one using for example the following command:
```
python -mvenv ${HOME}/myenv
```
Once the environment is created, we need to activate it:
```
source ${HOME}/myenv/bin/activate
```
Now that we are inside the virtual environment, we can install the package.
First we need to fetch it:
```
git clone git@github.com:geoporttishare/tiling.git tiling.git
cd tiling.git
python setup.py install
```
Now the package is installed in the virtual environment and is available
whenever you activate the environment.

## Usage

There are several ways to use the library. To get all tiles that begin with
'N4411':
```
>>> import tiling.tm35
>>> tiling.tm35.TM35Block.expand('N4411')
['N4411A1', 'N4411A2', 'N4411A3', 'N4411A4', 'N4411B1', 'N4411B2', 'N4411B3', 'N4411B4', 'N4411C1', 'N4411C2', 'N4411C3', 'N4411C4', 'N4411D1', 'N4411D2', 'N4411D3', 'N4411D4', 'N4411E1', 'N4411E2', 'N4411E3', 'N4411E4', 'N4411F1', 'N4411F2', 'N4411F3', 'N4411F4', 'N4411G1', 'N4411G2', 'N4411G3', 'N4411G4', 'N4411H1', 'N4411H2', 'N4411H3', 'N4411H4']
```
To get all the tiles intersecting a given window:
```
>>> tiling.tm35.TM35Block.overlapping_blocks(350000, 6966000, 356000, 6967000)
[P4113F4, P4113H2, P4113H4, P4114E3, P4114G1, P4114G3, P4131B2, P4132A1]
```
To get a neighbor of a specific tile:
```
>>> t = tiling.tm35.TM35Block('N4411A1')
>>> t.left_neighbor()
N4233G3
```
Get spatial information about a specific tile:
```
>>> t = tiling.tm35.TM35Block('N4411A1')
>>> t.bounds()
(404000.0, 6906000.0, 407000.0, 6909000.0)
>>> t.string
'N4411A1'
```

## Usage and Citing
When used, the following citing should be mentioned: "We made use of geospatial
data/instructions/computing resources provided by the Open Geospatial
Information Infrastructure for Research (oGIIR,
urn:nbn:fi:research-infras-2016072513) funded by the Academy of Finland."
