M8TE ver 1.5 (SNES 8bpp Tile Editor) 
Dec 9, 2022
.NET 4.5.2 (works with MONO on non-Windows systems)
For SNES game development. Mode 3 or 7.
Freeware by Doug Fraker


The MIT License (MIT)

    
version changes
1.0 - initial
1.1 - minor cosmetic changes
1.2 - fixed "save in range" off by 1 error
    - fixed rt click on tile editor bug
    - changed the default palette
1.3 - fixed a bug in the import palette where
      sometimes it wouldn't sort by brightness
    - import palette options allow less than 
      256 colors to get from an image
1.4 - added brushes "multi select" and "map edit"
      (replaces clone brushes, now removed)
    - command keys x=cut and a=select all added.
    - change v=paste and y=vertical flip
    - slight change to "best color" formula
      (should prefer a color closer to the original hue
      rather than a wrong color of the same brightness)
    - minor bug fixes
    - added a checkbox on import options, auto-
      put imported tiles on map (now off by default)
    - importing a 128x128 image (or smaller)
      now only blanks the needed tiles,
      and starts at the selected tile
    - allow small images to be imported as palettes
      (as small as 2x1) to allow 16x1 images as a palette
1.5 - bumped up version # to show that
      there were lots of changes 

This app is for generating, editing, and arranging 
SNES tiles and tilemaps (and palettes).

You can target Mode 3 (or 4) and Mode 7 with this app.
Both use 8bpp, but the formats are very different and
not very interchangable. Here's some differences.

Mode 3
------
-One 32x32 map
-Up to 4 tilesets
-Flipping of tiles allowed (H and/or V)
-The graphics format is planar / bitplanes
-The maps are 2 bytes per tile

(things not supported by this app)
-8x8 or 16x16 tiles (we are using only 8x8)
-a second layer 16 color (4bpp) map...you
 will have to use M1TE to create that


Mode 7
------
-One 128x128 map (split up into 16 - 32x32 maps)
-One tileset
-No flipping of tiles
-The graphics format is linear
-The maps are 1 byte per tile



Notes

The last 64 tiles (on tileset 4) are blocked from use. 
The reason is that using 8bpp graphics is so large that
if we used the entire 4 tilesets, there would be
no room left for tilemaps, or anything else (sprites)

Map height is disabled in Mode 7.

Mode 3 will be stuck at map 1.

Mode 7 will be stuck at tileset 1.

The RLE is a special compression format that I wrote, 
specifically for SNES maps (but could be used for tiles).
See unrle.txt (or my SNES projects) for decompression code.




Tilemaps
-------- 
1 layer. 8x8 tiles of 8bpp (256 color).
mode 3, 1 32x32 map.
mode 7, choose from 16 different maps of 32x32 (because
mode 7 uses a large 128x128 map), arranged like this...
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 16

**Editing is disabled in preview mode.** (except palettes)

Left click to add tiles to the tile map.
Right click to select a given tile, and get info on it.
You can edit the attributes of the selected tile by clicking 
H Flip or V Flip (mode 7 can't have flipped tiles)

The priority options are disabled.




Tilesets
--------
mode 3 - 4 sets of 8bpp tiles
mode 7 - 1 set of 8bpp tiles

Left click/Right click to open an editing box.
Numberpad 2,4,6,8 to move to adjacent tile. (some brushes only)
(see the key commands below)
1,2,3,4 - to change the tilset.

* the last 64 tiles (tileset 4, Mode 3) are blocked.
  see note above about that.



Tile Edit Box
-------------
Left click - place the currently selected color on the grid
Right click - get the color under the pointer
Numberpad 2,4,6,8 to move to adjacent tile.
Arrow keys to shift the image.
F - fills a tile with selected color
H - flip horizontal
Y - flip vertical
R - rotate clockwise
L - rotate counter clockwise
Delete - fills with color 0 (transparent)
C - copy
X - cut
P - paste
A - select all (only works for some brushes)



Palette
-------
Works the same in either mode. One big palette of 256 colors.

Left/Right click - select a color
R - edit red
G - edit green
B - edit blue
Hex - manually type the SNES color code (2 bytes)
(the color doesn't update until you hit Return in one of these boxes)

Key presses...(click a palette color first)
Q = copy selected color
W = paste to the selected color
E = delete the selected color (sets 0000 black)

* use caution naming palettes the same as your tileset, 
if you use YY-CHR like I do. YY-CHR will auto-create a 
palette, if you load a .chr and it also finds a .pal of 
the same name. However, it assumes RGB and not the
15 bit SNES style palette, so the palette will be junk 
colors. The load/save palette as RGB options are 
specifically for YY-CHR. THAT palette can be the same 
name as the tileset.

Even though you have 256 colors to choose from, you might
want to reserve a few for sprites (which would use the
2nd half of the palette, 128-255).



Brushsize
---------
Brushes are for the map. 1x1 means place the current 
tile. 3x3 and 5x5 will place multiples of the same tile. 
It is for painting larger areas of the screen with the 
same tile.

2x2 next is a pseudo 16x16 placement. It places x, x+1, 
x+$10, x+$11 of the selected tile in a 2x2 block on the 
screen. This might be useful if the tileset has tiles 
arranged in 16x16 blocks.

(Clone from Tiles and Clone from Map. Removed/Replaced)

Fill the Map - click on a map to fill it with the selected 
tile. (mode 7, this fills only the current 32x32 map)

Multi Tile Select (this is what you should be using mostly) - 
you can now select multiple tiles at once, and flip/shift/copy/etc
and place them on the map all as a block. But, the code to update 
the map is slower, so if you are only placing a single tile at a 
time, it will be smoother using the 1x1 brush.

Map Edit Only - You can now select multiple tiles on the map view
with this brush, and copy/cut/paste/fill/delete and flip them
all at once. 
(some of the checkboxes are disabled with this brush/mode.
Use key commands to flip - h and y)
Tip - Combine fill (f) with "palette only" to change 
the palette of the selected area.
You can't rotate or pixel shift in this mode.
(note - mode 7 tiles don't flip)



Menu
----
All the menu options should be self-explanatory. Some of 
them won't work if you are in the wrong mode. The message 
box should explain the problem.

Loading a 16 color palette loads to the currently selected 
palette row. Same with saving 16 color. It saves the 
currently selected palette row.

Saving Maps only saves the currently selected map. Loading 
maps only loads to the currently selected map.

Loading/Saving 1 tileset will load/save the currently 
selected set. You can also save 2 tilsets (Mode 3). If you
have more than 2 tilsets to save, you will have to split
it into 2 different save files. (there is a size limit
in the RLE code of 32768 bytes, that's why max 2).

File/Export Image saves the current view on the Tilemap 
as .png .bmp .gif or .jpg

Tiles/Remove Duplicate Tiles - will look within the same 
bit depth for duplicates (including flipped versions of 
the same tile), and remove them. 
It will also scan the maps and renumber them to match 
the new tilesets.
* this function will work differently in Mode 7, because
it won't flip tiles.

Tiles/Load to Selected Tile - first select a tile in the tileset. Then click this to load a CHR file at the 
selected point. You can combine CHR files this way, or 
use it as a paste option.

Tiles/Save Tiles in a Range - if you only want to save a 
portion of a tileset, or maybe 1 1/2 of a tileset. Also, 
can use like a copy/paste with the above.

Maps/Load to Selected Y* - first select a location in the
tile map, then this will load a map starting at that row

Maps/Load to Selected Y, Offset to Selected Tile* - First
select a tile map location, then select a tile in the set,
then choose this to load a map at the specific map row,
and it will also change the tile numbers in the map you
are loading to start at the selected tile. Why? Let's say
you are working on one project, which has a tileset and
map saved, and you want to import those into another
project, so you load the tileset below the current tileset,
and now the corresponding map has the tile numbers wrong.
This would adjust the tile numbers on the imported map,
for the now relocated tiles.

*currently, these only work in Mode 3.



Import an image
---------------
.png .jpg .bmp .gif - files need to be 256x240 or smaller
This will be a 3 step process. 
First, select options and set a dither level.
Then, get the palette from the image (or make your own palette).
Finally, get the tiles/map from the image.
-CAUTION, it will erase the entire tileset and the current map
 (only if it is larger than 128x128, a small image will only
  delete the needed area)
-if a file has an indexed palette, it will not read it... 
it always auto-generates an optimized palette
-in Mode 7 the size limit is 128x128 pixel.
-the dithering is with brightness, and is not very good with hue shifts
-dithered graphics don't compress very well



BG Mode / Mode 7 Preview
------------------------
is a zoomed out view of the 128x128 Mode 7 map.
Editing is disabled in this mode.



Native .M8 file format details...
16 byte header = 
 2 bytes = "M8"
 1 byte = # of the file version (should be 1)
 1 byte = # of palettes (should be 1)
 1 byte = # of maps (should be 16)
 1 byte = # of 8bpp tilesets (should be 4)
 1 byte = map height
 1 byte = which bg mode (0,1,2)
 pad 8 zeros
512 bytes per palette (should be 512 total)
2048 bytes per tile map (x16 should be 32768 total)
16384 bytes per 4bpp tile set (x4 should be 65536 total)

16 + 512 + 32768 + 65536 = 98832 bytes per file, exactly.




///////////////////////////////////////////////
TODO-
-more load map options (mode 7)
-make it easier to change maps, like...
 scroll bars for mode 7 ?
///////////////////////////////////////////////



Credits -
I used Klarth's Console Graphics Document...
https://mrclick.zophar.net/TilEd/download/consolegfx.txt
in making this software. 


