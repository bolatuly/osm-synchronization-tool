class Building(object):
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def house_num(self):
        return self._house_num

    @house_num.setter
    def house_num(self, house_num):
        self._house_num = house_num

    @property
    def usage(self):
        return self._usage

    @usage.setter
    def usage(self, usage):
        self._usage = usage

    @property
    def levels(self):
        return self._levels

    @levels.setter
    def levels(self, levels):
        self._levels = levels

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, street):
        self._street = street

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def geom(self):
        return self._geom

    @geom.setter
    def geom(self, geom):
        self._geom = geom
