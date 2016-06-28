import os
import requests
import sqlite3
from models import det_ax, cli_ax
import datetime
from django.utils.dateformat import format
import time
import re

def time_check():
    latest_entry = det_ax.objects.order_by('-time')[0]
    print "Last organization data recorded into the database: " + latest_entry.org
    print "Last (clicky) time data was recorded into the database: " + latest_entry.timep
    print "Last (unix) time data was recorded into the database: " + latest_entry.time
    print "Last session ID data recorded into the database: " + latest_entry.si

    x = datetime.datetime.now()
    current_time = time.mktime(x.timetuple())
    z = (int(current_time) - int(latest_entry.time)) / (60*60*24)
    y = max(0, z+1)
    print "Acquiring data from %s day(s) ago to update database" %(y-1)
    populate(y)

def populate(time):
    for s in range (0,time):
        url = 'https://api.clicky.com/api/stats/4?site_id=100716069&sitekey=93c104e29de28bd9&type=visitors-list'
        date = '&date=%s-days-ago' %s
        limit = '&limit=all'
        output = '&output=json'
        total = url+date+limit+output
        r = requests.get(total, verify=False)
        data = r.json()
        print "Starting population script:  %s" %(total)
        for item in data[0]['dates'][0]['items']:
            if item.has_key("geolocation"):
                geol = item["geolocation"]
            else:
                geol = ""
            if item.has_key("organization"):
                org = item["organization"]
            else:
                org = ""
            si = item["session_id"]
            ip = item["ip_address"]
            ip_float = float((ip).replace(".",""))
            while ip_float < 10**11:
                ip_float = ip_float *10
            time = item["time"]
            timep = item["time_pretty"]
            reg1 = timep
            reg2 = re.sub(r' ',',',reg1)
            reg3 = re.sub(r',,',',',reg2)
            reg4 = re.split(',', reg3)
            month = reg4[1]
            year = reg4[3]
            add_detail(geol, org, si, ip, ip_float, time, timep, month, year)
            add_client(org)

def add_detail(geol, org, si, ip, ip_float, time, timep, month, year):
    entry = det_ax.objects.update_or_create(geol=geol, org=org, si=si, ip=ip, ip_float=ip_float, time=time, timep=timep, month=month, year=year)[0]
    return entry

def add_client(org):
    entry = cli_ax.objects.update_or_create(org=org)[0]
    return entry

time_check()
