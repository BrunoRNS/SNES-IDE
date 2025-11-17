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
tilfont:
.incbin "pvsneslibfont.pic"

palfont:
.incbin "pvsneslibfont.pal"


.ends

.section ".rodata3" superfree
soundbrr:
.incbin "tada.brr"
soundbrr_end:


.ends
