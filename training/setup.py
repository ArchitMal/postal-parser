import csv
import os
import nltk

ROOT_FOLDER_NAME = '../../structured_data/testdata'
OUT_FILE_NAME = '../data/test_CoNLL_addresses.txt'
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


def parse_dir(root_location, delimiter=',', level=0, parent_info=[]):
    # really gross recursive function that goes through all files and subfolders
    # then processes each csv into the list of dictionaries

    dir_contents = next(os.walk(root_location))
    sub_directories = dir_contents[1]
    files = dir_contents[2]

    #TODO: Fix Level_labels to reflect the actual relevant label
    level_labels = ['country', 'state', 'city']

    # RECURSIVE STATE: parse through all sub-directories recursively
    all_addresses = []
    for sub_dir in sub_directories:
        folder_name = root_location + '/' + sub_dir
        label = level_labels[level]
        parents = parent_info +[{'label': label, 'value': sub_dir}]
        folder_addresses = parse_dir(folder_name, delimiter=delimiter, level=level+1,parent_info=parents)
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
    # TODO: how to assign values from parent_info alreaady in headers (eg. state/region)
    out_list = []
    with open(file_location, newline='') as file:
        reader = csv.reader(file, delimiter=delimiter)
        headers = next(reader)
        for row in reader:
            line = [{'label': OA_TO_LIBPOSTAL[headers[i]], 'value':row[i]} for i in range(len(row))]
            for parent in parent_info:
                if parent['label'] == 'state':
                    line[7] = parent    #watch this hardcode, pulls the column which has province/region in it
                else:
                    line.append(parent)

            out_list.append(line)
    return out_list

    
# ///////////////////////////////////////////////////////////////////////////////////////
#   STEP 2
#   Owner: Archi & Ian
#   description: takes the dict and enters it into OpenCage to generate the sentence as would be entered by human

#   Parameters
#      csv_dict:   the dictionary created by read_csv()
#      return:     returns opencage generated string
#      eg output:  123 [house number] Main Street [road] Toronto [city] Ontario [state] M1V 3N2 [postcode] Canada [country]
def run_open_cage(csv_dict):
    '''
    Converts csv_dict, a list of dictionaries, into a readable address
    string. For now, this keeps all pieces of information.

    >>>sample = [{'value': '123','label':'house_number'},
    {'value':'Main Street','label':'road'}]
    >>>run_open_cage(sample)
    123 [house_number] Main Street [road]

    '''
    address_string = ''

    given_labels = ('house', 'level', 'unit', 'po_box', 'house_number',
                    'road', 'near',  'city', 'suburb', 'city_district',
                    'state_district', 'state', 'postcode',
                    'country_region', 'country', 'lon', 'lat', 'id', 'hash')

    for i in range(len(given_labels)):
        counter = 0
        while counter < len(csv_dict):
            if csv_dict[counter]['label'].lower() == given_labels[i]:
                address_string = address_string + " " \
                                 + csv_dict[counter]['value']\
                                 + " [" + csv_dict[counter]['label'] + "]"
                break
            else:
                counter += 1

    return address_string.strip()

#   Owner: Archi & Ian
#   Description: Sorts csv_dict to create a list of dictionaries such that they are in the same order they would be in an address string written by a human.
#   Parameters
##      csv_dict:   the dictionary created by read_csv()
##      return:     returns sorted list of csv_dict according to label placement

def address_sorter(csv_dict):
    '''
    Sorts csv_dict to create a list of dictionaries such that they are in the
    same order they would be in an address string written by a human.

    >>>sample = [{'value':'Main Street','label':'road'},
    {'value': '123','label':'house_number'}]
    >>>address_sorter(sample)
    [{'value': '123', 'label': 'house_number'},
     {'value': 'Main Street', 'label': 'road'}]

    '''

    address_list = []

    given_labels = ('house', 'level', 'unit', 'po_box', 'house_number',
                    'road', 'near', 'city', 'suburb', 'city_district',
                    'state_district', 'state', 'postcode',
                    'country_region', 'country', 'lon', 'lat', 'id', 'hash')

    for i in range(len(given_labels)):
        counter = 0
        while counter < len(csv_dict):
            if csv_dict[counter]['label'].lower() == given_labels[i]:
                address_list.append(csv_dict[counter])
                break
            else:
                counter += 1

    return address_list
    
#///////////////////////////////////////////////////////////////////////////////////////
#   STEP 3
#   Owner: Mona & Saira
#   description: takes lists from zip_lists and for each cage string, looks at the hash of word->tag and assigns the correct tag to that word, formatting all into a string to be put into a file
#
#   Parameters
##      zipped_lists:  output from zip_lists(), list of touples with the human string and the map of word->tag
##      return:     returns finished string of all items to be written to file
##      eg output:  "DOCTYPPE -X- -X- -0-\n3a NPP NPP B-Unit\nMain NPP NPP B-Street\nSt. NPP NPP I-Street ... "


def NER_tags(address):
    tags ={}
    for part in address:
        tokens = part['value'].split(' ')
        for i in range(len(tokens)):
            if i == 0:
                tags[tokens[i]] = 'B-' + part['label']
            else:
                tags[tokens[i]] = 'I-' + part['label']
    return tags

def tokenize(address):
    tokens = []
    for part in address:
        tokens= tokens + part['value'].split(' ')
    return tokens


###ADD POS tagging formula here ###
def POS_tags(tokens):
        tagged=nltk.pos_tag(tokens)
                
        return tagged

#   Owner: Mona & Saira
#   description: just writes the output of the above to a file
#
#   Parameters
##      FILE_NAME:  root file location
##      return:     n/a
##      eg output:  complete CONLL file

def to_CoNLL(address):
    tokens = tokenize(address)
    tags = NER_tags(address)
    pos = POS_tags(tokens)
    conll=''
    for i in range(len(tokens)):
        conll =conll+ '{} {} {} {} \n'.format(tokens[i], pos[i][1], pos[i][1], tags[tokens[i]])
    return conll

def write_CONLL_file(all_lines):
    file = open(OUT_FILE_NAME, 'w+')
    conll = '-DOCSTART- -X- -X- O \n'
    file.write(conll)
    for address in all_lines:
        file.write(to_CoNLL(address))
        file.write('\n')
    file.close()




#Just so you all can see the logic

def main():
    csv_dict = parse_dir(ROOT_FOLDER_NAME)
    cage_strings = [address_sorter(line) for line in csv_dict]
    write_CONLL_file(cage_strings)

main()