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
# $Id: Event.py,v 1.11 2006/12/30 02:28:05 rosborn Exp $
#
"""PyCal: Python web calendar

Editor class defining calendar events.
"""

import os
import calendar

from PyCal import *
import Event
import GetModule
from Utilities import Today, FormatDay, NextDay

class WorshipEvent(Event.Event):

    """Event class for a calendar worship event."""

    def __init__(self, ID=None):
        """Initialize an instance of the Worship Event class."""
        self.banner = ""
        self.service = ""
        self.preacher = ""
        self.sermon = ""
        self.reading = []
        self.music = []
        self.notes = ""
        if ID:
            self.dir = os.path.join(homeDir, ID)
            self.Read()

    def FormatDescription(self):
        """Format the event description with the service information."""
        text = []
        if self.service:
            text.append("%s" % HTML.Strong(self.service))
        if self.preacher:
            text.append("%s %s" % (HTML.Strong("Sermon:"), self.preacher))
        if self.sermon:
            text.append("   &quot;%s&quot;" % self.sermon)
        if self.reading:
            text.append("%s %s" % (HTML.Strong("Scripture:", 
                                   ", ".join(self.reading))))
        if self.music:
            text.append("%s %s" % (HTML.Strong("Music:", 
                                   "\n       ".join(self.music))))
        if self.notes:
            text.append(self.notes)
        self.description = "\n".join(text)
       
    def FormatWorship(self):
        """Format the HTML entry for the Worship page."""
        content = HTML.Container()
        if self.title:
            content.Add(HTML.Header("%s %s" % (FormatTime(self.start), 
                                               self.title), 
                                    level=3, style="margin-top:5px"))
        if self.service:
            content.Add(HTML.Header(self.service, level=3, class_="subheader", 
                                    style="text-align:center"))
        table = HTML.Table(border="0", cellpadding="0",    
                           style="margin-left:20px")
        if self.preacher:
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Sermon:", width="70"))
            row.Add(HTML.Cell(self.preacher, width="200"))
            table.Add(row)
        if self.sermon:
            row = HTML.Row()
            row.Add(HTML.Cell("&quot;%s&quot;" % self.sermon, colspan="2", 
                              style="padding-left:20px"))
            table.Add(row)
        if self.reading:
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Scripture:", valign="top"))
            row.Add(HTML.Cell(str(HTML.Break()).join(self.reading),
                              valign="top"))
            table.Add(row)
        if self.music:
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Music:", valign="top"))
            row.Add(HTML.Cell(str(HTML.Break()).join(self.music), 
                              valign="top"))
            table.Add(row)
        content.Add(table)
        return content


def FormatWorship(services):
    """Return the HTML code for the Worship Page."""
    content = HTML.Container()
    content.Add(HTML.Header(date, style="margin-top:0"))
    content.Add(HTML.Header(banner, level=2, class_="subheader"))
    for service in services:
        event = WorshipEvent(service["ID"])
        content.Add(event.FormatWorship())
    return content

def GetServiceDates():
    """Return a list of dates containing worship services.
    
       The dates are returned as dictionary keys to items 
       containing the calendar event data.
    """
    y, m, d = Today()
    dates = {}
    for next in range(21):
        services = GetModule.GetEvents(y, m, d, category="Worship")
        if services:
            dates[(y, m, d)] = services
        y, m, d = NextDay(y, m, d)
    return dates
