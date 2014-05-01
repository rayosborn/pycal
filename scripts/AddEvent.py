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
# $Id: AddEvent.py,v 1.2 2004/03/28 22:59:50 osborn Exp $
#
"""
CGI script to add a calendar event.
"""

from pycal.PyCal import CalendarError
from pycal.Event import Event
from pycal.GetModule import GetEditors
from pycal.PrintModule import LoginPage, ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm
import time

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user == "admin" or user in GetEditors():
            new_event = Event()
            year, month, day = None, None, None
            if form.has_key("year"):
                date = form["year"]
                if form.has_key("month"):
                    date += " "+form["month"]
                    if form.has_key("day"):
                        date += " "+form["day"]
                        new_event.start = time.strptime(date, "%Y %m %d")
                    else:
                        new_event.start = time.strptime(date, "%Y %m")
                else:
                    new_event.start = time.strptime(date, "%Y")
            new_event.end = new_event.start
            new_event.reservation["start"] = new_event.start
            new_event.reservation["end"] = new_event.end
            new_event.reservation["option"] = "Same as Event"
            new_event.pattern = "Once Only"
            print new_event.EditPage()
        else:
            print LoginPage(script="AddEvent.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



