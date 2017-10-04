# Connectwise Manage API - Python Library
This Python 2.7 Library provides a wrapper for the Connectwise Manage API v4.6 rel 3.0. (Documentation: https://developer.connectwise.com/Manage/Developer_Guide)

Base-URL: https://{connectwiseSite}/v4_6_release/apis/3.0/

## Usage
`>>> import cwmanage`

`>>> cw = cwmanage.api("HOSTNAME","TOKEN")`  # To get your TOKEN follow instructions here: https://gist.github.com/bersfo/12efa79de156aa6f96d80ff14a060822

`>>> cw.get_companies()` # This should return a JSON object including the first 1000 companies in your CW Manage instance.

`>>> cw.get_members()` # This should return a JSON object including the first 1000 members in your CW Manage instance.

`>>> cw.get_timeEntries("MEMBER","[2017-09-21T00:00:00Z]","[2017-09-22T00:00:00Z]")` # This should return a JSON object including all time entries for MEMBER on September 21, 2017.

`>>> cw.get_schedule("MEMBER","[2017-09-21T00:00:00Z]","[2017-09-22T00:00:00Z]")` # This should return a JSON object including all sheduled entries for MEMBER on September 21, 2017.

## ToDo
The Connectwise Manage API offers many more endpoints and methods. I will add those as I need them for my projects. If you'd like to contribute, please open a pull request.

If you find any issues with the methods provided so far, please open an issue.