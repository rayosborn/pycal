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

import os
from pycal.PyCal import CalendarError
import pycal.OptionModule as OptionModule
from pycal.PageModule import Page
from pycal.Utilities import MonthDays

def main():

    #Check if this script is already running in another process
    try:
        import psutil
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1].endswith('CheckUpdates.py'):
                    if process.pid != os.getpid():
                        return
            except IndexError, psutil.NoSuchProcess:
                pass
    except ImportError:
        pass

    try:
        days = OptionModule.Read("updates").keys()
        days.sort()
        months = []
        for (y, m, d) in days:
            format(y, m, d)
            OptionModule.Delete("updates", (y, m, d))
            if (y, m) not in months:
                months.append((y, m))
        for (y, m) in months:
            try:
                format(y, m)
            except CalendarError:
                for d in MonthDays(y, m):
                    Page(y, m, d).PutEvents()
                format(y, m)
    except CalendarError, errorText:
        print "%s/%s/%s: %s" % (`y`, `m`, `d`, errorText)

def format(y, m, d=None):
    p = Page(y, m, d)
    p.PutEvents()
    p.Format()
    p.Format(private=True)

if __name__ == "__main__":
    main()



