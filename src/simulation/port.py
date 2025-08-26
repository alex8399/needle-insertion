from abc import ABC, abstractmethod
from typing import Dict, override
import serial
import time

from exception import PortReadingDataException, PortInitializingException, PortParsingDataException


class AbstractPortReader(ABC):

    @abstractmethod
    def read(self) -> str:
        pass


class AbstractPortParser(ABC):

    @abstractmethod
    def parse(self, rawData: str) -> Dict:
        pass


class AbstractPortControllerSingleton(ABC):
    portReader: AbstractPortReader
    portParser: AbstractPortParser
    instance: 'AbstractPortControllerSingleton' = None

    def __new__(cls) -> 'AbstractPortControllerSingleton':
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.init()
        return cls.instance

    @abstractmethod
    def init(self) -> None:
        pass

    def getData(self) -> Dict:
        rawData = self.portReader.read()
        parsedData = self.portParser.parse(rawData)
        return parsedData


class Port9600COM3Reader(AbstractPortReader):
    SERIAL_PORT: str = 'COM3'
    BAUD_RATE: int = 115200

    body: serial.Serial

    def __init__(self):
        try:
            self.body = serial.Serial(
                self.SERIAL_PORT, self.BAUD_RATE, timeout=1)
        except:
            self.body = None
            raise PortInitializingException()

        time.sleep(2)

    @override
    def read(self) -> str:
        rawData = str()

        while True:
            if self.body.in_waiting > 0:
                try:
                    rawData = self.body.readline().decode('utf-8').strip()
                except:
                    raise PortReadingDataException()

                break
        
        return rawData


class BarPortParser(AbstractPortParser):

    @override
    def parse(self, rawData: str) -> Dict:
        parsedData = dict()
        
        try:
            parsedData = {
                k.strip(): float(v)
                for k, v in (part.split('=')
                             for part in rawData.split('|'))
            }
        except:
            raise PortParsingDataException()
        
        return parsedData


class Bar9600COM3PortControllerSingleton(AbstractPortControllerSingleton):

    def init(self) -> None:
        self.portReader = Port9600COM3Reader()
        self.portParser = BarPortParser()
