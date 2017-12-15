from geoalchemy2 import *
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

db = create_engine('postgresql://postgres:zxc123@localhost:5432/sync_custom')
# db.echo = True
metadata = MetaData(db)
buildings = Table('building', metadata, autoload=True)
roads = Table('road', metadata, autoload=True)
rivers = Table('river', metadata, autoload=True)

Session = sessionmaker(bind=db)
ses = Session()


class Building(Base):
    __tablename__ = "building"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    addr_house_num = Column(String)
    usage = Column(String)
    levels = Column(String)
    addr_street = Column(String)
    building_type = Column(String)
    geom = Column(Geometry)

    @staticmethod
    def edit(building):
        b = ses.query(Building).filter_by(id=building.id).first()
        if b:
            b.name = building.name
            b.addr_house_num = building.house_num
            b.usage = building.usage
            b.levels = building.levels
            b.addr_street = building.street
            b.building_type = building.type
            b.geom = building.geom
            ses.add(b)
            ses.commit()
            return building
        else:
            return None

    @staticmethod
    def add(building):
        b = ses.query(Building).filter_by(id=building.id).first()
        if b:
            # Temporarily return true, then it should be false
            return building
        else:
            b = Building()
            b.id = building.id
            b.name = building.name
            b.addr_house_num = building.house_num
            b.usage = building.usage
            b.levels = building.levels
            b.addr_street = building.street
            b.building_type = building.type
            b.geom = building.geom
            ses.add(b)
            ses.commit()
            return building

    @staticmethod
    def delete(building):
        # simulate deletion
        # TODO later decide
        return building


class Road(Base):
    __tablename__ = "road"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    road_type = Column(String)
    access = Column(String)
    oneway = Column(String)
    geom = Column(Geometry)

    @staticmethod
    def edit(road):
        b = ses.query(Road).filter_by(id=road.id).first()
        if b:
            b.name = road.name
            b.road_type = road.road_type
            b.access = road.access
            b.oneway = road.oneway
            b.geom = road.geom
            ses.add(b)
            ses.commit()
            return road
        else:
            return None

    @staticmethod
    def add(road):
        b = ses.query(Road).filter_by(id=road.id).first()
        if b:
            # Temporarily return true, then it should be false
            return road
        else:
            b.id = road.id
            b.name = road.name
            b.road_type = road.road_type
            b.access = road.access
            b.oneway = road.oneway
            b.geom = road.geom
            ses.add(b)
            ses.commit()
            return None

    @staticmethod
    def delete(road):
        # simulate deletion
        # TODO later decide
        return road


class River(Base):
    __tablename__ = "river"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    width = Column(String)
    geom = Column(Geometry)

    @staticmethod
    def edit(river):
        b = ses.query(River).filter_by(id=river.id).first()
        if b:
            b.name = river.name
            b.width = river.width
            b.geom = river.geom
            ses.add(b)
            ses.commit()
            return river
        else:
            return None

    @staticmethod
    def add(river):
        b = ses.query(River).filter_by(id=river.id).first()
        if b is None:
            # Temporarily return true, then it should be false
            return river
        else:
            b.id = river.id
            b.name = river.name
            b.width = river.width
            b.geom = river.geom
            ses.add(b)
            ses.commit()
            return river

    @staticmethod
    def delete(river):
        # simulate deletion
        # TODO later decide
        return river
