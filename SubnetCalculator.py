#Created By Himansa(github.com/himansaBro)
#in Python 3.10.1(2024)
#Tested on Windows 10 64 bit pc

import math

ts=[128,64,32,16,8,4,2,1]
#---------------------------------------------+Utilitys+------------------------------------------
#Decimal to 8 bit Binary Calculations
def DeTOBin(De):
    out=[0,0,0,0,0,0,0,0]
    if De < 256:
        for i in range(0,8):
            out[7-i]=De%2
            De=De//2
    return out

#8 Bit Binary to Decimal Calculations
def BinTODe(Bin):
    out=0
    for i in range(0,8):
        out+=Bin[i]*(2**(7-i))
    return out

#Binary Counting eg: BCount(2) returns [[0,0],[0,1],[1,0],[1,1]]
def BCount(n):
    total_combinations = 2 ** n
    combinations = []
    for i in range(total_combinations):
        binary_representation = bin(i)[2:].zfill(n)
        combination = [int(bit) for bit in binary_representation]
        combinations.append(combination)
    return combinations

#-------------------------------------------+Calculations+----------------------------------------
#ganarator for Subnets Network Adress using Main Network's Network Adress,CIDR(Net.Bits),No of Subnets
def Subnets(IP,CIDR,Nets):
    networks=[]
    #Creating IP To Binary
    xx=IP.split(".")
    BIP = DeTOBin(int(xx[0]))+DeTOBin(int(xx[1]))+DeTOBin(int(xx[2]))+DeTOBin(int(xx[3]))
    NBits=int(math.ceil(math.log2(int(Nets))))
    Com=BCount(NBits)
    for i in range(0,len(Com)):
        TIP=BIP
        for j in range(0,NBits):
            TIP[CIDR+j]=Com[i][j]
        TIPSet=[TIP[i:i+8] for i in range(0, 32, 8)]
        networks.append(str(BinTODe(TIPSet[0]))+"."+str(BinTODe(TIPSet[1]))+"."+str(BinTODe(TIPSet[2]))+"."+str(BinTODe(TIPSet[3])))
    return networks
    
#Calculate Subnet Mask Using HostBits
def Subnet_Mask(Host):
    out= [0,0,0,0]
    Host=int(Host)
    x=(Host//8)-1
    while x>=0:
        out[x]=255
        x-=1
    lh=Host-(((Host//8)*8))-1
    while lh>=0:
        out[(Host//8)]+=ts[lh]
        lh-=1
    output=str(out[0])+"."+str(out[1])+"."+str(out[2])+"."+str(out[3])
    return output

#Calculate Max Nodes By HostBits
def Nodes(Host):
    Net = 32-int(Host)
    Net = 2**Net
    return Net

#Calculate Network Adress By SubnetMask AND IP
def Net_Addr(SMask,IP):
    NETA=[0,0,0,0]
    SMSet = SMask.split(".")
    IPSet = IP.split(".")
    for i in range(0,4):
        SMSet[i]=int(SMSet[i])
    for i in range(0,4):
        IPSet[i]=int(IPSet[i])
    i=0
    while i<4:
        NETA[i]=SMSet[i] & IPSet[i]
        i+=1
    outp=str(NETA[0])+"."+str(NETA[1])+"."+str(NETA[2])+"."+str(NETA[3])
    return outp

#Calculate Brodcast Adress By NOT(Subnet Mask) OR IP
def Brod_Addr(SMask,IP):
    NETA=[0,0,0,0]
    SMSet = SMask.split(".")
    IPSet = IP.split(".")
    for i in range(0,4):
        SMSet[i]=int(SMSet[i])
        IPSet[i]=int(IPSet[i])
    i=0
    while i<4:
        NETA[i] = SMSet[i] & IPSet[i]
        NETA[i] = NETA[i] | (~SMSet[i] & 0xFF)
        i+=1
    outp=str(NETA[0])+"."+str(NETA[1])+"."+str(NETA[2])+"."+str(NETA[3])
    return outp

def VLSMSubNets(IP,CIDR,Nets):
    Nets=int(Nets)
    nets=[]
    MNets = 2**int(math.log2(Nets))
    FNets = Nets-MNets
    networks=Subnets(IP,CIDR,MNets)
    sci=CIDR+int(math.ceil(math.log2(int(MNets))))
    i=0
    for NetAddr in networks:
        nets.append({
            "Nodes":Nodes(sci),
            "SubMask":Subnet_Mask(sci),
            "NetAddr":networks[i],
            "BroAddr":Brod_Addr(Subnet_Mask(sci),networks[i]),
            "CIDR":sci,
            "LV":0
            })
        i+=1
    for i in range(0,FNets):
        DIP=nets[0]["NetAddr"]
        DCIDR=int(nets[0]["CIDR"])
        DNets=2
        DLV=int(nets[0]["LV"])
        nets.pop(0)
        Dn=Subnets(DIP,DCIDR,DNets)
        nets.append({
            "Nodes":Nodes(DCIDR+1),
            "SubMask":Subnet_Mask(DCIDR+1),
            "NetAddr":Dn[0],
            "BroAddr":Brod_Addr(Subnet_Mask(DCIDR+1),Dn[0]),
            "CIDR":DCIDR+1,
            "LV":DLV+1
            })
        nets.append({
            "Nodes":Nodes(DCIDR+1),
            "SubMask":Subnet_Mask(DCIDR+1),
            "NetAddr":Dn[1],
            "BroAddr":Brod_Addr(Subnet_Mask(DCIDR+1),Dn[1]),
            "CIDR":DCIDR+1,
            "LV":DLV+1
            })
    return nets

#-------------------------------------------+Checks+------------------------------------
def isValidIP(IP):
    v=False
    try:
        cidr=IP.split("/")[1]
        ip = IP.split("/")[0].split(".")
        cidr=int(cidr)
        for i in range(0,4):
            ip[i]=int(ip[i])
        if cidr<33 and ip[0]<256 and ip[1]<256 and ip[2] < 256 and ip[3] < 256:
            v=True 
    except:
        v=False
    return v
#0=OK 1=Isn't A number 2= Too Big
def isValidSN(SN,CIDR):
    v=1
    try:
        if (CIDR+int(math.ceil(math.log2(int(SN)))))<32:
            v=0
        else:
            v=2
    except:
        v=1
    return v

#------------------------------------------Main Program--------------------------------------
def NormalGroup(y,sn):
    if isValidIP(y):
        ip= y.split("/")[0]
        ci = y.split("/")[1]
        ci=int(ci)
        print("Main #",y)
        print("\t-Nodes            :",Nodes(ci))
        print("\t-Subnet Mask      :",Subnet_Mask(ci))
        print("\t-Network Adress   :",Net_Addr(Subnet_Mask(ci),ip))
        print("\t-Brodcast Adress  :",Brod_Addr(Subnet_Mask(ci),Net_Addr(Subnet_Mask(ci),ip)),"\n")
        if sn!="0":
            if isValidSN(sn,ci)==0:
                nAddrs = Subnets(Net_Addr(Subnet_Mask(ci),ip),ci,int(sn))
                sci=ci+int(math.ceil(math.log2(int(sn))))
                cou=1
                for nA in nAddrs:
                    print("Subnet #",cou,"\t",nA,"/",sci)
                    print("\t-Nodes            :",Nodes(sci))
                    print("\t-Subnet Mask      :",Subnet_Mask(sci))
                    print("\t-Network Adress   :",nA)
                    print("\t-Brodcast Adress  :",Brod_Addr(Subnet_Mask(sci),nA),"\n")
                    cou+=1
            elif isValidSN(sn,ci)==1:
                print("This IP can't Handle That much Subnets,Max Subnets for this Network is :",2**(32-int(ci)))
            elif isValidSN(sn,ci)==2:
                print("Subnet Count isn't a Number")
    else:
        print("Invalid IP OR CIDR,use xxxx.xxxx.xxxx.xxxx/yy for ips")
def VLSMGroup(y,sn):
    if isValidIP(y):
        ip= y.split("/")[0]
        ci = y.split("/")[1]
        ci=int(ci)
        print("Main #",y)
        print("\t-Nodes            :",Nodes(ci))
        print("\t-Subnet Mask      :",Subnet_Mask(ci))
        print("\t-Network Adress   :",Net_Addr(Subnet_Mask(ci),ip))
        print("\t-Brodcast Adress  :",Brod_Addr(Subnet_Mask(ci),Net_Addr(Subnet_Mask(ci),ip)),"\n")
        if sn!="0":
            if isValidSN(sn,ci)==0:
                nAddrs = VLSMSubNets(Net_Addr(Subnet_Mask(int(ci)),ip),ci,int(sn))
                cou=1
                for nA in nAddrs:
                    print("Subnet #",cou,"\t",nA["NetAddr"],"/",nA["CIDR"])
                    print("\t-Nodes            :",nA["Nodes"])
                    print("\t-Subnet Mask      :",nA["SubMask"])
                    print("\t-Network Adress   :",nA["NetAddr"])
                    print("\t-Brodcast Adress  :",nA["BroAddr"])
                    print("\t-Subnet Level     :",nA["LV"],"\n")
                    cou+=1
            elif isValidSN(sn,ci)==1:
                print("This IP can't Handle That much Subnets,Max Subnets for this Network is :",2**(32-int(ci)))
            elif isValidSN(sn,ci)==2:
                print("Subnet Count isn't a Number")
while True:
    y=input("Enter IP/CIDR..(e to exit)..............:")
    if y == "e":
            print("\nHave a Nice Day! Exiting\n")
            break
    sn=input("Enter number of Subnets,0 for no subnets:")
    ch=input("Use VLSM Subnetting(y=yes/n=no/i=info)..:")
    if ch=="i":
        print("""
---------------About Subnetting Methods----------------------------
This program uses two popular subnetting methods to create subnets:

1.Standard Subnet Masking (Normal Way)
    This method is simpler and easier to understand. All subnets are of
    equal size, which can lead to wasted IP addresses. For example, if
    we want to create a network with 5 subnets, we would divide the
    available address space into 8 subnets (the next power of 2),
    potentially wasting 3 subnets' worth of addresses.

    >>Easy to Manage
    >>Compatible with OLD Routers and Switchs
    
2.Variable Length Subnet Masking (VLSM)
    VLSM allows for subnets of different sizes, making efficient use of IP
    addresses. This method is more flexible but can be more complex to
    implement. For example, For example, if we want to create a network
    with 5 subnets,VLSM makes 5 subnets with creating 4 subnet and dividing
    1 subnet into 2 subnets,that won't genarate wasting subnets like Standard Way

    PROS
    >>New and Modern Hardware Supports VLSM
    >>reduce the need for additional hardware to manage traffic
    >>More scalable and flexible, potentially reducing the need
      for future reconfiguration and associated costs. It allows
      for better utilization of IP address space, which can be a
      significant cost-saving factor in large networks.

    CONS
    >>More complex to manage because you have subnets of varying
    sizes, which requires more careful planning and management.

NOTE:VLSM Subnets Are Created from that program isn't Totally
     Optimized,There are many factors to consider for Make More
     Optimized Subets,it's hard to do in CLI.Better check is this
     subnets meets your needs.
     Check github.com/himansaBro ,Sometimes New Updates can More Optimised
     or GUI Available
----------------------------------------------------------------------
""")
        ch=input("Use VLSM Subnetting(y=yes/n=no/i=info)..:")
    if ch=="n":
        NormalGroup(y,sn)
    elif ch=="y":
        VLSMGroup(y,sn)
    else:
        print("Invalid Input:",ch)
    ret=input("Program Ended. you can Navigate in here\n\t1.Reuse\n\t2.Exit\n\t3.About\nEnter a Choice:")
    if ret=="2":
        break
    elif ret=="3":
        print("""
---------------------About-------------------------------------
>>>>>>>Advanced Nubnet Calculator<<<<<<<
Version : 1.0 (First Release)
Dev     : Himansa [CodeHack] (github.com/himansaBro)
Tested On: Windows 10(64BIT) python 3.10.1
           Turmux Android with python(pkg install python)
           
    This is a first version of ASC, feel free to comment on
Ideas for improve Program(himansarajapacksha@gmail.com)
This CLI Program created for verify Logic,Java GUI Program
will Comming soon...
detailed instructions can found on readme.md Located on github
Reposatory
    That program Devoloped for classless ip Adresses,but you can
    use other one simply adding there host bit count as cidr
    Class A = 8
    Class B = 16
    Class C = 24
--------------------------------------------------------------
""")
        break
    
