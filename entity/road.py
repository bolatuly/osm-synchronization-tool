class Road(object):
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
    def road_type(self):
        return self._road_type

    @road_type.setter
    def road_type(self, road_type):
        self._road_type = road_type

    @property
    def access(self):
        return self._access

    @access.setter
    def access(self, access):
        self._access = access

    @property
    def oneway(self):
        return self._oneway

    @access.setter
    def oneway(self, oneway):
        self._oneway = oneway

    @property
    def geom(self):
        return self._geom

    @geom.setter
    def geom(self, geom):
        self._geom = geom
