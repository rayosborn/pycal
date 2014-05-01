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
# $Id: Editor.py,v 1.7 2004/08/05 12:04:01 osborn Exp $
#
"""PyCal: Python web calendar

Module for handling options stored in options.db.
"""

from PyCal import *
import DatabaseModule
import PrintModule
import HTML
from Utilities import ConvertBreaks

def Add(options, selection, value=None):
    """Add an option to the database."""
    selections = DatabaseModule.Read(options, "options")
    if selections == None:
        selections = {selection: value}
    else:
        selections[selection] = value
    DatabaseModule.Store(selections, options, "options")

def Read(options):
    """Read a list of options from the database."""
    return DatabaseModule.Read(options, "options")

def Get(options, key):
    """Return the value of an option key."""
    dict = Read(options)
    return dict[key]

def Delete(options, selection):
    """Delete an option from the database."""
    selections = DatabaseModule.Read(options, "options")
    try:
        del selections[selection]
        DatabaseModule.Store(selections, options, "options")
    except KeyError:
        pass

def EditPage(options, selection):
    """Print a web page to edit the values of an option."""
    if options == "categories":
        option = "category"
    else:
        option = options[:-1]
    title = "Edit %s" % option.capitalize()
    content = HTML.Container()
    content.Add(HTML.Header("Edit %s" % option.capitalize()))
    selections = DatabaseModule.Read(options, "options")
    form = HTML.Form("ModifyOption.py")
    table = HTML.Table([200, 350], cellspacing="0", align="center")
    row = HTML.Row()
    row.Add(HTML.HeaderCell(option.capitalize()))
    row.Add(HTML.HeaderCell(selection, class_="sunday"))
    table.Add(row)
    row = HTML.Row()
    row.Add(HTML.HeaderCell("Description"))
    if selections[selection]:
        row.Add(HTML.Cell(HTML.TextArea("description", 
                                        ConvertBreaks(selections[selection]),
                                        rows=5, cols=40)))
    else:                                    
        row.Add(HTML.Cell(HTML.TextArea("description", rows=5, cols=40)))
    table.Add(row)
    form.Add(table)
    form.Add(HTML.Para("%s%s%s%s%s" 
                       % (HTML.Submit("modify", "Modify %s" 
                                     % option.capitalize()),
                          HTML.TAB,
                          HTML.Submit("delete", "Delete %s"
                                     % option.capitalize()),
                          HTML.TAB,
                          HTML.Submit("cancel", "Cancel")),
                       class_="center"))
    form.Add(HTML.HiddenInput("options", options))
    form.Add(HTML.HiddenInput("selection", selection))
    content.Add(form)
    content.Add(PrintModule.BottomMonthsTable())
    return HTML.Page(title, content)


