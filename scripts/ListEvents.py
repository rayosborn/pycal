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
# $Id: ListEvents.py,v 1.1 2004/05/08 15:20:58 osborn Exp $
#
"""
CGI script to list events according to certain criteria.
"""

from pycal.PyCal import CalendarError
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.PrintModule import ListPage, ErrorPage
from pycal.Utilities import Today, DayLength, ReadDate
import pycal.HTML as HTML

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        type, status, layout = None, None, None
        if form.has_key("type"):
            type = form["type"]
            if not isinstance(type, list):
                type = [type]
        else:
            type = ["Event", "Special", "Banner", "Holiday"]
        if form.has_key("setup"):
            if form["setup"] == "setup":
                type = ["Setup"]
        if form.has_key("status"):
            status = form["status"]
            if not isinstance(status, list):
                status = [status]
        else:
            status = ["Approved"]
        if form.has_key("layout"):
            layout = form["layout"]
        location, resource, category = None, None, None
        if form.has_key("location"):
            if form["location"] <> "Location...":
                location = form["location"]
        if form.has_key("resource"):
            if form["resource"] <> "Resource...":
                resource = form["resource"]
        if form.has_key("category"):
            if form["category"] <> "Category...":
                category = form["category"]
        if form.has_key("startyear") and form.has_key("startmonth") and \
           form.has_key("startday"):
            start = ReadDate(form["startyear"], form["startmonth"], 
                             form["startday"])
        else:
            start = Today()
        if form.has_key("length"):
            try:
                length = int(form["length"])
            except TypeError:
                raise CalendarError, "Invalid entry for number of days"
        else:
            length = 14
        year, month, day = start[0:3]
        print ListPage(year, month, day, length, type, status, layout,
                      location, resource, category)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



