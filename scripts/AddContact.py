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
# $Id: AddEditor.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#
"""
CGI script to add a calendar contact to the contact database.
"""

from pycal.PyCal import CalendarError
from pycal.Editor import Contact
from pycal.GetModule import GetEditors
from pycal.PasswordModule import SetPassword
from pycal.PrintModule import AdminPage, LoginPage
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.Utilities import IsEmail

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user == "admin" or user in GetEditors():
            message = "Contact added"
            if form.has_key("firstname") and form.has_key("lastname"):
                c = Contact()
                c.firstname = form["firstname"]
                c.lastname = form["lastname"]
                c.user = c.firstname + " " + c.lastname
                c.name = c.user
            else:
                raise CalendarError, "No full name specified"
            if form.has_key("phone"):
                c.phone = form["phone"]
            if form.has_key("email"):
                if IsEmail(form["email"]):
                    c.email = form["email"]
                else:
                    message = "Invalid email address"
            #Set an initial password at random
            c.password = SetPassword()
            c.Store()
            print c.ContactPage(message)
        else:
            print LoginPage("Not authorized for this operation", 
                           script="AddContact.py", form=form)
    except CalendarError, errorText:
        print AdminPage(errorText)

if __name__ == "__main__":
    main()



