# NanoProm
Original Xbox and standalone EEPROM flasher for Arduino Nano / Pro Micro

## Overview & Features

NanoProm is inspired by <a href="https://github.com/Ryzee119/ArduinoProm">Ryzee119’s ArduinoProm</a>, which in turn owes its roots to <a href="https://github.com/grimdoomer/PiPROM">Grimdoomer’s PiPROM</a>.

After two days of trying to breathe life into my CH340-based USB-C Nano clone (MEGA328PB), which stubbornly refused to cooperate, I purchased a Micro variant (MEGA32U4) and - bam - that worked perfectly using Ryzee119’s ArduinoProm.

That could have been the end of it, since I just needed something to replace my last trusty Windows 98 laptop with a dying serial port - but stubbornness is my middle name. I figured, why not make a fun project to see if a bit of AI magic could help me learn C++ and Python enough to understand what’s going on? Maybe then I could even tinker the Nano to work after all.

The result - after plenty of cursing - is <strong>NanoProm</strong>: a tiny little bit of code I hope you all can use, if only because it was made with a healthy, huge dose of <strong>“NO WE WON’T” attitude</strong>.

<img src="images/stubbornness.webp" alt="Stubbornness" width="400">

## What NanoProm Can Do

* Read, write, and erase your <strong>Original Xbox onboard EEPROM</strong> without removing it.
* Read, write, and erase a <strong>standalone EEPROM (24c02)</strong> via chip legs or an adapter.
* Backup to your PC/Laptop as a <code>.bin</code> file.
* Flash the EEPROM with a new <code>.bin</code> file.
* Compare <code>.bin</code> files against the chip or other <code>.bin</code> files.
* Erase the EEPROM with <code>00</code> or <code>FF</code>.

> ⚠️ <strong>Warning:</strong> Use NanoProm at your own risk! It has some safety checks, but it cannot fix everything. Be careful not to short the Xbox or the board, and watch your hands!
