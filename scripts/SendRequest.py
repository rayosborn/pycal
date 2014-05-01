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
CGI script to send an email request to approve an event.
"""

from pycal.PyCal import *
from pycal.Editor import Editor
from pycal.Event import Event
from pycal.GetModule import GetEditors, GetSupervisors
from pycal.PrintModule import AdminPage, LoginPage, ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.CGImodule import SendEmail
from pycal.Utilities import FormatDate, FormatTime
import pycal.HTML as HTML
    
def main():
    
    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if form.has_key("ID"):
            e = Event(form["ID"])
            if form.has_key("cancel"):
                print e.EventView()
                return
        if user in GetEditors():
            name = Editor(user).name
            email = Editor(user).email
            if email:
                emailLink = "<%s>" % email
            else:
                emailLink = ""
            mailto = []
            for supervisor in GetSupervisors():
                mailto.append(Editor(supervisor).email)
            mailto.append(calendarEmail)
            subject = "%s Event Request" % calendarAbbr
            if form.has_key("message"):
                message = "Additional Message:\n%s" % form["message"]
            else:
                message = ""
            if form.has_key("prefix"):
                prefix = form["prefix"]
            else:
                prefix = "A change to"
            if e.status == "Approved":
                script = "EditEvent.py"
            else:
                script = "ViewEvent.py"
            text="""\
%s the following %s event has been requested:

Title: %s
Date: %s
Time: %s to %s
Location: %s
Resource: %s
Category: %s

Requested by: %s %s

Please visit the following URL to approve or modify the requested event:

<%s/%s?ID=%s>

%s
""" % (prefix, calendarAbbr, e.title, FormatDate(e.start, day=True), 
       FormatTime(e.reservation["start"]), FormatTime(e.reservation["end"]),
       ", ".join(e.locations), ", ".join(e.resources), ", ".join(e.categories), 
       name, emailLink, cgiURL, script, e.ID, message) 
            SendEmail(mailto, subject, text, cc=email)
            message = \
            "Requested information has been sent to the %s Administration" \
            % calendarAbbr
            print e.EventView(message)
        else:
            print LoginPage(script="SendRequest.py", form=form)        
    except CalendarError, errorText:
        print ErrorPage(errorText) 

if __name__ == "__main__":
    main()


