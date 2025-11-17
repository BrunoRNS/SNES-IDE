#include <snes.h>

// auto-generated global instructions
extern char javasnes_patterns, javasnes_patterns_end;
extern char javasnes_map, javasnes_map_end;
extern char javasnes_palette, javasnes_palette_end;
// end auto-generated global instructions

extern char tilfont, palfont;
extern char soundbrr_end, soundbrr;
brrsamples tadasound;
u16 bgColor = 128;
u8 keyapressed = 0;
u16 pads = 0;

void playIfAPressed(void) {
	consoleDrawText(5, 10, "Press A to play effect !");
	pads = padsCurrent(0);
	if ((pads & KEY_A)) {
			if ((keyapressed == 0)) {
				keyapressed = 1;
				spcPlaySound(0);
				bgColor += 16;
				setPaletteColor(0x00, bgColor);
		}
	} else {
			keyapressed = 0;
	}
	spcProcess();
	return;
}

void processor(void) {
	playIfAPressed();
	return;
}

int main(void) {
	
	spcBoot();
	
	spcAllocateSoundRegion(39);
	
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
	spcSetSoundEntry(15, 15, 4, &soundbrr_end - &soundbrr, &soundbrr, &tadasound);
	while (1) {
		processor();
		WaitForVBlank();
	}
	return 0;
}
