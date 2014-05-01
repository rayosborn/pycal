#!/usr/bin/env python

# PyCal - Python web calendar
#
# Copyright (C) 2004-2006 Ray Osborn
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
# $Id: ApproveEvent.py,v 1.4 2006/12/30 02:23:15 rosborn Exp $
#
"""
CGI script to approve a calendar event.
"""

from pycal.PyCal import *
from pycal.Event import Event
from pycal.GetModule import GetSupervisors
from pycal.PrintModule import LoginPage, ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user == "admin" or user in GetSupervisors():
            if form.has_key("ID"):
                primary_event = Event(form["ID"])
                primary_event.status = "Approved"
                primary_event.AddLog("Event approved")
                primary_event.Store()
                if primary_event.repeats:
                    for repeat in primary_event.repeats:
                        repeat_event = Event(repeat)
                        if repeat <> form["ID"]:
                            repeat_event.AddLog("Event approved", save=False)
                            repeat_event.status = "Approved"
                            repeat_event.Store()
                primary_event.UpdatePages()
                print primary_event.EventView()
            else:
                raise CalendarError, "No event specified"
        else:
            print LoginPage(script="ApproveEvent.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__=="__main__":
    main()

