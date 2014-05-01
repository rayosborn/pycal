#!/usr/bin/env python

# PyCal - Python web calendar
#
# Copyright (C) 2004-2008 Ray Osborn
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
"""
CGI script to update web pages at the start of a new day.
"""

import os
from pycal.PyCal import homeDir
from pycal.PageModule import Page

def main():
    years = GetDirectories(homeDir)
    for year in years:
        months = GetDirectories(year)
        for month in months:
#            PurgeDirectory(month)
            ResetMonth(month)
            days = GetDirectories(month)
            for day in days:
#                PurgeDirectory(day)
                ResetDay(day)

def GetDirectories(dir):
    """Return a list of date subdirectories in this directory."""
    paths = os.listdir(dir)
    paths.sort()
    dirs = []
    for path in paths:
        try:
            n = int(path)
            dirs.append(os.path.join(dir, path))
        except ValueError:
            pass
    return dirs

def ResetMonth(dir):
    """Reset the page cache for the given month."""
    if "pages.db" in os.listdir(dir):
        y, m = map(int, dir.replace("%s/" % homeDir,"").split('/'))
        print y, m
        FormatPage(y, m)

def ResetDay(dir):
    """Reset the page cache for the given day."""
    if "pages.db" in os.listdir(dir):
        y, m, d = map(int, dir.replace("%s/" % homeDir,"").split('/'))
        print y, m, d
        FormatPage(y, m, d)

def PurgeDirectory(dir):
    """Remove obsolete page caches."""
    if "pages.pickle" in os.listdir(dir):
        print os.path.join(dir, "pages.pickle")
        os.remove(os.path.join(dir, "pages.pickle"))
    if "pages.db~" in os.listdir(dir):
        print os.path.join(dir, "pages.db~")
        os.remove(os.path.join(dir, "pages.db~"))
    
def FormatPage(y, m, d=None):
    p = Page(y, m, d)
    p.PutEvents()
    p.Format()
    p.Format(private=True)
    
    
if __name__=="__main__":
    main()


