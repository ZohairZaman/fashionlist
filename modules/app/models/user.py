class User(object):
    def __init__(self, id = '', email = '', name = '', closet_id = '', wishlist_id = ''):
        self._id = id
        self._email = email
        self._name = name
        self._closet_id = closet_id
        self._wishlist_id = wishlist_id

    def __str__(self):
        print_str = 'User(id={}, email={}, name={}, closet_id={}, wishlist_id={})'.format(
            self.id,
            self.email,
            self.name,
            self.closet_id,
            self.wishlist_id
        )
        return print_str

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = str(value)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def closet_id(self):
        return self._closet_id

    @closet_id.setter
    def closet_id(self, value):
        self._closet_id = str(value)

    @property
    def wishlist_id(self):
        return self._wishlist_id

    @wishlist_id.setter
    def wishlist_id(self, value):
        self._wishlist_id = str(value)
