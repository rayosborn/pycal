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
# $Id: CurrentList.py,v 1.1 2004/04/24 12:07:44 osborn Exp $
#
"""
CGI script to view the calendar.
"""

from pycal.PyCal import *
from pycal.CGImodule import CGIprintHeader, CGIgetForm
from pycal.PrintModule import CurrentList
from pycal.Utilities import Today
import pycal.HTML as HTML

def main():

    try:
        CGIprintHeader()
        form = CGIgetForm()
        if form.has_key("length"):
            length = int(form["length"])
        else:
            length = 14
        if form.has_key("type"):
            type = form["type"]
            if not isinstance(type, list):
                type = [type]
        else:
            type = ["Event", "Special", "Banner", "Holiday"]
        if form.has_key("status"):
            status = form["status"]
            if not isinstance(status, list):
                status = [status]
        else:
            status = ["Approved"]
        location, resource, category = None, None, None
        if form.has_key("location"):
            location = form["location"]
        if form.has_key("resource"):
            resource = form["resource"]
        if form.has_key("category"):
            category = form["category"]
        year, month, day = Today()
        title = "%s Event List" % calendarAbbr
        content = HTML.Div(style="font-size:0.85em")
        content.Add(HTML.Para(CurrentList(year, month, day, length, type, 
                                          status, location, resource, 
                                          category)))
        print HTML.FramePage(title, content, width=172)
    except CalendarError, errorText:
        print errorText

if __name__ == "__main__":
    main()



