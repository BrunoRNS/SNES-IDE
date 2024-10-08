/*---------------------------------------------------------------------------------


    "Made with PVSnesLib" Logo for SNES Projects


---------------------------------------------------------------------------------*/
#include "snes.h"
#include "soundbank.h"

// ROM

#define BG0 0
#define BG1 1
#define BG2 2
#define BG3 3

#define PAL0 0
#define PAL1 1
#define PAL2 2

#define whiteColor RGB8(255, 255, 255)

const u8 emptyPicture[] = {
    // First part
    0b00000000, 0b00000000, // Bit plane 1 + Bit plane 0
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000,

    // Second part
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000, 
    0b00000000, 0b00000000
};

extern char SOUNDBANK__;

extern char logoPic, logoPic_end;
extern char logoPalette;

const u16 logoTileMap[] = {
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 70 | (PAL2<<10), 71 | (PAL2<<10), 72 | (PAL2<<10), 73 | (PAL2<<10), 74 | (PAL2<<10), 75 | (PAL2<<10), 76 | (PAL2<<10), 77 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 66 | (PAL2<<10), 67 | (PAL2<<10), 68 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 92 | (PAL2<<10), 93 | (PAL2<<10), 94 | (PAL2<<10), 95 | (PAL2<<10), 96 | (PAL2<<10), 97 | (PAL2<<10), 98 | (PAL2<<10), 99 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 69 | (PAL2<<10), 00 | (PAL2<<10), 01 | (PAL2<<10), 02 | (PAL2<<10), 03 | (PAL2<<10), 04 | (PAL1<<10), 05 | (PAL1<<10), 06 | (PAL1<<10), 07 | (PAL1<<10), 8 | (PAL1<<10), 9 | (PAL1<<10), 10 | (PAL1<<10), 11 | (PAL1<<10), 12 | (PAL1<<10), 13 | (PAL1<<10), 14 | (PAL1<<10), 15 | (PAL1<<10), 16 | (PAL1<<10), 17 | (PAL1<<10), 18 | (PAL1<<10), 19 | (PAL1<<10), 20 | (PAL1<<10), 21 | (PAL1<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 91 | (PAL2<<10), 22 | (PAL2<<10), 23 | (PAL2<<10), 24 | (PAL2<<10), 25 | (PAL2<<10), 26 | (PAL1<<10), 27 | (PAL1<<10), 28 | (PAL1<<10), 29 | (PAL1<<10), 30 | (PAL1<<10), 31 | (PAL1<<10), 32 | (PAL1<<10), 33 | (PAL1<<10), 34 | (PAL1<<10), 35 | (PAL1<<10), 36 | (PAL1<<10), 37 | (PAL1<<10), 38 | (PAL1<<10), 39 | (PAL1<<10), 40 | (PAL1<<10), 41 | (PAL1<<10), 42 | (PAL1<<10), 43 | (PAL1<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 44 | (PAL2<<10), 45 | (PAL2<<10), 46 | (PAL2<<10), 47 | (PAL2<<10), 48 | (PAL1<<10), 49 | (PAL1<<10), 50 | (PAL1<<10), 51 | (PAL1<<10), 52 | (PAL1<<10), 53 | (PAL1<<10), 54 | (PAL1<<10), 55 | (PAL1<<10), 56 | (PAL1<<10), 57 | (PAL1<<10), 58 | (PAL1<<10), 59 | (PAL1<<10), 60 | (PAL1<<10), 61 | (PAL1<<10), 62 | (PAL1<<10), 63 | (PAL1<<10), 64 | (PAL1<<10), 65 | (PAL1<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 
04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10), 04 | (PAL2<<10)
};

// RAM

u16 logoPalettePVSnesLib[] = {
    whiteColor, 

    RGB8(252, 254, 252),
    RGB8(0, 0, 0),
    RGB8(0, 0, 0), 
    RGB8(24, 178, 28),
    RGB8(161, 213, 183),
    RGB8(165, 174, 224),

    RGB8(44, 52, 174),
    RGB8(42, 76, 197),
    RGB8(71, 129, 253),
    RGB8(79, 166, 253),

    RGB8(26, 18, 94),
    RGB8(45, 32, 161),
    RGB8(94, 83, 201),
    RGB8(167, 159, 237),

    whiteColor
};

u16 bgTileIndex;
u16 bg3TileMap[1024];
u8 logoState;
u8 logoColorCounter;
u8 logoColorSpeed;
u16 framesCounter;

/*!\brief Load the logo music.
*/
void initLogoMusic() {
    spcSetBank(&SOUNDBANK__);
    spcLoad(MOD_LOGO);
}

/*!\brief Set all the tiles to 0, set a palette number and a tile priority.
    \param tileMap the tile map to clear
    \param paletteNumber the palette number
    \param priority the tile priority
*/
void clearBgTextEx(u16 *tileMap, u8 paletteNumber, u8 priority) {
    for (bgTileIndex=0; bgTileIndex < 1024;) {
        tileMap[bgTileIndex] = 0 | (paletteNumber<<10) | (priority<<13);
        bgTileIndex += 1;
    }
}

/*!\brief Create a white background on B3.
*/
void initBg3White() {
    bgSetMapPtr(BG2, 0x0000 + 2048, SC_32x32);
    bgSetGfxPtr(BG2, 0x5000);
    clearBgTextEx((u16 *)bg3TileMap, PAL0, 0);
    WaitForVBlank();
    setPaletteColor(PAL0, whiteColor);

    // Copy the BG3 tile map to VRAM
    dmaCopyVram((u8 *)bg3TileMap, 0x1000, 32*32*2);

    // Copy the BG3 tile set to VRAM
    dmaCopyVram((u8 *)emptyPicture, 0x5000, 32);
}

/*!\brief Insert a value at endIndex.
    \param array the array to update
    \param startIndex the start index
    \param endIndex the max index
    \param value the value to insert
*/
void insertElement(u16 array[], u8 startIndex, u8 endIndex, u16 value) {
    while (startIndex < endIndex) {
        array[startIndex] = array[startIndex + 1];
        startIndex++;
    }

    // Insert the new element at the specified index
    array[endIndex] = value;
}

/*!\brief Initialize the "Made with PVSnesLib" logo screen.
*/
void initPVSnesLibLogo() {
    logoState = 0;
    framesCounter = 0;

    // Load logo on BG1
    bgSetMapPtr(BG0, 0x0000, SC_32x32);
    bgInitTileSet(BG0, 
        &logoPic,
        &logoPalette,
        PAL1,
        (&logoPic_end - &logoPic),
        16*2*2,
        BG_16COLORS,
        0x3000);
    WaitForVBlank();
    dmaCopyVram((u8 *)logoTileMap, 0x0000, 1024*2);

    initBg3White();

    WaitForVBlank();
    initLogoMusic();
    
    WaitForVBlank();
    spcPlay(0);
    spcProcess();
    WaitForVBlank();
    
    setMode(BG_MODE1, 0);
    bgSetEnable(BG0);
    bgSetDisable(BG1);
    bgSetEnable(BG2);
    bgSetDisable(BG3);
}

/*!\brief Update "Made with PVSnesLib" logo animation.
    \return 1 when the logo animation is complete, 0 otherwise.
*/
u8 updatePVSnesLibLogo() {
    switch(logoState) {
        case 0:
            if (framesCounter == 40) {
                logoState = 1;
                logoColorCounter = 0;
                logoColorSpeed = 4;
            }

            spcProcess();
            break;

        case 1:
            if(logoColorCounter < 4) {
                if (logoColorSpeed == 4) {
                    insertElement(logoPalettePVSnesLib, 7, 10, logoPalettePVSnesLib[7]);
                    insertElement(logoPalettePVSnesLib, 11, 14, logoPalettePVSnesLib[11]);
                    dmaCopyCGram((u8 *)logoPalettePVSnesLib, PAL1<<4, 32);
                    logoColorCounter++;
                }

                logoColorSpeed -= 1;
                if (logoColorSpeed == 0) {
                    logoColorSpeed = 4;
                }

                spcProcess();

            } else {
                if (framesCounter == 112) {
                    spcStop();
                    logoState = 2;
                }
            }
            break;

        case 2:
            spcProcess();
            return 1;
    }

    framesCounter++;

    return 0;
}
