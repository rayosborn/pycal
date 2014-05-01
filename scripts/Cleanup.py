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
# $Id: Cleanup.py,v 1.1 2004/10/04 18:28:47 osborn Exp $
#
"""
CGI script to remove temporary files and old backups.
"""

from pycal.PyCal import CalendarError, homeDir, backupDir
import os
import stat
import time

def main():

    try:
        #Clean up the temporary directory of any files more than a day old
        PurgeTemporaryEvents()
        #Remove backups made more than a week ago
        PurgeBackups()
        #Remove redundant page caches for days where there are no events
        PurgeCalendar()
 
    except CalendarError:
        pass

def PurgeTemporaryEvents():
    """Remove all temporary events more than a day old."""
    os.chdir(os.path.join(homeDir, "tmp"))
    dirs = os.listdir(os.getcwd())
    for dir in dirs:
        files = os.listdir(dir)
        for file in files:
            creationTime = os.stat(os.path.join(dir, file))[stat.ST_ATIME]
            if time.time() - creationTime > 24*60*60:
                os.remove(os.path.join(dir, file))
        if not os.listdir(dir):
            os.rmdir(dir)
    

def PurgeBackups():
    """Remove all backup files more than a week old."""
    os.chdir(backupDir)
    files = os.listdir(os.getcwd())
    for file in files:
        if file.startswith("calendar") and file.endswith("tar.gz"):
            creationTime = os.stat(file)[stat.ST_ATIME]
            if time.time() - creationTime > 7*24*60*60:
                os.remove(file)
    
def PurgeCalendar():
    """Remove all dates that contain no events."""
    years = GetDirectories(homeDir)
    for year in years:
        months = GetDirectories(year)
        for month in months:
            days = GetDirectories(month)
            for day in days:
                events = GetDirectories(day)
                if len(events) == 0:
                    PurgeDirectory(day)
            days = GetDirectories(month)
            if len(days) == 0:
                PurgeDirectory(month)
        months = GetDirectories(year)
        if len(months) == 0:
            PurgeDirectory(year)
    
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

def PurgeDirectory(dir):
    """Remove a directory containing no events or dates."""
    if "pages.db" in os.listdir(dir):
        os.remove(os.path.join(dir, "pages.db"))
    if not os.listdir(dir):
        os.rmdir(dir)
    
if __name__=="__main__":
    main()


