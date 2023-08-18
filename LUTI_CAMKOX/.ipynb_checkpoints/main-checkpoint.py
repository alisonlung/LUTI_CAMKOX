"""
Land-Use Transport-Interaction Model - CAMKOX and London case study
main.py

Author: Yuet Yung Lung
Supervisor: Dr Fulvio D. Lopane
Repository: https://github.com/alisonlung/LUTI_CAMKOX 

Developed with reference to LUTI framework by Lopane et al. (2023): https://github.com/fdlopane/LUTI_HARMONY

25 August 2023
"""
import os
import time
import pandas as pd
import numpy as np
from geojson import dump

from LUTI_CAMKOX.globals import *
from LUTI_CAMKOX.maps import *
from LUTI_CAMKOX.utils import loadQUANTMatrix, loadMatrix, saveMatrix
from LUTI_CAMKOX.databuilder import ensureFile
from LUTI_CAMKOX.quantjobsmodel import QUANTJobsModel
from LUTI_CAMKOX.analytics import flowArrowsGeoJSON


def start_main(inputs, outputs):
    ################################################################################
    # Initialisation                                                               #
    ################################################################################

    # NOTE: this section provides the base data for the models that come later. This
    # will only be run on the first run of the program to assemble all the tables
    # required from the original sources. After that, if the file exists in the
    # directory, then nothing new is created and this section is effectively
    # skipped, up until the model run section at the end.

    # make a model-runs dir if we need it
    if not os.path.exists(modelRunsDir):
        os.makedirs(modelRunsDir)
    
            
    # Downloads first:
    # this will get the QUANT travel times matrices
    ensureFile(os.path.join(modelRunsDir,ZoneCodesFilename),url_QUANT_ZoneCodes) # zone code lookup that goes with it
    ################################################################################
    # Model run section
    ################################################################################
    print()
    print("Importing QUANT cij matrices")

    CAMKOX_MSOA_df =  pd.read_csv(inputs["CAMKOXMsoaFile"], usecols=["msoa11cd"]) # import file with CAMKOX MSOA codes
    CAMKOX_MSOA_df.columns = ['areakey'] # rename column "msoa11cd" to "areakey"
    CAMKOX_MSOA_list = CAMKOX_MSOA_df['areakey'].tolist()

    # load zone codes lookup file to convert MSOA codes into zone i indexes for the model
    zonecodes_EWS = pd.read_csv(os.path.join(modelRunsDir,ZoneCodesFilename))
    zonecodes_EWS.set_index('areakey')
    zonecodes_EWS_list = zonecodes_EWS['areakey'].tolist()

    #_____________________________________________________________________________________
    # IMPORT cij QUANT matrices
    # ROADS cij
    print()
    print("Importing QUANT roads cij for CAMKOX and London")

    if not os.path.isfile(os.path.join(modelRunsDir,QUANTCijRoadMinFilename_CAMKOX)):
        # load cost matrix, time in minutes between MSOA zones for roads:
        cij_road_EWS = loadQUANTMatrix(inputs["QUANTCijRoadMinFilename"])
        cij_road_EWS_df = pd.DataFrame(cij_road_EWS, index=zonecodes_EWS_list, columns=zonecodes_EWS_list) # turn the numpy array into a pd dataframe, (index and columns: MSOA codes)
        cij_road_CAMKOX_df = cij_road_EWS_df[CAMKOX_MSOA_list]  # Create CAMKOX df filtering EWS columns
        cij_road_CAMKOX_df = cij_road_CAMKOX_df.loc[CAMKOX_MSOA_list]  # Filter rows
        cij_road_CAMKOX = cij_road_CAMKOX_df.to_numpy()  # numpy matrix for CAMKOX (same format as utils loadQUANTMatrix)
        cij_road_CAMKOX[cij_road_CAMKOX < 1] = 1  # lower limit of 1 minute links
        saveMatrix(cij_road_CAMKOX, os.path.join(modelRunsDir,QUANTCijRoadMinFilename_CAMKOX))
        # save as csv file
        np.savetxt(os.path.join(modelRunsDir, "cij_road_CAMKOX.csv"), cij_road_CAMKOX, delimiter=",")
    else:
        cij_road_CAMKOX = loadMatrix(os.path.join(modelRunsDir,QUANTCijRoadMinFilename_CAMKOX))
        print('cij roads shape: ', cij_road_CAMKOX.shape)

    # Export cij matrices for checking
    # np.savetxt(os.path.join(modelRunsDir,'debug_cij_roads.csv'), cij_road_CAMKOX, delimiter=',', fmt='%i')

    #_____________________________________________________________________________________
    # BUS & FERRIES cij
    print()
    print("Importing QUANT bus cij for CAMKOX and London")

    if not os.path.isfile(os.path.join(modelRunsDir,QUANTCijBusMinFilename_CAMKOX)):
        # load cost matrix, time in minutes between MSOA zones for bus and ferries network:
        cij_bus_EWS = loadQUANTMatrix(inputs["QUANTCijBusMinFilename"])
        cij_bus_EWS_df = pd.DataFrame(cij_bus_EWS, index=zonecodes_EWS_list, columns=zonecodes_EWS_list) # turn the numpy array into a pd dataframe, (index and columns: MSOA codes)
        cij_bus_CAMKOX_df = cij_bus_EWS_df[CAMKOX_MSOA_list]  # Create CAMKOX df filtering EWS columns
        cij_bus_CAMKOX_df = cij_bus_CAMKOX_df.loc[CAMKOX_MSOA_list]  # Filter rows
        cij_bus_CAMKOX = cij_bus_CAMKOX_df.to_numpy()  # numpy matrix for CAMKOX (same format as utils loadQUANTMatrix)
        cij_bus_CAMKOX[cij_bus_CAMKOX < 1] = 1  # lower limit of 1 minute links
        saveMatrix(cij_bus_CAMKOX, os.path.join(modelRunsDir, QUANTCijBusMinFilename_CAMKOX))
        # save as csv file
        np.savetxt(os.path.join(modelRunsDir, "cij_bus_CAMKOX.csv"), cij_bus_CAMKOX, delimiter=",")
    else:
        cij_bus_CAMKOX = loadMatrix(os.path.join(modelRunsDir,QUANTCijBusMinFilename_CAMKOX))
        print('cij bus shape: ', cij_bus_CAMKOX.shape)

    # Export cij matrices for checking
    # np.savetxt(os.path.join(modelRunsDir,'debug_cij_bus.csv'), cij_bus_CAMKOX, delimiter=',', fmt='%i')

    #_____________________________________________________________________________________
    # RAILWAYS cij
    print()
    print("Importing 2021 & 2050 QUANT rail cij for CAMKOX and London")
    
    # load matrices for 2021
    if not os.path.isfile(os.path.join(modelRunsDir,QUANTCijRailMinFilename2021_CAMKOX)):
        # load cost matrix, time in minutes between MSOA zones for railways:
        cij_rail_EWS_2021 = loadQUANTMatrix(inputs["QUANTCijRailMinFilename2021"])
        cij_rail_EWS_df_2021 = pd.DataFrame(cij_rail_EWS_2021, index=zonecodes_EWS_list, columns=zonecodes_EWS_list) # turn the numpy array into a pd dataframe, (index and columns: MSOA codes)
        cij_rail_CAMKOX_df_2021 = cij_rail_EWS_df_2021[CAMKOX_MSOA_list]  # Create CAMKOX df filtering EWS columns
        cij_rail_CAMKOX_df_2021 = cij_rail_CAMKOX_df_2021.loc[CAMKOX_MSOA_list]  # Filter rows
        cij_rail_CAMKOX_2021 = cij_rail_CAMKOX_df_2021.to_numpy()  # numpy matrix for CAMKOX (same format as utils loadQUANTMatrix)
        cij_rail_CAMKOX_2021[cij_rail_CAMKOX_2021 < 1] = 1  # lower limit of 1 minute links
        saveMatrix(cij_rail_CAMKOX_2021, os.path.join(modelRunsDir, QUANTCijRailMinFilename2021_CAMKOX))
        # save as csv file
        np.savetxt(os.path.join(modelRunsDir, "cij_rail_CAMKOX_2021.csv"), cij_rail_CAMKOX_2021, delimiter=",")
    else:
        cij_rail_CAMKOX_2021 = loadMatrix(os.path.join(modelRunsDir,QUANTCijRailMinFilename2021_CAMKOX))
        print('2021 cij rail shape: ', cij_rail_CAMKOX_2021.shape)
        
    # load matrices for 2050 (with consideration of new rail route)
    if not os.path.isfile(os.path.join(modelRunsDir,QUANTCijRailMinFilename2050_CAMKOX)):
        # load cost matrix, time in minutes between MSOA zones for railways:
        cij_rail_EWS_2050 = loadQUANTMatrix(inputs["QUANTCijRailMinFilename2050"])
        cij_rail_EWS_df_2050 = pd.DataFrame(cij_rail_EWS_2050, index=zonecodes_EWS_list, columns=zonecodes_EWS_list) # turn the numpy array into a pd dataframe, (index and columns: MSOA codes)
        cij_rail_CAMKOX_df_2050 = cij_rail_EWS_df_2050[CAMKOX_MSOA_list]  # Create CAMKOX df filtering EWS columns
        cij_rail_CAMKOX_df_2050 = cij_rail_CAMKOX_df_2050.loc[CAMKOX_MSOA_list]  # Filter rows
        cij_rail_CAMKOX_2050 = cij_rail_CAMKOX_df_2050.to_numpy()  # numpy matrix for CAMKOX (same format as utils loadQUANTMatrix)
        cij_rail_CAMKOX_2050[cij_rail_CAMKOX_2050 < 1] = 1  # lower limit of 1 minute links
        saveMatrix(cij_rail_CAMKOX_2050, os.path.join(modelRunsDir, QUANTCijRailMinFilename2050_CAMKOX))
        # save as csv file
        np.savetxt(os.path.join(modelRunsDir, "cij_rail_CAMKOX_2050.csv"), cij_rail_CAMKOX_2050, delimiter=",")
    else:
        cij_rail_CAMKOX_2050 = loadMatrix(os.path.join(modelRunsDir,QUANTCijRailMinFilename2050_CAMKOX))
        print('2050 cij rail shape: ', cij_rail_CAMKOX_2050.shape)

    # Export cij matrices for checking
    # np.savetxt(os.path.join(modelRunsDir,'debug_cij_rail.csv'), cij_rail_CAMKOX, delimiter=',', fmt='%i')

    print()
    print("Importing 2021 & 2050 QUANT cij matrices completed.")
    print()
    #_____________________________________________________________________________________

    # IMPORT SObs QUANT matrices: observed trips
    print("Importing SObs matrices")

    # SObs ROADS
    print()
    print("Importing SObs for roads for CAMKOX and London")

    if not os.path.isfile(os.path.join(modelRunsDir,SObsRoadFilename_CAMKOX)):
        # load observed trips matrix for roads:
        SObs_road_EWS = loadQUANTMatrix(inputs["SObsRoadFilename"])
        SObs_road_EWS_df = pd.DataFrame(SObs_road_EWS, index=zonecodes_EWS_list, columns=zonecodes_EWS_list) # turn the numpy array into a pd dataframe, (index and columns: MSOA codes)
        SObs_road_CAMKOX_df = SObs_road_EWS_df[CAMKOX_MSOA_list]  # Create CAMKOX df filtering EWS columns
        SObs_road_CAMKOX_df = SObs_road_CAMKOX_df.loc[CAMKOX_MSOA_list]  # Filter rows
        SObs_road_CAMKOX = SObs_road_CAMKOX_df.to_numpy()  # numpy matrix for CAMKOX (same format as utils loadQUANTMatrix)
        saveMatrix(SObs_road_CAMKOX, os.path.join(modelRunsDir, SObsRoadFilename_CAMKOX))
    # else:
    #     SObs_road_CAMKOX = loadMatrix(os.path.join(modelRunsDir,SObsRoadFilename_CAMKOX))
    #     print('Sobs road shape: ', SObs_road_CAMKOX.shape)
    #_____________________________________________________________________________________

    # SObs BUS & FERRIES
    print()
    print("Importing SObs for bus & ferries for CAMKOX and London")

    if not os.path.isfile(os.path.join(modelRunsDir,SObsBusFilename_CAMKOX)):
        # load observed trips matrix for bus and ferries:
        SObs_bus_EWS = loadQUANTMatrix(inputs["SObsBusFilename"])
        SObs_bus_EWS_df = pd.DataFrame(SObs_bus_EWS, index=zonecodes_EWS_list, columns=zonecodes_EWS_list)  # turn the numpy array into a pd dataframe, (index and columns: MSOA codes)
        SObs_bus_CAMKOX_df = SObs_bus_EWS_df[CAMKOX_MSOA_list]  # Create CAMKOX df filtering EWS columns
        SObs_bus_CAMKOX_df = SObs_bus_CAMKOX_df.loc[CAMKOX_MSOA_list]  # Filter rows
        SObs_bus_CAMKOX = SObs_bus_CAMKOX_df.to_numpy()  # numpy matrix for CAMKOX (same format as utils loadQUANTMatrix)
        saveMatrix(SObs_bus_CAMKOX, os.path.join(modelRunsDir,SObsBusFilename_CAMKOX))
    # else:
    #     SObs_bus_CAMKOX = loadMatrix(os.path.join(modelRunsDir,SObsBusFilename_CAMKOX))
    #     print('Sobs bus shape: ', SObs_bus_CAMKOX.shape)
    #_____________________________________________________________________________________

    # SObs RAIL
    print()
    print("Importing SObs for rail for CAMKOX and London")

    if not os.path.isfile(os.path.join(modelRunsDir,SObsRailFilename_CAMKOX)):
        # load observed trips matrix for rails:
        SObs_rail_EWS = loadQUANTMatrix(inputs["SObsRailFilename"])
        SObs_rail_EWS_df = pd.DataFrame(SObs_rail_EWS, index=zonecodes_EWS_list, columns=zonecodes_EWS_list)  # turn the numpy array into a pd dataframe, (index and columns: MSOA codes)
        SObs_rail_CAMKOX_df = SObs_rail_EWS_df[CAMKOX_MSOA_list]  # Create CAMKOX df filtering EWS columns
        SObs_rail_CAMKOX_df = SObs_rail_CAMKOX_df.loc[CAMKOX_MSOA_list]  # Filter rows
        SObs_rail_CAMKOX = SObs_rail_CAMKOX_df.to_numpy()  # numpy matrix for CAMKOX (same format as utils loadQUANTMatrix)
        saveMatrix(SObs_rail_CAMKOX, os.path.join(modelRunsDir,SObsRailFilename_CAMKOX))
    # else:
    #     SObs_rail_CAMKOX = loadMatrix(os.path.join(modelRunsDir,SObsRailFilename_CAMKOX))
    #     print('Sobs bus shape: ', SObs_rail_CAMKOX.shape)
    #     print()
    #_____________________________________________________________________________________


    # now run the relevant models to produce the outputs
    runNewHousingDev(CAMKOX_MSOA_list, zonecodes_EWS, cij_road_CAMKOX, cij_bus_CAMKOX, cij_rail_CAMKOX_2021, cij_rail_CAMKOX_2050, inputs, outputs)

    # Maps creation:

    # Population maps:
    population_map_creation(inputs, outputs)

    # Flows maps:
    # THIS FEATURE IS TURNED OFF - generation of flows visualisation requires long run time
    # Road Network 
    create_flow_maps = False
    if create_flow_maps:
        flows_output_keys = ["JobsTijRoads2021", "JobsTijBus2021", "JobsTijRoads2050", "JobsTijBus2050", "NS_JobsTijRoads2050", "NS_JobsTijBus2050"]
        flows_map_creation(inputs, outputs, flows_output_keys)

    # Rail Netowork (Noted that only existing network is shown, new rail section is not visualised as it is not yet constructed):
    create_rail_flow_maps = False
    if create_rail_flow_maps:
        flows_output_keys = ["JobsTijRail2021", "JobsTijRail2050", "NS_JobsTijRail2050"]
        rail_flows_map_creation(inputs, outputs, flows_output_keys)    
   
################################################################################
# End initialisation
################################################################################

################################################################################
# New housing development scenario                                   
################################################################################
"""
New housing development scenario:
1. Run the 2021 Journey to Work model (for calibration)
2. Update population and number of dwellings from the new housing development table
3. Make predictions based on the new population/ number of dwellings & calibrated parameter
"""

def runNewHousingDev(CAMKOX_MSOA_list, zonecodes_EWS, cij_road_CAMKOX, cij_bus_CAMKOX, cij_rail_CAMKOX_2021, cij_rail_CAMKOX_2050, inputs, outputs):
    # First run the base model to calibrate it with 2011 observed trip data:
    # Run Journey to work model:
    beta_2021, DjPred_JtW_2021 = runJourneyToWorkModel(CAMKOX_MSOA_list, zonecodes_EWS, cij_road_CAMKOX, cij_bus_CAMKOX, cij_rail_CAMKOX_2021, inputs, outputs)

    # CAMKOX new housing development scenario:
    # base year: 2021, projection year: 2050
    # First, create the new population files: updated population per MSOA zone
    # 2021 (base year): no modification of attractors/jobs is required
    # 2050 (proj year): use census (2021) + new houses tot_2021_2050 (it also takes the previous years into account)
    # Then, run the models with this new populations

    # Create pop file for 2021 and 2050:
    #New Housing Development - Expansion
    # read csv from New_housing_dev_table and use columns: "Area Description" and "tot_2021_2026"
    NewHousingDev_table_2050 = pd.read_csv(inputs["CAMKOXNewHousingDev"], usecols=['Area Description', 'Tot_Alloc_E']) # for 2050 read the entry up to year 2050
    #New Housing Development - New Settlement
    NS_NewHousingDev_table_2050 = pd.read_csv(inputs["CAMKOXNewHousingDev"], usecols=['Area Description', 'Tot_Alloc_N']) # for 2050 read the entry up to year 2050


    # Group by MSOA and calculate population from number of houses
    Av_HH_size = 2.4  # The average household size in the UK is 2.4, from ONS (Household and resident characteristics: 2021)

    #New Housing Development - Expansion
    NewHousingDev_table_2050.rename(columns={'Tot_Alloc_E':'Expansion_2021_2050'}, inplace=True)
    NewHousingDev_table_2050['NewPop_2021_2050'] = NewHousingDev_table_2050['Expansion_2021_2050'] * Av_HH_size  # it's ok that it's not an integer as the final result will be a float anyway
    NewHousingPop_2050 = NewHousingDev_table_2050[['Area Description', 'NewPop_2021_2050']] # drop the n of houses column
    #New Housing Development - New Settlement
    NS_NewHousingDev_table_2050.rename(columns={'Tot_Alloc_N':'New_Settle_2021_2050'}, inplace=True)
    NS_NewHousingDev_table_2050['NS_NewPop_2021_2050'] = NS_NewHousingDev_table_2050['New_Settle_2021_2050'] * Av_HH_size  # it's ok that it's not an integer as the final result will be a float anyway
    NS_NewHousingPop_2050 = NS_NewHousingDev_table_2050[['Area Description', 'NS_NewPop_2021_2050']] # drop the n of houses column

    # Now run the JtW model with 2011 beta and updated pop (without calibration)
    #New Housing Development - Expansion
    beta_2021, DjPred_JtW_2050 = runJourneyToWorkModel(CAMKOX_MSOA_list, zonecodes_EWS, cij_road_CAMKOX, cij_bus_CAMKOX, cij_rail_CAMKOX_2050, inputs, outputs, 'NewHousingDev_Expand_2050', NewHousingPop_2050, beta_2021)
    #New Housing Development - New Settlement
    beta_2021, DjPred_JtW_2050 = runJourneyToWorkModel(CAMKOX_MSOA_list, zonecodes_EWS, cij_road_CAMKOX, cij_bus_CAMKOX, cij_rail_CAMKOX_2050, inputs, outputs, 'NewHousingDev_NewSettle_2050', NS_NewHousingPop_2050, beta_2021)


# Areas abbreviations for models' data:
# EW = England + Wales
# EWS = England + Wales + Scotland
# CAMKOX = Cambridge + Milton Keynes + Oxford, London is also included for flow analysis

################################################################################
# Journey to work Model                                                        #
################################################################################

"""
runJourneyToWorkModel
Origins: workplaces, Destinations: households' population
"""
# Journey to work model with households (HH) number of dwellings as attractor
def runJourneyToWorkModel(CAMKOX_MSOA_list, zonecodes_EWS, cij_road_CAMKOX, cij_bus_CAMKOX, cij_rail_CAMKOX, inputs, outputs, Scenario='2021', Scenario_pop_table=None, Beta_calibrated=None):
    print("Running Journey to Work ", Scenario, " model.")
    start = time.perf_counter()
    # Singly constrained model:
    # conserve the number of jobs and predict the population residing in MSOA zones
    # journeys to work generated by jobs
    # Origins: workplaces
    # Destinations: MSOAs households
    # Attractor: number of dwellings

    """
                    Journey to work    
     Origins:       workplaces         
     Destinations:  households         
     conserved:     jobs               
     predicted:     population @ MSOA  
     attractor:     Number of dwellings     
    """

    # Now run the model with or without calibration according to the scenario:
    # Data is transformed from 2021 MSOA to 2011 MSOA by Excel lookup with area filtered
    if not os.path.isfile(data_census_TS007_CAMKOX):
        data_census_TS007_CAMKOX_df = pd.read_csv(inputs["DataCensusTS007"], index_col='geography code')
        data_census_TS007_CAMKOX_df['geography code'] = data_census_TS007_CAMKOX_df.index # turn the index (i.e. MSOA codes) back into a columm
        data_census_TS007_CAMKOX_df.reset_index(drop=True, inplace=True)
        data_census_TS007_CAMKOX_df.to_csv(data_census_TS007_CAMKOX)

    HHZones, HHAttractors = QUANTJobsModel.loadEmploymentData_HHAttractiveness(data_census_TS007_CAMKOX, inputs["DwellingsCAMKOX"], Scenario)
    # if we are running a scenario, update the HHZones with the new population
    if Scenario == '2021':
        dfEi = pd.read_csv(inputs["Employment2021"])  # select the columns that I need from file
        dfEi.rename(columns={'geography code': 'msoa', 'Occupation (current): Total': 'employment_tot'}, inplace=True)
        # drop columns:
        dfEi = dfEi[['msoa','employment_tot']]
        jobs = dfEi.join(other=zonecodes_EWS.set_index('areakey'), on='msoa')  # this codes dfEi by zonei
        jobs.to_csv(data_jobs_employment) # save file to csv in model-runs directory

        HHZones.to_csv(data_HH_zones_2021)  # save file to csv in model-runs directory
        HHAttractors.to_csv(data_HH_attractors_2021)  # save file to csv in model-runs directory

        HHZones = HHZones[['zonei', 'Population_tot']]
        HHAttractors = HHAttractors[['zonei', 'N_of_Dwellings']]

    elif Scenario == 'NewHousingDev_Expand_2050':
        dfEi = pd.read_csv(inputs["Employment2050"])  # select the columns that I need from file
        dfEi.rename(columns={'Jobs': 'employment_tot'}, inplace=True)
        jobs = dfEi.join(other=zonecodes_EWS.set_index('areakey'), on='msoa')  # this codes dfEi by zonei

        # Rename Scenario_pop_table's columns:
        Scenario_pop_table.rename(columns={'Area Description':'zonei'}, inplace=True)

        # Update the population with the 2050 projection
        HHZones = HHZones.join(Scenario_pop_table.set_index('zonei'), on=['zonei'])
        HHZones['NewPop_2021_2050'] = HHZones['NewPop_2021_2050'].fillna(0)  # Replace NaN with 0
        HHZones['Population_tot'] = HHZones['Population_tot'] + HHZones['NewPop_2021_2050']
        HHZones = HHZones[['zonei', 'Population_tot']]

        # Update the number of dwellings with the 2050 projection
        NewHousingDev_table_2050 = pd.read_csv(inputs["CAMKOXNewHousingDev"], usecols=['Area Description', 'Tot_Alloc_E'])  # for 2050 read the entry up to year 2031
        NewHousingDev_table_2050.rename(columns={'Area Description': 'zonei', 'Tot_Alloc_E': 'Expansion_2021_2050'}, inplace=True)

        HHAttractors = HHAttractors.join(NewHousingDev_table_2050.set_index('zonei'), on=['zonei'])  # Join the Attractors df with the new houses df
        HHAttractors['Expansion_2021_2050'] = HHAttractors['Expansion_2021_2050'].fillna(0)  # Replace NaN with 0
        HHAttractors['N_of_Dwellings'] = HHAttractors['N_of_Dwellings'] + HHAttractors['Expansion_2021_2050']
        HHAttractors = HHAttractors[['zonei', 'N_of_Dwellings']]

        HHZones.to_csv(data_HH_zones_2050)  # save file to csv in model-runs directory
        HHAttractors.to_csv(data_HH_attractors_2050)  # save file to csv in model-runs directory
    
    elif Scenario == 'NewHousingDev_NewSettle_2050':
        dfEi = pd.read_csv(inputs["Employment2050"])  # select the columns that I need from file
        dfEi.rename(columns={'Jobs': 'employment_tot'}, inplace=True)
        jobs = dfEi.join(other=zonecodes_EWS.set_index('areakey'), on='msoa')  # this codes dfEi by zonei

        # Rename Scenario_pop_table's columns:
        Scenario_pop_table.rename(columns={'Area Description':'zonei'}, inplace=True)

        # Update the population with the 2050 projection
        HHZones = HHZones.join(Scenario_pop_table.set_index('zonei'), on=['zonei'])
        HHZones['NS_NewPop_2021_2050'] = HHZones['NS_NewPop_2021_2050'].fillna(0)  # Replace NaN with 0
        HHZones['Population_tot'] = HHZones['Population_tot'] + HHZones['NS_NewPop_2021_2050']
        HHZones = HHZones[['zonei', 'Population_tot']]

        # Update the number of dwellings with the 2050 projection
        NS_NewHousingDev_table_2050 = pd.read_csv(inputs["CAMKOXNewHousingDev"], usecols=['Area Description', 'Tot_Alloc_N'])  # for 2050 read the entry up to year 2031
        NS_NewHousingDev_table_2050.rename(columns={'Area Description': 'zonei', 'Tot_Alloc_N': 'NS_Newhouses_2021_2050'}, inplace=True)

        HHAttractors = HHAttractors.join(NS_NewHousingDev_table_2050.set_index('zonei'), on=['zonei'])  # Join the Attractors df with the new houses df
        HHAttractors['NS_Newhouses_2021_2050'] = HHAttractors['NS_Newhouses_2021_2050'].fillna(0)  # Replace NaN with 0
        HHAttractors['N_of_Dwellings'] = HHAttractors['N_of_Dwellings'] + HHAttractors['NS_Newhouses_2021_2050']
        HHAttractors = HHAttractors[['zonei', 'N_of_Dwellings']]

        HHZones.to_csv(NS_data_HH_zones_2050)  # save file to csv in model-runs directory
        HHAttractors.to_csv(NS_data_HH_attractors_2050)  # save file to csv in model-runs directory

    # Now run the model with or without calibration according to the scenario:
    if Scenario == '2021':
        # Load observed data for model calibration:
        SObs_road, SObs_bus, SObs_rail = QUANTJobsModel.loadObsData()

        # Use cij as cost matrix (MSOA to MSOA)
        m, n = cij_road_CAMKOX.shape
        model = QUANTJobsModel(m, n)
        model.setObsMatrix(SObs_road, SObs_bus, SObs_rail)
        model.setAttractorsAj(HHAttractors, 'zonei', 'N_of_Dwellings')
        model.setPopulationEi(jobs, 'zonei', 'employment_tot')
        model.setCostMatrixCij(cij_road_CAMKOX, cij_bus_CAMKOX, cij_rail_CAMKOX)

        Tij, beta_k, cbar_k = model.run3modes() # run the model with 3 modes + calibration

        # Compute the probability of a flow from an MSOA zone to any (i.e. all) of the possible point zones.
        jobs_probTij = model.computeProbabilities3modes(Tij)

        # Jobs accessibility:
        # Job accessibility is the distribution of population around a job location.

        DjPred_road = Tij[0].sum(axis=1)
        Ji_road = Calculate_Job_Accessibility(DjPred_road, cij_road_CAMKOX)

        DjPred_bus = Tij[1].sum(axis=1)
        Ji_bus = Calculate_Job_Accessibility(DjPred_bus, cij_bus_CAMKOX)

        DjPred_rail = Tij[2].sum(axis=1)
        Ji_rail = Calculate_Job_Accessibility(DjPred_rail, cij_rail_CAMKOX)

        # Save output:
        Jobs_accessibility_df = pd.DataFrame( {'areakey': CAMKOX_MSOA_list, 'JAcar21': Ji_road, 'JAbus21': Ji_bus, 'JArail21': Ji_rail})
        Jobs_accessibility_df.to_csv(outputs["JobsAccessibility2021"])

        # Housing Accessibility:
        # Housing accessibility is the distribution of jobs around a housing location.

        OiPred_road = Tij[0].sum(axis=0)
        Hi_road = Calculate_Housing_Accessibility(OiPred_road, cij_road_CAMKOX)

        OiPred_bus = Tij[1].sum(axis=0)
        Hi_bus = Calculate_Housing_Accessibility(OiPred_bus, cij_bus_CAMKOX)

        OiPred_rail = Tij[2].sum(axis=0)
        Hi_rail = Calculate_Housing_Accessibility(OiPred_rail, cij_rail_CAMKOX)

        # Save output:
        Housing_accessibility_df = pd.DataFrame({'areakey': CAMKOX_MSOA_list, 'HAcar21': Hi_road, 'HAbus21': Hi_bus, 'HArail21': Hi_rail})
        Housing_accessibility_df.to_csv(outputs["HousingAccessibility2021"])

        # Create a Oi Dj table
        jobs['DjPred_Car_21'] = Tij[0].sum(axis=1)
        jobs['DjPred_Bus_21'] = Tij[1].sum(axis=1)
        jobs['DjPred_Rail_21'] = Tij[2].sum(axis=1)
        jobs['DjPred_Tot_21'] = Tij[0].sum(axis=1) + Tij[1].sum(axis=1) + Tij[2].sum(axis=1)
        jobs['OiPred_Car_21'] = Tij[0].sum(axis=0)
        jobs['OiPred_Bus_21'] = Tij[1].sum(axis=0)
        jobs['OiPred_Rail_21'] = Tij[2].sum(axis=0)
        jobs['OiPred_Tot_21'] = Tij[0].sum(axis=0) + Tij[1].sum(axis=0) + Tij[2].sum(axis=0)
        jobs['Job_accessibility_roads'] = Jobs_accessibility_df['JAcar21']
        jobs['Jobs_accessibility_bus'] = Jobs_accessibility_df['JAbus21']
        jobs['Jobs_accessibility_rail'] = Jobs_accessibility_df['JArail21']
        jobs['Housing_accessibility_roads'] = Housing_accessibility_df['HAcar21']
        jobs['Housing_accessibility_bus'] = Housing_accessibility_df['HAbus21']
        jobs['Housing_accessibility_rail'] = Housing_accessibility_df['HArail21']
        jobs.to_csv(outputs["JobsDjOi2021"])

        # Save output matrices
        print("Saving output matrices...")

        # Probabilities:
        np.savetxt(outputs["JobsProbTijRoads2021"], jobs_probTij[0], delimiter=",")
        np.savetxt(outputs["JobsProbTijBus2021"], jobs_probTij[1], delimiter=",")
        np.savetxt(outputs["JobsProbTijRail2021"], jobs_probTij[2], delimiter=",")

        # People flows
        np.savetxt(outputs["JobsTijRoads2021"], Tij[0], delimiter=",")
        np.savetxt(outputs["JobsTijBus2021"], Tij[1], delimiter=",")
        np.savetxt(outputs["JobsTijRail2021"], Tij[2], delimiter=",")

        # Geojson flows files - arrows
        flow_zonecodes = pd.read_csv(inputs["ZonesCoordinates"])
        flow_car = flowArrowsGeoJSON(Tij[0], flow_zonecodes)
        with open(outputs["ArrowsFlowsCar2021"], 'w') as f:
            dump(flow_car, f)
        flow_bus = flowArrowsGeoJSON(Tij[1], flow_zonecodes)
        with open(outputs["ArrowsFlowsBus2021"], 'w') as f:
            dump(flow_bus, f)
        flow_rail = flowArrowsGeoJSON(Tij[2], flow_zonecodes)
        with open(outputs["ArrowsFlowsRail2021"], 'w') as f:
            dump(flow_rail, f)

        print("JtW model", Scenario, "cbar [roads, bus, rail] = ", cbar_k)
        print("JtW model", Scenario, "beta [roads, bus, rail] = ", beta_k)

        # Calculate predicted population
        DjPred = np.zeros(n)
        for k in range(len(Tij)):
            DjPred += Tij[k].sum(axis=1)
        # Create a dataframe with Zone and people count
        DjPred = pd.DataFrame(DjPred, columns=['population'])
        DjPred['zonei'] = CAMKOX_MSOA_list

        end = time.perf_counter()
        print("Journey to work model", Scenario, "run elapsed time (secs) =", end - start)
        print()

        return beta_k, DjPred

    elif Scenario == 'NewHousingDev_Expand_2050':
        # Use cij as cost matrix (MSOA to MSOA)
        m, n = cij_road_CAMKOX.shape
        model = QUANTJobsModel(m, n)
        model.setAttractorsAj(HHAttractors, 'zonei', 'N_of_Dwellings')
        model.setPopulationEi(jobs, 'zonei', 'employment_tot')
        model.setCostMatrixCij(cij_road_CAMKOX, cij_bus_CAMKOX, cij_rail_CAMKOX)

        Tij, cbar_k = model.run3modes_NoCalibration(Beta_calibrated)
        # Compute the probability of a flow from an MSOA zone to any (i.e. all) of the possible point zones.
        jobs_probTij = model.computeProbabilities3modes(Tij)

        # Jobs accessibility:
        DjPred_road = Tij[0].sum(axis=1)
        Ji_road = Calculate_Job_Accessibility(DjPred_road, cij_road_CAMKOX)

        DjPred_bus = Tij[1].sum(axis=1)
        Ji_bus = Calculate_Job_Accessibility(DjPred_bus, cij_bus_CAMKOX)

        DjPred_rail = Tij[2].sum(axis=1)
        Ji_rail = Calculate_Job_Accessibility(DjPred_rail, cij_rail_CAMKOX)

        # Save output:
        Jobs_accessibility_df = pd.DataFrame({'areakey': CAMKOX_MSOA_list, 'JAcar50': Ji_road, 'JAbus50': Ji_bus, 'JArail50': Ji_rail})
        Jobs_accessibility_df.to_csv(outputs["JobsAccessibility2050"])

        # Housing Accessibility:
        OiPred_road = Tij[0].sum(axis=0)
        Hi_road = Calculate_Housing_Accessibility(OiPred_road, cij_road_CAMKOX)

        OiPred_bus = Tij[1].sum(axis=0)
        Hi_bus = Calculate_Housing_Accessibility(OiPred_bus, cij_bus_CAMKOX)

        OiPred_rail = Tij[2].sum(axis=0)
        Hi_rail = Calculate_Housing_Accessibility(OiPred_rail, cij_bus_CAMKOX)

        # Save output:
        Housing_accessibility_df = pd.DataFrame({'areakey': CAMKOX_MSOA_list, 'HAcar50': Hi_road, 'HAbus50': Hi_bus,'HArail50': Hi_rail})
        Housing_accessibility_df.to_csv(outputs["HousingAccessibility2050"])

        # Create a Oi Dj table
        jobs['DjPred_Car_50'] = Tij[0].sum(axis=1)
        jobs['DjPred_Bus_50'] = Tij[1].sum(axis=1)
        jobs['DjPred_Rail_50'] = Tij[2].sum(axis=1)
        jobs['DjPred_Tot_50'] = Tij[0].sum(axis=1) + Tij[1].sum(axis=1) + Tij[2].sum(axis=1)
        jobs['OiPred_Car_50'] = Tij[0].sum(axis=0)
        jobs['OiPred_Bus_50'] = Tij[1].sum(axis=0)
        jobs['OiPred_Rail_50'] = Tij[2].sum(axis=0)
        jobs['OiPred_Tot_50'] = Tij[0].sum(axis=0) + Tij[1].sum(axis=0) + Tij[2].sum(axis=0)
        jobs['Job_accessibility_roads'] = Jobs_accessibility_df['JAcar50']
        jobs['Jobs_accessibility_bus'] = Jobs_accessibility_df['JAbus50']
        jobs['Jobs_accessibility_rail'] = Jobs_accessibility_df['JArail50']
        jobs['Housing_accessibility_roads'] = Housing_accessibility_df['HAcar50']
        jobs['Housing_accessibility_bus'] = Housing_accessibility_df['HAbus50']
        jobs['Housing_accessibility_rail'] = Housing_accessibility_df['HArail50']
        jobs.to_csv(outputs["JobsDjOi2050"])


        # Save output matrices
        print("Saving output matrices...")

        # Probabilities:
        np.savetxt(outputs["JobsProbTijRoads2050"], jobs_probTij[0], delimiter=",")
        np.savetxt(outputs["JobsProbTijBus2050"], jobs_probTij[1], delimiter=",")
        np.savetxt(outputs["JobsProbTijRail2050"], jobs_probTij[2], delimiter=",")

        # People flows
        np.savetxt(outputs["JobsTijRoads2050"], Tij[0], delimiter=",")
        np.savetxt(outputs["JobsTijBus2050"], Tij[1], delimiter=",")
        np.savetxt(outputs["JobsTijRail2050"], Tij[2], delimiter=",")

        # Geojson flows files - arrows
        flow_zonecodes = pd.read_csv(inputs["ZonesCoordinates"])
        flow_car = flowArrowsGeoJSON(Tij[0], flow_zonecodes)
        with open(outputs["ArrowsFlowsCar2050"], 'w') as f:
            dump(flow_car, f)
        flow_bus = flowArrowsGeoJSON(Tij[1], flow_zonecodes)
        with open(outputs["ArrowsFlowsBus2050"], 'w') as f:
            dump(flow_bus, f)
        flow_rail = flowArrowsGeoJSON(Tij[2], flow_zonecodes)
        with open(outputs["ArrowsFlowsRail2050"], 'w') as f:
            dump(flow_rail, f)

        print("JtW model", Scenario, " cbar [roads, bus, rail] = ", cbar_k)

        # Calculate predicted population
        DjPred = np.zeros(n)
        for k in range(len(Tij)):
            DjPred += Tij[k].sum(axis=1)
        # Create a dataframe with Zone and people count
        DjPred = pd.DataFrame(DjPred, columns=['population'])
        DjPred['zonei'] = CAMKOX_MSOA_list

        end = time.perf_counter()
        print("Journey to work model run elapsed time (secs)=", end - start)
        # print("Journey to work model run elapsed time (mins)=", (end - start) / 60)
        print()

        return Beta_calibrated, DjPred
    
    elif Scenario == 'NewHousingDev_NewSettle_2050':
        # Use cij as cost matrix (MSOA to MSOA)
        m, n = cij_road_CAMKOX.shape
        model = QUANTJobsModel(m, n)
        model.setAttractorsAj(HHAttractors, 'zonei', 'N_of_Dwellings')
        model.setPopulationEi(jobs, 'zonei', 'employment_tot')
        model.setCostMatrixCij(cij_road_CAMKOX, cij_bus_CAMKOX, cij_rail_CAMKOX)

        Tij, cbar_k = model.run3modes_NoCalibration(Beta_calibrated)
        # Compute the probability of a flow from an MSOA zone to any (i.e. all) of the possible point zones.
        jobs_probTij = model.computeProbabilities3modes(Tij)

        # Jobs accessibility:
        DjPred_road = Tij[0].sum(axis=1)
        Ji_road = Calculate_Job_Accessibility(DjPred_road, cij_road_CAMKOX)

        DjPred_bus = Tij[1].sum(axis=1)
        Ji_bus = Calculate_Job_Accessibility(DjPred_bus, cij_bus_CAMKOX)

        DjPred_rail = Tij[2].sum(axis=1)
        Ji_rail = Calculate_Job_Accessibility(DjPred_rail, cij_rail_CAMKOX)

        # Save output:
        Jobs_accessibility_df = pd.DataFrame({'areakey': CAMKOX_MSOA_list, 'JAcar50': Ji_road, 'JAbus50': Ji_bus, 'JArail50': Ji_rail})
        Jobs_accessibility_df.to_csv(outputs["NS_JobsAccessibility2050"])

        # Housing Accessibility:
        OiPred_road = Tij[0].sum(axis=0)
        Hi_road = Calculate_Housing_Accessibility(OiPred_road, cij_road_CAMKOX)

        OiPred_bus = Tij[1].sum(axis=0)
        Hi_bus = Calculate_Housing_Accessibility(OiPred_bus, cij_bus_CAMKOX)

        OiPred_rail = Tij[2].sum(axis=0)
        Hi_rail = Calculate_Housing_Accessibility(OiPred_rail, cij_bus_CAMKOX)

        # Save output:
        Housing_accessibility_df = pd.DataFrame({'areakey': CAMKOX_MSOA_list, 'HAcar50': Hi_road, 'HAbus50': Hi_bus,'HArail50': Hi_rail})
        Housing_accessibility_df.to_csv(outputs["NS_HousingAccessibility2050"])

        # Create a Oi Dj table
        jobs['DjPred_Car_50'] = Tij[0].sum(axis=1)
        jobs['DjPred_Bus_50'] = Tij[1].sum(axis=1)
        jobs['DjPred_Rail_50'] = Tij[2].sum(axis=1)
        jobs['DjPred_Tot_50'] = Tij[0].sum(axis=1) + Tij[1].sum(axis=1) + Tij[2].sum(axis=1)
        jobs['OiPred_Car_50'] = Tij[0].sum(axis=0)
        jobs['OiPred_Bus_50'] = Tij[1].sum(axis=0)
        jobs['OiPred_Rail_50'] = Tij[2].sum(axis=0)
        jobs['OiPred_Tot_50'] = Tij[0].sum(axis=0) + Tij[1].sum(axis=0) + Tij[2].sum(axis=0)
        jobs['Job_accessibility_roads'] = Jobs_accessibility_df['JAcar50']
        jobs['Jobs_accessibility_bus'] = Jobs_accessibility_df['JAbus50']
        jobs['Jobs_accessibility_rail'] = Jobs_accessibility_df['JArail50']
        jobs['Housing_accessibility_roads'] = Housing_accessibility_df['HAcar50']
        jobs['Housing_accessibility_bus'] = Housing_accessibility_df['HAbus50']
        jobs['Housing_accessibility_rail'] = Housing_accessibility_df['HArail50']
        jobs.to_csv(outputs["NS_JobsDjOi2050"])


        # Save output matrices
        print("Saving output matrices...")

        # Probabilities:
        np.savetxt(outputs["NS_JobsProbTijRoads2050"], jobs_probTij[0], delimiter=",")
        np.savetxt(outputs["NS_JobsProbTijBus2050"], jobs_probTij[1], delimiter=",")
        np.savetxt(outputs["NS_JobsProbTijRail2050"], jobs_probTij[2], delimiter=",")

        # People flows
        np.savetxt(outputs["NS_JobsTijRoads2050"], Tij[0], delimiter=",")
        np.savetxt(outputs["NS_JobsTijBus2050"], Tij[1], delimiter=",")
        np.savetxt(outputs["NS_JobsTijRail2050"], Tij[2], delimiter=",")

        # Geojson flows files - arrows
        flow_zonecodes = pd.read_csv(inputs["ZonesCoordinates"])
        flow_car = flowArrowsGeoJSON(Tij[0], flow_zonecodes)
        with open(outputs["NS_ArrowsFlowsCar2050"], 'w') as f:
            dump(flow_car, f)
        flow_bus = flowArrowsGeoJSON(Tij[1], flow_zonecodes)
        with open(outputs["NS_ArrowsFlowsBus2050"], 'w') as f:
            dump(flow_bus, f)
        flow_rail = flowArrowsGeoJSON(Tij[2], flow_zonecodes)
        with open(outputs["NS_ArrowsFlowsRail2050"], 'w') as f:
            dump(flow_rail, f)

        print("JtW model", Scenario, " cbar [roads, bus, rail] = ", cbar_k)

        # Calculate predicted population
        DjPred = np.zeros(n)
        for k in range(len(Tij)):
            DjPred += Tij[k].sum(axis=1)
        # Create a dataframe with Zone and people count
        DjPred = pd.DataFrame(DjPred, columns=['population'])
        DjPred['zonei'] = CAMKOX_MSOA_list

        end = time.perf_counter()
        print("Journey to work model run elapsed time (secs)=", end - start)
        # print("Journey to work model run elapsed time (mins)=", (end - start) / 60)
        print()

        return Beta_calibrated, DjPred
 
    
def Calculate_Job_Accessibility(DjPred, cij):
    # Job accessibility is the distribution of population around a job location.

    Ji = np.zeros(len(DjPred))
    for i in range(len(Ji)):
        for j in range(len(Ji)):
            Ji[i] += DjPred[j] / (cij[i, j] * cij[i, j])  # DjPred is residential totals

    # now scale to 100
    Sum = 0
    for i in range(len(Ji)): Sum += Ji[i]
    for i in range(len(Ji)): Ji[i] = 100.0 * Ji[i] / Sum
    return Ji

def Calculate_Housing_Accessibility(OiPred, cij):
    # Housing accessibility is the distribution of jobs around a housing location.

    Hi = np.zeros(len(OiPred))

    # Calculate housing accessibility for public transport
    for i in range(len(Hi)):
        for j in range(len(Hi)):
            Hi[i] += OiPred[j] / (cij[i, j] * cij[i, j])  # OiPred_pu is employment totals

    # now scale to 100
    Sum = 0
    for i in range(len(Hi)): Sum += Hi[i]
    for i in range(len(Hi)): Hi[i] = 100.0 * Hi[i] / Sum
    return Hi

################################################################################
# END OF MAIN PROGRAM                                                          #
################################################################################


