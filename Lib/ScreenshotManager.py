import cv2
import os
import numpy as np
import socket
from pathlib import Path
from datetime import datetime

class ScreenshotManager:
    _instance = None
    screenshot = None

    def __init__(self, ip_address="127.0.0.1", port=3000):
        self.sock = self.create_tcp_connection(ip_address, port)
        if not self.sock:
            raise ConnectionError(f"Failed to establish TCP connection to {ip_address}:{port}")

    @staticmethod
    def getInstance(ip_address="127.0.0.1", port=3000):
        if ScreenshotManager._instance is None:
            ScreenshotManager._instance = ScreenshotManager(ip_address, port)
        return ScreenshotManager._instance

    def create_tcp_connection(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            print(f"TCP connection established with {ip}:{port}")
            return sock
        except Exception as e:
            print(f"Error creating TCP connection: {e}")
            return None

    def set_screenshot(self, img):
        self.screenshot = img

    def get_screenshot(self):
        print(f"get_screenshot... ")
        return self.screenshot

    def take_screenshot(self):
        """
        Takes a screenshot using the provided socket and returns the image data as an OpenCV image.
        """
        try:
            if not self.sock:
                raise ConnectionError("No valid socket connection. Unable to take screenshot.")

            # Send the screenshot command
            self.sock.sendall(b'screenshot\n')
            print("Taking screenshot...")

            # Read the first 8 bytes to get the length of the image data
            length_bytes = self.sock.recv(8)
            if len(length_bytes) < 8:
                raise ValueError("Failed to read the length of the image data.")

            image_length = int.from_bytes(length_bytes, byteorder='little', signed=False)
            print(f"Expected image data length: {image_length} bytes")

            # Initialize a bytearray for the image data
            image_data = bytearray()
            remaining_bytes = image_length

            while remaining_bytes > 0:
                chunk_size = min(1024, remaining_bytes)
                chunk = self.sock.recv(chunk_size)
                if not chunk:
                    raise ValueError("Socket connection closed prematurely.")
                image_data.extend(chunk)
                remaining_bytes -= len(chunk)
            print("Transferred image data...")

            # Convert the received image data to a numpy array
            nparr = np.frombuffer(image_data, np.uint8)

            # Decode the image data to an OpenCV image
            screenshot = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            print("Image ready, setting screenshot")
            self.set_screenshot(screenshot)
            return screenshot
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def set_frame_match(self, path):
        """
        Reads an image from the given file path and returns it as a byte array.
        """
        try:
            print(f"Reading dummy screenshot from path: {path}")
            with open(path, 'rb') as file:
                binary_data = file.read()
            return binary_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def save_screenshot(self, img, name):
        """
        Save the screenshot with a timestamp and keyword in the filename.
        """
        time_stamp = str(datetime.now().astimezone().strftime('%Y-%m-%dT%H-%M-%S-%f'))
        screenshot_filename = f'{time_stamp}_{name}.jpg'
        screenshot_file_path = self.get_path(screenshot_filename)
        cv2.imwrite(screenshot_file_path, img)
        print(f"Screenshot saved to :{screenshot_file_path}")

    def save_annotated_screenshot(self, img, element):
        time_stamp = str(datetime.now().astimezone().strftime('%Y-%m-%dT%H-%M-%S-%f'))
        screenshot_filename = f'{time_stamp}_{element}.jpg'
        screenshot_filename = screenshot_filename.replace('/', '_')
        screenshot_file_path = self.get_path(screenshot_filename)
        cv2.imwrite(screenshot_file_path,img)
        print(f"Annotated Screenshot saved to :{screenshot_file_path}")

    def get_path(self, extension_path):
        script_dir = Path(__file__).parent.parent.parent.as_posix()
        dir_path = os.path.join(script_dir, "screenshot", extension_path)
        return dir_path


