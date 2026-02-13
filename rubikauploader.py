import os
import subprocess
import time
import shutil
import glob
import argparse
import requests

# --- CONFIGURATION ---
BOT_TOKEN = "TOKEN"
CHAT_ID = "b_chatID"
FOLDER_PATH = "./" # Path where your files are
DEFAULT_PASSWORD = "your_password"

BASE_URL = f"https://botapi.rubika.ir/v3/{BOT_TOKEN}"

def bot_request(method, data):
    url = f"{BASE_URL}/{method}"
    try:
        res = requests.post(url, json=data, timeout=20)
        return res.json()
    except Exception as e:
        print(f"❌ API Request Error ({method}): {e}")
        return {}

def rubika_3step_upload(file_path):
    res_url = bot_request("requestSendFile", {"type": "File"})
    upload_url = res_url.get("data", {}).get("upload_url")
    if not upload_url: 
        return None

    try:
        with open(file_path, "rb") as f:
            # Rubika's server expects the file bits here
            upload_res = requests.post(upload_url, files={'file': f}, timeout=600)
            return upload_res.json().get("data", {}).get("file_id")
    except Exception as e:
        print(f"❌ Upload Error: {e}")
        return None

def compress_and_upload(file_list, status_msg_id, active_password):
    existing_sessions = sorted(glob.glob(os.path.join(FOLDER_PATH, "temp_*")), reverse=True)
    
    if existing_sessions:
        output_dir = existing_sessions[0]
        time_id = os.path.basename(output_dir).replace("temp_", "")
        print(f"🔄 Resuming session: {time_id}")
    else:
        time_id = str(int(time.time_ns()))
        output_dir = os.path.join(FOLDER_PATH, "temp_" + time_id)
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"📦 Compressing...")
        # -v20m creates exactly 20,971,520 byte chunks
        command = ["7z", "a", "-mx=0", "-mhe=on", f"-p{active_password}", "-v20m", f"{output_dir}/{time_id}.7z"] + file_list
        subprocess.run(command)

    # 1. PATH FOR MANIFEST
    manifest_path = os.path.join(output_dir, f"manifest_{time_id}.txt")
    last_sent_file_path = os.path.join(output_dir, "last_sent_file.txt")
    last_sent_file_index = 0

    if os.path.exists(last_sent_file_path):
        with open(last_sent_file_path, "r") as f:
            last_sent_file = f.read().strip()
            try:
                last_sent_file_index = int(last_sent_file.split('.')[-1])
            except:
                last_sent_file_index = 0

    files_to_send = sorted(f for f in os.listdir(output_dir) if f.startswith(time_id) and ".7z" in f)

    for file_to_send in files_to_send[last_sent_file_index:]:
        print(f"Uploading: {file_to_send}")
        file_full_path = os.path.join(output_dir, file_to_send)
        
        file_id = rubika_3step_upload(file_full_path)
        
        if file_id:
            send_res = bot_request("sendFile", {
                "chat_id": CHAT_ID,
                "file_id": file_id,
                "caption": f"Part: {file_to_send}"
            })
            
            if send_res.get("status") == "OK":
                # 2. LOG TO MANIFEST: "filename|file_id"
                with open(manifest_path, "a") as f:
                    f.writelines(f"{file_to_send}|{file_id}\n")
                
                with open(last_sent_file_path, "w") as f:
                    f.write(file_to_send)
                print(f"✅ Success & Logged: {file_to_send}")
            else:
                print(f"❌ Send Error: {send_res}")
                return
        else:
            print(f"❌ Failed to get file_id for {file_to_send}")
            return

    # 3. UPLOAD THE MANIFEST ITSELF AT THE END
    print("📜 Uploading manifest...")
    manifest_id = rubika_3step_upload(manifest_path)
    if manifest_id:
        bot_request("sendFile", {
            "chat_id": CHAT_ID, 
            "file_id": manifest_id, 
            "caption": f"DOWNLOAD_MANIFEST_{time_id}"
        })

    # Keep output_dir if you want to double-check manifest, 
    # otherwise uncomment cleanup:
    # shutil.rmtree(output_dir)
    bot_request("sendMessage", {"chat_id": CHAT_ID, "text": "✅ All parts sent. Manifest uploaded!"})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+')
    parser.add_argument("-p", "--password", default=DEFAULT_PASSWORD)
    args = parser.parse_args()

    matched = []
    for pattern in args.files:
        matched.extend(glob.glob(os.path.join(FOLDER_PATH, pattern)))

    if matched:
        res = bot_request("sendMessage", {"chat_id": CHAT_ID, "text": "🚀 Initiating..."})
        # Extract message_id from Rubika's data structure
        msg_id = res.get("data", {}).get("message_id")
        if msg_id:
            compress_and_upload(matched, msg_id, args.password)
        else:
            print(f"❌ Initial message failed: {res}")
    else:
        print("❌ No files found.")
