package snes_examples.random;

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
import javasnes.util.logic.SnesIf;
import javasnes.util.operators.SnesOperator;
import javasnes.util.operators.assign.OperatorAssign;
import javasnes.util.operators.binary.OperatorBinAnd;
import javasnes.util.operators.unitary.OperatorCast;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.data.SnesVoid;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU16;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU32;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU8;

public class RandomExample {

    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {

        App.Builder randomExample = Config.generateApp();

        Map<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "RandomExample        ");

        MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

        randomExample.setMemoryMapping(memMap);

        AppData appData = Config.generateAppData();
        appData.registerData(new Data("tilfont", "pvsneslibfont.pic", false), (byte) 2);
        appData.registerData(new Data("palfont", "pvsneslibfont.pal", false), (byte) 2);

        randomExample.setAppData(appData);

        Boot boot = Config.generateBoot();

        randomExample.setBoot(boot);

        SnesInstruction[] globalDefs = new SnesInstruction[1];

        String[] loadExtern = {"tilfont", "palfont"};
        globalDefs[0] = new SnesLoadExtern(loadExtern, CHAR);

        randomExample.setGlobalInstructions(globalDefs);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[1];

        processes[0] = showRandomNumber();
        processor.addProcess(processes[0], null);

        randomExample.setProcessor(processor);
        randomExample.setSnesProcesses(processes);

        Make makefile = Config.generateMakefile();
        makefile.setRomName("JavaSnes_RandomExample");

        Config.addMakeRules(makefile);
        
        randomExample.setMakefile(makefile);

        Config.build(randomExample);

    }

    /**
     * Shows a random number when the A button is pressed.
     * 
     * The process uses the rand() function to generate a random number, and then
     * truncates it to a 16-bit unsigned integer using a bitwise AND operation.
     * The resulting value is then assigned to a variable called "randomNumber".
     * 
     * The process then waits for the A button to be pressed, and when it is,
     * it displays the value of "randomNumber" at position (6, 8) on the screen.
     * 
     * @return A SnesProcess object representing the process to show a random number.
     */
    public static SnesProcess showRandomNumber() {

        SnesInstruction[] commands = new SnesInstruction[6];

        SnesU16 pad0 = new SnesU16("pad0");
        SnesU8 randomNumber = new SnesU8("randomNumber");

        commands[0] = pad0;

        SnesOperator assignPad0 = new OperatorAssign(
            pad0.name, SnesInput.padsCurrent((byte) 0).sourceCode
        );

        commands[1] = assignPad0;

        commands[2] = randomNumber;

        SnesOperator truncateNumber = new OperatorBinAnd(
            new SnesU32("rand()"), new SnesU8("0x0F")
        );

        SnesOperator assignRandomValue = new OperatorAssign(
            randomNumber.name, truncateNumber.getSourceCode()
        );

        commands[3] = assignRandomValue;

        SnesInstruction pressButton = SnesOutput.consoleDrawText(
            1, 5, "Press A to show a random number", null
        );

        commands[4] = pressButton;

        List<SnesInstruction> ifPressAInstructions = new ArrayList<>();

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesOperator castRandomNumber = new OperatorCast(
            INT, randomNumber
        );

        SnesInstruction showRandomNumber = SnesOutput.consoleDrawText(
            6, 8, "Random number: %d     ", ", " + castRandomNumber.getSourceCode()
        );

        ifPressAInstructions.add(showRandomNumber);

        SnesIf ifPressA = new SnesIf(new OperatorBinAnd(
            pad0, new SnesU16(SnesInput.keys.KEY_A.sourceCode)
        ), ifPressAInstructions);

        ifPressA.generateSourceCode();

        commands[5] = ifPressA;

        return new SnesProcess(
            "showRandomNumber",
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
                    RandomExample.class.getProtectionDomain().getCodeSource().getLocation().toURI()
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
