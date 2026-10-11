"""
CampBuffsModBuffs Mod Build Script
Addon for CampBuffs requiring CampBuffs.
Adds DnD 5.5e Artificer Infusions (Enhanced Defense, Enhanced Weapon, Returning Weapon,
Repeating Shot, Enhanced Arcane Focus, Bag of Holding, Armor of Magical Strength,
Boots of the Winding Path, Repulsion Shield) and Mystra's Spells (Coming of Age,
Water Walk, Gift of Alacrity).
100% Native BG3 Patch 7 compatible.
"""
import os
import shutil
import subprocess
from PIL import Image

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(WORKSPACE_DIR, "build_campbuffs_modbuffs")
MODS_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Larian Studios\Baldur's Gate 3\Mods")
DIVINE = os.path.join(WORKSPACE_DIR, r"tools\lslib\Packed\Tools\Divine.exe")

MOD_NAME = "CampBuffsModBuffs"
MOD_UUID = "e4a7d182-59f3-4bc8-8c10-3d71e892c431"
BASE_MOD_UUID = "7cf9c6d5-936e-4f8d-8052-d71f42920844"
RING_ROOT_UUID = "c9b0a1d2-e3f4-5a6b-7c8d-9e0f1a2b3c4e"
OUTPUT_PAK = os.path.join(WORKSPACE_DIR, "Releases", "CampBuffsModBuffs.pak")

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
    img_144.save(os.path.join(controller_dir, "CampBuffsModBuffs_CastAll.png"), format="PNG")
    img_144.save(os.path.join(controller_dir, "CampBuffsModBuffs_Icon.png"), format="PNG")
    
    # 2. 380x380 for Tooltips
    tooltips_dir = os.path.join(BUILD_DIR, "Public", "Game", "Assets", "Tooltips", "Icons")
    os.makedirs(tooltips_dir, exist_ok=True)
    img_380 = img.resize((380, 380), Image.Resampling.LANCZOS)
    img_380.save(os.path.join(tooltips_dir, "CampBuffsModBuffs_CastAll.png"), format="PNG")
    img_380.save(os.path.join(tooltips_dir, "CampBuffsModBuffs_Icon.png"), format="PNG")
    
    # 3. 64x64 DXT5 DDS atlas
    atlas_dir = os.path.join(BUILD_DIR, "Public", MOD_NAME, "Assets", "Textures", "Icons")
    os.makedirs(atlas_dir, exist_ok=True)
    img_64 = img.resize((64, 64), Image.Resampling.LANCZOS)
    dds_path = os.path.join(atlas_dir, "CampBuffsModBuffs_Icons.dds")
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
                    <attribute id="ID" type="FixedString" value="c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f"/>
                    <attribute id="Localized" type="bool" value="False"/>
                    <attribute id="Name" type="LSString" value="CampBuffsModBuffs_Icons"/>
                    <attribute id="SRGB" type="bool" value="True"/>
                    <attribute id="SourceFile" type="LSString" value="Public/{MOD_NAME}/Assets/Textures/Icons/CampBuffsModBuffs_Icons.dds"/>
                    <attribute id="Streaming" type="bool" value="True"/>
                    <attribute id="Template" type="FixedString" value="CampBuffsModBuffs_Icons"/>
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
                    <attribute id="MapKey" type="FixedString" value="CampBuffsModBuffs_CastAll"/>
                    <attribute id="U1" type="float" value="0.0"/>
                    <attribute id="U2" type="float" value="1.0"/>
                    <attribute id="V1" type="float" value="0.0"/>
                    <attribute id="V2" type="float" value="1.0"/>
                </node>
                <node id="IconUV">
                    <attribute id="MapKey" type="FixedString" value="CampBuffsModBuffs_Icon"/>
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
                    <attribute id="Path" type="LSString" value="Assets/Textures/Icons/CampBuffsModBuffs_Icons.dds"/>
                    <attribute id="UUID" type="FixedString" value="c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f"/>
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
    with open(os.path.join(gui_dir, "Icons_CampBuffsModBuffs.lsx"), "w", encoding="utf-8") as f:
        f.write(icons_lsx)

def create_meta():
    print("[3] Creating meta.lsx with CampBuffs dependency...")
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
                        <node id="ModuleShortDesc">
                            <attribute id="Folder" type="LSString" value="CampBuffs"/>
                            <attribute id="MD5" type="LSString" value=""/>
                            <attribute id="Name" type="LSString" value="CampBuffs"/>
                            <attribute id="PublishHandle" type="uint64" value="0"/>
                            <attribute id="UUID" type="guid" value="{BASE_MOD_UUID}"/>
                            <attribute id="Version64" type="int64" value="36028797018963968"/>
                        </node>
                    </children>
                </node>
                <node id="ModuleInfo">
                    <attribute id="Author" type="LSString" value="UniversalModder"/>
                    <attribute id="CharacterCreationLevelName" type="FixedString" value=""/>
                    <attribute id="Description" type="LSString" value="Addon for CampBuffs requiring CampBuffs. Adds DnD 5.5e Artificer Infusions and Mystra's Spells camp buffs."/>
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
    print("[4] Creating RootTemplates for CampBuffs_ModBuffs_Ring...")
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
                    <attribute id="Name" type="LSString" value="CampBuffs_ModBuffs_Ring" />
                    <attribute id="LevelName" type="FixedString" value="" />
                    <attribute id="Type" type="FixedString" value="item" />
                    <attribute id="ParentTemplateId" type="FixedString" value="a631b70a-22e9-4e2c-bb07-2164c2beb5d0" />
                    <attribute id="DisplayName" type="TranslatedString" handle="hmod_ring_name" version="1" />
                    <attribute id="Description" type="TranslatedString" handle="hmod_ring_desc" version="1" />
                    <attribute id="Icon" type="FixedString" value="Item_LOOT_GEN_Ring_E_Gem_A_Gold" />
                    <attribute id="Stats" type="FixedString" value="CampBuffs_ModBuffs_Ring" />
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
    lsx_path = os.path.join(rt_dir, "CampBuffs_ModBuffs_Ring.lsx")
    lsf_path = os.path.join(rt_dir, "CampBuffs_ModBuffs_Ring.lsf")
    with open(lsx_path, "w", encoding="utf-8") as f:
        f.write(rt_content)
    cmd = [DIVINE, "-g", "bg3", "-a", "convert-resource", "-s", lsx_path, "-d", lsf_path]
    subprocess.run(cmd, check=True)
    os.remove(lsx_path)
    print(f"    Compiled RootTemplates to {lsf_path} (removed .lsx)")

def create_onetime_rewards():
    print("[4.5] Creating OneTimeRewards for CampBuffsModBuffs (Camp Chest / Traveller's Chest delivery)...")
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
                    <attribute id="UUID" type="guid" value="f2938475-b1c2-4d3e-9f4a-6b7c8d9e0f12"/>
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

    # Modded passives for DnD 5.5 + Mystra (only mod-specific entries)
    mod_passives = [
        # DnD 5.5e Artificer Infusions
        "CB_Toggle_Mod_EnhancedDefense_1", "CB_Toggle_Mod_EnhancedDefense_2",
        "CB_Toggle_Mod_EnhancedWeapon_1", "CB_Toggle_Mod_EnhancedWeapon_2",
        "CB_Toggle_Mod_ReturningWeapon",
        "CB_Toggle_Mod_RepeatingShot",
        "CB_Toggle_Mod_ArcaneFocus_1", "CB_Toggle_Mod_ArcaneFocus_2",
        "CB_Toggle_Mod_BagOfHolding",
        "CB_Toggle_Mod_ArmorOfMagicalStrength",
        "CB_Toggle_Mod_BootsOfWindingPath",
        "CB_Toggle_Mod_RepulsionShield",
        # Mystra's Spells
        "CB_Toggle_Mod_ComingOfAge",
        "CB_Toggle_Mod_WaterWalk",
        "CB_Toggle_Mod_GiftOfAlacrity"
    ]

    mod_ring_passives_str = ";".join(["CampBuffs_ModBuffs_Passive"] + mod_passives)

    # 1. Object.txt and Armor.txt
    object_content = f"""new entry "CampBuffs_ModBuffs_Ring"
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
data "PassivesOnEquip" "{mod_ring_passives_str}"
"""
    with open(os.path.join(data_dir, "Object.txt"), "w", encoding="utf-8") as f:
        f.write(object_content)
    with open(os.path.join(data_dir, "Armor.txt"), "w", encoding="utf-8") as f:
        f.write(object_content)

    # 2. Passive.txt
    passive_content = """new entry "CampBuffs_ModBuffs_Passive"
type "PassiveData"
data "Properties" "Highlighted"
data "Icon" "CampBuffsModBuffs_Icon"
data "DisplayName" "hmod_ring_name;1"
data "Description" "hmod_ring_desc;1"
data "Boosts" "UnlockSpell(Shout_CampBuffs_ModBuffs_CastAll);UnlockSpell(Zone_CB_ModBuffs);UnlockSpell(Shout_CampBuffs_ModBuffs_RemoveBuffs);UnlockSpell(Zone_CB_RemoveModBuffs)"

new entry "CB_Toggle_Mod_EnhancedDefense_1"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_ShieldOfFaith"
data "DisplayName" "hmod_edef1_name;1"
data "Description" "hmod_edef1_desc;1"

new entry "CB_Toggle_Mod_EnhancedDefense_2"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_ShieldOfFaith"
data "DisplayName" "hmod_edef2_name;1"
data "Description" "hmod_edef2_desc;1"

new entry "CB_Toggle_Mod_EnhancedWeapon_1"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Transmutation_MagicWeapon"
data "DisplayName" "hmod_eweap1_name;1"
data "Description" "hmod_eweap1_desc;1"

new entry "CB_Toggle_Mod_EnhancedWeapon_2"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Transmutation_MagicWeapon"
data "DisplayName" "hmod_eweap2_name;1"
data "Description" "hmod_eweap2_desc;1"

new entry "CB_Toggle_Mod_ReturningWeapon"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Transmutation_MagicWeapon"
data "DisplayName" "hmod_retweap_name;1"
data "Description" "hmod_retweap_desc;1"

new entry "CB_Toggle_Mod_RepeatingShot"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Transmutation_MagicWeapon"
data "DisplayName" "hmod_repshot_name;1"
data "Description" "hmod_repshot_desc;1"

new entry "CB_Toggle_Mod_ArcaneFocus_1"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "PassiveFeature_MagicInitiateCleric"
data "DisplayName" "hmod_focus1_name;1"
data "Description" "hmod_focus1_desc;1"

new entry "CB_Toggle_Mod_ArcaneFocus_2"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "PassiveFeature_MagicInitiateCleric"
data "DisplayName" "hmod_focus2_name;1"
data "Description" "hmod_focus2_desc;1"

new entry "CB_Toggle_Mod_BagOfHolding"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "GenericIcon_Intent_Utility"
data "DisplayName" "hmod_bag_name;1"
data "Description" "hmod_bag_desc;1"

new entry "CB_Toggle_Mod_ArmorOfMagicalStrength"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Evocation_DivineSmite"
data "DisplayName" "hmod_armstr_name;1"
data "Description" "hmod_armstr_desc;1"

new entry "CB_Toggle_Mod_BootsOfWindingPath"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Conjuration_MistyStep"
data "DisplayName" "hmod_boots_name;1"
data "Description" "hmod_boots_desc;1"

new entry "CB_Toggle_Mod_RepulsionShield"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Abjuration_ShieldOfFaith"
data "DisplayName" "hmod_repshld_name;1"
data "Description" "hmod_repshld_desc;1"

new entry "CB_Toggle_Mod_ComingOfAge"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Divination_Guidance"
data "DisplayName" "hmod_age_name;1"
data "Description" "hmod_age_desc;1"

new entry "CB_Toggle_Mod_WaterWalk"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Transmutation_Longstrider"
data "DisplayName" "hmod_ww_name;1"
data "Description" "hmod_ww_desc;1"

new entry "CB_Toggle_Mod_GiftOfAlacrity"
type "PassiveData"
data "Properties" "IsToggled;ToggledDefaultAddToHotbar"
data "Icon" "Spell_Divination_Guidance"
data "DisplayName" "hmod_alac_name;1"
data "Description" "hmod_alac_desc;1"
"""
    with open(os.path.join(data_dir, "Passive.txt"), "w", encoding="utf-8") as f:
        f.write(passive_content)

    # 3. Spell properties (ONLY mod-specific, does NOT redefine base mod spells)
    mod_props = [
        # DnD 5.5e Enhanced Defense (+1 or +2)
        "IF(HasPassive('CB_Toggle_Mod_EnhancedDefense_2', context.Source)):ApplyStatus(CB_MOD_ENHANCED_DEFENSE_2, 100, -1)",
        "IF(HasPassive('CB_Toggle_Mod_EnhancedDefense_1', context.Source) and not HasPassive('CB_Toggle_Mod_EnhancedDefense_2', context.Source)):ApplyStatus(CB_MOD_ENHANCED_DEFENSE_1, 100, -1)",
        # DnD 5.5e Enhanced Weapon (+1 or +2)
        "IF(HasPassive('CB_Toggle_Mod_EnhancedWeapon_2', context.Source)):ApplyStatus(CB_MOD_ENHANCED_WEAPON_2, 100, -1)",
        "IF(HasPassive('CB_Toggle_Mod_EnhancedWeapon_1', context.Source) and not HasPassive('CB_Toggle_Mod_EnhancedWeapon_2', context.Source)):ApplyStatus(CB_MOD_ENHANCED_WEAPON_1, 100, -1)",
        # DnD 5.5e Returning Weapon
        "IF(HasPassive('CB_Toggle_Mod_ReturningWeapon', context.Source)):ApplyStatus(CB_MOD_RETURNING_WEAPON, 100, -1)",
        # DnD 5.5e Repeating Shot
        "IF(HasPassive('CB_Toggle_Mod_RepeatingShot', context.Source)):ApplyStatus(CB_MOD_REPEATING_SHOT, 100, -1)",
        # DnD 5.5e Enhanced Arcane Focus (+1 or +2)
        "IF(HasPassive('CB_Toggle_Mod_ArcaneFocus_2', context.Source)):ApplyStatus(CB_MOD_ARCANE_FOCUS_2, 100, -1)",
        "IF(HasPassive('CB_Toggle_Mod_ArcaneFocus_1', context.Source) and not HasPassive('CB_Toggle_Mod_ArcaneFocus_2', context.Source)):ApplyStatus(CB_MOD_ARCANE_FOCUS_1, 100, -1)",
        # DnD 5.5e Bag of Holding
        "IF(HasPassive('CB_Toggle_Mod_BagOfHolding', context.Source)):ApplyStatus(CB_MOD_BAG_OF_HOLDING, 100, -1)",
        # DnD 5.5e Armor of Magical Strength
        "IF(HasPassive('CB_Toggle_Mod_ArmorOfMagicalStrength', context.Source)):ApplyStatus(CB_MOD_ARMOR_OF_MAGICAL_STRENGTH, 100, -1)",
        # DnD 5.5e Boots of the Winding Path
        "IF(HasPassive('CB_Toggle_Mod_BootsOfWindingPath', context.Source)):ApplyStatus(CB_MOD_BOOTS_OF_WINDING_PATH, 100, -1)",
        # DnD 5.5e Repulsion Shield
        "IF(HasPassive('CB_Toggle_Mod_RepulsionShield', context.Source)):ApplyStatus(CB_MOD_REPULSION_SHIELD, 100, -1)",
        # Mystra's Spells Coming of Age
        "IF(HasPassive('CB_Toggle_Mod_ComingOfAge', context.Source)):ApplyStatus(CB_MOD_COMING_OF_AGE, 100, -1)",
        # Mystra's Spells Water Walk
        "IF(HasPassive('CB_Toggle_Mod_WaterWalk', context.Source)):ApplyStatus(CB_MOD_WATER_WALK, 100, -1)",
        # Mystra's Spells Gift of Alacrity
        "IF(HasPassive('CB_Toggle_Mod_GiftOfAlacrity', context.Source)):ApplyStatus(CB_MOD_GIFT_OF_ALACRITY, 100, -1)"
    ]

    mod_only_props_str = ";".join(mod_props)

    # Only remove CB_MOD_* statuses defined by this mod (no external mod status refs)
    mod_remove_statuses = [
        "CB_MOD_ENHANCED_DEFENSE_1", "CB_MOD_ENHANCED_DEFENSE_2",
        "CB_MOD_ENHANCED_WEAPON_1", "CB_MOD_ENHANCED_WEAPON_2",
        "CB_MOD_RETURNING_WEAPON", "CB_MOD_REPEATING_SHOT",
        "CB_MOD_ARCANE_FOCUS_1", "CB_MOD_ARCANE_FOCUS_2",
        "CB_MOD_BAG_OF_HOLDING", "CB_MOD_ARMOR_OF_MAGICAL_STRENGTH",
        "CB_MOD_BOOTS_OF_WINDING_PATH", "CB_MOD_REPULSION_SHIELD",
        "CB_MOD_COMING_OF_AGE", "CB_MOD_WATER_WALK", "CB_MOD_GIFT_OF_ALACRITY"
    ]

    mod_remove_str = ";".join([f"RemoveStatus({s})" for s in mod_remove_statuses])

    # 4. Spell_Shout.txt: ONLY mod-specific spells (does NOT redefine Shout_CampBuffs_CastAll or Shout_CampBuffs_RemoveBuffs)
    spell_shout_content = f"""new entry "Shout_CampBuffs_ModBuffs_CastAll"
type "SpellData"
data "SpellType" "Shout"
data "Level" "0"
data "SpellProperties" "{mod_only_props_str}"
data "AreaRadius" "35"
data "TargetConditions" "(Ally() or Self()) and Character()"
data "Icon" "CampBuffsModBuffs_CastAll"
data "DisplayName" "hmod_cast_name;1"
data "Description" "hmod_cast_desc;1"
data "CastSound" "Spell_Cast_Healing_Aid_L1to3"
data "TargetSound" "Spell_Impact_Healing_Aid_L1to3"
data "CastEffectTextEvent" "Cast"
data "SpellAnimation" "414bbf02-2918-4f01-83fb-1ddc7a588d88,,;,,;7abe77ed-9c77-4eac-872c-5b8caed070b6,,;cb171bda-f065-4520-b470-e447f678ba1f,,;0c5dcc83-fa78-41da-b6a5-440b5ea30936,,;,,;bea988a0-2ec5-40d8-a67e-ffbd7454bc53,,;,,;,,"
data "PrepareEffect" "96a51ac8-2e7e-4718-bb62-dcfd18964a02"
data "CastEffect" "b50decc3-5f93-4467-8d3a-aa8b01fc915e"
data "TargetEffect" "a908e49b-b59f-4a20-b487-e25ae198d926"
data "Requirements" "!Combat"
data "MemoryCost" "0"

new entry "Zone_CB_ModBuffs"
type "SpellData"
using "Shout_CampBuffs_ModBuffs_CastAll"

new entry "Shout_CampBuffs_ModBuffs_RemoveBuffs"
type "SpellData"
data "SpellType" "Shout"
data "Level" "0"
data "SpellProperties" "{mod_remove_str}"
data "AreaRadius" "35"
data "TargetConditions" "(Ally() or Self()) and Character()"
data "Icon" "Spell_Abjuration_RemoveCurse"
data "DisplayName" "hmod_rem_name;1"
data "Description" "hmod_rem_desc;1"
data "CastSound" "Spell_Cast_Utility_Dispel"
data "TargetSound" "Spell_Impact_Utility_Dispel"
data "CastEffectTextEvent" "Cast"
data "SpellAnimation" "414bbf02-2918-4f01-83fb-1ddc7a588d88,,;,,;7abe77ed-9c77-4eac-872c-5b8caed070b6,,;cb171bda-f065-4520-b470-e447f678ba1f,,;0c5dcc83-fa78-41da-b6a5-440b5ea30936,,;,,;bea988a0-2ec5-40d8-a67e-ffbd7454bc53,,;,,;,,"
data "PrepareEffect" "96a51ac8-2e7e-4718-bb62-dcfd18964a02"
data "CastEffect" "b50decc3-5f93-4467-8d3a-aa8b01fc915e"
data "TargetEffect" "a908e49b-b59f-4a20-b487-e25ae198d926"
data "Requirements" "!Combat"
data "MemoryCost" "0"

new entry "Zone_CB_RemoveModBuffs"
type "SpellData"
using "Shout_CampBuffs_ModBuffs_RemoveBuffs"
"""
    with open(os.path.join(data_dir, "Spell_Shout.txt"), "w", encoding="utf-8") as f:
        f.write(spell_shout_content)
    with open(os.path.join(stats_dir, "Spell_Shout.txt"), "w", encoding="utf-8") as f:
        f.write(spell_shout_content)

    # 5. Status_BOOST.txt
    status_content = """new entry "CB_MOD_ENHANCED_DEFENSE_1"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_ShieldOfFaith"
data "DisplayName" "hmod_edef1_name;1"
data "Description" "hmod_edef1_desc;1"
data "Boosts" "AC(1)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_ENHANCED_DEFENSE_2"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_ShieldOfFaith"
data "DisplayName" "hmod_edef2_name;1"
data "Description" "hmod_edef2_desc;1"
data "Boosts" "AC(2)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_ENHANCED_WEAPON_1"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Transmutation_MagicWeapon"
data "DisplayName" "hmod_eweap1_name;1"
data "Description" "hmod_eweap1_desc;1"
data "Boosts" "RollBonus(MeleeWeaponAttack, 1);RollBonus(RangedWeaponAttack, 1);RollBonus(MeleeOffHandWeaponAttack, 1);RollBonus(RangedOffHandWeaponAttack, 1);CharacterWeaponDamage(1)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_ENHANCED_WEAPON_2"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Transmutation_MagicWeapon"
data "DisplayName" "hmod_eweap2_name;1"
data "Description" "hmod_eweap2_desc;1"
data "Boosts" "RollBonus(MeleeWeaponAttack, 2);RollBonus(RangedWeaponAttack, 2);RollBonus(MeleeOffHandWeaponAttack, 2);RollBonus(RangedOffHandWeaponAttack, 2);CharacterWeaponDamage(2)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_RETURNING_WEAPON"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Transmutation_MagicWeapon"
data "DisplayName" "hmod_retweap_name;1"
data "Description" "hmod_retweap_desc;1"
data "Boosts" "RollBonus(ThrownWeaponAttack, 1);RollBonus(MeleeWeaponAttack, 1);RollBonus(RangedWeaponAttack, 1);CharacterWeaponDamage(1)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_REPEATING_SHOT"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Transmutation_MagicWeapon"
data "DisplayName" "hmod_repshot_name;1"
data "Description" "hmod_repshot_desc;1"
data "Boosts" "RollBonus(RangedWeaponAttack, 1);RollBonus(RangedOffHandWeaponAttack, 1);CharacterWeaponDamage(1)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_ARCANE_FOCUS_1"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "PassiveFeature_MagicInitiateCleric"
data "DisplayName" "hmod_focus1_name;1"
data "Description" "hmod_focus1_desc;1"
data "Boosts" "SpellSaveDC(1);RollBonus(MeleeSpellAttack, 1);RollBonus(RangedSpellAttack, 1)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_ARCANE_FOCUS_2"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "PassiveFeature_MagicInitiateCleric"
data "DisplayName" "hmod_focus2_name;1"
data "Description" "hmod_focus2_desc;1"
data "Boosts" "SpellSaveDC(2);RollBonus(MeleeSpellAttack, 2);RollBonus(RangedSpellAttack, 2)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_BAG_OF_HOLDING"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "GenericIcon_Intent_Utility"
data "DisplayName" "hmod_bag_name;1"
data "Description" "hmod_bag_desc;1"
data "Boosts" "CarryCapacityMultiplier(12.5)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_ARMOR_OF_MAGICAL_STRENGTH"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Evocation_DivineSmite"
data "DisplayName" "hmod_armstr_name;1"
data "Description" "hmod_armstr_desc;1"
data "Boosts" "RollBonus(RawAbility, 2, Strength);RollBonus(SkillCheck, 2, Athletics);RollBonus(SavingThrow, 2, Strength);StatusImmunity(PRONE);StatusImmunity(KNOCKED_DOWN)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_BOOTS_OF_WINDING_PATH"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Conjuration_MistyStep"
data "DisplayName" "hmod_boots_name;1"
data "Description" "hmod_boots_desc;1"
data "Boosts" "ActionResource(Movement, 3, 0);UnlockSpell(Target_MistyStep)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_REPULSION_SHIELD"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Abjuration_ShieldOfFaith"
data "DisplayName" "hmod_repshld_name;1"
data "Description" "hmod_repshld_desc;1"
data "Boosts" "AC(1);RollBonus(SavingThrow, 1)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_COMING_OF_AGE"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Divination_Guidance"
data "DisplayName" "hmod_age_name;1"
data "Description" "hmod_age_desc;1"
data "Boosts" "RollBonus(SkillCheck, 1d4);RollBonus(RawAbility, 1d4)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_WATER_WALK"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Transmutation_Longstrider"
data "DisplayName" "hmod_ww_name;1"
data "Description" "hmod_ww_desc;1"
data "Boosts" "IgnoreDifficultTerrain();StatusImmunity(ACID);StatusImmunity(BURNING_LAVA);StatusImmunity(CAUSTIC_BRINE);StatusImmunity(DIFFICULT_TERRAIN_MUD);StatusImmunity(DIFFICULT_TERRAIN_LAVA);StatusImmunity(DIFFICULT_TERRAIN_DEEPWATER);StatusImmunity(PRONE_GREASE);StatusImmunity(PRONE_SEWER)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"

new entry "CB_MOD_GIFT_OF_ALACRITY"
type "StatusData"
data "StatusType" "BOOST"
data "Icon" "Spell_Divination_Guidance"
data "DisplayName" "hmod_alac_name;1"
data "Description" "hmod_alac_desc;1"
data "Boosts" "Initiative(2);RollBonus(Initiative, 1d8)"
data "StatusGroups" "SG_RemoveOnRespec"
data "RemoveEvents" "OnRest"
"""
    with open(os.path.join(data_dir, "Status_BOOST.txt"), "w", encoding="utf-8") as f:
        f.write(status_content)

    # 6. TreasureTable.txt (All Major Vendors Act 1-3 + Tutorial Chest + AMP Variants)
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
        treasure_blocks.append(f'new treasuretable "{t_name}"\nCanMerge 1\nnew subtable "1,1"\nobject category "I_CampBuffs_ModBuffs_Ring",1,0,0,0,0,0,0,0\n')

    treasure_content = "\n".join(treasure_blocks)
    with open(os.path.join(stats_dir, "TreasureTable.txt"), "w", encoding="utf-8") as f:
        f.write(treasure_content)
    with open(os.path.join(data_dir, "TreasureTable.txt"), "w", encoding="utf-8") as f:
        f.write(treasure_content)

def create_localization():
    print("[6] Creating English and Turkish Localization for CampBuffsModBuffs...")
    loc_dir = os.path.join(BUILD_DIR, "Mods", MOD_NAME, "Localization")
    
    en_entries = [
        ("hmod_ring_name", "Camp Buffs: Mod Buffs Ring"),
        ("hmod_ring_desc", "Addon ring for CampBuffs. Grants DnD 5.5e Artificer Infusions and Mystra's Spells buffs with hotbar toggles."),
        ("hmod_cast_name", "Cast Modded Camp Buffs"),
        ("hmod_cast_desc", "Apply all enabled DnD 5.5e and Mystra camp buffs to all party members in a 30m radius."),
        ("hmod_rem_name", "Remove Modded Camp Buffs"),
        ("hmod_rem_desc", "Remove all applied DnD 5.5e and Mystra camp buffs from party members in a 30m radius."),
        # DnD 5.5e
        ("hmod_edef1_name", "Mod Buff: Enhanced Defense (+1 AC)"),
        ("hmod_edef1_desc", "Include Artificer Enhanced Defense (+1 AC) when casting Camp Buffs."),
        ("hmod_edef2_name", "Mod Buff: Enhanced Defense (+2 AC)"),
        ("hmod_edef2_desc", "Include Artificer Enhanced Defense (+2 AC) when casting Camp Buffs."),
        ("hmod_eweap1_name", "Mod Buff: Enhanced Weapon (+1)"),
        ("hmod_eweap1_desc", "Include Artificer Enhanced Weapon (+1 Attack and Damage) when casting Camp Buffs."),
        ("hmod_eweap2_name", "Mod Buff: Enhanced Weapon (+2)"),
        ("hmod_eweap2_desc", "Include Artificer Enhanced Weapon (+2 Attack and Damage) when casting Camp Buffs."),
        ("hmod_retweap_name", "Mod Buff: Returning Weapon"),
        ("hmod_retweap_desc", "Include Artificer Returning Weapon (+1 attack/damage, thrown weapons return to hand) when casting Camp Buffs."),
        ("hmod_repshot_name", "Mod Buff: Repeating Shot"),
        ("hmod_repshot_desc", "Include Artificer Repeating Shot (+1 ranged attack/damage, magical repeating ammo) when casting Camp Buffs."),
        ("hmod_focus1_name", "Mod Buff: Enhanced Arcane Focus (+1)"),
        ("hmod_focus1_desc", "Include Artificer Enhanced Arcane Focus (+1 Spell Attack & Spell Save DC) when casting Camp Buffs."),
        ("hmod_focus2_name", "Mod Buff: Enhanced Arcane Focus (+2)"),
        ("hmod_focus2_desc", "Include Artificer Enhanced Arcane Focus (+2 Spell Attack & Spell Save DC) when casting Camp Buffs."),
        ("hmod_bag_name", "Mod Buff: Bag of Holding"),
        ("hmod_bag_desc", "Include Artificer Bag of Holding (12.5x carrying capacity multiplier) when casting Camp Buffs."),
        ("hmod_armstr_name", "Mod Buff: Armor of Magical Strength"),
        ("hmod_armstr_desc", "Include Artificer Armor of Magical Strength (+2 Strength checks/saves, immunity to prone/knockdown) when casting Camp Buffs."),
        ("hmod_boots_name", "Mod Buff: Boots of the Winding Path"),
        ("hmod_boots_desc", "Include Artificer Boots of the Winding Path (+3m movement speed, Misty Step teleport) when casting Camp Buffs."),
        ("hmod_repshld_name", "Mod Buff: Repulsion Shield"),
        ("hmod_repshld_desc", "Include Artificer Repulsion Shield (+1 AC, +1 Saves) when casting Camp Buffs."),
        # Mystra's Spells
        ("hmod_age_name", "Mod Buff: Ceremony - Coming of Age"),
        ("hmod_age_desc", "Include Mystra's Ceremony: Coming of Age (+1d4 to ability & skill checks) when casting Camp Buffs."),
        ("hmod_ww_name", "Mod Buff: Water Walk"),
        ("hmod_ww_desc", "Include Mystra's Water Walk (immunity to difficult terrain, grease, acid, lava) when casting Camp Buffs."),
        ("hmod_alac_name", "Mod Buff: Gift of Alacrity"),
        ("hmod_alac_desc", "Include Mystra's Gift of Alacrity (+2 and +1d8 Initiative bonus) when casting Camp Buffs.")
    ]

    tr_entries = [
        ("hmod_ring_name", "Kamp Buffları: Mod Buffları Yüzüğü"),
        ("hmod_ring_desc", "CampBuffs için ek eklenti yüzüğü. DnD 5.5e Artificer ve Mystra büyüleri bufflarını kısayol çubuğundaki pasif butonlarla sunar."),
        ("hmod_cast_name", "Mod Kamp Bufflarını Uygula"),
        ("hmod_cast_desc", "Açık olan tüm DnD 5.5e ve Mystra kamp bufflarını 30 metre içindeki tüm müttefiklere uygular."),
        ("hmod_rem_name", "Mod Kamp Bufflarını Kaldır"),
        ("hmod_rem_desc", "Uygulanmış tüm DnD 5.5e ve Mystra kamp bufflarını 30 metre içindeki tüm müttefiklerden kaldırır."),
        # DnD 5.5e
        ("hmod_edef1_name", "Mod Buffı: Gelişmiş Savunma (Enhanced Defense +1 AC)"),
        ("hmod_edef1_desc", "+1 Zırh Sınıfı (AC) sağlar."),
        ("hmod_edef2_name", "Mod Buffı: Gelişmiş Savunma (Enhanced Defense +2 AC)"),
        ("hmod_edef2_desc", "+2 Zırh Sınıfı (AC) sağlar."),
        ("hmod_eweap1_name", "Mod Buffı: Gelişmiş Silah (Enhanced Weapon +1)"),
        ("hmod_eweap1_desc", "Silah saldırı ve hasar zarlarına +1 bonus ekler."),
        ("hmod_eweap2_name", "Mod Buffı: Gelişmiş Silah (Enhanced Weapon +2)"),
        ("hmod_eweap2_desc", "Silah saldırı ve hasar zarlarına +2 bonus ekler."),
        ("hmod_retweap_name", "Mod Buffı: Geri Dönen Silah (Returning Weapon)"),
        ("hmod_retweap_desc", "Fırlatma ve silah saldırılarına +1 bonus verir; fırlatılan silahlar anında ele geri döner."),
        ("hmod_repshot_name", "Mod Buffı: Seri Atış (Repeating Shot)"),
        ("hmod_repshot_desc", "Menzilli silahlara +1 saldırı/hasar bonusu ve kesintisiz büyülü mühimmat sağlar."),
        ("hmod_focus1_name", "Mod Buffı: Gelişmiş Büyü Odağı (Enhanced Arcane Focus +1)"),
        ("hmod_focus1_desc", "Büyü Kurtulma Zorluğu (DC) ve Büyü Saldırı zarlarına +1 ekler."),
        ("hmod_focus2_name", "Mod Buffı: Gelişmiş Büyü Odağı (Enhanced Arcane Focus +2)"),
        ("hmod_focus2_desc", "Büyü Kurtulma Zorluğu (DC) ve Büyü Saldırı zarlarına +2 ekler."),
        ("hmod_bag_name", "Mod Buffı: Dipsiz Çanta (Bag of Holding)"),
        ("hmod_bag_desc", "Envanter taşıma kapasitesini 12.5 katına çıkarır."),
        ("hmod_armstr_name", "Mod Buffı: Büyülü Güç Zırhı (Armor of Magical Strength)"),
        ("hmod_armstr_desc", "Kuvvet kontrollerine ve kurtarma zarlarına +2 ekler; yere düşmeye (Prone) karşı tam bağışıklık sağlar."),
        ("hmod_boots_name", "Mod Buffı: Kıvrımlı Yol Çizmeleri (Boots of the Winding Path)"),
        ("hmod_boots_desc", "+3 metre hareket mesafesi kazandırır ve Puslu Adım (Misty Step) ışınlanmasını açar."),
        ("hmod_repshld_name", "Mod Buffı: İtici Kalkan (Repulsion Shield)"),
        ("hmod_repshld_desc", "+1 Zırh Sınıfı (AC) ve +1 Kurtarma Zarları bonusu sağlar."),
        # Mystra's Spells
        ("hmod_age_name", "Mod Buffı: Seremoni - Reşit Olma (Coming of Age)"),
        ("hmod_age_desc", "Yetenek ve beceri kontrollerine +1d4 bonus sağlar."),
        ("hmod_ww_name", "Mod Buffı: Suda Yürüme (Water Walk)"),
        ("hmod_ww_desc", "Zorlu zemin, kaygan yağ, lav, asit ve derin suya karşı tam bağışıklık sağlar."),
        ("hmod_alac_name", "Mod Buffı: Çeviklik Hediyesi (Gift of Alacrity)"),
        ("hmod_alac_desc", "Savaş başlangıcında inisiyatif zarlarına +2 ve +1d8 devasa inisiyatif bonusu sağlar.")
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
    print(f"[7] Packaging mod into {OUTPUT_PAK} using Divine with LZ4...")
    cmd = [DIVINE, "-g", "bg3", "-a", "create-package", "-s", BUILD_DIR, "-d", OUTPUT_PAK, "-c", "lz4"]
    subprocess.run(cmd, check=True)
    pak_size = os.path.getsize(OUTPUT_PAK)
    print(f"    Built PAK: {OUTPUT_PAK} ({pak_size:,} bytes)")
    
    print(f"[8] Installing {OUTPUT_PAK} to {MODS_DIR}...")
    os.makedirs(MODS_DIR, exist_ok=True)
    target_pak = os.path.join(MODS_DIR, f"{MOD_NAME}.pak")
    shutil.copy2(OUTPUT_PAK, target_pak)
    print(f"    Successfully installed to {target_pak}")

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
    print(f"ALL DONE! {MOD_NAME} BUILT AND INSTALLED SUCCESSFULLY!")