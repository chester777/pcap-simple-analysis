from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class HandledMsg(Base):
    __tablename__ = 'handled_massage_list'

    timestamp = Column(Integer)
    update_id = Column(String, primary_key=True)

    def __init__(self, timestamp, update_id):
        self.timestamp = timestamp
        self.update_id = update_id

    def __repr__(self):
        return f"<HandledMsg('{self.timestamp}','{self.update_id}')>"


class PacketData(Base):
    __tablename__ = 'packet_data'

    pcap_id = Column(String, primary_key=True)
    packet_num = Column(Integer)
    src_ip = Column(String)
    dst_ip = Column(String)
    highest_protocol = Column(String)
    layers = Column(String)
    packet_length = Column(Integer)

    def __init__(self, pcap_id, packet_num, src_ip, dst_ip, highest_protocol, layers, packet_length):
        self.pcap_id = pcap_id
        self.packet_num = packet_num
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.highest_protocol = highest_protocol
        self.layers = layers
        self.packet_length = packet_length

    def __repr__(self):
        _result = (f"<PacketData('{self.pcap_id}','{self.packet_num}','{self.src_ip}','{self.dst_ip}),"
                   f"'{self.highest_protocol}', '{self.layers}', '{self.packet_length}'>'")
        return _result
