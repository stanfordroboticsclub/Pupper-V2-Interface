from enum import Enum


class SerialReaderState(Enum):
    WAITING_BYTE1 = 0
    WAITING_BYTE2 = 1
    READING_LENGTH_BYTE1 = 2
    READING_LENGTH_BYTE2 = 3
    READING = 4


class NonBlockingSerialReader:
    def __init__(self, serial_handle, start_byte=69, start_byte2=69):
        self.start_byte = start_byte
        self.start_byte2 = start_byte2
        self.serial_handle = serial_handle
        self.byte_buffer = b""
        self.mode = SerialReaderState.WAITING_BYTE1
        self.message_length = -1

    def chew(self):
        while True:
            raw_data = self.serial_handle.read(1024)
            if not raw_data:
                break
            for in_byte in raw_data:
                if self.mode == SerialReaderState.WAITING_BYTE1:
                    if in_byte == self.start_byte:
                        self.mode = SerialReaderState.WAITING_BYTE2
                elif self.mode == SerialReaderState.WAITING_BYTE2:
                    if in_byte == self.start_byte2:
                        self.mode = SerialReaderState.READING_LENGTH_BYTE1
                    else:
                        self.mode = SerialReaderState.WAITING_BYTE1
                elif self.mode == SerialReaderState.READING_LENGTH_BYTE1:
                    self.message_length = int(in_byte) * 256
                    self.mode = SerialReaderState.READING_LENGTH_BYTE2
                elif self.mode == SerialReaderState.READING_LENGTH_BYTE2:
                    self.message_length += int(in_byte)
                    self.mode = SerialReaderState.READING
                elif self.mode == SerialReaderState.READING:
                    self.byte_buffer += bytes([in_byte])
                    if len(self.byte_buffer) == self.message_length:
                        self.message_length = -1
                        self.mode = SerialReaderState.WAITING_BYTE1
                        temp = self.byte_buffer
                        self.byte_buffer = b""
                        return temp
        return None
