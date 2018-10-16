gcp
===

gcp is a user-friendly file copier written in Python. Its name used to stand
for "Goffi's CoPier", but was changed into a recursive acronym: Gcp CoPier.


License
=======

gcp is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

gcp is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a [copy of the GNU General Public License](LICENSE)
along with gcp. If not, see <http://www.gnu.org/licenses/>.


About
=====

gcp is a file copier, loosely inspired from cp, but with high level
functionalities such as:

- **Progress bar.**
- gcp **keeps copying** even when there is an issue: it just skips the file,
  logs an error and goes on.
- **Logging**: gcp writes what it's doing to a log file; this allows you to
  know which files were effectively copied.
- **Fixing file names** to be compatible with the target filesystem (e.g.
  removing incompatible chars like `?` or `*` on FAT).
- **Queue**: if you launch a copy when another copy is already running, the
  files are added to the first queue; this optimizes hard drive head movement
  and filesystem fragmentation.
- **Files saving**: you can keep track of the files you have copied, and copy
  them again later (useful when, for example, you copy some free music to your
  friends on a regular basis).
- gcp will be **approximately option-compatible with (GNU) cp** (approximately
  because the behaviour is not exactly the same, see below).

**WARNING**: gcp is at a relatively early stage of development, use at your own
risks!


Installing
==========

The Python way
--------------

First, install the following packages on your system (these Debian packages
names, they may be different on other distros/systems):
- libdbus-1-dev
- libdbus-glib-1-dev
- libgirepository1.0-dev
- libcairo2-dev
- python3-cairo-dev

Then install gcp with pip:
    pip3 install gcp

On Debian-based systems
-----------------------

    apt install gcp


How to use it?
==============

Pretty much like cp (see `gcp --help` and `man gcp`).

Please note that the behaviour is not exactly the same as cp's, even if gcp
aims to be option-compatible. Mainly, the destination filenames can be modified
(cf. the `--fix-filenames` option).

gcp doesn't implement all the options GNU cp has yet, but it's a long-term
goal.


Logging
=======

The log file is aimed to be used by gcp itself, buts remains human-readable. It
is located in `~/.gcp/journal`.

3 states are used:
- **OK** means the file was copied and all operation were successful.
- **PARTIAL** means the file was copied, but something went wrong (file
  permissions could not be preserved, file name had to be changed, etc.).
- **FAILED**: the file was *not* copied.

After the state, a list of things that went wrong is shown, separated by ", ".


Contribution ideas
==================

Here are some ideas for future developments:
- handle XDG
- copy queue management (moving copy order)
- advanced console interface
- notification (XMPP and maybe email) when a long copy is finished
- retry for files that were not correctly copied
- badly encoded unicode filenames fix
- file copy integrity check

And in an even more distant future:
- graphic interface
- desktop (Kde, Gnome, XFCE...) integration
- distant copy (FTP)
- basic server mode, for copying files on network without the need of NFS or
  other heavy stuff


Credits
=======

A big big thanks to the authors/contributors of...

* **progressbar**:
  gcp uses [ProgressBar](https://pypi.python.org/pypi/progressbar), a class
  coded by Nilton Volpato that allows the textual representation of
  progression.

* **GLib**:
  This heavily used library is used here for the main loop, event catching, and
  for DBus. Get it at <https://developer.gnome.org/glib/>.

* **DBus**:
  This excellent IPC is ut the heart of gcp. Get more information at
  <https://www.freedesktop.org/wiki/Software/dbus/>.

* **Python** and its amazing standard library:
  gcp was coded quickly for my own needs thanks to this excellent and efficient
  language and its really huge standard library. Python can be download at
  <https://www.python.org/>.

If I forgot any credit, please contact me (email below) to fix that.

Big thanks to contributors and package maintainers.


Contributors
============

* Original author: Jérôme Poisson a.k.a. Goffi <goffi@goffi.org> 2010-2011.
* Thomas Preud'homme <robotux@celest.fr> 2011: manpage, stat resolution fix.
* Jingbei Li a.k.a. petronny 2016: conversion to Python3.
* Matteo Cypriani <mcy@lm7.fr> 2018: `--fix-filenames` option, Python3 fixes.


Contact
=======

Feedback, bug reports, patches, etc. are welcome, either by email or on the
repository's issue tracker <https://code.lm7.fr/mcy/gcp/issues>.

You can also have a look at Goffi's other main project, [Salut à
Toi](https://www.salut-a-toi.org/) (SàT), a Jabber/XMPP-based multi-frontend,
multipurpose communication tool.

Don't hesitate to give feedback :)
