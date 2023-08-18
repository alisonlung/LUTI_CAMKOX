# inputs and outputs of CAMKOX and London LUTI model:
# keys of the inputs and outputs dictionaries with the correpsonding file path

#Inputs of model
inputs = {}

# Census 2021
inputs["DataCensusTS007"]            = "./external-data/Census2021/MSOA/CAMKOX_2021_ts007.csv"
# Employment
inputs["Employment2021"]             = "./external-data/Employment/CAMKOX_2021_ts063.csv"
inputs["Employment2050"]             = "./external-data/Employment/CAMKOX_2050_occ.csv"
# Geography
inputs["CAMKOXMsoaFile"]             = "./external-data/CAMKOX_LON_MSOA.csv"
inputs["MsoaShapefile"]              = "./external-data/geography/msoa_camkox_lon_2011.shp"
inputs["RoadNetworkShapefile"]       = "./external-data/geography/major_roads.shp"
inputs["MSOACentroidsShapefile"]     = "./external-data/geography/msoa_camkox_lon_centroid.shp"
inputs["MSOACentroidsShapefileWGS84"]     = "./external-data/geography/msoa_camkox_lon_centroid_WGS84.shp"
# QUANT matrices
inputs["QUANTCijRoadMinFilename"]    = "./external-data/QUANT_matrices/dis1.bin"
inputs["QUANTCijBusMinFilename"]     = "./external-data/QUANT_matrices/dis2.bin"
inputs["QUANTCijRailMinFilename2021"]    = "./external-data/QUANT_matrices/dis_gbrail_min.bin"
inputs["QUANTCijRailMinFilename2050"]    = "./external-data/QUANT_matrices/dis3.bin"
inputs["SObsRoadFilename"]           = "./external-data/QUANT_matrices/SObs_1.bin"
inputs["SObsBusFilename"]            = "./external-data/QUANT_matrices/SObs_2.bin"
inputs["SObsRailFilename"]           = "./external-data/QUANT_matrices/SObs_3.bin"
# Housing
inputs["DwellingsCAMKOX"]            = "./external-data/Housing_attractiveness/CAMKOX_2021_dwellings_11geo.csv"
inputs["CAMKOXNewHousingDev"]        = "./external-data/New_housing_dev_table_V2.csv"
# Others
inputs["CAMKOXPostcodes"]            = "./external-data/pcd_CAMKOX.csv"
inputs["ZonesCoordinates"]           = "./external-data/zones_data_coordinates.csv"


#Outputs of model
outputs = {}

#2021
outputs["JobsAccessibility2021"]            = "./Outputs-CAMKOX_LON/jobs_accessibility_2021.csv"
outputs["HousingAccessibility2021"]         = "./Outputs-CAMKOX_LON/housing_accessibility_2021.csv"
outputs["JobsDjOi2021"]                     = "./Outputs-CAMKOX_LON/Jobs_DjOi_2021.csv"

outputs["JobsProbTijRoads2021"]             = "./Outputs-CAMKOX_LON/jobsProbTij_roads_2021.csv"
outputs["JobsProbTijBus2021"]               = "./Outputs-CAMKOX_LON/jobsProbTij_bus_2021.csv"
outputs["JobsProbTijRail2021"]              = "./Outputs-CAMKOX_LON/jobsProbTij_rail_2021.csv"
outputs["JobsTijRoads2021"]                 = "./Outputs-CAMKOX_LON/jobsTij_roads_2021.csv"
outputs["JobsTijBus2021"]                   = "./Outputs-CAMKOX_LON/jobsTij_bus_2021.csv"
outputs["JobsTijRail2021"]                  = "./Outputs-CAMKOX_LON/jobsTij_rail_2021.csv"
outputs["ArrowsFlowsCar2021"]               = "./Outputs-CAMKOX_LON/flows_2021_car.geojson"
outputs["ArrowsFlowsBus2021"]               = "./Outputs-CAMKOX_LON/flows_2021_bus.geojson"
outputs["ArrowsFlowsRail2021"]              = "./Outputs-CAMKOX_LON/flows_2021_rail.geojson"
#2050-Expansion
outputs["JobsAccessibility2050"]            = "./Outputs-CAMKOX_LON/jobs_accessibility_2050.csv"
outputs["HousingAccessibility2050"]         = "./Outputs-CAMKOX_LON/housing_accessibility_2050.csv"
outputs["JobsDjOi2050"]                     = "./Outputs-CAMKOX_LON/Jobs_DjOi_2050.csv"

outputs["JobsProbTijRoads2050"]             = "./Outputs-CAMKOX_LON/jobsProbTij_roads_2050.csv"
outputs["JobsProbTijBus2050"]               = "./Outputs-CAMKOX_LON/jobsProbTij_bus_2050.csv"
outputs["JobsProbTijRail2050"]              = "./Outputs-CAMKOX_LON/jobsProbTij_rail_2050.csv"
outputs["JobsTijRoads2050"]                 = "./Outputs-CAMKOX_LON/jobsTij_roads_2050.csv"
outputs["JobsTijBus2050"]                   = "./Outputs-CAMKOX_LON/jobsTij_bus_2050.csv"
outputs["JobsTijRail2050"]                  = "./Outputs-CAMKOX_LON/jobsTij_rail_2050.csv"
outputs["ArrowsFlowsCar2050"]               = "./Outputs-CAMKOX_LON/flows_2050_car.geojson"
outputs["ArrowsFlowsBus2050"]               = "./Outputs-CAMKOX_LON/flows_2050_bus.geojson"
outputs["ArrowsFlowsRail2050"]              = "./Outputs-CAMKOX_LON/flows_2050_rail.geojson"
#2050-New Settlement
outputs["NS_JobsAccessibility2050"]            = "./Outputs-CAMKOX_LON/jobs_accessibility_NS_2050.csv"
outputs["NS_HousingAccessibility2050"]         = "./Outputs-CAMKOX_LON/housing_accessibility_NS_2050.csv"
outputs["NS_JobsDjOi2050"]                     = "./Outputs-CAMKOX_LON/Jobs_DjOi_NS_2050.csv"

outputs["NS_JobsProbTijRoads2050"]             = "./Outputs-CAMKOX_LON/NS_jobsProbTij_roads_2050.csv"
outputs["NS_JobsProbTijBus2050"]               = "./Outputs-CAMKOX_LON/NS_jobsProbTij_bus_2050.csv"
outputs["NS_JobsProbTijRail2050"]              = "./Outputs-CAMKOX_LON/NS_jobsProbTij_rail_2050.csv"
outputs["NS_JobsTijRoads2050"]                 = "./Outputs-CAMKOX_LON/NS_jobsTij_roads_2050.csv"
outputs["NS_JobsTijBus2050"]                   = "./Outputs-CAMKOX_LON/NS_jobsTij_bus_2050.csv"
outputs["NS_JobsTijRail2050"]                  = "./Outputs-CAMKOX_LON/NS_jobsTij_rail_2050.csv"
outputs["NS_ArrowsFlowsCar2050"]               = "./Outputs-CAMKOX_LON/NS_flows_2050_car.geojson"
outputs["NS_ArrowsFlowsBus2050"]               = "./Outputs-CAMKOX_LON/NS_flows_2050_bus.geojson"
outputs["NS_ArrowsFlowsRail2050"]              = "./Outputs-CAMKOX_LON/NS_flows_2050_rail.geojson"
#maps-2021/50 (Expansion)
outputs["MapPopChange20212050"]             = "./Outputs-CAMKOX_LON/pop_change_21-50.png"
outputs["MapHousingAccChange20212050Roads"] = "./Outputs-CAMKOX_LON/HA_change_21-50_roads.png"
outputs["MapHousingAccChange20212050Bus"]   = "./Outputs-CAMKOX_LON/HA_change_21-50_bus.png"
outputs["MapHousingAccChange20212050Rail"]  = "./Outputs-CAMKOX_LON/HA_change_21-50_rail.png"
outputs["MapJobsAccChange20212050Roads"]    = "./Outputs-CAMKOX_LON/JA_change_21-50_roads.png"
outputs["MapJobsAccChange20212050Bus"]      = "./Outputs-CAMKOX_LON/JA_change_21-50_bus.png"
outputs["MapJobsAccChange20212050Rail"]     = "./Outputs-CAMKOX_LON/JA_change_21-50_rail.png"
outputs["MapResultsShapefile"]              = "./Outputs-CAMKOX_LON/CAMKOX_results.shp"
#maps-2021/50 (NewSettlement)
outputs["MapPopChange2021NS2050"]             = "./Outputs-CAMKOX_LON/NS_pop_change_21-50.png"
outputs["MapHousingAccChange2021NS2050Roads"] = "./Outputs-CAMKOX_LON/NS_HA_change_21-50_roads.png"
outputs["MapHousingAccChange2021NS2050Bus"]   = "./Outputs-CAMKOX_LON/NS_HA_change_21-50_bus.png"
outputs["MapHousingAccChange2021NS2050Rail"]  = "./Outputs-CAMKOX_LON/NS_HA_change_21-50_rail.png"
outputs["MapJobsAccChange2021NS2050Roads"]    = "./Outputs-CAMKOX_LON/NS_JA_change_21-50_roads.png"
outputs["MapJobsAccChange2021NS2050Bus"]      = "./Outputs-CAMKOX_LON/NS_JA_change_21-50_bus.png"
outputs["MapJobsAccChange2021NS2050Rail"]     = "./Outputs-CAMKOX_LON/NS_JA_change_21-50_rail.png"
outputs["NS_MapResultsShapefile"]              = "./Outputs-CAMKOX_LON/NS_CAMKOX_results.shp"
