import os
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import platform
from time import sleep

os.environ['MOZ_HEADLESS'] = '1'

if platform.system() == "Windows":
    firefox_profile_path = os.path.expanduser(
        "~") + os.sep + 'AppData' + os.sep + 'Local' + os.sep + 'Mozilla' + os.sep + 'Firefox' + os.sep + 'Profiles' + os.sep + 'inmersprofile.default-release'
else:
    firefox_profile_path = os.path.expanduser(
        "~") + "/snap/firefox/common/.mozilla/firefox/inmersprofile.default-release"

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--profile')
firefox_options.add_argument(firefox_profile_path)

output_file_path = "output.txt"  # Specify the file path for output

try:
    driver = webdriver.Firefox(options=firefox_options)
except:
    print("ERROR")
    driver.quit()


def write_to_output_file(content):
    with open(output_file_path, "a") as file:
        file.write(content + "\n")


def get_blip_caption(image_path):
    try:
        # Navigate to the BLIP webpage
        driver.get("https://replicate.com/salesforce/blip")

        sleep(3)

        # Find the task selection dropdown and choose "image_captioning"
        task_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'task'))
        )
        task_dropdown.send_keys("image_captioning")

        # Find the file input element to upload the image
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )

        # Upload the image using the file path
        upload_input.send_keys(os.path.abspath(image_path))

        # Wait for the caption to be generated
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="tabpanel"][aria-labelledby="preview"]'))
        )

        # Click the "Run" button
        run_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"][form="input-form"]'))
        )
        run_button.click()

        # Introduce a delay to allow time for the caption to be updated
        sleep(2)

        # Wait for the caption text to appear
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="value-output-string"]'))
        )

        # Extract the caption text
        caption_element = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="value-output-string"]')
        caption_text = caption_element.text

        return caption_text

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        write_to_output_file(error_message)
        return None


def process_image(image_path):
    try:
        tmp_path = image_path
        if platform.system() == "Windows":
            image_path = image_path.replace('\\', '\\\\')
        caption = get_blip_caption(image_path)
        if caption is not None:
            result = f"{tmp_path}: {caption}"
            print(result)
            write_to_output_file(result)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        write_to_output_file(error_message)


def main():
    try:
        if len(sys.argv) > 1:
            # If command-line argument is provided, use it as image path
            image_path = sys.argv[1]
        else:
            # If no command-line argument, prompt user for image path
            image_path = input("Enter the path to the image: ")
        process_image(image_path)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        write_to_output_file(error_message)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
