# PyCal - Python web calendar
#
# Copyright (C) 2004-2006 Ray Osborn
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
# $Id: PrintModule.py,v 1.5 2004/04/30 14:30:37 osborn Exp $
#
"""PyCal module containing web page print modules.

These modules print the HTML output used in various standard forms. 
"""

import os
import calendar
import urllib

from PyCal import *
import CGImodule
import Editor
import Event
import GetModule
import HTML
import LogModule
import OptionModule
import PageModule
import PasswordModule
from Utilities import FormatTime, FormatDay, FormatDate, ReadDate
from Utilities import Today, IsToday
from Utilities import StripID, IDdate, IDexists
from Utilities import WeekList, NextMonth, PreviousMonth, NextDay, PreviousDay

def YearView(year):
    """Return a web page displaying a calendar for the whole year."""
    title = "%s - %s" % (calendarName, CalendarTitle(year))
    content = HTML.Container()
    content.Add(FormatYearView(year))
    content.Add(CalendarOptions(year))
    return HTML.Page(title, content)

def MonthView(year, month, category=None):
    """Return a web page displaying events for the specified month and year."""
    title = "%s - %s" % (calendarName, CalendarTitle(year, month))
    content = HTML.Container()
    if category:
        content.Add(FormatMonthView(year, month, category))
    else:
        content.Add(str(PageModule.Page(year, month)))
    content.Add(CalendarOptions(year, month))
    return HTML.Page(title, content)
    
def DayView(year, month, day, category=None, updated=False):
    """Return a web page displaying events for the specified day."""
    title = "%s - %s" % (calendarName, CalendarTitle(year, month, day))
    content = HTML.Container()
    if updated or category: 
        content.Add(FormatDayView(year, month, day))
    else:
        content.Add(str(PageModule.Page(year, month, day)))
    content.Add(CalendarOptions(year, month, day))
    return HTML.Page(title, content)

def FormatYearView(year):
    """Format a web page displaying a calendar for the whole year."""
    calendar.setfirstweekday(calendar.SUNDAY)
    title = "%s - %s" % (calendarName, CalendarTitle(year))
    content = HTML.Container()
    navbar = NavigationBar(year)
    content.Add(navbar)
    content.Add(HTML.Header(CalendarTitle(year)))
    table = HTML.Table([240, 240, 240], cellspacing="0", align="center")
    row = HTML.Row()
    for month in range(1,4):
        row.Add(HTML.Cell(ReducedMonth(year, month)))
    table.Add(row)
    row = HTML.Row()
    for month in range(4,7):
        row.Add(HTML.Cell(ReducedMonth(year, month)))
    table.Add(row)
    row = HTML.Row()
    for month in range(7,10):
        row.Add(HTML.Cell(ReducedMonth(year, month)))
    table.Add(row)
    row = HTML.Row()
    for month in range(10,13):
        row.Add(HTML.Cell(ReducedMonth(year, month)))
    table.Add(row)
    content.Add(table)
    content.Add(navbar)
    return content
    
def FormatMonthView(year, month, category=None):
    """Format a web page displaying events for the specified month and year."""
    calendar.setfirstweekday(calendar.SUNDAY)
    content = HTML.Container()
    navbar = NavigationBar(year, month)
    content.Add(navbar)
    content.Add(HTML.Header(CalendarTitle(year, month)))
    div = HTML.Div(class_="monthview")
    table = HTML.Table([100, 100, 100, 100, 100, 100, 100], cellspacing="0", 
                       align="center")
    row = HTML.Row()
    for day in calendar.weekheader(10).split():
        row.Add(HTML.HeaderCell(day))
    table.Add(row)
    monthList = calendar.monthcalendar(year, month)
    for week in monthList:
        row = HTML.Row()
        for day in week:
            if day > 0:
                dayLink = HTML.Anchor \
                          ("%s/ViewCalendar.py?year=%d&month=%d&day=%d"
                           % (cgiURL, year, month, day), `day`)                     
                if IsToday(year, month, day):
                    cell = HTML.Cell(HTML.NamedAnchor("today"), class_="today")
                    cell.Add(dayLink)
                elif day == week[0]:
                    cell = HTML.Cell(dayLink, class_="sunday")
                else:
                    cell = HTML.Cell(dayLink)
                cell.Add(EventList(year, month, day))
            else:
                cell = HTML.Cell("&nbsp;", class_="empty")
            row.Add(cell)
        table.Add(row)
    div.Add(table)
    content.Add(div)
    content.Add(navbar)
    return content

def FormatDayView(year, month, day, category=None):
    """Format a web page displaying events for the specified day."""
    calendar.setfirstweekday(calendar.SUNDAY)
    content = HTML.Container()
    content.Add(NavigationBar(year, month, day))
    content.Add(HTML.Header(CalendarTitle(year, month, day)))
    div = HTML.Div(class_="dayview")
    table = HTML.Table([500, 200], cellspacing="0", align="center")
    row = HTML.Row()
    cell = HTML.Cell(HTML.Header("Scheduled Events"))
    cell.Add(HTML.HorizontalRule())
    cell.Add(EventList(year, month, day))
    row.Add(cell)
    row.Add(SideMonthsCell(year, month))
    table.Add(row)
    div.Add(table)
    content.Add(div)
    return content

def LoginPage(errorText=None, script=None, form=None, cgiLocation=cgiURL):
    """Print the login web page."""
    title = "%s Administration Login" % calendarAbbr
    content = HTML.Div()
    content.Add(HTML.Header(title))
    if errorText:
        content.Add(HTML.Para(errorText, class_="alert"))
    if script and form:
        f = HTML.Form(script, location=cgiLocation)
        for key in form.keys():
            f.Add(HTML.HiddenInput(key, form[key]))
    else:
        f = HTML.Form("Login.py")
    f.Add(HTML.Para("%s : %s%s %s : %s" 
                    % (HTML.Strong("Username"),
                       HTML.Input("user", size=12, maxlength=15),
                       HTML.TAB,
                       HTML.Strong("Password"),
                       HTML.Password("password", size=12, maxlength=15)),
                    class_="center"))
    f.Add(HTML.Para(HTML.Submit(value="Submit"), class_="center"))
    content.Add(f)
    content.Add(HTML.Para("%s%s%s" %
    (HTML.Strong("Important:"), 
     "From this point on, you must have cookies enabled in your browser", "otherwise you will not be able to proceed.")))
    content.Add(HTML.Para("%s%s%s" %
    ("Session cookies are used so that you don't need to re-authenticate ",
     "with every operation.  This cookie will expire automatically when ",
     "you exit your browser.")))
    content.Add(HTML.Header("Password Reminder", level=2))
    content.Add(HTML.Para("%s%s%s%s%s" %
    ("If you have forgotten your password, click here to have it sent to ",
     "your email address. If you have forgotten your username, please ",
     "contact the %s Administration &lt;" % calendarAbbr,
     HTML.Anchor("%s", scheme="mailto"),
     "&gt;.")))
    f = HTML.Form("SendReminder.py")
    f.Add(HTML.Para("%s : %s%s%s" 
                    % (HTML.Strong("Username"),
                       HTML.Input("user", size=12, maxlength=15),
                       HTML.TAB,
                       HTML.Submit(value="Email Password")),
                    class_="center"))
    content.Add(f)
    return HTML.Page(title, content)

def ErrorPage(errorText, extraText=None):
    """Print a CGI failure web page."""
    if str(errorText) == "Invalid user and/or password":
        return LoginPage(errorText)
    title = "Calendar Error"
    content = HTML.Div()
    content.Add(HTML.Header(title))
    content.Add(HTML.Para("CalendarError: %s" % errorText, class_="center"))
    if extraText: 
        content.Add(HTML.Para(extraText))
    content.Add(HTML.Para("%s%s%s" %
    ("If you believe that this error represents a bug in the web server, ",
     "please report it to the %s Administration" % calendarAbbr,
     "&lt;%s&gt;." % HTML.Anchor(calendarEmail, scheme="mailto:"))))
    content.Add(CalendarOptions())
    content.Add(BottomMonthsTable())
    return HTML.Page(title, content)
    
def AdminPage(message=None):
    """Print main web page for the calendar administrators."""
    title = '%s Calendar Administration Page' % calendarAbbr
    content = HTML.Container()
    content.Add(HTML.Header(title))
    if message:
        content.Add(HTML.Para(message, class_="alert"))
    content.Add(AdminOptions())
    content.Add(CalendarOptions())
    content.Add(BottomMonthsTable())
    return HTML.Page(title, content)

def EditorsPage(message=None):
    """Print the web page for listing and updating calendar editors."""
    user = CGImodule.CGIgetUser()
    supervisors = GetModule.GetSupervisors()
    if user == "admin" or user in supervisors:
        authorized = True
    else:
        authorized = False
    title = '%s Calendar Editors' % calendarAbbr
    content = HTML.Container()
    content.Add(HTML.Header(title))
    if message:
        content.Add(HTML.Para(message, class_="alert"))
    if authorized:
        table = HTML.Table([100, 200, 200, 150, 50], cellspacing="0", 
                           align="center")
    else:
        table = HTML.Table([100, 200, 200, 200], cellspacing="0", 
                           align="center")
    row = HTML.Row()
    row.Add(HTML.HeaderCell("Username"))
    row.Add(HTML.HeaderCell("Editor Name"))
    row.Add(HTML.HeaderCell("Email"))
    row.Add(HTML.HeaderCell("Phone"))
    if authorized:
        row.Add(HTML.HeaderCell(HTML.TAB))
    table.Add(row)
    for name in GetModule.GetEditors():
        e = Editor.Editor(name)
        row = HTML.Row()
        row.Add(HTML.HeaderCell(e.user, class_="sunday"))
        if name in supervisors:
            row.Add(HTML.HeaderCell("%s<sup>*</sup>" % e.name, 
                                    class_="sunday"))
            row.Add(HTML.HeaderCell(HTML.Anchor(e.email, scheme="mailto:"), 
                                    class_="sunday"))
            row.Add(HTML.HeaderCell(e.phone, class_="sunday"))
        else:
            row.Add(HTML.Cell(e.name, class_="center"))
            row.Add(HTML.Cell(HTML.Anchor(e.email, scheme="mailto:"), 
                              class_="center"))
            row.Add(HTML.Cell(e.phone, class_="center"))
        if authorized:
            row.Add(HTML.HeaderCell(HTML.Anchor("%s/EditEditor.py?editor=%s"
                                                % (cgiURL, 
                                                   urllib.quote(e.user)), 
                                                "Edit..."),       
                                    class_="sunday"))        
        table.Add(row)
    content.Add(table)
    content.Add(HTML.Para("* Calendar Supervisors",
                style="font-size:0.8em; margin-top:0;margin-left:20px"))
    if authorized:
        content.Add(HTML.Header("Add an Editor", level=2))
        content.Add(HTML.Para("""
        Use this form to add an editor, specifying their username and full
        name. The username is used for logins; it defines the Editor object
        and cannot be changed.  The full name and other details can be
        changed at any time.
        """))
        form = HTML.Form("AddEditor.py")
        form.Add(HTML.Para("Username : %s%sEditor Name : %s %s"
                           % (HTML.Input("username", 
                                         size=10, maxlength=25),
                              HTML.TAB,
                              HTML.Input("firstname", 
                                         size=10, maxlength=50),
                              HTML.Input("lastname", 
                                         size=20, maxlength=50)),
                           class_="center"))
        form.Add(HTML.Para(HTML.Submit("add", "Add New Editor..."),
                           class_="center"))
        content.Add(form)
    content.Add(CalendarOptions())
    content.Add(BottomMonthsTable())
    return HTML.Page(title, content)

def ContactsPage(message=None):
    """Print the web page for listing and updating calendar organizers."""
    title = '%s Calendar Organizers' % calendarAbbr
    content = HTML.Container()
    content.Add(HTML.Header(title))
    if message:
        content.Add(HTML.Para(message, class_="alert"))
    table = HTML.Table([250, 250, 150, 50], cellspacing="0", align="center")
    row = HTML.Row()
    row.Add(HTML.HeaderCell("Contact Name"))
    row.Add(HTML.HeaderCell("Email"))
    row.Add(HTML.HeaderCell("Phone"))
    row.Add(HTML.HeaderCell(HTML.TAB))
    table.Add(row)
    for name in GetModule.GetContacts():
        c = Editor.Contact(name)
        row = HTML.Row()
        row.Add(HTML.HeaderCell(c.user, class_="sunday"))
        row.Add(HTML.Cell(HTML.Anchor(c.email, scheme="mailto:"), 
                          class_="center"))
        row.Add(HTML.Cell(c.phone, class_="center"))
        row.Add(HTML.HeaderCell(HTML.Anchor("%s/EditContact.py?contact=%s"
                                            % (cgiURL, urllib.quote(c.user)),
                                            "Edit..."),       
                                class_="sunday"))        
        table.Add(row)
    content.Add(table)
    content.Add(HTML.Header("Add a Contact", level=2))
    content.Add(HTML.Para("""
    Use this form to add a contact, specifying their full name and 
    contact details."""))
    form = HTML.Form("AddContact.py")
    form.Add(HTML.Para("Name : %s %s"
                       % (HTML.Input("firstname", 
                                     size=10, maxlength=50),
                          HTML.Input("lastname", 
                                     size=20, maxlength=50)),
                       class_="center"))
    form.Add(HTML.Para(HTML.Submit("add", "Add New Contact..."),
                       class_="center"))
    content.Add(form)
    content.Add(CalendarOptions())
    content.Add(BottomMonthsTable())
    return HTML.Page(title, content)

def OptionsPage(options, message=None):
    """Print the web page for listing and updating calendar options."""
    user = CGImodule.CGIgetUser()
    if user == "admin" or user in GetModule.GetSupervisors():
        authorized = True
    else:
        authorized = False
    if options == "categories":
        option = "category"
    else:
        option = options[:-1]
    title = '%s Calendar %s' % (calendarAbbr, options)
    content = HTML.Container()
    content.Add(HTML.Header(title))
    if message:
        content.Add(HTML.Para(message, class_="alert"))
    if authorized:
        table = HTML.Table([200, 300, 50], cellspacing="0", 
                           align="center")
    else:
        table = HTML.Table([200, 350], cellspacing="0", 
                           align="center")
    row = HTML.Row()
    row.Add(HTML.HeaderCell("%s" % option.capitalize()))
    row.Add(HTML.HeaderCell("Description"))
    if authorized:
        row.Add(HTML.HeaderCell(HTML.TAB))
    table.Add(row)
    selections = OptionModule.Read(options)
    if selections:
        optionList = selections.keys()
        optionList.sort()
    else:
        optionList = []
    for selection in optionList:
        row = HTML.Row()
        row.Add(HTML.HeaderCell(selection, class_="sunday"))
        if selections[selection]:
            row.Add(HTML.Cell(selections[selection]))
        else:
            row.Add(HTML.Cell(HTML.TAB))
        if authorized:
            row.Add(HTML.HeaderCell(HTML.Anchor("%s/EditOption.py?%s=%s"
                                                % (cgiURL, option, 
                                                   urllib.quote(selection)),
                                                "Edit..."),
                                    class_="sunday"))        
        table.Add(row)
    content.Add(table)
    if authorized:
        content.Add(HTML.Header("Add a %s" % option.capitalize(), level=2))
        content.Add(HTML.Para("""
        Use this form to add a %s and its description to the list of options
        available to calendar events. The description can be changed at any
        time by clicking on Edit... in the above list.  
        """ % option))
        form = HTML.Form("AddOption.py")
        table = HTML.Table([200, 350], cellspacing="0", align="center")
        row = HTML.Row()
        row.Add(HTML.HeaderCell(option.capitalize()))
        row.Add(HTML.Cell(HTML.Input("selection", size=25, 
                                     maxlength=25)))
        table.Add(row)
        row = HTML.Row()
        row.Add(HTML.HeaderCell("Description"))
        row.Add(HTML.Cell(HTML.TextArea("description",
                                        rows=5, cols=40)))
        table.Add(row)
        form.Add(table)
        form.Add(HTML.Para(HTML.Submit("add", 
                                       "Add New %s..." % option.capitalize()),
                           class_="center"))
        form.Add(HTML.HiddenInput("options", options))
        content.Add(form)
    content.Add(CalendarOptions())
    content.Add(BottomMonthsTable())
    return HTML.Page(title, content)
    
def LogsPage():
    """Print the web page for listing the event logs."""
    user = CGImodule.CGIgetUser()
    title = '%s Calendar Event Logs' % calendarAbbr
    content = HTML.Container()
    content.Add(HTML.Header(title))
    table = HTML.Table([200,150,100,250], cellpadding="5")
    row = HTML.Row()
    row.Add(HTML.HeaderCell("Time"))
    row.Add(HTML.HeaderCell("Event"))
    row.Add(HTML.HeaderCell("User"))
    row.Add(HTML.HeaderCell("Log"))
    table.Add(row)
    logs = LogModule.Read()
    for log in logs:
        row = HTML.Row(style="font-size:0.9em")
        row.Add(HTML.HeaderCell(log[0], class_="sunday"))
        ID = log[1]
        link = "%s/ViewEvent.py?ID=%s" % (cgiURL, ID)
        row.Add(HTML.Cell(HTML.Anchor(link, ID),  class_="sunday",
                          style="text-align: center"))
        row.Add(HTML.Cell(log[3],  class_="sunday", style="text-align: center"))
        row.Add(HTML.Cell(log[4].replace('\n','<br>\n'), class_="sunday"))
        table.Add(row)
        row = HTML.Row(style="font-size:0.9em")
        row.Add(HTML.Cell("&nbsp;"))
        row.Add(HTML.Cell(log[2], colspan="3"))
        table.Add(row)
    content.Add(table)
    content.Add(CalendarOptions())
    content.Add(BottomMonthsTable())
    return HTML.Page(title, content)
    
def EmailPage(message, URL=""):
    """Print the email composition page."""
    user = CGIlogin()
    title = "Compose Email"
    content = HTML.Container()
    content.Add(HTML.Header(title))
    content.Add(HTML.Header("Message to %s" % message["addressee"], level=2))
    form = HTML.Form("ConfirmEmail.py")
    table = HTML.Table([150, 550], cellspacing="0", align="center")
    row = HTML.Row()
    row.Add(HTML.HeaderCell("Subject"))
    row.Add(HTML.Cell(HTML.Input("subject", message["subject"],
                                 size=80, maxlength=255)))
    table.Add(row)
    row = HTML.Row()
    row.Add(HTML.HeaderCell("Email Text"))
    row.Add(HTML.Cell(HTML.TextArea("text", message["text"], rows=10, cols=80)))
    table.Add(row)
    content.Add(table)
    content.Add(HTML.Para("Please give your name and a valid email address"))
    table = HTML.Table([150, 550], cellspacing="0", align="center")
    row = HTML.Row()
    row.Add(HTML.HeaderCell("Name"))
    row.Add(HTML.Cell(HTML.Input("name", message["name"], size=80, 
                                 maxlength=255)))
    table.Add(row)
    row = HTML.Row()
    row.Add(HTML.HeaderCell("Email"))
    row.Add(HTML.Cell(HTML.Input("email", message["mailfrom"], size=80, 
                                 maxlength=255)))
    table.Add(row)
    content.Add(table)
    form.Add(HTML.Para("%s%s%s"
                    % (HTML.Submit(value="Prepare Email..."),
                       HTML.TAB,
                       HTML.Submit("cancel", "Cancel")),
                    class_="center"))
    form.Add(HTML.HiddenInput("addressee", message["addressee"]))
    form.Add(HTML.HiddenInput("mailto", message["mailto"]))
    if URL:
        form.Add(HTML.HiddenInput("URL", URL))
    content.Add(form)
    return HTML.Page(title, content)     

def ListForm(message=None):
    """Print the list view page specifying viewing options."""
    title = "%s List View" % calendarName
    content = HTML.Container()
    content.Add(HTML.Header(title))
    if message:
        content.Add(HTML.Para(message, class_="alert"))
    content.Add(HTML.Para("""
    Use this form to list events between the selected dates according to 
    criteria defined by the drop-down menus.  If no criteria are selected, 
    all the events will be listed.
    """))
    form = HTML.Form("ListEvents.py")
    table = HTML.Table(cols=[200,200,200], align="center", cellspacing="0")
    row = HTML.Row()
    row.Add(HTML.HeaderCell(HTML.Selections("location", 
                                            GetModule.GetLocations(),
                                            label=True),
                            class_="sunday"))
    row.Add(HTML.HeaderCell(HTML.Selections("resource",        
                                            GetModule.GetResources(), 
                                            label=True),
                            class_="sunday"))
    row.Add(HTML.HeaderCell(HTML.Selections("category", 
                                            GetModule.GetCategories(),
                                            label=True),
                            class_="sunday"))
    table.Add(row)
    year, month, day = Today()
    row = HTML.Row()
    row.Add(HTML.HeaderCell("From %s%s, %s%sfor%s%s days"
                            % (HTML.Selections("startmonth", monthList, 
                                               monthList[month-1]),
                               HTML.Selections("startday", dayList, `day`),
                               HTML.Selections("startyear", yearList, `year`),
                               HTML.TAB, HTML.TAB,
                               HTML.Input("length", 
                                          value=str(14), size=3, maxlength=3)),
                               colspan="3", class_="sunday"))
    table.Add(row)
    row = HTML.Row()
    options = ["normal", "compressed", "signpost", "notice", "weekly"]
    descriptions = ["Regular", "Compressed", "Signpost", "Notice", "Weekly"]
    row.Add(HTML.HeaderCell(HTML.RadioButtons("layout", options, "normal", 
                                              descriptions),
                            colspan="3", class_="sunday"))
    table.Add(row)
    user = CGImodule.CGIgetUser()
    if user:
        row = HTML.Row()
        options = ["Event", "Special", "Banner", "Holiday", "Private", "Setup"]
        row.Add(HTML.HeaderCell(HTML.Checkboxes("type", options, 
                                ["Event", "Special", "Banner", "Holiday", 
                                 "Private"]),
                                colspan="3", class_="sunday"))
        table.Add(row)
        row = HTML.Row()
        options = ["all", "setup"]
        descriptions = ["All Events", "Events with Setup"]
        row.Add(HTML.HeaderCell(HTML.RadioButtons("setup", options, "all", 
                                                  descriptions),
                                colspan="3", class_="sunday"))
        table.Add(row)
        row = HTML.Row()
        options = ["Approved", "Requested"]
        row.Add(HTML.HeaderCell(HTML.Checkboxes("status", options, 
                                ["Approved"]), colspan="2", class_="sunday"))
        row.Add(HTML.HeaderCell(HTML.Selections("organizer", 
                                                GetModule.GetOrganizers(),
                                                label=True),
                                class_="sunday"))
        table.Add(row)
    row = HTML.Row(HTML.HeaderCell(HTML.Submit(value="List Events"),
                                   class_="sunday", colspan="3"))
    table.Add(row)
    form.Add(table)
    content.Add(form)
    content.Add(CalendarOptions())
    content.Add(BottomMonthsTable())
    return HTML.Page(title, content)


def ListPage(year, month, day, length, type=None, status=None, layout=None, 
             organizer=None, location=None, resource=None, category=None):
    """Print a list of public events according to certain criteria.""" 
    content = HTML.Container()
    title = []
    if location or resource or category:
        if category:
            title.append(category)
        if location:
            title.append(location)
        if resource:
            title.append(resource)
        if organizer:
            title.append(organizer)
        title = ", ".join(title)
    if layout == "weekly":
        calendar.setfirstweekday(calendar.SUNDAY)
        weeks = WeekList(year, month, day, length)
        sy, sm, sd = weeks[0]
        ey, em, ed = weeks[-1]
        if title:
            content.Add(HTML.Header(title))
        content.Add(HTML.Header("%s to %s" % (FormatDay(sy, sm, sd), 
                                              FormatDay(ey, em, ed))))
        div = HTML.Div(class_="monthview")
        table = HTML.Table([100, 100, 100, 100, 100, 100, 100], 
                           cellspacing="0", align="center")
        row = HTML.Row()
        for day in calendar.weekheader(10).split():
            row.Add(HTML.HeaderCell(day))
        table.Add(row)
        for y, m, d in weeks:
            dayLink = HTML.Anchor("%s/ViewCalendar.py?year=%d&month=%d&day=%d"
                                  % (cgiURL, y, m, d), `d`)
            week, day = divmod(weeks.index((y,m,d)),7)
            if day == 0:
                if week > 0:
                    table.Add(row)
                row = HTML.Row()
                cell = HTML.Cell(dayLink, class_="sunday")
            else:
                cell = HTML.Cell(dayLink)
            events = GetModule.GetEvents(y, m, d, type, status, organizer,
                                         location, resource, category)
            for e in events:
                if not e["title"]:
                    e["title"] = "Untitled"
                if e["type"] == "Banner":
                    cell.Add(HTML.Header(HTML.Anchor("%s/ViewEvent.py?ID=%s" 
                                                     % (cgiURL, e["ID"]),
                                                     e["title"]),
                                         level=2, class_="title"))
                elif e["type"] == "Holiday":
                    cell.Add(HTML.Header(e["title"], level=2, class_="title"))
                else:
                    cell.Add(HTML.Para(FormatTime(e["start"]), class_="time"))
                    if e["type"] == "Special":
                        title = HTML.Span(e["title"], style="font-weight:bold")
                    else:
                        title = e["title"]
                    cell.Add(HTML.Para(HTML.Anchor("%s/ViewEvent.py?ID=%s" 
                                                   % (cgiURL, e["ID"]),
                                                   title),
                                       class_="event"))
                    if not location:
                        cell.Add(HTML.Para(e["location"], class_="location"))
            row.Add(cell)
        table.Add(row)
        div.Add(table)
        content.Add(div)
        content.Add(CalendarOptions())
        content.Add(BottomMonthsTable(year, month))
    else:
        content.Add(HTML.Header("%s Calendar Events" % calendarAbbr))
        table = HTML.Table(cols=[500, 200], cellspacing="0", cellpadding="10",
                           align="center")
        row = HTML.Row()
        cell = HTML.Cell(style="background-color:transparent")
        if title:
            cell.Add(HTML.Header(title, style="text-decoration:underline"))
        if layout == "normal":
            cell.Add(CurrentList(year, month, day, length, type, status,
                                 location, resource, category))
        elif layout == "compressed":
            cell.Add(CompressedList(year, month, day, length, type, status,
                                    location, resource, category))
        elif layout == "signpost":
            cell.Add(SignpostList(year, month, day, length, type, status,
                                  location, resource, category))
        elif layout == "notice":
            cell.Add(NoticeList(year, month, day, length, type, status,
                                location, resource, category))
        row.Add(cell)
        row.Add(SideMonthsCell(year, month))
        table.Add(row)
        content.Add(table)
        content.Add(CalendarOptions())
    return HTML.Page("%s Calendar Events" % calendarAbbr, content)

def AdminOptions():
    """Print administrative options."""
    user = CGImodule.CGIgetUser()
    output = HTML.Container()
    output.Add(HTML.Header("Calendar Options", level=2))
    output.Add(HTML.Para("%s%s%s%s" %
    ("Calendar events can be scheduled in a particular location, allocated a ",
     "particular resource, and assigned a particular category.  View a list ",
     "of all these event options and their descriptions by clicking on one ",
     "of the buttons below.""")))
    f = HTML.Form("ViewOptions.py")
    p = HTML.Para(class_="center")
    p.Add(HTML.Submit("locations", "View Locations..."))
    p.Add(HTML.TAB)
    p.Add(HTML.Submit("resources", "View Resources..."))
    p.Add(HTML.TAB)
    p.Add(HTML.Submit("categories", "View Categories..."))
    f.Add(p)
    output.Add(f)
    output.Add(HTML.Header("Calendar Logs", level=2))
    output.Add(HTML.Para("%s%s%s" %
    ("This is a list of all recent changes made to the calendar.  Each ",
     "event contains a log of all creation and modification dates, ",
     "but this is a list of the most recent log entries.""")))
    f = HTML.Form("ViewLogs.py")
    f.Add(HTML.Para(HTML.Submit(value="View Event Logs..."),
                    class_="center"))
    output.Add(f)
    output.Add(HTML.Header("Calendar Editors", level=2))
    output.Add(HTML.Para("%s%s%s" %
    ("This is a list of all the people who have the authority to add or ",
     "modify this calendar, along with their phone numbers and email ",
     "addresses.  The list is not available to the public.""")))
    f = HTML.Form("ViewEditors.py")
    f.Add(HTML.Para(HTML.Submit(
                    value="View List of Calendar Editors..."),
                    class_="center"))
    output.Add(f)
    output.Add(HTML.Header("Calendar Contacts", level=2))
    output.Add(HTML.Para("%s%s%s%s%s" %
    ("This is a list of people who are potential organizers of events, ",
     "but who do not have editor privilege.  This list is provided to ",
     "make it easy for calendar supervisors to include full contact ",
     "information when they enter events on behalf of non-editors. ",
     "The list is not available to the public.""")))
    f = HTML.Form("ViewContacts.py")
    f.Add(HTML.Para(HTML.Submit(value="View List of Contacts..."),
                    class_="center"))
    output.Add(f)
    if user == "admin" or user in GetModule.GetSupervisors():
        output.Add(HTML.Header("Calendar Updates", level=2))
        output.Add(HTML.Para("%s%s%s%s%s%s%s" %
        ("Use this form to update a day or month view immediately.  If an ",
         "event is added or modified, the day view is updated immediately. ",
         "However, the month view and the day view of subsequent repeats are ",
         "updated by a background process, which is currently launched every ",
         "20 minutes.  This form is provided in case an update is required ",
         "more urgently, or if an update was unsuccessful.  Please note that ", 
         "month updates can take a long time to process.""")))
        f = HTML.Form("UpdateCalendar.py")
        year, month, day = Today()
        month = monthList[month-1]
        f.Add(HTML.Para("%s%s, %s" 
                           % (HTML.Selections("month", monthList, month),
                              HTML.Selections("day", dayList, `day`),
                              HTML.Selections("year", yearList, `year`)),
                           class_="center"))
        f.Add(HTML.Para("%s%s%s" 
                        % (HTML.Submit("dayview", "Update Day"),
                           HTML.TAB,
                           HTML.Submit("monthview", "Update Month")),
                        class_="center"))
        output.Add(f)
    return output   

def EventList(year, month, day):
    """Print a list of events for the given day."""
    user = CGImodule.CGIgetUser()
    output = HTML.Div()
    events = GetModule.GetEvents(year, month, day)
    for e in events:
        if not e["title"]:
            e["title"] = "Untitled"
        if e["type"] == "Banner":
            output.Add(HTML.Header(HTML.Anchor("%s/ViewEvent.py?ID=%s" 
                                               % (cgiURL, e["ID"]),
                                               e["title"]),
                                   level=2, class_="title"))
        elif e["type"] == "Holiday":
            title = HTML.Span(e["title"], class_="holiday")
            output.Add(HTML.Header(HTML.Anchor("%s/ViewEvent.py?ID=%s" 
                                               % (cgiURL, e["ID"]),
                                               title),
                                   level=2, class_="title"))
        else:
            if user:
                span = HTML.Span(" to %s" % FormatTime(e["end"]), 
                                 class_="hide")
                if e["reservation"]["start"] <> e["start"] or \
                   e["reservation"]["end"] <> e["end"]:
                    span.Add(" (%s to %s)"
                             % (FormatTime(e["reservation"]["start"]),
                                FormatTime(e["reservation"]["end"])))
                para = HTML.Para("%s%s" % (FormatTime(e["start"]), span),
                                 class_="time")
                if e["setup"]:
                    output.Add(HTML.Div(para, class_="setup"))
                else:
                    output.Add(para)
            else:
                output.Add(HTML.Para(FormatTime(e["start"]), class_="time"))
            if user and Event.Event(e["ID"]).CheckConflicts():
                div = HTML.Div(class_="conflict")
            elif e["status"] == "Requested":
                div = HTML.Div(class_="requested")
            elif e["type"] == "Private":
                div = HTML.Div(class_="private")
            elif e["type"] == "Setup":
                div = HTML.Div(class_="setup")
            else:
                div = HTML.Div()
            if e["type"] == "Special":
                title = HTML.Span(e["title"], style="font-weight:bold")
            else:
                title = e["title"]
            div.Add(HTML.Para(HTML.Anchor("%s/ViewEvent.py?ID=%s" 
                                          % (cgiURL, e["ID"]),
                                          title),
                              class_="event"))
            if user:
                para = HTML.Para(e["location"], class_="location")
                if e["location"] in e["locations"]:
                    e["locations"].remove(e["location"])
                if e["locations"]:
                    para.Add(HTML.Span("(%s)" % ", ".join(e["locations"]),
                                       class_="hide"))
                div.Add(para)
            else:
                div.Add(HTML.Para(e["location"], class_="public"))
            output.Add(div)
    if output.items:
        return output
    else:
        return ""    

def CurrentList(year, month, day, length, type, status, organizer=None,
                location=None, resource=None, category=None):
    """Print a list of events for the given day."""
    output = HTML.Div(class_="listview")
    y, m, d = year, month, day
    for next in range(length):
        div = HTML.Div()
        events = GetModule.GetEvents(y, m, d, type, status, organizer,
                                     location, resource, category)
        meetings = False
        for e in events:
            if not e["title"]:
                e["title"] = "Untitled"
            if "Banner" in type and e["type"] == "Banner":
#               if location or resource or category:
#                    pass
#                else:
                div.Add(HTML.Header(HTML.Anchor("%s/ViewEvent.py?ID=%s" 
                                                % (cgiURL, e["ID"]),
                                                e["title"]),
                                    style="margin:0", level=3))
            elif "Holiday" in type and e["type"] == "Holiday":
                title = HTML.Span(e["title"], class_="holiday")
                div.Add(HTML.Header(HTML.Anchor("%s/ViewEvent.py?ID=%s" 
                                                % (cgiURL, e["ID"]),
                                                title),
                                    style="margin:0", level=3))
            else:
                meetings = True
                div.Add(HTML.Para(FormatTime(e["start"]), class_="time"))
                if e["type"] == "Special":
                    title = HTML.Span(e["title"], style="font-weight:bold")
                else:
                    title = e["title"]
                div.Add(HTML.Para(HTML.Anchor("%s/ViewEvent.py?ID=%s"                                               
                                              % (cgiURL, e["ID"]),
                                              title),
                                  class_="event"))
                if location == None:
                    div.Add(HTML.Para(e["location"], class_="location"))
        if meetings:
            output.Add(HTML.Header(FormatDay(y, m, d), level=3))
            output.Add(div)
        y, m, d = NextDay(y, m, d)    
    if output.items:
        return output
    else:
        return ""    

def CompressedList(year, month, day, length, type, status, organizer=None,
                   location=None, resource=None, category=None):
    """Print a list of events for the given day in a compressed format."""
    output = HTML.Div(style="color:black")
    y, m, d = year, month, day
    for next in range(length):
        div = HTML.Div()
        events = GetModule.GetEvents(y, m, d, type, status, organizer,
                                     location, resource, category)
        meetings = False
        for e in events:
            if not e["title"]:
                e["title"] = "Untitled"
            if ("Banner" in type and e["type"] == "Banner") or \
               ("Holiday" in type and e["type"] == "Holiday"):
                if location or resource or category:
                    pass
                else:
                    div.Add(HTML.Header(e["title"], style="margin:0", 
                                        level=3))
            else:
                meetings = True
                if e["type"] == "Special":
                    title = HTML.Span(e["title"], style="font-weight:bold")
                else:
                    title = e["title"]
                div.Add("%s - %s" % (FormatTime(e["start"]), title))
                div.Add(HTML.Break())
        if meetings:
            output.Add(HTML.Span(FormatDay(y, m, d), style="font-weight:bold"))
            output.Add(HTML.Break())
            output.Add(div)
        y, m, d = NextDay(y, m, d)
    if output.items:
        return output
    else:
        return ""    

def SignpostList(year, month, day, length, type, status, organizer=None,
                 location=None, resource=None, category=None):
    """Print a list of events for the given day in a one-line format."""
    output = HTML.Div(style="color:black")
    y, m, d = year, month, day
    for next in range(length):
        div = HTML.Div()
        events = GetModule.GetEvents(y, m, d, type, status, organizer,
                                     location, resource, category)
        meetings = False
        for e in events:
            if not e["title"]:
                e["title"] = "Untitled"
            if ("Banner" in type and e["type"] == "Banner") or \
               ("Holiday" in type and e["type"] == "Holiday"):
                if location or resource or category:
                    pass
                else:
                    div.Add(HTML.Header(e["title"], style="margin:0", 
                                        level=3))
            else:
                meetings = True
                if e["type"] == "Special":
                    title = HTML.Span(e["title"], style="font-weight:bold")
                else:
                    title = e["title"]
                div.Add("%s - %s - %s" % (FormatTime(e["start"]), 
                                          title, e["location"]))
                div.Add(HTML.Break())
        if meetings:
            output.Add(HTML.Span(FormatDay(y, m, d), style="font-weight:bold"))
            output.Add(HTML.Break())
            output.Add(div)
        y, m, d = NextDay(y, m, d)
    if output.items:
        return output
    else:
        return ""    

def NoticeList(year, month, day, length, type, status, organizer=None,
               location=None, resource=None, category=None):
    """Print a list of events for the given day in a two-line format."""
    output = HTML.Div(class_="listview", style="color:black")
    y, m, d = year, month, day
    for next in range(length):
        div = HTML.Div()
        events = GetModule.GetEvents(y, m, d, type, status, organizer,
                                     location, resource, category)
        meetings = False
        for e in events:
            if not e["title"]:
                e["title"] = "Untitled"
            if "Banner" in type and e["type"] == "Banner":
                if location or resource or category:
                    pass
                else:
                    div.Add(HTML.Header(e["title"], style="margin:0", 
                                        level=3))
            elif "Holiday" in type and e["type"] == "Holiday":
                div.Add(HTML.Header(e["title"], style="margin:0", level=3))
            else:
                meetings = True
                text = FormatTime(e["start"])
                if location == None and e["location"]:
                    text = "%s - %s" % (text, e["location"])
                div.Add(HTML.Para(text, class_="time", style="color:black"))
                if e["type"] == "Special":
                    title = HTML.Span(e["title"], style="font-weight:bold")
                else:
                    title = e["title"]
                div.Add(HTML.Para(title, style="margin:0px 0px 3px 0px", 
                                  class_="event"))
        if meetings:
            output.Add(HTML.Header(FormatDay(y, m, d), level=3))
            output.Add(div)
        y, m, d = NextDay(y, m, d)    
    if output.items:
        return output
    else:
        return ""    

def WikiList(year, month, day, length, type, status, organizer=None,
               location=None, resource=None, category=None):
    """Print a list of events for the given day in a two-line format."""
    output = HTML.Div(class_="listview", style="color:black")
    y, m, d = year, month, day
    for next in range(length):
        div = HTML.Preformatted()
        events = GetModule.GetEvents(y, m, d, type, status, organizer,
                                     location, resource, category)
        meetings = False
        for e in events:
            if not e["title"]:
                e["title"] = "Untitled"
            if "Banner" in type and e["type"] == "Banner":
                if location or resource or category:
                    pass
                else:
                    div.Add('|-')
                    div.Add('! align="left" colspan="3" | %s' % e["title"])                                         
            elif "Holiday" in type and e["type"] == "Holiday":
                div.Add('|-')
                div.Add('! align="left" colspan="3" | %s' % e["title"])                                         
            else:
                meetings = True
                div.Add('|-')
                div.Add('| align="right" valign="top" width="50"  | %s' 
                        % FormatTime(e["start"]))
                div.Add('| align="center" valign="top" width="10" | -')
                div.Add('| align="left" |' % e["title"])
        if meetings:
            output.Add('{| width="100%"')
            output.Add('|-')
            output.Add('! align="left" colspan="3" | %s' % FormatDay(y, m, d))
            output.Add(div)
        y, m, d = NextDay(y, m, d)    
    if output.items:
        return output
    else:
        return ""    

def RepeatList(repeatIDs):
    """Print a table of links to repeat IDs."""
    rows, cols = divmod(len(repeatIDs), 3)
    if rows > 0: 
        cols = 3
    columns = [120 for x in range(cols)]
    table = HTML.Table(columns, cellspacing="0", align="center")
    row = HTML.Row()
    column = 1
    for ID in repeatIDs:
        link = "%s/ViewEvent.py?ID=%s" % (cgiURL, ID)
        row.Add(HTML.HeaderCell(HTML.Anchor(link, StripID(ID))))
        column = column + 1
        if column > 3:
            table.Add(row)
            row = HTML.Row()
            column = 1
    table.Add(row)
    return table

def ReducedMonth(year, month, links=False):
    """Print a small table containing the days in a specified month."""
    calendar.setfirstweekday(calendar.SUNDAY)
    output = HTML.Div(style="font-size:0.9em")
    if links:
        header = HTML.Table([16, 138, 16], align="center", style="margin:0", 
                            cellspacing="0", border="0", class_="transparent")
        row = HTML.Row()
        row.Add(HTML.HeaderCell(PreviousLink(year, month, small=True),
                                style="vertical-align:bottom",
                                class_="transparent"))
        row.Add(HTML.HeaderCell(HTML.Header(MonthLink(year, month), level=2,
                                            class_="title"),
                                class_="transparent"))
        row.Add(HTML.HeaderCell(NextLink(year, month, small=True), 
                                style="vertical-align:bottom",
                                class_="transparent"))
        header.Add(row)
    else:
        header = HTML.Header(MonthLink(year, month), level=2, class_="title")
    output.Add(header)
    table = HTML.Table([23, 23, 23, 23, 23, 23, 23], cellspacing="0", 
                       align="center")
    row = HTML.Row()
    for day in calendar.weekheader(2).split():
        row.Add(HTML.HeaderCell(day))
    table.Add(row)
    monthList = calendar.monthcalendar(year, month)
    for week in monthList:
        row = HTML.Row()
        for day in week:
            if day > 0:
                dayLink = HTML.Anchor \
                          ("%s/ViewCalendar.py?year=%d&month=%d&day=%d"
                           % (cgiURL, year, month, day), `day`)
                if IsToday(year, month, day):
                    cell = HTML.HeaderCell(dayLink, class_="today")
                elif day == week[0]:
                    cell = HTML.HeaderCell(dayLink, class_="sunday")
                else:
                    cell = HTML.HeaderCell(dayLink, class_="weekday")
            else:
                cell = HTML.Cell("&nbsp;", class_="empty")
            row.Add(cell)
        table.Add(row)
    output.Add(table)
    return output

def ReducedMonthSmall(year, month, links=False):
    """Print a smaller table containing the days in a specified month."""
    calendar.setfirstweekday(calendar.SUNDAY)
    output = HTML.Div(style="font-size:0.8em")
    if links:
        header = HTML.Table([16, 117, 16], align="center", style="margin:0", 
                            cellspacing="0", border="0", class_="transparent")
        row = HTML.Row()
        row.Add(HTML.HeaderCell(PreviousLink(year, month, smaller=True),
                                style="vertical-align:bottom",
                                class_="transparent"))
        row.Add(HTML.HeaderCell(HTML.Header(MonthLink(year, month), level=2,
                                            class_="title"),
                                class_="transparent"))
        row.Add(HTML.HeaderCell(NextLink(year, month, smaller=True), 
                                style="vertical-align:bottom",
                                class_="transparent"))
        header.Add(row)
    else:
        header = HTML.Header(MonthLink(year, month), level=2, class_="title")
    output.Add(header)
    table = HTML.Table([20, 20, 20, 20, 20, 20, 20], cellspacing="0", 
                       align="center")
    row = HTML.Row()
    for day in calendar.weekheader(2).split():
        row.Add(HTML.HeaderCell(day))
    table.Add(row)
    monthList = calendar.monthcalendar(year, month)
    for week in monthList:
        row = HTML.Row()
        for day in week:
            if day > 0:
                dayLink = HTML.Anchor \
                          ("%s/ViewCalendar.py?year=%d&month=%d&day=%d"
                           % (cgiURL, year, month, day), `day`)
                if IsToday(year, month, day):
                    cell = HTML.HeaderCell(dayLink, class_="today")
                elif day == week[0]:
                    cell = HTML.HeaderCell(dayLink, class_="sunday")
                else:
                    cell = HTML.HeaderCell(dayLink, class_="weekday")
            else:
                cell = HTML.Cell("&nbsp;", class_="empty")
            row.Add(cell)
        table.Add(row)
    output.Add(table)
    return output

def SideMonthsCell(year=None, month=None):
    """Display sidebar containing current and neighboring months."""
    cell = HTML.Cell()
    if not year and not month:
        year, month = Today()[0:2]
    y, m = PreviousMonth(year, month)
    cell.Add(ReducedMonth(y, m))
    cell.Add(HTML.HorizontalRule())
    cell.Add(ReducedMonth(year, month))
    cell.Add(HTML.HorizontalRule())
    y, m = NextMonth(year, month)
    cell.Add(ReducedMonth(y, m))
    return cell

def BottomMonthsTable(year=None, month=None):
    """Display sidebar containing current and neighboring months."""
    if not year and not month:
        year, month = Today()[0:2]
    table = HTML.Table([200,200,200], cellspacing="0", align="center")
    row = HTML.Row()
    row.Add(HTML.Cell(ReducedMonth(year, month)))
    y, m = NextMonth(year, month)
    row.Add(HTML.Cell(ReducedMonth(y, m)))
    y, m = NextMonth(y, m)
    row.Add(HTML.Cell(ReducedMonth(y, m)))
    table.Add(row)
    return table

def NavigationBar(year, month=None, day=None, ID=None):
    """Return navigation arrows."""
    table = HTML.Table(cols=[32,32,32], class_="title", align="center")
    row = HTML.Row()
    row.Add(HTML.Cell(PreviousLink(year, month, day, ID)))
    row.Add(HTML.Cell(ThisLink(year, month, day, ID)))
    row.Add(HTML.Cell(NextLink(year, month, day, ID)))
    table.Add(row)
    return table

def CalendarTitle(year, month=None, day=None):
    """Return a title containing the current period."""
    if day:
        title = "%s, %s %d, %d" \
                % (calendar.day_name[calendar.weekday(year,month,day)],
                  calendar.month_name[month], day, year)
    elif month:
        title = "%s, %d" % (calendar.month_name[month], year)
    else:
        title = "%d" % year
    return title
    
def CalendarOptions(year=None, month=None, day=None):
    """Add links to administrative options."""
    user = CGImodule.CGIgetUser()
    if user == "admin" or user in GetModule.GetSupervisors():
        supervisor = True
    else:
        supervisor = False
    row = HTML.Row()
    row.Add(HTML.HeaderCell(HTML.Anchor(homeURL, "Home", target="_top")))
    y, m, d = Today()
    link = "%s/ViewCalendar.py?year=%d&month=%d&day=%d" % (cgiURL, y, m, d)
    row.Add(HTML.HeaderCell(HTML.Anchor(link, "Today")))
    link = "%s/DefineList.py" % cgiURL
    row.Add(HTML.HeaderCell(HTML.Anchor(link, "List View")))
    if user:
        qualifier = ""
        if year:
            qualifier += "?year=%d" % year
            if month:
                qualifier += "&month=%d" % month
                if day:
                    qualifier += "&day=%d" % day
        link = "%s/AddEvent.py%s" % (cgiURL, qualifier)
        row.Add(HTML.HeaderCell(HTML.Anchor(link, "Add Event")))
        if user == "admin":
            link = "%s/ViewAdmin.py" % cgiURL
            row.Add(HTML.HeaderCell(HTML.Anchor(link, "Admin Page")))
        else:
            link = "%s/EditEditor.py?editor=%s" % (cgiURL, urllib.quote(user))
            row.Add(HTML.HeaderCell(HTML.Anchor(link, "Admin Page")))
        link = "%s/help.html" % webURL
        row.Add(HTML.HeaderCell(HTML.Anchor(link, "Help")))
        link = "%s/Logout.py%s" % (cgiURL, qualifier)
        row.Add(HTML.HeaderCell(HTML.Anchor(link, "Logout")))
    else:
        link = "%s/login.html" % webURL
        row.Add(HTML.HeaderCell(HTML.Anchor(link, "Login")))
    table = HTML.Table(cellspacing="0", cellpadding="5", align="center")
    table.Add(row)
    return table

def PreviousLink(year, month=None, day=None, ID=None, small=False, smaller=False):
    """Return an HTML anchor containing a pointer to the previous period."""
    if ID:
        previousID = PreviousEvent(ID)
        if previousID:
            link = "%s/ViewEvent.py?ID=%s" % (cgiURL, previousID)
        else:
            link = None
        title = "Previous Event"
    elif day:
        y, m, d = PreviousDay(year, month, day)
        link = "%s/ViewCalendar.py?year=%d&month=%d&day=%d" % (cgiURL, y, m, d)
        title = FormatDay(y, m, d)
    elif month:
        y, m = PreviousMonth(year, month)
        if small:
            link = "%s/CurrentMonth.py?year=%d&month=%d" % (cgiURL, y, m)
        elif smaller:
            link = "%s/CurrentMonthSmall.py?year=%d&month=%d" % (cgiURL, y, m)
        else:
            link = "%s/ViewCalendar.py?year=%d&month=%d" % (cgiURL, y, m)
        title = "%s, %d" % (monthList[m-1], y)
    else:
        link = "%s/ViewCalendar.py?year=%d" % (cgiURL, year-1)
        title = "%d" % (year-1)
    if link:
        if small or smaller:
            return HTML.Anchor(link,
                               HTML.Image(os.path.join(imgURL, "left.gif"),
                                          height=16, width=16),
                               target="_self", title=title)
        else:
            return HTML.Anchor(link,
                               HTML.Image(os.path.join(imgURL, "left.gif")),
                               title=title)
    else:
        return "&nbsp;"

def ThisLink(year, month=None, day=None, ID=None):
    """Return an HTML anchor to the current period."""
    target = "_self"
    if ID:
        link = "%s/ViewCalendar.py?year=%d&month=%d&day=%d" \
               % (cgiURL, year, month, day)
        title = FormatDay(year, month, day)
    elif day:
        link = "%s/ViewCalendar.py?year=%d&month=%d"  % (cgiURL, year, month)
        title = "%s, %d" % (monthList[month-1], year)
    elif month:
        link = "%s/ViewCalendar.py?year=%d" % (cgiURL, year)
        title = "%d" % year
    else:
        link = homeURL
        title = "Home Page"
        target = "_top"
    return HTML.Anchor(link,
                       HTML.Image(os.path.join(imgURL, "up.gif")),
                       title=title, target=target)
                                          
def NextLink(year, month=None, day=None, ID=None, small=False, smaller=False):
    """Return an HTML anchor containing a pointer to the next period."""
    if ID:
        nextID = NextEvent(ID)
        if nextID:
            link = "%s/ViewEvent.py?ID=%s" % (cgiURL, nextID)
            title = "Next Event"
        else:
            link = None
    elif day:
        y, m, d = NextDay(year, month, day)
        link = "%s/ViewCalendar.py?year=%d&month=%d&day=%d" % (cgiURL, y, m, d)
        title = FormatDay(y, m, d)
    elif month:
        y, m = NextMonth(year, month)
        if small:
            link = "%s/CurrentMonth.py?year=%d&month=%d" % (cgiURL, y, m)
        elif smaller:
            link = "%s/CurrentMonthSmall.py?year=%d&month=%d" % (cgiURL, y, m)
        else:
            link = "%s/ViewCalendar.py?year=%d&month=%d" % (cgiURL, y, m)
        title = "%s, %d" % (monthList[m-1], y)
    else:
        link = "%s/ViewCalendar.py?year=%d" % (cgiURL, year+1)
        title = "%d" % (year+1)
    if link:
        if small or smaller:
            return HTML.Anchor(link,
                               HTML.Image(os.path.join(imgURL, "right.gif"),
                                          height=16, width=16),
                               target="_self", title=title)
        else:
            return HTML.Anchor(link,
                               HTML.Image(os.path.join(imgURL, "right.gif")),
                               title=title)
    else:
        return "&nbsp;"

def MonthLink(year, month):
    """Return a month title with a link to the month view."""
    link = "%s/ViewCalendar.py?year=%d&month=%d" % (cgiURL, year, month)
    title = "%s, %d" % (calendar.month_name[month], year)
    return HTML.Anchor(link, title)

def NextEvent(ID):
    """Return the following event of the day."""
    y, m, d = IDdate(ID)
    IDs = GetModule.GetEventIDs(y, m, d)
    if ID not in IDs:
        PageModule.Page(y, m, d).PutEvents()
        IDs = GetModule.GetEventIDs(y, m, d)
    index = IDs.index(ID)
    if index == len(IDs) - 1:
        return None
    else:
        return IDs[index+1]

def PreviousEvent(ID):
    """Return the preceding event of the day."""
    y, m, d = IDdate(ID)
    IDs = GetModule.GetEventIDs(y, m, d)
    if ID not in IDs:
        PageModule.Page(y, m, d).PutEvents()
        IDs = GetModule.GetEventIDs(y, m, d)
    index = IDs.index(ID)
    if index == 0:
        return None
    else:
        return IDs[index-1]

