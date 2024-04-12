import subprocess
import socket


import pandas as pd


list_of_host_names = [
    'google.com',
    'vk.com',
    'youtube.com',
    'translate.yandex.ru',
    'fresh.nsuts.ru',
    'github.com', 
    'nsu.ru',
    "huawei.com",
    "nstu.ru",
    "mi.com",
    "apple.com"
    ]

timing_result = list()
ttl_result = list()
ip_address = list()
name_domin = list()

for ip in list_of_host_names:
    ip_ = (socket.gethostbyname(ip))
    ip_address.append(ip_)
    result = subprocess.run(
        ['ping', '-c', '1', ip],
        text=True,
        capture_output=True,
        check=True)
    name_domin.append(ip)

    for line in result.stdout.splitlines():
        if "icmp_seq" in line:
            timing = line.split('time=')[-1].split(' ms')[0]
            ttl = line.split('ttl=')[-1].split()[0]
            timing_result.append(timing)
            ttl_result.append(ttl)


df = pd.DataFrame({
    "Name Domain": name_domin,
    "IP ADDRESS": ip_address,
    "Timing": timing_result,
    "TTL": ttl_result
})

df.to_csv("output.csv", index=False, sep=';')
