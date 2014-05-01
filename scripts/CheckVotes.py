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
# $Id: CheckUpdates.py,v 1.1 2004/08/07 13:10:07 osborn Exp $
#
"""
CGI script to check for page updates.
"""

import sys
sys.path.append("/home/dgfumc/www/cgi-bin/calendar")
from pycal.PyCal import CalendarError
import pycal.OptionModule as OptionModule

def main():

    try:
        forum = OptionModule.Read("forum")
        for topic in forum.keys():
            multiples = []
            for vote in forum[topic]:
                count = forum[topic].count(vote)
                if count > 2 and vote not in multiples:
                    multiples.append(vote)                    
                    print "%s voted for '%s' %s times" % (vote, topic, count)
    except CalendarError, errorText:
        print "%s/%s: %s" % (year, month, errorText)

if __name__ == "__main__":
    main()


