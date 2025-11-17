#include <snes.h>

// auto-generated global instructions
extern char javasnes_patterns, javasnes_patterns_end;
extern char javasnes_map, javasnes_map_end;
extern char javasnes_palette, javasnes_palette_end;
// end auto-generated global instructions

extern char tilfont, palfont;
u32 timer = 0;

void ifExample(void) {
	u8 num1 = 4;
	u8 num2 = 8;
	if ((num1 > num2)) {
			consoleDrawText(3, 3, "%d > %d", (int) num1, (int) num2);
	} else if ((num1 < num2)) {
			consoleDrawText(3, 3, "%d < %d", (int) num1, (int) num2);
	} else {
			consoleDrawText(3, 3, "%d == %d", (int) num1, (int) num2);
	}
	return;
}

void switchExample(void) {
	s8 num = -8;
	switch (num) {
			case 8:
		consoleDrawText(3, 6, "num = 8");
		break;
			case -8:
		consoleDrawText(3, 6, "num = -8");
		break;
			default:
		consoleDrawText(3, 6, "num is not -8 or 8");
		break;
	}
	return;
}

void whileLoopExample(void) {
	while ((timer < 200)) {
			consoleDrawText(3, 9, "timer: %d", (int) timer);
			timer++;
			WaitForVBlank();
	}

	return;
}

void processor(void) {
	ifExample();
	switchExample();
	whileLoopExample();
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
