import socket
import os
import struct
import time
import sys
import subprocess

ICMP_ECHO_REQUEST = 8  

def checksum(source_string):
    """Calculate the checksum of the packet."""
    countTo = (len(source_string) // 2) * 2
    count = 0
    sum = 0
    while count < countTo:
        value = source_string[count + 1] * 256 + source_string[count]
        sum += value
        sum &= 0xffffffff  
        count += 2
    if countTo < len(source_string):
        sum += source_string[len(source_string) - 1]
        sum &= 0xffffffff 
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def create_packet(seq):
    """Create an ICMP packet."""
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, os.getpid(), seq)
    my_checksum = checksum(header)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), os.getpid(), seq)
    return header

def traceroute(destination, max_hops=30):
    """Perform a traceroute to the destination."""
    dest_addr = socket.gethostbyname(destination)
    print(f'Traceroute to {dest_addr} ({destination}), {max_hops} hops max:')
    
    for ttl in range(1, max_hops + 1):
        icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        icmp.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        icmp.settimeout(1)

        packet = create_packet(ttl)
        start_time = time.time()
        icmp.sendto(packet, (destination, 0))

        try:
            recv_packet, addr = icmp.recvfrom(1024)
            round_trip_time = (time.time() - start_time) * 1000  
            print(f'{ttl}\t{round_trip_time:.2f} ms\t{addr[0]}')
            if addr[0] == dest_addr:
                print("Достигнут целевой узел.")
                break  
        except socket.timeout:
            print(f'{ttl}\t* * * Request timed out.')

        icmp.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        destination = input("Введите домен или IP-адрес: ")
    else:
        destination = sys.argv[1]
    
    traceroute(destination)
    
    input("Нажмите Enter для выхода...")