
# Archi & Ian
FILE_NAME = '../data/sample_of_toronto.csv'

"""
Example of .csv file:

LON,    LAT,    NUMBER, STREET,     UNIT,   CITY,       DISTRICT,   REGION, POSTCODE,   ID, HASH
-49.41, 29.523, 52,     Main St.,   3a,     Toronto,    ,           ON,     N6C4E9,     ,   529a2b19a...
-50.1,  -23.1,  9,      South St.,  ,       Rio,        ,           BR,     12345,      ,   21203asf124...

(csv files are separated into country folders, so that will be added in afterwards)
"""

#///////////////////////////////////////////////////////////////////////////////////////
#   STEP 1
#   Owner: Archi & Ian
#   description: takes root data location and processes data into dictionary
#
#   Parameters
##      FILE_NAME:  root file location
##      return:     returns list of dictionaries with keys matching opencage
##      eg output:  [{'houseNumber': '3a', 'road': 'Main St.', 'neighborhood': '', 'city': 'Toronto', 'county':...]
def read_csv(root_location):
    pass
    

#   Owner: Archi & Ian
#   description: basically takes the dict and flips it around so that the words point to their tag rather than vice verca.
#   Adding in because Archi and Ian got worried about runtime
#   return: dict mapping entity to its relating tag.
#   eg output:  [{'3a': 'houseNumber', 'Main' : 'road', 'St.' : 'road' ....}, {...}, ... ]
def dict_to_hash(csv_dict)
    csv_dict_flipped = {value:key for key, value in csv_dict.items()}
    return csv_dict_flipped
    
    
    
    
#///////////////////////////////////////////////////////////////////////////////////////
#   STEP 2
#   Owner: Archi & Ian
#   description: takes the dict and enters it into OpenCage to generate the overall sentance as would be entered by human
#
#   Parameters
##      csv_dict:   the dictionary created by read_csv()
##      return:     returns list of opencage generated strings
##      eg output:  ["52 Main St., Unit 3a, Toronto, ON, N6C 4E9","9 South St., Rio BR, 12345",...]
def run_open_cage(csv_dict):
    pass
    
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
def zip_lists(cage_strings,word_hash):
    pass
    
    
    
    
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
    
    clean_add = address.str.replace(',', "")
    tokens_list = clean_add.split(' ')
    return tokens_list

def NER_tags(address_dict):
    '''Takes the address dict of form {token:tag} and outputs a dict of form {token:BIO tag}'''
    NER ={}
    for key in address_dict:
        tokens = key.split(" ")
        for i in range(len(tokens)):
            if i == 0:
                NER[tokens[i]] = 'B-' + address_dict[key]
            else:
                NER[tokens[i]] = 'I-' + address_dict[key]
    return NER

###ADD POS tagging formula here ###
def POS_tags(address_dict):
    
        
        keys=list(address_dict.keys())
        
        tagged.append(nltk.pos_tag(keys))
        return tagged



#   Owner: Mona & Saira
#   description: just writes the output of the above to a file
#
#   Parameters
##      FILE_NAME:  root file location
##      return:     n/a
##      eg output:  complete CONLL file

def write_CONLL_file(zipped_lists):
    '''Takes zipped addresses and writes a CoNLL format file '''
    
    file = open(OutDIR, "w+")
    for address in zipped_list:
        add_str, add_dict = address
        tokens = tokenize(add_str)
        tags = NER_tags(add_dict)
        pos = POS_tags(add_dict) # change to pos tagging formula here
        i = 0
        file.write('-DOCSTART- -X- -X- O \n')
        for token in tokens:
        file.write('{} {} {} {} \n'.format(token, pos[i], pos[i], tags[token]))
    
        file.write('\n')
    file.close()

#Just so you all can see the logic

OutDIR = 'CoNLL_addresses.txt'

def main():
    csv_dict = read_csv(FILE_NAME)
    word_hash = dict_to_hash(csv_dict)
    cage_strings = run_open_cage(csv_dict)
    zipped_lists = zip_lists(cage_strings, word_hash)
    write_CONLL_file(zipped_lists)
