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
# $Id: ViewOptions.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#
"""
CGI script to access the administrative options page.
"""

from pycal.PyCal import CalendarError
from pycal.PrintModule import OptionsPage, LoginPage, ErrorPage
from pycal.CGImodule import CGIgetForm, CGIlogin
    
def main():    
    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user:
            if form.has_key("locations"):
                print OptionsPage("locations")
            elif form.has_key("resources"):
                print OptionsPage("resources")
            elif form.has_key("categories"):
                print OptionsPage("categories")
            else:
                raise CalendarError, "No viewing option specifed"
        else:
            print LoginPage(script="ViewOptions.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()

