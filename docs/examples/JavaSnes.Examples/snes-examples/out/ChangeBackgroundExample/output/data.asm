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
patterns1:
.incbin "map1.pic"
patterns1_end:


.ends

.section ".rodata3" superfree
palette1:
.incbin "map1.pal"
palette1_end:

map1:
.incbin "map1.map"
map1_end:


.ends

.section ".rodata4" superfree
patterns2:
.incbin "map2.pic"
patterns2_end:


.ends

.section ".rodata5" superfree
palette2:
.incbin "map2.pal"
palette2_end:

map2:
.incbin "map2.map"
map2_end:


.ends

.section ".rodata6" superfree
patterns3:
.incbin "map3.pic"
patterns3_end:


.ends

.section ".rodata7" superfree
palette3:
.incbin "map3.pal"
palette3_end:

map3:
.incbin "map3.map"
map3_end:


.ends
