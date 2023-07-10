"""
globals.py

Globals used by model
"""
import os

########################################################################################################################
# Directories paths
modelRunsDir = "./LUTI_CAMKOX/model-runs"

########################################################################################################################
# These are download urls for big external data that can't go in the GitHub repo
url_QUANT_ZoneCodes = "https://liveuclac-my.sharepoint.com/:x:/g/personal/ucfnrmi_ucl_ac_uk/EdlPQ9GtHsFBigZ_sUnOKX0BqJB38g_TeqX8NorvojelfQ?e=6ZsPBE&download=1"

########################################################################################################################
# File names (no complete path as they might be present in more folders with the same name)
# e.g. check that this file is in AAA folder, otherwise load it from BBB folder
ZoneCodesFilename = 'EWS_ZoneCodes.csv'

#cost matrix names
QUANTCijRoadMinFilename = 'dis1.bin'
QUANTCijBusMinFilename = 'dis2.bin' 
QUANTCijRailMinFilename2021 = 'dis_gbrail_min.bin'
QUANTCijRailMinFilename2050 = 'dis3.bin'  

QUANTCijRoadMinFilename_CAMKOX = 'Cij_road_min_CAMKOX.bin' # England and Wales
QUANTCijBusMinFilename_CAMKOX = 'Cij_bus_min_CAMKOX.bin' # England and Wales
QUANTCijRailMinFilename2021_CAMKOX = 'Cij_gbrail_min_CAMKOX.bin' # England and Wales
QUANTCijRailMinFilename2050_CAMKOX = 'Cij_rail_min_CAMKOX.bin' # England and Wales

CijRoadMinFilename = 'Cij_road_min.bin'
CijBusMinFilename = 'Cij_bus_min.bin'
CijRailMinFilename = 'Cij_gbrail_min.bin'

SObsRoadFilename_CAMKOX = 'SObs_1_CAMKOX.bin'
SObsBusFilename_CAMKOX = 'SObs_2_CAMKOX.bin'
SObsRailFilename_CAMKOX = 'SObs_3_CAMKOX.bin'

#centroids for the cost matrices
QUANTCijRoadCentroidsFilename = 'roadcentroidlookup_QC.csv'
QUANTCijBusCentroidsFilename = 'buscentroidlookup_QC.csv'
QUANTCijRailCentroidsFilename = 'gbrailcentroidlookup_QC.csv'

########################################################################################################################
# -- INPUT FILES --
# Census data
data_census_TS007_CAMKOX = os.path.join(modelRunsDir,"TS007EW_MSOA_CAMKOX.csv")

# Employment
HH_floorspace_CAMKOX = os.path.join(modelRunsDir,"FS_OA1.0_CAMKOX.csv")

########################################################################################################################
# -- OUTPUT FILES --

### Journey to work model
# Employment
data_jobs_employment = os.path.join(modelRunsDir,"jobsEmployment.csv")
Jobs_DjOi_2021 = os.path.join(modelRunsDir, "Jobs_DjOi_2021.csv")
Jobs_DjOi_2050 = os.path.join(modelRunsDir, "Jobs_DjOi_2050.csv")
NS_Jobs_DjOi_2050 = os.path.join(modelRunsDir, "NS_Jobs_DjOi_2050.csv")

# Zones and attractors
data_HH_zones_2021 = os.path.join(modelRunsDir,"jobs_Pop_Zones_2021.csv")
data_HH_zones_2050 = os.path.join(modelRunsDir,"jobs_Pop_Zones_2050.csv")
NS_data_HH_zones_2050 = os.path.join(modelRunsDir,"NS_jobs_Pop_Zones_2050.csv")

data_HH_attractors_2021 = os.path.join(modelRunsDir,"jobs_HH_Attractors_2021.csv")
data_HH_attractors_2050 = os.path.join(modelRunsDir,"jobs_HH_Attractors_2050.csv")
NS_data_HH_attractors_2050 = os.path.join(modelRunsDir,"NS_jobs_HH_Attractors_2050.csv")

# Probabilities
data_jobs_probTij_roads_2021_csv = os.path.join(modelRunsDir,"jobsProbTij_roads_2021.csv")
data_jobs_probTij_bus_2021_csv = os.path.join(modelRunsDir,"jobsProbTij_bus_2021.csv")
data_jobs_probTij_rail_2021_csv = os.path.join(modelRunsDir,"jobsProbTij_rail_2021.csv")

# Flows
data_jobs_Tij_roads_2021_csv = os.path.join(modelRunsDir,"jobsTij_roads_2021.csv")
data_jobs_Tij_bus_2021_csv = os.path.join(modelRunsDir,"jobsTij_bus_2021.csv")
data_jobs_Tij_rail_2021_csv = os.path.join(modelRunsDir,"jobsTij_rail_2021.csv")

# Job accessibility
data_jobs_accessibility_2021 = os.path.join(modelRunsDir,"data_jobs_accessibility_2021.csv")

# Housing accessibility
data_housing_accessibility_2021 = os.path.join(modelRunsDir,"data_housing_accessibility_2021.csv")

# Merged Csvs
Pop_Change = os.path.join(modelRunsDir, "Population_change.csv")
HA_Change = os.path.join(modelRunsDir, "Housing_Accessibility_change.csv")
Job_Change = os.path.join(modelRunsDir, "Jobs_Accessibility_change.csv")
NS_Pop_Change = os.path.join(modelRunsDir, "NS_Population_change.csv")
NS_HA_Change = os.path.join(modelRunsDir, "NS_Housing_Accessibility_change.csv")
NS_Job_Change = os.path.join(modelRunsDir, "NS_Jobs_Accessibility_change.csv")

########################################################################################################################
