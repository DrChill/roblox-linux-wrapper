#!/usr/bin/env python3	

#  Copyright 2014 DrChill
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from gi.repository import Gtk

import fnmatch
import os
from subprocess import Popen

devnull = open(os.devnull, 'wb') # use this in python < 3.3
								 # python >= 3.3 has subprocess.DEVNULL

def recursiveFind(pathToSearch, filenameToFind):
	for root, dirnames, filenames in os.walk(pathToSearch):
		for filename in fnmatch.filter(filenames, filenameToFind):
			return os.path.join(root, filename)

def getGameId(dlgParent):
	dialogWindow = Gtk.MessageDialog(dlgParent,
						  Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
						  Gtk.MessageType.QUESTION,
						  Gtk.ButtonsType.OK_CANCEL,
						  "Please enter the URL of the game you would like to play")

	dialogWindow.set_title("Game Url")

	dialogBox = dialogWindow.get_content_area()
	userEntry = Gtk.Entry()
	dialogBox.pack_end(userEntry, False, False, 0)

	dialogWindow.show_all()
	response = dialogWindow.run()
	text = userEntry.get_text() 
	dialogWindow.destroy()
	return text

class RLWWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title='Roblox Linux Wrapper')
		self.set_border_width(10)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(vbox)

		play_btn = Gtk.Button(label='Play Roblox')
		legacy_play_btn = Gtk.Button(label='Play Roblox (Legacy Mode)')
		studio_btn = Gtk.Button(label='Roblox Studio')
		uninstall_rlw_btn = Gtk.Button(label='Uninstall Roblox Linux Wrapper')
		reset_roblox_defaults_btn = Gtk.Button(label='Reset Roblox to defaults')
		uninstall_roblox_btn = Gtk.Button(label='Uninstall Roblox')

		play_btn.connect('clicked', self.on_play_btn_clicked)
		legacy_play_btn.connect('clicked', self.on_legacy_play_btn_clicked)
		studio_btn.connect('clicked', self.on_studio_btn_clicked)
		uninstall_rlw_btn.connect('clicked', self.on_uninstall_rlw_btn_clicked)
		reset_roblox_defaults_btn.connect('clicked', self.on_reset_roblox_defaults_btn_clicked)
		uninstall_roblox_btn.connect('clicked', self.on_uninstall_roblox_btn_clicked)

		vbox.pack_start(play_btn, True, True, 0)
		vbox.pack_start(legacy_play_btn, True, True, 0)
		vbox.pack_start(studio_btn, True, True, 0)
		vbox.pack_start(uninstall_rlw_btn, True, True, 0)
		vbox.pack_start(reset_roblox_defaults_btn, True, True, 0)
		vbox.pack_start(uninstall_roblox_btn, True, True, 0)
	
	def on_play_btn_clicked(self, button):
		Popen(['wine', 'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
			'http://www.roblox.com/Games.aspx'])

	def on_legacy_play_btn_clicked(self, button):
		gameId = getGameId(self)
		if gameId != None:
			wineprefix = os.environ.get('HOME')
			if 'WINEPREFIX' in os.environ:
				wineprefix = os.environ.get('WINEPREFIX')

			robloxPlayerLocation = recursiveFind(wineprefix, 'RobloxPlayerBeta.exe')
			Popen(['wine', robloxPlayerLocation, '--id', gameId])

	def on_studio_btn_clicked(self, button):
		pass

	def on_uninstall_rlw_btn_clicked(self, button):
		pass

	def on_reset_roblox_defaults_btn_clicked(self, button):
		pass

	def on_uninstall_roblox_btn_clicked(self, button):
		pass


win = RLWWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()