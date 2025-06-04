import os
import requests

class FileOps:
    def upload_folder(self, folder_path, server_url):
        if not os.path.isdir(folder_path):
            print(f"{folder_path} is not a valid directory.")
            return

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    response = requests.post(server_url, files={"file": f})
                    if response.status_code == 200:
                        print(f"Uploaded {file_path} successfully.")
                    else:
                        print(f"Failed to upload {file_path}. Status code: {response.status_code}")
