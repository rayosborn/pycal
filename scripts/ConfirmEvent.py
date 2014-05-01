#!/usr/bin/env python

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
# $Id: ConfirmEvent.py,v 1.3 2006/12/27 21:44:30 rosborn Exp $
#
"""
CGI script to confirm a calendar event.
"""

from pycal.PyCal import *
from pycal.Event import Event, TemporaryEvent
from pycal.GetModule import GetEditors, GetNextEvent
from pycal.PrintModule import LoginPage, ErrorPage, DayView
from pycal.CGImodule import CGIlogin, CGIgetForm, CGIflush
from pycal.Utilities import DatePath, Today, Now, CopyTime, IsValidID, StripID, IDdate
from pycal.PageModule import Page
import os

def main():

    try:
        form = CGIgetForm()
        user = CGIlogin(form)
        if user:
            if form.has_key("ID"):
                temporary_event = TemporaryEvent(form["ID"])
                if form.has_key("cancel"):
                    if temporary_event.start:
                        y, m, d = temporary_event.start[0:3]
                    else:
                        y, m, d = Today()
                    print DayView(y, m, d)
                    if temporary_event.ID.find("tmp") >= 0:
                        temporary_event.Remove()
                elif form.has_key("edit"):
                    print temporary_event.EditPage()
                else:
                    if hasattr(temporary_event, "oldID"):
                        old = True
                        oldID = temporary_event.oldID
                    else:
                        old = False
                    primary_event = None
                    if form.has_key("repeats"):
                        IDs = []
                        for repeat in form["repeats"]:
                            if IsValidID(repeat):
                                ID = repeat
                            else:
                                ID = os.path.join(repeat, "%03d"
                                                  % GetNextEvent(repeat))
                            IDs.append(ID)
                        #Remove new set of repeats from other excluded repeats
                        if old:
                            old_repeats = Event(oldID).repeats
                            if old_repeats:
                                discards = filter(lambda ID:ID not in IDs,
                                                  old_repeats)
                                for ID in discards:
                                    old_event = Event(ID)
                                    old_event.repeats = discards
                                    old_event.AddLog(
                                    "Removed from repeat list of %s" % oldID,
                                    save=False)
                                    old_event.Store()
                        #Now update the new set of repeats
                        if old:
                            primaryID = oldID
                            logMessage = "Repeated events updated"
                        else:
                            primaryID = IDs[0]
                            logMessage = "Repeated events created"
                        for ID in IDs:
                            new_event = Event(ID)
                            new_event.Copy(temporary_event)
                            new_event.start = CopyTime(ID, new_event.start)
                            new_event.end = CopyTime(ID, new_event.end, 
                                                     end=True)
                            new_event.reservation["start"] = \
                                CopyTime(ID, new_event.reservation["start"])
                            new_event.reservation["end"] = \
                                CopyTime(ID, new_event.reservation["end"], 
                                         end=True)
                            new_event.repeats = IDs
                            if ID == primaryID:
                                new_event.AddLog(logMessage)
                            new_event.Store()
                        primary_event = Event(primaryID)
                    elif old:
                        primary_event = Event(oldID)
                        if hasattr(temporary_event, "pattern"):
                            primary_event.ClearRepeats()
                        if temporary_event.start[0:3] == \
                           primary_event.start[0:3]:
                            primary_event.Copy(temporary_event)
                            primary_event.repeats = []
                            primary_event.AddLog("Event updated")
                            primary_event.Store()
                        else:
                            primary_event.Remove()
                            primary_event.UpdatePages()
                            primary_event = None
                    if not primary_event:
                        year, month, day = temporary_event.start[0:3]
                        eventDir = DatePath(year, month, day)
                        ID = os.path.join(eventDir, "%03d" 
                                                    % GetNextEvent(eventDir))
                        primary_event = Event(ID)
                        primary_event.Copy(temporary_event)
                        primary_event.created = Now()
                        if old:
                            primary_event.AddLog("Event date changed")
                        else:
                            primary_event.AddLog("Event created")
                        primary_event.Store()
                    temporary_event.Remove()
                    primary_event.UpdatePages()
                    print primary_event.EventView()
                    CGIflush()
            else:
                raise CalendarError, "No event specified"
        else:
            print LoginPage(script="ConfirmEvent.py", form=form)
    except CalendarError, errorText:
        print ErrorPage(errorText)

if __name__ == "__main__":
    main()



