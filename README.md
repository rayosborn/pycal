Introduction
============
PyCal provides an online calendar that can be used to schedule meetings and
events. It allows for rooms and other resources to be booked, with warnings
shown when there are scheduling conflicts.

Installing and Running
======================
The latest version of PyCal can be downloaded from the PyCal [Git 
repository](https://github.com/rayosborn/pycal).

```
    $ git clone http://github.com/rayosborn/pycal.git
```

The cgi-bin directory must be defined when installing:

```
    $ cd pycal
    $ python setup.py install --install-scripts=/path/to/cgi-bin/dir
```
