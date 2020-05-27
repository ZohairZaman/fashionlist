class Brand(object):
    @classmethod
    def fromdict(cls, d):
        allowed = (
            '_id', 'name', 'listings'
        )
        df = {k : v for k, v in d.items() if k in allowed}
        return cls(**df)

    def __init__(self, _id= '', name = '', listings = []):
        self._id = _id
        self._name = name
        self._listings = listings

    def __str__(self):
        print_str = 'Brand('
        for attr, value in vars(self).items():
            print_str += '{}={}'.format(attr, value)
        print_str += ')'
        return print_str

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = str(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def listings(self):
        return self._listings

    @listings.setter
    def listings(self, value):
        self._listings = value
