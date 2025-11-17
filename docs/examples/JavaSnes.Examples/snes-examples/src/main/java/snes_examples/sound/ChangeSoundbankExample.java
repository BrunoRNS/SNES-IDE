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
import javasnes.util.operators.logical.OperatorEquals;
import javasnes.util.operators.logical.OperatorOr;
import javasnes.util.operators.ternary.OperatorTernary;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.array.data.SnesCharArray;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.number.signed.SnesS8;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU16;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU8;

public class ChangeSoundbankExample {

    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {

        App.Builder changeSoundbankExample = Config.generateApp();

        Map<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "ChangSoundbankExample");

        MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

        changeSoundbankExample.setMemoryMapping(memMap);

        AppData appData = Config.generateAppData();
        appData.registerData(new Data("tilfont", "pvsneslibfont.pic", false), (byte) 2);
        appData.registerData(new Data("palfont", "pvsneslibfont.pal", false), (byte) 2);

        changeSoundbankExample.setAppData(appData);

        Boot boot = Config.generateBoot();
        changeSoundbankExample.setBoot(boot);

        changeSoundbankExample.addSnesMacro(new SnesInclude("\"soundbank.h\""));

        SnesInstruction[] globalDefs = new SnesInstruction[6];

        String[] loadExternFont = {"tilfont", "palfont"};
        globalDefs[0] = new SnesLoadExtern(loadExternFont, CHAR);

        String[] loadExternBank = {"SOUNDBANK__0", "SOUNDBANK__1", "SOUNDBANK__2"};
        globalDefs[1] = new SnesLoadExtern(loadExternBank, CHAR);

        globalDefs[2] = new SnesU16("bgColor", "128");
        globalDefs[3] = new SnesU8("keyapressed", "0");
        globalDefs[4] = new SnesU8("keybpressed", "0");

        // -2 - changed to pollen, -1 - not changed(is pollen)
        // 1 - not changed(is whatislove), 2 - changed to whatislove
        globalDefs[5] = new SnesS8("changed", "-1");

        changeSoundbankExample.setGlobalInstructions(globalDefs);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[3];

        processes[0] = changeToPollen8();
        processor.addProcess(processes[0], null);

        processes[1] = changeToWhatisLove();
        processor.addProcess(processes[1], null);

        processes[2] = updateScreen();
        processor.addProcess(processes[2], null);

        changeSoundbankExample.setProcessor(processor);
        changeSoundbankExample.setSnesProcesses(processes);

        Make makefile = Config.generateMakefile();

        makefile.setRomName("JavaSnes_ChangeSoundbankExample");

        makefile.addHeaderLine("AUDIOFILES := pollen8.it whatislove.it");
        makefile.addHeaderLine("export SOUNDBANK := soundbank");

        makefile.addVariable("SMCONVFLAGS", "-s -o $(SOUNDBANK) -V -b 5");

        makefile.addRule(new Make.MakeRule("musics", "$(SOUNDBANK).obj"));

        Config.addMakeRules(makefile);

        changeSoundbankExample.setMakefile(makefile);

        Config.build(changeSoundbankExample);

    }

    /**
     * Returns a SnesProcess that changes the soundbank to whatislove if the A
     * key is pressed. The process first assigns the current pad state to a
     * variable of "padsCurrent". Then, it checks if the A key is pressed by
     * checking the value of the "keyapressed" variable. If the A key is
     * pressed, it sets "keyapressed" to 1 and "changed" to 2. If the A key is
     * not pressed, it sets "keyapressed" to 0.
     *
     * @return a SnesProcess that changes the soundbank to whatislove if the A
     * key is pressed.
     */
    public static SnesProcess changeToWhatisLove() {

        SnesInstruction[] commands = new SnesInstruction[1];

        List<SnesInstruction> ifNotPressedCommands = new ArrayList<>();

        ifNotPressedCommands.add(new OperatorAssign("keyapressed", "0"));

        SnesElse ifNotPressed = new SnesElse(ifNotPressedCommands);

        List<SnesInstruction> ifPressedCommands = new ArrayList<>();

        ifPressedCommands.add(new OperatorAssign("keyapressed", "1"));
        ifPressedCommands.add(new OperatorAssign("changed", "2"));

        SnesOperator ifPressed = new OperatorAnd("padsCurrent(0) & KEY_A", "keyapressed == 0");

        SnesIf ifStatement = new SnesIf(ifPressed, ifPressedCommands, ifNotPressed);

        ifStatement.generateSourceCode();

        commands[0] = ifStatement;

        return new SnesProcess("changeToWhatisLove", (byte) 0, commands);

    }

    /**
     * Returns a SnesProcess that changes the soundbank to Pollen8 if the B key
     * is pressed. The process first assigns the current pad state to a variable
     * "padsCurrent". Then, it checks if the B key is pressed by checking the
     * value of the "keybpressed" variable. If the B key is pressed, it changes
     * the soundbank to Pollen8 and sets the "changed" variable to -2. If the B
     * key is not pressed, it sets the "keybpressed" variable to 0.
     *
     * @return a SnesProcess that changes the soundbank to Pollen8 if the B key
     * is pressed.
     */
    public static SnesProcess changeToPollen8() {

        SnesInstruction[] commands = new SnesInstruction[1];

        List<SnesInstruction> ifNotPressedCommands = new ArrayList<>();

        ifNotPressedCommands.add(new OperatorAssign("keybpressed", "0"));

        SnesElse ifNotPressed = new SnesElse(ifNotPressedCommands);

        List<SnesInstruction> ifPressedCommands = new ArrayList<>();

        ifPressedCommands.add(new OperatorAssign("keybpressed", "1"));
        ifPressedCommands.add(new OperatorAssign("changed", "-2"));

        SnesOperator ifPressed = new OperatorAnd("padsCurrent(0) & KEY_B", "keybpressed == 0");

        SnesIf ifStatement = new SnesIf(ifPressed, ifPressedCommands, ifNotPressed);

        ifStatement.generateSourceCode();

        commands[0] = ifStatement;

        return new SnesProcess("changeToPollen8", (byte) 0, commands);

    }

    /**
     * Returns a SnesProcess that updates the screen by processing sound
     * messages, waiting for VBlank, incrementing the background color, and
     * drawing text to the console. If the soundbank has been changed to
     * WHATISLOVE or POLLEN8, it loads the corresponding the new soundbank and
     * plays the music. If the soundbank has not been changed, it simply
     * processes the sound messages and waits for VBlank.
     *
     * @return a SnesProcess that updates the screen as described above.
     */
    public static SnesProcess updateScreen() {

        SnesInstruction[] commands = new SnesInstruction[8];

        SnesU16 bgColor = new SnesU16("bgColor");

        List<SnesInstruction> ifChangedCommands = new ArrayList<>();

        ifChangedCommands.add(SnesSound.spcLoad(
                new OperatorTernary(
                        new OperatorEquals("changed", "2"),
                        new SnesCharArray("MOD_WHATISLOVE", (short) 14),
                        new SnesCharArray("MOD_POLLEN8", (short) 11)
                ).getSourceCode()
        ));

        ifChangedCommands.add(SnesSound.spcPlay(0));
        ifChangedCommands.add(new OperatorAssign("changed", "2", '/'));

        SnesOperator ifChanged = new OperatorOr("changed == -2", "changed == 2");

        SnesIf ifStatement = new SnesIf(ifChanged, ifChangedCommands);

        ifStatement.generateSourceCode();

        commands[0] = ifStatement;

        commands[1] = SnesSound.spcProcess();
        commands[2] = SnesOutput.waitForVblank();

        commands[3] = new SnesRawInstruction("bgColor++;");
        commands[4] = SnesOutput.setPaletteColor("0x00", bgColor);

        commands[5] = SnesOutput.consoleDrawText(5, 10, "Let's the music play !", null);
        commands[6] = SnesOutput.consoleDrawText(5, 12, "    A to WHATISLOVE   ", null);
        commands[7] = SnesOutput.consoleDrawText(5, 13, "    B to POLLEN8      ", null);

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
                    .put("spcSetBank", new String[]{"&SOUNDBANK__2"});

            boot.get("betweenSPCVRAMLoadCommands")
                    .put("spcSetBank", new String[]{"&SOUNDBANK__1"});

            boot.get("betweenSPCVRAMLoadCommands")
                    .put("spcSetBank", new String[]{"&SOUNDBANK__0"});

            // Begin with MOD_POLLEN8
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
                    ChangeSoundbankExample.class.getProtectionDomain().getCodeSource().getLocation().toURI()).normalize()
                    .toAbsolutePath().getParent();

            Path fontDataPath = actualPath.resolve("data").resolve("pvsneslibfont.png");

            // Add IT files to copy to the destination
            Path soundDataPath1 = actualPath.resolve("data").resolve("pollen8.it");
            Path soundDataPath2 = actualPath.resolve("data").resolve("whatislove.it");

            Path ouptutPath = actualPath.resolve("output");

            cleanBuild(ouptutPath);

            app.addDataToCopy(fontDataPath.toString());
            app.addDataToCopy(soundDataPath1.toString());
            app.addDataToCopy(soundDataPath2.toString());

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
