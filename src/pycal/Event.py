# PyCal - Python web calendar
#
# Copyright (C) 2004-6 Ray Osborn
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
# $Id: Event.py,v 1.11 2006/12/30 02:28:05 rosborn Exp $
#
"""PyCal: Python web calendar

Editor class defining calendar events.
"""

import os
import time
import calendar

from PyCal import *
import CGImodule
import DatabaseModule
import Editor
import GetModule
import HTML
import LogModule
import OptionModule
import PageModule
import PrintModule
from Utilities import FormatTime, FormatDate, NextDay
from Utilities import PreviousMonth, NextMonth, CopyTime
from Utilities import PathDate, StripID, StripIDs, IsValidID, IDexists, IsEmail
from Utilities import ConvertBreaks, ConvertCRLFs, StripHTML

class Event(object):

    """Event class for a calendar object.

    This class is instantiated by an Add Event click.  
    """

    def __init__(self, ID=None):
        """Initialize an instance of the Event class."""
        self.ID = ""
        self.title = ""
        self.type = "Event"
        self.description = ""
        self.location = ""
        self.start = ""
        self.end = ""
        self.repeats = []
        self.logs = []
        self.organizer = ""
        self.phone = ""
        self.email = ""
        self.reservation = {}
        self.locations = []
        self.resources = []
        self.categories = []
        self.setup = ""
        self.status = ""
        self.created = None
        self.editor = ""
        self.notifyList = []
        self.dir = ""
        if ID:
            self.ID = ID
            self.dir = os.path.join(homeDir, ID)
            self.Read()
            #Put in for backward compatibility
            if self.location:
                try:
                    self.locations.remove(self.location)
                except ValueError:
                    pass
                self.locations.insert(0, self.location)
            if not self.reservation.has_key("start"):
                self.reservation["start"] = self.start
                self.reservation["end"] = self.end
                self.reservation["option"] = "Same as Event"
                if self.locations:
                    self.location = self.locations[0]

    def __cmp__(self, other):
        """Sort events by their start times."""
        if self.type == "Holiday":
            if other.type == "Holiday":
                return 0
            else:
                return -1
        elif other.type == "Holiday":
            if self.type == "Holiday":
                return 0
            else:
                return 1
        elif self.type == "Banner":
            if other.type == "Holiday":
                return 1
            elif other.type == "Banner":
                return 0
            else:
                return -1
        elif other.type == "Banner":
            if self.type == "Holiday":
                return -1
            elif self.type == "Banner":
                return 0
            else:
                return 1
        elif self.start == other.start:
            if self.type == "Special":
                if other.type == "Holiday" or other.type == "Banner":
                    return 1
                elif other.type == "Special":
                    return 0
                else:
                    return -1
            elif self.type == "Event":
                if other.type == "Holiday" or other.type == "Banner" or \
                   other.type == "Special":
                    return 1
                elif other.type == "Event":
                    return 0
                else:
                    return -1
            elif self.type == "Private":
                if other.type == "Holiday" or other.type == "Banner" or \
                   other.type == "Special" or other.type == "Event":
                    return 1
                elif other.type == "Private":
                    return 0
                else:
                    return -1
            elif self.type == "Setup":
                if other.type == "Setup":
                    return 0
                else:
                    return 1
        return cmp(self.start, other.start)

    def __str__(self):
        """Output event details for a command-line session."""
        output = ["%s: %s" % (self.ID, self.title)]
        output.append(FormatDate(self.start, day=True))
        if self.type <> "Banner" and self.type <> "Holiday":
            output.append("Event Time: %s to %s" 
                          % (FormatTime(self.start), FormatTime(self.end)))
            output.append("Event Reservation: %s to %s" 
                          % (FormatTime(self.reservation["start"]), 
                             FormatTime(self.reservation["end"])))
        output.append("Status: %s" % self.status)
        output.append("Type: %s" % self.type)
        if self.description:
            output.append("Description:")
            output.append(ConvertBreaks(self.description))
        if self.locations:
            output.append("Locations: %s" % ", ".join(self.locations))
        if self.resources:
            output.append("Resources: %s" % ", ".join(self.resources))
        if self.categories:
            output.append("Categories: %s" % ", ".join(self.categories))
        if self.organizer:
            output.append("Organizer: %s" % self.organizer)
        if self.phone:
            output.append("Phone: %s" % self.phone)
        if self.email:
            output.append("Email: %s" % self.email)
        if self.repeats:
            output.append("Repeats: %s" % ", ".join(self.repeats))
        return "\n".join(output)

    def Read(self):
        """Read the current Event database into the Event object."""
        DatabaseModule.Read("event", "events", self.dir, self)
        
    def Store(self):
        """Store the current Event object for later use and update cache."""
        DatabaseModule.Store(self, "event", "events", self.dir)

    def Copy(self, other):
        """Copy another event ignoring the ID and directory."""
        self.title = other.title
        self.type = other.type
        self.description = other.description
        self.location = other.location
        self.start = other.start
        self.end = other.end
        self.repeats = other.repeats
        self.logs = other.logs
        self.organizer = other.organizer
        self.phone = other.phone
        self.email = other.email
        self.reservation = other.reservation
        self.locations = other.locations
        self.resources = other.resources
        self.categories = other.categories
        self.setup = other.setup
        self.status = other.status
        self.editor = other.editor
        self.notifyList = other.notifyList

    def Remove(self):
        """Delete the event."""
        try:
            os.chdir(self.dir)
            for file in os.listdir("."):
                os.remove(file)
            os.chdir("../")
            os.rmdir(self.dir)
        except OSError, errorText:
            raise CalendarError, errorText
        self.ClearRepeats()
        
    def AddLog(self, log, save=True):
        """Add a log entry to the event database with a time stamp."""
        timestamp = FormatTime(time.localtime(time.time()), "ISO8601")
        user = CGImodule.CGIgetUser()
        try:
            self.logs.append((timestamp, user, log))
        except NameError:
            self.logs = [(timestamp, user, log)]
        if save:
            LogModule.Add(timestamp, self.ID, self.title, user, log)
 
    def ClearRepeats(self):
        """Remove ID from other repeated events."""
        for repeat in self.repeats:
            if repeat <> self.ID and IDexists(repeat):
                other = Event(repeat)
                try:
                    other.repeats.remove(self.ID)
                    if len(other.repeats) == 1:
                        other.repeats = []
                    other.Store()
                except ValueError:
                    pass

    def AddNotification(self, email):
        """Add an email address to the notify list."""
        from Utilities import IsEmail
        if IsEmail(email):
            if email not in self.notifyList:
                self.notifyList.append(email)
                self.Store()
        else:
            raise CalendarError, "Invalid email address"

    def RemoveNotification(self, email):
        """Remove an email address from the notify list."""
        if email in self.notifyList:
            self.notifyList.remove(email)
            self.Store()

    def UpdatePages(self):
        """Add a flag to update page caches for this event and all repeats."""
        if self.repeats:
            dates = []
            for ID in self.repeats:
                y, m, d = PathDate(StripID(ID))
                if ID <> self.ID:
                    OptionModule.Add("updates", (y, m, d))
        y, m, d = PathDate(StripID(self.ID))
        OptionModule.Add("updates", (y, m, d))
        #Update the primary event's display right away
        p = PageModule.Page(y, m, d)
        p.PutEvents()
        p.Format()
        p.Format(private=True)

    def EventView(self, message=None, updating=False):
        """Print formatted display of event."""
        user = CGImodule.CGIgetUser()
        title = self.title
        content = HTML.Container()
        year, month, day = self.start[0:3]
        if not updating:
            content.Add(PrintModule.NavigationBar(year, month, day, self.ID))
        content.Add(HTML.Header(PrintModule.CalendarTitle(year, month, day)))
        if message:
            content.Add(HTML.Para(message, class_="alert"))
        table = HTML.Table([500, 200], cellspacing="0", align="center")
        row = HTML.Row()
        if self.status == "Requested":
            cell = HTML.Cell(class_="requested")
        elif self.type == "Private":
            cell = HTML.Cell(class_="private")
        elif self.type == "Setup":
            cell = HTML.Cell(class_="setup")
        else:
            cell = HTML.Cell()
        if user and updating:
            f = HTML.Form("ConfirmEvent.py")
            t = HTML.Table(class_="transparent", cellspacing="0",
                           cellpadding="5", align="center")
            r = HTML.Row()
            r.Add(HTML.HeaderCell(HTML.Submit("edit", "Return to Edit"),
                                  class_="transparent"))
            r.Add(HTML.HeaderCell(HTML.Submit("confirm", "Confirm Event"),
                                  class_="transparent"))
            r.Add(HTML.HeaderCell(HTML.Submit("cancel", "Cancel Edit"),
                                  class_="transparent"))
            t.Add(r)
            f.Add(t)
            f.Add(HTML.Para(
            """This is a preview of the event display.%sPress "Confirm Event" 
            to save it to the calendar.""" % HTML.Break(), class_="alert"))
            f.Add(HTML.Header(self.title))
        else:
            cell.Add(HTML.Header(self.title))
        t = HTML.Table([120, 360], cellspacing="0", align="center")
        if user:
            t.Add(HTML.Row(HTML.HeaderCell("Event Description", colspan=2,
                                           class_="empty")))
            r = HTML.Row()
            r.Add(HTML.HeaderCell("Type", style="padding:5px"))
            r.Add(HTML.Cell(self.type, style="padding:5px"))
            t.Add(r)
        if self.type <> "Banner" and self.type <> "Holiday":
            r = HTML.Row()
            r.Add(HTML.HeaderCell("Time", style="padding:5px"))
            r.Add(HTML.Cell("%s to %s" % (FormatTime(self.start),
                                          FormatTime(self.end)), 
                            style="padding:5px"))
            t.Add(r)
        r = HTML.Row()
        r.Add(HTML.HeaderCell("Description", style="padding:5px"))
        r.Add(HTML.Cell(self.description, style="padding:5px"))
        t.Add(r)
        r = HTML.Row()
        r.Add(HTML.HeaderCell("Location", style="padding:5px"))
        r.Add(HTML.Cell(self.location, style="padding:5px"))
        t.Add(r)
        r = HTML.Row()
        r.Add(HTML.HeaderCell("Organizer", style="padding:5px"))
        if self.organizer and self.email:
            url = "%s/ComposeMessage.py?ID=%s" % (cgiURL, self.ID)
            r.Add(HTML.Cell(HTML.Anchor(url, self.organizer), 
                            style="padding:5px"))
        else:
            r.Add(HTML.Cell(self.organizer, style="padding:5px"))
        t.Add(r)
        if user:
            r = HTML.Row()
            r.Add(HTML.HeaderCell("Phone", style="padding:5px"))
            r.Add(HTML.Cell(self.phone, style="padding:5px"))
            t.Add(r)
            r = HTML.Row()
            r.Add(HTML.HeaderCell("Email", style="padding:5px"))
            r.Add(HTML.Cell(HTML.Anchor(self.email, scheme="mailto:"), 
                            style="padding:5px"))
            t.Add(r)
            t.Add(HTML.Row(HTML.HeaderCell("Event Reservation", colspan=2,
                                           class_="empty")))
            if self.type <> "Banner" and self.type <> "Holiday":
                r = HTML.Row()
                r.Add(HTML.HeaderCell("Reservation", style="padding:5px"))
                r.Add(HTML.Cell("%s to %s" 
                                % (FormatTime(self.reservation["start"]),
                                   FormatTime(self.reservation["end"])), 
                                style="padding:5px"))
                t.Add(r)
            r = HTML.Row()
            r.Add(HTML.HeaderCell("Locations", style="padding:5px"))
            r.Add(HTML.Cell(", ".join(self.locations), style="padding:5px"))
            t.Add(r)
            r = HTML.Row()
            r.Add(HTML.HeaderCell("Resources", style="padding:5px"))
            r.Add(HTML.Cell(", ".join(self.resources), style="padding:5px"))
            t.Add(r)
            r = HTML.Row()
            r.Add(HTML.HeaderCell("Categories", style="padding:5px"))
            r.Add(HTML.Cell(", ".join(self.categories), style="padding:5px"))
            t.Add(r)
            r = HTML.Row()
            r.Add(HTML.HeaderCell("Setup", style="padding:5px"))
            r.Add(HTML.Cell(self.setup, style="padding:5px"))
            t.Add(r)
            r = HTML.Row()
            r.Add(HTML.HeaderCell("Status", style="padding:5px"))
            if self.status == "Requested" and self.created:
                status = "Requested on %s at %s" % (FormatDate(self.created),
                                                    FormatTime(self.created))
            else:
                status = self.status
            r.Add(HTML.Cell(status, style="padding:5px"))
            t.Add(r)
            if updating:
                conflicts = self.CheckConflicts(checkRepeats=True)
            else:
                conflicts = self.CheckConflicts()
            if conflicts:
                r = HTML.Row()
                r.Add(HTML.HeaderCell("Conflicts", 
                                      style="padding:5px;color:red"))
                c = HTML.Cell(style="padding:5px")
                c.Add(ListConflicts(conflicts))
                r.Add(c)
                t.Add(r)
            if self.repeats:
                r = HTML.Row()
                r.Add(HTML.HeaderCell("Repeats", style="padding:5px"))
                c = HTML.Cell(class_="sunday", 
                              style="padding:5px;text-align:center")
                if updating and hasattr(self, "pattern"):
                    c.Add(HTML.Checkboxes("repeats", self.repeats, 
                                          self.repeats, 
                                          StripIDs(self.repeats), 
                                          columns=3))
                else:
                    c.Add(PrintModule.RepeatList(self.repeats))
                    if updating:
                        for repeat in self.repeats:
                            c.Add(HTML.HiddenInput("repeats", repeat))
                r.Add(c)
                t.Add(r)
            if updating:
                f.Add(t)
                f.Add(HTML.HiddenInput("ID", self.ID))
                cell.Add(f)
            else:
                f = self.EventOptions()
                cell.Add(t)
                cell.Add(f)
        else:
            cell.Add(t)
        if self.status == "Approved" and not updating:
            t = HTML.Table([480], cellspacing="0", align="center")
            t.Add(HTML.Row(HTML.HeaderCell("Notification List")))
            if user:
                c = HTML.Cell(HTML.Para("""
                Add email addresses (one per line) that you wish to add
                to the event notification list.  If this is a repeating
                event, they will be added to all the repeats """, 
                                        class_="status"))
            else:
                c = HTML.Cell(HTML.Para("""
                If you wish to be reminded of this event or notified if
                there are any changes, submit your email address here. 
                If this is a repeating event, your email address will be
                added to all the repeats.  Contact the %s Administration
                if you wish to have your address removed.""" % calendarAbbr,
                                        class_="status"))
            f = HTML.Form("AddNotification.py")
            if user:
                f.Add(HTML.Para("%s%s%s" 
                      % (HTML.TextArea("email", rows=5, cols=40),
                         HTML.Break(),
                         HTML.Submit(value="Add Email Addresses")),
                                     class_="center"))
            else:
                f.Add(HTML.Para("%s%s%s" 
                      % (HTML.Input("email", size=40, maxlength=80),
                         HTML.TAB,
                         HTML.Submit(value="Add Email")), class_="center"))
            f.Add(HTML.HiddenInput("ID", self.ID))
            c.Add(f)
            f = HTML.Form("RemoveNotification.py")
            if user and self.notifyList:
                f.Add(HTML.Para("%s%s%s" 
                                % (HTML.Selections("email", self.notifyList, 
                                                   label=True),
                                   HTML.TAB,
                                   HTML.Submit(value="Remove Email")),
                                class_="center"))
                f.Add(HTML.HiddenInput("ID", self.ID))
                c.Add(f)
            t.Add(HTML.Row(c))
            cell.Add(t)
        row.Add(cell)
        row.Add(PrintModule.SideMonthsCell(year, month))
        table.Add(row)
        content.Add(table)
        content.Add(PrintModule.CalendarOptions(year, month, day))
        return HTML.Page(StripHTML(title), content)

    def EventOptions(self):
        """Add links to event options."""
        user = CGImodule.CGIgetUser()
        if user == "admin" or user in GetModule.GetSupervisors():
            supervisor = True
        else:
            supervisor = False
        table = HTML.Table(cellspacing="0", cellpadding="5", align="center")
        row = HTML.Row()
        if self.status == "Requested":
            if supervisor:
                link = "%s/ApproveEvent.py?ID=%s" % (cgiURL, self.ID)
                row.Add(HTML.HeaderCell(HTML.Anchor(link, "Approve Event")))
            elif user:
                link = "%s/RequestEvent.py?ID=%s" % (cgiURL, self.ID)
                row.Add(HTML.HeaderCell(HTML.Anchor(link, "Request Approval")))
        elif not supervisor:
            link = "%s/RequestEvent.py?ID=%s" % (cgiURL, self.ID)
            row.Add(HTML.HeaderCell(HTML.Anchor(link, "Request Change")))
        if user:
            link = "%s/EditEvent.py?ID=%s" % (cgiURL, self.ID)
            row.Add(HTML.HeaderCell(HTML.Anchor(link, "Edit Event")))
            link = "%s/CopyEvent.py?ID=%s" % (cgiURL, self.ID)
            row.Add(HTML.HeaderCell(HTML.Anchor(link, "Copy Event")))
        if supervisor:
            link = "%s/RemoveEvent.py?ID=%s" % (cgiURL, self.ID)
            row.Add(HTML.HeaderCell(HTML.Anchor(link, "Remove Event")))
        if user:
            link = "%s/ViewLog.py?ID=%s" % (cgiURL, self.ID)
            row.Add(HTML.HeaderCell(HTML.Anchor(link, "View Log")))
        if self.status == "Approved":
            link = "%s/NotifyList.py?ID=%s" % (cgiURL, self.ID)
            row.Add(HTML.HeaderCell(HTML.Anchor(link, "Notify List")))
        table.Add(row)
        return table

    def EditPage(self, message=None, copied=False):
        """Print form to add or modify a calendar event."""
        if self.ID:
            new = False
        else:
            new = True
        user = CGImodule.CGIgetUser()
        if user == "admin" or user in GetModule.GetSupervisors():
            supervisor = True
        else:
            supervisor = False
        if hasattr(self, "status"):
            if self.status == "Approved":
                requested = False
            else:
                requested = True
        else:
            requested = True
            self.status = "Requested"
        content = HTML.Container()
        if new:
            title = "Add New Event"
            content.Add(HTML.Header(title))
            self.status = "Requested"
            if not copied:
                self.type = "Event"
        else:
            title = "Event : %s" % self.title
            content.Add(HTML.Header(title, class_="title"))
            if isinstance(self.start, time.struct_time):
                content.Add(HTML.Para("%s" % FormatDate(self.start),
                                      class_="center",
                                      style="font-weight: bold"))
        if message:
            content.Add(HTML.Para(message, class_="alert"))
        form = HTML.Form("ModifyEvent.py")
        table = HTML.Table([150, 550], cellspacing="0", align="center")
        table.Add(HTML.Row(HTML.HeaderCell("Event Description", colspan=2,
                                           class_="empty")))
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Event Title"))
        row.Add(HTML.Cell(HTML.Input("title", self.title, size=80, 
                                     maxlength=255)))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Type"))
        if requested or supervisor:
            options = ["Event", "Special", "Banner", "Holiday", "Private", 
                       "Setup"]
            row.Add(HTML.HeaderCell(HTML.RadioButtons("type", 
                                                      options, self.type),
                                    class_="sunday"))
        else:
            row.Add(HTML.Cell(self.type))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Description"))
        row.Add(HTML.Cell(HTML.TextArea("description",
                                        ConvertBreaks(self.description), 
                                        rows=10, cols=80)))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Location"))
        if requested or supervisor:
            locations = GetModule.GetLocations()
            row.Add(HTML.HeaderCell(HTML.Selections("location", locations, 
                                                    self.location, label=True), 
                                    class_="sunday"))
        else:
            row.Add(HTML.Cell(self.location))
        table.Add(row)
        if requested or supervisor:
            if isinstance(self.start, time.struct_time):
                year = time.strftime("%Y", self.start)
                month = time.strftime("%B", self.start)
                day = time.strftime("%d", self.start).lstrip("0")
                starthour = time.strftime("%I", self.start).lstrip("0")
                startmin = time.strftime("%M", self.start)
                startmeridiem = time.strftime("%p", self.start).lower()
            else:
                year, month, day = None, None, None
                starthour, startmin, startmeridiem = None, None, None
            if isinstance(self.end, time.struct_time):
                endhour = time.strftime("%I", self.end).lstrip("0")
                endmin = time.strftime("%M", self.end)
                endmeridiem = time.strftime("%p", self.end).lower()
            else:
                endhour, endmin, endmeridiem = None, None, None
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Time"))
            row.Add(HTML.HeaderCell("%s:%s%s to %s:%s%s"
                    % (HTML.Selections("starthour", hourList, starthour),
                       HTML.Selections("startminute", minuteList, startmin),
                       HTML.Selections("startampm", meridiemList,startmeridiem),
                       HTML.Selections("endhour", hourList, endhour),
                       HTML.Selections("endminute", minuteList, endmin),
                       HTML.Selections("endampm", meridiemList, endmeridiem)),
                                    class_="sunday"))
            table.Add(row)
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Date"))
            row.Add(HTML.HeaderCell("%s%s, %s"
                    % (HTML.Selections("startmonth", monthList, month),
                       HTML.Selections("startday", dayList, day),
                       HTML.Selections("startyear", yearList, year)),
                                    class_="sunday"))
            table.Add(row)
        else:
            if self.type <> "Banner" and self.type <> "Holiday":
                row = HTML.Row()
                row.Add(HTML.HeaderCell("Time", style="padding:5px"))
                row.Add(HTML.Cell("%s to %s" % (FormatTime(self.start),
                                                FormatTime(self.end)), 
                                  style="padding:5px"))
                table.Add(row)
        if hasattr(self, "pattern"):
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Repeats"))
            cell = HTML.HeaderCell(class_="sunday")
            options = ["Once only", "Daily", "Weekly", "Monthly", 
                       "Annually", "Same Day Monthly"]
            cell.Add("%s%s%s%s%s%s" 
                     % (HTML.Selections("pattern", options, 
                                        selected=self.pattern),
                        HTML.Input("number", 
                                   value=`len(self.repeats)`, size=5, 
                                   maxlength=5),
                        "times OR until",
                        HTML.Selections("endmonth", monthList, month),
                        HTML.Selections("endday", dayList, day),
                        HTML.Selections("endyear", yearList, year)))
            row.Add(cell)
            table.Add(row)
        elif self.repeats:
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Repeats"))
            cell = HTML.HeaderCell(class_="sunday", style="padding:10px")
            options = ["single", "future", "all"]
            descriptions = ["Edit this event only", "Edit future repeats",
                            "Edit all repeats"]
            cell.Add(HTML.RadioButtons("repeat", options, "single", 
                                       descriptions))
            cell.Add(PrintModule.RepeatList(self.repeats))
            for repeat in self.repeats:
                cell.Add(HTML.HiddenInput("repeats", repeat))
            row.Add(cell)
            table.Add(row)
        if new and not copied:
            e = Editor.Editor(user)
            self.organizer = e.name
            self.phone = e.phone
            self.email = e.email
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Organizer"))
        row.Add(HTML.Cell("%s%sOR%s%s"
                          % (HTML.Input("organizer", self.organizer, 
                             size=30, maxlength=255),
                             HTML.TAB, HTML.TAB,
                             HTML.Selections("name", 
                                             GetModule.GetOrganizers(),
                                             label=True))))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Phone"))
        row.Add(HTML.Cell("%s%s%s" 
                          % (HTML.Input("phone", self.phone, size=30, 
                                        maxlength=255),
                             HTML.TAB,
                             HTML.Span("Not displayed in public calendar",
                             style="font-style:italic;font-size:0.75em"))))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Email"))
        row.Add(HTML.Cell("%s%s%s" 
                          % (HTML.Input("email", self.email, size=30, 
                                        maxlength=255),
                             HTML.TAB,
                             HTML.Span("Not displayed in public calendar",
                             style="font-style:italic;font-size:0.75em"))))
        table.Add(row)
        table.Add(HTML.Row(HTML.HeaderCell("Event Reservations", colspan=2,
                                           class_="empty")))
        if requested or supervisor:
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Reservation Times"))
            cell = HTML.HeaderCell(class_="sunday")
            options = ["Same as Event", "Longer than Event", "All Day"]                
            if new and not copied:
                self.reservation["option"] = "Same as Event"
            cell.Add(HTML.RadioButtons("reserve", options, 
                                       self.reservation["option"]))
            cell.Add(HTML.Break())
            start = self.reservation["start"]
            if isinstance(start, time.struct_time):
                starthour = time.strftime("%I", start).lstrip("0")
                startmin = time.strftime("%M", start)
                startmeridiem = time.strftime("%p", start).lower()
            else:
                starthour, startmin, startmeridiem = None, None, None
            end = self.reservation["end"]
            if isinstance(end, time.struct_time):
                endhour = time.strftime("%I", end).lstrip("0")
                endmin = time.strftime("%M", end)
                endmeridiem = time.strftime("%p", end).lower()
            else:
                endhour, endmin, endmeridiem = None, None, None
            cell.Add("%s:%s%s to %s:%s%s"
            % (HTML.Selections("resstarthour", hourList, starthour),
               HTML.Selections("resstartminute", minuteList, startmin),
               HTML.Selections("resstartampm", meridiemList, startmeridiem),
               HTML.Selections("resendhour", hourList, endhour),
               HTML.Selections("resendminute", minuteList, endmin),
               HTML.Selections("resendampm", meridiemList, endmeridiem)))
            row.Add(cell)
            table.Add(row)
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Additional Resources"))
            cell = HTML.HeaderCell(class_="sunday")
            t = HTML.Table([180, 180, 180], class_="transparent", 
                           cellspacing="0", align="center")
            r = HTML.Row()
            c = HTML.HeaderCell("Locations", class_="transparent")
            c.Add(HTML.Break())
            try:
                self.locations.remove(self.location)
            except ValueError:
                pass
            c.Add(HTML.Selections("locations", locations, self.locations,
                                  multiple=True))
            r.Add(c)
            c = HTML.HeaderCell("Resources", class_="transparent")
            c.Add(HTML.Break())
            resources = GetModule.GetResources()
            c.Add(HTML.Selections("resources", resources, self.resources,
                                  multiple=True))
            r.Add(c)
            c = HTML.HeaderCell("Categories", class_="transparent")
            c.Add(HTML.Break())
            categories = GetModule.GetCategories()
            c.Add(HTML.Selections("categories", categories, self.categories, 
                                  multiple=True))
            r.Add(c)
            t.Add(r)
            cell.Add(t)
            row.Add(cell)
            table.Add(row)
        else:
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Locations", style="padding:5px"))
            try:
                self.locations.remove(self.location)
            except ValueError:
                pass
            row.Add(HTML.Cell(", ".join(self.locations), style="padding:5px"))
            for location in self.locations:
                row.Add(HTML.HiddenInput("locations", location))
            table.Add(row)
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Resources", style="padding:5px"))
            row.Add(HTML.Cell(", ".join(self.resources), style="padding:5px"))
            for resource in self.resources:
                row.Add(HTML.HiddenInput("resources", resource))
            table.Add(row)
            row = HTML.Row()
            categories = GetModule.GetCategories()
            row.Add(HTML.HeaderCell("Categories", style="padding:5px"))
            row.Add(HTML.Cell(HTML.Selections("categories", categories, 
                                               self.categories, multiple=True)))
            table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Setup Instructions"))
        row.Add(HTML.Cell(HTML.TextArea("setup",
                                        ConvertBreaks(self.setup), 
                                        rows=5, cols=80)))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Status"))
        if supervisor:
            options = ["Approved", "Requested"]
            row.Add(HTML.HeaderCell(HTML.RadioButtons("status", options, 
                                                      self.status),
                                    class_="sunday"))
        else:
            row.Add(HTML.HeaderCell(self.status, class_="sunday"))
            row.Add(HTML.HiddenInput("status", self.status))
        table.Add(row)
        form.Add(table)
        form.Add(HTML.HiddenInput("editor", user))
        if new:
            form.Add(HTML.Para("%s%s%s"
                               % (HTML.Submit(value="Add Event"),
                                  HTML.TAB,
                                  HTML.Submit("cancel", "Cancel")),
                               class_="center"))
        else:
            form.Add(HTML.Para("%s%s%s"
                               % (HTML.Submit(value="Update Event"),
                                  HTML.TAB,
                                  HTML.Submit("cancel", "Cancel")),
                               class_="center"))
            form.Add(HTML.HiddenInput("ID", self.ID))
        content.Add(form)
        if isinstance(self.start, time.struct_time):
            year, month = self.start[0:2]
        else:
            year, month = None, None
        content.Add(PrintModule.BottomMonthsTable(year, month))
        return HTML.Page(title, content)

    def RemovePage(self):
        """Print form to remove a calendar event."""
        user = CGImodule.CGIgetUser()
        if self.status == "Approved" and user <> "admin" and \
          user not in GetModule.GetSupervisors():
            message = "Not authorized to remove an approved event"
            return self.EventView(message)
        title = "Event : %s" % self.title
        content = HTML.Container()
        content.Add(HTML.Header("Event : %s" % self.title, class_="title"))
        if isinstance(self.start, time.struct_time):
            content.Add(HTML.Para("%s" % FormatDate(self.start),
                                  class_="center", style="font-weight: bold"))
        form = HTML.Form("ConfirmRemoval.py")
        table = HTML.Table([150, 550], cellspacing="0", align="center")
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Event Title", style="padding:5px"))
        row.Add(HTML.Cell(self.title, style="padding:5px"))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Event Type", style="padding:5px"))
        row.Add(HTML.Cell(self.type, style="padding:5px"))
        table.Add(row)
        if self.type <> "Banner" and self.type <> "Holiday":
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Time", style="padding:5px"))
            row.Add(HTML.Cell("%s to %s" % (FormatTime(self.start),
                                            FormatTime(self.end)), 
                              style="padding:5px"))
            table.Add(row)
        if self.repeats:
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Repeats"))
            cell = HTML.HeaderCell("Remove: %s" % HTML.TAB, class_="sunday", 
                                   style="padding:10px")
            options = ["single", "future", "all"]
            descriptions = ["Only this event", "Future repeats", "All repeats"]
            cell.Add(HTML.RadioButtons("repeat", options, "single", 
                                       descriptions))
            cell.Add(PrintModule.RepeatList(self.repeats))
            for repeat in self.repeats:
                cell.Add(HTML.HiddenInput("repeats", repeat))
            row.Add(cell)
            table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Status", style="padding:5px"))
        row.Add(HTML.HeaderCell(self.status, class_="sunday", 
                                style="padding:5px"))
        table.Add(row)
        form.Add(table)
        form.Add(HTML.HiddenInput("editor", user))
        form.Add(HTML.Para("%s%s%s"
                           % (HTML.Submit(value="Confirm Removal"),
                              HTML.TAB,
                              HTML.Submit("cancel", "Cancel")),
                           class_="center"))
        form.Add(HTML.HiddenInput("ID", self.ID))
        content.Add(form)
        if isinstance(self.start, time.struct_time):
            year, month = self.start[0:2]
        else:
            year, month = None, None
        content.Add(PrintModule.BottomMonthsTable(year, month))
        return HTML.Page(title, content)

    def RequestPage(self):
        """Send an email requesting approval of an event."""
        user = CGImodule.CGIgetUser()
        name = Editor.Editor(user).name
        email = Editor.Editor(user).email
        if email:
            email = "&lt;%s&gt;" % email
        else:
            email = ""
        title = "%s Event Request" % calendarAbbr
        content = HTML.Container()
        content.Add(HTML.Header("%s Event Request" % calendarAbbr, 
                                class_="title"))
        content.Add(HTML.Para("""
        The following message will be sent to the %s Administration.  If you
        wish to add a message, please use the text box below.
        """ % calendarName))
        table = HTML.Table([600], align="center", cellspacing="0", 
                           cellpadding="20")
        if self.status == "Requested":
            prefix = "Your approval of"
        else:
            prefix = "A change to"
        table.Add(HTML.Row(HTML.Cell(ConvertCRLFs("""\
%s the following %s event has been requested:

Title: %s
Date: %s
Time: %s to %s
Location: %s
Resource: %s
Category: %s

Requested by: %s %s

Please visit the following URL to approve or modify the requested event:

&lt;%s/ViewEvent.py?ID=%s&gt;
""" % (prefix, calendarAbbr, self.title, FormatDate(self.start, day=True), 
       FormatTime(self.start), FormatTime(self.end), 
       ", ".join(self.locations), ", ".join(self.resources), 
       ", ".join(self.categories), 
       name, email, cgiURL, self.ID)))))
        content.Add(table)
        form = HTML.Form("SendRequest.py")
        table = HTML.Table([150, 450], cellspacing="0", align="center")
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Message"))
        row.Add(HTML.Cell(HTML.TextArea("message")))
        table.Add(row)
        form.Add(table)
        form.Add(HTML.Para("%s%s%s"
                           % (HTML.Submit(value="Send Message"),
                              HTML.TAB,
                              HTML.Submit("cancel", "Cancel")),
                           class_="center"))
        form.Add(HTML.HiddenInput("ID", self.ID))
        form.Add(HTML.HiddenInput("prefix", prefix))
        content.Add(form)
        content.Add(PrintModule.CalendarOptions())
        year, month = self.start[0:2]
        content.Add(PrintModule.BottomMonthsTable(year, month))
        return HTML.Page(title, content)

    def NotifyPage(self):
        """Send an email notification to those who have requested it."""
        user = CGImodule.CGIgetUser()
        name = Editor.Editor(user).name
        email = Editor.Editor(user).email
        if email:
            email = "&lt;%s&gt;" % email
        else:
            email = ""
        title = "Event Log: %s" % self.title
        content.Add(HTML.Header("%s Event Notification" % calendarAbbr, 
                                class_="title"))
        content.Add(HTML.Para("""
        The following message will be sent to the list of those who
        requested notification of this event.  It contains the main
        details of the event.  If you wish to add a message, please use
        the text box below.
        """))
        table = HTML.Table([600], align="center", cellspacing="0", 
                           cellpadding="20")
        table.Add(HTML.Row(HTML.Cell(ConvertCRLFs("""\
Title: %s
Date: %s
Time: %s to %s
Location: %s

%s

Please visit the following URL to view further details:

&lt;%s/ViewEvent.py?ID=%s&gt;

If you wish to be removed from the notification list for this event, 
please contact the %s Administration.
""" % (self.title, FormatDate(self.start, day=True), 
       FormatTime(self.start), FormatTime(self.end), self.location,
       ConvertBreaks(self.description), cgiURL, self.ID, calendarAbbr)))))
        content.Add(table)
        form = HTML.Form("SendNotification.py")
        table = HTML.Table([150, 450], cellspacing="0", align="center")
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Message"))
        row.Add(HTML.Cell(HTML.TextArea("message")))
        table.Add(row)
        form.Add(table)
        form.Add(HTML.Para("%s%s%s"
                           % (HTML.Submit(value="Send Message"),
                              HTML.TAB,
                              HTML.Submit("cancel", "Cancel")),
                               class_="center"))
        form.Add(HTML.HiddenInput("ID", self.ID))
        content.Add(form)
        content.Add(PrintModule.CalendarOptions())
        year, month = self.start[0:2]
        content.Add(PrintModule.BottomMonthsTable(year, month))
        return HTML.Page(title, content)

    def MessagePage(self):
        """Send an email to the event organizer (hiding their address)."""
        if IsEmail(self.email):            
            user = CGImodule.CGIgetUser()
            if user in GetModule.GetEditors():
                e = GetModule.GetEditor(user)
                name = e.name
                email = e.email
            else:
                name = ""
                email = ""
            title = "%s Event Message" % calendarAbbr
            content = HTML.Container()
            content.Add(HTML.Header("%s Event Message" % calendarAbbr, 
                                    class_="title"))
            content.Add(HTML.Para("""
            Use this form to send an email to the organizer of the
            event.  You must supply your name and a valid email address,
            but this information will not be stored.
            """))
            form = HTML.Form("SendMessage.py")
            table = HTML.Table([150, 450], cellspacing="0", align="center")
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Name"))
            row.Add(HTML.Cell(HTML.Input("name", name, size=50)))
            table.Add(row)
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Email"))
            row.Add(HTML.Cell(HTML.Input("email", email, size=50)))
            table.Add(row)
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Subject"))
            row.Add(HTML.Cell(HTML.Input("subject", size=50)))
            table.Add(row)
            row = HTML.Row()
            row.Add(HTML.HeaderCell("Message"))
            row.Add(HTML.Cell(HTML.TextArea("message")))
            table.Add(row)
            form.Add(table)
            form.Add(HTML.Para("%s%s%s"
                               % (HTML.Submit(value="Send Message"),
                                  HTML.TAB,
                                  HTML.Submit("cancel", "Cancel")),
                                  class_="center"))
            form.Add(HTML.HiddenInput("ID", self.ID))
            content.Add(form)
            content.Add(PrintModule.CalendarOptions())
            year, month = self.start[0:2]
            content.Add(PrintModule.BottomMonthsTable(year, month))
            return HTML.Page(title, content)
        else:
            self.PrintEventView("The organizer's email address is unavailable.")

    def LogPage(self):
        """Print logs of event updates."""
        year, month, day = self.start[0:3]
        title = "Event Log: %s" % self.title
        content = HTML.Container()
        content.Add(HTML.Header("Event Log: %s" % self.title, class_="title"))
        table = HTML.Table([500, 200], cellspacing="0", align="center")
        row = HTML.Row()
        cell = HTML.Cell()
        t = HTML.Table([190,90,200], cellpadding="5")
        r = HTML.Row()
        r.Add(HTML.HeaderCell("Time"))
        r.Add(HTML.HeaderCell("User"))
        r.Add(HTML.HeaderCell("Log"))
        t.Add(r)
        for log in self.logs:
            r = HTML.Row(HTML.HeaderCell(log[0], class_="sunday",
                         style="font-size:0.9em"))
            r.Add(HTML.Cell(log[1], style="text-align: center"))
            r.Add(HTML.Cell(log[2].replace('\n','<br>\n')))
            t.Add(r)
        cell.Add(t)
        t = HTML.Table(cellspacing="0", cellpadding="5", align="center")
        r = HTML.Row()
        link = "%s/ViewEvent.py?ID=%s" % (cgiURL, self.ID)
        r.Add(HTML.HeaderCell(HTML.Anchor(link, "View Event")))
        t.Add(r)
        cell.Add(t)
        row.Add(cell)
        row.Add(PrintModule.SideMonthsCell(year, month))
        table.Add(row)
        content.Add(table)
        content.Add(PrintModule.CalendarOptions(year, month, day))
        return HTML.Page(title, content)
        
    def CheckConflicts(self, checkRepeats=False):
        """Check availability of specified locations and/or resources."""
        start = self.reservation["start"]
        end = self.reservation["end"]
        list = []
        if checkRepeats and self.repeats:
            for repeat in self.repeats:
                list.extend(GetConflicts(CopyTime(repeat, start),
                                         CopyTime(repeat, end, end=True),
                                         self.locations, self.resources))
        else:
            try:
                list.extend(GetConflicts(start, end, self.locations, 
                                         self.resources))
            except ValueError:
                raise CalendarError, \
                      "There is a problem with Event ID %s" \
                      % HTML.Anchor("%s/ViewEvent.py?ID=%s" 
                                    % (cgiURL, self.ID), self.ID)
        if "oldID" in self.__dict__.keys():
            thisID = self.oldID
        else:
            thisID = self.ID
        conflicts = []
        for conflict in list:
            ID, locations, resources = conflict
            if ID <> thisID and ID not in self.repeats:
                conflicts.append(conflict)
        return conflicts


class TemporaryEvent(Event):

    """Class for temporary events."""

    def __init__(self, ID=None):
        """Open or create an events database in a temporary directory."""
        self.ID = ""
        self.title = ""
        self.type = "Event"
        self.description = ""
        self.location = ""
        self.start = ""
        self.end = ""
        self.repeats = []
        self.logs = []
        self.organizer = ""
        self.phone = ""
        self.email = ""
        self.reservation = {"start":None,"end":None,"option":"Same as Event"}
        self.locations = []
        self.resources = []
        self.categories = []
        self.setup = ""
        self.status = ""
        self.created = None
        self.editor = ""
        self.notifyList = []
        self.dir = ""
        if ID:
            self.dir = os.path.join(homeDir, ID)
            self.Read()
        else:
            tmpDir = os.path.join(homeDir, "tmp")
            if not os.path.exists(tmpDir):
                omask = os.umask(0)
                os.mkdir(tmpDir)
                os.umask(omask)
            self.ID = os.path.join("tmp", 
                                   "%03d" % GetModule.GetNextEvent("tmp"))
            self.dir = os.path.join(homeDir, self.ID)

    def AddLog(self, log):
        """Add a log entry to the event database with a time stamp."""
        timestamp = FormatTime(time.localtime(time.time()), "ISO8601")
        user = CGImodule.CGIgetUser()
        try:
            self.logs.append((timestamp, user, log))
        except NameError:
            self.logs = [(timestamp, user, log)]


def GetConflicts(start, end, locations, resources):
    """Return a list of potential location and/or resource conflicts."""
    year, month, day = start[0:3]
    events = GetModule.GetEvents(year, month, day)
    conflicts = []
    for e in events:
        if start >= e["reservation"]["end"] or \
           end <= e["reservation"]["start"]:
            pass
        else:
            locationConflicts = []
            for location in locations:
                if location in e["locations"]:
                    locationConflicts.append(location)
            resourceConflicts = []
            for resource in resources:
                if resource in e["resources"]:
                    resourceConflicts.append(resource)
            if locationConflicts or resourceConflicts:
                conflicts.append((e["ID"], locationConflicts, 
                                           resourceConflicts))
    return conflicts

def ListConflicts(conflicts):
    """Output a list of potential location and/or resource conflicts."""
    d = HTML.Div()
    for conflict in conflicts:
        ID, locations, resources = conflict
        e = Event(ID)
        div = HTML.Div(class_="dayview")
        para = HTML.Para(class_="time")
        para.Add("%s %s to %s:" 
                 % (FormatDate(e.reservation["start"]), 
                    FormatTime(e.reservation["start"]), 
                    FormatTime(e.reservation["end"])))
        para.Add(", ".join(locations+resources))
        div.Add(para)
        para = HTML.Para(HTML.Anchor("%s/ViewEvent.py?ID=%s" % (cgiURL, e.ID),
                                     e.title),
                         class_="event")
        div.Add(para)
        d.Add(div)
    return str(d)        

