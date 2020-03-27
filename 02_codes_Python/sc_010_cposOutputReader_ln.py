#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: cposOutputReader_ln.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2020-03-23 15:02:34
# Last Modified: 2020-03-27 15:45:09
################################################################# 

from __future__ import print_function
from struct import unpack,pack
import time, datetime
import getopt
import sys
import os

def usage():
    print('Usage:\n' \
            ' -h, --help: print help message. \n' \
            ' -v, --version: print script version.\n' \
            ' -f, --filename: the name of file which will be dealed.\n' \
            ' -w, --write: the log which contains all the result.(format as csv)\n' \
            ' eg: ./%s -f ln_tdm_pcm.pcap -w abc.csv\n' \
            '' % os.path.basename(__file__))
    sys.exit()

def version():
    print("Version: 1.0.1")
    sys.exit()

def get_one_pkt(fp):
    pkt_head=fp.read(16)
    if pkt_head == '':
        return None
    frame_len=unpack("I",pkt_head[8:12])[0]
    frame=fp.read(frame_len)
    return frame

def a2s(ascii_str):
    str_hex_out = ""
    for c in ascii_str:
        str_hex_out += str('%02x' % ord(c))
    return str_hex_out

def std_print(ascii_str, char=" ", tail=True, text_h = "", text_t = ""):
    if tail == True:
        print(text_h+char.join("{:02x}".format(ord(c)) for c in ascii_str)+text_t)
    else:
        print(text_h+char.join("{:02x}".format(ord(c)) for c in ascii_str)+text_t, end = "")
    return char.join("{:02x}".format(ord(c)) for c in ascii_str)

def mac_print(pkt_ptr):
    mac = pkt_ptr[0:12]
    dmac = std_print(mac[0:6], ":", False, "DMAC/SMAC：", "/")
    smac = std_print(mac[6:12], ":")
    return dmac + "/" + smac

def log_title_write(pkt_ptr):
    if a2s(pkt_ptr[14:16]) + a2s(pkt_ptr[16:18]) == "444802fd" and cnt == 1:
        flog.write("PktSN,DMAC/SMAC,PktLen,PktType,SeqNum,DevType,ChasID,SlotID,CardType,HwVer,Cap2M,HwChIDFist,OptPortInfFirst,FrameNumFirst,E1TextFirst,HwChIDLast,OptPortInfLast,FrameNumLast,E1TextLast\n")
    elif a2s(pkt_ptr[14:16]) + a2s(pkt_ptr[16:18]) == "1e0701fe" and cnt == 1:
        flog.write("PktSN,DMAC/SMAC,PktLen,PktType,SeqNum,DataLen,PktType,ChassisID,CapTime,CapTime(ns),InfType,UpDownLink,CardType,SlotID,SigType,TsRate,OptPortInf,HwChID,TsChID,SS7Text\n")
    elif a2s(pkt_ptr[14:16]) + a2s(pkt_ptr[16:18]) == "444811ee" and cnt == 1:
        flog.write("PktSN,DMAC/SMAC,PktLen,PktType,SeqNum,DevType,ChassisID,SlotID,CardType,HwVer,GroupNum,TimeStampFlag,ReservedField,PktLen,PktType,OptPortInf,ChID,VPI/VCI,CapTime,CapTime(ns),AAL2Text\n")
    elif a2s(pkt_ptr[14:16]) + a2s(pkt_ptr[16:18]) == "1e0712ed" and cnt == 1:
        flog.write("PktSN,DMAC/SMAC,PktLen,PktType,SeqNum,PktLen,PktType,ChassisID,CapTime,CapTime(ns),ChID,VPI/VCI,ReservedFiled,AAL5Text\n")

def ana_tdm_pcm(pkt_ptr):
    pcm_pkt_seq_int = unpack("I",pkt_ptr[18:22])[0]
    pcm_pkt_seq = "0x" + a2s(pkt_ptr[18:22]) + "(" + str(pcm_pkt_seq_int) + ")"
    pcm_dev_type = "0x" + a2s(pkt_ptr[22])
    pcm_chassis_id = int(a2s(pkt_ptr[23]), 16)
    pcm_slot_id = int(a2s(pkt_ptr[24]), 16)
    pcm_card_type = "0x" + a2s(pkt_ptr[25])
    pcm_hw_ver = "0x" + a2s(pkt_ptr[26])
    pcm_fr_2M = int(a2s(pkt_ptr[27]), 16)
    print('Packet sequence num: %s\n'\
            'Dev_type: %s\n'\
            'Chassis id: %d\n'\
            'Slot id: %d\n'\
            'Card type: %s\n'\
            'Hardware version: %s\n'\
            'Capacity of 2M: %d'
            '' % (pcm_pkt_seq, pcm_dev_type, pcm_chassis_id, pcm_slot_id, pcm_card_type, pcm_hw_ver, pcm_fr_2M))
    pkt_e1 = pkt_ptr[28:]
    for num in range(0,42):
        pcm_e1_id_hw = int(a2s(pkt_e1[35*num]), 16)
        print("Hw chID: %d" % pcm_e1_id_hw)
        if pcm_card_type == "0x18":
            pcm_port_id = (int(a2s(pkt_e1[35*num + 1]),16) >> 1) & 0x7f
            pcm_port_info = pcm_slot_id
        elif pcm_card_type == "0x1e":
            pcm_port_id = (int(a2s(pkt_e1[35*num + 1]),16) >> 7) & 0x01
            pcm_ch_155M = (int(a2s(pkt_e1[35*num + 1]),16) >> 1) & 0x3f
            pcm_port_info = str(pcm_port_id) + "/" + str(pcm_ch_155M)
        print("Opt port info: %s" % pcm_port_info)
        pcm_fr_num =int(a2s(pkt_e1[35*num + 2]), 16)
        print("Frame count: %d" % pcm_fr_num)
        pcm_text = a2s(pkt_e1[35*num + 3:35*(num+1)])
        print("PCM text: %s" % pcm_text)
        if num == 0:
            first_e1_hw_id = str(pcm_e1_id_hw)
            first_pcm_port_info = pcm_port_info
            first_fr_num = str(pcm_fr_num)
            first_pcm_text = pcm_text
            first_e1 = first_e1_hw_id+","+first_pcm_port_info+","+first_fr_num+","+first_pcm_text
        elif num == 41:
            last_e1_hw_id = str(pcm_e1_id_hw)
            last_pcm_port_info = pcm_port_info
            last_fr_num = str(pcm_fr_num)
            last_pcm_text = pcm_text
            last_e1 = last_e1_hw_id+","+last_pcm_port_info+","+last_fr_num+","+last_pcm_text
    pkt_pcm_result = pcm_pkt_seq+","+pcm_dev_type+","+str(pcm_chassis_id)+","+str(pcm_slot_id)\
                    +","+pcm_card_type+","+pcm_hw_ver+","+str(pcm_fr_2M)+","+first_e1+","+last_e1
    return pkt_pcm_result

def ana_tdm_ss7(pkt_ptr):
    ss7_pkt_seq_int = unpack("I",pkt_ptr[18:22])[0]
    ss7_pkt_seq = "0x" + a2s(pkt_ptr[18:22]) + "(" + str(ss7_pkt_seq_int) + ")"
    ss7_pkt_len = unpack("h",pkt_ptr[22:24])[0]
    ss7_pkt_type = "0x" + a2s(pkt_ptr[24])
    ss7_chassis_id = int(a2s(pkt_ptr[25]), 16)
    ss7_time_sec = unpack("I",pkt_ptr[26:30])[0]
    ss7_time_sec_str = time.strftime(" %Y-%m-%d %H:%M:%S", time.localtime(ss7_time_sec))
    ss7_time_nansec = unpack("I",pkt_ptr[30:34])[0]
    ss7_channel_id = unpack("I", pkt_ptr[34:38])[0]
    ss7_inf_type = (ss7_channel_id >> 28) & 0x0f
    ss7_up_down = (ss7_channel_id >> 27) & 0x01
    ss7_card_type = (ss7_channel_id >> 24) & 0x07
    ss7_slot_id = (ss7_channel_id >> 20) & 0x0f
    ss7_signal_type = (ss7_channel_id >> 18) & 0x03
    ss7_ts_rate = (ss7_channel_id >> 16) & 0x03
    ss7_opt_id_l = (ss7_channel_id >> 13) & 0x07
    ss7_opt_id_h = (ss7_channel_id >> 11) & 0x03
    ss7_opt_id = (ss7_opt_id_h << 3) + ss7_opt_id_l
    ss7_hw_id = (ss7_channel_id >> 5) & 0x3f
    ss7_ts_2M = ss7_channel_id & 0x1f
    ss7_text = a2s(pkt_ptr[38:])
    print('Packet sequence num: %s\n'\
            'Data length: %d\n'\
            'Packet type: %s\n'\
            'Chassis id: %d\n'\
            'Capture time: %s\n'\
            'Capture time(ns): %s\n'\
            'Interface type: %s\n'\
            'Uplink or Downlink: %s\n'\
            'Card type: %s\n'\
            'Slot id: %s\n'\
            'Signal type: %s\n'\
            'Ts rate: %s\n'\
            'Optical port id: %d\n'\
            'Hw channel id: %d\n'\
            'Ts channel id: %d\n'\
            'SS7 text: %s\n'\
            '' % (ss7_pkt_seq, ss7_pkt_len, ss7_pkt_type, ss7_chassis_id, ss7_time_sec_str, ss7_time_nansec, bin(ss7_inf_type), \
                ss7_up_down, ss7_card_type, ss7_slot_id, bin(ss7_signal_type), bin(ss7_ts_rate), ss7_opt_id, ss7_hw_id, ss7_ts_2M, ss7_text))
    pkt_ss7_result = ss7_pkt_seq+","+str(ss7_pkt_len)+","+ss7_pkt_type+","+str(ss7_chassis_id)+","+ss7_time_sec_str+","\
                    +str(ss7_time_nansec)+","+str(ss7_inf_type)+","+str(ss7_up_down)+","+str(ss7_card_type)+","\
                    +str(ss7_slot_id)+","+bin(ss7_signal_type)+","+bin(ss7_ts_rate)+","+str(ss7_opt_id)+","+str(ss7_hw_id)+","+str(ss7_ts_2M)+","+ss7_text
    return pkt_ss7_result

def ana_atm_aal2(pkt_ptr):
    aal2_pkt_seq_int = unpack("I",pkt_ptr[18:22])[0]
    aal2_pkt_seq = "0x" + a2s(pkt_ptr[18:22]) + "(" + str(aal2_pkt_seq_int) + ")"
    aal2_dev_type = "0x" + a2s(pkt_ptr[22])
    aal2_chassis_id = int(a2s(pkt_ptr[23]), 16)
    aal2_slot_id = int(a2s(pkt_ptr[24]), 16) + 1
    aal2_card_type = "0x" + a2s(pkt_ptr[25])
    aal2_hw_ver = "0x" + a2s(pkt_ptr[26])
    aal2_group_num = int(a2s(pkt_ptr[27]), 16)
    aal2_flag_timestamp = "0x" + a2s(pkt_ptr[28])
    aal2_reserved = "0x" + a2s(pkt_ptr[29:40])
    aal2_pkt_len = int(a2s(pkt_ptr[40]), 16)
    aal2_ptk_type = "0x" + a2s(pkt_ptr[41])
    aal2_opt_id = int(a2s(pkt_ptr[42]), 16)
    aal2_opt_id_155M = str(aal2_opt_id)
    aal2_opt_id_10Ge = str(aal2_opt_id >> 7 & 0x01) + "-" + str(aal2_opt_id >> 1 & 0x3f)
    aal2_opt_id_str = "0x" + a2s(pkt_ptr[42]) + "(" + aal2_opt_id_155M + "/" + aal2_opt_id_10Ge + ")"
    aal2_channel_id = "0x" + a2s(pkt_ptr[43])
    aal2_vpi_vci = "0x" + a2s(pkt_ptr[44:48])
    if aal2_flag_timestamp == "0x01":
        aal2_time_sec = unpack("I",pkt_ptr[48:52])[0]
        aal2_time_sec_str = time.strftime(" %Y-%m-%d %H:%M:%S", time.localtime(aal2_time_sec))
        aal2_time_nansec = unpack("I",pkt_ptr[52:56])[0]
        aal2_text = a2s(pkt_ptr[56:])
    elif aal2_flag_timestamp == "0x00":
        aal2_time_sec_str = "---"
        aal2_time_nansec = "---"
        aal2_text = a2s(pkt_ptr[48:])
    else:
        print("Error 2: Timestamp field error!")
    print('Packet sequence num: %s\n'\
            'Device type: %s\n'\
            'Chassis id: %d\n'\
            'Slot id: %d\n'\
            'Card type: %s\n'\
            'Hardware version: %s\n'\
            'Group num: %d\n'\
            'Timestamp or not: %s\n'\
            'Reserved field: %s\n'\
            'Packet length: %d\n'\
            'Packet type: %s\n'\
            'Optical port id: %s\n'\
            'Channel id: %s\n'\
            'VPI/VCI: %s\n'\
            'Capture Time: %s\n'\
            'Capture Time(ns): %s\n'\
            'AAL2 text: %s\n'\
            '' % (aal2_pkt_seq, aal2_dev_type, aal2_chassis_id, aal2_slot_id, aal2_card_type, aal2_hw_ver,\
                aal2_group_num, aal2_flag_timestamp, aal2_reserved, aal2_pkt_len, aal2_ptk_type,aal2_opt_id_str,\
                aal2_channel_id, aal2_vpi_vci, aal2_time_sec_str, aal2_time_nansec, aal2_text))
    pkt_aal2_result = aal2_pkt_seq+","+aal2_dev_type+","+str(aal2_chassis_id)+","+str(aal2_slot_id)+","+aal2_card_type+","+aal2_hw_ver\
                    +","+str(aal2_group_num)+","+aal2_flag_timestamp+","+aal2_reserved+","+str(aal2_pkt_len)+","+aal2_ptk_type\
                    +","+aal2_opt_id_str+","+aal2_channel_id+","+aal2_vpi_vci+","+aal2_time_sec_str+","+str(aal2_time_nansec)+","+aal2_text 
    return pkt_aal2_result

def ana_atm_aal5(pkt_ptr):
    aal5_pkt_seq_int = unpack("I",pkt_ptr[18:22])[0]
    aal5_pkt_seq = "0x" + a2s(pkt_ptr[18:22]) + "(" + str(aal5_pkt_seq_int) + ")"
    aal5_pkt_len = unpack("h",pkt_ptr[22:24])[0]
    aal5_ptk_type = "0x" + a2s(pkt_ptr[24])
    aal5_chassis_id = int(a2s(pkt_ptr[25]), 16)
    aal5_time_sec = unpack("I",pkt_ptr[26:30])[0]
    #aal5_time_sec = int(a2s(pkt_ptr[26:30]), 16)
    aal5_time_sec_str = time.strftime(" %Y-%m-%d %H:%M:%S", time.localtime(aal5_time_sec))
    aal5_time_nansec = unpack("I",pkt_ptr[30:34])[0]
    aal5_channel_id = unpack("I", pkt_ptr[34:38])[0]
    aal5_channel = (aal5_channel_id >> 17) & 0xff
    aal5_vpi_vci = "0x" + a2s(pkt_ptr[38:42])
    aal5_reserved = "0x" + a2s(pkt_ptr[42:46])
    aal5_text = a2s(pkt_ptr[46:])
    print('Packet sequence num: %s\n'\
            'Packet length: %d\n'\
            'Packet type: %s\n'\
            'Chassis id: %d\n'\
            'Capture Time: %s\n'\
            'Capture Time(ns): %s\n'\
            'Channel id: %d\n'\
            'VPI/VCI: %s\n'\
            'Reserved field: %s\n'\
            'AAL5 text: %s\n'\
            '' % (aal5_pkt_seq, aal5_pkt_len, aal5_ptk_type, aal5_chassis_id, aal5_time_sec_str,\
                aal5_time_nansec, aal5_channel, aal5_vpi_vci, aal5_reserved, aal5_text))
    pkt_aal5_result = aal5_pkt_seq+","+str(aal5_pkt_len)+","+aal5_ptk_type+","+str(aal5_chassis_id)+","+aal5_time_sec_str\
                    +","+str(aal5_time_nansec)+","+str(aal5_channel)+","+aal5_vpi_vci+","+aal5_reserved+","+aal5_text
    return pkt_aal5_result

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvf:w:", ["help", "version", "filename=", "write="])
        if len(opts) == 0:
            usage()
    except getopt.GetoptError:
        usage()
    
    now_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    log_name = "xxx_" + now_str + ".csv"
    file_name = "ln_tdm_pcm.pcap"
    for name, value in opts:
        if name in ('-h', '--help'):
            usage()
        elif name in ('-v', '--version'):
            version()
        elif name in ('-f', '--filename'):
            file_name = value
        elif name in ('-w', '--write'):
            log_name = value.split(".")[0] + "_" + now_str + ".csv"
            print(log_name)

    cnt = 1
    flog = open(log_name, "w")
    fpcap = open(file_name,"r")
    fpcap.read(24)
    while 1:
        pkt_ptr = get_one_pkt(fpcap)
        if pkt_ptr == None:
            break
        while a2s(pkt_ptr[12:14]) == "8100":
            pkt_ptr = pkt_ptr[0:12] + pkt_ptr[16:]
        log_title_write(pkt_ptr)
        if cnt == 1:
            print("The 1st packet:")
        elif cnt == 2:
            print("The 2nd packet:")
        else:
            print("The %dth packet:" % cnt)
        dsmac = mac_print(pkt_ptr)
        pkt_len = int(a2s(pkt_ptr[12:14]), 16)
        print("Packet length: %d" % pkt_len)
        pkt_type_major = a2s(pkt_ptr[14:16])
        pkt_type_minor = a2s(pkt_ptr[16:18])
        if pkt_type_major + pkt_type_minor == "444802fd":
            pkt_type = "tdm_pcm"
            print("Packet type: %s" % pkt_type)
            pkt_ana_result = ana_tdm_pcm(pkt_ptr)
            flog.write(str(cnt)+","+dsmac+","+str(pkt_len)+","+pkt_type+","+pkt_ana_result+"\n")
        elif pkt_type_major + pkt_type_minor == "1e0701fe":
            pkt_type = "tdm_ss7"
            print("Packet type: %s" % pkt_type)
            pkt_ana_result = ana_tdm_ss7(pkt_ptr)
            flog.write(str(cnt)+","+dsmac+","+str(pkt_len)+","+pkt_type+","+pkt_ana_result+"\n")
        elif pkt_type_major + pkt_type_minor == "444811ee":
            pkt_type = "atm_aal2"
            print("Packet type: %s" % pkt_type)
            pkt_ana_result = ana_atm_aal2(pkt_ptr)
            flog.write(str(cnt)+","+dsmac+","+str(pkt_len)+","+pkt_type+","+pkt_ana_result+"\n")
        elif pkt_type_major + pkt_type_minor == "1e0712ed":
            pkt_type = "atm_aal5"
            print("Packet type: %s" % pkt_type)
            pkt_ana_result = ana_atm_aal5(pkt_ptr)
            flog.write(str(cnt)+","+dsmac+","+str(pkt_len)+","+pkt_type+","+pkt_ana_result+"\n")
        else:
            print("Error 1: Unknown packet type!")
        cnt += 1
        print("")
    fpcap.close()
    flog.close()

