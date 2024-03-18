args = {
    # Setup:
    "db": "egon-data-local",  # database session
    "scn_name": "eGon2035",  # scenario: eGon2035, eGon100RE, eGon2035_lowflex, eGon100RE_lowflex
    "start_snapshot": 1,
    "end_snapshot": 15,
    "gridversion": None,  # Currently not needed
    "branch_capacity_factor": {"HV": 0.5, "eHV": 0.7},  # p.u. branch rating
    "foreign_lines": {
        "carrier": "DC",  # 'DC' for modeling foreign lines as links
        "capacity": "osmTGmod",  # 'osmTGmod', 'tyndp2020', 'ntc_acer' or 'thermal_acer'
    },
    "scn_extension": None,  # None or array of extension scenarios (currently not provided, but needed once new lines from NEP are set up)
    "scn_decommissioning": None,  # None or decommissioning scenario (currently not provided)
    
    # Optimisation and powerflow:
    "method": {  # Choose method and settings for optimization
        "type": "lopf",  # type of optimization, currently only 'lopf'
        "n_iter": 1,  # abort criterion of iterative optimization, 'n_iter' or 'threshold'
        "pyomo": True,  # set if pyomo is used for model building
    },
    "solver": "glpk",  # glpk, cplex or gurobi
    "solver_options": {},
    "model_formulation": "kirchhoff",  # formulation of the LPF problem (all are equivalent)
    "extendable": {
        "extendable_components": [
            "as_in_db"
        ],  # Array of components to optimize
        "upper_bounds_grid": {  # Set upper bounds for grid expansion
            # lines in Germany
            "grid_max_D": None,  # relative to existing capacity
            "grid_max_abs_D": {  # absolute capacity per voltage level
                "380": {"i": 1020, "wires": 4, "circuits": 4},
                "220": {"i": 1020, "wires": 4, "circuits": 4},
                "110": {"i": 1020, "wires": 4, "circuits": 2},
                "dc": 0,
            },
            # border crossing lines
            "grid_max_foreign": 4,  # relative to existing capacity
            "grid_max_abs_foreign": None,  # absolute capacity per voltage level
        },
    },
    "generator_noise": 789456,  # a small random noise to the marginal costs of each generator in order to prevent an optima plateau
    "extra_functionality": {},  # Choose function name (e.g. "min_renewable_share" or "cross_border_flow") or {}    
    "load_shedding": False,  # helpful when debugging - a very expensive generator is added to each bus 
    "lpfile": False,  # save pyomo's lp file: False or /path/to/lpfile.lp
    "csv_export": "results",  # save results as csv: False or /path/tofolder
    "pf_post_lopf": {
        "active": True,  # choose if a pf should be performed after the lopf
        "add_foreign_lopf": True,  # keep results of lopf for foreign DC-links
        "q_allocation": "p_nom",  # allocate reactive power via 'p_nom' or 'p'
    },
    
    # Spatial complexity reduction and disaggregation:
    "network_clustering_ehv": False,  # clustering of HV buses to EHV buses
    "network_clustering": {
        "active": True,  # choose if clustering is activated
        "method": "kmedoids-dijkstra",  # choose clustering method: kmeans or kmedoids-dijkstra
        "n_clusters_AC": 60,  # total number of resulting AC nodes (DE+foreign)
        "cluster_foreign_AC": False,  # take foreign AC buses into account, True or False
        "method_gas": "kmedoids-dijkstra",  # choose clustering method: kmeans or kmedoids-dijkstra
        "n_clusters_gas": 17,  # total number of resulting CH4 nodes (DE+foreign)
        "cluster_foreign_gas": False,  # take foreign CH4 buses into account, True or False
        "k_elec_busmap": False,  # False or path/to/busmap.csv
        "k_gas_busmap": False,  # False or path/to/ch4_busmap.csv
        "bus_weight_tocsv": None,  # None or path/to/bus_weight.csv
        "bus_weight_fromcsv": None,  # None or path/to/bus_weight.csv
        "gas_weight_tocsv": None,  # None or path/to/gas_bus_weight.csv
        "gas_weight_fromcsv": None,  # None or path/to/gas_bus_weight.csv
        "line_length_factor": 1,  # Factor to multiply distance between new buses for new line lengths
        "remove_stubs": False,  # remove stubs bevore kmeans clustering
        "use_reduced_coordinates": False,  # If True, do not average cluster coordinates
        "random_state": 42,  # random state for replicability of clustering results
        "n_init": 10,  # affects clustering algorithm, only change when neccesary
        "max_iter": 100,  # affects clustering algorithm, only change when neccesary
        "tol": 1e-6,  # affects clustering algorithm, only change when neccesary
        "CPU_cores": 8,  # number of cores used during clustering, "max" for all cores available.
    },
    "sector_coupled_clustering": {
        "active": True,  # choose if clustering is activated
        "carrier_data": {  # select carriers affected by sector coupling
            "central_heat": {
                "base": ["CH4", "AC"],
                "strategy": "simultaneous",  # select strategy to cluster other sectors
            },
        },
    },
    "disaggregation": None,  # None or 'uniform'
    
    # Temporal complexity reduction and disaggregation:
    "snapshot_clustering": {
        "active": False,  # choose if clustering is activated
        "method": "segmentation",  # 'typical_periods' or 'segmentation'
        "extreme_periods": None,  # consideration of extreme timesteps; e.g. 'append'
        "how": "daily",  # type of period - only relevant for 'typical_periods'
        "storage_constraints": "soc_constraints",  # additional constraints for storages  - only relevant for 'typical_periods'
        "n_clusters": 5,  #  number of periods - only relevant for 'typical_periods'
        "n_segments": 5,  # number of segments - only relevant for segmentation
    },
    "skip_snapshots": 5,  # False or number of snapshots to skip
    "temporal_disaggregation": {
        "active": False,  # choose if temporally full complex dispatch optimization should be conducted
        "no_slices": 8,  # number of subproblems optimization is divided into
    },

    # Other
    "comments": None,
}
