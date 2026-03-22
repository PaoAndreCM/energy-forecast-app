import requests
import time
from bisect import bisect_left

def fetch_available_timestamps():
    """Fetch available timestamps. The available timestamps correspond to the beginning of each week.
    These timestamps can then be used to fetch the consumption corresponding to that week.
    """

    url = 'https://www.smard.de/app/chart_data/410/DE/index_quarterhour.json'

    response = requests.get(url)
    response.raise_for_status()
    # TODO handle status error

    data = response.json()
    return data.get('timestamps', [])

def fetch_consumption(timestamp):
    """Fetch consumption corresponding to one week, starting on the Monday containing the timestamp"""

    # see available timestamps for fetching
    available = fetch_available_timestamps()

    # locate index for the Monday that starts the week containing the timestamp
    index = bisect_left(available, timestamp)

    if available[index] == timestamp:
        pass #index is correct
    elif index == 0:
        # timestamp is before earliest available Monday
        print("Error: Target is before earliest available data")
        return None
        # TODO handle this error appropriately
    else:
        index -=1 # timestamp is not Monday 00:00, index needs to be previous one 

    
    # fetch the consumption for corresponding Monday
    timestamp = available[index] 
    url = f'https://www.smard.de/app/chart_data/410/DE/410_DE_quarterhour_{timestamp}.json'

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data.get('series', [])


# Test
if __name__ == "__main__":
    test_timestamp = 1710800000000
    result = fetch_consumption(test_timestamp)
    print(f"Got {len(result)} data points")
