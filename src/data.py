import requests
import time
from bisect import bisect_left
from config import SEQ_LEN, PRED_LEN, OFFSET, SMARD_BASE_URL

def fetch_available_timestamps():
    """Fetch available timestamps. The available timestamps correspond to the beginning of each week.
    These timestamps can then be used to fetch the consumption corresponding to that week.
    """

    url = SMARD_BASE_URL+'index_quarterhour.json'

    response = requests.get(url)
    response.raise_for_status()
    # TODO handle status error

    data = response.json()
    return data.get('timestamps', [])

def fetch_week_consumption(monday_ts):
    """Fetch consumption corresponding to the week starting on the Monday containing the timestamp
    Args:
        week_start_ts (int) Unix timestamp in ms for a Monday at 00.00
    """

    url = f'{SMARD_BASE_URL}410_DE_quarterhour_{monday_ts}.json'

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data.get('series', [])

def calculate_start_of_week(timestamp):
    """Calculate the timestamp for Monday 00.00 of the week containing the given timestamp 
    Args: 
        timestamp (int): Unix timestamp in ms"""
    
    # convert to s
    timestamp_s = timestamp / 1000

    # get time struct
    t = time.gmtime(timestamp_s)

    # calculate Monday
    monday_s = timestamp_s - (t.tm_wday * 24 * 3600) - (t.tm_hour * 3600) - (t.tm_min * 60) - t.tm_sec
    monday_ts = monday_s * 1000
    return monday_ts


def get_input(timestamp):
    """Take desired forecast timestamp and return input needed for model to generate forecast"""

    input_start = calculate_input_start_timestamp(timestamp)
    monday_ts = calculate_start_of_week(input_start)
    input = fetch_week_consumption(monday_ts)

    stitch_needed = needs_stitching(input_start)

    #TODO calculate prev_mon_timestamp, obtain actual input from input + input2

    prev_mon_timestamp = 0
    if stitch_needed:
        input_2 = fetch_week_consumption(prev_mon_timestamp)

    return input

def needs_stitching(timestamp):
    """Returns True if the input for the requested timestamp must come from two different weeks."""
    # TODO implement
    return True

def calculate_input_start_timestamp(timestamp):
    # TODO implement
    
    return 0


# Test
if __name__ == "__main__":
    test_timestamp = 1710800000000
    result = get_input(test_timestamp)
    print(f"Got {len(result)} data points")
