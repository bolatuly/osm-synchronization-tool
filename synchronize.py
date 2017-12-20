import osmium as o

from custom_schema import Building
from custom_schema import River
from custom_schema import Road
from database import Database
from json_maker import geojson


class FileStatsHandler(o.SimpleHandler):
    def __init__(self):
        super(FileStatsHandler, self).__init__()
        self.deleted = []
        self.added = []
        self.modified = []

    def node(self, n):
        self.decision(n, 'node')

    def way(self, w):
        self.decision(w, 'way')

    def relation(self, r):
        self.decision(r, 'relation')

    def decision(self, feature, type):
        if feature.deleted:
            self.deleted.append(self.handle_type(type, feature))
        elif feature.version == 1:
            self.added.append(self.handle_type(type, feature))
        else:
            self.modified.append(self.handle_type(type, feature))

    def handle_type(self, type, feature):
        if type == 'node':
            return [type, feature.changeset, feature.id,
                    [feature.location.lat, feature.location.lon], self.simplify_tags(feature.tags), feature.timestamp,
                    feature.uid, feature.user, feature.version]
        if type == 'way':
            return [type, feature.changeset, feature.id,
                    self.simplify_nodes(feature.nodes), self.simplify_tags(feature.tags), feature.timestamp,
                    feature.uid, feature.user, feature.version]

        if type == 'relation':
            return [type, feature.changeset, feature.id,
                    self.simplify_members(feature.members), self.simplify_tags(feature.tags), feature.timestamp,
                    feature.uid, feature.user, feature.version]

    def simplify_tags(self, tags):
        data = []
        for i in tags:
            data.append((i.k, i.v))
        return data

    def simplify_nodes(self, nodes):
        data = []
        for i in nodes:
            data.append(i.ref)
        return data

    def simplify_members(self, members):
        data = []
        for i in members:
            data.append(i.ref)
        return data


class Processor:
    @staticmethod
    def makeEntity(id, geom, tags, type):
        dictionary = dict(tags)
        if type == 'building':
            building = Building()
            building.id = id
            building.geom = geom
            building.name = dictionary['name'] if 'name' in dictionary else None
            building.addr_house_num = dictionary['addr:housenumber'] if 'addr:housenumber' in dictionary else None
            building.usage = dictionary['building:use'] if 'building:use' in dictionary else None
            building.levels = dictionary['building:levels'] if 'building:levels' in dictionary else None
            building.addr_street = dictionary['addr:street'] if 'addr:street' in dictionary else None
            building.building_type = dictionary['building'] if 'building' in dictionary else None
            return building
        elif type == 'river':
            river = River()
            river.id = id
            river.geom = geom
            river.name = dictionary['name'] if 'name' in dictionary else None
            river.width = dictionary['width'] if 'width' in dictionary else None
            return river
        elif type == 'road':
            road = Road()
            road.id = id
            road.geom = geom
            road.name = dictionary['name'] if 'name' in dictionary else None
            road.road_type = dictionary['highway'] if 'highway' in dictionary else None
            road.access = dictionary['access'] if 'access' in dictionary else None
            road.oneway = dictionary['oneway'] if 'oneway' in dictionary else None
            return road

    @staticmethod
    def delete(db, type, feature):
        data = db.select(feature, type)
        tags = []
        if len(data) != 0:
            for d in data:
                id = d[0]
                geom = d[3]
                tags.append((d[1], d[2]))
            entity = Processor.makeEntity(id, geom, tags, type)
            if type == 'building':
                return Building().delete(entity)
            if type == 'road':
                return Road().delete(entity)
            if type == 'river':
                return River().delete(entity)

    @staticmethod
    def add(db, type, feature):
        data = db.select(feature, type)
        tags = []
        if len(data) != 0:
            for d in data:
                id = d[0]
                geom = d[3]
                tags.append((d[1], d[2]))
            entity = Processor.makeEntity(id, geom, tags, type)
            if type == 'building':
                return Building().add(entity)
            if type == 'road':
                return Road().add(entity)
            if type == 'river':
                return River().add(entity)

    @staticmethod
    def edit(db, type, feature):
        data = db.select(feature, type)
        tags = []
        if len(data) != 0:
            for d in data:
                id = d[0]
                geom = d[3]
                tags.append((d[1], d[2]))
            entity = Processor.makeEntity(id, geom, tags, type)
            if type == 'building':
                return Building().edit(entity)
            if type == 'road':
                return Road().edit(entity)
            if type == 'river':
                return River().edit(entity)


def syncronize(file):
    h = FileStatsHandler()

    h.apply_file(file, locations=True)

    b_added = []
    b_edited = []
    road_added = []
    road_edited = []
    river_added = []
    river_edited = []

    db = Database()

    for feature in h.added:
        if feature[0] == 'way':
            for item in feature[4]:
                if item[0] == 'building':
                    entity = Processor.add(db, 'building', feature)
                    if entity is not None:
                        entity = geojson(entity, 'added')
                        b_added.append(entity)
                elif item[0] == 'highway' and item[1] == 'road':
                    entity = Processor.add(db, 'road', feature)
                    if entity is not None:
                        entity = geojson(entity, 'added')
                        road_added.append(entity)
                elif item[0] == 'waterway' and item[1] == 'river':
                    entity = Processor.add(db, 'river', feature)
                    if entity is not None:
                        entity = geojson(entity, 'added')
                        river_added.append(entity)

    for feature in h.modified:
        if feature[0] == 'way':
            for item in feature[4]:
                if item[0] == 'building':
                    entity = Processor.edit(db, 'building', feature)
                    if entity is not None:
                        entity = geojson(entity, 'modified')
                        b_edited.append(entity)
                elif item[0] == 'highway' and item[1] == 'road':
                    entity = Processor.edit(db, 'road', feature)
                    if entity is not None:
                        entity = geojson(entity, 'modified')
                        road_edited.append(entity)
                elif item[0] == 'waterway' and item[1] == 'river':
                    entity = Processor.edit(db, 'river', feature)
                    if entity is not None:
                        entity = geojson(entity, 'modified')
                        river_edited.append(entity)

    data = {"b_added": b_added,
            "road_added": road_added, "river_added": river_added,
            "b_edited": b_edited, "road_edited": road_edited, "river_edited": river_edited}

    return data


def initial_data(file):
    h = FileStatsHandler()

    h.apply_file(file, locations=True)

    b_deleted = []
    b_edited = []
    road_deleted = []
    road_edited = []
    river_deleted = []
    river_edited = []

    for feature in h.deleted:
        if feature[0] == 'way':
            for item in feature[4]:
                if item[0] == 'building':
                    entity = Building().select(feature[2])
                    if entity is not None:
                        entity = geojson(entity, 'deleted')
                        b_deleted.append(entity)
                elif item[0] == 'highway' and item[1] == 'road':
                    entity = Road().select(feature[2])
                    if entity is not None:
                        entity = geojson(entity, 'deleted')
                        road_deleted.append(entity)
                elif item[0] == 'waterway' and item[1] == 'river':
                    entity = River().select(feature[2])
                    if entity is not None:
                        entity = geojson(entity, 'deleted')
                        river_deleted.append(entity)

    for feature in h.modified:
        if feature[0] == 'way':
            for item in feature[4]:
                if item[0] == 'building':
                    entity = Building().select(feature[2])
                    if entity is not None:
                        entity = geojson(entity, 'modified')
                        b_edited.append(entity)
                elif item[0] == 'highway' and item[1] == 'road':
                    entity = Road().select(feature[2])
                    if entity is not None:
                        entity = geojson(entity, 'modified')
                        road_edited.append(entity)
                elif item[0] == 'waterway' and item[1] == 'river':
                    entity = River().select(feature[2])
                    if entity is not None:
                        entity = geojson(entity, 'modified')
                        river_edited.append(entity)

    data = {"b_deleted": b_deleted, "road_deleted": road_deleted, "river_deleted": river_deleted,
            "b_edited": b_edited, "road_edited": road_edited, "river_edited": river_edited}

    return data
