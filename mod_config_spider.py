import requests
import json
import webbrowser
from time import sleep
from bs4 import BeautifulSoup


'''
CHANGE -> file_path line: 20 -> to the path of your mod list txt.
It can consist of mod names on each line, and with numbering: 1. example mod

Two modules are required "requests" and "bs4", `pip install module_name`.
Script outputs config ready json modlist.

To validate json if needed https://jsonlint.com/
'''


# ---> CHANGE ME <---
file_path = r'C:\Users\Foo\example.txt'

def read_list(path, numbered):
    mods = []
    try:
        with open(path, 'r') as f:
            file = f.read()
            mod_list = file.split('\n')  # split on newline into a list
    except FileNotFoundError:
        print(f'Error file not found in path {file_path}')
        exit(1)

    for line in mod_list:
        if numbered:
            line = line.split(' ', 1)[1].strip()  # split off list numbering
        mods.append(line)

    return mods


def get_api(mod_name):
    base = 'https://reforger.armaplatform.com'
    url = f'{base}/workshop?search={mod_name}'
    print(f'url = {url}')

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Can't connect to {url}")
        exit(1)

    sleep(1)  # rate limit

    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find("a", class_="group flex flex-col")['href']

    link = base + result

    return link


def parse_api(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Can't connect to {url}")
        exit(1)

    sleep(1)  # rate limit
    soup = BeautifulSoup(response.content, "html.parser")

    result = {}

    mod_id = soup.find("span", class_="leading-none").text.strip()
    name = soup.find("h1").text.strip()

    entries = soup.find_all("dt", class_="py-3.5 font-bold leading-none")

    for idx, item in enumerate(entries):
        if item.text.strip() == 'Version':
            version = soup.find_all("dd", class_="flex items-center gap-1")[idx].text.strip()
            break

    result['modId'] = mod_id
    result['name'] = name
    result['version'] = version

    return result


def format_cfg(mods):
    return ',\n'.join(mods)


def save_output(config):
    try:
        with open('modlist.txt', 'x') as f:
            f.write(config)
    except FileExistsError:
        with open('modlist.txt', 'w') as f:
            f.write(config)


def browse(url):
    webbrowser.open(url)


def main():
    json_modlist = []
    url_list = []

    print(f'example: 1. "mod_name_or_mod_url"')
    b = input(f'Are text file entries prefixed with numbers? (y/n): ')
    if b == 'y':
        numbered = True
    else:
        numbered = False

    mod_list = read_list(file_path, numbered)

    a = input('Are text file entries links or mod names? (name/link): ')
    print('web scrapping in progress...')

    for mod in mod_list:
        if a == 'name':
            link = get_api(mod)
        else:
            link = mod

        url_list.append(link)
        mod_info = parse_api(link)

        json_obj = json.dumps(mod_info, indent=4)
        json_modlist.append(json_obj)

    config = format_cfg(json_modlist)
    save_output(config)

    print(config)
    print('\njson saved to modlist.txt')

    answer = input('\nDo you want to open all mod page links? (y/*): ').lower()

    if answer == 'y':
        for link in url_list:
            browse(link)
            sleep(1)


if __name__ == '__main__':
    main()