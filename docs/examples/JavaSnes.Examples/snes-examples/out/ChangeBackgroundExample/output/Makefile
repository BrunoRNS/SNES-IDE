ifeq ($(strip $(PVSNESLIB_HOME)),)
$(error "Please create an environment variable PVSNESLIB_HOME by following this guide: https://github.com/alekmaul/pvsneslib/wiki/Installation")
endif

include ${PVSNESLIB_HOME}/devkitsnes/snes_rules

.PHONY: all clean logo bitmaps
export ROMNAME := JavaSnes_ChangeBackgroundExample

all: logo bitmaps $(ROMNAME).sfc

bitmaps: map1.map map1.pic map1.pal map2.map map2.pic map2.pal map3.map map3.pic map3.pal

javasnes_logo.pic: javasnes_logo.bmp
	@echo convert javasnes_logo to map/pic/pal... $(notdir $@)
	$(GFXCONV) -s 8 -o 16 -u 16 -e 0 -p -m -t bmp -i $<

map3.map: map3.bmp
	$(GFXCONV) -s 8 -o 16 -u 16 -e 0 -p -m -t bmp -i $<

map2.map: map2.bmp
	$(GFXCONV) -s 8 -o 16 -u 16 -e 0 -p -m -t bmp -i $<

map1.map: map1.bmp
	$(GFXCONV) -s 8 -o 16 -u 16 -e 0 -p -m -t bmp -i $<

logo: javasnes_logo.pic javasnes_logo.map javasnes_logo.pal

clean: cleanBuildRes cleanRom cleanGfx cleanAudio
