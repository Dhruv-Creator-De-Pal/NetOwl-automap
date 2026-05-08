
def devices(target: str) -> list[dict[str, str]]:
    from scapy.all import ARP, Ether, srp

    arp_req = ARP(pdst=target)
    broadcast_etherframe = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast_etherframe / arp_req

    answered, unanswered = srp(packet, timeout=10, verbose=False)

    results=[]
    for sent , received in answered:
        results.append({"IP":received.psrc, "MAC" : received.hwsrc})
    return results
    
