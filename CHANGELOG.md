# Changelog - Baldur's Gate 3: CampBuffs

All notable changes to the **CampBuffs** and **CampBuffsModBuffs** mods are documented in this file.

## [v1.0.0] - Initial Release

### Architecture & Modularity
- **Dual-Mod Architecture**:
  - `CampBuffs.pak` (Base Mod): 100% pure vanilla BG3 camp buffs. No external mod dependencies.
  - `CampBuffsModBuffs.pak` (Optional Add-on): Extends the system with DnD 5.5e Artificer Infusions and Mystra's Spells. Requires `CampBuffs.pak`.
- **100% Native Patch 7 Compatibility**:
  - Built entirely using native Larian Stats, RootTemplates, and Localization.
  - **No Script Extender (SE) required**. Works seamlessly in singleplayer, multiplayer, and official in-game mod environments.

### Spells & Buff Mechanics
- **35m Shout AoE Delivery**:
  - Instant area application for the caster and all party members / summons within 35 meters.
  - Fixed 1-second animation abort by integrating native `CastEffectTextEvent "Cast"` timeline events and `SpellType "Shout"`.
- **Customizable Passives Hotbar Toggles**:
  - Every single buff can be individually toggled on or off from the Passives tab on the hotbar.
  - Only enabled buffs are cast when using the "Camp Buffs" spell.
- **Tiered Aid Spell (Levels 2 through 6)**:
  - Aid is split into 5 distinct tiers (+5, +10, +15, +20, +25 Max HP) to prevent early-game balance distortion.
  - Hierarchical priority ensures only the highest enabled tier is applied.
- **Safe "Remove Buffs" Spell**:
  - Dedicated shout spell that cleanly strips all applied camp buffs from the entire party without touching permanent or other native statuses.

### Item Acquisition & Distribution
- **Guaranteed Traveller's Chest Delivery (OneTimeRewards)**:
  - Leverages Patch 7's official `OneTimeRewards` system.
  - Automatically deposits 2 rings into the player's camp Traveller's Chest upon loading **any** save file (new game or mid-campaign).
- **Comprehensive Merchant Integration (Act 1, Act 2, Act 3)**:
  - Rings sold by all primary merchants across the entire campaign for a nominal price of 1 Gold.
  - Includes: Arron, Dammon, Mattis, Roah Moonglow, Blurg, Lady Esther, Quartermaster Talli, Lann Tarv, Danthelon, Exxvikyap, and more.
- **Ancient Mega Pack (AMP) Conflict Resolution**:
  - Fully integrated across all 108+ AMP vendor subtable variants (`_AMP`, `_None`).
  - Implements Larian's strict `I_` item prefix standard and isolated `new subtable "1,1"` blocks for 100% drop rate guarantee.
