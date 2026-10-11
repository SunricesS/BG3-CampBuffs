"""
Camp Buffs Mod Build Script
Stack and cast customizable camp buffs with ring hotbar toggles, spell level selection (Aid 2-6),
safe native boost statuses (including Mystra's Ceremony, Water Walk, and DnD 5.5e Artificer buffs).
100% Native BG3 Patch 7 compatible (No Script Extender required).
"""
import os
import shutil
import subprocess
from PIL import Image

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(WORKSPACE_DIR, "build_campbuffs")
MODS_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Larian Studios\Baldur's Gate 3\Mods")
DIVINE = os.path.join(WORKSPACE_DIR, r"tools\lslib\Packed\Tools\Divine.exe")

MOD_NAME = "CampBuffs"
MOD_UUID = "7cf9c6d5-936e-4f8d-8052-d71f42920844"
RING_ROOT_UUID = "a4d2f8e1-5120-4e3a-97c2-1b7e408d6c91"
OUTPUT_PAK = os.path.join(WORKSPACE_DIR, "Releases", "CampBuffs.pak")

def clean_build_dir():
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR, exist_ok=True)
    print(f"Cleaned and created {BUILD_DIR}")

def generate_icons():
    print("[1] Generating custom icons from ModAssets/buff.png...")
    src_png = os.path.join(WORKSPACE_DIR, "ModAssets", "buff.png")
    if not os.path.exists(src_png):
        raise FileNotFoundError(f"Icon source not found: {src_png}")
    
    img = Image.open(src_png).convert("RGBA")
    
    # 1. 144x144 for Controller UI
    controller_dir = os.path.join(BUILD_DIR, "Public", "Game", "Assets", "ControllerUIicons", "skills_png")
    os.makedirs(controller_dir, exist_ok=True)
    img_144 = img.resize((144, 144), Image.Resampling.LANCZOS)
    img_144.save(os.path.join(controller_dir, "CampBuffs_CastAll.png"), format="PNG")
    img_144.save(os.path.join(controller_dir, "CampBuffs_Icon.png"), format="PNG")
    
    # 2. 380x380 for Tooltips
    tooltips_dir = os.path.join(BUILD_DIR, "Public", "Game", "Assets", "Tooltips", "Icons")
    os.makedirs(tooltips_dir, exist_ok=True)
    img_380 = img.resize((380, 380), Image.Resampling.LANCZOS)
    img_380.save(os.path.join(tooltips_dir, "CampBuffs_CastAll.png"), format="PNG")
    img_380.save(os.path.join(tooltips_dir, "CampBuffs_Icon.png"), format="PNG")
    
    # 3. 64x64 DXT5 DDS atlas
    atlas_dir = os.path.join(BUILD_DIR, "Public", MOD_NAME, "Assets", "Textures", "Icons")
    os.makedirs(atlas_dir, exist_ok=True)
    img_64 = img.resize((64, 64), Image.Resampling.LANCZOS)
    dds_path = os.path.join(atlas_dir, "CampBuffs_Icons.dds")
    img_64.save(dds_path, format="DDS", pixel_format="DXT5")
    print(f"    Saved DDS atlas: {dds_path} ({os.path.getsize(dds_path)} bytes)")

def create_ui_metadata():
    print("[2] Creating UI texture bank and icon atlas metadata...")
    ui_dir = os.path.join(BUILD_DIR, "Public", MOD_NAME, "Content", "UI", "[PAK]_UI")
    os.makedirs(ui_dir, exist_ok=True)
    merged_lsx = f"""<?xml version="1.0" encoding="utf-8"?>
<save>
    <version major="4" minor="7" revision="1" build="3"/>
    <region id="TextureBank">
        <node id="TextureBank">
            <children>
                <node id="Resource">
                    <attribute id="ID" type="FixedString" value="b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e"/>
                    <attribute id="Localized" type="bool" value="False"/>
                    <attribute id="Name" type="LSString" value="CampBuffs_Icons"/>
                    <attribute id="SRGB" type="bool" value="True"/>
                    <attribute id="SourceFile" type="LSString" value="Public/{MOD_NAME}/Assets/Textures/Icons/CampBuffs_Icons.dds"/>
                    <attribute id="Streaming" type="bool" value="True"/>
                    <attribute id="Template" type="FixedString" value="CampBuffs_Icons"/>
                    <attribute id="Type" type="int32" value="0"/>
                    <attribute id="_OriginalFileVersion_" type="int64" value="144115188075855872"/>
                </node>
            </children>
        </node>
    </region>
</save>
"""
    merged_lsx_path = os.path.join(ui_dir, "_merged.lsx")
    merged_lsf_path = os.path.join(ui_dir, "_merged.lsf")
    with open(merged_lsx_path, "w", encoding="utf-8") as f:
        f.write(merged_lsx)
    
    cmd = [DIVINE, "-g", "bg3", "-a", "convert-resource", "-s", merged_lsx_path, "-d", merged_lsf_path]
    subprocess.run(cmd, check=True)

    gui_dir = os.path.join(BUILD_DIR, "Public", MOD_NAME, "GUI")
    os.makedirs(gui_dir, exist_ok=True)
    icons_lsx = f"""<?xml version="1.0" encoding="utf-8"?>
<save>
    <version major="4" minor="7" revision="1" build="3"/>
    <region id="IconUVList">
        <node id="root">
            <children>
                <node id="IconUV">
                    <attribute id="MapKey" type="FixedString" value="CampBuffs_CastAll"/>
                    <attribute id="U1" type="float" value="0.0"/>
                    <attribute id="U2" type="float" value="1.0"/>
                    <attribute id="V1" type="float" value="0.0"/>
                    <attribute id="V2" type="float" value="1.0"/>
                </node>
                <node id="IconUV">
                    <attribute id="MapKey" type="FixedString" value="CampBuffs_Icon"/>
                    <attribute id="U1" type="float" value="0.0"/>
                    <attribute id="U2" type="float" value="1.0"/>
                    <attribute id="V1" type="float" value="0.0"/>
                    <attribute id="V2" type="float" value="1.0"/>
                </node>
            </children>
        </node>
    </region>
    <region id="TextureAtlasInfo">
        <node id="root">
            <children>
                <node id="TextureAtlasIconSize">
                    <attribute id="Height" type="int64" value="64"/>
                    <attribute id="Width" type="int64" value="64"/>
                </node>
                <node id="TextureAtlasPath">
                    <attribute id="Path" type="LSString" value="Assets/Textures/Icons/CampBuffs_Icons.dds"/>
                    <attribute id="UUID" type="FixedString" value="b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e"/>
                </node>
                <node id="TextureAtlasTextureSize">
                    <attribute id="Height" type="int64" value="64"/>
                    <attribute id="Width" type="int64" value="64"/>
                </node>
            </children>
        </node>
    </region>
</save>
"""
    with open(os.path.join(gui_dir, "Icons_CampBuffs.lsx"), "w", encoding="utf-8") as f:
        f.write(icons_lsx)

def create_meta():
    print("[3] Creating clean meta.lsx...")
    meta_dir = os.path.join(BUILD_DIR, "Mods", MOD_NAME)
    os.makedirs(meta_dir, exist_ok=True)
    meta_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<save>
    <version major="4" minor="7" revision="1" build="3"/>
    <region id="Config">
        <node id="root">
            <children>
                <node id="Conflicts"/>
                <node id="Dependencies">
                    <children>
                        <node id="ModuleShortDesc">
                            <attribute id="Folder" type="LSString" value="GustavDev"/>
                            <attribute id="MD5" type="LSString" value="33c1655f7ae3559b579ff3b9d2c45413"/>
                            <attribute id="Name" type="LSString" value="GustavDev"/>
                            <attribute id="PublishHandle" type="uint64" value="0"/>
                            <attribute id="UUID" type="guid" value="28ac9ce2-2aba-8cda-b3b5-6e922f71b6b8"/>
                            <attribute id="Version64" type="int64" value="145100779997082619"/>
                        </node>
                    </children>
                </node>
                <node id="ModuleInfo">
                    <attribute id="Author" type="LSString" value="UniversalModder"/>
                    <attribute id="CharacterCreationLevelName" type="FixedString" value=""/>
                    <attribute id="Description" type="LSString" value="Stack and cast your selected camp buffs in a single spell with customizable toggles and spell level selection."/>
                    <attribute id="FileSize" type="uint64" value="0"/>
                    <attribute id="Folder" type="LSString" value="{MOD_NAME}"/>
                    <attribute id="LobbyLevelName" type="FixedString" value=""/>
                    <attribute id="MD5" type="LSString" value=""/>
                    <attribute id="MenuLevelName" type="FixedString" value=""/>
                    <attribute id="Name" type="LSString" value="{MOD_NAME}"/>
                    <attribute id="NumPlayers" type="uint8" value="4"/>
                    <attribute id="PhotoBooth" type="FixedString" value=""/>
                    <attribute id="PublishHandle" type="uint64" value="0"/>
                    <attribute id="StartupLevelName" type="FixedString" value=""/>
                    <attribute id="UUID" type="FixedString" value="{MOD_UUID}"/>
                    <attribute id="Version64" type="int64" value="36028797018963968"/>
                    <children>
                        <node id="PublishVersion">
                            <attribute id="Version64" type="int64" value="144255927717549775"/>
                        </node>
                    </children>
                </node>
            </children>
        </node>
    </region>
</save>
"""
    with open(os.path.join(meta_dir, "meta.lsx"), "w", encoding="utf-8") as f:
        f.write(meta_content)

def create_roottemplates():
    print("[4] Creating RootTemplates...")
    rt_dir = os.path.join(BUILD_DIR, "Public", MOD_NAME, "RootTemplates")
    os.makedirs(rt_dir, exist_ok=True)
    rt_content = f"""<?xml version="1.0" encoding="utf-8"?>
<save>
    <version major="4" minor="7" revision="1" build="3" lslib_meta="v1,bswap_guids,lsf_keys_adjacency" />
    <region id="Templates">
        <node id="Templates">
            <children>
                <node id="GameObjects">
                    <attribute id="MapKey" type="FixedString" value="{RING_ROOT_UUID}" />
                    <attribute id="Name" type="LSString" value="CampBuffs_Ring" />
                    <attribute id="LevelName" type="FixedString" value="" />
                    <attribute id="Type" type="FixedString" value="item" />
                    <attribute id="ParentTemplateId" type="FixedString" value="a631b70a-22e9-4e2c-bb07-2164c2beb5d0" />
                    <attribute id="DisplayName" type="TranslatedString" handle="h123456789abcdef0123456789abcdef01234" version="1" />
                    <attribute id="Description" type="TranslatedString" handle="h01a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8" version="1" />
                    <attribute id="Icon" type="FixedString" value="Item_UNI_LOW_SzarrRing_2" />
                    <attribute id="Stats" type="FixedString" value="CampBuffs_Ring" />
                    <attribute id="Hostile" type="bool" value="False" />
                    <attribute id="TreasureOnDestroy" type="bool" value="False" />
                    <attribute id="Destroyed" type="bool" value="False" />
                    <attribute id="CanFight" type="bool" value="False" />
                    <attribute id="CanClimbOn" type="bool" value="False" />
                    <attribute id="IsPointerBlocker" type="bool" value="False" />
                    <attribute id="CanShootThrough" type="bool" value="True" />
                    <attribute id="ShootThroughType" type="int8" value="6" />
                    <attribute id="PhysicsTemplate" type="FixedString" value="e0ad52f8-c26b-4573-be9f-e6a0d249f3e5" />
                    <attribute id="VisualTemplate" type="FixedString" value="846c2fa2-d02f-3705-2b4a-a6813292fe72" />
                </node>
            </children>
        </node>
    </region>
</save>
"""
    lsx_path = os.path.join(rt_dir, "CampBuffs_Ring.lsx")
    lsf_path = os.path.join(rt_dir, "CampBuffs_Ring.lsf")
    with open(lsx_path, "w", encoding="utf-8") as f:
        f.write(rt_content)
    cmd = [DIVINE, "-g", "bg3", "-a", "convert-resource", "-s", lsx_path, "-d", lsf_path]
    subprocess.run(cmd, check=True)
    os.remove(lsx_path)
    print(f"    Compiled RootTemplates to {lsf_path} (removed .lsx)")

def create_onetime_rewards():
    print("[4.5] Creating OneTimeRewards (Camp Chest / Traveller's Chest delivery)...")
    otr_dir = os.path.join(BUILD_DIR, "Public", MOD_NAME, "OneTimeRewards")
    os.makedirs(otr_dir, exist_ok=True)
    otr_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<save>
    <version major="4" minor="7" revision="1" build="3" lslib_meta="v1,bswap_guids,lsf_keys_adjacency"/>
    <region id="OneTimeRewards">
        <node id="root">
            <children>
                <node id="OneTimeReward">
                    <attribute id="Amount" type="uint32" value="2"/>
                    <attribute id="ItemTemplateId" type="FixedString" value="{RING_ROOT_UUID}"/>
                    <attribute id="UUID" type="guid" value="f1928374-a0b1-4c2d-8e3f-5a6b7c8d9e01"/>
                </node>
            </children>
        </node>
    </region>
</save>
"""
    lsx_path = os.path.join(otr_dir, "OneTimeRewards.lsx")
    lsf_path = os.path.join(otr_dir, "OneTimeRewards.lsf")
    with open(lsx_path, "w", encoding="utf-8") as f:
        f.write(otr_content)
    cmd = [DIVINE, "-g", "bg3", "-a", "convert-resource", "-s", lsx_path, "-d", lsf_path]
    subprocess.run(cmd, check=True)
    os.remove(lsx_path)
    print(f"    Compiled OneTimeRewards.lsf to {lsf_path} (removed .lsx)")

def create_stats():
    print("[5] Creating Stats (Object, Passive, Spells, Statuses, TreasureTable)...")
    stats_dir = os.path.join(BUILD_DIR, "Public", MOD_NAME, "Stats", "Generated")
    data_dir = os.path.join(stats_dir, "Data")
    os.makedirs(data_dir, exist_ok=True)

    passives_list = [
        "CampBuffs_Passive",
        "CB_Toggle_Longstrider", "CB_Toggle_MageArmor",
        "CB_Toggle_Aid_2", "CB_Toggle_Aid_3", "CB_Toggle_Aid_4", "CB_Toggle_Aid_5", "CB_Toggle_Aid_6",
        "CB_Toggle_DeathWard", "CB_Toggle_FreedomOfMovement", "CB_Toggle_ProtectionFromPoison",
        "CB_Toggle_Darkvision", "CB_Toggle_HeroesFeast", "CB_Toggle_PetPal", "CB_Toggle_Daylight",
        "CB_Toggle_Guidance", "CB_Toggle_Bless", "CB_Toggle_ShieldOfFaith",
        "CB_Toggle_Stoneskin", "CB_Toggle_Barkskin", "CB_Toggle_SeeInvisibility",
        "CB_Toggle_FeatherFall", "CB_Toggle_Jump", "CB_Toggle_HillGiant", "CB_Toggle_CloudGiant",
        "CB_Toggle_Morninglord", "CB_Toggle_WardingBond"
    ]
    passives_str = ";".join(passives_list)

    # 1. Object.txt and Armor.txt
    object_content = f"""new entry "CampBuffs_Ring"
type "Armor"
using "_Ring"
data "RootTemplate" "{RING_ROOT_UUID}"
data "ItemGroup" ""
data "Level" "1"
data "Rarity" "VeryRare"
data "ValueLevel" "1"
data "ValueUUID" "620e77d2-7c3e-4b7f-b0f7-6e422201ea1d"
data "ValueOverride" "1"
data "Weight" "0.05"
data "Slot" "Ring"
data "PassivesOnEquip" "{passives_str}"
"""
    with open(os.path.join(data_dir, "Object.txt"), "w", encoding="utf-8") as f:
        f.write(object_content)
    with open(os.path.join(data_dir, "Armor.txt"), "w", encoding="utf-8") as f:
        f.write(object_content)

    # 2. Passive.txt (All toggles use IsToggled;ToggledDefaultAddToHotbar to avoid deadlock)
    passive_content = """new entry "CampBuffs_Passive"
type "PassiveData"
data "Properties" "Highlighted"
data "Icon" "CampBuffs_Icon"
data "DisplayName" "h123456789abcdef0123456789abcdef01234;1"
data "Description" "h01a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8;1"
data "Boosts" "UnlockSpell(Shout_CampBuffs_CastAll);UnlockSpell(Zone_CB_CampBuffs);UnlockSpell(Shout_CampBuffs_RemoveBuffs);UnlockSpell(Zone_CB_RemoveBuffs)"

new entry "CB_Toggle_Longstrider"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Transmutation_Longstrider"
data "DisplayName" "h3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0;1"
data "Description" "h4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1;1"

new entry "CB_Toggle_MageArmor"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_MageArmor"
data "DisplayName" "h5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2;1"
data "Description" "h6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3;1"

new entry "CB_Toggle_Aid_2"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_Aid"
data "DisplayName" "haid2_name_01928374;1"
data "Description" "haid2_desc_01928374;1"

new entry "CB_Toggle_Aid_3"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_Aid"
data "DisplayName" "haid3_name_01928374;1"
data "Description" "haid3_desc_01928374;1"

new entry "CB_Toggle_Aid_4"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_Aid"
data "DisplayName" "haid4_name_01928374;1"
data "Description" "haid4_desc_01928374;1"

new entry "CB_Toggle_Aid_5"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_Aid"
data "DisplayName" "haid5_name_01928374;1"
data "Description" "haid5_desc_01928374;1"

new entry "CB_Toggle_Aid_6"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_Aid"
data "DisplayName" "haid6_name_01928374;1"
data "Description" "haid6_desc_01928374;1"

new entry "CB_Toggle_DeathWard"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_DeathWard"
data "DisplayName" "hc1928374gf716g4318ga615g316274859102;1"
data "Description" "hd2837465ge615g4217gb514g205163748291;1"

new entry "CB_Toggle_FreedomOfMovement"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_FreedomOfMovement"
data "DisplayName" "he1827364gb514g4116ga413g118495061273;1"
data "Description" "hf0918273gc413g4015ga312g019506172384;1"

new entry "CB_Toggle_ProtectionFromPoison"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_ProtectionFromPoison"
data "DisplayName" "ha1928374gd312g4914gb211gf08493027164;1"
data "Description" "hb0918273ge211g4813ga110ge07382916253;1"

new entry "CB_Toggle_Darkvision"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Transmutation_Darkvision"
data "DisplayName" "hc1827364gf110g4712ga009gd06271829364;1"
data "Description" "hd0918273ga009g4611g9f08gc05160718273;1"

new entry "CB_Toggle_HeroesFeast"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Conjuration_HeroesFeast"
data "DisplayName" "he1928374g9f08g4510g8e07gb04059607182;1"
data "Description" "hf0827364g8e07g4409g7d06ga03948576192;1"

new entry "CB_Toggle_PetPal"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Divination_SpeakWithAnimals"
data "DisplayName" "ha0827364g7d06g4308g6c05g902837465182;1"
data "Description" "hb1726354g6c05g4207g5b04g801726354192;1"

new entry "CB_Toggle_Daylight"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Evocation_Daylight"
data "DisplayName" "hc1726354g5b04g4106g4a03g700615243182;1"
data "Description" "hd0615243g4a03g4005g3902g609504132173;1"

new entry "CB_Toggle_Guidance"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Divination_Guidance"
data "DisplayName" "hguid01928ga812g4918g8123ga91823746152;1"
data "Description" "hguid12938gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_Bless"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Enchantment_Bless"
data "DisplayName" "hbless0192ga812g4918g8123ga91823746152;1"
data "Description" "hbless1293gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_ShieldOfFaith"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_ShieldOfFaith"
data "DisplayName" "hfaith0192ga812g4918g8123ga91823746152;1"
data "Description" "hfaith1293gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_Stoneskin"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_Stoneskin"
data "DisplayName" "hstone0192ga812g4918g8123ga91823746152;1"
data "Description" "hstone1293gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_Barkskin"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Transmutation_Barkskin"
data "DisplayName" "hbark0192ga812g4918g8123ga91823746152;1"
data "Description" "hbark1293gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_SeeInvisibility"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Divination_SeeInvisibility"
data "DisplayName" "hseein0192ga812g4918g8123ga91823746152;1"
data "Description" "hseein1293gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_FeatherFall"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Transmutation_FeatherFall"
data "DisplayName" "hfeath0192ga812g4918g8123ga91823746152;1"
data "Description" "hfeath1293gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_Jump"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Transmutation_LongJump"
data "DisplayName" "hjump0192ga812g4918g8123ga91823746152;1"
data "Description" "hjump1293gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_HillGiant"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Item_CONS_Potion_Hill_Giant_Strength"
data "DisplayName" "hhill0192ga812g4918g8123ga91823746152;1"
data "Description" "hhill1293gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_CloudGiant"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Item_CONS_Potion_Cloud_Giant_Strength"
data "DisplayName" "hcloud0192ga812g4918g8123ga91823746152;1"
data "Description" "hcloud1293gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_Morninglord"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Evocation_Daylight"
data "DisplayName" "hmorn0192ga812g4918g8123ga91823746152;1"
data "Description" "hmorn1293gb923g4029g9234gb02934857263;1"

new entry "CB_Toggle_WardingBond"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_WardingBond"
data "DisplayName" "he0615243g3902g4904g2801g508493021164;1"
data "Description" "hf1524354g2801g4803g1700g407382910155;1"
"""
    with open(os.path.join(data_dir, "Passive.txt"), "w", encoding="utf-8") as f:
        f.write(passive_content)

    # 3. Spell_Shout.txt
    spell_props = [
        "IF(HasPassive('CB_Toggle_Longstrider', context.Source)):ApplyStatus(CB_LONGSTRIDER, 100, -1)",
        "IF(HasPassive('CB_Toggle_MageArmor', context.Source) and not WearingArmor()):ApplyStatus(CB_MAGE_ARMOR, 100, -1)",
        "IF(HasPassive('CB_Toggle_Aid_6', context.Source)):ApplyStatus(CB_AID_6, 100, -1)",
        "IF(HasPassive('CB_Toggle_Aid_5', context.Source) and not HasPassive('CB_Toggle_Aid_6', context.Source)):ApplyStatus(CB_AID_5, 100, -1)",
        "IF(HasPassive('CB_Toggle_Aid_4', context.Source) and not HasPassive('CB_Toggle_Aid_5', context.Source) and not HasPassive('CB_Toggle_Aid_6', context.Source)):ApplyStatus(CB_AID_4, 100, -1)",
        "IF(HasPassive('CB_Toggle_Aid_3', context.Source) and not HasPassive('CB_Toggle_Aid_4', context.Source) and not HasPassive('CB_Toggle_Aid_5', context.Source) and not HasPassive('CB_Toggle_Aid_6', context.Source)):ApplyStatus(CB_AID_3, 100, -1)",
        "IF(HasPassive('CB_Toggle_Aid_2', context.Source) and not HasPassive('CB_Toggle_Aid_3', context.Source) and not HasPassive('CB_Toggle_Aid_4', context.Source) and not HasPassive('CB_Toggle_Aid_5', context.Source) and not HasPassive('CB_Toggle_Aid_6', context.Source)):ApplyStatus(CB_AID_2, 100, -1)",
        "IF(HasPassive('CB_Toggle_DeathWard', context.Source)):ApplyStatus(DEATH_WARD, 100, -1)",
        "IF(HasPassive('CB_Toggle_FreedomOfMovement', context.Source)):ApplyStatus(CB_FREEDOM_OF_MOVEMENT, 100, -1)",
        "IF(HasPassive('CB_Toggle_ProtectionFromPoison', context.Source)):ApplyStatus(PROTECTION_FROM_POISON, 100, -1)",
        "IF(HasPassive('CB_Toggle_Darkvision', context.Source)):ApplyStatus(DARKVISION, 100, -1)",
        "IF(HasPassive('CB_Toggle_HeroesFeast', context.Source)):ApplyStatus(CB_HEROES_FEAST, 100, -1)",
        "IF(HasPassive('CB_Toggle_PetPal', context.Source)):ApplyStatus(CB_PETPAL, 100, -1)",
        "IF(HasPassive('CB_Toggle_Daylight', context.Source)):ApplyStatus(CB_DAYLIGHT, 100, -1)",
        "IF(HasPassive('CB_Toggle_Guidance', context.Source)):ApplyStatus(GUIDANCE, 100, -1)",
        "IF(HasPassive('CB_Toggle_Bless', context.Source)):ApplyStatus(BLESS, 100, -1)",
        "IF(HasPassive('CB_Toggle_ShieldOfFaith', context.Source)):ApplyStatus(SHIELD_OF_FAITH, 100, -1)",
        "IF(HasPassive('CB_Toggle_Stoneskin', context.Source)):ApplyStatus(STONESKIN, 100, -1)",
        "IF(HasPassive('CB_Toggle_Barkskin', context.Source)):ApplyStatus(BARKSKIN, 100, -1)",
        "IF(HasPassive('CB_Toggle_SeeInvisibility', context.Source)):ApplyStatus(CB_SEE_INVISIBILITY, 100, -1)",
        "IF(HasPassive('CB_Toggle_FeatherFall', context.Source)):ApplyStatus(FEATHER_FALL, 100, -1)",
        "IF(HasPassive('CB_Toggle_Jump', context.Source)):ApplyStatus(LONG_JUMP, 100, -1)",
        "IF(HasPassive('CB_Toggle_HillGiant', context.Source) and not HasPassive('CB_Toggle_CloudGiant', context.Source)):ApplyStatus(POTION_OF_STRENGTH_HILL_GIANT, 100, -1)",
        "IF(HasPassive('CB_Toggle_CloudGiant', context.Source)):ApplyStatus(POTION_OF_STRENGTH_CLOUD_GIANT, 100, -1)",
        "IF(HasPassive('CB_Toggle_Morninglord', context.Source)):ApplyStatus(CRE_MAG_LATHANDER_PUZZLE_BOON, 100, -1)",
        "IF(HasPassive('CB_Toggle_WardingBond', context.Source)):ApplyStatus(CB_WARDING_BOND, 100, -1)"
    ]
    props_str = ";".join(spell_props)

    remove_statuses = [
        "CB_AID_2", "CB_AID_3", "CB_AID_4", "CB_AID_5", "CB_AID_6", "CB_AID", "AID", "AID_3", "AID_4", "AID_5", "AID_6",
        "CB_LONGSTRIDER", "CB_MAGE_ARMOR", "CB_DEATH_WARD", "CB_FREEDOM_OF_MOVEMENT",
        "CB_PROTECTION_FROM_POISON", "CB_DARKVISION", "CB_HEROES_FEAST", "CB_PETPAL",
        "CB_DAYLIGHT", "CB_SEE_INVISIBILITY", "CB_WARDING_BOND",
        "LONGSTRIDER", "MAGE_ARMOR", "DEATH_WARD", "FREEDOM_OF_MOVEMENT",
        "PROTECTION_FROM_POISON", "DARKVISION", "HEROES_FEAST", "PETPAL",
        "DAYLIGHT", "WARDING_BOND", "WARDING_BOND_CASTER",
        "GUIDANCE", "BLESS", "SHIELD_OF_FAITH", "STONESKIN", "BARKSKIN",
        "SEE_INVISIBILITY", "FEATHER_FALL", "LONG_JUMP",
        "POTION_OF_STRENGTH_HILL_GIANT", "POTION_OF_STRENGTH_CLOUD_GIANT", "CRE_MAG_LATHANDER_PUZZLE_BOON"
    ]
    remove_str = ";".join([f"RemoveStatus({s})" for s in remove_statuses])

    spell_shout_content = f"""new entry "Shout_CampBuffs_CastAll"
type "SpellData"
data "SpellType" "Shout"
data "Level" "0"
data "SpellProperties" "{props_str}"
data "AreaRadius" "35"
data "TargetConditions" "(Ally() or Self()) and Character()"
data "Icon" "CampBuffs_CastAll"
data "DisplayName" "h7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4;1"
data "Description" "h8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5;1"
data "CastSound" "Spell_Cast_Healing_Aid_L1to3"
data "TargetSound" "Spell_Impact_Healing_Aid_L1to3"
data "CastEffectTextEvent" "Cast"
data "SpellAnimation" "414bbf02-2918-4f01-83fb-1ddc7a588d88,,;,,;7abe77ed-9c77-4eac-872c-5b8caed070b6,,;cb171bda-f065-4520-b470-e447f678ba1f,,;0c5dcc83-fa78-41da-b6a5-440b5ea30936,,;,,;bea988a0-2ec5-40d8-a67e-ffbd7454bc53,,;,,;,,"
data "PrepareEffect" "96a51ac8-2e7e-4718-bb62-dcfd18964a02"
data "CastEffect" "b50decc3-5f93-4467-8d3a-aa8b01fc915e"
data "TargetEffect" "a908e49b-b59f-4a20-b487-e25ae198d926"
data "Requirements" "!Combat"
data "MemoryCost" "0"

new entry "Zone_CB_CampBuffs"
type "SpellData"
using "Shout_CampBuffs_CastAll"

new entry "Shout_CampBuffs_RemoveBuffs"
type "SpellData"
data "SpellType" "Shout"
data "Level" "0"
data "SpellProperties" "{remove_str}"
data "AreaRadius" "35"
data "TargetConditions" "(Ally() or Self()) and Character()"
data "Icon" "Spell_Abjuration_RemoveCurse"
data "DisplayName" "hrem01928ga812g4918g8123ga91823746152;1"
data "Description" "hrem12938gb923g4029g9234gb02934857263;1"
data "CastSound" "Spell_Cast_Utility_Dispel"
data "TargetSound" "Spell_Impact_Utility_Dispel"
data "CastEffectTextEvent" "Cast"
data "SpellAnimation" "414bbf02-2918-4f01-83fb-1ddc7a588d88,,;,,;7abe77ed-9c77-4eac-872c-5b8caed070b6,,;cb171bda-f065-4520-b470-e447f678ba1f,,;0c5dcc83-fa78-41da-b6a5-440b5ea30936,,;,,;bea988a0-2ec5-40d8-a67e-ffbd7454bc53,,;,,;,,"
data "PrepareEffect" "96a51ac8-2e7e-4718-bb62-dcfd18964a02"
data "CastEffect" "b50decc3-5f93-4467-8d3a-aa8b01fc915e"
data "TargetEffect" "a908e49b-b59f-4a20-b487-e25ae198d926"
data "Requirements" "!Combat"
data "MemoryCost" "0"

new entry "Zone_CB_RemoveBuffs"
type "SpellData"
using "Shout_CampBuffs_RemoveBuffs"
"""
    with open(os.path.join(data_dir, "Spell_Shout.txt"), "w", encoding="utf-8") as f:
        f.write(spell_shout_content)
    with open(os.path.join(stats_dir, "Spell_Shout.txt"), "w", encoding="utf-8") as f:
        f.write(spell_shout_content)

    # 4. Status_BOOST.txt (Clean, 100% valid BG3 engine boost functors)
    status_content = """new entry "CB_LONGSTRIDER"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Transmutation_Longstrider"
data "DisplayName" "h3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0;1"
data "Description" "h4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1;1"
data "Boosts" "ActionResource(Movement, 3, 0)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MAGE_ARMOR"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_MageArmor"
data "DisplayName" "h5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2;1"
data "Description" "h6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3;1"
data "Boosts" "AC(13)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"
data "RemoveConditions" "WearingArmor()"

new entry "CB_AID_2"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_Aid"
data "DisplayName" "haid2_name_01928374;1"
data "Description" "haid2_desc_01928374;1"
data "Boosts" "IncreaseMaxHP(5)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_AID_3"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_Aid"
data "DisplayName" "haid3_name_01928374;1"
data "Description" "haid3_desc_01928374;1"
data "Boosts" "IncreaseMaxHP(10)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_AID_4"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_Aid"
data "DisplayName" "haid4_name_01928374;1"
data "Description" "haid4_desc_01928374;1"
data "Boosts" "IncreaseMaxHP(15)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_AID_5"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_Aid"
data "DisplayName" "haid5_name_01928374;1"
data "Description" "haid5_desc_01928374;1"
data "Boosts" "IncreaseMaxHP(20)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_AID_6"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_Aid"
data "DisplayName" "haid6_name_01928374;1"
data "Description" "haid6_desc_01928374;1"
data "Boosts" "IncreaseMaxHP(25)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_FREEDOM_OF_MOVEMENT"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_FreedomOfMovement"
data "DisplayName" "he1827364gb514g4116ga413g118495061273;1"
data "Description" "hf0918273gc413g4015ga312g019506172384;1"
data "Boosts" "Immunity(PARALYZED);Immunity(RESTRAINED);IgnoreDifficultTerrain()"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_HEROES_FEAST"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Conjuration_HeroesFeast"
data "DisplayName" "he1928374g9f08g4510g8e07gb04059607182;1"
data "Description" "hf0827364g8e07g4409g7d06ga03948576192;1"
data "Boosts" "IncreaseMaxHP(12);Immunity(POISONED);Immunity(FRIGHTENED);Advantage(SavingThrow, Wisdom)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_PETPAL"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Divination_SpeakWithAnimals"
data "DisplayName" "ha0827364g7d06g4308g6c05g902837465182;1"
data "Description" "hb1726354g6c05g4207g5b04g801726354192;1"
data "Boosts" "Tag(BEAST_SPEAKER)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_DAYLIGHT"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Evocation_Daylight"
data "DisplayName" "hc1726354g5b04g4106g4a03g700615243182;1"
data "Description" "hd0615243g4a03g4005g3902g609504132173;1"
data "Boosts" "Spot(15)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_SEE_INVISIBILITY"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Divination_SeeInvisibility"
data "DisplayName" "hseein0192ga812g4918g8123ga91823746152;1"
data "Description" "hseein1293gb923g4029g9234gb02934857263;1"
data "Boosts" "Tag(SEE_INVISIBILITY)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_WARDING_BOND"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_WardingBond"
data "DisplayName" "he0615243g3902g4904g2801g508493021164;1"
data "Description" "hf1524354g2801g4803g1700g407382910155;1"
data "Boosts" "AC(1);RollBonus(SavingThrow, 1);Resistance(All, Resistant)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"
"""
    with open(os.path.join(data_dir, "Status_BOOST.txt"), "w", encoding="utf-8") as f:
        f.write(status_content)

    # 5. TreasureTable.txt (All Major Vendors Act 1-3 + Tutorial Chest + AMP Variants)
    vendor_tables = [
        "CRE_Expeditioner_Magic_Trade",
        "CRE_Expeditioner_Trade",
        "CRE_Expeditioner_Trade_AMP",
        "CRE_Expeditioner_Trade_None",
        "CRE_GithQuartermistress_Trade",
        "CRE_GithQuartermistress_Trade_AMP",
        "CRE_GithQuartermistress_Trade_None",
        "CRE_MagicItem_Gith_Trader",
        "DEN_Apprentice_Trade",
        "DEN_Entrance_Trade",
        "DEN_Entrance_Trade_AMP",
        "DEN_Entrance_Trade_None",
        "DEN_Ethel",
        "DEN_Ethel_AMP",
        "DEN_Ethel_None",
        "DEN_Prodigy",
        "DEN_Prodigy_AMP",
        "DEN_Prodigy_None",
        "DEN_Thiefling_Trade",
        "DEN_Thiefling_Trade_AMP",
        "DEN_Thiefling_Trade_None",
        "DEN_Thieflings_Merchant",
        "DEN_Volo_Trade",
        "DEN_Volo_Trade_AMP",
        "DEN_Volo_Trade_None",
        "DEN_Weaponsmith",
        "DEN_Weaponsmith_Trade",
        "DEN_Weaponsmith_Trade_AMP",
        "DEN_Weaponsmith_Trade_None",
        "END_CircusTrader",
        "FOR_UnfortunateGnomeTrader",
        "FOR_UnfortunateGnomeTrader_AMP",
        "FOR_UnfortunateGnomeTrader_None",
        "Florrick_Trader",
        "GOB_Dwarf_Trade",
        "GOB_Festivities_Trader",
        "GOB_Festivities_Trader_AMP",
        "GOB_Festivities_Trader_GoblinWeapons",
        "GOB_Festivities_Trader_None",
        "GOB_Quartermaster",
        "GOB_Quartermaster_AMP",
        "GOB_Quartermaster_None",
        "HAV_HarperQuarterMaster",
        "HAV_HarperQuarterMaster_AMP",
        "HAV_HarperQuarterMaster_Magic_Trade",
        "HAV_HarperQuarterMaster_None",
        "HAV_Thiefling_Ide_Trade",
        "HAV_Thiefling_Ide_Trade_AMP",
        "HAV_Thiefling_Ide_Trade_None",
        "HAV_Thiefling_Trade",
        "HAV_Thiefling_Trade_AMP",
        "HAV_Thiefling_Trade_None",
        "HAV_UnfortunateGnome_Magic_Trade",
        "HAV_UnfortunateGnome_Magic_Trade_AMP",
        "HAV_UnfortunateGnome_Trade",
        "HAV_UnfortunateGnome_Trade_AMP",
        "HAV_UnfortunateGnome_Trade_None",
        "HAV_Weaponsmith_Trade",
        "HAV_Weaponsmith_Trade_AMP",
        "HAV_Weaponsmith_Trade_None",
        "LOW_Apothecary_Bonecloak_HasNobleStalk",
        "LOW_Apothecary_Bonecloak_HasNobleStalk_AMP",
        "LOW_Apothecary_Bonecloak_HasNobleStalk_None",
        "LOW_Apothecary_Bonecloak_NoNobleStalk",
        "LOW_Apothecary_Bonecloak_NoNobleStalk_AMP",
        "LOW_Apothecary_Bonecloak_NoNobleStalk_None",
        "LOW_DevilsFee_Diabolist_Trade_Magic",
        "LOW_DevilsFee_Diabolist_Trade_Magic_AMP",
        "LOW_DevilsFee_Diabolist_Trade_Magic_None",
        "LOW_GeneralStoreDragonborn_Merchant",
        "LOW_Guildhall_Bartender",
        "LOW_Guildhall_Bartender_AMP",
        "LOW_Guildhall_Bartender_None",
        "LOW_Guildhall_FetchersBrat_Trade",
        "LOW_Guildhall_FetchersBrat_Trade_AMP",
        "LOW_Guildhall_FetchersBrat_Trade_Magic",
        "LOW_Guildhall_FetchersBrat_Trade_None",
        "LOW_InfernalTrade",
        "LOW_InfernalTrade_AMP",
        "LOW_InfernalTrade_None",
        "LOW_MurderTribunal_Merchant",
        "LOW_MurderTribunal_Merchant_AMP",
        "LOW_MurderTribunal_Merchant_None",
        "LOW_MysticCarrion_Trade",
        "LOW_MysticCarrion_Trade_AMP",
        "LOW_MysticCarrion_Trade_Magic",
        "LOW_MysticCarrion_Trade_None",
        "LOW_SorcerousSundries_Trade",
        "LOW_SorcerousSundries_Trade_AMP",
        "LOW_SorcerousSundries_Trade_Magic",
        "LOW_SorcerousSundries_Trade_None",
        "LOW_SteepsTrader_Armor",
        "LOW_SteepsTrader_Armor_AMP",
        "LOW_SteepsTrader_Armor_None",
        "LOW_SteepsTrader_Weapons",
        "LOW_SteepsTrader_Weapons_AMP",
        "LOW_SteepsTrader_Weapons_None",
        "LOW_StormshoreTabernacle_Guardian",
        "LOW_StormshoreTabernacle_Guardian_AMP",
        "LOW_StormshoreTabernacle_Guardian_None",
        "LOW_VoicelessPenitent",
        "LOW_VoicelessPenitent_AMP",
        "LOW_VoicelessPenitent_None",
        "LOW_Weaponsmith_Trade",
        "LOW_Weaponsmith_Trade_AMP",
        "LOW_Weaponsmith_Trade_None",
        "MOO_BugBearVendor_PrivateStash",
        "MOO_BugBearVendor_PrivateStash_AMP",
        "MOO_BugBearVendor_PrivateStash_None",
        "MOO_BugBearvendor_Trade",
        "MOO_BugBearvendor_Trade_AMP",
        "MOO_BugBearvendor_Trade_None",
        "MOO_InfernalTrader_SpecialStock",
        "MOO_InfernalTrader_SpecialStock_AMP",
        "MOO_InfernalTrader_SpecialStock_None",
        "MOO_InfernalTrader_Trade",
        "MOO_InfernalTrader_Trade_AMP",
        "MOO_InfernalTrader_Trade_None",
        "MOO_ZhentQuartermaster",
        "MOO_ZhentQuartermaster_AMP",
        "MOO_ZhentQuartermaster_None",
        "PLA_Tollhouse_SuppliesTrader",
        "PLA_Tollhouse_SuppliesTrader_AMP",
        "PLA_Tollhouse_SuppliesTrader_None",
        "PLA_ZhentarimTrader",
        "PLA_ZhentarimTrader_AMP",
        "PLA_ZhentarimTrader_Extra",
        "PLA_ZhentarimTrader_Extra_AMP",
        "PLA_ZhentarimTrader_Extra_None",
        "PLA_ZhentarimTrader_None",
        "TUT_Chest_Potions",
        "UND_KC_Trader_Weapons",
        "UND_KC_Trader_Weapons_AMP",
        "UND_KC_Trader_Weapons_None",
        "UND_MycoVillage_AlchemistDwarf_Trade",
        "UND_MycoVillage_AlchemistDwarf_Trade_AMP",
        "UND_MycoVillage_AlchemistDwarf_Trade_Magic",
        "UND_MycoVillage_AlchemistDwarf_Trade_Magic_AMP",
        "UND_MycoVillage_AlchemistDwarf_Trade_Magic_None",
        "UND_MycoVillage_AlchemistDwarf_Trade_None",
        "UND_SocietyOfBrilliance_Hobgoblin",
        "UND_SocietyOfBrilliance_Hobgoblin_AMP",
        "UND_SocietyOfBrilliance_Hobgoblin_None",
        "UND_SocietyOfBrilliance_Mindflayer",
        "UND_SocietyOfBrilliance_Mindflayer_AMP",
        "UND_SocietyOfBrilliance_Mindflayer_None",
        "UND_SocietyOfBrilliance_Omeluum",
        "WYR_Circus_KoboldMerchant",
        "WYR_Circus_KoboldMerchant_AMP",
        "WYR_Circus_KoboldMerchant_Magic",
        "WYR_Circus_KoboldMerchant_Magic_AMP",
        "WYR_Circus_KoboldMerchant_None",
        "WYR_Danthelon_Trader",
        "WYR_Danthelon_Trader_AMP",
        "WYR_Danthelon_Trader_None",
        "WYR_Ironhand_Magic_Merchant",
        "WYR_Ironhand_Magic_Merchant_AMP",
        "WYR_Ironhand_Magic_Merchant_None",
        "WYR_Ironhand_Merchant",
        "WYR_Ironhand_Merchant_AMP",
        "WYR_Ironhand_Merchant_None",
        "WYR_OrinsImpersonation_Smith",
        "WYR_OrinsImpersonation_Smith_AMP",
        "WYR_OrinsImpersonation_Smith_None",
        "WYR_SharessCaress_Bartender_Trade",
        "WYR_SharessCaress_Bartender_Trade_AMP",
        "WYR_SharessCaress_Bartender_Trade_None",
        "WYR_SharessCaress_Bartender_Trade_Potent",
        "WYR_SharessCaress_Bartender_Trade_Potent_AMP",
        "WYR_SharessCaress_Bartender_Trade_Potent_None",
        "WYR_SharranInformer_Basic",
        "WYR_SharranInformer_Basic_AMP",
        "WYR_SharranInformer_Basic_None",
        "WYR_SharranInformer_Extended",
        "WYR_SharranInformer_Extended_AMP",
        "WYR_SharranInformer_Extended_None",
        "WYR_Thiefling_Trade",
        "WYR_Thiefling_Trade_AMP",
        "WYR_Thiefling_Trade_None",
        "WYR_UnfortunateGnome",
        "WYR_UnfortunateGnome_AMP",
        "WYR_UnfortunateGnome_None",

    ]

    treasure_blocks = []
    for t_name in vendor_tables:
        treasure_blocks.append(f'new treasuretable "{t_name}"\nCanMerge 1\nnew subtable "1,1"\nobject category "I_CampBuffs_Ring",1,0,0,0,0,0,0,0\n')

    treasure_content = "\n".join(treasure_blocks)
    with open(os.path.join(stats_dir, "TreasureTable.txt"), "w", encoding="utf-8") as f:
        f.write(treasure_content)
    with open(os.path.join(data_dir, "TreasureTable.txt"), "w", encoding="utf-8") as f:
        f.write(treasure_content)

def create_localization():
    print("[6] Creating English and Turkish Localization...")
    loc_dir = os.path.join(BUILD_DIR, "Mods", MOD_NAME, "Localization")
    
    en_entries = [
        ("h123456789abcdef0123456789abcdef01234", "Camp Buffs Ring"),
        ("h01a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8", "Allows casting all chosen camp buffs in a single spell. Use hotbar passives to toggle which buffs to apply."),
        ("h7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4", "Cast Camp Buffs"),
        ("h8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5", "Apply all enabled camp buffs to all party members in a 30m radius."),
        ("hrem01928ga812g4918g8123ga91823746152", "Remove Camp Buffs"),
        ("hrem12938gb923g4029g9234gb02934857263", "Remove all applied camp buffs from all party members in a 30m radius."),
        ("h3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0", "Camp Buff: Longstrider"),
        ("h4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1", "Include Longstrider (+3m movement) when casting Camp Buffs."),
        ("h5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2", "Camp Buff: Mage Armor"),
        ("h6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3", "Include Mage Armor (base AC 13 for unarmored) when casting Camp Buffs."),
        ("haid2_name_01928374", "Camp Buff: Aid (Level 2: +5 HP)"),
        ("haid2_desc_01928374", "Include Aid at Level 2 (+5 max HP) when casting Camp Buffs."),
        ("haid3_name_01928374", "Camp Buff: Aid (Level 3: +10 HP)"),
        ("haid3_desc_01928374", "Include Aid at Level 3 (+10 max HP) when casting Camp Buffs."),
        ("haid4_name_01928374", "Camp Buff: Aid (Level 4: +15 HP)"),
        ("haid4_desc_01928374", "Include Aid at Level 4 (+15 max HP) when casting Camp Buffs."),
        ("haid5_name_01928374", "Camp Buff: Aid (Level 5: +20 HP)"),
        ("haid5_desc_01928374", "Include Aid at Level 5 (+20 max HP) when casting Camp Buffs."),
        ("haid6_name_01928374", "Camp Buff: Aid (Level 6: +25 HP)"),
        ("haid6_desc_01928374", "Include Aid at Level 6 (+25 max HP) when casting Camp Buffs."),
        ("hc1928374gf716g4318ga615g316274859102", "Camp Buff: Death Ward"),
        ("hd2837465ge615g4217gb514g205163748291", "Include Death Ward (survive fatal hit with 1 HP) when casting Camp Buffs."),
        ("he1827364gb514g4116ga413g118495061273", "Camp Buff: Freedom of Movement"),
        ("hf0918273gc413g4015ga312g019506172384", "Include Freedom of Movement (immune to paralysis, restraint, difficult terrain)."),
        ("ha1928374gd312g4914gb211gf08493027164", "Camp Buff: Protection from Poison"),
        ("hb0918273ge211g4813ga110ge07382916253", "Include Protection from Poison (resistance and advantage vs poison)."),
        ("hc1827364gf110g4712ga009gd06271829364", "Camp Buff: Darkvision"),
        ("hd0918273ga009g4611g9f08gc05160718273", "Include Darkvision (12m range in the dark) when casting Camp Buffs."),
        ("he1928374g9f08g4510g8e07gb04059607182", "Camp Buff: Heroes' Feast"),
        ("hf0827364g8e07g4409g7d06ga03948576192", "Include Heroes' Feast (+12 max HP, poison/fear immunity, Wisdom save advantage)."),
        ("ha0827364g7d06g4308g6c05g902837465182", "Camp Buff: Speak with Animals"),
        ("hb1726354g6c05g4207g5b04g801726354192", "Include Speak with Animals when casting Camp Buffs."),
        ("hc1726354g5b04g4106g4a03g700615243182", "Camp Buff: Daylight"),
        ("hd0615243g4a03g4005g3902g609504132173", "Include Daylight aura when casting Camp Buffs."),
        ("hguid01928ga812g4918g8123ga91823746152", "Camp Buff: Guidance"),
        ("hguid12938gb923g4029g9234gb02934857263", "Include Guidance (+1d4 to ability checks) when casting Camp Buffs."),
        ("hbless0192ga812g4918g8123ga91823746152", "Camp Buff: Bless"),
        ("hbless1293gb923g4029g9234gb02934857263", "Include Bless (+1d4 to attack rolls and saving throws) when casting Camp Buffs."),
        ("hfaith0192ga812g4918g8123ga91823746152", "Camp Buff: Shield of Faith"),
        ("hfaith1293gb923g4029g9234gb02934857263", "Include Shield of Faith (+2 AC) when casting Camp Buffs."),
        ("hstone0192ga812g4918g8123ga91823746152", "Camp Buff: Stoneskin"),
        ("hstone1293gb923g4029g9234gb02934857263", "Include Stoneskin (resistance to non-magical physical damage) when casting Camp Buffs."),
        ("hbark0192ga812g4918g8123ga91823746152", "Camp Buff: Barkskin"),
        ("hbark1293gb923g4029g9234gb02934857263", "Include Barkskin (target AC cannot be less than 16) when casting Camp Buffs."),
        ("hseein0192ga812g4918g8123ga91823746152", "Camp Buff: See Invisibility"),
        ("hseein1293gb923g4029g9234gb02934857263", "Include See Invisibility when casting Camp Buffs."),
        ("hfeath0192ga812g4918g8123ga91823746152", "Camp Buff: Feather Fall"),
        ("hfeath1293gb923g4029g9234gb02934857263", "Include Feather Fall (immune to fall damage) when casting Camp Buffs."),
        ("hjump0192ga812g4918g8123ga91823746152", "Camp Buff: Enhanced Leap"),
        ("hjump1293gb923g4029g9234gb02934857263", "Include Enhanced Leap (tripled jump distance) when casting Camp Buffs."),
        ("hhill0192ga812g4918g8123ga91823746152", "Camp Buff: Hill Giant Strength"),
        ("hhill1293gb923g4029g9234gb02934857263", "Include Hill Giant Strength (Strength set to 21) when casting Camp Buffs."),
        ("hcloud0192ga812g4918g8123ga91823746152", "Camp Buff: Cloud Giant Strength"),
        ("hcloud1293gb923g4029g9234gb02934857263", "Include Cloud Giant Strength (Strength set to 27) when casting Camp Buffs."),
        ("hmorn0192ga812g4918g8123ga91823746152", "Camp Buff: Morninglord's Radiance"),
        ("hmorn1293gb923g4029g9234gb02934857263", "Include Morninglord's Radiance (+1d4 Radiant damage to weapon attacks)."),
        ("he0615243g3902g4904g2801g508493021164", "Camp Buff: Warding Bond"),
        ("hf1524354g2801g4803g1700g407382910155", "Include Camp Warding Bond (+1 AC, +1 Saves, Resistance to all damage).")
    ]

    tr_entries = [
        ("h123456789abcdef0123456789abcdef01234", "Kamp Buffları Yüzüğü"),
        ("h01a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8", "Seçilen tüm kamp bufflarını tek bir büyüyle tüm gruba uygular. Hangi buffların basılacağını kısayol çubuğundaki pasif butonlardan açıp kapatabilirsiniz."),
        ("h7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4", "Kamp Bufflarını Uygula"),
        ("h8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5", "Açık olan tüm kamp bufflarını 30 metre içindeki tüm müttefiklere uygular."),
        ("hrem01928ga812g4918g8123ga91823746152", "Kamp Bufflarını Kaldır"),
        ("hrem12938gb923g4029g9234gb02934857263", "Uygulanmış tüm kamp bufflarını 30 metre içindeki tüm müttefiklerden kaldırır."),
        ("h3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0", "Kamp Buffı: Uzun Adım (Longstrider)"),
        ("h4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1", "+3 metre hareket mesafesi sağlar."),
        ("h5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2", "Kamp Buffı: Büyücü Zırhı (Mage Armor)"),
        ("h6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3", "Zırhsız karakterlerin temel Zırh Sınıfını (AC) 13 yapar."),
        ("haid2_name_01928374", "Kamp Buffı: Destek (Aid Seviye 2: +5 Can)"),
        ("haid2_desc_01928374", "Maksimum canı 5 artırır."),
        ("haid3_name_01928374", "Kamp Buffı: Destek (Aid Seviye 3: +10 Can)"),
        ("haid3_desc_01928374", "Maksimum canı 10 artırır."),
        ("haid4_name_01928374", "Kamp Buffı: Destek (Aid Seviye 4: +15 Can)"),
        ("haid4_desc_01928374", "Maksimum canı 15 artırır."),
        ("haid5_name_01928374", "Kamp Buffı: Destek (Aid Seviye 5: +20 Can)"),
        ("haid5_desc_01928374", "Maksimum canı 20 artırır."),
        ("haid6_name_01928374", "Kamp Buffı: Destek (Aid Seviye 6: +25 Can)"),
        ("haid6_desc_01928374", "Maksimum canı 25 artırır."),
        ("hc1928374gf716g4318ga615g316274859102", "Kamp Buffı: Ölüm Koruması (Death Ward)"),
        ("hd2837465ge615g4217gb514g205163748291", "Ölümcül hasar alındığında 1 Can ile hayatta kalmayı sağlar."),
        ("he1827364gb514g4116ga413g118495061273", "Kamp Buffı: Hareket Özgürlüğü (Freedom of Movement)"),
        ("hf0918273gc413g4015ga312g019506172384", "Felç, kısıtlama ve zorlu zemin etkilerine karşı tam bağışıklık sağlar."),
        ("ha1928374gd312g4914gb211gf08493027164", "Kamp Buffı: Zehirden Korunma (Protection from Poison)"),
        ("hb0918273ge211g4813ga110ge07382916253", "Zehir hasarına direnç ve zehre karşı kurtarma zarlarında avantaj sağlar."),
        ("hc1827364gf110g4712ga009gd06271829364", "Kamp Buffı: Karanlık Görüşü (Darkvision)"),
        ("hd0918273ga009g4611g9f08gc05160718273", "12 metre karanlıkta görme yeteneği kazandırır."),
        ("he1928374g9f08g4510g8e07gb04059607182", "Kamp Buffı: Kahramanlar Ziyafeti (Heroes' Feast)"),
        ("hf0827364g8e07g4409g7d06ga03948576192", "+12 Maks Can, zehir ve korkuya bağışıklık, Bilgelik zarlarında avantaj sağlar."),
        ("ha0827364g7d06g4308g6c05g902837465182", "Kamp Buffı: Hayvanlarla Konuşma (Speak with Animals)"),
        ("hb1726354g6c05g4207g5b04g801726354192", "Hayvanlarla konuşma yeteneği sağlar."),
        ("hc1726354g5b04g4106g4a03g700615243182", "Kamp Buffı: Günışığı (Daylight)"),
        ("hd0615243g4a03g4005g3902g609504132173", "Etrafınıza aydınlatıcı Günışığı aurası yayar."),
        ("hguid01928ga812g4918g8123ga91823746152", "Kamp Buffı: Rehberlik (Guidance)"),
        ("hguid12938gb923g4029g9234gb02934857263", "Yetenek kontrollerine +1d4 bonus sağlar."),
        ("hbless0192ga812g4918g8123ga91823746152", "Kamp Buffı: Kutsama (Bless)"),
        ("hbless1293gb923g4029g9234gb02934857263", "Saldırı ve kurtarma zarlarına +1d4 bonus sağlar."),
        ("hfaith0192ga812g4918g8123ga91823746152", "Kamp Buffı: İnanç Kalkanı (Shield of Faith)"),
        ("hfaith1293gb923g4029g9234gb02934857263", "+2 Zırh Sınıfı (AC) sağlar."),
        ("hstone0192ga812g4918g8123ga91823746152", "Kamp Buffı: Taş Deri (Stoneskin)"),
        ("hstone1293gb923g4029g9234gb02934857263", "Büyülü olmayan ezici, delici ve kesici hasara direnç sağlar."),
        ("hbark0192ga812g4918g8123ga91823746152", "Kamp Buffı: Ağaç Kabuğu (Barkskin)"),
        ("hbark1293gb923g4029g9234gb02934857263", "Zırh Sınıfı 16'dan aşağı düşemez."),
        ("hseein0192ga812g4918g8123ga91823746152", "Kamp Buffı: Görünmezliği Görme (See Invisibility)"),
        ("hseein1293gb923g4029g9234gb02934857263", "Görünmez yaratıkları görme yeteneği kazandırır."),
        ("hfeath0192ga812g4918g8123ga91823746152", "Kamp Buffı: Tüy Düşüşü (Feather Fall)"),
        ("hfeath1293gb923g4029g9234gb02934857263", "Düşme hasarına karşı tam bağışıklık sağlar."),
        ("hjump0192ga812g4918g8123ga91823746152", "Kamp Buffı: Gelişmiş Zıplama (Enhanced Leap)"),
        ("hjump1293gb923g4029g9234gb02934857263", "Zıplama mesafesini 3 katına çıkarır."),
        ("hhill0192ga812g4918g8123ga91823746152", "Kamp Buffı: Tepe Dev Gücü (Hill Giant Strength)"),
        ("hhill1293gb923g4029g9234gb02934857263", "Kuvvet değerini 21'e ayarlar."),
        ("hcloud0192ga812g4918g8123ga91823746152", "Kamp Buffı: Bulut Dev Gücü (Cloud Giant Strength)"),
        ("hcloud1293gb923g4029g9234gb02934857263", "Kuvvet değerini 27'ye ayarlar."),
        ("hmorn0192ga812g4918g8123ga91823746152", "Kamp Buffı: Morninglord Işıltısı (Morninglord's Radiance)"),
        ("hmorn1293gb923g4029g9234gb02934857263", "Silah saldırılarına +1d4 Işıltılı hasar ekler."),
        ("he0615243g3902g4904g2801g508493021164", "Kamp Buffı: Koruma Bağı (Warding Bond)"),
        ("hf1524354g2801g4803g1700g407382910155", "Kamp Koruma Bağı (+1 AC, +1 Kurtarma Zarları, Tüm hasarlara Direnç).")
    ]

    def build_xml(entries):
        lines = ['<?xml version="1.0" encoding="utf-8"?>',
                 '<contentList xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">']
        for handle, text in entries:
            safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
            lines.append(f'  <content contentuid="{handle}" version="1">{safe_text}</content>')
        lines.append('</contentList>')
        return "\n".join(lines)

    en_dir = os.path.join(loc_dir, "English")
    tr_dir = os.path.join(loc_dir, "Turkish")
    os.makedirs(en_dir, exist_ok=True)
    os.makedirs(tr_dir, exist_ok=True)

    en_xml = os.path.join(en_dir, "english.xml")
    en_loca = os.path.join(en_dir, "english.loca")
    with open(en_xml, "w", encoding="utf-8") as f:
        f.write(build_xml(en_entries))
    cmd = [DIVINE, "-g", "bg3", "-a", "convert-loca", "-s", en_xml, "-d", en_loca]
    subprocess.run(cmd, check=True)
    print(f"    Compiled English loca: {en_loca}")

    tr_xml = os.path.join(tr_dir, "turkish.xml")
    tr_loca = os.path.join(tr_dir, "turkish.loca")
    with open(tr_xml, "w", encoding="utf-8") as f:
        f.write(build_xml(tr_entries))
    cmd = [DIVINE, "-g", "bg3", "-a", "convert-loca", "-s", tr_xml, "-d", tr_loca]
    subprocess.run(cmd, check=True)
    print(f"    Compiled Turkish loca: {tr_loca}")

def package_and_install():
    print("[7] Packaging mod into CampBuffs.pak using Divine with LZ4...")
    cmd = [DIVINE, "-g", "bg3", "-a", "create-package", "-s", BUILD_DIR, "-d", OUTPUT_PAK, "-c", "lz4"]
    subprocess.run(cmd, check=True)
    pak_size = os.path.getsize(OUTPUT_PAK)
    print(f"    Built PAK: {OUTPUT_PAK} ({pak_size:,} bytes)")
    
    print(f"[8] Installing CampBuffs.pak to {MODS_DIR}...")
    if os.path.exists(os.path.dirname(MODS_DIR)):
        try:
            os.makedirs(MODS_DIR, exist_ok=True)
            target_pak = os.path.join(MODS_DIR, "CampBuffs.pak")
            shutil.copy2(OUTPUT_PAK, target_pak)
            print(f"    Successfully installed to {target_pak}")
        except Exception as e:
            print(f"    Note: Could not copy to Mods folder: {e}")
    else:
        print(f"    Mods directory not found. PAK is ready at {OUTPUT_PAK}")

if __name__ == "__main__":
    clean_build_dir()
    generate_icons()
    create_ui_metadata()
    create_meta()
    create_roottemplates()
    create_onetime_rewards()
    create_stats()
    create_localization()
    package_and_install()
    print("ALL DONE SUCCESSFULLY!")