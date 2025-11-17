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
patterns:
.incbin "ground.pc7"
patterns_end:

map:
.incbin "ground.mp7"
map_end:

palette:
.incbin "ground.pal"
palette_end:


.ends

.section ".rodata3" superfree
patterns2:
.incbin "sky.pic"
patterns2_end:

map2:
.incbin "sky.map"
map2_end:

palette2:
.incbin "sky.pal"
palette2_end:


.ends
