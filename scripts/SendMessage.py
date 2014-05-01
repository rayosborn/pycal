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
# $Id: SendRequest.py,v 1.1 2004/08/25 04:00:30 osborn Exp $
#
"""
CGI script to send an email message to an event organizer.
"""

from pycal.PyCal import *
from pycal.Event import Event
from pycal.PrintModule import ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.CGImodule import SendEmail
from pycal.Utilities import FormatDate, FormatTime, IsEmail
import pycal.HTML as HTML
    
def main():
    
    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if form.has_key("ID"):
            e = Event(form["ID"])
            if form.has_key("cancel"):
                print e.EventView()
            else:
                if IsEmail(form["email"]):
                    if form["name"]:
                        byline = "by %s " % form["name"]
                    else:
                        byline = ""
                    mailto = e.email
                    subject = "[%s] %s" % (calendarAbbr, form["subject"])
                    text = """\
%s

--------
The above message was sent %sfrom the web page of a %s calendar event.

Title: %s
Date: %s
Time: %s to %s
Location: %s

Please visit the following URL to view further details:
<%s/ViewEvent.py?ID=%s>
"""\
% (form["message"], byline, calendarAbbr, e.title, 
   FormatDate(e.start, day=True), FormatTime(e.start), FormatTime(e.end), 
   e.location, cgiURL, e.ID) 
                    SendEmail(mailto, subject, text, mailfrom=form["email"])
                    print e.EventView\
                    ("The message has been sent to the event organizer")
                else:
                    print e.EventView("You must provide a valid email address")
    except CalendarError, errorText:
        print ErrorPage(errorText) 

if __name__ == "__main__":
    main()

