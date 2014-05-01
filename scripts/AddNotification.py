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
CGI script to add an email address to the notification list.
"""

from pycal.PyCal import CalendarError
from pycal.Event import Event
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.PrintModule import ErrorPage
from pycal.Utilities import IsEmail

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if form.has_key("ID"):
            if form.has_key("email"):
                e = Event(form["ID"])
                emails = form["email"].split()
                for email in emails:
                    if not IsEmail(email):
                        raise CalendarError, "Invalid email address"
                if e.repeats:
                    for repeat in e.repeats:
                        for email in emails:
                            Event(repeat).AddNotification(email)
                else:
                    for email in emails:
                        e.AddNotification(email)
                print e.EventView("Email added to the notification list")
            else:
                raise CalendarError, "No email address given"
        else:
            raise CalendarError, "No event specified"
    except CalendarError, errorText:
        if e:
            print e.EventView(errorText)
        else:
            print ErrorPage(errorText)

if __name__ == "__main__":
    main()



