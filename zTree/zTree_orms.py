#!/usr/bin/python
import argparse
import sys

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKeyConstraint

Base = declarative_base()

class Global(Base):
    __tablename__ = 'globals'
    timestamp = Column(DateTime, primary_key=True, index=True)
    session = Column(Integer, primary_key=True, index=True, autoincrement=False)
    Period = Column(Integer, primary_key=True, index=True, autoincrement=False)
    NumPeriods = Column(Integer)
    RepeatTreatment = Column(Integer)

    # defines the 1:M globals to subjects relationship
    subjects = relationship('Subjects')

    # defines the 1:1 globals to summary relationship
    summary = relationship('Summary', uselist=False, backref='globals')

    # Add your experiment's custom global fields below


class Session(Base):
    __tablename__ = 'session'
    timestamp = Column(DateTime, primary_key=True, index=True)
    session = Column(Integer, primary_key=True, index=True, autoincrement=False)
    Subject = Column(Integer, primary_key=True, index=True, autoincrement=False)
    FinalProfit = Column(Float)
    ShowUpFee = Column(Float)
    ShowUpFeeInvested = Column(Float)
    MoneyAdded = Column(Float)
    MoneyToPay = Column(Float)
    MoneyEarned = Column(Float)

    # defines the 1:M session to subjects relationship
    subjects = relationship('Subjects')

    # Add your experiment's custom session fields below


class Questionnaire(Base):
    __tablename__ = 'questionnaire'
    timestamp = Column(DateTime, primary_key=True, index=True)
    Subject = Column(Integer, primary_key=True, index=True, autoincrement=False)
    client = Column(String)

    # Add your experiment's custom questionnaire fields below


class Subjects(Base):
    __tablename__ = 'subjects'
    __table_args__ = (
        # defines the 1:M globals to subjects relationship
        ForeignKeyConstraint(
            ('timestamp', 'session', 'Period'), 
            ('globals.timestamp', 'globals.session', 'globals.Period'),
            onupdate='cascade',
            ondelete='cascade'
        ), 
        # defines the 1:M session to subjects relationship
        ForeignKeyConstraint(
            ('timestamp', 'session', 'Subject'), 
            ('session.timestamp', 'session.session', 'session.Subject'),
            onupdate='cascade',
            ondelete='cascade'
        ), 
    )
    timestamp = Column(DateTime, primary_key=True, index=True)
    session = Column(Integer, primary_key=True, index=True, autoincrement=False)
    Period = Column(Integer, primary_key=True, index=True, autoincrement=False)
    Subject = Column(Integer, primary_key=True, index=True, autoincrement=False)
    Group = Column(Integer)
    Profit = Column(Float)
    TotalProfit = Column(Float)
    Participate = Column(Boolean)
    # Add your experiment's custom subject fields below


class Summary(Base):
    __tablename__ = 'summary'
    __table_args__ = (
        # defines the 1:1 globals to summary relationship
        ForeignKeyConstraint(
            ('timestamp', 'session', 'Period'), 
            ('globals.timestamp', 'globals.session', 'globals.Period'),
            onupdate='cascade',
            ondelete='cascade'
        ), 
    )
    timestamp = Column(DateTime, primary_key=True, index=True)
    session = Column(Integer, primary_key=True, index=True, autoincrement=False)
    Period = Column(Integer, primary_key=True, index=True, autoincrement=False)
    # Add your experiment's custom summary fields below


if __name__ == '__main__':
    description = 'ORMs for your zTree experiment.'
    description = '%s This utility will create the tables' % description 
    description = '%s when run from the command line.' % description
    p = argparse.ArgumentParser(description=description)
    p.add_argument('socket', help='Socket on which postgresql is listening')
    p.add_argument('db_name', help='Name of postgresql db')
    args = p.parse_args()

    dburl = 'postgresql+psycopg2://%s/%s' % (args.socket, args.db_name)
    engine = create_engine(dburl)
    Base.metadata.create_all(engine)
