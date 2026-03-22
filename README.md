# NanoProm
Original Xbox and standalone EEPROM flasher for Arduino Nano / Pro Micro

## Overview & Features

NanoProm is inspired by [Ryzee119’s ArduinoProm](https://github.com/Ryzee119/ArduinoProm), which in turn owes its roots to [Grimdoomer’s PiPROM](https://github.com/grimdoomer/PiPROM).

After two days of trying to breathe life into my CH340-based USB-C Nano clone (MEGA328PB), which stubbornly refused to cooperate, I purchased a Micro variant (MEGA32U4) and **bam** — that worked perfectly using Ryzee119’s ArduinoProm.

That could have been the end of it, since I just needed something to replace my last trusty Windows 98 laptop with a dying serial port — but stubbornness is my middle name. I figured, why not make a fun project to see if a bit of AI magic could help me learn C++ and Python enough to understand what’s going on? Maybe then I could even tinker the Nano to work after all.

The result — after plenty of cursing — is **NanoProm**: a tiny little bit of code I hope you all can use, if only because it was made with a healthy, huge dose of **“NO WE WON’T” attitude**.

![Stubbornness](images/stubbornness.webp)

---

## What NanoProm Can Do

* Read, write, and erase your **Original Xbox onboard EEPROM** without removing it.
* Read, write, and erase a **standalone EEPROM (24c02)** via chip legs or an adapter.
* Backup to your PC/Laptop as a `.bin` file.
* Flash the EEPROM with a new `.bin` file.
* Compare `.bin` files against the chip or other `.bin` files.
* Erase the EEPROM with `00` or `FF`.

---

> ⚠️ **Warning:** Use NanoProm at your own risk! It has some safety checks, but it cannot fix everything. Be careful not to short the Xbox or the board, and watch your hands!

---

NanoProm won’t hold your hand, but it *will* get the job done. Small, cheap, and stubborn — just like me.
