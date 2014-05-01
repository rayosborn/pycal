#!/usr/bin/env python

# PyCal - Python web calendar
#
# Copyright (C) 2007 Ray Osborn
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
# $Id$
#
"""
Script to transfer an ASCII pickle file derived from a BSDDB database 
into the database format chosen by 'shelve'.
"""

import os
import shelve
import pickle

from pycal.PyCal import homeDir

def main():
    """Dump copies of all the calendar databases"""
    convert("contacts")
    convert("editors")
    convert("logs")
    convert("options")
    convert("updates")
    years = GetDirectories(homeDir)
    for year in years:
        UnpickleDirectory(year)
        months = GetDirectories(year)
        for month in months:
            UnpickleDirectory(month)
            days = GetDirectories(month)
            for day in days:
                UnpickleDirectory(day)
                events = GetDirectories(day)
                for event in events:
                    UnpickleDirectory(event)

def convert(database, dir=homeDir):
    """Convert an ASCII pickle file into a 'shelve' database."""
    pickleFile = open(os.path.join(dir, "%s.pickle" % database))
    input = pickle.load(pickleFile)
    pickleFile.close()
    os.rename(os.path.join(dir, "%s.db" % database),
              os.path.join(dir, "%s.db~" % database))
    output = shelve.open(os.path.join(dir, "%s.db" % database))
    for key in input.keys():
        output[key] = input[key]
    output.close()
    
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

def UnpickleDirectory(dir):
    if "pages.pickle" in os.listdir(dir):
        convert("pages", dir)
    if "events.pickle" in os.listdir(dir):
        convert("events", dir)

if __name__=="__main__":
    main()
