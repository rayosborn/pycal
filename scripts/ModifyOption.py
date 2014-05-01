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
CGI script to modify a calendar event option.
"""

from pycal.PyCal import CalendarError
from pycal.GetModule import GetSupervisors
from pycal.PrintModule import OptionsPage, LoginPage, ErrorPage
from pycal.CGImodule import CGIlogin, CGIgetForm
from pycal.Utilities import ConvertCRLFs
import pycal.OptionModule as OptionModule

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user == "admin" or user in GetSupervisors():
            if form.has_key("options"):
                options = form["options"]
            else:
                raise CalendarError, "No option specified"
            if form.has_key("selection"):
                selection = form["selection"]
            else:
                raise CalendarError, "No selection specified"
            if form.has_key("description"):
                description = ConvertCRLFs(form["description"])
            else:
                description = ""
            if form.has_key("modify"):
                OptionModule.Add(options, selection, description)
                print OptionsPage(options, "%s modified" % selection)
            elif form.has_key("delete"):
                OptionModule.Delete(options, selection)
                print OptionsPage(options, "%s deleted" % selection)
            elif form.has_key("cancel"):
                print OptionsPage(options)
        else:
            print LoginPage(script="ModifyOption.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



