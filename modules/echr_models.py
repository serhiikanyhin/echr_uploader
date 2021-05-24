from peewee import *
import pandas as pd

database = SqliteDatabase("data/courts.db")


class BaseModel(Model):
    class Meta:
        database = database


class CourtDecision(BaseModel):
    court_decision_id = AutoField()
    application_number_id = IntegerField()
    application_number_year = IntegerField()
    application_number = IntegerField()
    application_title = CharField()
    date_of_introduction = CharField()
    name_of_representative = CharField()
    current_state_of_proceedings = CharField()
    last_major_event_date = CharField()
    last_major_event_description = CharField(max_length="1000")
    major_events = CharField(max_length="2000")


def insert_many_court_decisions(data):
    """
    append a new court_decision into the court_decisions table
    :param data: list of tuples with data [(2,21,'text'),(3,21,'text')...]
    """

    fields = [
        'application_number_id',
        'application_number_year',
        'application_number',
        'application_title',
        'date_of_introduction',
        'name_of_representative',
        'current_state_of_proceedings',
        'last_major_event_date',
        'last_major_event_description',
        'major_events'
    ]

    CourtDecision.insert_many(data, fields).execute()


def create_tables():
    with database:
        database.create_tables([CourtDecision])


def get_dataframe(table_name):
    cursor = database.execute_sql("SELECT * from " + table_name)
    df = pd.DataFrame(cursor.fetchall())
    df.columns = [i[0] for i in cursor.description]
    return df


if __name__ == '__main__':
    print()
