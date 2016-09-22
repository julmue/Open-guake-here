#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module adds a menu item to the nautilus right-click menu which allows to Open the Terminal
   on the Selected Folder/Current Directory at predefined Geometry just through the right-clicking"""

#   open-terminal-geometry.py version 3.0
#
#   Copyright 2009-2011 Giuseppe Penone <giuspen@gmail.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#   MA 02110-1301, USA.

from gi.repository import Nautilus, GObject, Gtk, GdkPixbuf
import urllib, os, subprocess
import locale, gettext

APP_NAME = "nautilus-pyextensions"
LOCALE_PATH = "/usr/share/locale/"
GEOMETRY = "100x25"
ICONPATH = "/usr/share/icons/gnome/48x48/apps/terminal.png"
# internationalization
locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP_NAME, LOCALE_PATH)
gettext.textdomain(APP_NAME)
_ = gettext.gettext
# post internationalization code starts here


class OpenTerminalGeometry(GObject.GObject, Nautilus.MenuProvider):
    """Implements the 'Open Guake here' extension to the nautilus right-click menu"""

    def __init__(self):
        """Nautilus crashes if a plugin doesn't implement the __init__ method"""
        try:
            factory = Gtk.IconFactory()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(ICONPATH)
            iconset = Gtk.IconSet.new_from_pixbuf(pixbuf)
            factory.add("terminal", iconset)
            factory.add_default()
        except: pass

    def run(self, menu, selected):
        """Runs the Open guake here on the given Directory"""
        uri_raw = selected.get_uri()
        if len(uri_raw) < 7: return
        cur_dir = urllib.unquote(uri_raw[7:]).decode('utf8')
        if os.path.isfile(cur_dir): cur_dir = os.path.dirname(cur_dir)

        subprocess.call([
            u'guake',
            u'--new-tab=%s' % cur_dir,
            u'--show',
            u'--rename-current-tab=%s' % os.path.basename(cur_dir)
        ])

    def get_file_items(self, window, sel_items):
        """Adds the 'Open guake here' menu item to the Nautilus right-click menu,
           connects its 'activate' signal to the 'run' method passing the selected Directory/File"""
        if len(sel_items) != 1 or sel_items[0].get_uri_scheme() != 'file': return
        item = Nautilus.MenuItem(name='NautilusPython::terminal',
                                 label=_('Open Guake Here'),
                                 tip=_('Open Guake on the Current/Selected Directory'),
                                 icon='terminal')
        item.connect('activate', self.run, sel_items[0])
        return [item]

    def get_background_items(self, window, current_directory):
        """Adds the 'Open guake here' menu item to the Nautilus right-click menu,
           connects its 'activate' signal to the 'run' method passing the current Directory"""
        item = Nautilus.MenuItem(name='NautilusPython::terminal',
                                 label=_('Open Guake Here'),
                                 tip=_('Open Guake on the Current Directory'),
                                 icon='terminal')
        item.connect('activate', self.run, current_directory)
        return [item]
