from datetime import datetime
import discord
import requests
from discord import Embed

from config import NEZHA_TOKEN
from functions.misc import percentage_bar


class ServerStatus:
    def __init__(self, server_id):
        data = get_server_status(server_id)['result'][0]
        self.id = data['id']
        self.name = data['name']
        self.tag = data['tag']
        self.last_active = data['last_active']
        self.ipv4 = data['ipv4']
        self.ipv6 = data['ipv6']
        self.valid_ip = data['valid_ip']

        host_info = data['host']
        self.host_platform = host_info['Platform']
        self.host_platform_version = host_info['PlatformVersion']
        self.host_cpu = host_info['CPU'][0]
        self.host_mem_total = host_info['MemTotal']
        self.host_disk_total = host_info['DiskTotal']
        self.host_swap_total = host_info['SwapTotal']
        self.host_arch = host_info['Arch']
        self.host_virtualization = host_info['Virtualization']
        self.host_boot_time = host_info['BootTime']
        self.host_country_code = host_info['CountryCode']
        self.host_version = host_info['Version']

        status_info = data['status']
        self.status_cpu = status_info['CPU']
        self.status_mem_used = status_info['MemUsed']
        self.status_swap_used = status_info['SwapUsed']
        self.status_disk_used = status_info['DiskUsed']
        self.status_net_in_transfer = status_info['NetInTransfer']
        self.status_net_out_transfer = status_info['NetOutTransfer']
        self.status_net_in_speed = status_info['NetInSpeed']
        self.status_net_out_speed = status_info['NetOutSpeed']
        self.status_uptime = status_info['Uptime']
        self.status_load1 = status_info['Load1']
        self.status_load5 = status_info['Load5']
        self.status_load15 = status_info['Load15']
        self.status_tcp_conn_count = status_info['TcpConnCount']
        self.status_udp_conn_count = status_info['UdpConnCount']
        self.status_process_count = status_info['ProcessCount']

    def __str__(self):
        return f"ServerStatus - Name: {self.name}, IPv4: {self.ipv4}, NetInSpeed: {self.status_net_in_speed}"

    def embed(self) -> Embed:
        embed = Embed(title=f'{self.name} Status', timestamp=datetime.now())
        cpu_bar = percentage_bar(self.status_cpu)
        mem_percentage = self.status_mem_used / self.host_mem_total
        memory_bar = percentage_bar(mem_percentage)
        disk_bar = percentage_bar(self.status_disk_used / self.host_disk_total)
        embed.description = f"""
        {self.host_country_code} | {self.host_platform} {self.host_platform_version}
        CPU:
        {cpu_bar}
        MEM:  {self.status_mem_used} / {self.host_mem_total}
        {memory_bar}
        DISK: {self.status_disk_used} / {self.host_disk_total} 
        {disk_bar}
        NETWORK:  IN: {self.status_net_in_speed}  OUT:{self.status_net_out_speed} 
        """
        if mem_percentage > 90:
            embed.colour = discord.Colour.red()
        elif mem_percentage > 60:
            embed.colour = discord.Colour.yellow()
        else:
            embed.colour = discord.Colour.green()
        return embed


def get_server_status(server_id) -> dict:
    # Define your API endpoint and token
    api_url = f'https://status.axekz.com/api/v1/server/details?id={server_id}&tag='
    api_token = NEZHA_TOKEN  # Replace with your actual token

    headers = {
        'Authorization': f'{api_token}'
    }

    try:
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            # Parse and process the response content
            data = response.json()
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {}


def get_server_list() -> dict:
    # Define your API endpoint and token
    api_url = 'https://status.axekz.com/api/v1/server/list?tag='
    api_token = NEZHA_TOKEN  # Replace with your actual token

    headers = {
        'Authorization': f'{api_token}'
    }

    try:
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            # Parse and process the response content
            data = response.json()
            return data
        else:
            print(f"Request failed with status code: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {}


def embeds_server_status():
    embeds = []
    servers = get_server_list()['result']
    for server in servers:
        status = ServerStatus(server['id'])
        embed_data = status.embed()
        embeds.append(embed_data)

    # Assuming you have a list of embeds called 'embeds'
    embed_dicts = [embed.to_dict() for embed in embeds]

    return embed_dicts


if __name__ == '__main__':
    print(embeds_server_status())
    pass
