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
# $Id: ViewCalendar.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#
"""
CGI script to view the calendar.
"""

from pycal.PyCal import CalendarError
from pycal.PrintModule import DayView, MonthView, YearView
from pycal.PrintModule import ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.Utilities import Today

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        year, month, day = (None, None, None)
        try:
            if form.has_key("day"):
                day = int(form["day"])
            if form.has_key("month"):
                month = int(form["month"])
            if form.has_key("year"):
                year = int(form["year"])
        except ValueError:
            raise CalendarError, "Invalid date"
        if day:
            print DayView(year, month, day)
        elif month:
            print MonthView(year, month)
        elif year:
            print YearView(year)
        else:
            year, month, day = Today()
            print MonthView(year, month)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



