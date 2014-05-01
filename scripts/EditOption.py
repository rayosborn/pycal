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
# $Id: EditEditor.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#
"""
CGI script to modify a calendar option.
"""

from pycal.PyCal import CalendarError
from pycal.Editor import Editor
from pycal.GetModule import GetSupervisors
from pycal.PrintModule import LoginPage, ErrorPage
from pycal.CGImodule import CGIgetForm, CGIlogin
import pycal.OptionModule as OptionModule

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user == "admin" or user in GetSupervisors():
            if form.has_key("location"):
                print OptionModule.EditPage("locations", form["location"])
            elif form.has_key("resource"):
                print OptionModule.EditPage("resources", form["resource"])
            elif form.has_key("category"):
                print OptionModule.EditPage("categories", form["category"])
            else:
                raise CalendarError, "No valid option specified"
        else:
            print LoginPage("Not authorized to change calendar options", 
                           script="EditOption.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



