import requests
import os

def download_file(url, filepath):
    response = requests.get(url)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded: {filepath}")

# Download FontAwesome fonts
download_file(
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.woff2",
    "admin/static/css/webfonts/fa-solid-900.woff2"
)

download_file(
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.ttf",
    "admin/static/css/webfonts/fa-solid-900.ttf"
)

print("FontAwesome fonts downloaded successfully!")