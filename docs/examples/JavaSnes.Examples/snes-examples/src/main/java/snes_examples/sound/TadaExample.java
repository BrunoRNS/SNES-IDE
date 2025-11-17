package snes_examples.sound;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import javasnes.App;
import javasnes.boot.Boot;
import javasnes.data.Data;
import javasnes.hdr.MemoryMapping;
import javasnes.input.SnesInput;
import javasnes.instruction.SnesInstruction;
import javasnes.makefile.Make;
import javasnes.output.SnesOutput;
import javasnes.sneslib.SnesSound;
import javasnes.util.logic.SnesElse;
import javasnes.util.logic.SnesIf;
import javasnes.util.operators.SnesOperator;
import javasnes.util.operators.assign.OperatorAssign;
import javasnes.util.operators.binary.OperatorBinAnd;
import javasnes.util.operators.logical.OperatorEquals;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU16;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU8;
import javasnes.util.types.vars.scalar.sound.SnesBrrSample;

public class TadaExample {

        final static SnesChar CHAR = new SnesChar("char");

        public static void main(String[] args) throws Exception {

                App.Builder tadaExample = Config.generateApp();

                Map<String, String> memMapConfig = new HashMap<>();
                memMapConfig.put("name", "TadaExample          ");

                MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

                tadaExample.setMemoryMapping(memMap);

                AppData appData = Config.generateAppData();
                appData.registerData(new Data("tilfont", "pvsneslibfont.pic", false), (byte) 2);
                appData.registerData(new Data("palfont", "pvsneslibfont.pal", false), (byte) 2);

                // Add Tada BRR to app data in a deticated bank, it requires end tag
                appData.registerData(new Data("soundbrr", "tada.brr", true), (byte) 3);

                tadaExample.setAppData(appData);

                Boot boot = Config.generateBoot();
                tadaExample.setBoot(boot);

                SnesInstruction[] globalDefs = new SnesInstruction[6];

                String[] loadExternFont = { "tilfont", "palfont" };
                globalDefs[0] = new SnesLoadExtern(loadExternFont, CHAR);

                String[] loadExternBrr = { "soundbrr", "soundbrr_end" };
                globalDefs[1] = new SnesLoadExtern(loadExternBrr, CHAR);

                globalDefs[2] = new SnesBrrSample("tadasound");
                globalDefs[3] = new SnesU16("bgColor", "128");
                globalDefs[4] = new SnesU8("keyapressed", "0");
                globalDefs[5] = new SnesU16("pads", "0");

                tadaExample.setGlobalInstructions(globalDefs);

                Processor processor = new Processor();
                SnesProcess[] processes = new SnesProcess[1];

                processes[0] = playIfAPressed();
                processor.addProcess(processes[0], null);

                tadaExample.setSnesProcesses(processes);
                tadaExample.setProcessor(processor);

                Make makefile = Config.generateMakefile();
                makefile.setRomName("JavaSnes_TadaExample");

                Config.addMakeRules(makefile);

                tadaExample.setMakefile(makefile);

                Config.build(tadaExample);

        }

        /**
         * A process that plays a sound and changes the background color if the A
         * key is pressed.
         *
         * This process first assigns the current pad state to a variable "pads".
         * Then, it checks if the A key is pressed by checking the value of the
         * "keyapressed" variable. If the A key is pressed, it plays a sound and
         * changes the background color to a color specified by the "bgColor"
         * variable. If the A key is not pressed, it sets the "keyapressed" variable
         * to 0.
         *
         * @return A process that plays a sound and changes the background color if
         *         the A key is pressed.
         */
        public static SnesProcess playIfAPressed() {

                SnesInstruction[] commands = new SnesInstruction[4];

                commands[0] = SnesOutput.consoleDrawText(5, 10, "Press A to play effect !", null);

                SnesU16 pads = new SnesU16("pads");
                SnesU16 bgColor = new SnesU16("bgColor");
                SnesU8 keyAPressedVar = new SnesU8("keyapressed");

                SnesOperator assignPadsCurrent = new OperatorAssign(
                                "pads", SnesInput.padsCurrent((byte) 0).sourceCode);

                commands[1] = assignPadsCurrent;

                List<SnesInstruction> ifNotPressedCommands = new ArrayList<>();

                ifNotPressedCommands.add(new OperatorAssign(keyAPressedVar.name, "0"));

                SnesElse ifNotPressed = new SnesElse(
                                ifNotPressedCommands);

                SnesOperator varACheck = new OperatorEquals(keyAPressedVar.name, "0");

                List<SnesInstruction> ifAVarCheckCommands = new ArrayList<>();

                ifAVarCheckCommands.add(new OperatorAssign(keyAPressedVar.name, "1"));
                ifAVarCheckCommands.add(SnesSound.spcPlaySound(0));
                ifAVarCheckCommands.add(new OperatorAssign(bgColor.name, "16", '+'));
                ifAVarCheckCommands.add(SnesOutput.setPaletteColor("0x00", bgColor));

                SnesIf ifAVarCheck = new SnesIf(
                                varACheck, ifAVarCheckCommands);

                ifAVarCheck.generateSourceCode();

                SnesOperator keyAPressed = new OperatorBinAnd(
                                pads, new SnesU16(SnesInput.keys.KEY_A.sourceCode));

                List<SnesInstruction> ifPressedCommands = new ArrayList<>();

                ifPressedCommands.add(ifAVarCheck);

                SnesIf ifAPressed = new SnesIf(
                                keyAPressed, ifPressedCommands, ifNotPressed);

                ifAPressed.generateSourceCode();

                commands[2] = ifAPressed;

                commands[3] = SnesSound.spcProcess();

                return new SnesProcess("playIfAPressed", (byte) 0, commands);

        }

        private static interface Config {

                public static App.Builder generateApp() {
                        return new App.Builder();
                }

                public static MemoryMapping generateMemoryMapping(Map<String, String> config) {

                        MemoryMapping memMap = new MemoryMapping(config);
                        return memMap;

                }

                public static AppData generateAppData() {
                        return new AppData();
                }

                public static Boot generateBoot() {

                        Boot boot = new Boot(postLogoCommands());
                        return boot;

                }

                public static Map<String, Map<String, String[]>> postLogoCommands() {

                        Map<String, Map<String, String[]>> boot = new HashMap<>();

                        boot.put("betweenSPCVRAMLoadCommands", new LinkedHashMap<>());

                        // around 10K of sound ram, 39 256-byte blocks
                        boot.get("betweenSPCVRAMLoadCommands")
                                        .put("spcAllocateSoundRegion", new String[] { "39" });

                        boot.put("postLogoCommands", new LinkedHashMap<>());

                        boot.get("postLogoCommands")
                                        .put("setScreenOff", null);

                        boot.get("postLogoCommands")
                                        .put("consoleSetTextMapPtr", new String[] { "0x6800" });

                        boot.get("postLogoCommands")
                                        .put("consoleSetTextGfxPtr", new String[] { "0x3000" });

                        boot.get("postLogoCommands")
                                        .put("consoleSetTextOffset", new String[] { "0x0100" });

                        boot.get("postLogoCommands")
                                        .put("consoleInitText", new String[] {
                                                        "0", "16 * 2", "&tilfont", "&palfont"
                                        });

                        boot.get("postLogoCommands")
                                        .put("bgSetGfxPtr", new String[] {
                                                        "0", "0x2000"
                                        });

                        boot.get("postLogoCommands")
                                        .put("bgSetMapPtr", new String[] {
                                                        "0", "0x6800", "SC_32x32"
                                        });

                        boot.get("postLogoCommands")
                                        .put("setScreenOn", null);

                        // Load BRR file
                        boot.get("postLogoCommands")
                                        .put("spcSetSoundEntry", new String[] {
                                                        "15", "15", "4", "&soundbrr_end - &soundbrr", "&soundbrr",
                                                        "&tadasound"
                                        });

                        return boot;

                }

                public static Make generateMakefile() {

                        return new Make();

                }

                public static void addMakeRules(Make makefile) {

                        Make.MakeRule textFont = new Make.MakeRule(
                                        "pvsneslibfont.pic",
                                        "pvsneslibfont.png",
                                        "$(GFXCONV) -s 8 -o 16 -u 16 -p -e 0 -i $<");

                        Make.MakeRule bitmaps = new Make.MakeRule(
                                        "bitmaps",
                                        "pvsneslibfont.pic pvsneslibfont.pal",
                                        "");

                        // Add Make Rule to build BRR files

                        Make.MakeRule soundbrr = new Make.MakeRule(
                                        "tada.brr",
                                        "tada.wav",
                                        "$(BRCONV) -e $< $@");

                        Make.MakeRule sounds = new Make.MakeRule(
                                        "sounds",
                                        "tada.brr",
                                        "");

                        makefile.addRule(textFont);
                        makefile.addRule(bitmaps);
                        makefile.addRule(soundbrr);
                        makefile.addRule(sounds);
                        makefile.addPhonyTarget("bitmaps");
                        makefile.addPhonyTarget("sounds");

                        // Add sounds rule to all rule
                        makefile.getRule("all").setPrerequisites(
                                        makefile.getRule("all").getPrerequisites() + " sounds bitmaps $(ROMNAME).sfc");

                }

                public static void build(App.Builder app) throws Exception {

                        Path actualPath = Paths.get(
                                        TadaExample.class.getProtectionDomain().getCodeSource().getLocation().toURI())
                                        .normalize().toAbsolutePath().getParent();

                        Path fontDataPath = actualPath.resolve("data").resolve("pvsneslibfont.png");

                        // Add WAV file to copy to the destination
                        Path soundDataPath = actualPath.resolve("data").resolve("tada.wav");

                        Path ouptutPath = actualPath.resolve("output");

                        cleanBuild(ouptutPath);

                        app.addDataToCopy(fontDataPath.toString());
                        app.addDataToCopy(soundDataPath.toString());

                        app.setDestination(ouptutPath.toString());

                        app.build();

                }

                public static void cleanBuild(Path directory) throws IOException {

                        if (Files.exists(directory)) {

                                Files.walk(directory)
                                                .sorted(Comparator.reverseOrder())
                                                .map(Path::toFile)
                                                .forEach(File::delete);

                                Files.createDirectories(directory);

                        }

                }

        }

}
