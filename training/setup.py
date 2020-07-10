import csv
import os

FILE_NAME = 'test.csv'
OUT_FILE_NAME = '../data/CoNLL_addresses.txt'
COUNTRY_FILE_NAME = 'countrywide.csv'

"""
Example of .csv file:

LON,    LAT,    NUMBER, STREET,     UNIT,   CITY,       DISTRICT,   REGION, POSTCODE,   ID, HASH
-49.41, 29.523, 52,     Main St.,   3a,     Toronto,    ,           ON,     N6C4E9,     ,   529a2b19a...
-50.1,  -23.1,  9,      South St.,  ,       Rio,        ,           BR,     12345,      ,   21203asf124...

(csv files are separated into country folders, so that will be added in afterwards)
"""

# ///////////////////////////////////////////////////////////////////////////////////////
#   STEP 1
#   Owner: Archi & Ian
#   description: takes root data location and processes data into dictionary
#
#   Parameters
#      FILE_NAME:  root file location
#      return:     returns list of dictionaries with keys matching opencage
#      eg output:  [{'houseNumber': '3a', 'road': 'Main St.', 'neighborhood': '', 'city': 'Toronto', 'county':...]


def read_all_csvs(root_location, delimiter=','):
    # parses through all csv's from the root data folder location
    dir_contents = next(os.walk(root_location))
    sub_directories = dir_contents[1]

    all_addresses = []
    for sub_dir in sub_directories:
        folder_name = root_location + '/' + sub_dir
        country_addresses = parse_country_dir(folder_name, sub_dir, delimiter)
        all_addresses += country_addresses
    return all_addresses


def parse_country_dir(folder_location, country_name, delimiter):
    # walks through the country folders, looks for countrywide.csv and calls read_csv() on it
    country_file_name = COUNTRY_FILE_NAME
    dir_contents = next(os.walk(folder_location))
    files = dir_contents[2]

    if country_file_name in files:
        file_name = folder_location + '/' + country_file_name
        out_list = read_csv(file_name, delimiter, country_name)
        return out_list
    return []


def read_csv(file_location, delimiter, country=''):
    # Opens a .csv file at location file_location and adds converts each line into a list of dictionaries
    out_list = []
    with open(file_location, newline='') as file:
        reader = csv.reader(file, delimiter=delimiter)
        headers = next(reader)
        for row in reader:
            line = [{'label': headers[i], 'value':row[i]} for i in range(len(row))]
            line.append({'label': 'Country', 'value': country})
            out_list.append(line)
    return out_list


#   Owner: Archi & Ian
#   description: takes the dict and flips it around so that the words point to their tag rather than vice verca.
#   Adding in because Archi and Ian got worried about runtime
#   return: dict mapping entity to its relating tag.
#   eg output:  [{'3a': 'houseNumber', 'Main' : 'road', 'St.' : 'road' ....}, {...}, ... ]
#def dict_to_hash(csv_dict):
#    csv_dict_flipped = {value:key for key, value in csv_dict.items()}
#    return csv_dict_flipped
    
    
    
    
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


#   Owner: Archi & Ian
#   description: literally runs numpy.zip on the lists generated by run_open_cage() and dict_to_hash(), turning them into a (using Java notation, sorry) List<Touple<String, Dict<String, String>>>
#
#   Parameters
##      cage_strings:   output from run_open_cage() containing the list of all the strings
##      word_hash:      output from dict_to_hash(), containing the list of all of the dictionaries for each string
##      return:         returns one list with touples containing the elements from cage_strings and word_hash with matching indicies
##      eg output:  [("52 Main St., Unit 3a, Toronto, ON, N6C 4E9", {'3a': 'houseNumber', 'Main' : 'road', 'St.' : 'road' ....}),
#                    ("9 South St., Rio BR, 12345",{...}),
#                        ...]
#def zip_lists(cage_strings,word_hash):
#    pass
    
    
    
    
#///////////////////////////////////////////////////////////////////////////////////////
#   STEP 3
#   Owner: Mona & Saira
#   description: takes lists from zip_lists and for each cage string, looks at the hash of word->tag and assigns the correct tag to that word, formatting all into a string to be put into a file
#
#   Parameters
##      zipped_lists:  output from zip_lists(), list of touples with the human string and the map of word->tag
##      return:     returns finished string of all items to be written to file
##      eg output:  "DOCTYPPE -X- -X- -0-\n3a NPP NPP B-Unit\nMain NPP NPP B-Street\nSt. NPP NPP I-Street ... "
import nltk
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
    csv_dict = read_csv(FILE_NAME)
    word_hash = dict_to_hash(csv_dict)
    cage_strings = run_open_cage(csv_dict)
    zipped_lists = zip_lists(cage_strings, word_hash)
    write_CONLL_file(zipped_lists)
