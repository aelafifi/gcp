gcp v0.1.3
(c) Jérôme Poisson aka Goffi 2010, 2011

gcp (Goffi's cp) is a files copier.


** LICENSE **

gcp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gcp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gcp.  If not, see <http://www.gnu.org/licenses/>.



** WTF ? **
gcp is a file copier, loosely inspired from cp, but with high level functionalities like:
	- progression indicator
	- gcp continue copying even when there is an issue: he just skip the file with problem, and go on
	- journalization: gcp write what he is doing, this allow to know which files were effectively copied
	- fixing names to be compatible with the target filesystem (e.g. removing incompatible chars like "?" or "*" on vfat)
	- if you launch a copy when an other is already running, the files are added to the first queue, this avoid your hard drive to move its read/write head all the time
	- files saving: you can keep track of files you have copied, and re-copy them later (useful when, for example, you always copy some free music to all your friends).
	- gcp will be approximately option-compatible with cp (approximately because the behaviour is not exactly the same, see below)

/!\ WARNING /!\
gcp is at an early stage of development, and really experimental: use at your own risks !

** How to use it ? **
Pretty much like cp (see gcp --help). 
Please note that the behaviour is not exactly the same as cp, even if gcp want to be option-compatible. Mainly, the destination filenames can be changed (by default, can be deactivated).
gcp doesn't implement yet all the options from cp, but it's planed.

** journalizaion **
The journal is planed to be used by gcp itself, buts remains human-readable. It is located in ~/.gcp/journal

3 states are used:
- OK means the file is copied and all operation were successful
- PARTIAL means the file is copied, but something went wrong (e.g. changing the permissions of the file)
- FAILED: the file is *not* copied

after the state, a list of things which went wront are show, separated by ", "

** What's next ? **

Several improvment are already planed
- copy queue management (moving copy order)
- advanced console interface
- notification (xmpp and maybe mail) when a long copy is finished
- retry for files which were not correctly copied
- badly encoded unicode filenames fix
- file copy integrity check

... and other are with a "maybe"
- graphic interface
- desktop (Kde, Gnome, XFCE, ...) integration
- distant copy (ftp)
- basic server mode, for copying files on network without the need of nfs or other heavy stuff

** Credits **

A big big thank to the authors/contributors of...

	progressbar:
	gcp use ProgressBar (http://pypi.python.org/pypi/progressbar/2.2), a class coded by Nilton Volpato which allow the textual representation of progression.

	GLib:
	This heavily used library is used here for the main loop, event catching, and for DBus. Get it at http://library.gnome.org/devel/glib/

	DBus:
	This excellent IPC is in the heart of gcp. Get more information at www.freedesktop.org/wiki/Software/dbus

	python and its amazing standard library:
	gcp was coded quickly for my own need thanks to this excellent and efficient language and its really huge standard library. Python can be download at www.python.org

If I forgot any credit, please contact me (mail below) to fix it.

Big thanks to contributors and package mainteners

** Contributions **
2011: Thomas Preud'homme <robotux@celest.fr>: manpage, stat resolution fix



** Contact **

You can contact me at goffi@goffi.org .
You'll find the latest version on my ftp: ftp://ftp.goffi.org/gcp, or check the wiki ( http://wiki.goffi.org/wiki/Gcp )
Please report any bug on http://bugs.goffi.org
You can also have a look to my other main projects (and maybe to the smaller ones too ;) ):
- lm (list movie): a tool to list movies using IMdB data, loosely inspired from ls
- SàT: my main project, a jabber/XMPP client, which is a brick to many others things I have in mind

Don't hesitate to give feedback :)
