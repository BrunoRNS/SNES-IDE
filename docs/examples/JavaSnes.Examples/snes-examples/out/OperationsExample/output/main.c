#include <snes.h>

// auto-generated global instructions
extern char javasnes_patterns, javasnes_patterns_end;
extern char javasnes_map, javasnes_map_end;
extern char javasnes_palette, javasnes_palette_end;
// end auto-generated global instructions

extern char tilfont, palfont;

void addTwoNumbers(void) {
	u8 num1 = 4;
	u8 num2 = 5;
	u8 result;
	result = (num1 + num2);
	consoleDrawText(3, 1, "%d + %d = %d", (int) num1, (int) num2, (int) result);
	return;
}

void subTwoNumbers(void) {
	u8 num1 = 6;
	u8 num2 = 3;
	u8 result;
	result = (num1 - num2);
	consoleDrawText(3, 4, "%d - %d = %d", (int) num1, (int) num2, (int) result);
	return;
}

void plusTwoNumbers(void) {
	u8 num1 = 4;
	u8 num2 = 5;
	u8 result;
	result = (num1 * num2);
	consoleDrawText(3, 7, "%d * %d = %d", (int) num1, (int) num2, (int) result);
	return;
}

void divideTwoNumbers(void) {
	u8 num1 = 8;
	u8 num2 = 2;
	u8 result;
	result = (num1 / num2);
	consoleDrawText(3, 10, "%d / %d = %d", (int) num1, (int) num2, (int) result);
	return;
}

void modTwoNumbers(void) {
	u8 num1 = 26;
	u8 num2 = 5;
	u8 result;
	result = (num1 % num2);
	consoleDrawText(3, 13, "%d %% %d = %d", (int) num1, (int) num2, (int) result);
	return;
}

void shiftTwoNumbers(void) {
	u8 num1 = 4;
	u8 num2 = 16;
	u8 result1;
	u8 result2;
	result1 = (num1 << 3);
	result2 = (num2 >> 2);
	consoleDrawText(3, 16, "%d << 3 = %d", (int) num1, (int) result1);
	consoleDrawText(3, 19, "%d >> 2 = %d", (int) num2, (int) result2);
	return;
}

void shiftTwoSignedNumbers(void) {
	s8 num1 = -4;
	s8 num2 = -16;
	s8 result1;
	s8 result2;
	result1 = (num1 << 3);
	result2 = (num2 >> 2);
	consoleDrawText(3, 21, "%d << 3 = %d", (int) num1, (int) result1);
	consoleDrawText(3, 24, "%d >> 2 = %d", (int) num2, (int) result2);
	return;
}

void processor(void) {
	addTwoNumbers();
	subTwoNumbers();
	plusTwoNumbers();
	divideTwoNumbers();
	modTwoNumbers();
	shiftTwoNumbers();
	shiftTwoSignedNumbers();
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
