# Ear Candy - Pulseaduio sound managment tool
# Copyright (C) 2008 Jason Taylor
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import curses 

from CursesHelpers import *

class SinkInput():
    def __init__(self, index, struct):

        self.index = index
        self.update(struct)

    def update(self, struct):
        self.name = struct.name
        self.client = struct.client
        self.sink = struct.sink

        self.driver = struct.driver
        self.driver = struct.driver

        self.channels = struct.volume.channels
        self.volume = par.volume_to_linear(struct.volume)

    def draw_control(self, win, active):

        # gauge, one bar for each channel
        gauge = win.derwin(22, self.channels+2, 0, 8-(self.channels/2))
        for i in range(0, self.channels):
            barheight = min(20, int(self.volume[i] * 18))
            gauge.vline(21-barheight, i+1, curses.ACS_BLOCK, barheight)
        gauge.border()

        win.move(23, 4)
        win.addstr(center(par.pa_clients[self.client].clean_name, 13), curses.color_pair(2) if par.pa_clients[self.client].clean_name != par.pa_clients[self.client].name else 0)
        win.move(24, 3)
        win.addstr(center(self.name, 13), curses.A_BOLD if active else 0)

    def draw_info(self, win):
        win.move(0, 2)
        win.addstr(center(self.name, 40) + "\n")

        win.addstr("\nDriver:\t\t" + self.driver)
        win.addstr("\nClient:\t\t" + par.pa_clients[self.client].name)
        win.addstr("\nLatency:\t")
        win.addstr("\nState:\t\t")

    def changeVolume(self, up):
        volume = []
        for i in range(0, len(self.volume)):
            volume.append(max(0.0, min(1.0, self.volume[i] + (+0.1 if up else -0.1))))
        par.set_sink_input_volume(self.index, volume)

from ParCur import par

"""
('index', c_uint32),
('name', c_char_p),
('owner_module', c_uint32),
('client', c_uint32),
('sink', c_uint32),
('sample_spec', pa_sample_spec),
('channel_map', pa_channel_map),
('volume', pa_cvolume),
('buffer_usec', pa_usec_t),
('sink_usec', pa_usec_t),
('resample_method', c_char_p),
('driver', c_char_p),
('mute', c_int),
("proplist",        POINTER(c_int)),
('monitor_index', c_int),
"""
