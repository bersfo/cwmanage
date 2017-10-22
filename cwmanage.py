##
# This module includes methods that answer Connectwise Manage API requests with JSON objects.
# version = 0.1, author = bersfo, last updated = 10/03/2017
#
# currently supported API requests:
#       GET https://{connectwiseSite}/v4_6_release/apis/3.0/company/companies
#       GET https://{connectwiseSite}/v4_6_release/apis/3.0/system/members
#       GET https://{connectwiseSite}/v4_6_release/apis/3.0/schedule/entries
#       GET https://{connectwiseSite}/v4_6_release/apis/3.0/time/entries
##

# standard Python library for web server requests
import requests
# standard Python library for time manipulation
from datetime import date, datetime, timedelta
import arrow

class api(object):
    """ A Connectwise Manage API request object

        cwHost - The FQDN of your Connectwise Manage server
        cwToken - Follow https://gist.github.com/bersfo/12efa79de156aa6f96d80ff14a060822 to create your access token with Python
    """

    def __init__(self, cwHost, cwToken):
        self.cwUrl = "https://" + cwHost + "/v4_6_release/apis/3.0/"
        self.cwHeaders = {"Authorization": "Basic " + cwToken, "Content-Type": "application/json"}
        #TODO: Read system's timezone and determine time difference (in minutes) to UTC automatically
        self.cwTzUTCdiff = 420 #Pacific Time

    # Get a list of the first 1000 companies and return as JSON.
    def get_companies(self):
        try:
            r = requests.get(self.cwUrl + "company/companies?pageSize=1000&conditions=type/id==1", headers=self.cwHeaders)
            r.raise_for_status()
        except:
            print(r.text)
            raise
        return r.json()

    # Get a list of the first 1000 members and return as JSON.
    def get_members(self):
        try:
            r = requests.get(self.cwUrl + "system/members?pageSize=1000", headers=self.cwHeaders)
            r.raise_for_status()
        except:
            print(r.text)
            raise
        return r.json()

    # Get all scheduled entries for member between dateStart and dateEnd and return as JSON.
    # member is the CW user name
    # dateStart and dateEnd have this format: [2017-09-04T00:00:00Z]
    # (dateStart and dateEnd arguments are optional - will result in today)
    def get_schedule(self, member, dateStart="[" + date.today().isoformat() + "T00:00:00Z]", dateEnd="[" + date.today().isoformat() + "T23:59:59Z]"):
        # subtract difference to UTC timezone
        datestartutc = arrow.get(dateStart).datetime + timedelta(minutes=self.cwTzUTCdiff)
        dateendutc = arrow.get(dateEnd).datetime + timedelta(minutes=self.cwTzUTCdiff)
        # format to String object for URL
        datestartutcstring = '[' + datestartutc.strftime("%Y-%m-%dT%H:%M:%SZ") + ']'
        dateendutcstring = '[' + dateendutc.strftime("%Y-%m-%dT%H:%M:%SZ") + ']'
        try:
            r = requests.get(self.cwUrl + 'schedule/entries?pageSize=1000&conditions=member/identifier="' + member + '" and dateStart>' + datestartutcstring + ' and dateEnd<' + dateendutcstring, headers=self.cwHeaders)
            r.raise_for_status()
        except:
            print(r.text)
            raise
        # Fix the UTC difference
        schedule = r.json()
        for entry in schedule:
            datestartutc = arrow.get(entry['dateStart']).datetime - timedelta(minutes=self.cwTzUTCdiff)
            dateendutc = arrow.get(entry['dateEnd']).datetime - timedelta(minutes=self.cwTzUTCdiff)
            entry['dateStart'] = '[' + datestartutc.strftime("%Y-%m-%dT%H:%M:%SZ") + ']'
            entry['dateEnd'] = '[' + dateendutc.strftime("%Y-%m-%dT%H:%M:%SZ") + ']'
        return schedule

    # Get all time entries for member between dateStart and dateEnd and return as JSON.
    # member is the CW user name
    # dateStart and dateEnd have this format: [2017-09-04T00:00:00Z]
    # (dateStart and dateEnd arguments are optional - will result in today)
    def get_timeEntries(self, member, dateStart="[" + date.today().isoformat() + "T00:00:00Z]", dateEnd="[" + date.today().isoformat() + "T23:59:59Z]"):
        # subtract difference to UTC timezone
        datestartutc = arrow.get(dateStart).datetime + timedelta(minutes=self.cwTzUTCdiff)
        dateendutc = arrow.get(dateEnd).datetime + timedelta(minutes=self.cwTzUTCdiff)
        # format to String object for URL
        datestartutcstring = '[' + datestartutc.strftime("%Y-%m-%dT%H:%M:%SZ") + ']'
        dateendutcstring = '[' + dateendutc.strftime("%Y-%m-%dT%H:%M:%SZ") + ']'
        try:
            r = requests.get(self.cwUrl + 'time/entries?pageSize=1000&conditions=member/identifier="' + member + '" and timeStart>=' + datestartutcstring + ' and timeEnd<=' + dateendutcstring, headers=self.cwHeaders)
            r.raise_for_status()
        except:
            print(r.text)
            raise
        # Fix the UTC difference
        times = r.json()
        for entry in times:
            datestartutc = arrow.get(entry['dateStart']).datetime - timedelta(minutes=self.cwTzUTCdiff)
            dateendutc = arrow.get(entry['dateEnd']).datetime - timedelta(minutes=self.cwTzUTCdiff)
            entry['dateStart'] = '[' + datestartutc.strftime("%Y-%m-%dT%H:%M:%SZ") + ']'
            entry['dateEnd'] = '[' + dateendutc.strftime("%Y-%m-%dT%H:%M:%SZ") + ']'
        return times
