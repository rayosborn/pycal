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
# $Id: PasswordModule.py,v 1.1.1.1 2004/03/10 15:09:20 osborn Exp $
#

"""PyCal module containing administrator password modules.

This module will set, get, and/or check the main administrator password 
that is stored in homeDir/admin.pw.  It is derived from similar modules
in the Mailman distribution.
"""

from PyCal import *
import Editor
import GetModule
import binascii
import Cookie
import hashlib
import marshal
import os
import string
import time

def SetAdminPassword(password):
    """Set the administrator password."""
    filename = os.path.join(homeDir,"admin.pw")
    omask = os.umask(022)                         # rw-r-----
    try:
        fp = open(filename, 'w')
        fp.write(hashlib.new('sha1',password).hexdigest() + '\n')
        fp.close()
    finally:
        os.umask(omask)
    
def GetAdminPassword():
    """Get the administrator password."""   
    filename = os.path.join(homeDir,"admin.pw")
    try:
        fp = open(filename)
        challenge = fp.read()[:-1]                # strip off trailing nl
        fp.close()
    except IOError, e:
        return None
    return challenge

def CheckAdminPassword(response):
    """Check the administrator password."""
    challenge = GetAdminPassword()
    if challenge is None:
        return None
    return challenge == hashlib.new('sha1',response).hexdigest()

def MakeCookie(user, password, expires=31536000):
    """Construct a cookie from the username, password, and a timestamp."""
    # Get a digest of the secret, plus other informationpassword.
    mac = hashlib.new('sha1',password).hexdigest()
    # Create the cookie object.
    C = Cookie.SimpleCookie()
    C["user"] = binascii.hexlify(marshal.dumps((user, mac)))
#   C["user"]["path"] = cgiURL
    # Set the RFC 2109 required header.
    C["user"]["version"] = 1
    # Expire cookie by the specified time (one year by default)
    C["user"]["expires"] = expires 
    C["user"]["max-age"] = expires 
    return C

def GetCookie():
    """Check that a cookie is valid."""
    C = Cookie.SimpleCookie()
    try:
        C.load(os.environ["HTTP_COOKIE"])
    except KeyError:
        return None
    if not C.has_key("user"):
        return None
    try:
        data = marshal.loads(binascii.unhexlify(C["user"].value))
        user, mac = data
    except (EOFError, ValueError, TypeError, KeyError):
        return None
    # Calculate what the mac ought to be based on the cookie's timestamp
    # and the password.
    password = GetPassword(user)
    if password <> mac:
        return None
    # Authenticated!
    return user

def DeleteCookie():
    """Delete a user cookie by setting the expiry date to now."""
    # Create the cookie object.
    C = Cookie.SimpleCookie()
    C["user"] = "logout"
#   C["user"]["path"] = cgiURL
    # Set the RFC 2109 required header.
    C["user"]["version"] = 1
    # Expire cookie in about six months
    C["user"]["expires"] = 0 
    return C

def SetPassword():
    """Return a random password."""
    chars = string.lowercase[0:25]+string.uppercase[0:25]+string.digits   
    t = time.localtime(time.time())
    password = ""
    for x in t[1:7]: 
        password = password + chars[x]
    return password

def GetPassword(user):
    """Get a user's password."""
    if user == "admin":
        return GetAdminPassword()
    if user in GetModule.GetEditors():
        m = Editor.Editor(user)
        return hashlib.new('sha1',m.password).hexdigest()
    return None

def CheckPassword(user, password):
    """Check a user's password."""
    if user == "admin":
        return CheckAdminPassword(password)
    if user in GetModule.GetEditors():
        m = Editor.Editor(user)
        return password == m.password
    return 0


