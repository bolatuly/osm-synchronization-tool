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


# all changes to db temporarly commented
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
            b = building
            # ses.add(b)
            # ses.commit()
            return b
        else:
            return None

    @staticmethod
    def add(building):
        b = ses.query(Building).filter_by(id=building.id).first()
        if b:
            return None
        else:
            b = building
            # ses.add(b)
            # ses.commit()
            return b

    @staticmethod
    def delete(building):
        # simulate deletion
        # TODO later decide
        return building

    @staticmethod
    def select(building):
        b = ses.query(Building).filter_by(id=building).first()
        if b:
            return b
        else:
            return None


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
            b = road
            # ses.add(b)
            # ses.commit()
            return b
        else:
            return None

    @staticmethod
    def add(road):
        b = ses.query(Road).filter_by(id=road.id).first()
        if b:
            return None
        else:
            b = road
            # ses.add(b)
            # ses.commit()
            return b

    @staticmethod
    def delete(road):
        # simulate deletion
        # TODO later decide
        return road

    @staticmethod
    def select(road):
        b = ses.query(Road).filter_by(id=road).first()
        if b:
            return b
        else:
            return None


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
            b = river
            # ses.add(b)
            # ses.commit()
            return b
        else:
            return None

    @staticmethod
    def add(river):
        b = ses.query(River).filter_by(id=river.id).first()
        if b:
            return None
        else:
            b = river
            # ses.add(b)
            # ses.commit()
            return b

    @staticmethod
    def delete(river):
        # simulate deletion
        # TODO later decide
        return river

    @staticmethod
    def select(river):
        b = ses.query(River).filter_by(id=river).first()
        if b:
            return b
        else:
            return None
