from typing import Optional
import requests
import os
from dotenv import load_dotenv
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Load environment variables from .env file
load_dotenv()
JWT = os.getenv('PINATA_JWT')

def download_image(image_url: str) -> Optional[np.ndarray]:
    """
    Download an image from a given URL, convert it to a NumPy array using OpenCV, and return the image.

    Args:
    - image_url (str): The URL of the image to be downloaded.

    Returns:
    - Optional[np.ndarray]: The NumPy array representing the downloaded image, or None if an error occurs.
    """
    try:
        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()  # Raise an HTTPError for bad responses

        # Convert to a NumPy array and then to a CV2 image
        image_data = np.frombuffer(image_response.content, np.uint8)
        background_image = cv2.imdecode(image_data, cv2.IMREAD_UNCHANGED)

        print("Image downloaded successfully")
        return background_image

    except requests.exceptions.RequestException as req_error:
        print(f"Error during image download: {req_error}")
        return None

    except cv2.error as cv2_error:
        print(f"Error decoding image with OpenCV: {cv2_error}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None



def customize_certificate(
        username: str, 
        title: str, 
        issued_date: str,
        week_number: int,
        image_url: str="https://res.cloudinary.com/dv9se1fwu/image/upload/v1705084396/ykinhidb5xum6lsl6l5z.png", 
        academy_logo_path: str="../images/10x_logo.png") -> np.ndarray:
    """
    Customize a certificate by adding text and logos to a background image.

    Args:
    - username (str): The full name of the individual receiving the certificate.
    - title (str): The name of the completed course or challenge.
    - issued_date (str): The date when the certificate is issued.
    - academy_logo_path (str): The file path to the academy's logo image.
    - image_url (string): the url of background image

    Returns:
    - np.ndarray: The customized certificate as a NumPy array.

    Note:
    - This function saves the customized certificate image to a file named '{username}_certificate.png'.
    """

    try:
        print("Customizing certificate started.")

        # downloa background image
        background_image = download_image(image_url)
        assert background_image is not None, 'Error loading the background image'

        # Load the academy logo from a local file
        logo_image = cv2.imread(academy_logo_path, cv2.IMREAD_UNCHANGED)
        assert logo_image is not None, 'Error loading the academy logo'

        # Resize logo
        scale_percent = 10  # percent of original size
        logo_width = int(logo_image.shape[1] * scale_percent / 100)
        logo_height = int(logo_image.shape[0] * scale_percent / 100)
        dim = (logo_width, logo_height)
        logo_image = cv2.resize(logo_image, dim, interpolation=cv2.INTER_AREA)

        # Convert the background to a PIL Image
        background_pil = Image.fromarray(cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(background_pil)

        # Define font size and color
        font_large = ImageFont.load_default(size=24)  # Adjust as needed
        font_medium = ImageFont.load_default(size=24)  # Adjust as needed
        font_color = (59, 31, 24)

        # Add text to the certificate
        draw.text((264, 430), 'This certifies that', font=font_medium, fill=font_color)
        draw.text((460, 430), username, font=font_large, fill=font_color)
        draw.text((264, 485), 'Has successfully completed the', font=font_medium, fill=font_color)
        draw.text((264, 540), title, font=font_large, fill=font_color)
        draw.text((320, 595), 'Date of Issue:', font=font_medium, fill=font_color)
        draw.text((470, 595), issued_date, font=font_medium, fill=font_color)

        # Paste the academy logo onto the certificate
        logo_image_pil = Image.fromarray(logo_image)
        logo_image_pil = logo_image_pil.convert("RGBA")
        background_pil.paste(logo_image_pil, (50, 50), logo_image_pil)


        # Convert back to CV2 image to save or display
        final_certificate = cv2.cvtColor(np.array(background_pil), cv2.COLOR_RGB2BGR)

        output_path = f'../images/certificates/{username}_week_{week_number}_certificate.png'
        cv2.imwrite(output_path, final_certificate)
        print(f"Customized certificate saved to {output_path}")

        return upload_certificate_to_pinata(username, week_number, output_path)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return np.zeros((1, 1, 3), dtype=np.uint8)  # Return a blank image or handle the error as needed
    
    
def upload_certificate_to_pinata(username, week_number, output_path):
    try:
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        # filename = f"../images/certificates/{username}_week_{week_number}_certificate.png"
        headers = {
            "pinataMetadata": f"{username}_week_{week_number}_certificate",
            "Authorization": "Bearer " + JWT
        }

        with open(output_path, 'rb') as f:
            response = requests.post(url, files={"file": f}, headers=headers)

        if response.status_code == 200:
            print(f"Successfully uploaded {username}'s week {week_number} challenge certificate.")
            return response.json()["IpfsHash"]
        else:
            print(f"Failed to upload {username}'s certificate. Response: {response.text}")
            return None
    except Exception as e:
        print(f"upload certificate to pinata failed: {e}")
        return None


def get_image_url(ipfs_hash):
    try:
        return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    except Exception as e:
        print(f"Get image from url failed: {e}")
        return None