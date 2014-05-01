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
# $Id: EditEvent.py,v 1.3 2004/03/28 23:02:53 osborn Exp $
#
"""
CGI script to modify a calendar event.
"""

from pycal.PyCal import CalendarError
from pycal.Event import Event
from pycal.GetModule import GetEditors
from pycal.PrintModule import LoginPage, ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user == "admin" or user in GetEditors():
            if form.has_key("ID"):
                e = Event(form["ID"])
            else:
                raise CalendarError, "Cannot edit non-existent event"
            print e.EditPage()
        else:
            print LoginPage(script="EditEvent.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



