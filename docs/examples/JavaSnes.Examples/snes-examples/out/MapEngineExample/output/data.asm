.include "hdr.asm"

.section ".rodata1" superfree
javasnes_patterns:
.incbin "javasnes_logo.pic"

javasnes_patterns_end:


javasnes_map:
.incbin "javasnes_logo.map"

javasnes_map_end:


javasnes_palette:
.incbin "javasnes_logo.pal"

javasnes_palette_end:

.ends

.section ".rodata2" superfree
tileset:
.incbin "tileslevel1.pic"
tileset_end:

tilesetpal:
.incbin "tileslevel1.pal"


.ends

.section ".rodata3" superfree
mapkungfu:
.incbin "BG1.m16"

tilesetatt:
.incbin "maplevel01.b16"

tilesetdef:
.incbin "maplevel01.t16"


.ends
