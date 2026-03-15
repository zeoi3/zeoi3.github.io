import json
import urllib.request
import re
import os

repos = {
    "inputLock": "zeoi3/inputLock-Releases",
    "onedockAI": "zeoi3/onedockAI-releases",
    "PixLog": "zeoi3/PixLog-Releases"
}

def get_latest_asset(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {'User-Agent': 'Mozilla/5.0'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for asset in data.get('assets', []):
                name = asset.get('name', '')
                if name.endswith('.zip') or name.endswith('.dmg'):
                    return asset.get('browser_download_url')
    except Exception as e:
        print(f"Error fetching {repo}: {e}")
    return None

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    for key, repo in repos.items():
        url = get_latest_asset(repo)
        if url:
            print(f"Found latest URL for {key}: {url}")
            pattern = rf'(id="link-{key}"\s+href=")[^"]+(")'
            html = re.sub(pattern, rf'\g<1>{url}\g<2>', html)
        else:
            print(f"Could not find .zip/.dmg for {key}")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html updated successfully.")

if __name__ == "__main__":
    main()
