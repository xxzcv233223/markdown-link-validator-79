import re
import sys
import requests

def validate_markdown_links(file_path):
    """Reads a markdown file and validates all HTTP/HTTPS links."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    # Regex to find standard Markdown links: [text](url)
    links = re.findall(r'\[.*?\]\((https?://[^\s)]+)\)', text)
    unique_links = set(links)

    print(f"Found {len(unique_links)} unique links. Validating...\n")

    for link in unique_links:
        try:
            # Using HEAD request to save bandwidth
            response = requests.head(link, timeout=5, allow_redirects=True)
            status = response.status_code
            symbol = "✓" if 200 <= status < 400 else "✗"
            print(f"[{symbol}] {status} - {link}")
        except requests.RequestException as e:
            print(f"[✗] ERROR - {link} ({str(e)})")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python link_validator.py <path_to_markdown_file>")
    else:
        validate_markdown_links(sys.argv[1])