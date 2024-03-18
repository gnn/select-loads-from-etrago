from types import SimpleNamespace as SN

from etrago import Etrago
import shapely

import args


def read(path="bremen.geojson"):
    """Read the GeoJSON file at `path` into a shapely geometry.

    Note
    ----
    The file "bremen.geojson", which should accompany this script, was
    created on https://overpass-turbo.eu/ using the query

    ```
    rel(62559);
    out geom;
    ```

    and exporting the result to GeoJSON.
    """
    with open("bremen.geojson", "r", encoding="utf-8") as f:
        return shapely.from_geojson("".join(f.readlines()))


def data():
    bremen = read()
    etrago = Etrago(args.args, json_path=None)
    etrago.build_network_from_db()
    loads = etrago.network.loads.reset_index(names="Load").set_index("bus")

    buses = SN()
    buses.in_bremen = etrago.network.buses[
        etrago.network.buses.loc[:, "geom"].apply(bremen.contains)
    ]
    # Apparently, of the 223 `buses` contained in Bremen, only 108 have
    # an associated load, so we need to calculate the intersection of
    # both indexes to avoid key errors.
    buses.with_loads = buses.in_bremen.loc[
        buses.in_bremen.index.intersection(loads.index), :
    ]

    # Now we can select the load ids attached to buses in Bremen and
    # then pull the corresponding load timeseries out of `loads_t`
    loads = loads.loc[buses.with_loads.index, "Load"]
    loads = etrago.network.loads_t["p_set"].loc[:, loads]

    return SN(bremen=bremen, etrago=etrago, buses=buses, loads=loads)


def main():
    help = (
        "\nThis script reads in a geometry from the accompanying"
        '\n"bremen.geojson" file, downloads data from an eTraGo'
        "\ncompatible database, calculates which buses are contained"
        "\nin the given geometry, selects the loads which are attached"
        "\nto these buses and prints these loads.\n"
        "\nTo do something useful with the data, you probably want to"
        "\n`import` the script, then do `data = loads.data()` and do"
        "\nstuff with the object. The loads contained in the geometry"
        "\nare then located in `data.loads`."
        "\nSee the accompanying README.md for a bit more detail.\n"
        "\nNow accessing the data and calculating the loads.\n"
    )
    print(help)
    loads = data().loads
    print()
    print(loads)


if __name__ == "__main__":
    main()
