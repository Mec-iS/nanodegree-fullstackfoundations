__author__ = 'lorenzo'

'''Configuration'''
import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()
'''End Configuration'''

'''Class'''
class Restaurant(Base):
    #
    # Table
    #
    __tablename__ = 'restaurant'

    #
    # Mapper
    #
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

    pass
'''End Class'''

'''Class'''
class MenuItem(Base):
    #
    # Table
    #
    __tablename__ = 'menu_item'

    #
    # Mapper
    #
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    pass
'''End Class'''

'''Configuration'''
engine = create_engine(
    r'sqlite:///C:\Github\restaurantmenu.db'
)
'''End Configuration'''



