from openai import OpenAI
from dotenv import load_dotenv
import os
from logger import logger
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from typing import Optional


# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is available
if not api_key:
    raise ValueError("API key is not set. Make sure it is available in your .env file.")

def generate_image(prompt: str) -> str:
    """
    Generate an image using the OpenAI Images API based on the given prompt.

    Args:
    - prompt (str): The text prompt to generate the image.

    Returns:
    - str: The URL of the generated image.
    """
    try:
        client = OpenAI(api_key=api_key)

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            quality="hd",
            n=1,
        )

        image_url = response.data[0].url
        logger.info("Image generated successfully")

        return image_url
    except Exception as e:
        logger.error(f"Error while generating image: {e}")
        return ""



def generate_image_variation(image_src: str) -> str:
    """
    Generate variations of an input image using the OpenAI Images API.

    Args:
    - image_src (str): The path or URL of the input image.

    Returns:
    - str: The URL of the generated image variation.
    """
    try:
        client = OpenAI(api_key=api_key)
        response = client.images.create_variation(
            image=open(image_src, "rb"),
            model="dall-e-3",
            n=2,
            size="1024x1024"
        )

        image_url = response.data[0].url
        logger.info("Image variation generated successfully")
        return image_url
    except Exception as e:
        logger.error(f"Error while generating image variation: {e}")
        return ""
    

def chat_completion(prompt: str) -> str:
    """
    Generate a chat-based completion using the OpenAI Chat API.

    Args:
    - prompt (str): The user's prompt to continue the conversation.

    Returns:
    - str: The completed content based on the user's input.

    Example:
    ```python
    user_prompt = "Tell me a joke."
    completion = chat_completion(user_prompt)
    print(completion)
    ```

    In this example, the function generates a chat-based completion based on the user's prompt.
    """
    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        logger.info("Chat completion done.")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(e)
        return ""
    


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

        logger.info("Image downloaded successfully")
        return background_image

    except requests.exceptions.RequestException as req_error:
        logger.error(f"Error during image download: {req_error}")
        return None

    except cv2.error as cv2_error:
        logger.error(f"Error decoding image with OpenCV: {cv2_error}")
        return None

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None



def customize_certificate(full_name: str, course_name: str, date_of_issue: str, academy_logo_path: str, image_url: str) -> np.ndarray:
    """
    Customize a certificate by adding text and logos to a background image.

    Args:
    - full_name (str): The full name of the individual receiving the certificate.
    - course_name (str): The name of the completed course or challenge.
    - date_of_issue (str): The date when the certificate is issued.
    - academy_logo_path (str): The file path to the academy's logo image.
    - image_url (string): the url of background image

    Returns:
    - np.ndarray: The customized certificate as a NumPy array.

    Note:
    - This function saves the customized certificate image to a file named '{full_name}_certificate.png'.
    """

    try:
        logger.info("Customizing certificate started.")

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
        font_large = ImageFont.load_default()  # Adjust as needed
        font_medium = ImageFont.load_default()  # Adjust as needed
        font_color = (255, 255, 255)

        # Add text to the certificate
        draw.text((120, 100), 'Certificate of Completion', font=font_large, fill=font_color)
        draw.text((120, 200), 'This certifies that', font=font_medium, fill=font_color)
        draw.text((120, 300), full_name, font=font_large, fill=font_color)
        draw.text((120, 400), 'Has successfully completed the', font=font_medium, fill=font_color)
        draw.text((120, 500), course_name, font=font_large, fill=font_color)
        draw.text((120, 600), 'Date of Issue:', font=font_medium, fill=font_color)
        draw.text((320, 600), date_of_issue, font=font_medium, fill=font_color)

        # Paste the academy logo onto the certificate
        logo_image_pil = Image.fromarray(logo_image)
        logo_image_pil = logo_image_pil.convert("RGBA")
        background_pil.paste(logo_image_pil, (50, 50), logo_image_pil)

        # Add footer text
        footer_text = 'This certificate is hereby issued in recognition of the successful completion of the specified challenge. Congratulations!'
        draw.text((120, 700), footer_text, font=font_medium, fill=font_color)

        # Convert back to CV2 image to save or display
        final_certificate = cv2.cvtColor(np.array(background_pil), cv2.COLOR_RGB2BGR)

        output_path = f'../images/{full_name}_final_certificate.png'
        cv2.imwrite(output_path, final_certificate)
        logger.info(f"Customized certificate saved to {output_path}")

        return final_certificate

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return np.zeros((1, 1, 3), dtype=np.uint8)  # Return a blank image or handle the error as needed