import csv
import os
from training.address import Address
import pyspark as ps


ROOT_FOLDER_NAME = '../../structured_data/testdata'
OUT_FILE_NAME = '../data/sample_test_data.csv'
OA_TO_LIBPOSTAL = {'LAT': '',
                   'LON': '',
                   'NUMBER': 'house_number',
                   'STREET': 'road',
                   'UNIT': 'unit',
                   'CITY': 'city',
                   'DISTRICT': '',
                   'REGION': 'state',
                   'POSTCODE': 'postcode',
                   'ID': '',
                   'HASH': ''}
# ///////////////////////////////////////////////////////////////////////////////////////
#   STEP 1
#   Owner: Archi & Ian
#   description: takes root data location and processes data into dictionary
#
#   Parameters
#      FILE_NAME:  root file location
#      return:     returns list of dictionaries with keys matching opencage
#      eg output:  [{'houseNumber': '3a', 'road': 'Main St.', 'neighborhood': '', 'city': 'Toronto', 'county':...]

def parse_dir(root_location, country, delimiter=','):
    dir_contents = next(os.walk(root_location))
    sub_directories = dir_contents[1]

    label = 'country'
    parents = [{'label': label, 'value': country}]

    all_addresses = __parse_dir(root_location,delimiter,0,parents)
    return all_addresses

def __parse_dir(root_location, delimiter, level, parent_info):
    # really gross recursive function that goes through all files and subfolders
    # then processes each csv into the list of dictionaries

    dir_contents = next(os.walk(root_location))
    sub_directories = dir_contents[1]
    files = dir_contents[2]

    #TODO: Fix Level_labels to reflect the actual relevant label
    level_labels = ['state', 'city']

    # RECURSIVE STATE: parse through all sub-directories recursively
    all_addresses = []
    for sub_dir in sub_directories:
        folder_name = root_location + '/' + sub_dir
        label = level_labels[level]
        parents = parent_info +[{'label': label, 'value': sub_dir}]
        folder_addresses = __parse_dir(folder_name, delimiter=delimiter, level=level+1,parent_info=parents)
        all_addresses += folder_addresses

    # BASE CASE: parse through all files in directory
    for file in files:
        if len(file) > 3 and file[-4:] == '.csv':
            file_location = root_location + '/' + file
            label = level_labels[level]
            parents = parent_info + get_info_from_file_name(label,file)
            file_addresses = read_csv(file_location, delimiter, parent_info=parents)
            all_addresses += file_addresses
    return all_addresses

def get_info_from_file_name(label, file_name):
    # Takes in a .csv filename and pulls out the relevent inormation for the address if there is any
    clean_file_name = file_name.replace('.csv','').replace('city_of_','').replace('municipality_of_','')
    if clean_file_name == 'countrywide' or clean_file_name == 'statewide':
        return []
    return [{'label': label, 'value': clean_file_name}]

def read_csv(file_location, delimiter, parent_info=[]):
    # Opens a .csv file at location file_location and adds converts each line into a list of dictionaries
    out_list = []
    with open(file_location, newline='') as file:
        reader = csv.reader(file, delimiter=delimiter)
        headers = next(reader)
        for row in reader:
            line = []
            for i in range(len(row)):
                label = OA_TO_LIBPOSTAL[headers[i]]
                value = row[i]
                if value and label:
                    line.append({'label': label, 'value': value})
            for parent in parent_info:
                line.append(parent)
            out_list.append(Address(line))
    return out_list


def write_csv(file_name, addresses):
    with open(file_name, 'w') as file:
        [file.write(str(address) + '\n') for address in addresses]

def to_spark():
  """
  Reads CSV into Spark Dataframe. Can replace the location of the local file with the gcp bucket location.
  More details can be found https://cloud.google.com/dataproc/docs/tutorials/gcs-connector-spark-tutorial
  
  """
    spark = ps.sql.SparkSession.builder.\
        master('local').\
        appName('Postal Parser').\
        getOrCreate()
    address_df = spark.read.csv('../data/sample_test_data.csv', header=True, inferSchema=True)
    return address_df

def main():
    dir_contents = next(os.walk(ROOT_FOLDER_NAME))
    sub_directories = dir_contents[1]
    accum = []
    for sub_dir in sub_directories:
        directory = ROOT_FOLDER_NAME+ '/'+sub_dir
        csv_lists = parse_dir(directory,sub_dir)
        accum += csv_lists
    write_csv(OUT_FILE_NAME, accum)
    to_spark()
main()
