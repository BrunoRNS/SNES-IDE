#include <snes.h>

// auto-generated global instructions
extern char javasnes_patterns, javasnes_patterns_end;
extern char javasnes_map, javasnes_map_end;
extern char javasnes_palette, javasnes_palette_end;
// end auto-generated global instructions

extern char tilfont, palfont;
u16 pads = 0;

void changeTextWithPadPress(void) {
	pads = padsCurrent(0);
	switch (pads) {
			case KEY_A:
		consoleDrawText(5, 5, "A!     ");
		break;
			case KEY_B:
		consoleDrawText(5, 5, "B!     ");
		break;
			case KEY_X:
		consoleDrawText(5, 5, "X!     ");
		break;
			case KEY_Y:
		consoleDrawText(5, 5, "Y!     ");
		break;
			case KEY_START:
		consoleDrawText(5, 5, "Start! ");
		break;
			case KEY_SELECT:
		consoleDrawText(5, 5, "Select!");
		break;
			case KEY_UP:
		consoleDrawText(5, 5, "Up!    ");
		break;
			case KEY_DOWN:
		consoleDrawText(5, 5, "Down!  ");
		break;
			case KEY_LEFT:
		consoleDrawText(5, 5, "Left!  ");
		break;
			case KEY_RIGHT:
		consoleDrawText(5, 5, "Right! ");
		break;
			case KEY_L:
		consoleDrawText(5, 5, "L!     ");
		break;
			case KEY_R:
		consoleDrawText(5, 5, "R!     ");
		break;
	}
	return;
}

void processor(void) {
	changeTextWithPadPress();
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
	while (1) {
		processor();
		WaitForVBlank();
	}
	return 0;
}
