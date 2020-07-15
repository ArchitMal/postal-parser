import nltk
import re
import random
GIVEN_LABELS = ('house', 'level', 'unit', 'po_box', 'house_number',
                'road', 'near',  'city', 'suburb', 'city_district',
                'state_district', 'state', 'postcode',
                'country_region', 'country', 'lon', 'lat', 'id', 'hash')
shuffle=True


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
        
    @staticmethod 
    def add_delete_randomly_tags(add):
      if add is True:
        #randomly duplicate one of tags
        order= tuple([GIVEN_LABELS[x] for x in range(1, random.randrange(1,15))])+GIVEN_LABELS
      else:
        deleted_tags=[GIVEN_LABELS[x] for x in range(1, random.randrange(2,5))]
        order = tuple([x for x in GIVEN_LABELS if x not in deleted_tags])
      return order
        
      
    @staticmethod 
    def make_randomized_order():
       if shuffle is True:
          order = tuple(random.sample(t, len(t)))
       else:
          r=random.randint(0,3)
          if r==1:
            order=('house_number','road', 'near',  'city', 'suburb', 'city_district',
                  'state_district', 'state', 'postcode','house', 'level', 'unit', 'po_box',
                  'country_region', 'country', 'lon', 'lat', 'id', 'hash')
          if r==2:
            order=('house', 'house_number','po_box', 'road', 'near',  'city', 'suburb','house_number', 'city_district',
                  'state_district', 'state', 'postcode', 'level', 'unit', ,
                  'country_region', 'country', 'lon', 'lat', 'id', 'hash')
          if r==3:
            add=True
            order=add_delete_randomly_tags(add)
       return order
      
    def change_default_order(self):
       new_order=make_randomized_order()
       self.order = new_order
      
      
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
