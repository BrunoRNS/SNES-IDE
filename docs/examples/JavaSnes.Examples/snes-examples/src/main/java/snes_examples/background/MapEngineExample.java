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
import javasnes.util.logic.SnesElseIf;
import javasnes.util.logic.SnesIf;
import javasnes.util.operators.assign.OperatorAssign;
import javasnes.util.operators.logical.OperatorAnd;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.number.signed.SnesS16;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU16;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU8;

public class MapEngineExample {

    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {

        App.Builder mapEngineExample = Config.generateApp();

        Map<String, String> memoryMappingConfig = new HashMap<>();
        memoryMappingConfig.put("name", "MapEngineExample     ");

        MemoryMapping memoryMapping = Config.generateMemoryMapping(memoryMappingConfig);

        mapEngineExample.setMemoryMapping(memoryMapping);

        AppData appData = Config.generateAppData();

        appData.registerData(new Data("tileset", "tileslevel1.pic", true), (byte) 2);
        appData.registerData(new Data("tilesetpal", "tileslevel1.pal", false), (byte) 2);

        appData.registerData(new Data("mapkungfu", "BG1.m16", false), (byte) 3);
        appData.registerData(new Data("tilesetatt", "maplevel01.b16", false), (byte) 3);
        appData.registerData(new Data("tilesetdef", "maplevel01.t16", false), (byte) 3);

        mapEngineExample.setAppData(appData);

        Boot boot = Config.generateBoot();
        mapEngineExample.setBoot(boot);

        SnesInstruction[] globalInstructions = new SnesInstruction[5];

        globalInstructions[0] = new SnesLoadExtern(new String[] {
            "tileset", "tileset_end", "tilesetpal", "mapkungfu", "tilesetatt", "tilesetdef"
        }, CHAR);

        globalInstructions[1] = new SnesU16("pad0", "0");
        globalInstructions[2] = new SnesS16("mapscx", "16 * 8");
        globalInstructions[3] = new SnesU8("keyl", "0");
        globalInstructions[4] = new SnesU8("keyr", "0");

        mapEngineExample.setGlobalInstructions(globalInstructions);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[1];

        processes[0] = moveCameraInBackground();
        processor.addProcess(processes[0], null);

        mapEngineExample.setProcessor(processor);
        mapEngineExample.setSnesProcesses(processes);

        Make makefile = Config.generateMakefile();
        makefile.setRomName("JavaSnes_MapEngineExample");

        Config.addMakeRules(makefile);

        mapEngineExample.setMakefile(makefile);

        Config.build(mapEngineExample);

    }


    /**
     * A process that updates the camera position in the background
     * based on user input. It is called by the boot process.
     * 
     * It updates the camera position in the background based on the
     * user input. The camera moves in the left-right direction when
     * the user presses the left or right key.
     * 
     * @return a SnesProcess that updates the camera position in the background
     * based on user input.
     */
    public static SnesProcess moveCameraInBackground() {
        
        SnesInstruction[] instructions = new SnesInstruction[5];

        instructions[0] = SnesOutput.mapUpdate();
        instructions[1] = new OperatorAssign(
            "pad0", SnesInput.padsCurrent((byte) 0).sourceCode
        );

        List<SnesInstruction> ifLeft = new ArrayList<>();

        ifLeft.add(
            new OperatorAssign(
                "mapscx",
                "1", '-'
            )
        );
        
        List<SnesInstruction> ifRight = new ArrayList<>();

        ifRight.add(
            new OperatorAssign(
                "mapscx",
                "1", '+'
            )
        );

        SnesElseIf elseIf = new SnesElseIf(
            new OperatorAnd("pad0 & KEY_RIGHT", "mapscx < (208 * 8)"),
            ifRight
        ); 

        SnesIf ifStatement = new SnesIf(
            new OperatorAnd("pad0 & KEY_LEFT", "mapscx > 16 * 8"),
            ifLeft, new ArrayList<>(){{ add(elseIf); }}
        );

        ifStatement.generateSourceCode();

        instructions[2] = ifStatement;

        instructions[3] = SnesOutput.mapUpdateCamera("mapscx", "0");

        instructions[4] = SnesOutput.mapVblank();

        return new SnesProcess("MoveCameraInBackground", (byte) 0, instructions);

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
                    .put("bgSetDisable", new String[] { "0" });

            boot.get("postLogoCommands")
                    .put("bgInitTileSet", new String[] {
                        "0", "&tileset", "&tilesetpal", "0", "(&tileset_end - &tileset)",
                        "16 * 2 * 3", "BG_16COLORS", "0x2000"
                    });

            boot.get("postLogoCommands")
                    .put("bgSetMapPtr", new String[] {
                        "0", "0x6800", "SC_64x32"
                    });
            
            boot.get("postLogoCommands")
                    .put("bgSetEnable", new String[] {
                        "0"
                    });

            boot.get("postLogoCommands")
                    .put("setScreenOn", null);

            boot.get("postLogoCommands")
                    .put("mapLoad", new String[] {
                        "(u8*) &mapkungfu", "(u8*) &tilesetdef", "(u8*) &tilesetatt"
                    });

            boot.get("postLogoCommands")
                    .put("WaitForVBlank", null);

            return boot;

        }

        public static Make generateMakefile() {

            return new Make();

        }

        public static void addMakeRules(Make makefile) {

            Make.MakeRule tiles = new Make.MakeRule(
                    "tileslevel1.pic",
                    "tileslevel1.png",
                    "$(GFXCONV) -s 8 -o 48 -u 16 -p -m -i $<"
            );

            Make.MakeRule map = new Make.MakeRule(
                    "BG1.m16",
                    "maplevel01.tmj tileslevel1.pic",
                    "$(TMXCONV) $< tileslevel1.map"
            );

            Make.MakeRule bitmaps = new Make.MakeRule(
                    "bitmaps",
                    "BG1.m16 tileslevel1.pic",
                    ""
            );

            makefile.addRule(tiles);
            makefile.addRule(map);

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

            Path tiles = dataPath.resolve("tileslevel1.png");
            Path tmjMap = dataPath.resolve("maplevel01.tmj");

            cleanBuild(ouptutPath);

            app.addDataToCopy(tiles.toString());
            app.addDataToCopy(tmjMap.toString());

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
