import csv
import os
import nltk

ROOT_FOLDER_NAME = '../../structured_data/testdata'
OUT_FILE_NAME = '../data/CoNLL_addresses.txt'
COUNTRY_FILE_NAME = 'countrywide.csv'
OA_TO_LIBPOSTAL = {'LAT': '',
                   'LON': '',
                   'NUMBER': 'house_number',
                   'STREET': 'road',
                   'UNIT': 'unit',
                   'CITY': 'city',
                   'DISTRICT': 'state_district',
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
    level_labels = ['country', 'state', 'state_district','city','city_district']

    # RECURSIVE STATE: parse through all sub-directories recursively
    all_addresses = []
    for sub_dir in sub_directories:
        folder_name = root_location + '/' + sub_dir
        label = OA_TO_LIBPOSTAL[level_labels[level]]
        parents = parent_info +[{'label': label, 'value': sub_dir}]
        folder_addresses = parse_dir(folder_name, delimiter=delimiter, level=level+1,parent_info=parents)
        all_addresses += folder_addresses

    # BASE CASE: parse through all files in directory
    for file in files:
        if len(file) > 3 and file[-4:] == '.csv':
            file_location = root_location + '/' + file
            label = OA_TO_LIBPOSTAL[level_labels[level]]
            parents = parent_info + [{'label': label, 'value': file[:-4]}]
            file_addresses = read_csv(file_location, delimiter, parent_info=parents)
            all_addresses += file_addresses
    return all_addresses


def read_csv(file_location, delimiter, parent_info=[]):
    # Opens a .csv file at location file_location and adds converts each line into a list of dictionaries
    # TODO: how to assign values from parent_info alreaady in headers (eg. state/region)
    out_list = []
    with open(file_location, newline='') as file:
        reader = csv.reader(file, delimiter=delimiter)
        headers = next(reader)
        for row in reader:
            line = [{'label': OA_TO_LIBPOSTAL[headers[i]], 'value':row[i]} for i in range(len(row))]
            [line.append(parent) for parent in parent_info]
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
    address_string = ""

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
def tokenize(address_str):
    '''Takes the address str and outputs list of ordered tokens in the address'''
    
    clean_add = address_str.replace(',', " ")
    tokens_list = clean_add.split(' ')
    
    return tokens_list

def NER_tags(address_dict, address_str):
    '''Takes the address dict of form {token:tag} and outputs a dict of form {token:BIO tag}'''
    NER ={}
    for key in address_dict:
        tokens = key.split(" ")
        for i in range(len(tokens)):
            if i == 0:
                NER[tokens[i]] = 'B-' + address_dict[key]
            else:
                NER[tokens[i]] = 'I-' + address_dict[key]
    tokens=tokenize(address_str)
    for token in tokens:
        if token not in address_dict.keys():
            NER[token]='O'
    
    return NER

###ADD POS tagging formula here ###
def POS_tags(tokens):
    
    tagged=nltk.pos_tag(tokens)
    return dict(tagged)

#   Owner: Mona & Saira
#   description: just writes the output of the above to a file
#
#   Parameters
##      FILE_NAME:  root file location
##      return:     n/a
##      eg output:  complete CONLL file

def write_CONLL_file(zipped_lists):
    '''Takes zipped addresses and writes a CoNLL format file '''
    OutDIR = 'CoNLL_addresses.txt'
    file = open(OutDIR, "w+")
    for address in zipped_lists:
        add_str, add_dict = address
        tokens = tokenize(add_str)
        tags = NER_tags(add_dict,add_str)
        pos = POS_tags(tokens) # change to pos tagging formula here
        i = 0
        
        file.write('-DOCSTART- -X- -X- O \n')
        for token in tokens: 
            print()
        for token in tokens:
            file.write('{} {} {} {} \n'.format(token, pos[token], pos[token], tags[token]))
        
        file.write('\n')
    file.close()



#Just so you all can see the logic

def main():
    csv_dicts = parse_dir(ROOT_FOLDER_NAME)
    cage_dicts = run_open_cage(csv_dicts)
    write_CONLL_file(cage_dicts)
