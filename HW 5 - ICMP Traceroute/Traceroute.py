from socket import *
import socket
import os
import sys
import struct
import time
import select
import binascii  
        
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT  = 2.0 
TRIES    = 2
def checksum(string): 
    csum = 0
    countTo = (len(string) // 2) * 2 
    
    count = 0
    while count < countTo:
        #print("string[count+1]: '" + str(string[count+1]) + "' string[count]: '" + str(string[count]) + "'")
        #thisVal = ord(str(string[count+1])) * 256 + ord(str(string[count]))
        thisVal = ord(string[count+1]) * 256 + ord(string[count])
        csum = csum + thisVal 
        csum = csum & 0xffffffff 
        count = count + 2
    
    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff 
    
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum 
    answer = answer & 0xffff 
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer 

def build_header(csum):
    return struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, csum, os.getpid() & 0xFFFF, 1)

def build_packet():
    # Make the header
    # Append checksum to the header.
    # Don't send the packet yet, just return the final packet in this function.
    # So the function ending should look like this
    #TODO: Implement this
    csum = 0
    header = build_header(csum)
    data = struct.pack("d", time.time())
    csum = checksum(str(header + data))
    header = build_header(csum)
    packet = header + data
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):

            destAddr = gethostbyname(hostname)
            #TODO: Student
            # SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw
            #Fill in start
            # Make a raw socket named mySocket
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)
            #Fill in end
            # setsockopt method is used to set the time-to-live field.
            
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    print("  *        *        *    Request timed out.")
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    print("  *        *        *    Request timed out.")
                
            except timeout:
                continue			
            
            else:
                #TODO: Student
                # Fetch the ICMP type and code from the received packet
                #Fill in start
                #Fetch the icmp type from the IP packet
                header = recvPacket[20:28]
                types, code, chksum, packetID, sequence = struct.unpack("bbHHh", header)
                #Fill in end
                #print(types,"\n")
                if types == 11:
                    bytes = struct.calcsize("d") 
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("  %d    rtt=%.0f ms    %s" %(ttl, (timeReceived -t)*1000, addr[0]))
                
                elif types == 3:
                    bytes = struct.calcsize("d") 
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("  %d    rtt=%.0f ms    %s" %(ttl, (timeReceived-t)*1000, addr[0]))
                
                elif types == 0:
                    bytes = struct.calcsize("d") 
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("  %d    rtt=%.0f ms    %s" %(ttl, (timeReceived - timeSent)*1000, addr[0]))
                    return
            
                else:
                    print("error")			
                break	
            finally:				
                mySocket.close()		
get_route("google.com")	
