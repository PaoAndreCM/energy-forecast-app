import requests
import time
from bisect import bisect_left
from config import SEQ_LEN, PRED_LEN, OFFSET,OFFSET_HOURS, SMARD_BASE_URL

WEEK_ms = 7 * 24 * 60 * 60 * 1000 # milliseconds in week

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
    
    available = fetch_available_timestamps()

    index = bisect_left(available, timestamp)

    if available[index] != timestamp:
        if index != 0:
            index -= 1
        else:
            # TODO handle this error properly
            print("start of week not available as fetchable timestamp")

    monday_ts = available[index]
    return monday_ts

def get_input(timestamp):
    """Take desired forecast timestamp and return input needed for model to generate forecast"""

    input_start = calculate_input_start_timestamp(timestamp)
    monday_ts = calculate_start_of_week(input_start)
    input = fetch_week_consumption(monday_ts)

    if monday_ts != input_start:
        next_monday_ts = monday_ts + WEEK_ms
        input = input + fetch_week_consumption(next_monday_ts)

        for i, pair in enumerate(input):
            if pair[0] >= input_start:
                start_index = i
                break
        
        input = input[start_index:start_index+SEQ_LEN]
    return input

def calculate_input_start_timestamp(timestamp):
    # input starts at timestamp - offset in ms - week in ms
    input_start = timestamp - (OFFSET_HOURS*60*60*1000) - WEEK_ms
    return input_start


# Test
if __name__ == "__main__":
    test_timestamp = 1741682931691
    result = get_input(test_timestamp)
    readable = time.strftime( '%Y-%m-%d %H:%M:%S' ,time.gmtime(test_timestamp/1000))
    print(f"Got {len(result)} data points")
    print(readable)
    print(result[0])
    readable = time.strftime( '%Y-%m-%d %H:%M:%S' ,time.gmtime(result[671][0]/1000))
    print(readable)
