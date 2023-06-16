from Utilities import Util
import logging

"""
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                                               /
    /                      NAME                     /
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     CLASS                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TTL                      |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                   RDLENGTH                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    /                     RDATA                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

    """

class AnswerSection:
    def __init__(self, _binaryString):
        self.binaryString = _binaryString

    def get_binaryString(self):
        """ 
            Returns a binary string representation of the QuestionSection 
        """
        return self.binaryString

    def get_NAME(self):
        """
        NAME - a domain name to which this resource record pertains.
        Most moderm DNS servers will use a compressed representation for the 
        NAME object this compress representation    
        0xc Name is a pointer
        0x00c Pointer is to the name at offset 0x00c (0x03777777...)
        You will only have to deal with the compressed respresentation value 0xc00c
        """
        if(self.binaryString[0:16] != "1100000000001100"):
            return "None Pointer Style Not supported"
            logging.info('DNS recieved unsported NAME Format %s', 'not of the form c0c0x', extra={'NAME': self.binaryString[0:16]})

            #raise Exception('parse NAME block in answer section and result was not of from 0xc0 0x0c')
        return b'\xc0\x0c'

    def get_TYPE(self) -> int:
        """
        TYPE - two octets containing one of the RR type codes.  This
        field specifies the meaning of the data in the RDATA field.
                        
        """
        #TODO: Student impment this method
        return Util.binaryToInt(self.binaryString[16:32])

    def get_CLASS(self) -> int:
        """
        CLASS           two octets which specify the class of the data in the
                        RDATA field.
        """
        #TODO: Student impment this method
        return Util.binaryToInt(self.binaryString[32:48])

    def get_TTL(self):
        """
            TTL             a 32 bit unsigned integer that specifies the time
                            interval (in seconds) that the resource record may be
                            cached before it should be discarded.  Zero values are
                            interpreted to mean that the RR can only be used for the
                            transaction in progress, and should not be cached.
        """
        #TODO: Student impment this method
        return Util.binaryToInt(self.binaryString[48:80])

    def get_RDLENGTH(self):
        """RDLENGTH        an unsigned 16 bit integer that specifies the length in
                        octets of the RDATA field.
                        """
        #TODO: Student impment this method
        return Util.binaryToInt(self.binaryString[80:96])

    def set_RDLENGTH(self, _RDLENGTH):
        """
            Function takes an int and sets the length value for RD_DATA
        """
        #TODO: Student impment this method
        RDLENGTH_binary = Util.intToBinary(_RDLENGTH,16)
        self.binaryString = self.binaryString[:80] + RDLENGTH_binary + self.binaryString[96:]
        


    def get_RDATA(self)-> str:
        """
        RDATA           a variable length string of octets that describes the
                        resource.  The format of this information varies
                        according to the TYPE and CLASS of the resource record.
                        For example, the if the TYPE is A and the CLASS is IN,
                        the RDATA field is a 4 octet ARPA Internet address.
        For this assignment only have to support (Type AAAA with CLASS: IN)  and Type: A with CLASS: IN
        """
        #TODO: Student impment this method
        _RDLENGTH = self.get_RDLENGTH()
        _RDATA = self.binaryString[96:(96 + (8*_RDLENGTH))]
        return Util.binaryToIpAddress(_RDATA, 4)

    def set_RDATA(self, _ip_address):
        #TODO: Student impment this method
        _RDLENGTH = len(_ip_address)
        #self.set_RDLENGTH(_RDLENGTH)
        binary_address = Util.IpAddressToBinary(_ip_address, 4)
        self.binaryString = self.binaryString[:96] + binary_address #+ self.binaryString[(96 + (8*_RDLENGTH)):]
        # pass

    def get_RDLENGTH(self):
        """RDLENGTH        an unsigned 16 bit integer that specifies the length in
                        octets of the RDATA field.
                        """
        #TODO: Student impment this method
        return Util.binaryToInt(self.binaryString[80:96])

    def set_RDLENGTH(self, _RDLENGTH):
        """
            Function takes an int and sets the length value for RD_DATA
        """
        #TODO: Student impment this method
        RDLENGTH_binary = Util.intToBinary(_RDLENGTH,16)
        self.binaryString = self.binaryString[:80] + RDLENGTH_binary + self.binaryString[96:]

    def __str__(self):
        """ A to String implementation that used to generate the string for log
            Do not modifiy this is used by the grader        
        """
        return ("Answer Section Information \n"
            +"Name: "+str(self.get_NAME()) +"\n"
            +"Type: "+ str(self.get_TYPE()) +"\n"
            +"Class: "+ str(self.get_CLASS()) +"\n"
            +"TTL: "+ str(self.get_TTL()) +"\n"
            +"RDLENGTH: "+ str(self.get_RDLENGTH()) +"\n"
            +"RDDATA: "+ self.get_RDATA() +"\n")
    
    def serializeAnswerSection(self):
        """
         This function returns a byte array repsenting the answer section it should correctly
         Be carefully when serializing the RDATA field
         
         """ 
        return Util.binaryStringToHex(self.binaryString)

class AnswerParsingManager:
   
    @staticmethod
    def extractAnswerObjects(_binaryString, _answer_count):
        answerArray = []
        len_binary_string = len(_binaryString)
        base = 0  # represents the end position of the last question
        end_of_section = 0 
        rdata_offset = 96
        for currentAnswer in range(0, _answer_count):
            for i in range(base, len_binary_string, 8):
                start_index = base + 80
                end_index = start_index + 16
                rd_length = (8*Util.binaryToInt(_binaryString[start_index:end_index]))
                newbase = i + rdata_offset + rd_length
                answerArray.append(AnswerSection(_binaryString[base:newbase]))
                base = newbase
                end_of_section = base
                break
        return (answerArray,end_of_section)
        