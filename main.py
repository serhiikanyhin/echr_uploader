from modules.echr_models import *
from modules.echr_multi_downloader import *
from modules.echr_export import *
from modules.echr_statistics import *
import time
from itertools import islice


def run_script():

    print("Start -", time.strftime("%H:%M:%S", time.localtime()))

    # DATABASE
    create_tables()

    # GET ALL DATA FROM WEBSITE
    download_data()

    # COURT DECISIONS DATAFRAME
    court_decisions_df = get_dataframe("court_decisions")

    # EXPORT EXEL
    export_exel(court_decisions_df)

    # CREATE PLOTS
    create_plots(court_decisions_df)

    print("End -", time.strftime("%H:%M:%S", time.localtime()))


def download_data():
    print_status("Year", "Start", "End", "Time", "Courts")
    for year in [
            "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18",
            "19", "20", "21"]:
        print_status(year, "", "", time.strftime("%H:%M:%S", time.localtime()), "")
        download_year_data(year, 10000)
        database.commit()


def download_year_data(year, batch_size):
    """
    :param year: target year
    :param batch_size: size of batch - depend on search solidity
    :return: all founded court decisions data within year
    """

    batch_end = 0
    work_status = True

    # Loop while find any exist cort decisions in batch
    while work_status is True:

        # Async function parameters
        batch_start = batch_end + 1
        batch_end = batch_start + batch_size - 1
        application_numbers_range = list(range(batch_start, batch_end))
        batch_court_decisions = async_download(application_numbers_range, year)

        # Check if async download results is empty
        batch_len = len(batch_court_decisions)
        if batch_len == 0:
            work_status = False
        else:
            print_status(year, batch_start, batch_end, time.strftime("%H:%M:%S", time.localtime()), batch_len)

        [insert_many_court_decisions(i) for i in chunk(batch_court_decisions, 1000)]


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def print_status(year, start, end, current_time, courts):
    """
    Prints table row to console with info about handled batch
    :param year: year of court decisions
    :param start: first court application number in batch
    :param end: last court application number in batch
    :param current_time: time of end handling
    :param courts: number of existing courts in batch
    """
    print("{0:<4}".format(year),
          "{0:<6}".format(start),
          "{0:<6}".format(end),
          "{0:<9}".format(current_time),
          "{0:<6}".format(courts)
          )


if __name__ == '__main__':
    run_script()
