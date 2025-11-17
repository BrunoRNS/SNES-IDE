package snes_examples.hello_world;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

import javasnes.App; // App construct the application
import javasnes.boot.Boot; // Boot defines the boot sequence of the application
import javasnes.data.Data; // The Data to be added in AppData class
import javasnes.hdr.MemoryMapping; // The ROM memory mapping and definitions
import javasnes.instruction.SnesInstruction; // An abstract class for all instructions in SNES
import javasnes.makefile.Make; // Generates the makefile, which will build the C code in ROM
import javasnes.output.SnesOutput; // Output definitions, in this example, only consoleDrawText
import javasnes.util.structures.SnesLoadExtern; // Load extern definitions, from AppData for example
import javasnes.util.types.AppData; // The data container, will generate data.asm which collects the data from files
import javasnes.util.types.Processor; // The processor method, which will execute 60 times per second, and run other processes
import javasnes.util.types.SnesProcess; // The process class represents the method in C/SNES development
import javasnes.util.types.vars.scalar.data.SnesChar; // To create Char variables/methods or use its type def
import javasnes.util.types.vars.scalar.data.SnesVoid; // To create void variables/methods or use its type def


public class HelloWorldExplainedConfigExample {
    
    final static SnesVoid VOID = new SnesVoid();
    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {

        // App.Builder will construct the application, based on other objects
        // Use .set(ClassName) to add something
        App.Builder helloWorld = Config.generateApp();

        // Define memory mapping of the ROM
        // as it only uses the default mapping, only change the ROM name
        // it must be a 21 char string
        HashMap<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "Javasnes HelloWorld  ");
        MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

        helloWorld.setMemoryMapping(memMap);

        // AppData, which defines the name to export and the data file to load
        // Data(name, dataFile, needEndTag), bankToPut
        AppData appData = Config.generateAppData();
        appData.registerData(new Data("tilfont", "pvsneslibfont.pic", false), (byte) 2);
        appData.registerData(new Data("palfont", "pvsneslibfont.pal", false), (byte) 2);

        helloWorld.setAppData(appData);

        // Create Boot Sequence based on method generateBoot
        Boot boot = Config.generateBoot();

        helloWorld.setBoot(boot);

        // Create a global definition that includes tilfont and palfont from AppData
        // They are loaded as char objects
        SnesInstruction[] globalDefs = new SnesInstruction[1];
        String[] loadExtern = {"tilfont", "palfont"};
        globalDefs[0] = new SnesLoadExtern(loadExtern, CHAR);

        helloWorld.setGlobalInstructions(globalDefs);

        // Define processor method and a process that printHelloWorld
        // The processes are saved in an array, and loaded from printHelloWorld method
        // Add process to processor
        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[1];
        processes[0] = printHelloWorld();
        processor.addProcess(processes[0], null);

        helloWorld.setProcessor(processor);
        helloWorld.setSnesProcesses(processes);

        // Define makefile to build the data from data folder to snes data that can be loaded
        // in AppData class
        // The rules used are defined in Config.addMakeRules
        Make makefile = Config.generateMakefile();
        makefile.setRomName("JavaSnes_HelloWorldExplainedConfigExample");
        Config.addMakeRules(makefile);

        helloWorld.setMakefile(makefile);

        // Build application in a snes ROM
        Config.build(helloWorld);

    }

    /**
     * A process that prints out "Hello World from JavaSnes!" to the console.
     *
     * @return a process that prints out the message
     */
    public static SnesProcess printHelloWorld() {

        SnesInstruction[] commands = new SnesInstruction[1];

        commands[0] = SnesOutput.consoleDrawText(3, 10, "Hello World from JavaSnes!", null);

        return new SnesProcess(
                "printHelloWorld",
                (byte) 0, commands, VOID
        );

    }

    private static interface Config {

        // Build the App Builder
        public static App.Builder generateApp() {
            return new App.Builder();
        }

        // Generate the map of memory
        public static MemoryMapping generateMemoryMapping(Map<String, String> config) {

            MemoryMapping memMap = new MemoryMapping(config);
            return memMap;

        }

        // Generate the datas of the App
        public static AppData generateAppData() {
            return new AppData();
        }

        // Start the App
        public static Boot generateBoot() {

            Boot boot = new Boot(postLogoCommands());
            return boot;

        }

        // Start initialization / sequence of commands after initialization
        public static Map<String, Map<String, String[]>> postLogoCommands() {

            Map<String, Map<String, String[]>> boot = new HashMap<>();

            boot.put("postLogoCommands", new LinkedHashMap<>());

            // Screen off
            boot.get("postLogoCommands")
                    .put("setScreenOff", null);

            //---------Configure the screen-----------------------------
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
            //------------------------------------------------------

            // Screen On
            boot.get("postLogoCommands")
                    .put("setScreenOn", null);

            return boot;

        }

        // Generate the Make File
        public static Make generateMakefile() {

            return new Make();

        }

        // Defines what will be created in the make file.
        public static void addMakeRules(Make makefile) {

            // Text font
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

        // Build the App
        public static void build(App.Builder app) throws Exception {

            Path actualPath = Paths.get(
                    HelloWorldExplainedConfigExample.class.getProtectionDomain().getCodeSource().getLocation().toURI()
            ).normalize().toAbsolutePath().getParent();

            Path dataPath = actualPath.resolve("data").resolve("pvsneslibfont.png");
            Path ouptutPath = actualPath.resolve("output");

            cleanBuild(ouptutPath);

            app.addDataToCopy(dataPath.toString());
            app.setDestination(ouptutPath.toString());

            app.build();

        }

        // Clean the Directory
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
