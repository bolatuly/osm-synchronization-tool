import postgresql


class Database:
    def __init__(self):
        self._db = postgresql.open('pq://postgres:zxc123@localhost:5432/sync_osm')

    def select(self, feature, type):
        if type == 'building':
            query = "SELECT osm_id, (each(tags)).key, (each(tags)).value, way from planet_osm_polygon where osm_id = " + str(
                feature[2])
        elif type == 'road':
            query = "SELECT osm_id, (each(tags)).key, (each(tags)).value, way from planet_osm_roads where osm_id = " + str(
                feature[2])
        elif type == 'river':
            query = "SELECT osm_id, (each(tags)).key, (each(tags)).value, way from planet_osm_line where osm_id = " + str(
                feature[2])
        res = self._db.query(query)
        return res
