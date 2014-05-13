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
# $Id: PyCal.py,v 1.5 2006/12/28 13:24:33 rosborn Exp $
#
"""PyCal: Python web calendar 

PyCal consists of a set of Python CGI scripts that provide a
comprehensive web-based calendar administration system.
"""

import os
import calendar
import re

__version__ = "0.3.0"
__author__ = "Ray Osborn <RayOsborn@mac.com>"

from config import *

# File paths and URL's
imgDir = os.path.join(webDir, "images")
imgURL = webURL+"/images"
# calendar links for the HTML footer
loginLink = '<a href="%s/login.html">Login Page</a>' % webURL

def yearNumber(x):
    return "%d" % x
def monthNumber(x):
    return calendar.month_name[x]
def dayNumber(x):
    return "%d" % x
def hourNumber(x):
    return "%d" % x
def minuteNumber(x):
    return "%02d" % x

yearList = map(yearNumber, range(2004, 2015))
monthList = map(monthNumber, range(1,13))
dayList = map(dayNumber, range(1,32))
hourList = map(hourNumber, range(1,13))
minuteList = map(minuteNumber, range(60))
meridiemList = ["am", "pm"]

reTitle = re.compile(r".*<h1>(.*?)</h1>.*",re.DOTALL)


class CalendarError(Exception):
    """Calendar error class."""
    pass

          


