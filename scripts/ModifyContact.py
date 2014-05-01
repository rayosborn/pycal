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
# $Id: ModifyEditor.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#
"""
CGI script to modify a contact's details.
"""

from pycal.PyCal import CalendarError
from pycal.Editor import Contact
from pycal.PrintModule import ContactsPage, LoginPage, ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.Utilities import IsEmail

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user:
            if form.has_key("cancel"):
                print ContactsPage()
            elif form.has_key("delete"):
                if form.has_key("username"):
                    c = Contact(form["username"])
                    c.Delete()
                    message = "Contact deleted"
                else:
                    message = "Contact not specified"
                print ContactsPage(message)
            elif form.has_key("firstname") and form.has_key("lastname"):
                name = "%s %s" % (form["firstname"], form["lastname"])
                if name == form["username"]:
                    c = Contact(name)
                else:
                    c = Contact()
                    c.user = name
                    c.name = name
                    c.firstname = form["firstname"]
                    c.lastname = form["lastname"]
                    oldContact = Contact(form["username"])
                    c.phone = oldContact.phone
                    c.email = oldContact.email
                    oldContact.Delete()
                message = "Contact details successfully updated"
                if form.has_key("email"):
                    if IsEmail(form["email"]):
                        c.email = form["email"]
                    else:
                        message = "Invalid email address"
                else:
                    c.email = ""
                if form.has_key("phone"):
                    c.phone = form["phone"]
                else:
                    c.phone = ""
                c.Store()
                print ContactsPage(message)
            else:
                print ContactsPage("Name not fully specified")
        else:
            print LoginPage(script="ModifyContact.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



