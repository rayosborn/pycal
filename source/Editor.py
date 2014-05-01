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

Editor class defining calendar editors.
"""

from PyCal import *
import HTML
import CGImodule
import DatabaseModule
import GetModule
import PrintModule

class Editor(object):

    """Editor class.

    This class is instantiated using the overall administration form.  
    It stores the name and contact information of a calendar editor.
    """

    def __init__(self, user=None):
        """Initialize an instance of the Editor class."""
        self.user = ""
        self.name = ""
        self.firstname = ""
        self.lastname = ""
        self.email = ""
        self.phone = ""
        self.password = ""
        self.authority = ""
        self.database = "editors"
        if user:
            self.user = user
            self.Read()
    
    def __cmp__(self, other):
        """Sort editors by their last names."""
        return cmp(self.lastname, other.lastname)            

    def Read(self):
        """Read the editor database into the Editor object."""
        DatabaseModule.Read(self.user, self.database, object=self)
        
    def Store(self):
        """Store the current Editor object for later use."""
        DatabaseModule.Store(self, self.user, self.database)

    def Delete(self):
        """Remove an editor from the database."""
        DatabaseModule.Delete(self.user, self.database)           

    def EditorPage(self, message=None):
        """Print editor's home page."""
        user = CGImodule.CGIgetUser()
        title = "%s Editor Page" % calendarAbbr
        content = HTML.Container()
        content.Add(HTML.Header("Username <em>%s</em> : %s" % 
                                (self.user, self.name),
                                level=2, class_="title"))
        if message:
            content.Add(HTML.Para(message, class_="alert"))
        content.Add(HTML.Header("Editor Contact Details"))
        form = HTML.Form("ModifyEditor.py")
        table = HTML.Table([150, 400], cellspacing="0", align="center")
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Editor's Name"))
        row.Add(HTML.HeaderCell("%s %s" %
                          (HTML.Input("firstname", self.firstname, 
                                      size=18, maxlength=255),
                           HTML.Input("lastname", self.lastname, 
                                      size=29, maxlength=255)),
                                class_="sunday"))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Email"))
        row.Add(HTML.HeaderCell(HTML.Input("email", self.email, 
                                           size=50, maxlength=255),
                                class_="sunday"))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Phone"))
        row.Add(HTML.HeaderCell(HTML.Input("phone", self.phone, 
                                           size=50, maxlength=255),
                                class_="sunday"))
        table.Add(row)
        if user == "admin" or user in GetModule.GetSupervisors():
            authorized = True
        else:
            authorized = False
        if authorized:
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Authority"))
            if self.authority == "":
                self.authority = "Editor"
            options = ["Editor", "Supervisor"]
            row.Add(HTML.HeaderCell(HTML.RadioButtons("authority", options, 
                                                      self.authority),
                                    class_="sunday"))
            table.Add(row)
        form.Add(table)
        form.Add(HTML.Para(HTML.Submit(value="Update Editor Details"),
                           class_="center"))
        form.Add(HTML.HiddenInput("username", self.user))
        content.Add(form)
        if authorized and user <> self.user:
            content.Add(HTML.Header("Delete Editor", level=2))
            content.Add(HTML.Para("""
            Only supervisors can delete an editor record.  This
            operation is immediate and irreversible.  You can add an
            equivalent record but the password will be different."""))
            form = HTML.Form("ModifyEditor.py")
            form.Add(HTML.Para(HTML.Submit("delete", "Delete Editor"),
                               class_="center"))
            form.Add(HTML.HiddenInput("username", self.user))
            content.Add(form)
            content.Add(HTML.Header("Notify Editor", level=2))
            content.Add(HTML.Para("""
            Send an email informing the editor of the currently assigned 
            username and password."""))
            form = HTML.Form("SendReminder.py")
            form.Add(HTML.Para(HTML.Submit(value="Send Login Info to Editor"),
                               class_="center"))
            form.Add(HTML.HiddenInput("user", self.user))
            content.Add(form)
        content.Add(HTML.Header("Change Password", level=2))
        form = HTML.Form("ChangePassword.py")
        form.Add(HTML.Para("Password : %s%s Verify Password : %s"
                           % (HTML.Password("newpassword", 
                                            size=20, maxlength=25),
                              HTML.TAB,
                              HTML.Password("verification", 
                                            size=20, maxlength=25)),
                           class_="center"))
        form.Add(HTML.Para(HTML.Submit(value="Change Password..."),
                           class_="center"))
        form.Add(HTML.HiddenInput("username", self.user))
        content.Add(form)
        if user == self.user:
            content.Add(PrintModule.AdminOptions())
        else:
            content.Add(HTML.Header("Calendar Editors", level=2))
            form = HTML.Form("ViewEditors.py")
            form.Add(HTML.Para(HTML.Submit(
                               value="Return to List of Calendar Editors..."),
                               class_="center"))
            content.Add(form)
        content.Add(PrintModule.CalendarOptions())
        content.Add(PrintModule.BottomMonthsTable())
        return HTML.Page(title, content)

class Contact(Editor):
    """Contact class.
    
    This class is a sub-class of an editor that stores basic contact
    information for a calendar organizer.
    """
    
    def __init__(self, name=None):
        """Initialize an instance of the Contact class."""
        self.user = ""
        self.name = ""
        self.firstname = ""
        self.lastname = ""
        self.email = ""
        self.phone = ""
        self.password = ""
        self.database = "contacts"
        if name:
            self.user = name
            self.name = name
            self.Read()
    
    def ContactPage(self, message=None):
        """Print contact's edit page."""
        user = CGImodule.CGIgetUser()
        title = "%s Contact" % calendarAbbr
        content = HTML.Container()
        if message:
            content.Add(HTML.Para(message, class_="alert"))
        content.Add(HTML.Header("Contact Details"))
        form = HTML.Form("ModifyContact.py")
        table = HTML.Table([150, 400], cellspacing="0", align="center")
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Contact's Name"))
        row.Add(HTML.HeaderCell("%s %s" %
                          (HTML.Input("firstname", self.firstname, 
                                      size=18, maxlength=255),
                           HTML.Input("lastname", self.lastname, 
                                      size=29, maxlength=255)),
                                class_="sunday"))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Email"))
        row.Add(HTML.HeaderCell(HTML.Input("email", self.email, 
                                           size=50, maxlength=255),
                                class_="sunday"))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Phone"))
        row.Add(HTML.HeaderCell(HTML.Input("phone", self.phone, 
                                           size=50, maxlength=255),
                                class_="sunday"))
        table.Add(row)
        form.Add(table)
        form.Add(HTML.Para("%s%s%s%s%s"
                           %(HTML.Submit(value="Update Contact Details"),
                             HTML.TAB,
                             HTML.Submit("delete", "Delete Contact"),
                             HTML.TAB,
                             HTML.Submit("cancel", "Cancel")),                                    
                           class_="center"))
        form.Add(HTML.HiddenInput("username", self.user))
        content.Add(form)
        content.Add(PrintModule.CalendarOptions())
        content.Add(PrintModule.BottomMonthsTable())
        return HTML.Page(title, content)
