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
# $Id: ConfirmMessage.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#
"""
CGI script to send an email message to all the contact authors on a list.
"""

from config import *
from PyCal import CalendarError
from PrintModule import ErrorPage
from CGImodule import CGIprintHeader, CGIflush, CGIgetForm, CGIgetUser
from CGImodule import SendEmail
from Utilities import ConvertMessage, ConvertTeX
import pycal.HTML as HTML
import cgi
import re
    
def main():
    
    try:
        CGIprintHeader()
        form = CGIgetForm()
        user, name, email = CGIgetUser(form)
        IDlist = form["list"][1:-1].split(", ")
        try:
            subject = form["subject"]
        except KeyError:
            subject = ""
        text = ""
        if form.has_key("options"):
            if not subject:
                subject = "calendar Notification"
            if isinstance(form["options"], list):
                options = form["options"]
            else:
                options = [form["options"]]
            reference = "This abstract"
            if "Editor" in options:
                text = \
            "The calendar editor assigned to this abstract is %s <%s>\n\n" \
                       % ("[[[editor]]]", "[[[email]]]")
                reference = "It"
            if "Presentation" in options:
                text = text + \
            "%s has been selected for %s presentation.\n\n" \
                % (reference, "[[[presentation]]]")
                reference = "It"
            if "Session" in options:
                text = text + \
            "%s has been assigned to the following session:\n" + \
                "    %s - %s\n\n" \
                % (reference, "[[[session]]]", "[[[time]]]")
        try:
            if text:
                text = "%s\n\n%s" % (text, form["message"])
            else:
                text = form["message"]
        except KeyError:
            pass
        if text == "":
            raise CalendarError, "No text specified for this message"
        elif subject == "":
            raise CalendarError, "Enter subject before submitting"
        subject = "[%s] %s" % (calendarAbbr, subject)
        text = '%s\nCalendar No. %s: %s\n-----------------\n%s' \
               % (calendarName, "[[[ID]]]", "[[[title]]]", text)
        if len(IDlist) == 1:
            ID = int(IDlist[0])
            abs = Calendar(ID)
            text = ConvertMessage(abs, text)
        title = "Calendar Message"
        content = HTML.Container()
        content.Add(HTML.Header("Calendar Message"))
        content.Add(HTML.Header("Message Preview", level=2))
        defs = HTML.DefinitionList()
        defs.Add({"Subject": cgi.escape(subject)})
        HTMLtext = re.sub("<BR>", "", ConvertTeX(cgi.escape(text)))
        HTMLtext = re.sub('\n', '<br />', HTMLtext)
        HTMLtext = HTMLtext.replace('[[[', '<span style="color: red">')
        HTMLtext = HTMLtext.replace(']]]', '</span>')
        defs.Add({"Message": HTMLtext})
        content.Add(defs)
        content.Add(HTML.Header("Addressees", level=2))
        content.Add(HTML.Para("""
        The message will be sent to the following addresses:
        """))
        para = HTML.Para()
        for ID in IDlist:
            ID = int(ID)
            abs = Calendar(ID)
            para.Add("%s Calendar no. %d: %s &lt;%s&gt;<br />" 
                     % (HTML.TAB, ID, abs.contact, abs.email))
        content.Add(para)
        content.Add(HTML.HorizontalRule())
        f = HTML.Form("SendMessage.py")
        f.Add(HTML.Para(HTML.Submit(value="Send Message..."),
                        class_="center"))
        f.Add(HTML.HiddenInput("list", form["list"]))
        f.Add(HTML.HiddenInput("subject", subject))
        f.Add(HTML.HiddenInput("message", text))
        content.Add(f)
        content.Add(HTML.HorizontalRule())
        f = HTML.Form("AdminView.py")
        f.Add(HTML.Para(HTML.Submit(value="Admin Page"), class_="center"))
        content.Add(f)
        print HTML.Page(title, content)     
        CGIflush()
    except CalendarError, errorText:
        print ErrorPage(errorText) 

if __name__ == "__main__":
    main()


