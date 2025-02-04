#!/usr/bin/env python
# coding: utf-8

# ## Getting a zip distance matrix for easy lookup

# Necessary Imports

import os
import pandas as pd
import numpy as np
import mpu
import json

import warnings
warnings.filterwarnings("ignore")

# Helper functions
def walk_up_folder(path, depth=1):
    """
    Helper method to navigate the file system and get to the file location
    """
    _cur_depth = 1
    while _cur_depth < depth:
        path = os.path.dirname(path)
        _cur_depth += 1
    return path

def geodist(coord1,coord2):
    """
    Calculate the distance between
    (lat1, lon1), (lat2, lon2)
    """
    # Convert to miles 1km = 0.621371 miles
    return round(mpu.haversine_distance(coord1,coord2)*0.621371,2)

def fill_lfromu(A):
    """
    Fill out the symmetric values in the lower triangle based on upper
    Not needed since it is covered in the for loop above
    """
    out = A.T + A
    np.fill_diagonal(out,0)
    return out

import numba as nb
#@nb.njit(parallel=True,fastmath=True)
def func(len_matrix,coordinates):
    zip_dist = np.zeros((len_matrix, ) * 2)
    indices = np.arange(len_matrix)
    # Get upper triangular pairs
    fill_cells = np.stack(np.triu_indices(len_matrix), axis=1)
    # Loop through upper triangular indices while avoiding diagonal element indices
    for idx in fill_cells:
        i,j = indices[idx]
        if i!=j:
            zip_dist[i][j]= zip_dist[j][i] = geodist(coordinates[i],coordinates[j])
    return zip_dist

# ## Loading raw data
# 
# Source - https://github.com/symerio/postal-codes-data/blob/master/data/geonames/US.txt 
# 
# **Geocoding format**
# The result of a geo-localistion query is a pandas.DataFrame with the following columns,
# 
# country_code: iso country code, 2 characters  
# postal_code : postal code  
# place_name : place name (e.g. town, city etc)  
# state_name : 1. order subdivision (state)  
# state_code : 1. order subdivision (state)  
# county_name : 2. order subdivision (county/province)  
# county_code : 2. order subdivision (county/province)  
# community_name : 3. order subdivision (community)  
# community_code : 3. order subdivision (community)  
# latitude : estimated latitude (wgs84)  
# longitude : estimated longitude (wgs84)  
# accuracy : accuracy of lat/lng from 1=estimated to 6=centroid  


if __name__ =="__main__":
    
    data_dir = os.path.join(walk_up_folder(os.getcwd(), 2), "Data/")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print("Data folder created")
        
    # Load USZips data
    source_file = os.path.join(data_dir,"US_zips.txt")
    if os.path.exists(source_file):
        print("Loading the source file")
        print("Processing the dataframe")
        zip_df = pd.read_csv(source_file),sep='\t',header=None,
                             names=["country_code","postal_code","place_name","state_name","state_code",
                                    "county_name","county_code","community_name","community_code",
                                    "latitude","longitude","accuracy"])

        # Dropping unnecessary columns
        zip_df.drop(["country_code","place_name","state_name","county_name","county_code","community_name","community_code"],axis=1,inplace=True)
        # There were 2 duplicate instances
        zip_df.drop_duplicates(subset=["postal_code"],keep='last',inplace=True)
        # Coordinate column as (lat,long)
        zip_df["coord"]=list(zip(zip_df["latitude"],zip_df["longitude"]))
        zip_df["mapping"] = zip_df.index # Column with index

        # ## Lookup Matrix
        #
        # The idea is to form a (41483,41483) matrix where the cell values are the haversize distances between two zips that are indexed.
        # I'll save the index look up and the matrix file as json or pkl


        # Dictionary mapping the zipcode to index
        zip_index = dict(zip(zip_df["postal_code"].astype(str),zip_df["mapping"]))
        print(len(zip_index))
        # Saving the indexer
        with open(os.path.join(data_dir, "zips_indexer.json")), 'w') as f:
            json.dump(zip_index, f)
        print("ZiptoIndex json saved!")
        
        # Matrix
        len_matrix = zip_df.shape[0]
        coordinates = zip_df.coord.values
        
        print("Creating the pairwise distance matrix! This might take an hour, why don't you go get something to eat? ")
        # Takes 1hour. Unfortunately numba.jit doesn't work with user defined functions ")
        zip_dist = func(len_matrix,coordinates)
        # Convert to float32
        print("ZipDist Matrix saving!")
        np.savez_compressed(os.path.join(data_dir, "zip_dist.npz")), np.float32(zip_dist))
    else:
        print("Please ensure you have the source file of the raw zips data in the Data directory and try again !")


