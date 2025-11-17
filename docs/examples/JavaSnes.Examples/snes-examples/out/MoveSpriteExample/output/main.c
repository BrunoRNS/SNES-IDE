#include <snes.h>
#define FRAMES_PER_ANIMATION 3

// auto-generated global instructions
extern char javasnes_patterns, javasnes_patterns_end;
extern char javasnes_map, javasnes_map_end;
extern char javasnes_palette, javasnes_palette_end;
// end auto-generated global instructions

extern char palsprite, palsprite_end, gfxsprite, gfxsprite_end;
typedef struct {
	s16 x, y;
	u16 gfx_frame, anim_frame;
	u8 state, flipx;
} Monster;

enum {
	W_RIGHT = 2,
	W_DOWN = 0,
	W_UP = 1,
	W_LEFT = 2,
};

enum {
	SCREEN_BOTTOM = 224,
	SCREEN_LEFT = -16,
	SCREEN_RIGHT = 256,
	SCREEN_TOP = -16,
};

char sprTiles[9] = {0, 2, 4, 6, 8, 10, 12, 14, 32};
u16 pad0 = 0;
Monster monster = {.x = 100, .y = 100};

void updateSprite(void) {
	pad0 = padsCurrent(0);
	switch (pad0) {
			case KEY_DOWN:
		monster.y = (monster.y <= SCREEN_BOTTOM) ? monster.y + 1 : monster.y;
		monster.flipx = 0;
		monster.state = W_DOWN;
		break;
			case KEY_LEFT:
		monster.x = (monster.y >= SCREEN_LEFT) ? monster.x - 1 : monster.x;
		monster.flipx = 1;
		monster.state = W_LEFT;
		break;
			case KEY_RIGHT:
		monster.x = (monster.x <= SCREEN_RIGHT) ? monster.x + 1 : monster.x;
		monster.flipx = 0;
		monster.state = W_RIGHT;
		break;
			case KEY_UP:
		monster.y = (monster.y >= SCREEN_TOP) ? monster.y - 1 : monster.y;
		monster.flipx = 0;
		monster.state = W_UP;
		break;
	}
	monster.anim_frame = (pad0 && (monster.anim_frame >= FRAMES_PER_ANIMATION)) ? 0 : (pad0 & pad0) ? monster.anim_frame + 1 : monster.anim_frame;
	monster.gfx_frame = sprTiles[(monster.anim_frame + (FRAMES_PER_ANIMATION * monster.state))];
	oamSet(0, monster.x, monster.y, 3, monster.flipx, 0, monster.gfx_frame, 0);
	return;
}

void processor(void) {
	updateSprite();
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
	oamInitGfxSet(&gfxsprite, (&gfxsprite_end - &gfxsprite), &palsprite, (&palsprite_end - &palsprite), 0, 0x0000, OBJ_SIZE16_L32);
	oamSet(0, monster.x, monster.y, 0, 0, 0, 0, 0);
	oamSetEx(0, OBJ_SMALL, OBJ_SHOW);
	oamSetVisible(0, OBJ_SHOW);
	setScreenOn();
	while (1) {
		processor();
		WaitForVBlank();
	}
	return 0;
}
