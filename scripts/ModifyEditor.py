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
CGI script to modify an editor's details in the editor database.
"""

from pycal.PyCal import CalendarError
from pycal.Editor import Editor
from pycal.GetModule import GetEditors, GetSupervisors
from pycal.PrintModule import EditorsPage, LoginPage, ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.Utilities import IsEmail

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if form.has_key("username"):
            e = Editor(form["username"])
        else:
            raise CalendarError, "No username specified"
        if user == e.user or user == "admin" or user in GetSupervisors():
            if form.has_key("cancel"):
                print EditorsPage()
            elif form.has_key("delete"):
                if user == e.user:
                    print e.EditorPage("Cannot delete yourself")
                else:
                    e.Delete()
                    print EditorsPage("Editor deleted")
            else:
                if form.has_key("firstname") and form.has_key("lastname"):
                    e.firstname = form["firstname"]
                    e.lastname = form["lastname"]
                    e.name =  "%s %s" % (e.firstname, e.lastname)
                message = "Editor details successfully updated"
                if form.has_key("email"): 
                    if IsEmail(form["email"]):
                        e.email = form["email"]
                    else:
                        message = "Invalid email address"
                else:
                    e.email = ""
                if form.has_key("phone"):
                    e.phone = form["phone"]
                else:
                    e.phone = ""
                if form.has_key("authority"):
                    e.authority = form["authority"]
                e.Store()
                print e.EditorPage(message)
        else:
            print LoginPage(script="ModifyEditor.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



