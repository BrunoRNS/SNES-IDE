package snes_examples.c_logic_examples;

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
import javasnes.util.keywords.KeyWords;
import javasnes.util.logic.SnesElse;
import javasnes.util.logic.SnesElseIf;
import javasnes.util.logic.SnesIf;
import javasnes.util.logic.SnesSwitch;
import javasnes.util.loops.SnesWhile;
import javasnes.util.operators.SnesOperator;
import javasnes.util.operators.logical.OperatorGreater;
import javasnes.util.operators.logical.OperatorSmaller;
import javasnes.util.operators.unitary.OperatorCast;
import javasnes.util.operators.unitary.OperatorIncrement;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.data.SnesVoid;
import javasnes.util.types.vars.scalar.number.signed.SnesS8;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU32;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU8;

public class LogicLoopsExample {

    final static SnesChar CHAR = new SnesChar("char");
    final static SnesVoid VOID = new SnesVoid();

    public static void main(String[] args) throws Exception {

        App.Builder logicLoopsExample = Config.generateApp();

        HashMap<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "LogicLoopsExample    ");
        MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

        logicLoopsExample.setMemoryMapping(memMap);

        AppData appData = Config.generateAppData();
        appData.registerData(new Data("tilfont", "pvsneslibfont.pic", false), (byte) 2);
        appData.registerData(new Data("palfont", "pvsneslibfont.pal", false), (byte) 2);

        logicLoopsExample.setAppData(appData);

        Boot boot = Config.generateBoot();

        logicLoopsExample.setBoot(boot);

        SnesInstruction[] globalDefs = new SnesInstruction[2];
        String[] loadExtern = {"tilfont", "palfont"};
        globalDefs[0] = new SnesLoadExtern(loadExtern, CHAR);
        globalDefs[1] = new SnesU32("timer", "0");

        logicLoopsExample.setGlobalInstructions(globalDefs);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[3];

        processes[0] = ifExample();
        processes[1] = switchExample();
        processes[2] = whileLoopExample();

        processor.addProcess(processes[0], null);
        processor.addProcess(processes[1], null);
        processor.addProcess(processes[2], null);

        logicLoopsExample.setProcessor(processor);
        logicLoopsExample.setSnesProcesses(processes);

        Make makefile = Config.generateMakefile();
        makefile.setRomName("JavaSnes_LogicLoopsExample");
        Config.addMakeRules(makefile);

        logicLoopsExample.setMakefile(makefile);

        Config.build(logicLoopsExample);

    }

    /**
     * Generate a SnesProcess for an if-else statement example.
     *
     * This process will print out whether num1 is greater than, less than, or
     * equal to num2.
     *
     * @return a SnesProcess for the if-else statement example
     */
    public static SnesProcess ifExample() {

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesInstruction[] commands = new SnesInstruction[3];

        SnesU8 num1 = new SnesU8("num1", "4");
        SnesU8 num2 = new SnesU8("num2", "8");

        SnesOperator greater = new OperatorGreater(num1, num2);
        SnesOperator less = new OperatorSmaller(num1, num2);

        SnesOperator cast1 = new OperatorCast(INT, num1);
        SnesOperator cast2 = new OperatorCast(INT, num2);

        commands[0] = num1;
        commands[1] = num2;

        SnesInstruction output1 = SnesOutput.consoleDrawText(
                3, 3, "%d > %d", ", "
                + cast1.getSourceCode()
                + ", "
                + cast2.getSourceCode()
        );

        SnesInstruction output2 = SnesOutput.consoleDrawText(
                3, 3, "%d < %d", ", "
                + cast1.getSourceCode()
                + ", "
                + cast2.getSourceCode()
        );

        SnesInstruction output3 = SnesOutput.consoleDrawText(
                3, 3, "%d == %d", ", "
                + cast1.getSourceCode()
                + ", "
                + cast2.getSourceCode()
        );

        ArrayList<SnesInstruction> ifGreater = new ArrayList<>();
        ifGreater.add(output1);

        ArrayList<SnesInstruction> ifLess = new ArrayList<>();
        ifLess.add(output2);

        ArrayList<SnesInstruction> ifEqual = new ArrayList<>();
        ifEqual.add(output3);

        SnesElseIf elseifStatement = new SnesElseIf(
                less,
                ifLess
        );

        ArrayList<SnesElseIf> elseifStatements = new ArrayList<>();
        elseifStatements.add(elseifStatement);

        SnesElse elseStatement = new SnesElse(
                ifEqual
        );

        SnesIf ifStatement = new SnesIf(
                greater,
                ifGreater,
                elseifStatements,
                elseStatement
        );

        ifStatement.generateSourceCode();

        commands[2] = ifStatement;

        SnesProcess ifExample = new SnesProcess(
                "ifExample",
                commands, VOID
        );

        return ifExample;

    }

    /**
     * This function generates a process that contains a switch statement. The
     * switch statement takes an s8 variable as input and has two cases: -8 and
     * 8. Each case prints a message to the console indicating which case was
     * taken. If the input is not -8 or 8, a default case prints a message to
     * the console.
     *
     * @return a process containing a switch statement
     */
    public static SnesProcess switchExample() {

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesInstruction[] commands = new SnesInstruction[2];

        SnesS8 num = new SnesS8("num", "-8");

        commands[0] = num;

        Map<String, List<SnesInstruction>> cases = new HashMap<>();

        List<SnesInstruction> case0 = new ArrayList<>();
        case0.add(SnesOutput.consoleDrawText(3, 6, "num = -8", null));
        case0.add(KeyWords.snesBreak);
        cases.put("-8", case0);

        List<SnesInstruction> case1 = new ArrayList<>();
        case1.add(SnesOutput.consoleDrawText(3, 6, "num = 8", null));
        case1.add(KeyWords.snesBreak);
        cases.put("8", case1);

        List<SnesInstruction> defaultCase = new ArrayList<>();
        defaultCase.add(SnesOutput.consoleDrawText(3, 6, "num is not -8 or 8", null));
        defaultCase.add(KeyWords.snesBreak);

        SnesSwitch switchCase = new SnesSwitch(
                num, cases, defaultCase
        );

        switchCase.generateSourceCode();

        commands[1] = switchCase;

        SnesProcess switchExample = new SnesProcess(
                "switchExample",
                commands, VOID
        );

        return switchExample;

    }

    /**
     * This function generates a process that contains a while loop. The while
     * loop runs until a timer variable reaches 200. The loop body prints the
     * value of the timer variable each iteration.
     *
     * @return a process containing a while loop
     */
    public static SnesProcess whileLoopExample() {

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesInstruction[] commands = new SnesInstruction[1];

        SnesU32 timer = new SnesU32("timer", "0");

        SnesOperator cast = new OperatorCast(INT, timer);

        SnesInstruction output = SnesOutput.consoleDrawText(
                3, 9, "timer: %d", ", "
                + cast.getSourceCode()
        );

        SnesOperator loop = new OperatorSmaller(timer.name, "200"); // runs until timer == 200

        SnesOperator increment = new OperatorIncrement(timer, true);

        SnesInstruction incrementInstruction = new SnesRawInstruction(
                increment.getSourceCode() + ";"
        );

        List<SnesInstruction> innerInstructions = new ArrayList<>();
        innerInstructions.add(output);
        innerInstructions.add(incrementInstruction);
        innerInstructions.add(KeyWords.waitvbl);

        SnesWhile whileLoop = new SnesWhile(
                loop,
                innerInstructions
        );

        whileLoop.generateSourceCode();

        commands[0] = whileLoop;

        SnesProcess whileLoopExample = new SnesProcess(
                "whileLoopExample",
                commands, VOID
        );

        return whileLoopExample;

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
                    LogicLoopsExample.class.getProtectionDomain().getCodeSource().getLocation().toURI()
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
