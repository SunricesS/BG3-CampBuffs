# Baldur's Gate 3 - Camp Buffs (Toplu Kamp Büyüleri)

[![Game Version](https://img.shields.io/badge/Baldur's%20Gate%203-Patch%207%2B-blue.svg)](https://baldursgate3.game)
[![Script Extender](https://img.shields.io/badge/Script%20Extender-Not%20Required%20(100%25%20Native)-success.svg)](#)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v1.0.0-orange.svg)](https://github.com/SunricesS/BG3-CampBuffs/releases)

A modular, lightweight, and fully native mod for **Baldur's Gate 3 (Patch 7+)** that automates the tedious daily routine of camp buffing. Equip the ring, select your preferred buffs in the Passives hotbar tab, and apply all enabled buffs to your entire party with a single click.

---

## 🌟 Key Features

- **⚡ 1-Click Group Buffing:** Cast all your desired camp buffs instantly on yourself and all allies/summons within **35 meters** via a zero-cost shout spell.
- **🎛️ Individual Hotbar Toggles:** Every buff can be individually turned ON or OFF under the **Passives** tab of your action bar. Only selected buffs are cast!
- **📶 Scalable Aid (Level 2 to Level 6):** Choose the exact tier of the Aid spell (+5, +10, +15, +20, or +25 Max HP) that matches your party level. A built-in priority system ensures only the highest enabled tier is applied.
- **🧹 Dedicated "Remove Buffs" Spell:** Clear all camp buffs at any time with a single click.
- **🎒 Guaranteed Ring Delivery:**
  - **Camp Traveller's Chest:** Uses Patch 7's official `OneTimeRewards` system to deposit 2 copies into your camp chest automatically—works on **new games AND existing saves**.
  - **Comprehensive Merchants:** Sold by all major merchants across Act 1, Act 2, and Act 3 for just **1 Gold**.
  - **Tutorial Chest:** Available in the Cartilaginous Chest on the Nautiloid.
- **🛡️ 100% Native & Stable:** Built entirely with native Larian stats and templates. **No Script Extender (SE) required**. Full controller and keyboard/mouse UI support.
- **🔄 Conflict-Free Compatibility:** Fully tested and compatible with major overhauls, including **Ancient Mega Pack (AMP)** across all vendor table variants.

---

## 📦 Modular Architecture

The mod is divided into two separate, modular packages:

| Package | File | Description | Requirements |
|---|---|---|---|
| **Base Mod** | `CampBuffs.pak` | Contains 22+ pure vanilla Baldur's Gate 3 camp buffs. | None (Base Game Patch 7+) |
| **Optional Add-on** | `CampBuffsModBuffs.pak` | Adds 12 powerful infusions and spells from **DnD 5.5e (Artificer)** and **Mystra's Spells**. | Requires `CampBuffs.pak` |

---

## 📜 Included Buffs

### 1. Base Mod: Vanilla Buffs (`CampBuffs.pak`)

| Buff | In-Game Name | Effect |
|---|---|---|
| **Longstrider** | Uzun Adım | +3m Movement Speed until Long Rest |
| **Mage Armor** | Büyücü Zırhı | Base AC becomes 13 + DEX (unarmored) |
| **Aid (Tier 2-6)** | Destek (Kademeli) | +5 / +10 / +15 / +20 / +25 Maximum HP |
| **Death Ward** | Ölüm Koruması | Survive fatal damage with 1 HP |
| **Freedom of Movement** | Hareket Özgürlüğü | Immunity to Paralysis, Restrained, and difficult terrain |
| **Protection from Poison** | Zehirden Korunma | Poison Resistance + Advantage on Poison saves |
| **Darkvision** | Karanlık Görüşü | See in darkness up to 12m |
| **Heroes' Feast** | Kahramanlar Ziyafeti | +12 Max HP, Immunity to Poison/Frightened, Advantage on WIS saves |
| **Speak with Animals** | Hayvanlarla Konuşma | Understand and converse with beasts |
| **See Invisibility** | Görünmezliği Görme | Detect invisible creatures within 9m |
| **Daylight** | Günışığı | 15m radiant aura dispelling magical darkness |
| **Guidance** | Rehberlik | +1d4 bonus to Ability Checks |
| **Bless** | Kutsama | +1d4 bonus to Attack Rolls and Saving Throws |
| **Shield of Faith** | İnanç Kalkanı | +2 Armor Class (AC) |
| **Stoneskin** | Taş Deri | Resistance to non-magical physical damage |
| **Barkskin** | Ağaç Kabuğu | AC cannot drop below 16 |
| **Feather Fall** | Tüy Düşüşü | Immunity to fall damage |
| **Enhanced Leap** | Gelişmiş Zıplama | Triples jump distance |
| **Hill Giant Strength** | Tepe Devi Gücü | Sets Strength to 21 |
| **Cloud Giant Strength** | Bulut Devi Gücü | Sets Strength to 27 |
| **Morninglord's Radiance** | Morninglord Işıltısı | Adds +1d4 Radiant damage to weapon attacks |
| **Warding Bond** | Koruma Bağı | +1 AC, +1 Saving Throws, Resistance to all damage |

### 2. Add-on: DnD 5.5e & Mystra Buffs (`CampBuffsModBuffs.pak`)

| Buff | Category | Effect |
|---|---|---|
| **Enhanced Defense (+1 / +2)** | Artificer Infusion | +1 or +2 to Armor Class |
| **Enhanced Weapon (+1 / +2)** | Artificer Infusion | +1 or +2 to Weapon Attack and Damage rolls |
| **Returning Weapon** | Artificer Infusion | +1 Weapon bonus + weapon returns instantly upon being thrown |
| **Repeating Shot** | Artificer Infusion | +1 Ranged Weapon bonus + unlimited magical ammunition |
| **Enhanced Arcane Focus (+1 / +2)**| Artificer Infusion | +1 or +2 to Spell Save DC and Spell Attack rolls |
| **Bag of Holding** | Artificer Infusion | Multiplies carrying capacity by **12.5x** |
| **Armor of Magical Strength** | Artificer Infusion | +2 to STR checks/saves + Immunity to Prone/Knockdown |
| **Boots of the Winding Path** | Artificer Infusion | +3m Movement speed + free Misty Step teleport |
| **Repulsion Shield** | Artificer Infusion | +1 AC and +1 to all Saving Throws |
| **Coming of Age** | Mystra's Ceremony | +1d4 bonus to all Ability and Skill checks |
| **Water Walk** | Mystra's Spells | Full immunity to Acid, Deep Water, Mud, Grease/Ice, Difficult Terrain |
| **Gift of Alacrity** | Mystra's Spells | +2 and +1d8 bonus to Initiative rolls |

---

## 🎮 How to Use

1. **Obtain the Ring(s):**
   - Go to your camp and open the **Traveller's Chest** (2 rings are waiting inside).
   - Or buy them from any major merchant for 1 gold.
2. **Equip the Ring:**
   - Equip `CampBuffs_Ring` (or `CampBuffs_ModBuffs_Ring` for the addon).
3. **Configure Your Buffs:**
   - Open your action bar and switch to the **Passives** tab.
   - Toggle individual buffs ON or OFF according to your preference.
   - For Aid, choose the tier that matches your progression (Level 2 to Level 6).
4. **Cast the Spell:**
   - Click the **"Cast Camp Buffs"** spell icon on your hotbar. All party members within 35 meters will receive the enabled buffs simultaneously.
5. **Clear Buffs Anytime:**
   - Click the **"Remove Camp Buffs"** spell to safely wipe the buffs whenever needed.

---

## 📥 Installation

### Method 1: Baldur's Gate 3 Mod Manager (Recommended)
1. Download `CampBuffs-v1.0.0.zip` (and `CampBuffsModBuffs-v1.0.0.zip` if desired) from the official [Releases](https://github.com/SunricesS/BG3-CampBuffs/releases) page.
2. Open **BG3 Mod Manager**.
3. Drag and drop the `.zip` or `.pak` files into the manager window.
4. Move `CampBuffs` (and `CampBuffsModBuffs`) from the right pane (Inactive) to the left pane (Active).
5. Click **File -> Save Order**, then **File -> Export Order to Game**.

### Method 2: In-Game Mod Manager (Patch 7)
1. Place `CampBuffs.pak` (and `CampBuffsModBuffs.pak`) into your mods folder:
   ```
   %LocalAppData%\Larian Studios\Baldur's Gate 3\Mods\
   ```
2. Launch Baldur's Gate 3 and open the **Mod Manager** from the main menu.
3. Enable the mod(s) in the list and apply changes.

### ⚠️ Load Order Advice
If you use loot or shop overhaul mods such as **Ancient Mega Pack (AMP)**:
- Place `CampBuffs` and `CampBuffsModBuffs` **below** Ancient Mega Pack in your load order.
- This ensures the rings appear in vendor inventories regardless of vendor table overrides.

### 🗑️ Safe Uninstallation
To cleanly remove the mod without corrupting your save files:
1. **Cast "Remove Camp Buffs":** Use the "Remove Camp Buffs" spell in-game to clear all active mod statuses from your entire party.
2. **Unequip Rings:** Remove `CampBuffs_Ring` and `CampBuffs_ModBuffs_Ring` from all characters.
3. **Save Game:** Create a fresh manual save file (do not rely solely on autosave/quicksave).
4. **Remove Mod:** Disable or delete the mod in your mod manager, or delete the `.pak` file(s) from your `%LocalAppData%\Larian Studios\Baldur's Gate 3\Mods\` directory.

---

## 🛠️ Building from Source

The repository includes complete build automation using Python and LSLib's Divine CLI.

### Prerequisites
- Python 3.10+
- Pillow (`pip install -r requirements.txt`)
- Windows OS (LSLib Divine is bundled under `tools/lslib/`)

### Build Commands
```bash
# Clone the repository
git clone https://github.com/SunricesS/BG3-CampBuffs.git
cd BG3-CampBuffs

# Install dependencies
pip install -r requirements.txt

# Build Base Mod (produces Releases/CampBuffs.pak)
python build_camp_buffs.py

# Build Add-on Mod (produces Releases/CampBuffsModBuffs.pak)
python build_camp_buffs_modbuffs.py
```

The build scripts will automatically generate DDS textures, UI metadata, RootTemplates, Stats, TreasureTables, OneTimeRewards, and compiled `.loca` files, then bundle everything into LZ4-compressed `.pak` archives.

---

## 🇹🇷 Türkçe Açıklama & Rehber

### Genel Bakış
**CampBuffs**, Baldur's Gate 3'te her uzun dinlenme (Long Rest) sonrası tek tek büyü basma zahmetini ortadan kaldıran pratik bir moddur. Yüzüğü taktığınızda eylem çubuğunuza gelen büyüyle, seçtiğiniz tüm kamp büyülerini tek tıkla 35 metre içindeki tüm grubunuza uygularsınız.

### Öne Çıkan Özellikler
- **Tek Tıkla Toplu Büyü:** Uzun Adım, Kutsama, Koruma Bağı, Destek, Günışığı, vb. tüm büyüleri saniyeler içinde uygular.
- **Pasifler Sekmesinden Açma/Kapama:** Hangi büyüyü isteyip istemediğinizi eylem çubuğundaki **Pasifler** sekmesinden tek tıkla özelleştirebilirsiniz. Sadece açık bıraktığınız büyüler basılır.
- **Kademeli Destek (Aid 2 - 6):** Oyunun başındayken dengenin bozulmaması için Destek büyüsünü Seviye 2'den (+5 HP) Seviye 6'ya (+25 HP) kadar seçebilirsiniz.
- **Buff Temizleme:** İstediğiniz an "Buffları Kaldır" büyüsüyle tüm mod etkilerini temizleyebilirsiniz.
- **Garantili Erişim (Kamp Sandığı & Satıcılar):**
  - Haritadan **"Kampa Git"** dediğinizde yatağınızın yanındaki **Gezgin Sandığı'nda (Traveller's Chest)** 2 adet yüzük sizi bekler (yeni oyun veya kayıtlı oyun fark etmeksizin).
  - Act 1, Act 2 ve Act 3'teki tüm ana tüccarlarda **1 Altın** karşılığında satılır.
- **%100 Patch 7 Uyumlu:** Script Extender gerektirmez, doğrudan oyun motorunun yerel sistemiyle çalışır.

### Kurulum
1. [Releases (Sürümler)](https://github.com/SunricesS/BG3-CampBuffs/releases) sayfasından `.pak` dosyalarını veya `.zip` arşivini indirin.
2. `C:\Users\<KullanıcıAdınız>\AppData\Local\Larian Studios\Baldur's Gate 3\Mods\` klasörüne kopyalayın.
3. BG3 Mod Manager veya oyun içi mod yöneticisinden aktifleştirip kaydedin.

### 🗑️ Güvenli Mod Kaldırma (Safe Uninstallation)
Kayıt dosyanızın (save) zarar görmemesi ve modun sorunsuz kaldırılması için şu adımları izleyin:
1. **Büyüleri Temizleyin:** Oyunda "Remove Camp Buffs" (Buffları Kaldır) büyüsünü kullanarak tüm gruptaki aktif mod bufflarını temizleyin.
2. **Yüzükleri Çıkarın:** Karakterlerinizin üzerindeki mod yüzüklerini (`CampBuffs_Ring`, `CampBuffs_ModBuffs_Ring`) çıkarıp envantere veya sandığa koyun.
3. **Oyunu Kaydedin:** Temiz bir manuel kayıt (Manual Save) alın.
4. **Modu Kaldırın:** Mod yöneticisinden modu devre dışı bırakın veya `.pak` dosyasını `Mods/` klasöründen silin.

---

## 📄 License & Legal Notice

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License ([CC BY-NC 4.0](LICENSE))**.

You are free to share, copy, and adapt this material for **non-commercial** purposes, provided appropriate credit is given. Commercial distribution, sale, or paywalling of this mod or any derivative works is strictly prohibited.

---

## ⚖️ Legal Disclaimer (Yasal Uyarı)

- **Baldur's Gate 3** is a registered trademark of **Larian Studios Games Ltd.**
- **Dungeons & Dragons (D&D)**, Forgotten Realms, and associated names and mechanics are trademarks and copyrights of **Wizards of the Coast LLC**, a subsidiary of **Hasbro, Inc.**
- This project is an **unofficial, non-profit, fan-made modification** created solely for community entertainment.
- It is **not endorsed by, sponsored by, or affiliated with** Larian Studios or Wizards of the Coast.
- All original game assets, engine logic, and intellectual properties belong to their respective copyright holders.
