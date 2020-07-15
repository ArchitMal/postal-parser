import nltk
import re
GIVEN_LABELS = ('house', 'level', 'unit', 'po_box', 'house_number',
                'road', 'near',  'city', 'suburb', 'city_district',
                'state_district', 'state', 'postcode',
                'country_region', 'country', 'lon', 'lat', 'id', 'hash')


class Address:
    # Representation of a structured address for development of training data

    def __init__(self, dictionary, order=GIVEN_LABELS):
        # Description: Builds Address object from a list of dictionaries
        #   Parameter: dictionary
        #       takes in a list of dictionaries of the form
        #       [{'label': ____, 'value': ____},...]
        #   Parameter: order
        #       A tuple or list of lib postal labels (as strings)
        #       in the order expected for the unstructured address
        self.address_dict = dictionary
        self.order = order
        self.ordered = False

    def __str__(self):
        # Description: Converts the class to a string, checks if ordered before returning
        if not self.ordered:
            self.order_address(self.order)
        accum_string = ''
        for value in self.address_dict:
            accum_string += value['value']
            accum_string += ' '
        return accum_string.strip()

    def order_address(self):
        # Description: Sorts csv_dict to create a list of dictionaries
        #   such that they are in the same order they would be in an
        #   address string written by a human.  Uses the order stored in class
        address_list = []
        for i in range(len(self.order)):
            counter = 0
            while counter < len(self.address_dict):
                if self.address_dict[counter]['label'].lower() == self.order[i]:
                    address_list.append(self.address_dict[counter])
                    break
                else:
                    counter += 1
        self.address_dict = address_list
        self.ordered = True
    
    def make_randomized_order():
       order = ('level', 'unit', 'po_box', 'house',
                'road', 'near',  'city', 'suburb', 'city_district',
                'state_district', 'state', 'postcode',
                'country_region', 'country', 'lon', 'lat', 'id', 'hash')
      
      
    def change_default_order(self):
       order=make_randomized_order()
       self.order = order
      
      
    def to_conll(self):
        # Description: Takes the address in the order stored and develops the CONLL
        #   representation of the address
        tokens = self._tokenize()
        tags = self._ner_tags()
        pos = self._pos_tags(tokens)
        conll = ''
        for i in range(len(tokens)):
            token_val = tokens[i]
            pos_val = pos[i][1]
            tag_val = tags[token_val]
            conll = conll + '{} {} {} {} \n'.format(token_val, pos_val, pos_val, tag_val)
        return conll

    def _ner_tags(self):
        tags = {}
        for part in self.address_dict:
            value = part['value'].split(' ')
            tokens = []
            tokens = tokens + [word for word in value if word]
            for i in range(len(tokens)):
                if i == 0:
                    tags[tokens[i]] = 'B-' + part['label']
                else:
                    tags[tokens[i]] = 'I-' + part['label']
        return tags

    def _tokenize(self):
        tokens = []
        for part in self.address_dict:
            value = re.split(' |_', part['value'])
            tokens = tokens + [word for word in value if word]
        return tokens

    def _pos_tags(self, tokens):
        tagged = nltk.pos_tag(tokens)
        return tagged
