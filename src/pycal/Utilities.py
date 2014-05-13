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
# $Id: Utilities.py,v 1.6 2006/12/29 21:39:20 rosborn Exp $
#
"""PyCal: Python web calendar 

Miscellaneous utilities.
"""

from PyCal import *
import os
import re
import time
import calendar

def FormatTime(t, format=None):
    """Return the time as a formatted string."""
    if not isinstance(t, time.struct_time):
        return str(t)
    if format == "ISO8601":
        return time.strftime("%Y-%m-%d %H:%M:%S %Z", t)
    else:
        return re.sub('^0', '', time.strftime("%I:%M%p", t).lower())

def FormatDate(t, day=False):
    """Return the date as a formatted string."""
    if not isinstance(t, time.struct_time):
        return str(t)
    if day:
        return re.sub(' 0', ' ', time.strftime("%A, %B %d, %Y", t))
    else:
        return re.sub(' 0', ' ', time.strftime("%B %d, %Y", t))

def FormatDay(year, month, day):
    """Return the day and date as a formatted string."""
    t = time.strptime("%s %s %s" % (`year`, `month`, `day`), "%Y %m %d")
    return re.sub(' 0', ' ', time.strftime("%A, %B %d, %Y", t))

def ReadDate(year, month, day):
    """Return time structure from date string."""
    date = "%s %s %s" % (year, month, day)
    return time.strptime(date, "%Y %B %d")

def ReadTime(year, month, day, hour, minute, meridiem, end=False):
    """Return time structure from date string."""
    date = "%s %s %s %s %s %s" % (year, month, day, hour, minute, meridiem)
    t = time.strptime(date, "%Y %B %d %I %M %p")
    if end and t.tm_hour == 0 and t.tm_min == 0:
        t = AddDay(t)
    return t

def DatePath(year=None, month=None, day=None):
    """Return the date as a directory path."""
    if day:
        return os.path.join(`year`, "%02d" % month, "%02d" % day)
    elif month:
        return os.path.join(`year`, "%02d" % month)
    elif year:
        return `year`
    else:
        return ""
    
def PathDate(path):
    """Return the date from a directory path."""   
    return time.strptime(path, "%Y/%m/%d")[0:3]

def CopyTime(path, date, end=False):
    """Return time structure with new date overlaying time."""    
    t = time.strptime("%s %s" % (StripID(path), time.strftime("%H:%M", date)), 
                      "%Y/%m/%d %H:%M")
    if end and t.tm_hour == 0 and t.tm_min == 0:
        t = AddDay(t)
    return t
    
def NextMonth(year, month):
    """Return the year and month of the following month."""
    month = month + 1
    if month == 13:
        month = 1
        year = year + 1
    return (year, month)
    
def PreviousMonth(year, month):
    """Return the year and month of the preceding month."""
    month = month - 1
    if month == 0:
        month = 12
        year = year - 1
    return (year, month)

def WeekList(year, month, day, length=7):
    """Return weeks starting with the one containing a particular day."""
    start = calendar.weekday(year, month, day)
    if start <> 6:
        day = day - start - 1
        if day < 1:
            year, month = PreviousMonth(year, month)
            day = calendar.monthrange(year, month)[1] + day
    week = []
    length = (divmod(length-1,7)[0] + 1) * 7
    for i in range(length):
        week.append((year, month, day))
        year, month, day = NextDay(year, month, day)
    return week

def NextWeek(year, month, day):
    """Return the year, month, and day of the following week."""
    day = day + 7
    if day > calendar.monthrange(year, month)[1]:
        day = day - calendar.monthrange(year, month)[1]
        year, month = NextMonth(year, month)
    return (year, month, day)
    
def PreviousWeek(year, month, day):
    """Return the year, month, and day of the preceding week."""
    day = day - 7
    if day < 1:
        year, month = PreviousMonth(year, month)
        day = calendar.monthrange(year, month)[1] + day
    return (year, month, day)
    
def NextDay(year, month, day):
    """Return the year, month, and day of the following day."""
    day = day + 1
    if day > calendar.monthrange(year, month)[1]:
        year, month = NextMonth(year, month)
        day = 1
    return (year, month, day)

def PreviousDay(year, month, day):
    """Return the year, month, and day of the preceding day."""
    day = day - 1
    if day == 0:
        year, month = PreviousMonth(year, month)
        day = calendar.monthrange(year, month)[1]
    return (year, month, day)

def MonthDays(year, month):
    """Return a list of days for a particular month."""
    return range(1, calendar.monthrange(year, month)[1]+1)

def Today():
    """Return today's date"""
    return time.localtime()[0:3]
    
def IsToday(year, month, day):
    """Return true if the specified day is today."""
    return (year, month, day) == time.localtime()[0:3]

def Now():
    """Return current time as a time structure."""
    return time.localtime()

def AddDay(t):
    """Add 24 hours to the specified time."""
    timelist = list(t)
    timelist[8] = -1
    return time.localtime(time.mktime(time.struct_time(timelist)) + 60*60*24)

def DayLength(start, end):
    """Return number of days between two dates (inclusive)."""
    return int(round((time.mktime(end) - time.mktime(start))/(60*60*24))) + 1

def MakeRepeats(pattern, start, end, number=None):
    """Return a list of repeat events from a given pattern."""
    calendar.setfirstweekday(calendar.SUNDAY)
    y, m, d = start[0:3]
    end = end[0:3]
    repeats = []
    if pattern == "Daily":
        if number:
            for i in range(number):
                repeats.append(DatePath(y, m, d))
                y, m, d = NextDay(y, m, d)
        else:
            date = DatePath(y, m, d)
            while date <= end:
                repeats.append(DatePath(y, m, d))
                y, m, d = NextDay(y, m, d)
                date = (y, m, d)                
    elif pattern == "Weekly":
        if number:
            for i in range(number):
                repeats.append(DatePath(y, m, d))
                y, m, d = NextWeek(y, m, d)
        else:
            date = DatePath(y, m, d)
            while date <= end:
                repeats.append(DatePath(y, m, d))
                y, m, d = NextWeek(y, m, d)
                date = (y, m, d)                
    elif pattern == "Monthly": 
        if number:
            for i in range(number):
                repeats.append(DatePath(y, m, d))
                y, m = NextMonth(y, m)
        else:
            date = DatePath(y, m, d)
            while date <= end:
                repeats.append(DatePath(y, m, d))
                y, m = NextMonth(y, m)
                date = (y, m, d)                
    elif pattern == "Annually":
        if number:
            for i in range(number):
                repeats.append(DatePath(y, m, d))
                y = y + 1
        else:
            date = DatePath(y, m, d)
            while date <= end:
                repeats.append(DatePath(y, m, d))
                y = y + 1
                date = (y, m, d)                
    elif pattern == "Same Day Monthly":
        week = ((d - 1) / 7) + 1
        if number:
            for i in range(number):
                repeats.append(DatePath(y, m, d))
                newWeek = week + 1
                while newWeek <> week:
                    y, m, d = NextWeek(y, m, d)
                    newWeek = ((d - 1) / 7) + 1
        else:
            date = DatePath(y, m, d)
            while date <= end:
                repeats.append(DatePath(y, m, d))
                newWeek = week + 1
                while newWeek <> week:
                    y, m, d = NextWeek(y, m, d)
                    newWeek = ((d - 1) / 7) + 1
                date = (y, m, d)
    return repeats

def IsValidID(ID):
    """Returns true if the ID is valid for an event, i.e. not just a path."""
    if re.search("/\d\d\d$", ID):
        return 1
    else:
        return 0
    
def IDexists(ID):
    """Returns true if an event database exists for this ID."""
    if re.search("/\d\d\d$", ID):
        if os.path.exists(os.path.join(homeDir, ID, "events.db")):
            return 1
        else:
            return 0
    else:
        return 0
    
def StripID(ID):
    """Remove event ID so that it only contains the date."""        
    return re.sub("/\d\d\d$", "", ID)
        
def StripIDs(IDs):
    """Remove event ID from a list returning only the dates."""
    list = []
    for ID in IDs:
        list.append(StripID(ID))
    return list

def IDdate(ID):
    """Return the year, month, and day from an ID."""
    return tuple(map(int, StripID(ID).split("/")))

def PathExists(path):
    """Returns true if the directory path exists."""
    if os.path.exists(os.path.join(homeDir, str(path))):
        return 1
    else:
        return 0
    
def ConvertMessage(event, message):
    """Replace placeholders in email text with abstract values."""
    from GetModule import GetEditor, GetEvent
    title = event.title
    if len(title) > 50:
        title = title[:50]+"..."
    message = message.replace("[[[title]]]", title)
    message = message.replace("[[[editor]]]", event.editor)
    message = message.replace("[[[email]]]", GetEditor(event.editor).email)
    message = message.replace("[[[time]]]", FormatTime(event.schedule))
    return message

def ConvertCRLFs(inputText):
    """Convert all CR and CR/LF line terminations to HTML line breaks."""
    import HTML
    outputText = inputText.replace("\r\n", "\n")
    outputText = outputText.replace("\r", "\n")
    return outputText.replace("\n", "<br />")

def ConvertBreaks(inputText):
    """Convert all HTML line breaks to line feeds."""
    outputText = inputText.replace("\n", "")
    return outputText.replace("<br />", "\n")

def IsValid(data, maxlength=30, allowed=r"^\w+$", prohibited=None):
    """Check whether the supplied text is a valid field entry.
    
     data is valid if <= maxlength,
     AND if an allowed RE is specified:  must match allowed.
     AND must not match prohibited RE
     Defaults: maxlength: 30, allowed: string of 1 or more \w word chars
     """
    if len(data) > maxlength:
        return 0 # not valid
    if allowed:
        matchAllowed = re.search(allowed, data)
        if not matchAllowed:
            return 0 # not valid
    if prohibited: # function can also be used to exclude prohibited RE
        matchProhibited = re.search(prohibited, data)
        if matchProhibited:
            return 0 # not valid
    return 1 # passed all tests so should be valid 

def IsEmail(address):
    """Check whether a supplied email address is valid or not.
    
      Allowed RE: any word characters , dot (.), hyphen (-) and at (@) .
      Prohibited RE: any dot or at in the wrong place,
      or no at or more than 1 at's or zero dot's.
      
    """
    return IsValid(address, maxlength = 100,
                   allowed=r"^[\w\.\-@]+$",
                   prohibited=r"^[\.@]|[\.@][\.@]|@.*@|[\.@]$|^[^.]+$|^[^@]+$") 

def StripHTML(text):
    """Strip HTML tags from a string and return plain text."""
    import re
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return "" # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            import htmlentitydefs
            entity = htmlentitydefs.entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return unichr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return unicode(entity, "iso-8859-1")
        return text # leave as is
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)

    
