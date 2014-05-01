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
# $Id: CurrentMonth.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#
"""
CGI script to view the calendar.
"""

from pycal.PyCal import *
from pycal.CGImodule import CGIprintHeader, CGIgetForm
from pycal.PrintModule import ReducedMonth, CalendarTitle
from pycal.Utilities import Today
import pycal.HTML as HTML

def main():

    try:
        CGIprintHeader()
        form = CGIgetForm()
        if form.has_key("year") and form.has_key("month"):
            year, month = int(form["year"]), int(form["month"])
        else:
            year, month = Today()[0:2]
        title = "%s - %s" % (calendarName, CalendarTitle(year, month))
        table = HTML.Table([170], class_="transparent", cellspacing="0", 
                           cellpadding="0", align="center")
        table.Add(HTML.Row(HTML.Cell(ReducedMonth(year, month, links=True), 
                                     class_="transparent")))
        print HTML.FramePage(title, table, width=172)
    except CalendarError, errorText:
        print errorText

if __name__ == "__main__":
    main()



