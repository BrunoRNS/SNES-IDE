#include <snes.h>

// auto-generated global instructions
extern char javasnes_patterns, javasnes_patterns_end;
extern char javasnes_map, javasnes_map_end;
extern char javasnes_palette, javasnes_palette_end;
// end auto-generated global instructions

extern char tilfont, palfont;
u16 pads = 0;
s32 loadedValue = 0;

void saveGame(void) {
	pads = padsCurrent(0);
	if ((pads & KEY_B)) {
			consoleCopySram((u8*) &loadedValue, 4);
	}
	return;
}

void loadGame(void) {
	pads = padsCurrent(0);
	if ((pads & KEY_A)) {
			consoleLoadSram((u8*) &loadedValue, 4);
	}
	return;
}

void addOrsubValue(void) {
	pads = padsCurrent(0);
	if ((pads & KEY_UP)) {
			loadedValue += 1;
	} else if ((pads & KEY_DOWN)) {
			loadedValue -= 1;
	}
	consoleDrawText(0, 2, "Press Up or Down to add or sub 1");
	consoleDrawText(0, 4, "Press A to load, B to save value");
	consoleDrawText(4, 8, "Value: %d        ", (int) loadedValue);
	return;
}

void processor(void) {
	saveGame();
	loadGame();
	addOrsubValue();
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
	consoleSetTextMapPtr(0x6800);
	consoleSetTextGfxPtr(0x3000);
	consoleSetTextOffset(0x0100);
	consoleInitText(0, 16 * 2, &tilfont, &palfont);
	bgSetGfxPtr(0, 0x2000);
	bgSetMapPtr(0, 0x6800, SC_32x32);
	setScreenOn();
	consoleCopySram((u8 *) &loadedValue, 4);
	while (1) {
		processor();
		WaitForVBlank();
	}
	return 0;
}
