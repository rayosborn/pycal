# PyCal - Python web calendar
#
# Copyright (C) 2004 Ray Osborn
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# $Id: GetModule.py,v 1.7 2004/07/30 16:47:36 osborn Exp $
#
"""PyCal: Python web calendar 

Modules to extract information from the editor and/or event databases.
"""

from pycal.PyCal import *
import Editor
import Event
import CGImodule
import DatabaseModule
import OptionModule
from Utilities import DatePath
import os

def GetEditors(name=False):
    """Return a list of calendar editors."""
    editorList = DatabaseModule.Values("editors")
    editorList.sort()
    if name:
        editors = map(lambda e: e.name, editorList)
    else:
        editors = map(lambda e: e.user, editorList)
    return editors

def GetSupervisors(name=False):
    """Return a list of calendar supervisors."""
    editors = DatabaseModule.Values("editors")
    supervisors = []
    if name:
        editors.sort()
        for e in editors:
            if e.authority == "Supervisor":
                supervisors.append(e.name)
    else:
        for e in editors:
            if e.authority == "Supervisor":
                supervisors.append(e.user)
        supervisors.sort()
    return supervisors

def GetEditor(name):
    """Return the Editor object identified by 'name'"""
    for user in GetEditors():
        e = Editor.Editor(user)
        if e.name == name: 
            return e
        
def GetContacts():
    """Return a list of calendar contacts."""
    contactList = DatabaseModule.Values("contacts")
    contactList.sort()
    contacts = map(lambda c: c.user, contactList)
    return contacts

def GetOrganizers():
    """Return a list of calendar organizers."""
    organizerList = DatabaseModule.Values("editors") +\
                    DatabaseModule.Values("contacts")
    organizerList.sort()
    organizers = map(lambda o: o.name, organizerList)
    return organizers

def GetEditorEmails():
    """Return a list of editor email addresses."""
    editorList = DatabaseModule.Values("editors")
    editorList.sort()
    return map(lambda e: e.email, editorList)    

def GetEvents(year, month, day, type=None, status=None,
              location=None, resource=None, category=None):
    """Return a list of events for the given day."""
    user = CGImodule.CGIgetUser()
    if user:
        if type == None: 
            type = ["Event", "Special", "Banner", "Holiday", "Private", 
                    "Setup"]
        if status == None: 
            status = ["Approved", "Requested"]
    else:
        type = ["Event", "Special", "Banner", "Holiday"]
        status = ["Approved"]
    import PageModule
    events = PageModule.Page(year, month, day).GetEvents()
    if events:
        events = filter(lambda e: e["status"] in status, events)
        events = filter(lambda e: e["type"] in type or 
                                  ("Setup" in type and e["setup"]), events)
        if location:
            events = filter(lambda e: location in e["locations"], events)
        if resource:
            events = filter(lambda e: resource in e["resources"], events)
        if category:
            events = filter(lambda e: category in e["categories"], events)
    return events

def GetEventIDs(year, month, day):
    """Return a list of event IDs for the given day."""
    return map(lambda e: e["ID"], GetEvents(year, month, day))

def GetCache(year, month, day):
    """Return a dictionary containing a summary of all the day's events."""
    eventDir = DatePath(year, month, day)
    IDs = []
    try:
        files = os.listdir(os.path.join(homeDir, eventDir))
        files.sort()
        for file in files:
            try:
                number = int(file)
                IDs.append(os.path.join(eventDir, file))
            except ValueError:
                pass
    except OSError:
        pass
    events = map(Event.Event, IDs)
    events.sort()
    return map(lambda e: {"ID": e.ID, 
                          "status": e.status, 
                          "type": e.type,
                          "title": e.title,
                          "location": e.location,
                          "start": e.start,
                          "end": e.end,
                          "repeats": e.repeats,
                          "reservation": e.reservation,
                          "setup": e.setup,
                          "locations": e.locations,
                          "resources": e.resources,
                          "categories": e.categories}, events)

def GetNextEvent(eventDir):
    """Return the event directory for a new event."""
    IDs = []
    try:
        files = os.listdir(os.path.join(homeDir, eventDir))
        files.sort()
        for file in files:
            try:
                IDs.append(int(file))
            except ValueError:
                pass
    except OSError:
        pass
    if len(IDs) == 0:
        return 1
    elif IDs[-1] < 999:
        return IDs[-1] + 1
    else:
        raise CalendarError, "Max. number of events for database"

def GetLocations():
    """Return a list of locations available for scheduling."""
    list = OptionModule.Read("locations").keys()
    list.sort()
    return list

def GetResources():
    """Return a list of resources available for scheduling."""
    list = OptionModule.Read("resources").keys()
    list.sort()
    return list

def GetCategories():
    """Return a list of event categories."""
    list = OptionModule.Read("categories").keys()
    list.sort()
    return list
