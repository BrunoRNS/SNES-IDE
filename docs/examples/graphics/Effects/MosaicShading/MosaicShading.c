/*---------------------------------------------------------------------------------


    Simple tile mode 1 demo
    -- alekmaul


---------------------------------------------------------------------------------*/
#include "snes.h"

extern char patterns, patterns_end;
extern char palette, palette_end;
extern char map, map_end;

//---------------------------------------------------------------------------------

// NOTE: Does not pause execution if a pad 0 key is currently pressed.
void WaitForKey() {
    while (padsCurrent(0) == 0)
    {
        WaitForVBlank();
    }
}

int main(void)
{
    // Copy tiles to VRAM
    bgInitTileSet(0, &patterns, &palette, 0, (&patterns_end - &patterns), (&palette_end - &palette), BG_16COLORS, 0x4000);

    // Copy Map to VRAM
    bgInitMapSet(0, &map, (&map_end - &map), SC_32x32, 0x1000);

    // Now Put in 16 color mode and disable other BGs except 1st one
    setMode(BG_MODE1, 0);
    bgSetDisable(1);
    bgSetDisable(2);
    setScreenOn();

    WaitForKey();

    // Now just play with effects :P
    while (1)
    {
        // Fade out so light to black
        setFadeEffect(FADE_OUT);
        WaitForVBlank();
        WaitForKey();

        // Fade in now so black to light
        setFadeEffect(FADE_IN);
        WaitForVBlank();
        WaitForKey();

        // Now do some big pixels
        setMosaicEffect(MOSAIC_OUT, MOSAIC_BG1);
        WaitForVBlank();
        WaitForKey();

        // And now restore screen to normal
        setMosaicEffect(MOSAIC_IN, MOSAIC_BG1);
        WaitForVBlank();
        WaitForKey();
    }
    return 0;
}
