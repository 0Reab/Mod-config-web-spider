import json
import requests
from bs4 import BeautifulSoup
from time import sleep


file_path = r'C:\Users\StillAStojke\Desktop\modlist.json'
url = r'https://reforger.armaplatform.com/workshop/'


def read_cfg(config):
    result = []

    with open(file_path, 'r') as f:
        mods_lst = json.load(f)
        print(f'Reading file -> {file_path}')
        print(f'Processing: {len(mods_lst)} mods...')

        for mod in mods_lst:
            del mod['version']
            result.append(mod)

    return result


def api_request(modID, name):
    api = url + modID

    r = requests.get(api)
    print(f'http request -> {api}')


    if r.status_code != 200:
        print(f'Workshop unreachable - http status {r.status_code}')

    soup = BeautifulSoup(r.content, 'html.parser')
    entries = soup.find_all("dt", class_="py-3.5 font-bold leading-none")

    for idx, item in enumerate(entries):
        if item.next.strip() == 'Version size':
            size = soup.find_all("dd", class_="flex items-center gap-1")[idx].text.strip()
            print(f'Found version number -> {name} -> {size}')
            break

    return {name : size}


def convert_to_gb(size):
    value, unit = size.strip().split()
    value = float(value)
    unit = unit.lower()

    unit_to_bytes = {
        'kb': 1024,
        'mb': 1024 ** 2,
        'gb': 1024 ** 3,
    }

    if unit not in unit_to_bytes:
        raise ValueError(f"Unsupported unit: {unit}")

    # Convert to bytes first
    bytes_val = value * unit_to_bytes[unit]

    # Convert bytes to GB
    gb_val = bytes_val / unit_to_bytes['gb']
    return gb_val


def main():
    mod_list = read_cfg(file_path)
    result = []
    total_size = 0

    for mod in mod_list:
        name = mod['name']
        mod_id = mod['modId']

        result.append(api_request(mod_id, name))
        sleep(0.15)
        #print(f'name = {name} modId = {mod_id}')

    print('\n')

    for dicc in result:
        for n, s in dicc.items():
            print(f'{n} {s}')
            total_size += convert_to_gb(s)

    print('\n')
    print(f'Total mod list size {round(total_size,2)} GB')


if __name__ == '__main__':
    main()