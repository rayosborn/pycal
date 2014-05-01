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
# $Id: Login.py,v 1.3 2004/04/23 03:07:50 osborn Exp $
#
"""
CGI script to log the user into the calendar administration system.
"""

from pycal.PyCal import CalendarError
from pycal.Editor import Editor
from pycal.GetModule import GetEditors
from pycal.PrintModule import AdminPage, ErrorPage
from pycal.CGImodule import CGIgetForm, CGIlogin
from pycal.Utilities import Today
    
def main():
    
    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user == "admin":
            print AdminPage()
        elif user in GetEditors():
            e = Editor(user)
            print e.EditorPage()
            return
        else:
            raise CalendarError, "Invalid user and/or password"
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()

