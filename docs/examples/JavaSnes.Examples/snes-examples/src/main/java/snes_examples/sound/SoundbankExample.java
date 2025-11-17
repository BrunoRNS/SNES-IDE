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
import javasnes.instruction.SnesInstruction;
import javasnes.instruction.SnesRawInstruction;
import javasnes.makefile.Make;
import javasnes.output.SnesOutput;
import javasnes.sneslib.SnesSound;
import javasnes.util.logic.SnesElse;
import javasnes.util.logic.SnesIf;
import javasnes.util.macros.SnesInclude;
import javasnes.util.operators.SnesOperator;
import javasnes.util.operators.assign.OperatorAssign;
import javasnes.util.operators.logical.OperatorAnd;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU16;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU8;

public class SoundbankExample {

    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {

        App.Builder soundbankExample = Config.generateApp();

        Map<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "SoundbankExample     ");

        MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

        soundbankExample.setMemoryMapping(memMap);

        AppData appData = Config.generateAppData();
        appData.registerData(new Data("tilfont", "pvsneslibfont.pic", false), (byte) 2);
        appData.registerData(new Data("palfont", "pvsneslibfont.pal", false), (byte) 2);

        soundbankExample.setAppData(appData);

        Boot boot = Config.generateBoot();
        soundbankExample.setBoot(boot);

        soundbankExample.addSnesMacro(new SnesInclude("\"soundbank.h\""));

        SnesInstruction[] globalDefs = new SnesInstruction[5];

        String[] loadExternFont = {"tilfont", "palfont"};
        globalDefs[0] = new SnesLoadExtern(loadExternFont, CHAR);

        String[] loadExternBank = {"SOUNDBANK__"};
        globalDefs[1] = new SnesLoadExtern(loadExternBank, CHAR);

        globalDefs[2] = new SnesU16("bgColor", "128");
        globalDefs[3] = new SnesU8("keyapressed", "0");
        globalDefs[4] = new SnesU8("keybpressed", "0");

        soundbankExample.setGlobalInstructions(globalDefs);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[3];

        processes[0] = pauseMusic();
        processor.addProcess(processes[0], null);

        processes[1] = resumeMusic();
        processor.addProcess(processes[1], null);

        processes[2] = updateScreen();
        processor.addProcess(processes[2], null);

        soundbankExample.setProcessor(processor);
        soundbankExample.setSnesProcesses(processes);

        Make makefile = Config.generateMakefile();

        makefile.setRomName("JavaSnes_SoundbankExample");

        makefile.addHeaderLine("AUDIOFILES := pollen8.it");
        makefile.addHeaderLine("export SOUNDBANK := soundbank");

        makefile.addVariable("SMCONVFLAGS", "-s -o $(SOUNDBANK) -V -b 5");

        makefile.addRule(new Make.MakeRule("musics", "$(SOUNDBANK).obj"));

        Config.addMakeRules(makefile);

        soundbankExample.setMakefile(makefile);

        Config.build(soundbankExample);

    }

    /**
     * Returns a SnesProcess that pauses all sound channels if the A key is
     * pressed.
     *
     * @return A process that pauses all sound channels if the A key is pressed.
     */
    public static SnesProcess pauseMusic() {

        SnesInstruction[] commands = new SnesInstruction[1];

        List<SnesInstruction> ifNotPressedCommands = new ArrayList<>();

        ifNotPressedCommands.add(new OperatorAssign("keyapressed", "0"));

        SnesElse ifNotPressed = new SnesElse(ifNotPressedCommands);

        List<SnesInstruction> ifPressedCommands = new ArrayList<>();

        ifPressedCommands.add(new OperatorAssign("keyapressed", "1"));
        ifPressedCommands.add(SnesSound.spcPauseMusic());

        SnesOperator ifPressed = new OperatorAnd("padsCurrent(0) & KEY_A", "keyapressed == 0");

        SnesIf ifStatement = new SnesIf(ifPressed, ifPressedCommands, ifNotPressed);

        ifStatement.generateSourceCode();

        commands[0] = ifStatement;

        return new SnesProcess("pauseMusic", (byte) 0, commands);

    }

    /**
     * Returns a SnesProcess that resumes all sound channels if the B key is
     * pressed.
     *
     * @return A process that resumes all sound channels if the B key is
     * pressed.
     */
    public static SnesProcess resumeMusic() {

        SnesInstruction[] commands = new SnesInstruction[1];

        List<SnesInstruction> ifNotPressedCommands = new ArrayList<>();

        ifNotPressedCommands.add(new OperatorAssign("keybpressed", "0"));

        SnesElse ifNotPressed = new SnesElse(ifNotPressedCommands);

        List<SnesInstruction> ifPressedCommands = new ArrayList<>();

        ifPressedCommands.add(new OperatorAssign("keybpressed", "1"));
        ifPressedCommands.add(SnesSound.spcResumeMusic());

        SnesOperator ifPressed = new OperatorAnd("padsCurrent(0) & KEY_B", "keybpressed == 0");

        SnesIf ifStatement = new SnesIf(ifPressed, ifPressedCommands, ifNotPressed);

        ifStatement.generateSourceCode();

        commands[0] = ifStatement;

        return new SnesProcess("resumeMusic", (byte) 0, commands);

    }

    /**
     * Returns a SnesProcess that updates the screen by processing sound
     * messages, waiting for VBlank, incrementing the background color, and
     * drawing text to the console.
     *
     * @return A process that updates the screen as described above.
     */
    public static SnesProcess updateScreen() {

        SnesInstruction[] commands = new SnesInstruction[7];

        SnesU16 bgColor = new SnesU16("bgColor");

        commands[0] = SnesSound.spcProcess();
        commands[1] = SnesOutput.waitForVblank();

        commands[2] = new SnesRawInstruction("bgColor++;");
        commands[3] = SnesOutput.setPaletteColor("0x00", bgColor);

        commands[4] = SnesOutput.consoleDrawText(5, 10, "Let's the music play !", null);
        commands[5] = SnesOutput.consoleDrawText(5, 12, "    A to PAUSE       ", null);
        commands[6] = SnesOutput.consoleDrawText(5, 13, "    B to RESUME      ", null);

        return new SnesProcess("updateScreen", (byte) 0, commands);

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

            boot.get("betweenSPCVRAMLoadCommands")
                    .put("spcSetBank", new String[]{"&SOUNDBANK__"});

            boot.get("betweenSPCVRAMLoadCommands")
                    .put("spcLoad", new String[]{"MOD_POLLEN8"});

            boot.put("postLogoCommands", new LinkedHashMap<>());

            boot.get("postLogoCommands")
                    .put("setScreenOff", null);

            boot.get("postLogoCommands")
                    .put("consoleSetTextMapPtr", new String[]{"0x6800"});

            boot.get("postLogoCommands")
                    .put("consoleSetTextGfxPtr", new String[]{"0x3000"});

            boot.get("postLogoCommands")
                    .put("consoleSetTextOffset", new String[]{"0x0100"});

            boot.get("postLogoCommands")
                    .put("consoleInitText", new String[]{
                "0", "16 * 2", "&tilfont", "&palfont"
            });

            boot.get("postLogoCommands")
                    .put("bgSetGfxPtr", new String[]{
                "0", "0x2000"
            });

            boot.get("postLogoCommands")
                    .put("bgSetMapPtr", new String[]{
                "0", "0x6800", "SC_32x32"
            });

            boot.get("postLogoCommands")
                    .put("setScreenOn", null);

            boot.get("postLogoCommands")
                    .put("spcPlay", new String[]{
                "0"
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

            makefile.addRule(textFont);
            makefile.addRule(bitmaps);
            makefile.addPhonyTarget("bitmaps");
            makefile.addPhonyTarget("musics");

            makefile.getRule("all").setPrerequisites(
                    makefile.getRule("all").getPrerequisites() + " musics bitmaps $(ROMNAME).sfc");

        }

        public static void build(App.Builder app) throws Exception {

            Path actualPath = Paths.get(
                    SoundbankExample.class.getProtectionDomain().getCodeSource().getLocation().toURI()).normalize()
                    .toAbsolutePath().getParent();

            Path fontDataPath = actualPath.resolve("data").resolve("pvsneslibfont.png");

            // Add IT file to copy to the destination
            Path soundDataPath = actualPath.resolve("data").resolve("pollen8.it");

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
