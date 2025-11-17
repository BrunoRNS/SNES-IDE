#include <snes.h>

// auto-generated global instructions
extern char javasnes_patterns, javasnes_patterns_end;
extern char javasnes_map, javasnes_map_end;
extern char javasnes_palette, javasnes_palette_end;
// end auto-generated global instructions

extern char patterns1, patterns2, patterns2_end, map3, map2, map3_end, map1, palette2, palette1, palette3, map1_end, palette2_end, patterns1_end, map2_end, patterns3_end, patterns3, palette1_end, palette3_end;
u8 actualBackground = 0;

void changeToNextBackground(void) {
	u16 pads = padsCurrent(0);
	if ((pads & KEY_A)) {
			actualBackground = (actualBackground == 2) ? 0 : (actualBackground + 1);
			setScreenOff();
			dmaClearVram();
			switch (actualBackground) {
				case 0:
					bgInitTileSet(0, &patterns1, &palette1, 0, (&patterns1_end - &patterns1), (&palette1_end - &palette1), BG_16COLORS, 0x4000);
					bgInitMapSet(0, &map1, (&map1_end - &map1), SC_32x32, 0x0000);
					setScreenOn();
					break;
				case 1:
					bgInitTileSet(0, &patterns2, &palette2, 0, (&patterns2_end - &patterns2), (&palette2_end - &palette2), BG_16COLORS, 0x4000);
					bgInitMapSet(0, &map2, (&map2_end - &map2), SC_32x32, 0x0000);
					setScreenOn();
					break;
				case 2:
					bgInitTileSet(0, &patterns3, &palette3, 0, (&patterns3_end - &patterns3), (&palette3_end - &palette3), BG_16COLORS, 0x4000);
					bgInitMapSet(0, &map3, (&map3_end - &map3), SC_32x32, 0x0000);
					setScreenOn();
					break;
		}
	}
	return;
}

void processor(void) {
	changeToNextBackground();
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
	
	setScreenOn();
	while (1) {
		processor();
		WaitForVBlank();
	}
	return 0;
}
