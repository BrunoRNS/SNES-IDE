;************************************************
; snesmod soundbank data                        *
; total size:      72666 bytes                  *
;************************************************

.include "hdr.asm"

.BANK 5
.SECTION "SOUNDBANK0" ; need dedicated bank(s)

SOUNDBANK__0:
.incbin "soundbank.bnk" read $8000
.ENDS

.BANK 6
.SECTION "SOUNDBANK1" ; need dedicated bank(s)

SOUNDBANK__1:
.incbin "soundbank.bnk" skip $8000 read $8000
.ENDS

.BANK 7
.SECTION "SOUNDBANK2" ; need dedicated bank(s)

SOUNDBANK__2:
.incbin "soundbank.bnk" skip $10000
.ENDS

