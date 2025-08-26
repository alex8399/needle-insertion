from abc import ABC


class PortBaseException(Exception, ABC):
    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PortReadingDataException(PortBaseException):

    def __init__(self):
        super().__init__("An error occurred while reading data from the port.")


class PortInitializingException(PortBaseException):

    def __init__(self):
        super().__init__("An error occurred while initializing the port.")


class PortParsingDataException(PortBaseException):

    def __init__(self):
        super().__init__("An error occurred during data parsing from the port.")
