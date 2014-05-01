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
# $Id: AddEditor.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#
"""
CGI script to remove an email address from the notification list.
"""

from pycal.PyCal import CalendarError
from pycal.Event import Event
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.PrintModule import AdminPage

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if form.has_key("ID"):
            if form.has_key("email"):
                e = Event(form["ID"])
                if e.repeats:
                    for repeat in e.repeats:
                        Event(repeat).RemoveNotification(form["email"])
                else:
                    e.RemoveNotification(form["email"])
                print e.EventView("Email removed from notification list")
            else:
                raise CalendarError, "No email address given"
        else:
            raise CalendarError, "No event specified"
    except CalendarError, errorText:
        print AdminPage(errorText)

if __name__ == "__main__":
    main()



