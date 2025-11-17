package snes_examples.sprite;

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
import javasnes.util.macros.SnesDefine;
import javasnes.util.operators.assign.OperatorAssign;
import javasnes.util.operators.assign.OperatorObj;
import javasnes.util.operators.binary.OperatorBinAnd;
import javasnes.util.operators.logical.OperatorAnd;
import javasnes.util.operators.logical.OperatorGreaterOrEqual;
import javasnes.util.operators.logical.OperatorSmallerOrEqual;
import javasnes.util.operators.math.OperatorAdd;
import javasnes.util.operators.math.OperatorPlus;
import javasnes.util.operators.ternary.OperatorTernary;
import javasnes.util.structures.SnesEnum;
import javasnes.util.structures.SnesLoadExtern;
import javasnes.util.structures.SnesTypedef;
import javasnes.util.types.AppData;
import javasnes.util.types.Processor;
import javasnes.util.types.SnesProcess;
import javasnes.util.types.vars.array.data.SnesCharArray;
import javasnes.util.types.vars.scalar.data.SnesChar;
import javasnes.util.types.vars.scalar.data.SnesVoid;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU16;
import javasnes.util.types.vars.scalar.number.unsigned.SnesU8;
import snes_examples.background.ChangeBackgroundExample;

public class MoveSpriteExample {

    final static SnesChar CHAR = new SnesChar("char");

    public static void main(String[] args) throws Exception {

        App.Builder moveSpriteExample = Config.generateApp();

        Map<String, String> memMapConfig = new HashMap<>();
        memMapConfig.put("name", "MoveSpriteExample    ");

        MemoryMapping memMap = Config.generateMemoryMapping(memMapConfig);

        moveSpriteExample.setMemoryMapping(memMap);

        AppData appData = Config.generateAppData();

        appData.registerData(new Data("gfxsprite", "sprites.pic", true), (byte) 2);
        appData.registerData(new Data("palsprite", "sprites.pal", true), (byte) 2);

        moveSpriteExample.setAppData(appData);

        Boot boot = Config.generateBoot();
        moveSpriteExample.setBoot(boot);

        moveSpriteExample.addSnesMacro(new SnesDefine("FRAMES_PER_ANIMATION 3"));

        SnesInstruction[] globalInstructions = new SnesInstruction[7];

        String[] loadExtern = {
            "gfxsprite", "palsprite", "gfxsprite_end", "palsprite_end"
        };

        globalInstructions[0] = new SnesLoadExtern(loadExtern, CHAR);

        Map<String, List<String>> typedefFields = new LinkedHashMap<>();

        typedefFields.put(
                "s16", new ArrayList<>() {{add("x"); add("y");}}
        );
        typedefFields.put(
                "u16", new ArrayList<>() {{add("gfx_frame"); add("anim_frame");}}
        );
        typedefFields.put(
                "u8", new ArrayList<>() {{add("state"); add("flipx");}}
        );

        SnesTypedef monster = new SnesTypedef(
                "Monster",
                typedefFields
        );

        globalInstructions[1] = monster;

        HashMap<String, String> enumFields1 = new HashMap<>();

        enumFields1.put("W_DOWN", "0");
        enumFields1.put("W_UP", "1");
        enumFields1.put("W_LEFT", "2");
        enumFields1.put("W_RIGHT", "2");

        SnesEnum spriteState = new SnesEnum(
                enumFields1
        );

        globalInstructions[2] = spriteState;

        HashMap<String, String> enumFields2 = new HashMap<>();

        enumFields2.put("SCREEN_TOP", "-16");
        enumFields2.put("SCREEN_BOTTOM", "224");
        enumFields2.put("SCREEN_LEFT", "-16");
        enumFields2.put("SCREEN_RIGHT", "256");

        SnesEnum screenLimits = new SnesEnum(
                enumFields2
        );

        globalInstructions[3] = screenLimits;

        SnesCharArray sprTiles = new SnesCharArray(
                "sprTiles", (short) 9, "{0, 2, 4, 6, 8, 10, 12, 14, 32}"
        );

        globalInstructions[4] = sprTiles;
        globalInstructions[5] = new SnesU16("pad0", "0");
        globalInstructions[6] = new Monster(
                "monster", "{.x = 100, .y = 100}"
        );

        moveSpriteExample.setGlobalInstructions(globalInstructions);

        Processor processor = new Processor();
        SnesProcess[] processes = new SnesProcess[1];

        processes[0] = updateSprite();
        processor.addProcess(processes[0], null);

        moveSpriteExample.setProcessor(processor);
        moveSpriteExample.setSnesProcesses(processes);

        Make makefile = Config.generateMakefile();
        makefile.setRomName("JavaSnes_MoveSpriteExample");

        Config.addMakeRules(makefile);

        moveSpriteExample.setMakefile(makefile);

        Config.build(moveSpriteExample);

    }

    /**
     * A SnesProcess that updates the position of a sprite based on the user
     * input.
     *
     * The process first checks the current state of the user input and updates
     * the position of the sprite accordingly. If the user is pressing the left
     * button, the sprite will move left. If the user is pressing the right
     * button, the sprite will move right. If the user is pressing the up
     * button, the sprite will move up. If the user is pressing the down button,
     * the sprite will move down.
     *
     * The process also updates the animation frame of the sprite based on the
     * user input. If the user is pressing any of the buttons, the animation
     * frame will be incremented. If the animation frame equals
     * FRAMES_PER_ANIMATION, it will be reset to 0.
     *
     * The process finally sets the OAM position of the sprite to its current
     * position and animation frame.
     */
    public static SnesProcess updateSprite() {

        SnesInstruction[] commands = new SnesInstruction[5];

        SnesU16 pad0 = new SnesU16("pad0");

        commands[0] = new OperatorAssign(pad0.name, SnesInput.padsCurrent((byte) 0).sourceCode);

        Map<String, List<SnesInstruction>> movements = new HashMap<>();

        List<SnesInstruction> left = new ArrayList<>();
        List<SnesInstruction> right = new ArrayList<>();
        List<SnesInstruction> up = new ArrayList<>();
        List<SnesInstruction> down = new ArrayList<>();

        left.add(new OperatorObj("monster", "x", new OperatorTernary(
                new OperatorGreaterOrEqual("monster.y", "SCREEN_LEFT"), "monster.x - 1", "monster.x"
        ).getSourceCode()));

        left.add(new OperatorObj("monster", "flipx", "1"));
        left.add(new OperatorObj("monster", "state", "W_LEFT"));

        right.add(new OperatorObj("monster", "x", new OperatorTernary(
                new OperatorSmallerOrEqual("monster.x", "SCREEN_RIGHT"), "monster.x + 1", "monster.x"
        ).getSourceCode()));

        right.add(new OperatorObj("monster", "flipx", "0"));
        right.add(new OperatorObj("monster", "state", "W_RIGHT"));

        up.add(new OperatorObj("monster", "y", new OperatorTernary(
                new OperatorGreaterOrEqual("monster.y", "SCREEN_TOP"), "monster.y - 1", "monster.y"
        ).getSourceCode()));

        up.add(new OperatorObj("monster", "flipx", "0"));
        up.add(new OperatorObj("monster", "state", "W_UP"));

        down.add(new OperatorObj("monster", "y", new OperatorTernary(
                new OperatorSmallerOrEqual("monster.y", "SCREEN_BOTTOM"), "monster.y + 1", "monster.y"
        ).getSourceCode()));

        down.add(new OperatorObj("monster", "flipx", "0"));
        down.add(new OperatorObj("monster", "state", "W_DOWN"));

        left.add(KeyWords.snesBreak);
        right.add(KeyWords.snesBreak);
        up.add(KeyWords.snesBreak);
        down.add(KeyWords.snesBreak);

        movements.put(SnesInput.keys.KEY_LEFT.sourceCode, left);
        movements.put(SnesInput.keys.KEY_RIGHT.sourceCode, right);
        movements.put(SnesInput.keys.KEY_UP.sourceCode, up);
        movements.put(SnesInput.keys.KEY_DOWN.sourceCode, down);

        SnesSwitch moveSprite = new SnesSwitch(
                pad0, movements
        );

        moveSprite.generateSourceCode();

        commands[1] = moveSprite;

        commands[2] = new OperatorObj("monster", "anim_frame", new OperatorTernary(
                new OperatorAnd(
                        pad0.name,
                        new OperatorGreaterOrEqual(
                                "monster.anim_frame", "FRAMES_PER_ANIMATION"
                        ).getSourceCode()
                ), "0", new OperatorTernary(
                        new OperatorBinAnd(pad0, pad0), "monster.anim_frame + 1", "monster.anim_frame"
                ).getSourceCode()
        ).getSourceCode());

        commands[3] = new OperatorObj("monster", "gfx_frame", "sprTiles["
                + new OperatorAdd(new SnesU8("monster.anim_frame"), new SnesU8(new OperatorPlus(
                        new SnesU8("FRAMES_PER_ANIMATION"), new SnesU8("monster.state")
                ).getSourceCode())).getSourceCode() + "]"
        );

        commands[4] = SnesOutput.oamSet(
                0, "monster.x", "monster.y", "3", "monster.flipx", "0", "monster.gfx_frame", "0"
        );

        return new SnesProcess(
                "updateSprite",
                (byte) 0,
                commands
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
                    .put("bgSetDisable", new String[] {"0"});
        
            boot.get("postLogoCommands")
                    .put("oamInitGfxSet", new String[] {
                        "&gfxsprite",
                        "(&gfxsprite_end - &gfxsprite)",
                        "&palsprite",
                        "(&palsprite_end - &palsprite)",
                        "0",
                        "0x0000",
                        SnesOutput.ObjSize.OBJ_SIZE16_L32
                    });

            boot.get("postLogoCommands")
                    .put("oamSet", new String[] {
                        "0",
                        "monster.x",
                        "monster.y",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0"
                    });

            boot.get("postLogoCommands")
                    .put("oamSetEx", new String[] {
                        "0",
                        SnesOutput.ObjState.OBJ_SMALL,
                        SnesOutput.ObjState.OBJ_SHOW
                    });

            boot.get("postLogoCommands")
                    .put("oamSetVisible", new String[] {
                        "0",
                        SnesOutput.ObjState.OBJ_SHOW
                    });

            boot.get("postLogoCommands")
                    .put("setScreenOn", null);

            return boot;

        }

        public static Make generateMakefile() {

            return new Make();

        }

        public static void addMakeRules(Make makefile) {

            Make.MakeRule sprites = new Make.MakeRule(
                    "sprites.pic",
                    "sprites.bmp",
                    "$(GFXCONV) -s 16 -o 16 -u 16 -t bmp -i $<"
            );

            Make.MakeRule bitmaps = new Make.MakeRule(
                    "bitmaps",
                    "sprites.pic",
                    ""
            );

            makefile.addRule(sprites);
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

            Path sprites = dataPath.resolve("sprites.bmp");

            cleanBuild(ouptutPath);

            app.addDataToCopy(sprites.toString());
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
 * Represents a Monster object in SNES C code.
 * 
 * As the object is a costum typedef, we need to create a new class that extends SnesVoid,
 * a generic class for any object.
 */
class Monster extends SnesVoid {

    {
        this.type = "Monster";
    }

    public Monster(String name) {
        this.name = name;
        this.defaultValue = null;
        this.generateSourceCode();
    }

    public Monster(String name, String defaultValue) {
        this.name = name;
        this.defaultValue = defaultValue;
        this.generateSourceCode();
    }

}
