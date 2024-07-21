
Before start programming with pvsneslib is very good to know the basic of how this IDE works and also how snes works

For this I made this simple tutorial: snes-basic

With your snes ide installed click in create-new-project and then you choose a folder like: C:\\Users\\User\\Desktop and then the name of your project like hello_world(no spaces or special characters), you shall have those files inside a hello_world folder in your desired folder:

main.c -> here your code
snes.h -> here your library
snes/folder -> here your library's requirements
data.asm -> Where you import data to your game with assembly
hdr.asm -> here you define your memory mapping
pvsneslib.pic -> pvsneslib font image in binary snes format(later we see how we create it)
pvsneslib.pal -> pvsneslib font pallete(later we see how we create it)

Let's begin looking into main.c
```c
#include "snes.h"

extern char tilfont, palfont;

//---------------------------------------------------------------------------------
int main(void)
{
    // Initialize SNES
    consoleInit();

    // Initialize text console with our font
    consoleSetTextVramBGAdr(0x6800);
    consoleSetTextVramAdr(0x3000);
    consoleSetTextOffset(0x0100);
    consoleInitText(0, 16 * 2, &tilfont, &palfont);

    // Init background
    bgSetGfxPtr(0, 0x2000);
    bgSetMapPtr(0, 0x6800, SC_32x32);

    // Now Put in mode 1
    setMode(BG_MODE1, 0);
    // disable Bgs except current
    bgSetDisable(1);
    bgSetDisable(2);

    // Draw a wonderful text :P
    consoleDrawText(10, 10, "Hello World !");

    // Wait for nothing :P
    setScreenOn();

    while (1)
    {
        WaitForVBlank();
    }
    return 0;
}
```

here we have a lot of functions from the imported library(snes.h) making the hello world for us
before the begin of main function we have: extern char tilfont, palfont; they are defined in data.asm, let's check it!

```s
.include "hdr.asm"

.section ".rodata1" superfree

tilfont:
.incbin "pvsneslibfont.pic"

palfont:
.incbin "pvsneslibfont.pal"

.ends
```

first we include the memory mapping, the hdr.asm, then in a section named rodata we have the fonts used on main.c, that make all the sense now!

before we see how the memory mapping works let's make some explanation:

when working with snes you should only use these types:
u8 -> char of 8 bits
u16 -> char of 16 bits
snesbool -> a boolean(true or false) for snes

chars also works as integers.

You can include using <> those libraries:

ctype.h
float.h
limits.h
math.h
setjmp.h
stdarg.h
stdbool.h
stddef.h
stdint.h
stdio.h
stdlib.h
string.h
strings.h

but very rarely you will use them.

also, understanding C code, you can navigate into snes folder and see all the functions that you can use on snes using snes.h, they're a lot!

But what is MODE_1 when we use set_Mode()? now I'll explain you

In SNES we have a lot of graphic modes, we only will use these ones:

Mode    # Colors for BG
         1   2   3   4
======---=---=---=---=
0        4   4   4   4
1       16  16   4   -
2       16  16   -   -
3      256  16   -   -
4      256   4   -   -
5       16   4   -   -
6       16   -   -   -
7      256   -   -   -  3d graphics
7EXTBG 256 128   -   -  3d graphics

In pvsneslib the best mode for us is mode1, because is with more functions, another modes you shall have to create by yourself some functions.

Now let's check hdr.asm for we compile our project:

```s
.define LOROM 1
.define SLOWROM 1

.ifndef HIROM                     ;==LoRom==

.MEMORYMAP                      ; Begin describing the system architecture.
  SLOTSIZE $8000                ; The slot is $8000 bytes in size. More details on slots later.
  DEFAULTSLOT 0                 ; There is only 1 slot in SNES, there are more in other consoles.
  SLOT 0 $8000                  ; Defines Slot 0 starting address.
  SLOT 1 $0 $2000
  SLOT 2 $2000 $E000
  SLOT 3 $0 $10000
.ENDME          ; End MemoryMap definition

.ROMBANKSIZE $8000              ; Every ROM bank is 32 KBytes in size

.else                           ;==HiRom==

.MEMORYMAP                      ; Begin describing the system architecture.
  SLOTSIZE $10000               ; The slot is $10000 bytes in size. More details on slots later.
  DEFAULTSLOT 0                 ; There is only 1 slot in SNES, there are more in other consoles.
  SLOT 0 $0000                  ; Defines Slot 0 starting address.
  SLOT 1 $0 $2000
  SLOT 2 $2000 $E000
  SLOT 3 $0 $10000
  SLOT 4 $6000                  ; Used for direct SRAM access.
.ENDME          ; End MemoryMap definition

.ROMBANKSIZE $10000              ; Every ROM bank is 32 KBytes in size

.endif

.ROMBANKS 8                     ; 2 Mbits - Tell WLA we want to use 8 ROM Banks

.SNESHEADER
  ID "SNES"                     ; 1-4 letter string, just leave it as "SNES"

  NAME "SNES IDE template    "  ; Program Title - can not be over 21 bytes,
  ;    "123456789012345678901"  ; use spaces for unused bytes of the name.

.ifdef FASTROM
  FASTROM
.else
  SLOWROM
.endif

.ifdef HIROM
  HIROM
.else
  LOROM
.endif

  CARTRIDGETYPE $00             ; $00=ROM, $01=ROM+RAM, $02=ROM+SRAM, $03=ROM+DSP1, $04=ROM+RAM+DSP1, $05=ROM+SRAM+DSP1, $13=ROM+Super FX
  ROMSIZE $08                   ; $08=2 Megabits, $09=4 Megabits,$0A=8 Megabits,$0B=16 Megabits,$0C=32 Megabits
  SRAMSIZE $00                  ; $00=0 kilobits, $01=16 kilobits, $02=32 kilobits, $03=64 kilobits
  COUNTRY $01                   ; $01= U.S., $00=Japan, $02=Europe, $03=Sweden/Scandinavia, $04=Finland, $05=Denmark, $06=France, $07=Netherlands, $08=Spain, $09=Germany, $0A=Italy, $0B=China, $0C=Indonesia, $0D=Korea
  LICENSEECODE $00              ; Just use $00
  VERSION $00                   ; $00 = 1.00, $01 = 1.01, etc.
.ENDSNES

.SNESNATIVEVECTOR               ; Define Native Mode interrupt vector table
  COP EmptyHandler
  BRK EmptyHandler
  ABORT EmptyHandler
  NMI VBlank
  IRQ EmptyHandler
.ENDNATIVEVECTOR

.SNESEMUVECTOR                  ; Define Emulation Mode interrupt vector table
  COP EmptyHandler
  ABORT EmptyHandler
  NMI EmptyHandler
  RESET tcc__start                   ; where execution starts
  IRQBRK EmptyHandler
.ENDEMUVECTOR

.ifdef FASTROM
.ifdef HIROM
.BASE $C0
.else
.BASE $80
.endif
.else
.ifdef HIROM
.BASE $40
.endif
.endif
```

I know, it sounds very complex, but the thing you have to know now is that every bank in the SNES cardridge have 32kb, and system uses the first four banks. 

Also now it's very simple to now if it's HIROM or LOROM, FASTROM or SLOWROM, because in the beginnig of the file we have .define LOROM and .define SLOWROM, if we had .define HIROM it would be HIROM, if we had defined .define FASTROM it would be a FASTROM. So, what's the difference?

Fastrom uses all snes' cpu, what would be faster, but nintendo didn't recommend It, nintendo recommend to use only SLOWROM that preserves some cpu.

HIROM and LOROM difference is more complex, but for now, HIROM can use more space for bank then LOROM can.

If you want to change from SLOWROM to FASTROM or LOROM for HIROM, just change it in .define in the beggining of the code.

Let's finally compile!

Just click in compiler and it will run automatizer(my creation to avoid Makefile)!
It will ask where is your game folder, for e.g. C:\Users\User\Desktop\Hello_World
After that automatizer will ask you HIROM or LOROM?
And then FASTROM or SLOWROM

YOU MUST SELECT THE SAME MEMORY MAPPING OF THE hdr.asm FILE

Then the automatizer will ask if you want debug mode(recommendable only for experient programmers, it won't delete temporary files created in process)

just write down **n** and press enter

will open a screen checking if the linkfile order is correct, just confirm order and press ok, maybe it can load a while and show a lot of errors. After that will appear success, press enter to exit twice. Now in the same folder as the game source you will have output.sfc, now you can run emulator, and select this rom. Now, just say, hello SNES world!

Now, how the pvsneslibfont.pic and .pal were created?

Open graphic-tools and select the option copy pvsneslib text font, and just copy it to the desired folder, you shall have font.png there, rename it to pvsneslibfont.png. Now open graphic-tools again and select gfx4snes from pvsneslib!

Choose your image: pvsneslibfont.png

and now select the correct options:

-s and down number 8
-R
-e and down number 0
-o and down number 16
-p
-u and down number 16

Now press run, and gfx4snes will convert your pvsneslibfont.png in pvsneslibfont.pal and .pic

Now you understand how the basic of snes works and some of it's formats, happy coding!