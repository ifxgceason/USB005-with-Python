from USB005_class import IFX #import usb005_class.py

# create dongle obj
dongle=IFX()

# show usb005_class version
print(f"API vers:{dongle.version}")

# scanI2C bus
devicelist=dongle.scanI2C()
print(f"I2C bus:{devicelist}")

# print all device MFR_ID

for device in devicelist:
    deviceaddr=int(device,16)
    dongle.set2page(deviceaddr,0x00)
    print(f"{device} MFR_ID:{dongle.readPMBusMFRID(deviceaddr)}")
    print(f"    Temperature:{dongle.readPMBusTemp(deviceaddr)}C")

# device 0x6C and 0x75 both is Sierra family
print("==start to print Sierra Vout==")
dongle.set2page(0x6c,0) #set 0x6c to page0
print(f"0x6c Vout:{dongle.sierraReadVoutValue(0x6c)}V") # read 0x6c loopA Vout

dongle.set2page(0x6c,1) #set 0x6c to page1
print(f"0x6c Vout:{dongle.sierraReadVoutValue(0x6c)}V") # read 0x6c loopB Vout

dongle.set2page(0x75,0) #set 0x75 to page0
print(f"0x75 Vout:{dongle.sierraReadVoutValue(0x75)}V") # read 0x6c loopA Vout

dongle.set2page(0x75,1) #set 0x75 to page1
print(f"0x75 Vout:{dongle.sierraReadVoutValue(0x75)}V") # read 0x6c loopB Vout
