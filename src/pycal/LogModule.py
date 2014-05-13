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
# $Id: LogModule.py,v 1.1 2006/12/29 17:54:24 rosborn Exp $
#
"""PyCal: Python web calendar

Module for handling event logs in logs.db.
"""

from PyCal import *
import DatabaseModule

def Add(timestamp, ID, title, user, log):
    """Add a log message to the database."""
    DatabaseModule.Store((ID, title, user, log), timestamp, "logs")
    Purge()

def Read():
    """Read a list of log entries from the database."""
    timestamps = DatabaseModule.Keys("logs")
    timestamps.sort()
    timestamps.reverse()
    entries = []
    for timestamp in timestamps:
        ID, title, user, log = DatabaseModule.Read(timestamp, "logs")
        entries.append((timestamp, ID, title, user, log))
    return entries

def Purge(size=logSize):
    """Purge the log database of the oldest entries."""
    timestamps = DatabaseModule.Keys("logs")
    timestamps.sort()
    timestamps.reverse()
    for timestamp in timestamps[size:]:
        DatabaseModule.Delete(timestamp, "logs")
    


