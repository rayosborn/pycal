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
# $Id: PageModule.py,v 1.2 2004/08/05 12:18:24 osborn Exp $
#
"""PyCal: Python web calendar

Page class defining preformatted web pages.
"""

import os
import time

from PyCal import *
import CGImodule
import DatabaseModule
import PrintModule
from Utilities import DatePath, PathExists

class Page(object):

    """Page class for the calendar.

    This class is instantiated or modified whenever a web page is being
    printed or an event addition/modification is confirmed.  Its purpose is
    to cache web pages so that they do not need to be dynamically created
    every time they are viewed.
    """

    def __init__(self, year=None, month=None, day=None):
        """Initialize an instance of the Event class."""
        self.year = year
        self.month = month
        self.day = day
        self.public = None
        self.private = None
        ID = DatePath(year, month, day)
        if ID:
            self.dir = os.path.join(homeDir, ID)
            if PathExists(self.dir):
                self.Read()

    def __str__(self):
        """Return a string representation of the page.
        
        The page will be formatted if it is not already prepared.
        """
        if CGImodule.CGIgetUser():
            if not self.private:
                self.Format(private=True)
            return self.private
        else:
            if not self.public:
                self.Format()
            return self.public

    def Read(self):
        """Read the current Page database into the Page object."""
        DatabaseModule.Read("pages", "pages", self.dir, self)
        
    def Remove(self):
        """Delete the current Page database."""
        DatabaseModule.Remove("pages", self.dir)
    
    def Store(self):
        """Store the current Page object for later use."""
        DatabaseModule.Store(self, "pages", "pages", self.dir)
    
    def PutEvents(self):
        """Store a list of events for a particular day."""
        if self.day:
            import GetModule
            self.events = GetModule.GetCache(self.year, self.month, self.day)
            if self.events:
                self.Store()
            else:
                self.Remove()
    
    def GetEvents(self):
        """Return  a list of events for a particular day."""
        if self.day:
            if not hasattr(self, "events"):
                self.PutEvents()
            return self.events
        else:
            return []

    def Format(self, private=False):
        """Format the current Page object."""
        user = CGImodule.user
        if private:
            CGImodule.user = "admin"
        else:
            CGImodule.user = ""
        if self.day:
            if private:
                self.private = str(PrintModule.FormatDayView(self.year, 
                                                             self.month, 
                                                             self.day))
            else:
                self.public = str(PrintModule.FormatDayView(self.year,                            
                                                            self.month, 
                                                            self.day))
            if hasattr(self, "events"):
                if self.events:
                    self.Store()
        elif self.month:
            if private:
                self.private = str(PrintModule.FormatMonthView(self.year, 
                                                               self.month))
            else:
                self.public = str(PrintModule.FormatMonthView(self.year, 
                                                              self.month))
            if PathExists(DatePath(self.year, self.month)):
                self.Store()
        elif self.year:
            if private:
                self.private = str(PrintModule.FormatYearView(self.year))
            else:
                self.public = str(PrintModule.FormatYearView(self.year))
        CGImodule.user = user

    def Clear(self):
        """Clear previously formatted versions of page.
        
        Calling this enforces a reformatting of the page on the next print."""
        self.public = None
        self.private = None
        self.Store()
                                              
