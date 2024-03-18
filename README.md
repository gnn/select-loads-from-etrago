# Access eTraGo data and get loads attached to buses in the given geometry

The two files contained in this repository comprise a code that allows
accessing an eTraGo compatible database and limit the loads contained in
this database to the ones attached to buses contained in the geometry
given in the accompanying GeoJSON file.


# Requirements

The following Python packages need to be installed in order to work with
the script:

```
eTraGo
shapely >= 2.0.0
```

You also need an eTraGo compatible database that the script can access.
In order to facilitate access, create a file with the path
`HOME/.etrago_database/config.ini`, where `HOME` is your home directory.
Put the credentials needed to access the databas into the file in the
following format:

```ini
[egon-data-local]
username =
host =
port =
database =
password =
```

# Using the script

Open a Python console in the directory in which the scripts reside and
execute:

```python
import loads

data = loads.data()
```

After this, `data` will contain an object with the attributes `bremen`,
`etrago`, `buses` and `loads` where `bremen` contains the geometry read
from the GeoJSON file, `etrago` contains the `Etrago` object constructed
from the data read from the database, `buses` is and object with two
attributes, each containing a different set of buses and `loads`
contains a `DataFrame` with those loads, which are attached to buses
contained inside the geometry.
