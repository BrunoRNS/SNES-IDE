package snes_examples.background;

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
import javasnes.util.logic.SnesIf;
import javasnes.util.logic.SnesSwitch;
import javasnes.util.operators.SnesOperator;
import javasnes.util.operators.assign.OperatorAssign;
import javasnes.util.operators.binary.OperatorBinAnd;
import javasnes.util.operators.logical.OperatorEquals;
import javasnes.util.operators.math.OperatorAdd;
import javasnes.util.operators.ternary.OperatorTernary;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU16;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU8;

public class ChangeBackgroundExample {

    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {
        
        App.Builder changeBackgroundApp = Config.generateApp();

        Map<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "ChanBackgroundExample");

        changeBackgroundApp.setMemoryMapping(Config.generateMemoryMapping(memMapConfig));

        AppData appData = Config.generateAppData();

        /**
         * Registering data
         * 
         * 1 bank for each map's patterns
         * 1 bank for each map's palette and map
         * 
         */
        
        appData.registerData(new Data("patterns1", "map1.pic", true), (byte) 2);

        appData.registerData(new Data("palette1", "map1.pal", true), (byte) 3);
        appData.registerData(new Data("map1", "map1.map", true), (byte) 3);

        appData.registerData(new Data("patterns2", "map2.pic", true), (byte) 4);

        appData.registerData(new Data("palette2", "map2.pal", true), (byte) 5);
        appData.registerData(new Data("map2", "map2.map", true), (byte) 5);

        appData.registerData(new Data("patterns3", "map3.pic", true), (byte) 6);

        appData.registerData(new Data("palette3", "map3.pal", true), (byte) 7);
        appData.registerData(new Data("map3", "map3.map", true), (byte) 7);

        changeBackgroundApp.setAppData(appData);

        Boot boot = Config.generateBoot();
        changeBackgroundApp.setBoot(boot);

        SnesInstruction[] globalDefs = new SnesInstruction[2];

        String[] loadExtern = {
            "patterns1", "patterns1_end",
            "palette1", "palette1_end",
            "map1", "map1_end",
            "patterns2", "patterns2_end",
            "palette2", "palette2_end",
            "map2", "map2_end",
            "patterns3", "patterns3_end",
            "palette3", "palette3_end",
            "map3", "map3_end",
        };

        globalDefs[0] = new SnesLoadExtern(loadExtern, CHAR);

        // 0 for map 1, 1 for map 2, etc
        globalDefs[1] = new SnesU8("actualBackground", "0");

        changeBackgroundApp.setGlobalInstructions(globalDefs);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[1];

        processes[0] = changeToNextBackground();
        processor.addProcess(processes[0], null);

        changeBackgroundApp.setProcessor(processor);
        changeBackgroundApp.setSnesProcesses(processes);

        Make makefile = Config.generateMakefile();
        makefile.setRomName("JavaSnes_ChangeBackgroundExample");

        Config.addMakeRules(makefile);

        changeBackgroundApp.setMakefile(makefile);

        Config.build(changeBackgroundApp);

    }

    /**
     * Returns a SnesProcess that changes the background to the next one when the A key 
     * is pressed.
     * 
     * The process checks if the A key is currently being pressed, and if so, it increments 
     * the background counter.
     * The background counter is used to determine which background to load next. 
     * The background counter is reset to 0 when it reaches 2.
     * 
     * The process then sets the screen off and clears the VRAM.
     * 
     * Finally, the process uses a SnesSwitch to determine which background to load next 
     * based on the background counter.
     * The SnesSwitch has four cases: one for each background, and uses the background counter
     * to determine which case to execute.
     * 
     * @return a SnesProcess that changes the background to the next one when the A key is 
     * pressed.
     */
    public static SnesProcess changeToNextBackground() {

        SnesInstruction[] commands = new SnesInstruction[2];

        SnesU16 pads = new SnesU16("pads", SnesInput.padsCurrent((byte) 0).sourceCode);
        SnesU8 actualBackground = new SnesU8("actualBackground");

        commands[0] = pads;

        SnesOperator changeToNextBackground = new OperatorBinAnd(
            pads, new SnesU16(SnesInput.keys.KEY_A.sourceCode)
        );

        List<SnesInstruction> ifNextBackgroundCommands = new ArrayList<>();
        
        ifNextBackgroundCommands.add(
            new OperatorAssign(
                "actualBackground", new OperatorTernary(
                    new OperatorEquals("actualBackground", "2"),
                    new SnesU8("0"),
                    new SnesU8(
                        (new OperatorAdd(
                            new SnesU8("actualBackground"), new SnesU8("1")
                        )).getSourceCode()
                    )
                ).getSourceCode()
            )
        );

        ifNextBackgroundCommands.add(SnesOutput.setScreenOff());
        ifNextBackgroundCommands.add(SnesOutput.dmaClearVram());

        Map<String, List<SnesInstruction>> cases = new HashMap<>();

        List<SnesInstruction> case0 = new ArrayList<>();
        List<SnesInstruction> case1 = new ArrayList<>();
        List<SnesInstruction> case2 = new ArrayList<>();

        addToCase(case0, 1);
        addToCase(case1, 2);
        addToCase(case2, 3);
        
        cases.put("0", case0);
        cases.put("1", case1);
        cases.put("2", case2);

        SnesSwitch ifNextBackgroundCommandsSwitchBg = new SnesSwitch(actualBackground, cases);
        ifNextBackgroundCommandsSwitchBg.generateSourceCode();

        ifNextBackgroundCommands.add(ifNextBackgroundCommandsSwitchBg);

        SnesIf ifNextBackground = new SnesIf(
            changeToNextBackground, ifNextBackgroundCommands
        );

        ifNextBackground.generateSourceCode();

        commands[1] = ifNextBackground;

        return new SnesProcess("changeToNextBackground", (byte) 0, commands);

    }

    /**
     * Adds the necessary instructions to the given list of instructions to change to the map
     * with the given index.
     *
     * This method adds the following instructions to the given list of instructions:
     * 1. bgInitTileSet to initialize the tile set with the given index
     * 2. bgInitMapSet to initialize the map set with the given index
     * 3. setScreenOn to turn on the screen
     *
     * @param cases the list of instructions to add to
     * @param index the index of the map to change to
     */
    public static void addToCase(List<SnesInstruction> cases, int index) {

        cases.add(SnesOutput.bgInitTileSet(
            0, "&patterns" + index, "&palette" + index, "0",
            "(&patterns" + index + "_end - &patterns" + index + ")",
            "(&palette" + index + "_end - &palette" + index + ")",
            "BG_16COLORS", "0x4000"
        ));

        cases.add(SnesOutput.bgInitMapSet(
            0, "&map" + index, "(&map" + index + "_end - &map" + index + ")", "SC_32x32",
            "0x0000"
        ));

        cases.add(SnesOutput.setScreenOn());

        cases.add(KeyWords.snesBreak);

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

            // Only need to set the screen on, as we don't use the text engine in this example
            boot.get("postLogoCommands")
                    .put("setScreenOn", null);

            return boot;

        }

        public static Make generateMakefile() {

            return new Make();

        }

        public static void addMakeRules(Make makefile) {

            Make.MakeRule bg0 = new Make.MakeRule(
                "map1.map",
                "map1.bmp",
                "$(GFXCONV) -s 8 -o 16 -u 16 -e 0 -p -m -t bmp -i $<"
            );

            Make.MakeRule bg1 = new Make.MakeRule(
                "map2.map",
                "map2.bmp",
                "$(GFXCONV) -s 8 -o 16 -u 16 -e 0 -p -m -t bmp -i $<"
            );

            Make.MakeRule bg2 = new Make.MakeRule(
                "map3.map",
                "map3.bmp",
                "$(GFXCONV) -s 8 -o 16 -u 16 -e 0 -p -m -t bmp -i $<"
            );


            Make.MakeRule bitmaps = new Make.MakeRule(
                "bitmaps",
                "map1.map map1.pic map1.pal map2.map map2.pic map2.pal map3.map map3.pic map3.pal",
                ""
            );

            makefile.addRule(bg0);
            makefile.addRule(bg1);
            makefile.addRule(bg2);

            makefile.addRule(bitmaps);
            makefile.addPhonyTarget("bitmaps");

            makefile.getRule("all").setPrerequisites(
                    makefile.getRule("all").getPrerequisites() + " bitmaps $(ROMNAME).sfc"
            );

        }

        public static void build(App.Builder app) throws Exception {

            Path actualPath = Paths.get(
                    ChangeBackgroundExample.class.getProtectionDomain().getCodeSource().getLocation().toURI()
            ).normalize().toAbsolutePath().getParent();

            Path dataPath = actualPath.resolve("data");
            Path ouptutPath = actualPath.resolve("output");

            Path bg0 = dataPath.resolve("map1.bmp");
            Path bg1 = dataPath.resolve("map2.bmp");
            Path bg2 = dataPath.resolve("map3.bmp");

            cleanBuild(ouptutPath);

            app.addDataToCopy(bg0.toString());
            app.addDataToCopy(bg1.toString());
            app.addDataToCopy(bg2.toString());

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
