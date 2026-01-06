import requests
import os

def download_file(url, filepath):
    response = requests.get(url)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded: {filepath}")

# Download Bootstrap CSS
download_file(
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
    "admin/static/css/vendor/bootstrap.min.css"
)

# Download FontAwesome CSS
download_file(
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    "admin/static/css/vendor/fontawesome.min.css"
)

print("Assets downloaded successfully!")