import nltk
GIVEN_LABELS = ('house', 'level', 'unit', 'po_box', 'house_number',
                'road', 'near',  'city', 'suburb', 'city_district',
                'state_district', 'state', 'postcode',
                'country_region', 'country', 'lon', 'lat', 'id', 'hash')


class Address:
    # takes in a list of dictionaries of the form [{'label': ____, 'value': ____},...]
    def __init__(self, dictionary, order=GIVEN_LABELS):
        self.address_dict = dictionary
        self.order = order
        self.ordered = False

    def __str__(self):
        if not self.ordered:
            self.order_address(self.order)
        accum_string = ''
        for value in self.address_dict:
            accum_string += value['value']
            accum_string += ' '
        return accum_string.strip()

    #   Description: Sorts csv_dict to create a list of dictionaries such that they are in the same order they would be in an address string written by a human.
    #   Parameters
    ##      order:
    ##      return:     sorts the csv_dict according to label placement
    def order_address(self, order):
        address_list = []
        for i in range(len(order)):
            counter = 0
            while counter < len(self.address_dict):
                if self.address_dict[counter]['label'].lower() == order[i]:
                    address_list.append(self.address_dict[counter])
                    break
                else:
                    counter += 1
        self.address_dict = address_list

    def to_conll(self, address):
        tokens = self._tokenize(address)
        tags = self._ner_tags(address)
        pos = self._pos_tags(tokens)
        conll = ''
        for i in range(len(tokens)):
            token_val = tokens[i]
            pos_val = pos[i][1]
            tag_val = tags[token_val]
            conll = conll + '{} {} {} {} \n'.format(token_val, pos_val, pos_val, tag_val)
        return conll

    def _ner_tags(self, address):
        tags = {}
        for part in address:
            value = part['value'].split(' ')
            tokens = []
            tokens = tokens + [word for word in value if word]
            for i in range(len(tokens)):
                if i == 0:
                    tags[tokens[i]] = 'B-' + part['label']
                else:
                    tags[tokens[i]] = 'I-' + part['label']
        return tags

    def _tokenize(self, address):
        tokens = []
        for part in address:
            value = part['value'].split(' ')
            tokens = tokens + [word for word in value if word]
        return tokens

    ###ADD POS tagging formula here ###
    def _pos_tags(self, tokens):
        tagged = nltk.pos_tag(tokens)
        return tagged
