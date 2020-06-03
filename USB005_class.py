import clr

#import USB005.dll 
clr.AddReference("USB005")
clr.FindAssembly("USB005")
from IRDongle import USB005


i2c=USB005()
class IFX():
    def __init__(self):
        self.usbHandle=0
        self.lowbyte=0
        self.highbyte=0
        self.Connect()
        self.version=20200603 #for version control.

    def __str__(self):
        return str(self.usbHandle)
    
    def __call__(self):
        print(f"usbHandle is, {self.usbHandle}")

    def Connect(self):
        self.usbHandle=i2c.Connect()
            
    def Close(self):
        self.usbHandle=i2c.Close(self.usbHandle)
        
    def readReg(self,slaveAddress,regAddress,readData=0):
        result=i2c.ReadRegister(self.usbHandle,slaveAddress,regAddress,readData)
        if result[0]!=0:
            self.status=1
        else:
            __=hex(slaveAddress)
            #set status to zero, it mean commend has been completed. 
            self.status=0
            return __
            
        return 
        
    def scanI2C(self):
        result=list()
        for i in range(0,128):
            temp=self.readReg(i,0)
            if temp == None:
                continue
            else:
                result.append(temp)
        self.status=0
        return result

    def linearFormat16(self,voutmode=8):
        vout_byte=hex(self.highbyte*16*16+self.lowbyte)
        result=((1/(2**voutmode))*int(vout_byte,16))
        return result

        
    def set2page(self, slaveaddress, page):
        pagelist=list()
        pagelist.append(page)
        pagelist.append(0)
        i2c.MrwInitialize()
        i2c.MrwWrite(slaveaddress, 0x00,1, pagelist)
        i2c.MrwExecute(self.usbHandle,1,pagelist)
        return None

    def readPMBusMFRID(self,PMBusSlaveAddress):
        result=self.TxRx(PMBusSlaveAddress,0x99,2)
        result_chr=list()
        result_chr.append(chr(result[1]))
        result_chr.append(chr(result[2]))
                                
        return result_chr
    def Tx(self,PMBusSlaveAddress,Trage_reg,Tx_data):
        Tx_data_list=list()
        Tx_data_list.append(Tx_data)
        i2c.MrwInitialize()
        i2c.MrwWrite(PMBusSlaveAddress,Trage_reg,len(Tx_data_list),Tx_data_list)
        i2c.MrwExecute(self.usbHandle,len(Tx_data_list),Tx_data_list)
        return None
        
    def TxRx(self,PMBusSlaveAddress,Tx_data,Rx_len=0):
        i2c.MrwInitialize()
        Tx_data_list=list()
        result=list()
        #change Tx_data to list()
        Tx_data_list.append(Tx_data)

        Write_data_list=Tx_data_list.copy()
        
        # write_data_list=Tx_data_list+len(Rx_len)
        for i in range(0,Rx_len):
            Write_data_list.append(0)
        
            
        i2c.MrwReadWrite(PMBusSlaveAddress,len(Tx_data_list),Tx_data_list,len(Write_data_list))
        result.append(i2c.MrwExecute(self.usbHandle,len(Tx_data_list),Write_data_list))
        result_list=list()
        for i in range(0,Rx_len+1):
            result_list.append(result[0][1].Get(i))
        
        return result_list[:]
    def sierraReadVoutMode(self,PMBusSlaveAddress):
        result=self.TxRx(PMBusSlaveAddress,0x20,1)
        sierra_vout_mode_dict={34:"10mV/div",33:"5mV/div"}
        result_mode=sierra_vout_mode_dict.get(result[0])
        return result_mode

    def sierraReadVoutValue(self,PMBusSlaveAddress):
        voutmode=self.TxRx(PMBusSlaveAddress,0x20,1)
        if voutmode[0] == 34:
            #10mV/div
            result=self.TxRx(PMBusSlaveAddress,0x8B,1)
            voutvalue=result[0]*0.01+0.49
        elif voutmode[0] ==33:
            #5mV/div
            result=self.TxRx(PMBusSlaveAddress,0x8B,1)
            voutvalue=result[0]*0.005+0.245
        else:
            voutvalue = 99
            pass
        
        return voutvalue

    
    def readPMBusTemp(self,PMBusSlaveAddress):
        result=self.TxRx(PMBusSlaveAddress,0x8d,1)
        temperature=result[0]
        return temperature


if __name__=="__main__":
    dongle=IFX()
    print(dongle.scanI2C())
    dongle.set2page(0x18,0)

    

