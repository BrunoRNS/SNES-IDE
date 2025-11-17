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
import javasnes.util.keywords.KeyWords;
import javasnes.util.logic.SnesSwitch;
import javasnes.util.macros.SnesDefine;
import javasnes.util.operators.assign.OperatorAssign;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.abstracts.scalar.data.SnesScalarData;
import javasnes.util.types.vars.array.number.unsigned.SnesU8Array;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU16;

public class ThreeDBackgroundExample {

    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {

        App.Builder threeDBackgroundExample = Config.generateApp();

        Map<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "3DBackgroundExample  ");

        threeDBackgroundExample.setMemoryMapping(Config.generateMemoryMapping(memMapConfig));

        AppData appData = Config.generateAppData();

        appData.registerData(new Data("patterns", "ground.pc7", true), (byte) 2);
        appData.registerData(new Data("map", "ground.mp7", true), (byte) 2);
        appData.registerData(new Data("palette", "ground.pal", true), (byte) 2);

        appData.registerData(new Data("patterns2", "sky.pic", true), (byte) 3);
        appData.registerData(new Data("map2", "sky.map", true), (byte) 3);
        appData.registerData(new Data("palette2", "sky.pal", true), (byte) 3);

        threeDBackgroundExample.setAppData(appData);

        Boot boot = Config.generateBoot();
        threeDBackgroundExample.setBoot(boot);

        threeDBackgroundExample.addSnesMacro(new SnesDefine("SKYLINEY 96"));

        SnesInstruction[] globalDefs = new SnesInstruction[13];

        String[] loadExtern = {
            "patterns", "patterns_end",
            "map", "map_end",
            "palette", "palette_end",
            "patterns2", "patterns2_end",
            "map2", "map2_end",
            "palette2", "palette2_end"
        };

        globalDefs[0] = new SnesLoadExtern(loadExtern, CHAR);

        SnesU8Array modeTable = new SnesU8Array(
                "ModeTable", (short) 5,
                "{SKYLINEY, BG_MODE3, 1, BG_MODE7, 0x00}"
        );

        globalDefs[1] = modeTable;

        SnesU8Array bgTable = new SnesU8Array(
                "BGTable", (short) 5,
                "{SKYLINEY, 0x12, 1, 0x11, 0x00}"
        );

        globalDefs[2] = bgTable;

        SnesU8Array perspectiveX = generatePerspectiveX();

        globalDefs[3] = perspectiveX;

        SnesU8Array perspectiveY = generatePerspectiveY();

        globalDefs[4] = perspectiveY;

        globalDefs[5] = new SnesU16("pad0");
        globalDefs[6] = new SnesU16("sz", "0");
        globalDefs[7] = new SnesU16("sx", "0");
        globalDefs[8] = new SnesU16("sy", "0");

        globalDefs[9] = new SnesDmaMemory("data_to_transfertMode");
        globalDefs[10] = new SnesDmaMemory("data_to_transfertBG");
        globalDefs[11] = new SnesDmaMemory("data_to_transfertX");
        globalDefs[12] = new SnesDmaMemory("data_to_transfertY");

        threeDBackgroundExample.setGlobalInstructions(globalDefs);

        // This process will be called by boot, and not by the processor
        SnesProcess getTables = getTables();
        threeDBackgroundExample.addSnesProcess(getTables);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[2];

        processes[0] = updateCameraInBg();
        processor.addProcess(processes[0], null);

        processes[1] = setMode7HdmaPerspective();
        processor.addProcess(processes[1], null);

        threeDBackgroundExample.setProcessor(processor);
        threeDBackgroundExample.addSnesProcesses(processes);

        Make makefile = Config.generateMakefile();
        makefile.setRomName("JavaSnes_3DBackgroundExample");

        Config.addMakeRules(makefile);

        threeDBackgroundExample.setMakefile(makefile);

        Config.build(threeDBackgroundExample);

    }

    /**
     * A process that updates the camera position in the background
     * based on user input. It is called by the boot process.
     *
     * It updates the camera position in the background based on the
     * user input. The camera moves in the left-right direction when
     * the user presses the left or right key, in the up-down direction
     * when the user presses the up or down key, and in the front-back
     * direction when the user presses the R or L key.
     */
    public static SnesProcess updateCameraInBg() {

        SnesInstruction[] commands = new SnesInstruction[2];

        SnesU16 pad0 = new SnesU16("pad0");

        commands[0] = new OperatorAssign(pad0.name, SnesInput.padsCurrent((byte) 0).sourceCode);

        Map<String, List<SnesInstruction>> movements = new HashMap<>();

        List<SnesInstruction> left = new ArrayList<>();
        List<SnesInstruction> right = new ArrayList<>();
        List<SnesInstruction> up = new ArrayList<>();
        List<SnesInstruction> down = new ArrayList<>();
        List<SnesInstruction> front = new ArrayList<>();
        List<SnesInstruction> back = new ArrayList<>();

        left.add(new OperatorAssign("sx", "1", '-'));
        left.add(KeyWords.snesBreak);
        right.add(new OperatorAssign("sx", "1", '+'));
        right.add(KeyWords.snesBreak);

        // Y axis is inverted
        up.add(new OperatorAssign("sy", "1", '-'));
        up.add(KeyWords.snesBreak);
        down.add(new OperatorAssign("sy", "1", '+'));
        down.add(KeyWords.snesBreak);

        front.add(new OperatorAssign("sz", "1", '+'));
        front.add(KeyWords.snesBreak);
        back.add(new OperatorAssign("sz", "1", '-'));
        back.add(KeyWords.snesBreak);

        movements.put(SnesInput.keys.KEY_LEFT.sourceCode, left);
        movements.put(SnesInput.keys.KEY_RIGHT.sourceCode, right);

        movements.put(SnesInput.keys.KEY_UP.sourceCode, up);
        movements.put(SnesInput.keys.KEY_DOWN.sourceCode, down);

        movements.put(SnesInput.keys.KEY_R.sourceCode, front);
        movements.put(SnesInput.keys.KEY_L.sourceCode, back);

        SnesSwitch switchMovements = new SnesSwitch(pad0, movements);
        switchMovements.generateSourceCode();

        commands[1] = switchMovements;

        return new SnesProcess(
            "updateCameraInBg",
            (byte) 0, commands
        );

    }

    /**
     * A process that sets the mode 7 registers to enable an affine
     * transformation of the background using DMA channels 1, 2, 3 and 4.
     *
     * It sets the mode 7 affine transformation registers to enable an affine
     * transformation of the background using DMA channels 1, 2, 3 and 4. The
     * transformation is set to use the data in the data_to_transfertMode, data_to_transfertBG,
     * data_to_transfertX and data_to_transfertY DmaMemory objects.
     */
    public static SnesProcess setMode7HdmaPerspective() {

        SnesInstruction[] commands = new SnesInstruction[28];

        commands[0] = new OperatorAssign("REG_M7HOFS", "(sx & 255)");
        commands[1] = new OperatorAssign("REG_M7HOFS", "sx >> 8");
        commands[2] = new OperatorAssign("REG_M7VOFS", "(sy & 255)");
        commands[3] = new OperatorAssign("REG_M7VOFS", "sy >> 8");

        commands[4] = new OperatorAssign("REG_BG2HOFS", "(sx & 255)");
        commands[5] = new OperatorAssign("REG_BG2HOFS", "sx >> 8");

        commands[6] = new OperatorAssign("REG_M7X", "(sx + 128) & 255");
        commands[7] = new OperatorAssign("REG_M7X", "(sx + 128) >> 8");
        commands[8] = new OperatorAssign("REG_M7Y", "(sy + 112) & 255");
        commands[9] = new OperatorAssign("REG_M7Y", "(sy + 112) >> 8");

        commands[10] = new OperatorAssign("REG_HDMAEN", "0");

        commands[11] = new OperatorAssign("REG_DMAP1", "0x00");
        commands[12] = new OperatorAssign("REG_BBAD1", "0x05");
        commands[13] = new OperatorAssign("REG_A1T1LH", "data_to_transfertMode.mem.c.addr");
        commands[14] = new OperatorAssign("REG_A1B1", "data_to_transfertMode.mem.c.bank");

        commands[15] = new OperatorAssign("REG_DMAP2", "0x00");
        commands[16] = new OperatorAssign("REG_BBAD2", "0x2C");
        commands[17] = new OperatorAssign("REG_A1T2LH", "data_to_transfertBG.mem.c.addr");
        commands[18] = new OperatorAssign("REG_A1B2", "data_to_transfertBG.mem.c.bank");

        commands[19] = new OperatorAssign("REG_DMAP3", "0x02");
        commands[20] = new OperatorAssign("REG_BBAD3", "0x1B");
        commands[21] = new OperatorAssign("REG_A1T3LH", "data_to_transfertX.mem.c.addr");
        commands[22] = new OperatorAssign("REG_A1B3", "data_to_transfertX.mem.c.bank");

        commands[23] = new OperatorAssign("REG_DMAP4", "0x02");
        commands[24] = new OperatorAssign("REG_BBAD4", "0x1E");
        commands[25] = new OperatorAssign("REG_A1T4LH", "data_to_transfertY.mem.c.addr");
        commands[26] = new OperatorAssign("REG_A1B4", "data_to_transfertY.mem.c.bank");

        // 00011110; Enable DMA channels 1, 2, 3 and 4
        commands[27] = new OperatorAssign("REG_HDMAEN", "0x1E");

        return new SnesProcess("setMode7_HdmaPerspective", (byte) 0, commands);

    }

    /**
     * A process that sets the pointers of the mode, background, perspective X and perspective Y
     * tables to the addresses of the respective tables in memory.
     * 
     * @return a SnesProcess that sets the pointers of the mode, background, perspective X and
     * perspective Y tables to the addresses of the respective tables in memory.
     */
    public static SnesProcess getTables() {
        
        SnesInstruction[] commands = new SnesInstruction[4];

        commands[0] = new OperatorAssign("data_to_transfertMode.mem.p", "(u8 *)&ModeTable");
        commands[1] = new OperatorAssign("data_to_transfertBG.mem.p", "(u8 *)&BGTable");
        commands[2] = new OperatorAssign("data_to_transfertX.mem.p", "(u8 *)&PerspectiveX");
        commands[3] = new OperatorAssign("data_to_transfertY.mem.p", "(u8 *)PerspectiveY");

        return new SnesProcess("getTables", (byte) 0, commands);

    }

    /**
     * Returns a SnesU8Array containing the data for the perspective X table.
     * 
     * The data is a 264 element array with the following format:
     * <pre>SKYLINEY, 256 & 255, 256 >> 8</pre>
     * followed by 255 - SKYLINEY elements with the value 0xFF
     * followed by 264 - SKYLINEY - 255 elements with the value
     * (x + 128) & 255, where x is the x-coordinate of the point
     * in the 3D space.
     * 
     * @return a SnesU8Array containing the data for the perspective X table
     */
    public static SnesU8Array generatePerspectiveX() {

        return new SnesU8Array(
                "PerspectiveX", (short) 264,
                "{\n"
                + "        SKYLINEY, 256 & 255, 256 >> 8,\n"
                + "        0xFF,\n"
                + "        1, 0,\n"
                + "        0, 2,\n"
                + "        243, 1,\n"
                + "        231, 1,\n"
                + "        220, 1,\n"
                + "        209, 1,\n"
                + "        199, 1,\n"
                + "        189, 1,\n"
                + "        179, 1,\n"
                + "        170, 1,\n"
                + "        161, 1,\n"
                + "        153, 1,\n"
                + "        145, 1,\n"
                + "        137, 1,\n"
                + "        130, 1,\n"
                + "        123, 1,\n"
                + "        116, 1,\n"
                + "        109, 1,\n"
                + "        103, 1,\n"
                + "        97, 1,\n"
                + "        91, 1,\n"
                + "        85, 1,\n"
                + "        79, 1,\n"
                + "        74, 1,\n"
                + "        69, 1,\n"
                + "        64, 1,\n"
                + "        59, 1,\n"
                + "        54, 1,\n"
                + "        49, 1,\n"
                + "        45, 1,\n"
                + "        40, 1,\n"
                + "        36, 1,\n"
                + "        32, 1,\n"
                + "        28, 1,\n"
                + "        24, 1,\n"
                + "        20, 1,\n"
                + "        17, 1,\n"
                + "        13, 1,\n"
                + "        9, 1,\n"
                + "        6, 1,\n"
                + "        3, 1,\n"
                + "        0, 1,\n"
                + "        252, 0,\n"
                + "        249, 0,\n"
                + "        246, 0,\n"
                + "        243, 0,\n"
                + "        240, 0,\n"
                + "        238, 0,\n"
                + "        235, 0,\n"
                + "        232, 0,\n"
                + "        230, 0,\n"
                + "        227, 0,\n"
                + "        225, 0,\n"
                + "        222, 0,\n"
                + "        220, 0,\n"
                + "        217, 0,\n"
                + "        215, 0,\n"
                + "        213, 0,\n"
                + "        211, 0,\n"
                + "        208, 0,\n"
                + "        206, 0,\n"
                + "        204, 0,\n"
                + "        202, 0,\n"
                + "        200, 0,\n"
                + "        198, 0,\n"
                + "        196, 0,\n"
                + "        195, 0,\n"
                + "        193, 0,\n"
                + "        191, 0,\n"
                + "        189, 0,\n"
                + "        187, 0,\n"
                + "        186, 0,\n"
                + "        184, 0,\n"
                + "        182, 0,\n"
                + "        181, 0,\n"
                + "        179, 0,\n"
                + "        178, 0,\n"
                + "        176, 0,\n"
                + "        175, 0,\n"
                + "        173, 0,\n"
                + "        172, 0,\n"
                + "        170, 0,\n"
                + "        169, 0,\n"
                + "        167, 0,\n"
                + "        166, 0,\n"
                + "        165, 0,\n"
                + "        163, 0,\n"
                + "        162, 0,\n"
                + "        161, 0,\n"
                + "        159, 0,\n"
                + "        158, 0,\n"
                + "        157, 0,\n"
                + "        156, 0,\n"
                + "        155, 0,\n"
                + "        153, 0,\n"
                + "        152, 0,\n"
                + "        151, 0,\n"
                + "        150, 0,\n"
                + "        149, 0,\n"
                + "        148, 0,\n"
                + "        147, 0,\n"
                + "        146, 0,\n"
                + "        145, 0,\n"
                + "        144, 0,\n"
                + "        143, 0,\n"
                + "        142, 0,\n"
                + "        141, 0,\n"
                + "        140, 0,\n"
                + "        139, 0,\n"
                + "        138, 0,\n"
                + "        137, 0,\n"
                + "        136, 0,\n"
                + "        135, 0,\n"
                + "        134, 0,\n"
                + "        133, 0,\n"
                + "        132, 0,\n"
                + "        132, 0,\n"
                + "        131, 0,\n"
                + "        130, 0,\n"
                + "        129, 0,\n"
                + "        128, 0,\n"
                + "        127, 0,\n"
                + "        127, 0,\n"
                + "        126, 0,\n"
                + "        125, 0,\n"
                + "        124, 0,\n"
                + "        124, 0,\n"
                + "        123, 0}"
        );

    }

    /**
     * Generates a perspective Y table used in the SNES renderer.
     * <p>
     * This table is used to map the y-coordinate of a pixel in a 256x256 image
     * to a 16-bit signed integer value based on the perspective of the pixel.
     * <p>
     * The table is generated with the formula:
     * <code>
     * int y = (int) ((float) y / 256.0 * (float) SKYLINEY);
     * </code>
     * where SKYLINEY is a constant.
     * <p>
     * The table is then quantized to 8 bits.
     * <p>
     * The table is used in the render loop of the SNES renderer.
     */
    public static SnesU8Array generatePerspectiveY() {

        return new SnesU8Array(
                "PerspectiveY", (short) 264,
                "{\n"
                + "        SKYLINEY, 256 & 255, 256 >> 8,\n"
                + "        0xFF,\n"
                + "122, 0,\n"
                + "        0, 16,\n"
                + "        60, 15,\n"
                + "        139, 14,\n"
                + "        233, 13,\n"
                + "        85, 13,\n"
                + "        204, 12,\n"
                + "        78, 12,\n"
                + "        218, 11,\n"
                + "        109, 11,\n"
                + "        8, 11,\n"
                + "        170, 10,\n"
                + "        82, 10,\n"
                + "        0, 10,\n"
                + "        178, 9,\n"
                + "        105, 9,\n"
                + "        36, 9,\n"
                + "        227, 8,\n"
                + "        166, 8,\n"
                + "        107, 8,\n"
                + "        52, 8,\n"
                + "        0, 8,\n"
                + "        206, 7,\n"
                + "        158, 7,\n"
                + "        113, 7,\n"
                + "        69, 7,\n"
                + "        28, 7,\n"
                + "        244, 6,\n"
                + "        206, 6,\n"
                + "        170, 6,\n"
                + "        135, 6,\n"
                + "        102, 6,\n"
                + "        70, 6,\n"
                + "        39, 6,\n"
                + "        9, 6,\n"
                + "        237, 5,\n"
                + "        209, 5,\n"
                + "        182, 5,\n"
                + "        157, 5,\n"
                + "        132, 5,\n"
                + "        108, 5,\n"
                + "        85, 5,\n"
                + "        62, 5,\n"
                + "        41, 5,\n"
                + "        20, 5,\n"
                + "        0, 5,\n"
                + "        236, 4,\n"
                + "        217, 4,\n"
                + "        198, 4,\n"
                + "        180, 4,\n"
                + "        163, 4,\n"
                + "        146, 4,\n"
                + "        129, 4,\n"
                + "        113, 4,\n"
                + "        98, 4,\n"
                + "        83, 4,\n"
                + "        68, 4,\n"
                + "        53, 4,\n"
                + "        39, 4,\n"
                + "        26, 4,\n"
                + "        12, 4,\n"
                + "        0, 4,\n"
                + "        243, 3,\n"
                + "        231, 3,\n"
                + "        218, 3,\n"
                + "        207, 3,\n"
                + "        195, 3,\n"
                + "        184, 3,\n"
                + "        173, 3,\n"
                + "        162, 3,\n"
                + "        152, 3,\n"
                + "        142, 3,\n"
                + "        132, 3,\n"
                + "        122, 3,\n"
                + "        112, 3,\n"
                + "        103, 3,\n"
                + "        94, 3,\n"
                + "        85, 3,\n"
                + "        76, 3,\n"
                + "        67, 3,\n"
                + "        59, 3,\n"
                + "        51, 3,\n"
                + "        43, 3,\n"
                + "        35, 3,\n"
                + "        27, 3,\n"
                + "        19, 3,\n"
                + "        12, 3,\n"
                + "        4, 3,\n"
                + "        253, 2,\n"
                + "        246, 2,\n"
                + "        239, 2,\n"
                + "        232, 2,\n"
                + "        226, 2,\n"
                + "        219, 2,\n"
                + "        212, 2,\n"
                + "        206, 2,\n"
                + "        200, 2,\n"
                + "        194, 2,\n"
                + "        188, 2,\n"
                + "        182, 2,\n"
                + "        176, 2,\n"
                + "        170, 2,\n"
                + "        165, 2,\n"
                + "        159, 2,\n"
                + "        154, 2,\n"
                + "        148, 2,\n"
                + "        143, 2,\n"
                + "        138, 2,\n"
                + "        133, 2,\n"
                + "        127, 2,\n"
                + "        123, 2,\n"
                + "        118, 2,\n"
                + "        113, 2,\n"
                + "        108, 2,\n"
                + "        103, 2,\n"
                + "        99, 2,\n"
                + "        94, 2,\n"
                + "        90, 2,\n"
                + "        85, 2,\n"
                + "        81, 2,\n"
                + "        77, 2,\n"
                + "        73, 2,\n"
                + "        68, 2,\n"
                + "        64, 2,\n"
                + "        60, 2,\n"
                + "        56, 2,\n"
                + "        52, 2,\n"
                + "        49, 2};"
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
                    .put("bgInitMapTileSet7", new String[] {
                        "&patterns", "&map", "&palette", "(&patterns_end - &patterns)",
                        "0x0000"
                    });

            boot.get("postLogoCommands")
                    .put("bgInitMapSet", new String[] {
                        "1", "&map2", "(&map2_end - &map2)", "SC_64x32", "0x4000"
                    });

            boot.get("postLogoCommands")
                    .put("bgInitTileSet", new String[] {
                        "1", "&patterns2", "&palette", "0", 
                        "(&patterns2_end - &patterns2)", 
                        "(&palette2_end - &palette2)", 
                        "BG_16COLORS", "0x5000"
                    });

            boot.get("postLogoCommands")
                    .put("setMode7", new String[] {"0"});

            boot.get("postLogoCommands")
                    .put("setScreenOn", null);

            boot.get("postLogoCommands")
                    .put("getTables", null);

            return boot;

        }

        public static Make generateMakefile() {

            return new Make();

        }

        public static void addMakeRules(Make makefile) {

            Make.MakeRule ground = new Make.MakeRule(
                    "ground.pc7",
                    "ground.png",
                    "$(GFXCONV) -p -m -M 7 -i $<"
            );

            Make.MakeRule sky = new Make.MakeRule(
                    "sky.pic",
                    "sky.png",
                    "$(GFXCONV) -s 8 -o 16 -u 16 -m -p -i $<"
            );

            Make.MakeRule bitmaps = new Make.MakeRule(
                    "bitmaps",
                    "ground.pc7 sky.pic",
                    ""
            );

            makefile.addRule(ground);
            makefile.addRule(sky);

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

            Path ground = dataPath.resolve("ground.png");
            Path sky = dataPath.resolve("sky.png");

            cleanBuild(ouptutPath);

            app.addDataToCopy(ground.toString());
            app.addDataToCopy(sky.toString());

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

/**
 * Type created to store the DMA memory
 */
class SnesDmaMemory extends SnesScalarData {

    {
        this.type = "dmaMemory";
    }

    public SnesDmaMemory(String name) {

        this.name = name;
        this.generateSourceCode();

    }

    public SnesDmaMemory(String name, String value) {

        this.name = name;
        this.defaultValue = value;

        this.generateSourceCode();

    }

}
