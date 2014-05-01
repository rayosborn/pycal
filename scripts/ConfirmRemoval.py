#!/usr/bin/env python

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
# $Id: ConfirmRemoval.py,v 1.2 2004/04/23 03:05:12 osborn Exp $
#
"""
CGI script to confirm removal of a calendar event.
"""

from pycal.PyCal import *
from pycal.Event import Event, TemporaryEvent
from pycal.GetModule import GetEditors, GetSupervisors
from pycal.PrintModule import DayView, LoginPage, ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.Utilities import PathDate, IDdate, Today
import os

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user == "admin" or user in GetSupervisors():
            supervisor = True
        else:
            supervisor = False
        if user:
            if form.has_key("ID"):
                e = Event(form["ID"])
                if form.has_key("cancel"):
                    print e.EventView()
                    return
                if e.status == "Approved" and not supervisor:
                    message = "Not authorized to remove an approved event"
                    print e.EventView(message)
                    return
                if form.has_key("repeat") and form["repeat"] <> "single":
                    if form["repeat"] == "future":
                        repeats = filter(lambda ID:IDdate(ID)>=Today(), 
                                         e.repeats)
                        e.AddLog("Future repeated events removed")
                    else:
                        repeats = e.repeats
                        e.AddLog("Repeated events removed")
                    for ID in repeats:
                        Event(ID).Remove()
                else:
                    e.AddLog("Event removed")
                    e.Remove()
                e.UpdatePages()
                y, m, d = e.start[0:3]
                print DayView(y, m, d, updated=True)
        else:
            print LoginPage(script="ConfirmRemoval.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



