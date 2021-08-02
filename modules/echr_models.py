import pandas as pd
from sqlalchemy import create_engine, Column, String, Integer, LargeBinary, Float, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine('sqlite+pysqlcipher:///data/courts.db', connect_args={'check_same_thread': False})
database = declarative_base()
session = sessionmaker(db)()


class CourtDecision(database):
    __tablename__ = 'court_decisions'
    court_decision_id = Column(Integer, primary_key=True)
    application_number_id = Column(String)
    application_number_year = Column(String)
    application_number = Column(String)
    application_title = Column(String)
    date_of_introduction = Column(String)
    name_of_representative = Column(String)
    current_state_of_proceedings = Column(String)
    last_major_event_date = Column(String)
    last_major_event_description = Column(String)
    major_events = Column(String)


def insert_many_court_decisions(records):
    """
    append a new court_decision into the court_decisions table
    :param records: list of tuples with data [{'par1':'val1','par2':'val2',...},{'par1':'val1','par2':'val2',...},...]
    """

    session.bulk_insert_mappings(CourtDecision, records)
    session.commit()


def get_dataframe():
    df = pd.read_sql(session.query(CourtDecision).statement, session.bind)
    return df


database.metadata.create_all(db)

if __name__ == '__main__':
    print()
