#include <snes.h>
#define SKYLINEY 96

// auto-generated global instructions
extern char javasnes_patterns, javasnes_patterns_end;
extern char javasnes_map, javasnes_map_end;
extern char javasnes_palette, javasnes_palette_end;
// end auto-generated global instructions

extern char patterns_end, patterns2, patterns2_end, map2, palette2, patterns, palette, map2_end, map_end, map, palette2_end, palette_end;
u8 ModeTable[5] = {SKYLINEY, BG_MODE3, 1, BG_MODE7, 0x00};
u8 BGTable[5] = {SKYLINEY, 0x12, 1, 0x11, 0x00};
u8 PerspectiveX[264] = {
	        SKYLINEY, 256 & 255, 256 >> 8,
	        0xFF,
	        1, 0,
	        0, 2,
	        243, 1,
	        231, 1,
	        220, 1,
	        209, 1,
	        199, 1,
	        189, 1,
	        179, 1,
	        170, 1,
	        161, 1,
	        153, 1,
	        145, 1,
	        137, 1,
	        130, 1,
	        123, 1,
	        116, 1,
	        109, 1,
	        103, 1,
	        97, 1,
	        91, 1,
	        85, 1,
	        79, 1,
	        74, 1,
	        69, 1,
	        64, 1,
	        59, 1,
	        54, 1,
	        49, 1,
	        45, 1,
	        40, 1,
	        36, 1,
	        32, 1,
	        28, 1,
	        24, 1,
	        20, 1,
	        17, 1,
	        13, 1,
	        9, 1,
	        6, 1,
	        3, 1,
	        0, 1,
	        252, 0,
	        249, 0,
	        246, 0,
	        243, 0,
	        240, 0,
	        238, 0,
	        235, 0,
	        232, 0,
	        230, 0,
	        227, 0,
	        225, 0,
	        222, 0,
	        220, 0,
	        217, 0,
	        215, 0,
	        213, 0,
	        211, 0,
	        208, 0,
	        206, 0,
	        204, 0,
	        202, 0,
	        200, 0,
	        198, 0,
	        196, 0,
	        195, 0,
	        193, 0,
	        191, 0,
	        189, 0,
	        187, 0,
	        186, 0,
	        184, 0,
	        182, 0,
	        181, 0,
	        179, 0,
	        178, 0,
	        176, 0,
	        175, 0,
	        173, 0,
	        172, 0,
	        170, 0,
	        169, 0,
	        167, 0,
	        166, 0,
	        165, 0,
	        163, 0,
	        162, 0,
	        161, 0,
	        159, 0,
	        158, 0,
	        157, 0,
	        156, 0,
	        155, 0,
	        153, 0,
	        152, 0,
	        151, 0,
	        150, 0,
	        149, 0,
	        148, 0,
	        147, 0,
	        146, 0,
	        145, 0,
	        144, 0,
	        143, 0,
	        142, 0,
	        141, 0,
	        140, 0,
	        139, 0,
	        138, 0,
	        137, 0,
	        136, 0,
	        135, 0,
	        134, 0,
	        133, 0,
	        132, 0,
	        132, 0,
	        131, 0,
	        130, 0,
	        129, 0,
	        128, 0,
	        127, 0,
	        127, 0,
	        126, 0,
	        125, 0,
	        124, 0,
	        124, 0,
        123, 0};
u8 PerspectiveY[264] = {
	        SKYLINEY, 256 & 255, 256 >> 8,
	        0xFF,
	122, 0,
	        0, 16,
	        60, 15,
	        139, 14,
	        233, 13,
	        85, 13,
	        204, 12,
	        78, 12,
	        218, 11,
	        109, 11,
	        8, 11,
	        170, 10,
	        82, 10,
	        0, 10,
	        178, 9,
	        105, 9,
	        36, 9,
	        227, 8,
	        166, 8,
	        107, 8,
	        52, 8,
	        0, 8,
	        206, 7,
	        158, 7,
	        113, 7,
	        69, 7,
	        28, 7,
	        244, 6,
	        206, 6,
	        170, 6,
	        135, 6,
	        102, 6,
	        70, 6,
	        39, 6,
	        9, 6,
	        237, 5,
	        209, 5,
	        182, 5,
	        157, 5,
	        132, 5,
	        108, 5,
	        85, 5,
	        62, 5,
	        41, 5,
	        20, 5,
	        0, 5,
	        236, 4,
	        217, 4,
	        198, 4,
	        180, 4,
	        163, 4,
	        146, 4,
	        129, 4,
	        113, 4,
	        98, 4,
	        83, 4,
	        68, 4,
	        53, 4,
	        39, 4,
	        26, 4,
	        12, 4,
	        0, 4,
	        243, 3,
	        231, 3,
	        218, 3,
	        207, 3,
	        195, 3,
	        184, 3,
	        173, 3,
	        162, 3,
	        152, 3,
	        142, 3,
	        132, 3,
	        122, 3,
	        112, 3,
	        103, 3,
	        94, 3,
	        85, 3,
	        76, 3,
	        67, 3,
	        59, 3,
	        51, 3,
	        43, 3,
	        35, 3,
	        27, 3,
	        19, 3,
	        12, 3,
	        4, 3,
	        253, 2,
	        246, 2,
	        239, 2,
	        232, 2,
	        226, 2,
	        219, 2,
	        212, 2,
	        206, 2,
	        200, 2,
	        194, 2,
	        188, 2,
	        182, 2,
	        176, 2,
	        170, 2,
	        165, 2,
	        159, 2,
	        154, 2,
	        148, 2,
	        143, 2,
	        138, 2,
	        133, 2,
	        127, 2,
	        123, 2,
	        118, 2,
	        113, 2,
	        108, 2,
	        103, 2,
	        99, 2,
	        94, 2,
	        90, 2,
	        85, 2,
	        81, 2,
	        77, 2,
	        73, 2,
	        68, 2,
	        64, 2,
	        60, 2,
	        56, 2,
	        52, 2,
        49, 2};;
u16 pad0;
u16 sz = 0;
u16 sx = 0;
u16 sy = 0;
dmaMemory data_to_transfertMode;
dmaMemory data_to_transfertBG;
dmaMemory data_to_transfertX;
dmaMemory data_to_transfertY;

void getTables(void) {
	data_to_transfertMode.mem.p = (u8 *)&ModeTable;
	data_to_transfertBG.mem.p = (u8 *)&BGTable;
	data_to_transfertX.mem.p = (u8 *)&PerspectiveX;
	data_to_transfertY.mem.p = (u8 *)PerspectiveY;
	return;
}

void updateCameraInBg(void) {
	pad0 = padsCurrent(0);
	switch (pad0) {
			case KEY_DOWN:
		sy += 1;
		break;
			case KEY_R:
		sz += 1;
		break;
			case KEY_LEFT:
		sx -= 1;
		break;
			case KEY_RIGHT:
		sx += 1;
		break;
			case KEY_UP:
		sy -= 1;
		break;
			case KEY_L:
		sz -= 1;
		break;
	}
	return;
}

void setMode7_HdmaPerspective(void) {
	REG_M7HOFS = (sx & 255);
	REG_M7HOFS = sx >> 8;
	REG_M7VOFS = (sy & 255);
	REG_M7VOFS = sy >> 8;
	REG_BG2HOFS = (sx & 255);
	REG_BG2HOFS = sx >> 8;
	REG_M7X = (sx + 128) & 255;
	REG_M7X = (sx + 128) >> 8;
	REG_M7Y = (sy + 112) & 255;
	REG_M7Y = (sy + 112) >> 8;
	REG_HDMAEN = 0;
	REG_DMAP1 = 0x00;
	REG_BBAD1 = 0x05;
	REG_A1T1LH = data_to_transfertMode.mem.c.addr;
	REG_A1B1 = data_to_transfertMode.mem.c.bank;
	REG_DMAP2 = 0x00;
	REG_BBAD2 = 0x2C;
	REG_A1T2LH = data_to_transfertBG.mem.c.addr;
	REG_A1B2 = data_to_transfertBG.mem.c.bank;
	REG_DMAP3 = 0x02;
	REG_BBAD3 = 0x1B;
	REG_A1T3LH = data_to_transfertX.mem.c.addr;
	REG_A1B3 = data_to_transfertX.mem.c.bank;
	REG_DMAP4 = 0x02;
	REG_BBAD4 = 0x1E;
	REG_A1T4LH = data_to_transfertY.mem.c.addr;
	REG_A1B4 = data_to_transfertY.mem.c.bank;
	REG_HDMAEN = 0x1E;
	return;
}

void processor(void) {
	updateCameraInBg();
	setMode7_HdmaPerspective();
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
	bgInitMapTileSet7(&patterns, &map, &palette, (&patterns_end - &patterns), 0x0000);
	bgInitMapSet(1, &map2, (&map2_end - &map2), SC_64x32, 0x4000);
	bgInitTileSet(1, &patterns2, &palette, 0, (&patterns2_end - &patterns2), (&palette2_end - &palette2), BG_16COLORS, 0x5000);
	setMode7(0);
	setScreenOn();
	getTables();
	while (1) {
		processor();
		WaitForVBlank();
	}
	return 0;
}
