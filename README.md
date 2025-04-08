# Mod-config-web-spider
Creates json config mod list out of a basic name/url mod list for arma reforger config.json mod list.

## Example:
From:
`https://reforger.armaplatform.com/workshop/595F2BF2F44836FB-RHS-StatusQuo`
or just the name -> `RHS Status Quo`
To:
`{
    "modId": "595F2BF2F44836FB",
    "name": "RHS - Status Quo",
    "version": "0.11.4250"
}`

## Usage:
1. Change file_path in the script to your mod list text file.
2. `pip install requests beautifulsoup4`
3. Run script `python mod_config_spider.py`

<br>
The mod list file can contain either exact mod names (as shown on the workshop) or direct URLs to mod pages.<br>
Numbering is optional.<br><br>

When you run the script, it’ll ask what type of list entries you're using.<br>
At the end, you'll be asked if you want to open the mod pages in your browser to double-check them.
