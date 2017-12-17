import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#association_table = Table('association', Base.metadata,
#    Column('post_id', Integer, ForeignKey('user.id')),
#    Column('comment_id', Integer, ForeignKey('comment.id'))
#)


class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    num_comments = Column(Integer, nullable=False)
    comment = relationship('Comment',)
    last_seen = Column(DateTime)
    submissions = Column(Integer)
    #account_created = Column(DateTime)



    def __repr__(self):
        return 'User({}, {}, {})'.format(self.name, self.num_comments, self.submissions)

    def __eq__(self, other):
        if hasattr(other, 'name'):
            return self.name == other.name
        else:
            return self.name == other

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    idx = Column(String)
    title = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    score = Column(Integer)
    created = Column(DateTime)
    #user = relationship("User" )

    def __repr__(self):
        return 'Comment({})'.format(self.name)

    def __eq__(self, other):
        if hasattr(other, 'idx'):
            return self.idx == other.idx
        else:
            return self.idx == other

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    idx = Column(String)
    title = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))

    # user = relationship("User" )

    def __repr__(self):
        return 'Post({})'.format(self.name)

    def __eq__(self, other):
        if hasattr(other, 'idx'):
            return self.idx == other.idx
        else:
            return self.idx == other
#class Post:
#    __tablename__ = 'comment'
#
#    id = Column(Integer, primary_key=True)
#    comment_id = Column(Integer, ForeignKey('child.id'))
#    comment = relationship("Comment",
#                           )


class OtherMeta(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)



# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///tpusers.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)