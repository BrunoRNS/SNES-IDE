package snes_examples.memory_mapping;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

import javasnes.App;
import javasnes.boot.Boot;
import javasnes.data.Data;
import javasnes.hdr.MemoryMapping;
import javasnes.instruction.SnesInstruction;
import javasnes.makefile.Make;
import javasnes.output.SnesOutput;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.scalar.data.SnesChar;

public class HiRomFastRomExample {

    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {

        App.Builder hiromFastromExample = Config.generateApp();

        HashMap<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "HiRomFastRomExample  ");
        
        MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

        // Set the memory mapping to use HiROM and FastROM
        memMap.HiROM = true;
        memMap.FastROM = true;

        // update the memory mapping
        memMap.generateASM();

        hiromFastromExample.setMemoryMapping(memMap);

        AppData appData = Config.generateAppData();
        appData.registerData(new Data("tilfont", "pvsneslibfont.pic", false), (byte) 2);
        appData.registerData(new Data("palfont", "pvsneslibfont.pal", false), (byte) 2);

        hiromFastromExample.setAppData(appData);

        Boot boot = Config.generateBoot();

        hiromFastromExample.setBoot(boot);

        SnesInstruction[] globalDefs = new SnesInstruction[1];

        String[] loadExtern = {"tilfont", "palfont"};
        globalDefs[0] = new SnesLoadExtern(loadExtern, CHAR);

        hiromFastromExample.setGlobalInstructions(globalDefs);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[1];

        processes[0] = printWonderfulText();
        processor.addProcess(processes[0], null);

        hiromFastromExample.setProcessor(processor);
        hiromFastromExample.setSnesProcesses(processes);

        Make makefile = Config.generateMakefile();
        makefile.setRomName("Javasnes_HiRomFastRomExample");

        // Tell to the compiler to use HiROM and FastROM
        makefile.addHeaderLine("HIROM=1");
        makefile.addHeaderLine("FASTROM=1");

        Config.addMakeRules(makefile);

        hiromFastromExample.setMakefile(makefile);

        Config.build(hiromFastromExample);

    }

    public static SnesProcess printWonderfulText() {

        SnesInstruction[] commands = new SnesInstruction[2];
        
        commands[0] = SnesOutput.consoleDrawText(4, 13, "This is a HiROM-FastROM", null);
        commands[1] = SnesOutput.consoleDrawText(10, 15, "mapped ROM!", null);

        // (byte) 0 is the same thing as using SnesVoid()
        return new SnesProcess(
            "printWonderfulText",
            (byte) 0, commands
        );

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
                    HiRomFastRomExample.class.getProtectionDomain().getCodeSource().getLocation().toURI()
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
