from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from sales_tool.models import Event

from datetime import datetime, timedelta
import pytz

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import UpdateView

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
redirect_uri='http://127.0.0.1:8000/'


def get_credentials():
    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES, redirect_uri) 
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: 
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main(request):
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    cest = pytz.timezone('Europe/Skopje')
    now = datetime.now(tz=cest) 
    timeMax = datetime(year=now.year, month=now.month, day=now.day, tzinfo=cest) + timedelta(days=90)
    timeMax = timeMax.isoformat()
    now = now.isoformat()
    print('Getting the upcoming 15 events')
    eventsResult = service.events().list(
        calendarId='laios.se_o4a9rd1std8vnds7j7qiu3rm7k@group.calendar.google.com', timeMin=now, timeMax=timeMax, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])


    p = []
    if not events:
        print('No upcoming events found.')
    for ev in events:
        if not Event.objects.filter(uniqueTempKey=ev['id']):
            d = 'No description'
            try:
                d= ev['description']
            except:
                print ('No description in dictionary for this object')
            p.append(Event(uniqueTempKey=ev['id'], title=ev['summary'], body=d, date=ev['start'].get('dateTime', ev['start'].get('date'))))

    Event.objects.bulk_create(
    p
    )
    #print(p)
    res = Event.objects.all()
    return render(request, 'sales_tool/calendar.html', {'event': res})

if __name__ == '__main__':
    main()

class EventUpdate(UpdateView):
    model = Event
    fields = ['saleDocLink','salePointsCreated','researchDone','internalMeetingCreated']