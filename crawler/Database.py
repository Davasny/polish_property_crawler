import pymysql
import config
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import JSON, LONGTEXT, TIMESTAMP, DECIMAL, DOUBLE, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Offer(Base):
    __tablename__ = 'polish_property_crawler'
    id = Column(Integer, primary_key=True)
    added_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    title = Column(String(400))
    description = Column(LONGTEXT)

    price = Column(DOUBLE)
    rent_price = Column(DOUBLE)

    latitude = Column(DECIMAL(11, 8))
    longitude = Column(DECIMAL(11, 8))

    surface = Column(DECIMAL(11, 6))
    surface_land = Column(DECIMAL(11, 6))
    surface_useful = Column(DECIMAL(11, 6))

    floor_num = Column(Integer)
    offer_id = Column(Integer, unique=True)
    seller_id = Column(Integer)

    available_since = Column(TIMESTAMP)
    build_year = Column(DATETIME)

    equipment = Column(JSON)
    extras_surface = Column(JSON)
    media = Column(JSON)
    security_types = Column(JSON)
    neighborhood_education = Column(JSON)
    neighborhood_health = Column(JSON)
    neighborhood_others = Column(JSON)
    neighborhood_public_transport = Column(JSON)

    area_fence = Column(String(200))
    area_shape = Column(String(200))
    attic = Column(String(200))
    basement = Column(String(200))
    bathroom = Column(String(200))
    bathroom_equipment = Column(String(200))
    bathroom_state = Column(String(200))
    building_elevation = Column(String(200))
    building_floors_num = Column(String(200))
    building_material = Column(String(200))
    building_ownership = Column(String(200))
    building_type = Column(String(200))
    city_name = Column(String(200))
    construction_status = Column(String(200))
    country = Column(String(200))
    district_name = Column(String(200))
    heating = Column(String(200))
    installation_state = Column(String(200))
    investment_name = Column(String(200))
    kitchen_type = Column(String(200))
    language = Column(String(200))
    loudness = Column(String(200))
    offer_type = Column(String(200))
    parking_spot = Column(String(200))
    parking_spot_num = Column(String(200))
    physical_rooms_num = Column(String(200))
    price_currency = Column(String(200))
    proper_type = Column(String(200))
    property_type = Column(String(200))
    region_name = Column(String(200))
    road_material = Column(String(200))
    roof = Column(String(200))
    rooms_num = Column(String(200))
    sewers = Column(String(200))
    source = Column(String(200))
    subregion_name = Column(String(200))
    windows_type = Column(String(200))
    world_orientation = Column(String(200))

    unknown = Column(JSON)


engine = create_engine('mysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    config.MYSQL['user'],
    config.MYSQL['password'],
    config.MYSQL['host'],
    config.MYSQL['port'],
    config.MYSQL['db'])
)

Base.metadata.create_all(engine)


class MySQL:
    def __init__(self):
        server = "localhost"
        user = "root"
        password = ""
        server_port = 3306
        database = "otodom_crawler"

        self.operating_database = pymysql.connect(host=server, user=user, password=password, database=database,
                                             charset='utf8', port=server_port)

        self.cur = self.operating_database.cursor()

    def new_query(self, command):
        if 'SELECT' in command:
            self.cur.execute(command)
            return self.cur.fetchall()
        elif 'INSERT' in command:
            self.cur.execute(command)
            self.operating_database.commit()
            return self.cur.lastrowid
        elif 'UPDATE' in command:
            self.cur.execute(command)
            self.operating_database.commit()
            return True
        elif 'DELETE' in command:
            self.cur.execute(command)
            self.operating_database.commit()
            return True
        else:
            return False
