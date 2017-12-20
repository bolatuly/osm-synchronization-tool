import geojson as gjs
import shapely.wkb as wkblib

from custom_schema import Building
from custom_schema import River
from custom_schema import Road


def geojson(entity, action):
    g = wkblib.loads(str(entity.geom), hex=True)
    id = entity.id
    properties = {"action": action}

    if type(entity) is Building:
        properties["name"] = entity.name
        properties["addr_house_num"] = entity.addr_house_num
        properties["usage"] = entity.usage
        properties["levels"] = entity.levels
        properties["addr_street"] = entity.addr_street
        properties["building_type"] = entity.building_type
        properties["table"] = "building"
    elif type(entity) is River:
        properties["name"] = entity.name
        properties["width"] = entity.width
        properties["table"] = "river"
    elif type(entity) is Road:
        properties["name"] = entity.name
        properties["road_type"] = entity.road_type
        properties["access"] = entity.access
        properties["oneway"] = entity.oneway
        properties["table"] = "road"
    else:
        print("aa")

    return gjs.Feature(id=id, geometry=g, properties=properties)
