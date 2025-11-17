#include <snes.h>
#include "soundbank.h"

// auto-generated global instructions
extern char javasnes_patterns, javasnes_patterns_end;
extern char javasnes_map, javasnes_map_end;
extern char javasnes_palette, javasnes_palette_end;
// end auto-generated global instructions

extern char tilfont, palfont;
extern char SOUNDBANK__0, SOUNDBANK__2, SOUNDBANK__1;
u16 bgColor = 128;
u8 keyapressed = 0;
u8 keybpressed = 0;
s8 changed = -1;

void changeToPollen8(void) {
	if ((padsCurrent(0) & KEY_B && keybpressed == 0)) {
			keybpressed = 1;
			changed = -2;
	} else {
			keybpressed = 0;
	}
	return;
}

void changeToWhatisLove(void) {
	if ((padsCurrent(0) & KEY_A && keyapressed == 0)) {
			keyapressed = 1;
			changed = 2;
	} else {
			keyapressed = 0;
	}
	return;
}

void updateScreen(void) {
	if ((changed == -2 || changed == 2)) {
			spcLoad((changed == 2) ? MOD_WHATISLOVE : MOD_POLLEN8);
			spcPlay(0);
			changed /= 2;
	}
	spcProcess();
	WaitForVBlank();
	bgColor++;
	setPaletteColor(0x00, bgColor);
	consoleDrawText(5, 10, "Let's the music play !");
	consoleDrawText(5, 12, "    A to WHATISLOVE   ");
	consoleDrawText(5, 13, "    B to POLLEN8      ");
	return;
}

void processor(void) {
	changeToPollen8();
	changeToWhatisLove();
	updateScreen();
	return;
}

int main(void) {
	
	spcBoot();
	
	spcSetBank(&SOUNDBANK__0);
	spcLoad(MOD_POLLEN8);
	
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
	spcPlay(0);
	while (1) {
		processor();
		WaitForVBlank();
	}
	return 0;
}
