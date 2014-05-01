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
# $Id: CheckUpdates.py,v 1.1 2004/08/07 13:10:07 osborn Exp $
#
"""
CGI script to check for page updates.
"""

import sys
sys.path.append("/home/dgfumc/www/cgi-bin/calendar")
from pycal.PyCal import CalendarError
import pycal.CGImodule as CGImodule
import pycal.GetModule as GetModule
from pycal.Event import Event
from pycal.Utilities import MonthDays, Today

def main():

    try:
        if len(sys.argv) > 2:
            year = int(sys.argv[1])
            month = int(sys.argv[2])
        else:
            year, month = Today()[0:2]
        CGImodule.user = "admin"
        for day in MonthDays(year, month):
            IDs=map(lambda x:x["ID"], GetModule.GetEvents(year, month, day))
            for ID in IDs:
                if Event(ID).email == "":
                    print ID, Event(ID).title
    except CalendarError, errorText:
        print "%s/%s: %s" % (year, month, errorText)

if __name__ == "__main__":
    main()


