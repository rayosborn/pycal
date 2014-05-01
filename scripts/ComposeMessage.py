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
# $Id: RemoveEvent.py,v 1.2 2004/04/23 03:13:35 osborn Exp $
#
"""
CGI script to compose an email message to an event organizer.
"""

from pycal.PyCal import CalendarError
from pycal.Event import Event
from pycal.PrintModule import ErrorPage
from pycal.CGImodule import CGIgetForm, CGIlogin
from pycal.Utilities import IDexists

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if form.has_key("ID"):
            ID = form["ID"]
            if IDexists(ID):
                e = Event(ID)
                print e.MessagePage()
            else:
                raise CalendarError, "Event does not exist"
        else:
            raise CalendarError, "No calendar event specified"
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



