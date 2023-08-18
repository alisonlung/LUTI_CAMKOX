"""
maps.py

Generate visualisation for population, accessibilities and flows 
"""
from LUTI_CAMKOX.globals import *
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import contextily as cx
from matplotlib_scalebar.scalebar import ScaleBar
import networkx as nx
import os
import osmnx as ox

def population_map_creation(inputs, outputs):
    #2050 - Expansion
    df_pop21 = pd.read_csv(outputs["JobsDjOi2021"], usecols=['msoa', 'OiPred_Tot_21'], index_col='msoa')
    df_pop50 = pd.read_csv(outputs["JobsDjOi2050"], usecols=['msoa', 'OiPred_Tot_50'], index_col='msoa')
    df_pop_merged = pd.merge(df_pop21, df_pop50, on='msoa')

    df_pop_merged['PopCh21_50'] = ((df_pop50['OiPred_Tot_50'] - df_pop21['OiPred_Tot_21']) / df_pop21['OiPred_Tot_21']) * 100.0

    df_pop_merged.to_csv(Pop_Change)
    pop_ch = pd.read_csv(Pop_Change)

    map_df = gpd.read_file(inputs["MsoaShapefile"])
    CAMKOX_map_popch_df = map_df.merge(pop_ch, left_on='MSOA11CD', right_on='msoa')

    # Plotting the Population change between 2021 - 2050
    fig3, ax3 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_map_popch_df.plot(column='PopCh21_50', cmap='Reds', ax=ax3, edgecolor='darkgrey', linewidth=0.1)
    ax3.axis('off')
    ax3.set_title('Population Change 2021 - 2050 in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='Reds', norm=None)
    sm._A = []
    cbar = fig3.colorbar(sm)
    cx.add_basemap(ax3, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapPopChange20212050"], dpi = 600)
    # plt.show()

    #Housing Accessibility Change
    df_HA_2021 = pd.read_csv(outputs["HousingAccessibility2021"], usecols=['areakey', 'HAcar21', 'HAbus21', 'HArail21'])
    df_HA_2050 = pd.read_csv(outputs["HousingAccessibility2050"], usecols=['areakey', 'HAcar50', 'HAbus50', 'HArail50'])

    #Merging the DataFrames
    df_HA_merged = pd.merge(df_HA_2021, df_HA_2050, on='areakey')

    df_HA_merged['HAC2150car'] = ((df_HA_2050['HAcar50'] - df_HA_2021['HAcar21']) / df_HA_2021['HAcar21']) * 100.0
    df_HA_merged['HAC2150bus'] = ((df_HA_2050['HAbus50'] - df_HA_2021['HAbus21']) / df_HA_2021['HAbus21']) * 100.0
    df_HA_merged['HAC2150rail'] = ((df_HA_2050['HArail50'] - df_HA_2021['HArail21']) / df_HA_2021['HArail21']) * 100.0

    df_HA_merged.to_csv(HA_Change)

    # Plotting the Housing Accessibility change
    HousingAcc_change = pd.read_csv(HA_Change)
    CAMKOX_map_HAch_df = map_df.merge(HousingAcc_change, left_on='MSOA11CD', right_on='areakey')

    # Producing Maps for Housing Accessibility Change 2021 - 2050 using car/bus/rail in the CAMKOX and London

    fig7, ax7 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_map_HAch_df.plot(column='HAC2150car', cmap='OrRd', ax=ax7, edgecolor='darkgrey', linewidth=0.1)
    ax7.axis('off')
    ax7.set_title('Housing Accessibility Change 2021 - 2050 using car in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=None)
    sm._A = []
    cbar = fig7.colorbar(sm)
    cx.add_basemap(ax7, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapHousingAccChange20212050Roads"], dpi=600)
    # plt.show()

    fig8, ax8 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_map_HAch_df.plot(column='HAC2150bus', cmap='OrRd', ax=ax8, edgecolor='darkgrey', linewidth=0.1)
    ax8.axis('off')
    ax8.set_title('Housing Accessibility Change 2021 - 2050 using bus in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=None)
    sm._A = []
    cbar = fig8.colorbar(sm)
    cx.add_basemap(ax8, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapHousingAccChange20212050Bus"], dpi=600)
    # plt.show()

    fig9, ax9 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_map_HAch_df.plot(column='HAC2150rail', cmap='OrRd', ax=ax9, edgecolor='darkgrey', linewidth=0.1)
    ax9.axis('off')
    ax9.set_title('Housing Accessibility Change 2021 - 2050 using rail in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=None)
    sm._A = []
    cbar = fig9.colorbar(sm)
    cx.add_basemap(ax9, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapHousingAccChange20212050Rail"], dpi=600)
    # plt.show()


    #Jobs Accessibility Change
    df_JobAcc_2021 = pd.read_csv(outputs["JobsAccessibility2021"], usecols=['areakey', 'JAcar21', 'JAbus21', 'JArail21'])
    df_JobAcc_2050 = pd.read_csv(outputs["JobsAccessibility2050"], usecols=['areakey', 'JAcar50', 'JAbus50', 'JArail50'])

    # Merging the DataFrames
    df_JobAcc_merged = pd.merge(df_JobAcc_2021, df_JobAcc_2050, on='areakey')

    df_JobAcc_merged['JAC2150car'] = ((df_JobAcc_2050['JAcar50'] - df_JobAcc_2021['JAcar21']) / df_JobAcc_2021['JAcar21']) * 100.0
    df_JobAcc_merged['JAC2150bus'] = ((df_JobAcc_2050['JAbus50'] - df_JobAcc_2021['JAbus21']) / df_JobAcc_2021['JAbus21']) * 100.0
    df_JobAcc_merged['JAC2150rail'] = ((df_JobAcc_2050['JArail50'] - df_JobAcc_2021['JArail21']) / df_JobAcc_2021['JArail21']) * 100.0

    df_JobAcc_merged.to_csv(Job_Change)

    # Plotting the Jobs Accessibility change
    JobAcc_change = pd.read_csv(Job_Change)
    CAMKOX_map_JAch_df = map_df.merge(JobAcc_change, left_on='MSOA11CD', right_on='areakey')

    # Producing Maps for Jobs Accessibility Change 2021 - 2050 using car/bus/rail in the CAMKOX and London

    fig13, ax13 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_map_JAch_df.plot(column='JAC2150car', cmap='Greens', ax=ax13, edgecolor='darkgrey', linewidth=0.1)
    ax13.axis('off')
    ax13.set_title('Jobs Accessibility Change 2021 - 2050 using car in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='Greens', norm=None)
    sm._A = []
    cbar = fig13.colorbar(sm)
    cx.add_basemap(ax13, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapJobsAccChange20212050Roads"], dpi=600)
    # plt.show()

    fig14, ax14 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_map_JAch_df.plot(column='JAC2150bus', cmap='Greens', ax=ax14, edgecolor='darkgrey', linewidth=0.1)
    ax14.axis('off')
    ax14.set_title('Jobs Accessibility Change 2021 - 2050 using bus in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='Greens', norm=None)
    sm._A = []
    cbar = fig14.colorbar(sm)
    cx.add_basemap(ax14, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapJobsAccChange20212050Bus"], dpi=600)
    # plt.show()

    fig15, ax15 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_map_JAch_df.plot(column='JAC2150rail', cmap='Greens', ax=ax15, edgecolor='darkgrey', linewidth=0.1)
    ax15.axis('off')
    ax15.set_title('Jobs Accessibility Change 2021 - 2050 using rail in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='Greens', norm=None)
    sm._A = []
    cbar = fig15.colorbar(sm)
    cx.add_basemap(ax15, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapJobsAccChange20212050Rail"], dpi=600)
    # plt.show()


    #Create a common shapefile (polygon) that contains:
    # 1. Population change (2021-2050)
    # 2. Housing Accessibility change for car, bus and rail (2021-2050)
    # 3. Jobs Accessibility change for car, bus and rail (2021-2050)
    tot_shp_df = CAMKOX_map_popch_df.merge(pd.merge(HousingAcc_change, JobAcc_change, on='areakey'), left_on='MSOA11CD', right_on='areakey')
    #Drop unsuseful columns
    #tot_shp_df.drop(columns=['objectid','msoa11nm', 'msoa11nmw', 'st_areasha', 'st_lengths', 'msoa', 'areakey'], inplace = True, axis = 1)
    #Save the shapefile
    tot_shp_df.to_file(outputs["MapResultsShapefile"])




    #2050-New Settlement
    df_pop21 = pd.read_csv(outputs["JobsDjOi2021"], usecols=['msoa', 'OiPred_Tot_21'], index_col='msoa')
    df_ns_pop50 = pd.read_csv(outputs["NS_JobsDjOi2050"], usecols=['msoa', 'OiPred_Tot_50'], index_col='msoa')
    df_ns_pop_merged = pd.merge(df_pop21, df_ns_pop50, on='msoa')

    df_ns_pop_merged['PopCh_ns_21_50'] = ((df_ns_pop50['OiPred_Tot_50'] - df_pop21['OiPred_Tot_21']) / df_pop21['OiPred_Tot_21']) * 100.0

    df_ns_pop_merged.to_csv(NS_Pop_Change)
    ns_pop_ch = pd.read_csv(NS_Pop_Change)

    map_df = gpd.read_file(inputs["MsoaShapefile"])
    CAMKOX_map_ns_popch_df = map_df.merge(ns_pop_ch, left_on='MSOA11CD', right_on='msoa')

    # Plotting the Population change between 2021 - 2050
    fig3, ax3 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_map_ns_popch_df.plot(column='PopCh_ns_21_50', cmap='Reds', ax=ax3, edgecolor='darkgrey', linewidth=0.1)
    ax3.axis('off')
    ax3.set_title('Population Change 2021 - 2050 in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='Reds', norm=None)
    sm._A = []
    cbar = fig3.colorbar(sm)
    cx.add_basemap(ax3, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapPopChange2021NS2050"], dpi = 600)
    # plt.show()

    #Housing Accessibility Change
    df_HA_2021 = pd.read_csv(outputs["HousingAccessibility2021"], usecols=['areakey', 'HAcar21', 'HAbus21', 'HArail21'])
    df_ns_HA_2050 = pd.read_csv(outputs["NS_HousingAccessibility2050"], usecols=['areakey', 'HAcar50', 'HAbus50', 'HArail50'])

    #Merging the DataFrames
    df_ns_HA_merged = pd.merge(df_HA_2021, df_ns_HA_2050, on='areakey')

    df_ns_HA_merged['HAC2150car'] = ((df_ns_HA_2050['HAcar50'] - df_HA_2021['HAcar21']) / df_HA_2021['HAcar21']) * 100.0
    df_ns_HA_merged['HAC2150bus'] = ((df_ns_HA_2050['HAbus50'] - df_HA_2021['HAbus21']) / df_HA_2021['HAbus21']) * 100.0
    df_ns_HA_merged['HAC2150rail'] = ((df_ns_HA_2050['HArail50'] - df_HA_2021['HArail21']) / df_HA_2021['HArail21']) * 100.0

    df_ns_HA_merged.to_csv(NS_HA_Change)

    # Plotting the Housing Accessibility change
    ns_HousingAcc_change = pd.read_csv(NS_HA_Change)
    CAMKOX_ns_map_HAch_df = map_df.merge(ns_HousingAcc_change, left_on='MSOA11CD', right_on='areakey')

    # Producing Maps for Housing Accessibility Change 2021 - 2050 using car/bus/rail in the CAMKOX and London

    fig7, ax7 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_ns_map_HAch_df.plot(column='HAC2150car', cmap='OrRd', ax=ax7, edgecolor='darkgrey', linewidth=0.1)
    ax7.axis('off')
    ax7.set_title('Housing Accessibility Change 2021 - 2050 using car in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=None)
    sm._A = []
    cbar = fig7.colorbar(sm)
    cx.add_basemap(ax7, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapHousingAccChange2021NS2050Roads"], dpi=600)
    # plt.show()

    fig8, ax8 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_ns_map_HAch_df.plot(column='HAC2150bus', cmap='OrRd', ax=ax8, edgecolor='darkgrey', linewidth=0.1)
    ax8.axis('off')
    ax8.set_title('Housing Accessibility Change 2021 - 2050 using bus in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=None)
    sm._A = []
    cbar = fig8.colorbar(sm)
    cx.add_basemap(ax8, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapHousingAccChange2021NS2050Bus"], dpi=600)
    # plt.show()

    fig9, ax9 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_ns_map_HAch_df.plot(column='HAC2150rail', cmap='OrRd', ax=ax9, edgecolor='darkgrey', linewidth=0.1)
    ax9.axis('off')
    ax9.set_title('Housing Accessibility Change 2021 - 2050 using rail in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=None)
    sm._A = []
    cbar = fig9.colorbar(sm)
    cx.add_basemap(ax9, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapHousingAccChange2021NS2050Rail"], dpi=600)
    # plt.show()


    #Jobs Accessibility Change
    df_JobAcc_2021 = pd.read_csv(outputs["JobsAccessibility2021"], usecols=['areakey', 'JAcar21', 'JAbus21', 'JArail21'])
    df_ns_JobAcc_2050 = pd.read_csv(outputs["NS_JobsAccessibility2050"], usecols=['areakey', 'JAcar50', 'JAbus50', 'JArail50'])

    # Merging the DataFrames
    df_ns_JobAcc_merged = pd.merge(df_JobAcc_2021, df_ns_JobAcc_2050, on='areakey')

    df_ns_JobAcc_merged['JAC2150car'] = ((df_ns_JobAcc_2050['JAcar50'] - df_JobAcc_2021['JAcar21']) / df_JobAcc_2021['JAcar21']) * 100.0
    df_ns_JobAcc_merged['JAC2150bus'] = ((df_ns_JobAcc_2050['JAbus50'] - df_JobAcc_2021['JAbus21']) / df_JobAcc_2021['JAbus21']) * 100.0
    df_ns_JobAcc_merged['JAC2150rail'] = ((df_ns_JobAcc_2050['JArail50'] - df_JobAcc_2021['JArail21']) / df_JobAcc_2021['JArail21']) * 100.0

    df_ns_JobAcc_merged.to_csv(NS_Job_Change)

    # Plotting the Jobs Accessibility change
    ns_JobAcc_change = pd.read_csv(NS_Job_Change)
    CAMKOX_ns_map_JAch_df = map_df.merge(ns_JobAcc_change, left_on='MSOA11CD', right_on='areakey')

    # Producing Maps for Jobs Accessibility Change 2021 - 2050 using car/bus/rail in the CAMKOX and London

    fig13, ax13 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_ns_map_JAch_df.plot(column='JAC2150car', cmap='Greens', ax=ax13, edgecolor='darkgrey', linewidth=0.1)
    ax13.axis('off')
    ax13.set_title('Jobs Accessibility Change 2021 - 2050 using car in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='Greens', norm=None)
    sm._A = []
    cbar = fig13.colorbar(sm)
    cx.add_basemap(ax13, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapJobsAccChange2021NS2050Roads"], dpi=600)
    # plt.show()

    fig14, ax14 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_ns_map_JAch_df.plot(column='JAC2150bus', cmap='Greens', ax=ax14, edgecolor='darkgrey', linewidth=0.1)
    ax14.axis('off')
    ax14.set_title('Jobs Accessibility Change 2021 - 2050 using bus in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='Greens', norm=None)
    sm._A = []
    cbar = fig14.colorbar(sm)
    cx.add_basemap(ax14, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapJobsAccChange2021NS2050Bus"], dpi=600)
    # plt.show()

    fig15, ax15 = plt.subplots(1, figsize=(20, 10))
    CAMKOX_ns_map_JAch_df.plot(column='JAC2150rail', cmap='Greens', ax=ax15, edgecolor='darkgrey', linewidth=0.1)
    ax15.axis('off')
    ax15.set_title('Jobs Accessibility Change 2021 - 2050 using rail in CAMKOX and London', fontsize=16)
    sm = plt.cm.ScalarMappable(cmap='Greens', norm=None)
    sm._A = []
    cbar = fig15.colorbar(sm)
    cx.add_basemap(ax15, crs=CAMKOX_map_popch_df.crs, source=cx.providers.CartoDB.Positron)
    plt.savefig(outputs["MapJobsAccChange2021NS2050Rail"], dpi=600)
    # plt.show()


    #Create a common shapefile (polygon) that contains:
    # 1. Population change (2021-2050)
    # 2. Housing Accessibility change for car, bus and rail (2021-2050)
    # 3. Jobs Accessibility change for car, bus and rail (2021-2050)
    ns_tot_shp_df =  CAMKOX_map_ns_popch_df.merge(pd.merge(ns_HousingAcc_change, ns_JobAcc_change, on='areakey'), left_on='MSOA11CD', right_on='areakey')
    #Drop unsuseful columns
    #tot_shp_df.drop(columns=['objectid','msoa11nm', 'msoa11nmw', 'st_areasha', 'st_lengths', 'msoa', 'areakey'], inplace = True, axis = 1)
    #Save the shapefile
    ns_tot_shp_df.to_file(outputs["NS_MapResultsShapefile"])

def flows_map_creation(inputs, outputs, flows_output_keys): # Using OSM

    Zone_nodes = nx.read_shp(inputs["MSOACentroidsShapefileWGS84"]) # Must be in epsg:4326 (WGS84)

    Case_Study_Zones = ["Oxfordshire", "Buckinghamshire", "City of Milton Keynes", "Northamptonshire", "Bedfordshire", "Cambridgeshire", "City of Peterborough", "Hertfordshire", "Greater London"]

    X = ox.graph_from_place(Case_Study_Zones, network_type='drive')
    # crs = X.graph["crs"]
    # print('Graph CRS: ', crs)
    # print()

    # ox.plot_graph(X) # test plot

    X = X.to_undirected()

    # Calculate the origins and destinations for the shortest paths algorithms to be run on OSM graph
    OD_list = calc_shortest_paths_ODs_osm(Zone_nodes, X)

    Flows = []

    for kk, flows_output_key in enumerate(flows_output_keys):
        Flows.append(pd.read_csv(outputs[flows_output_key], header=None))

        # Initialise weights to 0:
        for source, target in X.edges():
            X[source][target][0]["Flows_" + str(kk)] = 0

    TOT_count = len(OD_list)
    # print(OD_list)

    for n, i in enumerate(OD_list):
        print("Flows maps creation - iteration ", n+1, " of ", TOT_count)
        sssp_paths = nx.single_source_dijkstra_path(X, i, weight='length') # single source shortest paths from i to all nodes of the network
        for m, j in enumerate(OD_list):
            shortest_path = sssp_paths[j] # shortest path from i to j
            path_edges = zip(shortest_path, shortest_path[1:])  # Create edges from nodes of the shortest path

            for edge in list(path_edges):
                for cc in range(len(Flows)):
                    X[edge[0]][edge[1]][0]["Flows_" + str(cc)] += Flows[cc].iloc[n, m]

    # save graph to shapefile
    output_folder_path = "./Outputs-CAMKOX_LON/" + "Flows_shp"
    ox.save_graph_shapefile(X, filepath=output_folder_path)

def rail_flows_map_creation(inputs, outputs, flows_output_keys): # Using OSM

    Zone_nodes = nx.read_shp(inputs["MSOACentroidsShapefileWGS84"]) # Must be in epsg:4326 (WGS84)

    Case_Study_Zones = ["Oxfordshire", "Buckinghamshire", "City of Milton Keynes", "Northamptonshire", "Bedfordshire", "Cambridgeshire", "City of Peterborough", "Hertfordshire", "Greater London"]

    X = ox.graph_from_place(Case_Study_Zones, custom_filter='["railway"~"rail|subway|light_rail|tram|narrow_gauge"]') # railway is not included in network_type of package, need to set custom filter
    # crs = X.graph["crs"]
    # print('Graph CRS: ', crs)
    # print()

    # ox.plot_graph(X) # test plot

    X = X.to_undirected()

    # Calculate the origins and destinations for the shortest paths algorithms to be run on OSM graph
    OD_list = calc_shortest_paths_ODs_osm(Zone_nodes, X)

    Flows = []

    for kk, flows_output_key in enumerate(flows_output_keys):
        Flows.append(pd.read_csv(outputs[flows_output_key], header=None))

        # Initialise weights to 0:
        for source, target in X.edges():
            X[source][target][0]["Flows_" + str(kk)] = 0

    TOT_count = len(OD_list)
    # print(OD_list)

    for n, i in enumerate(OD_list):
        print("Flows maps creation - iteration ", n+1, " of ", TOT_count)
        sssp_paths = nx.single_source_dijkstra_path(X, i, weight='length') # single source shortest paths from i to all nodes of the network
        for m, j in enumerate(OD_list):
            shortest_path = sssp_paths[j] # shortest path from i to j
            path_edges = zip(shortest_path, shortest_path[1:])  # Create edges from nodes of the shortest path

            for edge in list(path_edges):
                for cc in range(len(Flows)):
                    X[edge[0]][edge[1]][0]["Flows_" + str(cc)] += Flows[cc].iloc[n, m]

    # save graph to shapefile
    output_folder_path = "./Outputs-CAMKOX_LON/" + "rail_Flows_shp"
    ox.save_graph_shapefile(X, filepath=output_folder_path)

def calc_shortest_paths_ODs_osm(zones_centroids, network):
    # For each zone centroid, this function calculates the closest node in the OSM graph.
    # These nodes will be used as origins and destinations in the shortest paths calculations.
    list_of_ODs = []
    for c in zones_centroids:
        graph_clostest_node = ox.nearest_nodes(network, c[0], c[1], return_dist=False)
        list_of_ODs.append(graph_clostest_node)
    return list_of_ODs