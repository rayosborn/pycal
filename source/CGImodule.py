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
# $Id: CGImodule.py,v 1.3 2004/07/30 16:45:09 osborn Exp $
#
"""PyCal module containing CGI modules.

This module provides a few operations required by many of the CGI script to
print and flush headers, and extract form dictionaries and user information.
"""

import cgi
import cgitb
import os
import sys

from PyCal import *
import GetModule
import PasswordModule
from Utilities import IsEmail

user = None

def CGIprintHeader():
    """Print HTTP header, flushing the output immediately.
    
    Some scripts take a while to process.  Since Python buffers output to 
    stdout, some browsers will time-out waiting for some response from the
    server.  Flushing the HTTP header should give us some breathing space.
    """
    cgitb.enable()
    print "Content-type: text/html; charset=UTF-8"
    print
    sys.stdout.flush()    

def CGIflush():
    """Flush existing CGI output immediately"""
    sys.stdout.flush()

def CGIgetForm():
    """Input CGI form fields, only passing back filled fields.
    
    In principle, the Python cgi library only instantiates form fields
    that contain data.  However, when I tested this, empty fields were
    nevertheless created.  Instead, I am transferring the fields into a
    conventional dictionary, since the FieldStorage class doesn't have a
    delete method. Then, the dictionary 'has_key' method will reliably
    detect filled fields.
    
    We lose the .file attribute, but since we are in control of all the
    file upload field names, and read entire files into text variables
    anyway, this is not a serious drawback.
    """
    form = cgi.FieldStorage()
    dict = {}
    for key in form.keys():
        if isinstance(form[key],list):
            dict[key] = []
            for item in form[key]:
               dict[key].append(item.value)
        elif form[key].value:
            dict[key] = form[key].value
    return dict
        
def CGIlogin(form, printHeader=True):
    """Return the user entered on the CGI form.
    
    This returns the user specified on the form.  If the form does not
    specify a user, the browser's cookies are checked.
    
    This will raise an CalendarError if 
       1) there is no user specified in the CGI form
       2) the user name is invalid 
          i.e., "admin" or a user in the Editor database
       3) the password is invalid
    """
 
    # Check to see if the user and/or password have been specified.
    global user
    try:
        user = form["user"].lower()
        password = form["password"].strip()
        if PasswordModule.CheckPassword(user, password):
            print PasswordModule.MakeCookie(user, password)
        else:
            CGIprintHeader()
            raise CalendarError, "Invalid user and/or password"
            return None
    except KeyError:
        user = PasswordModule.GetCookie()
    if printHeader:
        CGIprintHeader()
    return user

def CGIgetUser():
    """Return the user returned by CGIlogin.""" 
    global user
    return user

def SendEmail(mailto, subject, message, mailfrom=SMTPemail, cc=[], bcc=[], 
              footer=None):
    """Send email message within a CGI script."""
    
    import smtplib
    import StringIO

    if isinstance(mailto, str):
        mailto = [mailto]
    if isinstance(cc, str):
        cc = [cc]
    if isinstance(bcc, str):
        bcc = [bcc]
    for email in mailto:
        if not IsEmail(email):
            raise CalendarError, "Invalid email address for message"
    out = StringIO.StringIO()
    out.write("Subject: %s\n" % subject)
    if SMTPemail != calendarEmail: #Assume the SMTP server is fussy
        out.write("From: %s\n" % SMTPemail)
        out.write("Reply-To: %s\n" % mailfrom)
    else:
        out.write("From: %s\n" % mailfrom)
    out.write("To: %s\n" % ", ".join(mailto))
#    if mailfrom not in mailto+cc+bcc:
#        cc.append(mailfrom)
    if cc:
        out.write("Cc: %s\n" % ", ".join(cc))
        mailto.extend(cc)
    if bcc:
        out.write("Bcc: %s\n" % ", ".join(bcc))
        mailto.extend(bcc)
    out.write("\n"+message+"\n")
    if footer:
        out.write(footer)
    out.write("-- \n")
    if calendarSignature:
        out.write(calendarSignature.strip()+"\n")
    mail = smtplib.SMTP(SMTPserver)
    mail.sendmail(mailfrom, mailto, out.getvalue())
    mail.quit()

