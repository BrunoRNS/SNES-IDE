#include <snes.h>

// auto-generated global instructions
extern char javasnes_patterns, javasnes_patterns_end;
extern char javasnes_map, javasnes_map_end;
extern char javasnes_palette, javasnes_palette_end;
// end auto-generated global instructions

extern char tilesetatt, mapkungfu, tileset, tilesetpal, tileset_end, tilesetdef;
u16 pad0 = 0;
s16 mapscx = 16 * 8;
u8 keyl = 0;
u8 keyr = 0;

void MoveCameraInBackground(void) {
	mapUpdate();
	pad0 = padsCurrent(0);
	if ((pad0 & KEY_LEFT && mapscx > 16 * 8)) {
			mapscx -= 1;
	} else if ((pad0 & KEY_RIGHT && mapscx < (208 * 8))) {
			mapscx += 1;
	}
	mapUpdateCamera(mapscx, 0);
	mapVblank();
	return;
}

void processor(void) {
	MoveCameraInBackground();
	return;
}

int main(void) {
	
	spcBoot();
	
	
	bgInitTileSet(0, &javasnes_patterns, &javasnes_palette, 0, (&javasnes_patterns_end - &javasnes_patterns), (&javasnes_palette_end - &javasnes_palette), BG_16COLORS, 0x4000);
	bgInitMapSet(0, &javasnes_map, (&javasnes_map_end - &javasnes_map), SC_32x32, 0x0000);
	
	
	setMode(BG_MODE1, 0);
	bgSetDisable(1);
	bgSetDisable(2);
	setScreenOn();
	
	
	WaitForVBlank();
	
	u8 i;
	for (i = 0; i < 120; i++) {
		WaitForVBlank();
	}
	dmaClearVram();
	
	setScreenOff();
	bgSetDisable(0);
	bgInitTileSet(0, &tileset, &tilesetpal, 0, (&tileset_end - &tileset), 16 * 2 * 3, BG_16COLORS, 0x2000);
	bgSetMapPtr(0, 0x6800, SC_64x32);
	bgSetEnable(0);
	setScreenOn();
	mapLoad((u8*) &mapkungfu, (u8*) &tilesetdef, (u8*) &tilesetatt);
	WaitForVBlank();
	while (1) {
		processor();
		WaitForVBlank();
	}
	return 0;
}
