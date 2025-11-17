package snes_examples.sram;

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
import javasnes.sneslib.SnesUtilities;
import javasnes.util.logic.SnesElseIf;
import javasnes.util.logic.SnesIf;
import javasnes.util.operators.SnesOperator;
import javasnes.util.operators.assign.OperatorAssign;
import javasnes.util.operators.binary.OperatorBinAnd;
import javasnes.util.operators.unitary.OperatorCast;
import javasnes.util.operators.unitary.OperatorMemAdress;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.pointer.number.signed.SnesS32Pointer;
import javasnes.util.types.vars.pointer.number.unsigned.SnesU8Pointer;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.data.SnesVoid;
import javasnes.util.types.vars.scalar.number.signed.SnesS32;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU16;

public class SramSaveLoadExample {

    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {

        App.Builder sramSaveLoadExample = Config.generateApp();

        HashMap<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "SramSaveLoadExample  ");
        memMapConfig.put("cartridgeType", "$02");
        memMapConfig.put("sramsize", "$01");

        MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

        sramSaveLoadExample.setMemoryMapping(memMap);

        AppData appData = Config.generateAppData();
        appData.registerData(new Data("tilfont", "pvsneslibfont.pic", false), (byte) 2);
        appData.registerData(new Data("palfont", "pvsneslibfont.pal", false), (byte) 2);
        
        sramSaveLoadExample.setAppData(appData);

        Boot boot = Config.generateBoot();

        sramSaveLoadExample.setBoot(boot);

        SnesInstruction[] globalDefs = new SnesInstruction[3];

        String[] loadExtern = {"tilfont", "palfont"};
        globalDefs[0] = new SnesLoadExtern(loadExtern, CHAR);
        globalDefs[1] = new SnesU16("pads", "0");
        globalDefs[2] = new SnesS32("loadedValue", "0");

        sramSaveLoadExample.setGlobalInstructions(globalDefs);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[3];

        processes[0] = saveGame();
        processes[1] = loadGame();
        processes[2] = addOrsubValue();

        for (SnesProcess process : processes) {

            processor.addProcess(process, null);

        }

        sramSaveLoadExample.setSnesProcesses(processes);
        sramSaveLoadExample.setProcessor(processor);

        Make makefile = Config.generateMakefile();
        makefile.setRomName("JavaSnes_SramSaveLoadExample");

        Config.addMakeRules(makefile);
        
        sramSaveLoadExample.setMakefile(makefile);

        Config.build(sramSaveLoadExample);

    }

    /**
     * Generates a SnesProcess that saves a game from SRAM. The generated
     * process first checks if the B button is being pressed. If the B button is
     * being pressed, it saves the game from SRAM.
     *
     * @return a SnesProcess that saves a game from SRAM
     */
    public static SnesProcess saveGame() {

        SnesInstruction[] commands = new SnesInstruction[2];

        SnesOperator assignPads = new OperatorAssign(
            "pads", SnesInput.padsCurrent((byte) 0).sourceCode
        );

        commands[0] = assignPads;

        SnesU16 pads = new SnesU16("pads");
        SnesS32 loadedValue = new SnesS32("loadedValue");

        SnesOperator whetherToSaveOrNot = new OperatorBinAnd(
            pads, new SnesU16(SnesInput.keys.KEY_B.sourceCode)
        );

        List<SnesInstruction> ifSaveCommands = new ArrayList<>();
        
        final SnesU8Pointer U8POINTER = new SnesU8Pointer("u8*");
        U8POINTER.type = "u8*";

        SnesOperator castLoadedValue = new OperatorCast(
            U8POINTER, new SnesS32Pointer((new OperatorMemAdress(loadedValue)).getSourceCode())
        );
        
        SnesInstruction assignToValue = SnesUtilities.consoleCopySram(
            castLoadedValue.getSourceCode(), "4" // 32 bits = 4 bytes
        );

        ifSaveCommands.add(assignToValue);

        SnesIf ifSave = new SnesIf(whetherToSaveOrNot, ifSaveCommands);

        ifSave.generateSourceCode();

        commands[1] = ifSave;

        return new SnesProcess("saveGame", (byte) 0, commands);

    }

    /**
     * Generates a SnesProcess that loads a game from SRAM.
     * The generated process first checks if the A button is being pressed.
     * If the A button is being pressed, it loads the game from SRAM.
     * 
     * @return a SnesProcess that loads a game from SRAM
    */
    public static SnesProcess loadGame() {

        SnesInstruction[] commands = new SnesInstruction[2];

        SnesOperator assignPads = new OperatorAssign(
            "pads", SnesInput.padsCurrent((byte) 0).sourceCode
        );

        commands[0] = assignPads;

        SnesU16 pads = new SnesU16("pads");
        SnesS32 loadedValue = new SnesS32("loadedValue");

        SnesOperator whetherToLoadOrNot = new OperatorBinAnd(
            pads, new SnesU16(SnesInput.keys.KEY_A.sourceCode)
        );

        List<SnesInstruction> ifLoadCommands = new ArrayList<>();
        
        final SnesU8Pointer U8POINTER = new SnesU8Pointer("u8*");
        U8POINTER.type = "u8*";

        SnesOperator castLoadedValue = new OperatorCast(
            U8POINTER, new SnesS32Pointer((new OperatorMemAdress(loadedValue)).getSourceCode())
        );
        
        SnesInstruction assignToValue = SnesUtilities.consoleLoadSram(
            castLoadedValue.getSourceCode(), "4" // 32 bits = 4 bytes
        );

        ifLoadCommands.add(assignToValue);

        SnesIf ifLoad = new SnesIf(whetherToLoadOrNot, ifLoadCommands);

        ifLoad.generateSourceCode();

        commands[1] = ifLoad;

        return new SnesProcess("loadGame", (byte) 0, commands);

    }

    /**
     * Generates a SnesProcess that adds or subtracts 1 from a loaded value depending on whether the up or down button is pressed.
     * The generated process first checks if the up button is being pressed.
     * If the up button is being pressed, it adds 1 to the loaded value.
     * If the down button is being pressed, it subtracts 1 from the loaded value.
     * Finally, the generated process prints out the value of the loaded value.
     * 
     * @return a SnesProcess that adds or subtracts 1 from a loaded value depending on whether the up or down button is pressed.
     */
    public static SnesProcess addOrsubValue() {

        SnesInstruction[] commands = new SnesInstruction[5];

        SnesOperator assignPads = new OperatorAssign(
            "pads", SnesInput.padsCurrent((byte) 0).sourceCode
        );

        commands[0] = assignPads;

        SnesS32 loadedValue = new SnesS32("loadedValue");

        SnesOperator upIsPressed = new OperatorBinAnd(
            new SnesU16("pads"), new SnesU16(SnesInput.keys.KEY_UP.sourceCode)
        );

        SnesOperator downIsPressed = new OperatorBinAnd(
            new SnesU16("pads"), new SnesU16(SnesInput.keys.KEY_DOWN.sourceCode)
        );

        List<SnesInstruction> ifUpCommands = new ArrayList<>();
        SnesOperator addToLoadedValue = new OperatorAssign(loadedValue.name, "1", '+');

        ifUpCommands.add(addToLoadedValue);

        List<SnesInstruction> ifDownCommands = new ArrayList<>();
        SnesOperator subToLoadedValue = new OperatorAssign(loadedValue.name, "1", '-');

        ifDownCommands.add(subToLoadedValue);

        List<SnesElseIf> elseIfStatements = new ArrayList<>();
        SnesElseIf ifDown = new SnesElseIf(downIsPressed, ifDownCommands);

        elseIfStatements.add(ifDown);

        SnesIf ifUp = new SnesIf(
            upIsPressed, ifUpCommands, elseIfStatements
        );

        ifUp.generateSourceCode();

        commands[1] = ifUp;

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesOperator castLoadedValue = new OperatorCast(
            INT, loadedValue
        );

        commands[2] = SnesOutput.consoleDrawText(
            0, 2, "Press Up or Down to add or sub 1", null
        );

        commands[3] = SnesOutput.consoleDrawText(
            0, 4, "Press A to load, B to save value", null
        );

        commands[4] = SnesOutput.consoleDrawText(
            4, 8, "Value: %d        ", ", " + castLoadedValue.getSourceCode()
        );

        return new SnesProcess("addOrsubValue", (byte) 0, commands);

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

            // Set default value of SRAM to 0
            boot.get("postLogoCommands")
                    .put("consoleCopySram", new String[] {"(u8 *) &loadedValue", "4"});

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
                    SramSaveLoadExample.class.getProtectionDomain().getCodeSource().getLocation().toURI()
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
