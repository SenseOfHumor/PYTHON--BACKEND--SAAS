import requests
import os
from dotenv import load_dotenv
import xmltodict
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("TIME_API")


def get_local_time(loc):
    url = f"https://api.timezonedb.com/v2.1/list-time-zone?key={API_KEY}&format=xml&zone={loc}"
    response = requests.get(url)
    data = xmltodict.parse(response.content)
    
    if data['result']['status'] != 'OK':  ## check if the status is OK
        return f"Error: {data['result'].get('message', 'Unknown error')}"
    
    zones = data['result'].get('zones', {}).get('zone', {})  ## get the zone data
    
    # Ensure zones is always a list
    if isinstance(zones, dict):
        zones = [zones]

    for zone in zones:
        country_name = zone.get('countryName', 'N/A')
        zone_name = zone.get('zoneName', 'N/A')
        gmt_offset = zone.get('gmtOffset', 'N/A')
        timestamp = int(zone.get('timestamp', 0))
        # Convert the timestamp to a human-readable format
        local_time = datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')  ## convert the timestamp to human readable format
        local_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')  ## convert the timestamp to human readable format
        ## return (f"Country: {country_name}, City: {zone_name}, GMT Offset: {gmt_offset}, Local Time: {local_time}")
        return local_time, country_name, zone_name, gmt_offset, local_date
    



# Example usage
get_local_time("Asia/Kolkata")


#TODO: Implement the front end in way so that the recieved location can be passed to the function without error
#TODO: Implement some error handling in case the location is not found



## response format  --> XML
''''<countryCode>US</countryCode>
<countryName>United States</countryName>
<zoneName>America/New_York</zoneName>           --> (loc) America/New_York  -> (zone_name) New York
<gmtOffset>-14400</gmtOffset>
<timestamp>1720839808</timestamp>
</zone>'''

