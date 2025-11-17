package snes_examples.c_logic_examples;

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
import javasnes.util.operators.SnesOperator;
import javasnes.util.operators.assign.OperatorAssign;
import javasnes.util.operators.binary.OperatorBinSAL;
import javasnes.util.operators.binary.OperatorBinSAR;
import javasnes.util.operators.binary.OperatorBinSHL;
import javasnes.util.operators.binary.OperatorBinSHR;
import javasnes.util.operators.math.OperatorAdd;
import javasnes.util.operators.math.OperatorDivision;
import javasnes.util.operators.math.OperatorMod;
import javasnes.util.operators.math.OperatorPlus;
import javasnes.util.operators.math.OperatorSub;
import javasnes.util.operators.unitary.OperatorCast;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.data.SnesVoid;
import javasnes.util.types.vars.scalar.number.signed.SnesS8;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU8;

public class OperationsExample {

    final static SnesVoid VOID = new SnesVoid();
    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {

        App.Builder operationsExample = Config.generateApp();

        HashMap<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "OperationsExample    ");
        MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

        operationsExample.setMemoryMapping(memMap);

        AppData appData = Config.generateAppData();
        appData.registerData(new Data("tilfont", "pvsneslibfont.pic", false), (byte) 2);
        appData.registerData(new Data("palfont", "pvsneslibfont.pal", false), (byte) 2);

        operationsExample.setAppData(appData);

        Boot boot = Config.generateBoot();

        operationsExample.setBoot(boot);

        SnesInstruction[] globalDefs = new SnesInstruction[1];
        String[] loadExtern = {"tilfont", "palfont"};
        globalDefs[0] = new SnesLoadExtern(loadExtern, CHAR);

        operationsExample.setGlobalInstructions(globalDefs);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[7];

        processes[0] = addTwoNumbers();
        processor.addProcess(processes[0], null);

        processes[1] = subTwoNumbers();
        processor.addProcess(processes[1], null);

        processes[2] = plusTwoNumbers();
        processor.addProcess(processes[2], null);

        processes[3] = divideTwoNumbers();
        processor.addProcess(processes[3], null);

        processes[4] = modTwoNumbers();
        processor.addProcess(processes[4], null);

        processes[5] = shiftTwoNumbers();
        processor.addProcess(processes[5], null);

        processes[6] = shiftTwoSignedNumbers();
        processor.addProcess(processes[6], null);

        operationsExample.setSnesProcesses(processes);
        operationsExample.setProcessor(processor);

        Make makefile = Config.generateMakefile();
        makefile.setRomName("JavaSnes_OperationsExample");
        Config.addMakeRules(makefile);

        operationsExample.setMakefile(makefile);

        Config.build(operationsExample);

    }

    /**
     * Generates a process that adds two unsigned 8-bit numbers, num1 and num2.
     * The process stores the result in a variable named result. The process
     * then prints the values of num1, num2, and result.
     *
     * @return a process containing an addition operation
     */
    public static SnesProcess addTwoNumbers() {

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesInstruction[] comands = new SnesInstruction[5];

        SnesU8 num1 = new SnesU8("num1", "4");
        SnesU8 num2 = new SnesU8("num2", "5");
        SnesU8 result = new SnesU8("result");

        comands[0] = num1;
        comands[1] = num2;
        comands[2] = result;

        SnesOperator add = new OperatorAdd(num1, num2);
        SnesOperator assign = new OperatorAssign(result.name, add.getSourceCode());

        SnesOperator castNum1 = new OperatorCast(INT, num1);
        SnesOperator castNum2 = new OperatorCast(INT, num2);
        SnesOperator castResult = new OperatorCast(INT, result);

        comands[3] = assign;

        comands[4] = SnesOutput.consoleDrawText(
                3, 1, "%d + %d = %d", ", "
                + castNum1.getSourceCode()
                + ", "
                + castNum2.getSourceCode()
                + ", "
                + castResult.getSourceCode()
        );

        SnesProcess process = new SnesProcess("addTwoNumbers", comands, VOID);
        return process;

    }

    /**
     * Generate a process that takes two unsigned 8-bit numbers, num1 and num2,
     * and computes the result of num1 - num2. The process stores the result in
     * a variable named result. The process then prints the values of num1,
     * num2, and result.
     *
     * @return a process containing a subtraction operation
     */
    public static SnesProcess subTwoNumbers() {

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesInstruction[] comands = new SnesInstruction[5];

        SnesU8 num1 = new SnesU8("num1", "6");
        SnesU8 num2 = new SnesU8("num2", "3");
        SnesU8 result = new SnesU8("result");

        comands[0] = num1;
        comands[1] = num2;
        comands[2] = result;

        SnesOperator sub = new OperatorSub(num1, num2);
        SnesOperator assign = new OperatorAssign(result.name, sub.getSourceCode());

        SnesOperator castNum1 = new OperatorCast(INT, num1);
        SnesOperator castNum2 = new OperatorCast(INT, num2);
        SnesOperator castResult = new OperatorCast(INT, result);

        comands[3] = assign;

        comands[4] = SnesOutput.consoleDrawText(
                3, 4, "%d - %d = %d", ", "
                + castNum1.getSourceCode()
                + ", "
                + castNum2.getSourceCode()
                + ", "
                + castResult.getSourceCode()
        );

        SnesProcess process = new SnesProcess("subTwoNumbers", comands, VOID);
        return process;

    }

    /**
     * Generate a process that takes two unsigned 8-bit numbers, num1 and num2,
     * and computes the result of num1 + num2. The process stores the result in
     * a variable named result. The process then prints the values of num1,
     * num2, and result.
     *
     * @return a process containing an addition operation
     */
    public static SnesProcess plusTwoNumbers() {

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesInstruction[] comands = new SnesInstruction[5];

        SnesU8 num1 = new SnesU8("num1", "4");
        SnesU8 num2 = new SnesU8("num2", "5");
        SnesU8 result = new SnesU8("result");

        comands[0] = num1;
        comands[1] = num2;
        comands[2] = result;

        SnesOperator plus = new OperatorPlus(num1, num2);
        SnesOperator assign = new OperatorAssign(result.name, plus.getSourceCode());

        SnesOperator castNum1 = new OperatorCast(INT, num1);
        SnesOperator castNum2 = new OperatorCast(INT, num2);
        SnesOperator castResult = new OperatorCast(INT, result);

        comands[3] = assign;

        comands[4] = SnesOutput.consoleDrawText(
                3, 7, "%d * %d = %d", ", "
                + castNum1.getSourceCode()
                + ", "
                + castNum2.getSourceCode()
                + ", "
                + castResult.getSourceCode()
        );

        SnesProcess process = new SnesProcess("plusTwoNumbers", comands, VOID);
        return process;

    }

    /**
     * Generate a process that contains a division operation. The process
     * divides num1 by num2 and stores the result in a variable named result.
     * The process then prints out the values of num1, num2, and result.
     *
     * @return a process containing a division operation
     */
    public static SnesProcess divideTwoNumbers() {

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesInstruction[] comands = new SnesInstruction[5];

        SnesU8 num1 = new SnesU8("num1", "8");
        SnesU8 num2 = new SnesU8("num2", "2");
        SnesU8 result = new SnesU8("result");

        comands[0] = num1;
        comands[1] = num2;
        comands[2] = result;

        SnesOperator division = new OperatorDivision(num1, num2);
        SnesOperator assign = new OperatorAssign(result.name, division.getSourceCode());

        SnesOperator castNum1 = new OperatorCast(INT, num1);
        SnesOperator castNum2 = new OperatorCast(INT, num2);
        SnesOperator castResult = new OperatorCast(INT, result);

        comands[3] = assign;

        comands[4] = SnesOutput.consoleDrawText(
                3, 10, "%d / %d = %d", ", "
                + castNum1.getSourceCode()
                + ", "
                + castNum2.getSourceCode()
                + ", "
                + castResult.getSourceCode()
        );

        SnesProcess process = new SnesProcess("divideTwoNumbers", comands, VOID);
        return process;

    }

    /**
     * Generate a process that takes two unsigned 8-bit numbers, num1 and num2,
     * and computes the result of num1 modulo num2. The process stores the
     * result in a variable named result. The process then prints the values of
     * num1, num2, and result.
     *
     * @return a SnesProcess containing a modulo operation
     */
    public static SnesProcess modTwoNumbers() {

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesInstruction[] comands = new SnesInstruction[5];

        SnesU8 num1 = new SnesU8("num1", "26");
        SnesU8 num2 = new SnesU8("num2", "5");
        SnesU8 result = new SnesU8("result");

        comands[0] = num1;
        comands[1] = num2;
        comands[2] = result;

        SnesOperator mod = new OperatorMod(num1, num2);
        SnesOperator assign = new OperatorAssign(result.name, mod.getSourceCode());

        SnesOperator castNum1 = new OperatorCast(INT, num1);
        SnesOperator castNum2 = new OperatorCast(INT, num2);
        SnesOperator castResult = new OperatorCast(INT, result);

        comands[3] = assign;

        comands[4] = SnesOutput.consoleDrawText(
                3, 13, "%d %% %d = %d", ", "
                + castNum1.getSourceCode()
                + ", "
                + castNum2.getSourceCode()
                + ", "
                + castResult.getSourceCode()
        );

        SnesProcess process = new SnesProcess("modTwoNumbers", comands, VOID);
        return process;

    }

    /**
     * This function generates a process that contains two shift operations. The
     * process shifts num1 left by 3 bits, and num2 right by 2 bits. The results
     * of the shift operations are stored in result1 and result2 respectively.
     * The process then prints out the values of num1, result1, num2, and
     * result2.
     *
     * @return a process containing two shift operations
     */
    public static SnesProcess shiftTwoNumbers() {

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesInstruction[] comands = new SnesInstruction[8];

        SnesU8 num1 = new SnesU8("num1", "4");
        SnesU8 num2 = new SnesU8("num2", "16");
        SnesU8 result1 = new SnesU8("result1");
        SnesU8 result2 = new SnesU8("result2");

        comands[0] = num1;
        comands[1] = num2;
        comands[2] = result1;
        comands[3] = result2;

        SnesOperator shl = new OperatorBinSHL(num1, 3);
        SnesOperator assign1 = new OperatorAssign(result1.name, shl.getSourceCode());

        SnesOperator shr = new OperatorBinSHR(num2, 2);
        SnesOperator assign2 = new OperatorAssign(result2.name, shr.getSourceCode());

        comands[4] = assign1;
        comands[5] = assign2;

        SnesOperator castNum1 = new OperatorCast(INT, num1);
        SnesOperator castNum2 = new OperatorCast(INT, num2);
        SnesOperator castResult1 = new OperatorCast(INT, result1);
        SnesOperator castResult2 = new OperatorCast(INT, result2);

        comands[6] = SnesOutput.consoleDrawText(
                3, 16, "%d << 3 = %d", ", "
                + castNum1.getSourceCode()
                + ", "
                + castResult1.getSourceCode()
        );

        comands[7] = SnesOutput.consoleDrawText(
                3, 19, "%d >> 2 = %d", ", "
                + castNum2.getSourceCode()
                + ", "
                + castResult2.getSourceCode()
        );

        SnesProcess process = new SnesProcess("shiftTwoNumbers", comands, VOID);
        return process;

    }

    /**
     * Generate a process that takes two signed 8-bit numbers, num1 and num2,
     * and shifts them left and right by 3 and 2 bits respectively. The process
     * stores the results in variables named result1 and result2. The process
     * then prints out the values of num1, num2, result1, and result2.
     *
     * @return a process containing a left shift and a right shift operation
     */
    public static SnesProcess shiftTwoSignedNumbers() {

        final SnesVoid INT = new SnesVoid();
        INT.type = "int";

        SnesInstruction[] comands = new SnesInstruction[8];

        SnesS8 num1 = new SnesS8("num1", "-4");
        SnesS8 num2 = new SnesS8("num2", "-16");
        SnesS8 result1 = new SnesS8("result1");
        SnesS8 result2 = new SnesS8("result2");

        comands[0] = num1;
        comands[1] = num2;
        comands[2] = result1;
        comands[3] = result2;

        SnesOperator sal = new OperatorBinSAL(num1, 3);
        SnesOperator assign1 = new OperatorAssign(result1.name, sal.getSourceCode());

        SnesOperator sar = new OperatorBinSAR(num2, 2);
        SnesOperator assign2 = new OperatorAssign(result2.name, sar.getSourceCode());

        comands[4] = assign1;
        comands[5] = assign2;

        SnesOperator castNum1 = new OperatorCast(INT, num1);
        SnesOperator castNum2 = new OperatorCast(INT, num2);
        SnesOperator castResult1 = new OperatorCast(INT, result1);
        SnesOperator castResult2 = new OperatorCast(INT, result2);

        comands[6] = SnesOutput.consoleDrawText(
                3, 21, "%d << 3 = %d", ", "
                + castNum1.getSourceCode()
                + ", "
                + castResult1.getSourceCode()
        );

        comands[7] = SnesOutput.consoleDrawText(
                3, 24, "%d >> 2 = %d", ", "
                + castNum2.getSourceCode()
                + ", "
                + castResult2.getSourceCode()
        );

        SnesProcess process = new SnesProcess("shiftTwoSignedNumbers", comands, VOID);
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
                    OperationsExample.class.getProtectionDomain().getCodeSource().getLocation().toURI()
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
