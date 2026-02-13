import argparse
import requests
import sys

# Replace with your actual Bot Token
BOT_TOKEN = "TOKEN"

BASE_URL = f"https://botapi.rubika.ir/v3/{BOT_TOKEN}"

def get_download_link(file_id):
    """Fetches the clean GET download URL from Rubika Bot API."""
    url = f"{BASE_URL}/getFile"
    try:
        res = requests.post(url, json={"file_id": file_id}, timeout=15)
        data = res.json()
        if data.get("status") == "OK":
            return data.get("data", {}).get("download_url")
        else:
            print(f"⚠️ API Error for {file_id}: {data.get('status_det')}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description="Rubika Manifest to Aria2 Link Generator")
    parser.add_argument("-i", "--input", help="Path to manifest file (e.g., manifest_123.txt)")
    parser.add_argument("-o", "--output", default="captured_link.txt", help="Output file for aria2 links")
    args = parser.parse_args()

    # Determine input source
    manifest_source = args.input if args.input else "manifest.txt"
    
    try:
        with open(manifest_source, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Manifest file '{manifest_source}' not found.")
        sys.exit(1)

    aria2_content = []
    print(f"📡 Processing {len(lines)} parts from {manifest_source}...")

    for line in lines:
        if "|" not in line:
            continue
            
        filename, file_id = line.strip().split("|")
        print(f"🔗 Fetching link for: {filename}...", end="\r")
        
        download_url = get_download_link(file_id)
        
        if download_url:
            # Format for aria2c input file:
            # URL
            #   out=filename
            aria2_content.append(f"{download_url}\n  out={filename}\n")
        else:
            print(f"\n❌ Failed to fetch link for {filename}")

    with open(args.output, "w") as f:
        f.writelines(aria2_content)

    print(f"\n✅ Done! Saved {len(aria2_content)} links to {args.output}")
    print(f"👉 Run: aria2c -i {args.output} -j 5")

if __name__ == "__main__":
    main()
