#!/usr/bin/env python

import click
import socket
from datetime import datetime

@click.command()
@click.argument('destination', type=str)
def traceroute(destination):
    MAX_HOPS = 64
    PACKET_SIZE = 52
    dest_ip = socket.gethostbyname(destination)
    click.echo(f"traceroute to {destination} ({dest_ip}), {MAX_HOPS} hops max, {PACKET_SIZE} byte packets")
    with (
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as send_socket, 
            socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as recv_socket
        ):
        send_socket.settimeout(1)
        recv_socket.settimeout(1)
        for ttl in range(1, MAX_HOPS + 1):
            send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            start = datetime.now()
            send_socket.sendto(b'', (dest_ip, 33434 + ttl - 1))
            try:
                data, addr = recv_socket.recvfrom(1024)
                end = datetime.now()
                latency = round((end - start).total_seconds() * 1000, 3)
                try:
                    host = socket.gethostbyaddr(addr[0])[0]
                except:
                    host = addr[0]
                click.echo(f"{ttl} {host} ({addr[0]}) {latency} ms")
            except socket.timeout as ste:
                click.echo(f"{ttl} *")
            except socket.error as se:
                click.echo(f"{ttl} *")
            else:
                if addr[0] == dest_ip:
                    break

if __name__ == '__main__':
    traceroute()