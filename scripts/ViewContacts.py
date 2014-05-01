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
# $Id: ViewEditors.py,v 1.2 2004/08/15 22:12:42 osborn Exp $
#
"""
CGI script to list and update the calendar contacts.
"""

from pycal.PyCal import CalendarError
from pycal.PrintModule import ContactsPage, LoginPage, ErrorPage
from pycal.CGImodule import CGIgetForm, CGIlogin
    
def main():    
    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user:
            print ContactsPage()
        else:
            print LoginPage(script="ViewContacts.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()

