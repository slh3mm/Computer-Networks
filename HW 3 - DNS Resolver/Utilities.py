import struct
import math

class Util:

    @staticmethod
    def hexToBinaryString( _input_Bytes): 
        binaryString = ''
        for byte in _input_Bytes: 
           binaryString += bin(byte)[2:].zfill(8) 
        return binaryString
    
    @staticmethod
    def binaryStringToHex( _input_binary_string):
        hexString = b''
        for i in range(0, len(_input_binary_string), 8): 
            hexString += struct.pack("B", int(_input_binary_string[i: i+8],2))
        return hexString

    @staticmethod 
    def binaryToInt(_input_binary_string):
        if(_input_binary_string == ''):
            return 0

        if len(_input_binary_string) <=  8:
            return  int(_input_binary_string, 2)
        else:
            hexString = Util.binaryStringToHex(_input_binary_string)
            return int.from_bytes(hexString, byteorder='big', signed= False)

    @staticmethod 
    def intToBinary(_input_int, _number_of_bits):
        if(_number_of_bits <= 8):
            return bin(_input_int)[2:].zfill(_number_of_bits)
        else: 
            byteValues = _input_int.to_bytes(math.ceil(_number_of_bits/8), byteorder='big', signed= False)
            return Util.hexToBinaryString(byteValues)[:_number_of_bits]

    @staticmethod
    def boolToBinary(_input_bool): 
        return  '1' if _input_bool == True else '0'
    

    @staticmethod
    def binaryToBool(_input_binary):
        return  True if _input_binary == '1'else False

    @staticmethod
    def binaryToAscii(_input_binary):
        length_of_input = len(_input_binary)
        resultingString = ''
        if length_of_input % 8 != 0: 
            raise Exception('binaryToAscii passed an input binary string whose size was a multiple of 8')
        for i in range(0, length_of_input, 8):
            resultingString += chr(int(_input_binary[i:i+8],2))
        return resultingString

    @staticmethod
    def binaryToAsciiQNAME(_input_binary):
       #TODO: Implement QNAME 
       length_of_input = len(_input_binary)
       if length_of_input % 8 != 0: 
            raise Exception('binaryToAscii passed an input binary string whose size was a multiple of 8')
       resultingString = ''
       end_of_section = 0
       for i in range(0, length_of_input, 8):
           if i == end_of_section:
            end_of_octet = i+8
            end_of_section = end_of_octet+(8*Util.binaryToInt(_input_binary[i:end_of_octet]))
            resultingString += Util.binaryToAscii(_input_binary[end_of_octet:end_of_section])
       return resultingString

    @staticmethod
    def binaryToIpAddress(_input_binary, _ip_version):
        length_of_input = len(_input_binary)
        if _ip_version ==4:
            ip_address = ''
            for i in range(0, length_of_input, 8): 
                ip_address += str(int(_input_binary[i: i+8],2))
                ip_address += "." if i < 24 else ""
            return ip_address
        elif _ip_version == 6: 
            ip_address = 'Needs to Be Implemented'
            return ip_address
            #TODO: Student Add support for parsing IP_Version 6
        else: 
            raise Exception('unknow versino passed to Util.binaryToIpAddress only supports 4 & 6 but got '+ _ip_version)

        
#base+80:base+96
    @staticmethod
    def IpAddressToBinary(_input_Address , _ip_version):
        length_of_input = len(_input_Address)
        if _ip_version ==4:
            binaryString = ''
            octetArray = _input_Address.replace("\n","").split(".")
            for octet in octetArray: 
                binaryString += Util.intToBinary(int(octet), 8)
            return binaryString

        elif _ip_version == 6: 
            binaryString= 'Needs to Be Implemented'
            return binaryString
            #TODO: Student Add support for parsing IP_Version 6
        else: 
            raise Exception('unknow version passed to Util.IpAddressToBinary only supports 4 & 6 but got '+ _ip_version)

