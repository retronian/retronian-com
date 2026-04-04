---
layout: post
title: "How to Name Game Files for Emulators"
date: 2026-04-05
description: "Best practices for naming ROM files so emulators can properly identify games, scrape metadata, and display box art."
tags: [emulation, guide, tips]
---

One of the most common frustrations with retro gaming handhelds is getting your game library organized. You've dumped your ROMs, but they show up as cryptic filenames with no box art and no metadata. The fix? **Proper file naming.**

## Why File Names Matter

Most emulator frontends (EmulationStation, RetroArch playlists, Daijishō, etc.) rely on file names to:

1. **Display game titles** in the UI
2. **Scrape metadata** (descriptions, release dates, genres)
3. **Download box art and screenshots** automatically
4. **Match games to the correct emulator core**

If your files are named `game123.zip` or `ゼルダの伝説 (J) [!].nes`, the scraper will struggle.

## The No-Archive Standard

The most widely supported naming convention follows the **No-Intro** database naming standard:

```
Game Title (Region) [optional flags].extension
```

### Examples

```
Super Mario Bros. (USA).nes
Legend of Zelda, The - A Link to the Past (USA).sfc
Sonic the Hedgehog (Japan, USA).md
Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba
```

### Key Rules

- **Use the full English title** — Don't abbreviate
- **Region in parentheses** — `(USA)`, `(Japan)`, `(Europe)`, `(World)`
- **Revision in parentheses** — `(Rev 1)`, `(Rev 2)` if applicable
- **Articles go after comma** — "Legend of Zelda, The" not "The Legend of Zelda"
- **No special characters** that your filesystem can't handle

## Organizing by System

Keep your ROMs in clearly named directories matching the system:

```
/roms/
├── nes/
│   ├── Super Mario Bros. (USA).nes
│   └── Mega Man 2 (USA).nes
├── snes/
│   ├── Super Mario World (USA).sfc
│   └── Chrono Trigger (USA).sfc
├── gba/
│   ├── Pokemon - Emerald Version (USA, Europe).gba
│   └── Metroid - Zero Mission (USA).gba
└── psp/
    ├── Monster Hunter Freedom Unite (USA).iso
    └── Final Fantasy VII - Crisis Core (USA).iso
```

## Handling Multi-Disc Games

For systems like PS1 where games span multiple discs, use an `.m3u` playlist file:

```
# Final Fantasy VII.m3u
Final Fantasy VII (USA) (Disc 1).chd
Final Fantasy VII (USA) (Disc 2).chd
Final Fantasy VII (USA) (Disc 3).chd
```

The `.m3u` file should be in the same directory as the disc images. Point your emulator at the `.m3u` file, and it will handle disc swapping automatically.

## CHD: The Modern Choice

If you're using CD-based systems (PS1, Dreamcast, Saturn, PSP), convert your ISOs/BIN+CUE files to **CHD (Compressed Hunks of Data)** format:

```bash
chdman createcd -i game.cue -o game.chd
```

Benefits of CHD:

- **Significantly smaller** file sizes (40-60% compression)
- **Single file** per disc (no more BIN + CUE pairs)
- **Lossless** — no quality loss
- **Widely supported** by RetroArch and standalone emulators

## Quick Rename Tips

If you have a large library to rename, these tools can help:

- **Romcenter** or **clrmamepro** — Match and rename against No-Intro DATs
- **Bulk Rename Utility** (Windows) — Pattern-based renaming
- **rename** command (Linux/macOS) — `rename 's/\[!\]//' *.nes` to strip flags

### A Simple Script

For a quick cleanup on Linux/macOS:

```bash
# Remove common junk tags from filenames
for f in *.nes; do
  new=$(echo "$f" | sed 's/ \[!\]//g; s/ \[o[0-9]*\]//g; s/ \[b[0-9]*\]//g')
  [ "$f" != "$new" ] && mv "$f" "$new"
done
```

## The Payoff

Once your files are properly named, scraping becomes automatic. Fire up your frontend's scraper, point it at ScreenScraper or TheGamesDB, and watch as box art, descriptions, and metadata populate your library. It transforms your handheld from a file browser into a proper game console experience.

---

*Taking the time to organize your library upfront saves hours of frustration later. Trust us on this one.*
