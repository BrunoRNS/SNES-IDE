ifeq ($(strip $(PVSNESLIB_HOME)),)
$(error "Please create an environment variable PVSNESLIB_HOME by following this guide: https://github.com/alekmaul/pvsneslib/wiki/Installation")
endif

include ${PVSNESLIB_HOME}/devkitsnes/snes_rules

.PHONY: all clean logo bitmaps
export ROMNAME := JavaSnes_3DBackgroundExample

all: logo bitmaps $(ROMNAME).sfc

bitmaps: ground.pc7 sky.pic

ground.pc7: ground.png
	$(GFXCONV) -p -m -M 7 -i $<

javasnes_logo.pic: javasnes_logo.bmp
	@echo convert javasnes_logo to map/pic/pal... $(notdir $@)
	$(GFXCONV) -s 8 -o 16 -u 16 -e 0 -p -m -t bmp -i $<

logo: javasnes_logo.pic javasnes_logo.map javasnes_logo.pal

clean: cleanBuildRes cleanRom cleanGfx cleanAudio

sky.pic: sky.png
	$(GFXCONV) -s 8 -o 16 -u 16 -m -p -i $<
