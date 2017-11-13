import osmium as o

from custom_schema import Building as building_sync
from custom_schema import River as river_sync
from custom_schema import Road as road_sync
from entity.building import Building
from entity.river import River
from entity.road import Road
from database import Database


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
            building.house_num = dictionary['addr:housenumber'] if 'addr:housenumber' in dictionary else None
            building.usage = dictionary['building:use'] if 'building:use' in dictionary else None
            building.levels = dictionary['building:levels'] if 'building:levels' in dictionary else None
            building.street = dictionary['addr:street'] if 'addr:street' in dictionary else None
            building.type = dictionary['building'] if 'building' in dictionary else None
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
            road._road_type = dictionary['highway'] if 'highway' in dictionary else None
            road.access = dictionary['access'] if 'access' in dictionary else None
            road.oneway = dictionary['oneway'] if 'oneway' in dictionary else None
            return road

    @staticmethod
    def delete(db, type, feature):
        if type == 'building':
            b = Building()
            b.id = feature[2]
            return building_sync.delete(b)
        if type == 'road':
            b = Road()
            b.id = feature[2]
            return road_sync.delete(feature[2])
        if type == 'river':
            b = River()
            b.id = feature[2]
            return river_sync.delete(feature[2])

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
                return building_sync.add(entity)
            if type == 'road':
                return road_sync.add(entity)
            if type == 'river':
                return river_sync.add(entity)

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
                return building_sync.edit(entity)
            if type == 'road':
                return road_sync.edit(entity)
            if type == 'river':
                return river_sync.edit(entity)


if __name__ == '__main__':

    h = FileStatsHandler()

    h.apply_file("data/211.osc.gz", locations=True)

    b_deleted = b_added = b_edited = road_deleted = road_added = road_edited = river_deleted = river_added = river_edited = 0

    db = Database()

    for feature in h.deleted:
        if feature[0] == 'way':
            for item in feature[4]:
                if item[0] == 'building':
                    if Processor.delete(db, 'building', feature):
                        b_deleted += 1
                elif item[0] == 'highway' and item[1] == 'road':
                    if Processor.delete(db, 'road', feature):
                        road_deleted += 1
                elif item[0] == 'waterway' and item[1] == 'river':
                    if Processor.delete(db, 'river', feature):
                        river_deleted += 1

    for feature in h.added:
        if feature[0] == 'way':
            for item in feature[4]:
                if item[0] == 'building':
                    if Processor.add(db, 'building', feature):
                        b_added += 1
                elif item[0] == 'highway' and item[1] == 'road':
                    if Processor.add(db, 'road', feature):
                        road_added += 1
                elif item[0] == 'waterway' and item[1] == 'river':
                    if Processor.add(db, 'river', feature):
                        river_added += 1

    for feature in h.modified:
        if feature[0] == 'way':
            for item in feature[4]:
                if item[0] == 'building':
                    if Processor.edit(db, 'building', feature):
                        b_edited += 1
                elif item[0] == 'highway' and item[1] == 'road':
                    if Processor.edit(db, 'road', feature):
                        road_edited += 1
                elif item[0] == 'waterway' and item[1] == 'river':
                    if Processor.edit(db, 'river', feature):
                        river_edited += 1

    print("Deleted features: {:d} buildings, {:d} roads, {:d} rivers".format(b_deleted, road_deleted, river_deleted))
    print("Added features: {:d} buildings, {:d} roads, {:d} rivers".format(b_added, road_added, river_added))
    print("Modified features: {:d} buildings, {:d} roads, {:d} rivers".format(b_edited, road_edited, river_edited))
