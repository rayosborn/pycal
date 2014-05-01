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
CGI script to update web pages at the start of a new day.
"""

from pycal.PyCal import CalendarError
from pycal.Utilities import Today
from pycal.PageModule import Page
from pycal.Utilities import PreviousMonth, NextMonth, MonthDays
import sys

def main():

    try:
        if len(sys.argv) > 2:
            y = int(sys.argv[1])
            m = int(sys.argv[2])
            if len(sys.argv) == 4:
                d = int(sys.argv[3])
            else:
                d = None
            format(y, m, d)
        else:
            year, month = Today()[0:2]
            for day in MonthDays(year, month):
                format(year, month, day)
            format(year, month)
            y, m = PreviousMonth(year, month)
            for d in MonthDays(y, m):
                format(y, m, d)
            y, m = NextMonth(year, month)
            for d in MonthDays(y, m):
                format(y, m, d)
    except ValueError, CalendarError:
        pass

def format(y, m, d=None):
    p = Page(y, m, d)
    p.PutEvents()
    p.Format()
    p.Format(private=True)

if __name__ == "__main__":
    main()



