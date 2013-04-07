#!/usr/bin/env python
import XmlDict,GlobalObjects
from Components import Events,Component
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ConnectionException
import time
import serial
import logging, logging.config

class RFID(Component.generic):
  Name = "ModbusIO"
  componentName=""
  xmlname=""
  sinkList = []
  sourceList = ['IDOut']
  defaultConfig={}
  defaultState={}
  configuration={}  
 
  rfid_serial_dev=0 
  rfid_serial_timeout=5 
  rfid_serial_sleep=1 
  rfid_log=True 
  rfid_log_file="rfid.log"
  
  def __init__(self,componentName,xmlname):
    Component.generic.__init__(self)
    self.configuration=XmlDict.loadXml(xmlname)
    self.xmlname=xmlname
    self.componentName = componentName

    # Load Configuration for reading (input)
    self.rfid_serial_dev=self.configuration["serial_device"];
    self.rfid_serial_timeout=int(self.configuration["serial_timeout"]);

  def catchEvent(self,component,event,value):
    logger=logging.getLogger("service")

  def start(self):
    # open the serial port
    self.serial = serial.Serial('/dev/serial/by-id/usb-1a86_USB2.0-Ser_-if00-port0', 9600, timeout=5)

    logger=logging.getLogger("service")
    logger.info("Starting Service: " + self.componentName + " (RFID: " + self.xmlname + ").")
    while (GlobalObjects.running):
      code_hex = self.serial.read(14)
      if (len(code_hex)==14):
        try:
          code_dec = int(code_hex[3:11],16)
          Events.generate(self.componentName,'IDOut',{'value':code_dec})
        except ValueError:
          pass
        time.sleep(1)
        self.serial.flushInput() 

    self.serial.close()

