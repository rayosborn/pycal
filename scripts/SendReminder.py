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
# $Id: SendReminder.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#
"""
CGI script to send an email reminder of user and password.
"""

from pycal.PyCal import *
from pycal.Editor import Editor
from pycal.GetModule import GetEditors, GetSupervisors
from pycal.PrintModule import AdminPage, LoginPage, ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm, SendEmail
import pycal.HTML as HTML
    
def main():
    
    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if form.has_key("user"):
            username = form["user"]
        else:
            raise CalendarError, "No username specified"
        if username in GetEditors():
            e = Editor(username)
            if not e.email:
                raise CalendarError, "Email address not specified"
            mailto = e.email
            subject = "%s Calendar Editor Infomation" \
                      % calendarAbbr
            text="""\
%s has been registered as a %s Calendar Editor.
Username: %s     Password: %s

To login to the %s Calendar, go to <%s/login.html>
and use the assigned username and password.
""" % (e.name, calendarAbbr, e.user, e.password, calendarAbbr, webURL)
        SendEmail(mailto, subject, text)
        message = "Requested information has been sent to %s" \
                  % HTML.Anchor(mailto, scheme="mailto:")
        if user == "admin" or user in GetSupervisors():
            print AdminPage(message)
        else:
            print LoginPage(message)
    except CalendarError, errorText:
        print ErrorPage(errorText) 

if __name__ == "__main__":
    main()


