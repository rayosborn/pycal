#!/usr/bin/env python

# PyCal - Python web calendar
#
# Copyright (C) 2004-6 Ray Osborn
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
# $Id: ModifyEvent.py,v 1.5 2005/06/12 04:30:42 osborn Exp $
#
"""
CGI script to modify a calendar event.
"""

from pycal.PyCal import *
from pycal.Editor import Contact
from pycal.Event import Event, TemporaryEvent
from pycal.GetModule import GetEditors, GetEditor, GetSupervisors, GetContacts
from pycal.PrintModule import LoginPage, ErrorPage, DayView
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.Utilities import ReadDate, ReadTime, Today, MakeRepeats, Now, AddDay
from pycal.Utilities import IDexists, IDdate, ConvertCRLFs

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user == "admin" or user in GetSupervisors():
            supervisor = True
        else:
            supervisor = False
        if user is None:
            print LoginPage(script="ModifyEvent.py", form=form)
            return
        if form.has_key("ID"):
            ID = form["ID"]
            if not IDexists(ID):
                raise CalendarError, "No event to edit"
            if ID.find("tmp") >= 0:
                e = TemporaryEvent(ID)
            else:
                e = TemporaryEvent()
                e.Copy(Event(ID))
                e.oldID = ID
                e.oldDate = e.start[0:3]
        else:
            e = TemporaryEvent()
        if form.has_key("title"):
            e.title = form["title"]
        if form.has_key("type"):
            e.type = form["type"]
        else:
            e.type = "Event"
        if form.has_key("description"):
            e.description = ConvertCRLFs(form["description"])
        else:
            e.description = ""
        if form.has_key("location"):
            if form["location"] == "Location...":
                e.location = ""
            else:
                e.location = form["location"]           
        try:
            if type == "Banner" or type == "Holiday":
                e.start = ReadTime(form["startyear"], form["startmonth"], 
                                   form["startday"], 12, 0, "AM")
                e.end = e.start
            else:
                e.start = ReadTime(form["startyear"], form["startmonth"], 
                                   form["startday"], form["starthour"], 
                                   form["startminute"], 
                                   form["startampm"].upper())
                e.end = ReadTime(form["startyear"], form["startmonth"], 
                                 form["startday"], form["endhour"], 
                                 form["endminute"], 
                                 form["endampm"].upper(),
                                 end=True)
        except KeyError:
            if not hasattr(e, "oldID"):
                raise CalendarError, "Invalid date/time entry"
        if form.has_key("cancel"):
            if e.start:
                y, m, d = e.start[0:3]
            else:
                y, m, d = Today()
            print DayView(y, m, d)
            return
        if form.has_key("name") and form["name"] <> "Name...":
            if form["name"] in GetEditors(name=True):
                c = GetEditor(form["name"])
            else:
                c = Contact(form["name"])
            e.organizer = c.name
            e.phone = c.phone
            e.email = c.email
        elif form.has_key("organizer"):
            e.organizer = form["organizer"]
            if form.has_key("phone") and form.has_key("email"):
                e.phone = form["phone"]
                e.email = form["email"]
            else:
                if e.organizer in GetEditors(name=True):
                    c = GetEditor(e.organizer)
                elif e.organizer in GetContacts():
                    c = Contact(e.organizer)
                else:
                    c = None
                if form.has_key("phone"):
                    e.phone = form["phone"]
                elif c:
                    e.phone = c.phone
                if form.has_key("email"):
                    e.email = form["email"]
                elif c:
                    e.email = c.email
        else:
            e.organizer = ""
        try:
            e.reservation["option"] = form["reserve"]
            if e.reservation["option"] == "Same as Event":
                e.reservation["start"] = e.start
                e.reservation["end"] = e.end
            elif e.reservation["option"] == "All Day":
                e.reservation["start"] = ReadTime(form["startyear"], 
                                                  form["startmonth"], 
                                                  form["startday"],
                                                  "12", "00", "AM")
                e.reservation["end"] = ReadTime(form["startyear"], 
                                                form["startmonth"], 
                                                form["startday"],
                                                "12", "00", "AM", 
                                                end=True)
            else:
                e.reservation["start"] = ReadTime(form["startyear"], 
                                                  form["startmonth"], 
                                                  form["startday"],
                                                  form["resstarthour"], 
                                                  form["resstartminute"], 
                                                  form["resstartampm"].upper())
                e.reservation["end"] = ReadTime(form["startyear"], 
                                                form["startmonth"], 
                                                form["startday"],
                                                form["resendhour"], 
                                                form["resendminute"], 
                                                form["resendampm"].upper(),
                                                end=True)
                if e.reservation["start"] > e.start:
                    e.reservation["start"] = e.start
                if e.reservation["end"] < e.end:
                    e.reservation["end"] = e.end
        except KeyError:
            if not hasattr(e, "oldID"):
                raise CalendarError, "Invalid reservation time"
        if form.has_key("locations"):
            if isinstance(form["locations"], list):
                e.locations = form["locations"]
            else:
                e.locations = [form["locations"]]
            if "Locations..." in e.locations:
                e.locations.remove("Locations...")
        else:
            e.locations = []
        if e.location:
            try:
                e.locations.remove(e.location)
            except ValueError:
                pass
            e.locations.insert(0, e.location)
        if form.has_key("resources"): 
            if isinstance(form["resources"], list):
                e.resources = form["resources"]
            else:
                e.resources = [form["resources"]]
            if "Resources..." in e.resources:
                e.resources.remove("Resources...")
        else:
            e.resources = []
        if form.has_key("categories"): 
            if isinstance(form["categories"], list):
                e.categories = form["categories"]
            else:
                e.categories = [form["categories"]]
            if "Categories..." in e.categories:
               e.categories.remove("Categories...")
        else:
            e.categories = []
        if form.has_key("setup"):
            e.setup = ConvertCRLFs(form["setup"])
        else:
            e.setup = ""
        if form.has_key("status"):
            e.status = form["status"]
        if form.has_key("editor"): 
            e.editor = form["editor"]
        if form.has_key("pattern"):
            e.pattern = form["pattern"]
            if form["pattern"] <> "Once Only":
                e.number, e.final = None, None
                if form.has_key("number"):
                    e.number = int(form["number"])
                if form.has_key("endyear"):
                    e.final = ReadDate(form["endyear"], form["endmonth"],
                                       form["endday"])
                e.repeats = MakeRepeats(e.pattern, e.start, e.final, e.number)
            else:
                e.repeats = []
        elif form.has_key("repeat"):
            if form["repeat"] == "single":
                e.repeats = []
                e.pattern = "Once Only"
            elif form.has_key("repeats"):
                if isinstance(form["repeats"], list):
                    e.repeats = form["repeats"]
                else:
                    e.repeats = [form["repeats"]]
                if form["repeat"] == "future":
                    e.repeats = filter(lambda ID:IDdate(ID)>=Today(), e.repeats)
            else:
                e.repeats = []
        message = None
        if e.type <> "Banner" and e.type <> "Holiday" and e.end < e.start:
            message = "Warning: End of event precedes the start."
        elif e.type <> "Banner" and e.type <> "Holiday" and e.end == e.start:
            message = "Warning: Event has no duration."
        elif e.start < Now():
            message = "Warning: This event is in the past."
        elif not e.title:
            message = "Warning: No title given for event."
        if hasattr(e, "oldDate"):
            if e.oldDate <> e.start[0:3] and e.repeats:
                message = \
        "Warning: Changing the date will break the link with event repeats."
                e.repeats = []
                e.pattern = "Once Only"
        e.Store()
        print e.EventView(message=message, updating=True)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



