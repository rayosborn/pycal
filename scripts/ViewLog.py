#!/usr/bin/env python

# PyCal - Python web calendar
#
# Copyright (C) 2004-5 Ray Osborn
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
# $Id: ViewLog.py,v 1.1 2006/12/30 02:24:47 rosborn Exp $
#

"""
CGI script to print the log entries for an event.
"""

from pycal.PyCal import CalendarError
from pycal.Event import Event
from pycal.PrintModule import LoginPage, ErrorPage
from pycal.CGImodule import CGIgetForm, CGIlogin
from pycal.Utilities import IDexists

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if form.has_key("ID"):
            if IDexists(form["ID"]):
                e = Event(form["ID"])
                if user:
                    print e.LogPage()
                else:
                    print LoginPage(script="ViewLog.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__=="__main__":
    main()

