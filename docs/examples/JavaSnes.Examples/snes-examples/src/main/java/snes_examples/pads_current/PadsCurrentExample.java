package snes_examples.pads_current;

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
import javasnes.util.keywords.KeyWords;
import javasnes.util.logic.SnesSwitch;
import javasnes.util.operators.SnesOperator;
import javasnes.util.operators.assign.OperatorAssign;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.data.SnesVoid;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU16;

public class PadsCurrentExample {

    final static SnesChar CHAR = new SnesChar("char");
    final static SnesVoid VOID = new SnesVoid();

    public static void main(String[] args) throws Exception {

        App.Builder padsCurrentExample = Config.generateApp();

        HashMap<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "PadsCurrentExample   ");
        MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

        padsCurrentExample.setMemoryMapping(memMap);

        AppData appData = Config.generateAppData();
        appData.registerData(new Data("tilfont", "pvsneslibfont.pic", false), (byte) 2);
        appData.registerData(new Data("palfont", "pvsneslibfont.pal", false), (byte) 2);

        padsCurrentExample.setAppData(appData);

        Boot boot = Config.generateBoot();

        padsCurrentExample.setBoot(boot);

        SnesInstruction[] globalDefs = new SnesInstruction[2];

        String[] loadExtern = {"tilfont", "palfont"};

        globalDefs[0] = new SnesLoadExtern(loadExtern, CHAR);
        globalDefs[1] = new SnesU16("pads", "0");

        padsCurrentExample.setGlobalInstructions(globalDefs);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[1];

        processes[0] = changeTextWithPadPress();
        processor.addProcess(processes[0], null);

        padsCurrentExample.setSnesProcesses(processes);
        padsCurrentExample.setProcessor(processor);

        Make makefile = Config.generateMakefile();
        makefile.setRomName("JavaSnes_PadsCurrentExample");
        Config.addMakeRules(makefile);

        padsCurrentExample.setMakefile(makefile);

        Config.build(padsCurrentExample);

    }

    /**
     * This function generates a SnesProcess that changes the text on the screen
     * based on the current state of the pads. The process first gets the
     * current state of the pads using the padsCurrent function, and then uses a
     * switch statement to determine which text to display based on the current
     * state of the pads. The process then displays the text on the screen at
     * position (5, 5) using the consoleDrawText function.
     *
     * @return a SnesProcess that changes the text on the screen based on the
     * current state of the pads
     */
    public static SnesProcess changeTextWithPadPress() {

        SnesInstruction[] commands = new SnesInstruction[2];

        SnesU16 pads = new SnesU16("pads");

        SnesOperator getPadCurrent = new OperatorAssign(
                pads.name, SnesInput.padsCurrent((byte) 0).sourceCode
        );

        commands[0] = getPadCurrent;

        Map<String, List<SnesInstruction>> cases = new LinkedHashMap<>();

        List<SnesInstruction> caseA = new ArrayList<>();
        List<SnesInstruction> caseB = new ArrayList<>();
        List<SnesInstruction> caseX = new ArrayList<>();
        List<SnesInstruction> caseY = new ArrayList<>();
        List<SnesInstruction> caseStart = new ArrayList<>();
        List<SnesInstruction> caseSelect = new ArrayList<>();
        List<SnesInstruction> caseUp = new ArrayList<>();
        List<SnesInstruction> caseDown = new ArrayList<>();
        List<SnesInstruction> caseLeft = new ArrayList<>();
        List<SnesInstruction> caseRight = new ArrayList<>();
        List<SnesInstruction> caseL = new ArrayList<>();
        List<SnesInstruction> caseR = new ArrayList<>();

        caseA.add(SnesOutput.consoleDrawText(5, 5, "A!     ", null));
        caseB.add(SnesOutput.consoleDrawText(5, 5, "B!     ", null));
        caseX.add(SnesOutput.consoleDrawText(5, 5, "X!     ", null));
        caseY.add(SnesOutput.consoleDrawText(5, 5, "Y!     ", null));
        caseStart.add(SnesOutput.consoleDrawText(5, 5, "Start! ", null));
        caseSelect.add(SnesOutput.consoleDrawText(5, 5, "Select!", null));
        caseUp.add(SnesOutput.consoleDrawText(5, 5, "Up!    ", null));
        caseDown.add(SnesOutput.consoleDrawText(5, 5, "Down!  ", null));
        caseLeft.add(SnesOutput.consoleDrawText(5, 5, "Left!  ", null));
        caseRight.add(SnesOutput.consoleDrawText(5, 5, "Right! ", null));
        caseL.add(SnesOutput.consoleDrawText(5, 5, "L!     ", null));
        caseR.add(SnesOutput.consoleDrawText(5, 5, "R!     ", null));

        caseA.add(KeyWords.snesBreak);
        caseB.add(KeyWords.snesBreak);
        caseX.add(KeyWords.snesBreak);
        caseY.add(KeyWords.snesBreak);
        caseStart.add(KeyWords.snesBreak);
        caseSelect.add(KeyWords.snesBreak);
        caseUp.add(KeyWords.snesBreak);
        caseDown.add(KeyWords.snesBreak);
        caseLeft.add(KeyWords.snesBreak);
        caseRight.add(KeyWords.snesBreak);
        caseL.add(KeyWords.snesBreak);
        caseR.add(KeyWords.snesBreak);

        cases.put(SnesInput.keys.KEY_A.sourceCode, caseA);
        cases.put(SnesInput.keys.KEY_B.sourceCode, caseB);
        cases.put(SnesInput.keys.KEY_X.sourceCode, caseX);
        cases.put(SnesInput.keys.KEY_Y.sourceCode, caseY);
        cases.put(SnesInput.keys.KEY_START.sourceCode, caseStart);
        cases.put(SnesInput.keys.KEY_SELECT.sourceCode, caseSelect);
        cases.put(SnesInput.keys.KEY_UP.sourceCode, caseUp);
        cases.put(SnesInput.keys.KEY_DOWN.sourceCode, caseDown);
        cases.put(SnesInput.keys.KEY_LEFT.sourceCode, caseLeft);
        cases.put(SnesInput.keys.KEY_RIGHT.sourceCode, caseRight);
        cases.put(SnesInput.keys.KEY_L.sourceCode, caseL);
        cases.put(SnesInput.keys.KEY_R.sourceCode, caseR);

        SnesSwitch switchKey = new SnesSwitch(pads, cases, null);

        switchKey.generateSourceCode();

        commands[1] = switchKey;

        SnesProcess process = new SnesProcess("changeTextWithPadPress", commands, VOID);

        return process;

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

            return boot;

        }

        public static Make generateMakefile() {

            return new Make();

        }

        public static void addMakeRules(Make makefile) {

            Make.MakeRule textFont = new Make.MakeRule(
                    "pvsneslibfont.pic",
                    "pvsneslibfont.png",
                    "$(GFXCONV) -s 8 -o 16 -u 16 -p -e 0 -i $<"
            );

            Make.MakeRule bitmaps = new Make.MakeRule(
                    "bitmaps",
                    "pvsneslibfont.pic pvsneslibfont.pal",
                    ""
            );

            makefile.addRule(textFont);
            makefile.addRule(bitmaps);
            makefile.addPhonyTarget("bitmaps");

            makefile.getRule("all").setPrerequisites(
                    makefile.getRule("all").getPrerequisites() + " bitmaps $(ROMNAME).sfc"
            );

        }

        public static void build(App.Builder app) throws Exception {

            Path actualPath = Paths.get(
                    PadsCurrentExample.class.getProtectionDomain().getCodeSource().getLocation().toURI()
            ).normalize().toAbsolutePath().getParent();

            Path dataPath = actualPath.resolve("data").resolve("pvsneslibfont.png");
            Path ouptutPath = actualPath.resolve("output");

            cleanBuild(ouptutPath);

            app.addDataToCopy(dataPath.toString());
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
