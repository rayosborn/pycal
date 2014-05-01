#!/usr/bin/env python

# PyCal - Python web calendar
#
# Copyright (C) 2004-5 Ray Osborn
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
# $Id: Notify.py,v 1.1 2005/06/12 04:37:44 osborn Exp $
#
"""
CGI script to send an email notification of an event.

Two types of notification are sent.

1) The day before an event, event information is sent to those who have
   added their email address to the event's notification list.
2) Two days before an event, the event's organizer is reminded of the 
   event so that they can make last minute changes if necessary.
"""

from pycal.PyCal import *
from pycal.Event import Event
from pycal.GetModule import GetEvents, GetEditorEmails
from pycal.Utilities import Today, NextDay, FormatDate, FormatTime
from pycal.Utilities import StripHTML, ConvertBreaks
import pycal.CGImodule as CGImodule
    
def main():    
    CGImodule.user = "admin"
    y, m, d = Today()

# Notify those on the event's notify list the day before

    y, m, d = NextDay(y, m, d)
    events = GetEvents(y, m, d)
    for event in events:
        e = Event(event["ID"]) 
        if e.notifyList:
            mailto = calendarEmail
            bcc = e.notifyList
            subject = "%s Event Notification" % calendarAbbr
            text="""\
Title: %s
Date: %s
Time: %s to %s
Location: %s

%s

Please visit the following URL to view further details:

<%s/ViewEvent.py?ID=%s>

If you wish to be removed from the notification list for this event, 
please contact the %s Administration.
""" % (e.title, FormatDate(e.start, day=True), 
       FormatTime(e.start), FormatTime(e.end), e.location, 
       StripHTML(ConvertBreaks(e.description)),
       cgiURL, e.ID, calendarAbbr)
            try:
                CGImodule.SendEmail(mailto, subject, text, bcc=bcc)
            except CalendarError:
                pass
# Remind organizers of the event five days before
    for i in range(4):
        y, m, d = NextDay(y, m, d)
    events = GetEvents(y, m, d)
    for event in events:
        e = Event(event["ID"])
        if e.email:
            mailto =  e.email
            bcc = [calendarEmail]
            subject = "%s Event Reminder" % calendarAbbr
            description = """\
This is an automated reminder that you have organized the following event:

Title: %s
Date: %s
Time: %s to %s
Location: %s
Organizer: %s

%s

-----
"""% (e.title, FormatDate(e.start, day=True), 
       FormatTime(e.start), FormatTime(e.end), e.location, e.organizer,
       StripHTML(ConvertBreaks(e.description)))
            if e.email in GetEditorEmails():
                text = """%s
Please check that the event information is correct.  If it needs correction, 
do one of the following:
a) Visit <%s/ViewEvent.py?ID=%s> 
   and click on either "Edit Event" or "Request Changes".
b) Contact the %s Administration <%s> to request a change in the calendar.
""" % (description, cgiURL, e.ID, calendarAbbr, calendarEmail)
            else:
                text = """%s
Please check that the event information is correct.  If it needs correction, 
contact the %s Administration <%s> to request a change in the calendar.
""" % (description, calendarAbbr, calendarEmail)
            try:
                CGImodule.SendEmail(mailto, subject, text, bcc=bcc)
            except CalendarError:
                pass

if __name__ == "__main__":
    main()

