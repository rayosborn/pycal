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
# $Id: ChangePassword.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#
"""
CGI script to change an editor's password.
"""

from pycal.PyCal import CalendarError
from pycal.Editor import Editor
from pycal.GetModule import GetSupervisors
from pycal.PrintModule import LoginPage, ErrorPage
from pycal.CGImodule import CGIgetForm, CGIlogin, CGIprintHeader
from pycal.PasswordModule import MakeCookie

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form, printHeader=False)
        e = Editor(form["username"])
        if user == e.user or user == "admin" or user in GetSupervisors():
            if form["newpassword"]: 
                e.password = form["newpassword"].strip()
            if form["verification"]:
                if form["verification"].strip() == e.password:
                    message = "Password successfully changed."
                    e.Store()
                    if user == e.user:
                        print MakeCookie (user, e.password)
                else:
                    message = \
                    "Password not changed as the two entries did not match."
            CGIprintHeader()
            print e.EditorPage(message)
        else:
            print LoginPage(script="ChangePassword.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()


