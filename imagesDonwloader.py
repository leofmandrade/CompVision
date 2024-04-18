import requests
import os

def download_images(url_prefix, start_range, end_range, save_dir):
    # Create the save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Iterate over the range of numbers
    for i in range(start_range, end_range + 1):
        url = f"{url_prefix}/{i}.png"
        save_path = os.path.join(save_dir, f"{i}.png")
        
        # Download the image
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Save the image to the specified directory
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Image {i}.png downloaded successfully")
        else:
            print(f"Failed to download image {i}.png")

# Example usage
url_prefix = "https://raw.communitydragon.org/t/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons"
start_range = 151
end_range = 1000 # Adjust this range as needed
save_directory = "Champion Icons"  # Save images into "Champion Icons" directory

download_images(url_prefix, start_range, end_range, save_directory)
