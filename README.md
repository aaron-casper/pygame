# zombie splatter!

A simple top-down shooter being developed in pygame.

HUGE thanks to Mikael Lövqvist for debugging, streamlining, and in general being a genius with python

WASD/Mouse OR!!! Gamepad.

Note, if you have a gamepad connected, keyboard controls may not work.

To launch the game, clone the repo and run gameCore.py

Have fun, splatter some zombies, hack on the source, make new maps, whatever you want.

map_editor.py will launch the map editor.
the map editor modifies maps.db (sqlite3) which contains both the map tile data and the nodeGraph for the a* pathfinding algorithm.


Controls in the map editor are:
WASD to change map
mousewheel to change tile type (stone, grass, etc)
mouse to place
mouse2 to void tile (literally leaves a black void)
mouse3 (middle-click) to commit the map and nodegraph to database

If you are replacing existing tiles, you should void them before placing new.


-
Obligatory Open-Source MIT licensing blurb:
-
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

This permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
