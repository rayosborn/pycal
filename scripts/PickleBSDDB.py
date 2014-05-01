#!/usr/bin/python2.2

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
Script to convert a BSDDB database to an ASCII pickle file.
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
        PickleDirectory(year)
        months = GetDirectories(year)
        for month in months:
            PickleDirectory(month)
            days = GetDirectories(month)
            for day in days:
                PickleDirectory(day)
                events = GetDirectories(day)
                for event in events:
                    PickleDirectory(event)

def convert(database, dir=homeDir):
    """Convert a BSDDB database to an ASCII pickle file."""
    input = shelve.open(os.path.join(dir, "%s.db" % database))
    output = {}
    for key in input.keys():
        output[key] = input[key]
    input.close()
    pickleFile = open(os.path.join(dir, "%s.pickle" % database), "w")
    pickle.dump(output, pickleFile)

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

def PickleDirectory(dir):
    if "pages.db" in os.listdir(dir):
        convert("pages", dir)
    if "events.db" in os.listdir(dir):
        convert("events", dir)

if __name__=="__main__":
    main()
