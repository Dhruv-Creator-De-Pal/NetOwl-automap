


import asyncio





PORT_SERVICES = {
    # Lower Ports (System & Infrastructure)
    7: "Echo (ICMP-like testing / Character loopback)",
    19: "Chargen (Character Generator - Legacy testing)",
    20: "FTP-Data (File Transfer Protocol - Active Mode Data)",
    21: "FTP-Control (File Transfer Protocol - Command Channel)",
    22: "SSH (Secure Shell / SFTP / SCP - Encrypted Remote Access)",
    23: "Telnet (Unencrypted Remote Login - Plaintext Risk)",
    25: "SMTP (Simple Mail Transfer Protocol - MTA Mail Routing)",
    43: "WHOIS (Domain and IP Registry Lookups)",
    53: "DNS (Domain Name System - UDP Queries / TCP Zone Transfers)",
    67: "DHCP-Server (Bootstrap Protocol Server / IP Allocation)",
    68: "DHCP-Client (Bootstrap Protocol Client)",
    69: "TFTP (Trivial File Transfer Protocol - No Auth / UDP)",
    80: "HTTP (Hypertext Transfer Protocol - Unencrypted Web)",
    88: "Kerberos (Network Authentication / Windows AD Tickets)",
    110: "POP3 (Post Office Protocol v3 - Legacy Email Retrieval)",
    111: "RPCBind (ONC RPC Portmapper - Linux/Unix Shared Services)",
    123: "NTP (Network Time Protocol - Time Synchronization)",
    135: "MS-RPC (Microsoft Remote Procedure Call Endpoint Mapper)",
    137: "NetBIOS-NS (NetBIOS Name Service - Windows Name Resolution)",
    138: "NetBIOS-DGM (NetBIOS Datagram Service)",
    139: "NetBIOS-SSN (NetBIOS Session Service - Legacy File Sharing)",
    143: "IMAP (Internet Message Access Protocol - Modern Email Sync)",
    161: "SNMP (Simple Network Management Protocol - Agent Polling)",
    162: "SNMP-Trap (SNMP Alert Receiver)",
    179: "BGP (Border Gateway Protocol - Internet Routing)",
    389: "LDAP (Lightweight Directory Access Protocol - Auth/Lookup)",
    
    # Secure & Middle Range (Standard Services)
    443: "HTTPS (Hypertext Transfer Protocol Secure - TLS/SSL)",
    445: "SMB (Server Message Block - Windows File/Print Sharing)",
    465: "SMTPS (SMTP over SSL - Secure Mail Routing)",
    500: "ISAKMP/IKE (IPsec Key Exchange for VPN Tunnels)",
    514: "Syslog (System Logging Protocol - Message Receiver)",
    515: "LPD (Line Printer Daemon - Network Print Services)",
    548: "AFP (Apple Filing Protocol - Legacy macOS File Sharing)",
    587: "SMTP-Submission (Modern Client Email Sending with Auth)",
    631: "CUPS (Common Unix Printing System)",
    636: "LDAPS (LDAP over SSL - Encrypted Directory Access)",
    873: "Rsync (File Synchronization Protocol)",
    993: "IMAPS (IMAP over SSL/TLS - Secure Email Sync)",
    995: "POP3S (POP3 over SSL/TLS - Secure Email Retrieval)",
    1080: "SOCKS (Socket Secure Proxy - Firewall Bypass)",
    1194: "OpenVPN (OpenVPN Protocol Default)",
    1433: "MSSQL (Microsoft SQL Server Main Instance)",
    1434: "MSSQL-Monitor (SQL Server Browser / Instance Discovery)",
    1521: "Oracle-DB (Oracle Database Listener)",
    1723: "PPTP (Point-to-Point Tunneling Protocol - Legacy VPN)",
    1883: "MQTT (Message Queuing Telemetry Transport - IoT)",
    1900: "SSDP (Simple Service Discovery Protocol - UPnP)",
    2049: "NFS (Network File System - Linux Drive Mounting)",
    2375: "Docker-API (Docker Remote API - Unencrypted/Insecure)",
    2376: "Docker-TLS (Docker Remote API - Encrypted/Secure)",
    
    # High Ports (Databases, DevOps, & Web-Alt)
    3000: "Gitea/Grafana/React (Common Development Default)",
    3306: "MySQL (MySQL / MariaDB Database Access)",
    3389: "RDP (Remote Desktop Protocol - Windows GUI Access)",
    4500: "IPsec-NAT-T (IPsec NAT Traversal - VPN Data Traffic)",
    5000: "Flask / Docker Registry / UPnP Discovery",
    5353: "mDNS (Multicast DNS - Bonjour/Avahi Local Discovery)",
    5432: "PostgreSQL (PostgreSQL Database Access)",
    5672: "RabbitMQ (AMQP Messaging Broker)",
    5900: "VNC (Virtual Network Computing - Remote Desktop)",
    5985: "WinRM-HTTP (Windows Remote Management - Command Line)",
    5986: "WinRM-HTTPS (Windows Remote Management - Secure)",
    6379: "Redis (In-Memory Key-Value Store/Cache)",
    8000: "HTTP-Alt (Django/Flask Dev / Web Proxies)",
    8080: "HTTP-Proxy (Apache Tomcat / Alternative Web Server)",
    8443: "HTTPS-Alt (Plesk/vCenter / Alternative Secure Web)",
    8888: "Jupyter / Web Development (Common Sandbox Port)",
    9000: "PHP-FPM / Portainer (FastCGI / Container Management)",
    9100: "Prometheus Exporter (Monitoring Metrics)",
    9200: "Elasticsearch-API (REST Interface for Search)",
    9300: "Elasticsearch-Node (Internal Cluster Communication)",
    11211: "Memcached (High-Speed Object Caching)",
    27017: "MongoDB (NoSQL Database Primary Port)",
    27018: "MongoDB-Shard (Mongo Sharding Instance)",
}

PORT_RISKS = {
    # --- Low risk ---
    7: "low",
    9: "low",
    13: "low",
    37: "low",
    43: "low",
    67: "low",
    68: "low",
    80: "low",
    123: "low",
    443: "low",
    465: "low",
    500: "low",
    587: "low",
    636: "low",
    993: "low",
    995: "low",
    1194: "low",
    2376: "low",
    4500: "low",
    5353: "low",
    5986: "low",
    8443: "low",

    # --- Medium risk ---
    1: "medium",
    5: "medium",
    11: "medium",
    17: "medium",
    18: "medium",
    19: "medium",
    20: "medium",
    21: "medium",
    22: "medium",
    25: "medium",
    42: "medium",
    49: "medium",
    53: "medium",
    70: "medium",
    88: "medium",
    102: "medium",
    110: "medium",
    111: "medium",
    113: "medium",
    115: "medium",
    119: "medium",
    135: "medium",
    137: "medium",
    138: "medium",
    139: "medium",
    143: "medium",
    161: "medium",
    162: "medium",
    179: "medium",
    194: "medium",
    389: "medium",
    427: "medium",
    444: "medium",
    464: "medium",
    502: "medium",
    514: "medium",
    515: "medium",
    520: "medium",
    548: "medium",
    554: "medium",
    593: "medium",
    631: "medium",
    873: "medium",
    989: "medium",
    990: "medium",
    1080: "medium",
    1434: "medium",
    1701: "medium",
    1723: "medium",
    1883: "medium",
    1900: "medium",
    2049: "medium",
    3000: "medium",
    3260: "medium",
    3690: "medium",
    4000: "medium",
    4840: "medium",
    5000: "medium",
    5060: "medium",
    5061: "medium",
    5601: "medium",
    5672: "medium",
    5984: "medium",
    5985: "medium",
    6667: "medium",
    7000: "medium",
    8000: "medium",
    8008: "medium",
    8080: "medium",
    8081: "medium",
    8140: "medium",
    8888: "medium",
    9000: "medium",
    9090: "medium",
    9092: "medium",
    9100: "medium",
    9300: "medium",
    27018: "medium",
    27019: "medium",
    49152: "medium",

    # --- High risk ---
    23: "high",
    69: "high",
    79: "high",
    445: "high",
    512: "high",
    513: "high",
    543: "high",
    544: "high",
    902: "high",
    992: "high",
    1214: "high",
    1433: "high",
    1521: "high",
    2082: "high",
    2083: "high",
    2086: "high",
    2087: "high",
    2181: "high",
    2375: "high",
    3306: "high",
    3389: "high",
    4444: "high",
    5432: "high",
    5555: "high",
    5900: "high",
    6000: "high",
    6379: "high",
    6443: "high",
    9200: "high",
    10000: "high",
    11211: "high",
    27017: "high",
}


quick_ports =[20, 21, 22, 23, 25, 53, 67, 68, 69, 80,
    110, 111, 123, 135, 137, 138, 139, 143,
    161, 162, 443, 445, 465, 500, 514, 587,
    993, 995, 1433, 1521, 1900, 2049, 2375,
    2376, 3306, 3389, 4500, 5353, 5432, 5900,
    5985, 5986, 6379, 8080, 8443, 9200, 9300,
    11211, 27017]

smart_ports = [# Remote access / admin
    22, 23, 3389, 5900, 5985, 5986,
    80, 443, 8080, 8443,
    21, 111, 139, 445, 2049,
    1433, 1521, 3306, 5432, 6379, 9200, 9300, 11211, 27017,
    2375, 2376,
    53, 161, 162, 5353]

full_ports = list(range(1, 65536))

# above was the list of the pots and there risk tags expected with the help of linked lists 






# Here we are gettting the ports mode on weather to select the linked list of smart or the quickk or the full port scan 

def get_ports_mode(mode: str):
    """Return ports for the selected scan mode."""

    if mode == "quick":
        return quick_ports

    if mode == "smart":
        return smart_ports

    if mode == "full":
        return full_ports

    raise ValueError("Invalid mode. Please choose 'quick', 'smart', or 'full'.")




# here the number of port is being shown to the user with the help of the get_port_count_for_mode function and also a preview of the ports is being shown to the user with the help of get_port_preview_for_mode function which is showing only 12 ports as a preview to the user
def get_port_count_for_mode(mode: str) -> int:
    """Return number of ports selected for the scan mode."""

    ports = get_ports_mode(mode)
    return len(ports)




#here the number of port is being shown to the user with the help of the get_port_count_for_mode function and also a preview of the ports is being shown to the user with the help of get_port_preview_for_mode function which is showing only 12 ports as a preview to the user

def get_port_preview_for_mode(mode: str, limit: int = 12) -> list[int]:
    """Return a small preview of selected ports."""

    ports = get_ports_mode(mode)
    return list(ports[:limit])

#where the service si not in the scope of the sccanner returs the unkon for now we ll be adding the ai bassed probable info genrater latter to acccuratly inform the user about the innfo of the nnetwork 
def get_service_name(port: int) -> str:
    """Return a friendly service name for a port."""

    return PORT_SERVICES.get(port, "Unknown")


def get_port_risk(port: int) -> str:
    """Return a simple risk label for a port."""

    return PORT_RISKS.get(port, "unknown")


def build_port_results(open_ports: list[int]) -> list[dict]:
    """Build structured open-port results for CLI output and reports."""

    results = []

    for port in open_ports:
        results.append(
            {
                "port": port,
                "protocol": "tcp",
                "service": get_service_name(port),
                "risk": get_port_risk(port),
            }
        )

    return results


async def check_tcp_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Check if a TCP port is open on a single host."""

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout,
        )

        writer.close()
        await writer.wait_closed()

        return True

    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False


async def scan_ports_for_host(
    host: str,
    ports,
    timeout: float = 1.0,
    concurrency: int = 100,
) -> list[int]:
    """Scan multiple ports for a single host and return open ports."""

    semaphore = asyncio.Semaphore(concurrency)

    async def check_with_limit(port: int):
        async with semaphore:
            is_open = await check_tcp_port(host, port, timeout)
            return port if is_open else None

    results = await asyncio.gather(
        *(check_with_limit(port) for port in ports)
    )

    return [port for port in results if port is not None]