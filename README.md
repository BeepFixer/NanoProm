# NanoProm
Original Xbox and standalone EEPROM flasher for Arduino Nano / Pro Micro

![NanoProm Main](images/nanoprom_main.jpg)

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

# Wiring Guide

Below are the pinout diagrams used in this setup. 

All diagrams are colour-coded in each picture, to help you match the correct pin connections between components.

![Xbox LPC Pinout](images/Xbox_LPC-pinout.jpg)
![Arduino Nano Pinout](images/nano-pinout.jpg)
![Pro Micro Pinout](images/proMicro-pinout.jpg)
![24C02 Pinout](images/24c02-pinout.jpg)
![SOIC8 to DIP8 Adapter Pinout](images/soic8-to-dip8-adapter-pintout.jpg)

---

### >> IMPORTANT <<

Do **NOT** connect the **RED WIRE** when wiring directly to the Xbox!

The red wire (3.3V) is only required when powering the EEPROM externally, and should be left disconnected when using the Xbox as the power source!

Likewise, ensure that neither the Arduino board nor its pins (depending on the type used) come into contact with the Xbox mainboard surface or casing (GND), as this may cause a short circuit to the Xbox or the board!

---

## External EEPROM Connections

The 3.3V wire must be connected when working with the EEPROM outside of the Xbox, for example:

- Directly wiring to a 24C02 chip  
- Using a SOIC8-to-DIP8 adapter  

In these cases, the EEPROM must be powered by the board.

## Voltage Notes

The 24C02 EEPROM supports a supply voltage between **1.8V and 5.5V**.

Depending on the board used, you can supply either 3.3V or 5V from the board.

## Wires
I used pin headers on the Xbox, both boards, and the SOIC8 to DIP8 adapter, together with 10 cm female-to-female Dupont wires that connect to the male headers, as shown in the photos. 

However, the specific method is not critical - the connections themselves are what matter. 

You can also solder wires directly from the board to the LPC if preferred.

Keep the wires relatively short, as longer wires increase the chance of connection issues or failure.

---

# Arduino Setup

Firstly, NanoProm's firmware was written because I could not get my Nano clone to work with ArduinoProm. This is my first attempt at both C++ and Python, so the whole thing is essentially the result of a lot of trial and error, plenty of help from ChatGPT, and a lot of testing and re-testing.

In the end, it very much falls into the category of "it works on my computer" and "it works with the specific clone I have in my hand".

I was actually expecting to fall back to ArduinoProm for the Pro Micro, but NanoProm ended up working very nicely on both boards, which hopefully means it will also work with whatever Arduino clone you are using.

For reference, **the Nano** I used was sold as:
"Nano 3.0 Mini Type-C USB With the bootloader compatible Nano controller for Arduino CH340 USB driver 16MHz ATMEGA328PB"

The **Pro Micro** I used was sold as:
"Pro Micro ATmega32U4 5V 16MHz Replace ATmega328 For Arduino TYPE-C With 2 Row Pin Header for Leonardo Mini USB Interface Pro"

I am not linking to specific AliExpress listings, as these tend to appear and disappear frequently. The descriptions above are provided so you know what was tested.

---

## Software Setup: CH340 Driver

Check your computer's Device Manager and see if your Nano clone appears correctly under "Ports (COM & LPT)". 

In many cases, it will not show up properly by default, and you will need to install the appropriate drivers.

If you do not see it listed, as shown in the image below:

![Device Manager CH340 Missing](images/CH340-device-manager.jpg)

You will most likely need to install the CH340 driver for your Nano clone. 

This can be downloaded from WCH's official English website: https://wch-ic.com/downloads/CH341SER_ZIP.html -> **CH341SER.EXE**

Once you’ve installed the driver, check Device Manager again - your board should now be recognized and assigned a COM port.

## Software Setup: Arduino IDE

Once your board is recognized in Device Manager, you will need to install **Arduino IDE** to compile and upload the firmware to your board.

Download the latest version from here: https://www.arduino.cc/en/software/ (I am currently using 2.3.8).

1. Open `NanoProm.ino` in Arduino IDE
2. Select the right board
3. Select the right COM port
4. Verify 
5. Program

## Selecting the Right Board

First, make sure the correct board is selected from the Arduino IDE's list of available boards.  

Example for the **Pro Micro** variant (MEGA32U4 / Leonardo):  
![Pro Micro Board Selection](images/ide01promicro.jpg)

Example for the **Nano** variant (MEGA328PB / CH340-Based):  
![Nano Board Selection](images/ide02nano.jpg)

---

## Selecting the Right COM Port

Next, make sure the correct COM port is assigned.  

Check Windows Device Manager to see the assigned ports.  

**Pro Micro (MEGA32U4 / Leonardo)**:  
Device Manager view:  
![Pro Micro Device Manager](images/ProMicro-device-manager.jpg)  

COM port selection in Arduino IDE:  
![Pro Micro COM Port](images/ide01bpromicro.jpg)

**Nano (MEGA328PB / CH340-Based)**:  
Device Manager view:  
![Nano Device Manager](images/CH340-device-manager.jpg)  

COM port selection in Arduino IDE:  
![Nano COM Port](images/ide02bnano.jpg)

---

## Final Check in Arduino IDE

Once you have assigned the correct board and COM port, the bottom right of the Arduino IDE window should show the selected board and port.  

**Pro Micro (MEGA32U4 / Leonardo)**:  
![Pro Micro Final Check](images/ide01cpromicro.jpg)

**Nano (MEGA328PB / CH340-Based)**:  
![Nano Final Check](images/ide02cnano.jpg)

---

## Program the Firmware

Last but not least, hit the **Upload** button in Arduino IDE to write the firmware to your board. 

![Upload](images/ide01dpromicro.jpg)

You'll need to wait a few seconds. You may hear the typical USB connect/disconnect sounds, and once the upload finishes, you should see a message like this:

![Upload Complete](images/ide-doneuploading.jpg)

At this point, the firmware is successfully on your board. From here, we will use a Python script with a menu of options (explained in the next section) to read, write, or compare the EEPROM.

