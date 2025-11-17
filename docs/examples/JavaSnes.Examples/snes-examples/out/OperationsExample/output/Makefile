ifeq ($(strip $(PVSNESLIB_HOME)),)
$(error "Please create an environment variable PVSNESLIB_HOME by following this guide: https://github.com/alekmaul/pvsneslib/wiki/Installation")
endif

include ${PVSNESLIB_HOME}/devkitsnes/snes_rules

.PHONY: all clean logo bitmaps
export ROMNAME := JavaSnes_OperationsExample

all: logo bitmaps $(ROMNAME).sfc

pvsneslibfont.pic: pvsneslibfont.png
	$(GFXCONV) -s 8 -o 16 -u 16 -p -e 0 -i $<

bitmaps: pvsneslibfont.pic pvsneslibfont.pal

javasnes_logo.pic: javasnes_logo.bmp
	@echo convert javasnes_logo to map/pic/pal... $(notdir $@)
	$(GFXCONV) -s 8 -o 16 -u 16 -e 0 -p -m -t bmp -i $<

logo: javasnes_logo.pic javasnes_logo.map javasnes_logo.pal

clean: cleanBuildRes cleanRom cleanGfx cleanAudio
