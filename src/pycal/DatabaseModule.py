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
# $Id: DatabaseModule.py,v 1.2 2004/08/05 11:34:29 osborn Exp $
#
"""PyCal - Python web calendar. 

Functions performing common file operations on databases.

"""

import os
import shelve
import time

from PyCal import *

def Read(key, name, dir=homeDir, object=None):
    """Read the database into the supplied object."""
    if not os.path.exists(os.path.join(dir, "%s.db" % name)):
        return
    t = 0
    while t < 30:
        if IsLocked(name, dir):
            time.sleep(1)
            t = t + 1
        else:
            try:
                db = shelve.open(os.path.join(dir, "%s.db" % name))
                try:
                    value = None
                    if db.has_key(key):
                        if object:
                            for item in db[key].__dict__.keys():
                                object.__dict__[item] = db[key].__dict__[item]
                        else:
                            value = db[key]
                except KeyError:
                    raise CalendarError, "%s database read error" \
                                         % name.capitalize()
            finally:
                db.close()
            return value
    raise CalendarError, "%s database locked" % name.capitalize()
        
def Store(value, key, name, dir=homeDir):
    """Store the current object for later use."""
    omask = os.umask(0)
    if not os.path.exists(dir):
        os.makedirs(dir)
    Lock(name, dir)
    try:
        db = shelve.open(os.path.join(dir, "%s.db" % name))
        db[key] = value
    finally:
        db.close()
        Unlock(name, dir)
        os.umask(omask)

def Delete(key, name, dir=homeDir):
    """Removes a key from the database."""
    Lock(name, dir)
    try:
        db = shelve.open(os.path.join(dir, "%s.db" % name))
        if db.has_key(key):
            del db[key]
        db.close()
    finally:
        Unlock(name, dir)

def Keys(name, dir=homeDir):
    """Return a list of database keys."""
    t = 0
    while t < 30:
        if IsLocked(name, dir):
            time.sleep(1)
            t = t + 1
        else:
            try:
                db = shelve.open(os.path.join(dir, "%s.db" % name))
                keys = db.keys()
            finally:
                db.close()
            return keys
    raise CalendarError, "%s database locked" % name.capitalize()

def Values(name, dir=homeDir):
    """Return a list of database values."""
    t = 0
    while t < 30:
        if IsLocked(name, dir):
            time.sleep(1)
            t = t + 1
        else:
            try:
                db = shelve.open(os.path.join(dir, "%s.db" % name))
                keys = db.keys()
                values = []
                for key in keys:
                    values.append(db[key])
            finally:
                db.close()
            return values
    raise CalendarError, "%s database locked" % name.capitalize()

def Remove(name, dir=homeDir):
    """Delete the database file."""
    omask = os.umask(0)
    if os.path.exists(os.path.join(dir, "%s.db" % name)):
        Lock(name, dir)
        try:
            os.remove(os.path.join(dir, "%s.db" % name))
        finally:
            Unlock(name, dir)
            os.umask(omask)

def Lock(name, dir=homeDir):
    """Lock the database to prevent simultaneous writes.
    
    This uses an extremely simple file locking mechanism based on a tutorial
    by Guido van Rossum, but with the extra feature that stale locks will be
    automatically cleared, based on a predefined wait time.  The databases
    will only be locked during write operations.  Simultaneous reads are
    permitted.

    The databases are all fairly small, and the lock only needs to persist
    for the duration of any write operation, so these locks should not be
    very intrusive.

    Method
    ------
    1) A database "dir/name.db" will be locked by the creation of a directory
       called "dir/name.lock", using the function Lock(name, dir).  If the
       database is already locked, the function will attempt to create a new
       lock each second for 30 seconds before generating an error. (The
       default directory is homeDir defined in config.py).
    2) The lock is cleared by calling Unlock(name, dir), which removes the 
       lock directory.
    3) The existence of the lock is checked by calling IsLocked(name, dir), 
       which will automatically unlock the file if the lock was created more
       than lockWait seconds before.  This wait time is also set in
       config.py.
    """
    omask = os.umask(0)
    lockFile = os.path.join(dir, "%s.lock" % name)
    t = 0
    while t < 30:
        if IsLocked(name, dir):
            time.sleep(1)
            t = t + 1
        else:
            try:
                os.mkdir(lockFile)
                os.umask(omask)
                return
            except OSError:
                raise CalendarError, "%s database locked" % name.capitalize()
    os.umask(omask)
    raise CalendarError, "%s database locked" % name.capitalize()

def Unlock(name, dir=homeDir):
    """Unlock the database."""
    try:
        os.rmdir(os.path.join(dir, "%s.lock" % name))
    except OSError:
        pass

def IsLocked(name, dir=homeDir):
    """Return true if the database is locked.
        
    This routine will clear a stale lock, i.e. older than lockWait.
    """
    lockFile = os.path.join(dir, "%s.lock" % name)
    if os.path.exists(lockFile):
        if (time.time()-os.stat(lockFile).st_mtime) > lockWait:
            Unlock(name, dir)
            return False
        else:
            return True
    return False
        
