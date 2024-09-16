import cv2
import numpy as np
from robot.libraries.BuiltIn import BuiltIn
from ScreenshotManager import ScreenshotManager
from lxml import etree
from datetime import datetime
import os

class AppiumHelper:
    def __init__(self):
        self.driver = None
        self.ss_manager = ScreenshotManager.getInstance()

    def get_element_attributes_by_text(self, text):
        """
        Find an element by its partial text in the page source and retrieve its attributes.
        
        Args:
            text (str): The partial text to search for in the page source.

        Returns:
            dict: Dictionary containing the element's attributes, or None if not found.
        """
        # Get the current Appium driver from the AppiumLibrary
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()
        
        # Step 1: Get the page source dynamically
        page_source = driver.page_source
        print("page_source")
        print(page_source)
        # Step 2: Parse the page source using lxml
        tree = etree.fromstring(page_source.encode('utf-8'))
        print("tree")
        print(tree)

        
        # Step 3: Use XPath to find the element by partial text using contains()
        element = tree.xpath(f"//*[contains(@text, '{text}')]") or tree.xpath(f"//*[contains(@resource-id, '{text}')]")
        print("element")
        print(element)
        # If element is found, retrieve its attributes
        if element:
            element = element[0]  # Get the first matched element
            attributes = element.attrib  # Get the element's attributes
            
            # Return the attributes dictionary
            return attributes
        else:
            print(f"No element found with partial text: {text}")
            return None




    def capture_and_annotate_multiple_elements(self, texts, screenshot_name="screenshot.png"):
        """
        Capture a screenshot and annotate the areas around the elements with the given texts.
        
        Args:
            texts (list): A list of partial texts to search for.
            screenshot_name (str): The name of the screenshot file to save.
        """
        # Generate the timestamp
        time_stamp = str(datetime.now().astimezone().strftime('%Y-%m-%dT%H-%M-%S-%f'))

        # Ensure the screenshot_name does not have double ".png" extension
        if screenshot_name.endswith(".png.png"):
            screenshot_name = screenshot_name[:-4]

        # Modify the filename to include the timestamp
        final_filename = f"{time_stamp}-{screenshot_name}"

        # Get the current Appium driver from the AppiumLibrary
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()

        # Track found elements for failure checking
        found_elements = 0
        total_texts = len(texts)

        # Step 1: Capture the base screenshot if it doesn't exist yet
        if not os.path.exists(final_filename):
            driver.save_screenshot(final_filename)

        # Load the screenshot using OpenCV
        image = cv2.imread(final_filename)

        # Step 2: Iterate over each text and annotate if found
        for text in texts:
            attributes = self.get_element_attributes_by_text(text)

            if attributes and 'bounds' in attributes:
                found_elements += 1
                # Step 3: Parse the bounds attribute to get coordinates
                bounds = attributes['bounds']
                bounds = bounds.strip('[]').split('][')
                top_left = list(map(int, bounds[0].split(',')))
                bottom_right = list(map(int, bounds[1].split(',')))

                # Step 4: Draw a rectangle around the element based on the bounds
                cv2.rectangle(image, tuple(top_left), tuple(bottom_right), color=(0, 255, 0), thickness=3)
                print(f"Element with text '{text}' annotated.")
            else:
                print(f"Element with text '{text}' not found.")

        # Step 5: Save the annotated screenshot with the same filename
        cv2.imwrite(final_filename, image)

        # Step 6: Check if any elements were found; fail only if none are found
        if found_elements == 0:
            raise Exception(f"None of the provided texts were found: {texts}")
        elif found_elements < total_texts:
            print(f"Some elements were not found, but annotated screenshot saved at {final_filename}")
        else:
            print(f"All elements were found and annotated. Screenshot saved at {final_filename}")

        return final_filename

    def capture_screenshot_with_timestamp(self, base_screenshot_name):
        """
        Capture a screenshot with a timestamp and save it using the given base name.

        Args:
            base_screenshot_name (str): The base name for the screenshot file (without .png).
        
        Returns:
            str: The path of the saved screenshot with the timestamped filename.
        """
        # Generate the timestamp
        time_stamp = str(datetime.now().astimezone().strftime('%Y-%m-%dT%H-%M-%S-%f'))

        # Format the final screenshot name with timestamp
        final_screenshot_name = f"{time_stamp}-{base_screenshot_name}.png"

        # Get the current Appium driver from the AppiumLibrary
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()

        # Capture the screenshot and save it with the timestamped filename
        driver.save_screenshot(final_screenshot_name)

        print(f"Screenshot saved as: {final_screenshot_name}")

        # check if the screenshot is black screen
        if self.is_blank_screen(final_screenshot_name):
            # take screenshot using the external camera
            self.ss_manager.take_screenshot()
            self.ss_manager.save_screenshot(final_screenshot_name)
        return final_screenshot_name
    
    
    def is_black_screen(self, image_path):
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        average_colour = np.mean(gray_image)
        black_threshold = 10
        return average_colour < black_threshold
    
    def is_blank_screen(image_path, variance_threshold=15):
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        variance = np.var(gray_image)
        return variance < variance_threshold

    def tap_element_by_attributes(self, attributes):
        """
        Tap on an element using the attributes derived from the element.
        
        Args:
            attributes (dict): Dictionary containing the element's attributes.
        """
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()

        # Step 1: Try to find the element using XPath and click
        resource_id = attributes.get('resource-id')
        element_class = attributes.get('class')
        element_text = attributes.get('text')

        if resource_id:
            # Build XPath using resource-id if available
            xpath = f"//*[@resource-id='{resource_id}']"
        elif element_class and element_text:
            # Build XPath using class and text if available
            xpath = f"//{element_class}[@text='{element_text}']"
        else:
            xpath = None

        if xpath:
            try:
                # Try finding the element by XPath and tap it
                element = driver.find_element_by_xpath(xpath)
                element.click()
                print(f"Tapped element using XPath: {xpath}")
                return
            except Exception as e:
                print(f"Failed to tap element by XPath: {e}")
        
        # Step 2: If XPath fails, fall back to tapping by coordinates (bounds)
        bounds = attributes.get('bounds')
        if bounds:
            # Parse the bounds to get the top-left and bottom-right coordinates
            bounds = bounds.strip('[]').split('][')
            top_left = list(map(int, bounds[0].split(',')))
            bottom_right = list(map(int, bounds[1].split(',')))

            # Calculate the center of the element
            center_x = (top_left[0] + bottom_right[0]) // 2
            center_y = (top_left[1] + bottom_right[1]) // 2

            # Tap on the center of the element
            driver.tap([(center_x, center_y)])
            print(f"Tapped element by coordinates: ({center_x}, {center_y})")
        else:
            raise Exception("Unable to tap element: No valid XPath or bounds found")
    
    def crop_all_interactable_elements(self, screenshot_name="screenshot.png", output_dir="cropped_elements", annotate=False):
        """
        Capture a screenshot and crop all interactable elements using their bounds.
        Optionally, annotate the original screenshot with rectangles around the interactable elements.

        Args:
            screenshot_name (str): The name of the screenshot file to save.
            output_dir (str): The directory where cropped elements will be saved.
            annotate (bool): If True, also annotate the original screenshot with rectangles around the elements.
        """
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate the timestamp
        time_stamp = str(datetime.now().astimezone().strftime('%Y-%m-%dT%H-%M-%S-%f'))

        # Ensure the screenshot_name does not have double ".png" extension
        if screenshot_name.endswith(".png"):
            screenshot_name = screenshot_name[:-4]

        # Modify the filename to include the timestamp
        final_filename = f"{time_stamp}-{screenshot_name}"

        # Get the current Appium driver from the AppiumLibrary
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()

        # Step 1: Capture the base screenshot
        driver.save_screenshot(final_filename)

        # Load the screenshot using OpenCV
        image = cv2.imread(final_filename)

        # Get page source (XML) and parse it
        page_source = driver.page_source
        tree = etree.fromstring(page_source.encode('utf-8'))

        # Track element cropping
        element_count = 0

        # Step 2: Iterate over all elements and crop interactable ones (with 'bounds')
        for element in tree.xpath("//*[@bounds]"):
            bounds = element.get('bounds')
            bounds = bounds.strip('[]').split('][')
            top_left = list(map(int, bounds[0].split(',')))
            bottom_right = list(map(int, bounds[1].split(',')))

            # Crop the element from the screenshot
            cropped_image = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            
            # Save the cropped element
            cropped_filename = os.path.join(output_dir, f"cropped_element_{element_count}.png")
            cv2.imwrite(cropped_filename, cropped_image)
            print(f"Cropped element saved at: {cropped_filename}")
            element_count += 1

        # Step 3: If annotate flag is True, call the annotate_page_with_elements method
        if annotate:
            self.annotate_page_with_elements(final_filename)

        if element_count == 0:
            raise Exception("No interactable elements found with bounds.")
        else:
            print(f"Total interactable elements cropped: {element_count}")

        return element_count

    def get_clickable_elements_with_attributes(self):
        """
        Extract all visible and clickable elements from the page source and return their attributes.
        
        Returns:
            list: A list of dictionaries containing the attributes of clickable elements.
        """
        # Get the current Appium driver from the AppiumLibrary
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()

        # Get page source dynamically
        page_source = driver.page_source

        # Parse the page source using lxml
        tree = etree.fromstring(page_source.encode('utf-8'))

        # Define the list to store clickable elements' attributes
        clickable_elements = []

        # Find all clickable elements (using @clickable attribute or elements typically clickable like buttons)
        elements = tree.xpath("//*[contains(@clickable, 'true') or self::button or self::a]")

        # Iterate through all found elements
        for element in elements:
            # Extract element's attributes
            attributes = element.attrib
            bounds = attributes.get('bounds', None)
            
            # Ensure the element is visible (optional: implement additional checks for visibility)
            if bounds:
                clickable_elements.append(attributes)

        return clickable_elements
    
    def set_checkbox_state(self, state=True):
        """
        Set the state of the only checkbox on the page to checked or unchecked.

        Args:
            state (bool): True to check the checkbox, False to uncheck it.
        """
        # Get the current Appium driver from the AppiumLibrary
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()

        try:
            # Locate the checkbox element by its XPath
            checkbox_element = driver.find_element_by_xpath("//android.widget.CheckBox")

            # Get the current state of the checkbox (checked or unchecked)
            current_state = checkbox_element.get_attribute("checked") == "true"
            
            # If the current state is different from the desired state, click to change it
            if current_state != state:
                checkbox_element.click()
                print(f"Checkbox state set to: {'checked' if state else 'unchecked'}")
            else:
                print(f"Checkbox is already {'checked' if state else 'unchecked'}.")
        
        except Exception as e:
            print(f"Error setting checkbox state: {e}")

    
    def get_window_size(self):
        """Get the size of the device window."""
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        driver = appium_lib._current_application()
        return driver.get_window_size()
    
    def find_image(self, template_image_path, threshold=0.8):
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        self.driver = appium_lib._current_application()
        """Find an image on the screen and click it."""
        # Take a screenshot
        screenshot_path = '/tmp/screen.png'
        self.driver.save_screenshot(screenshot_path)

        # Read the screenshot and template image
        screenshot = cv2.imread(screenshot_path)
        template = cv2.imread(template_image_path)

        # Convert to grayscale
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Perform template matching
        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if match is above the threshold
        if max_val >= threshold:
            template_height, template_width = template_gray.shape[:2]
            click_x = max_loc[0] + template_width // 2
            click_y = max_loc[1] + template_height // 2

            # Simulate a click at the center of the found image
            return click_x, click_y

        else:
            raise ValueError("Image not found on the screen or match quality is too low.")
        

    def swipe_from_image(self, image_path, direction, percentage):
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        self.driver = appium_lib._current_application()
        """Find an image on the screen and swipe in the given direction by a percentage of the screen size."""
        # Get the coordinates of the image
        x, y = self.find_image(image_path)

        # Get the screen size
        window_size = self.get_window_size()
        width = window_size['width']
        height = window_size['height']

        # Calculate the swipe end points based on direction and percentage
        if direction.lower() == 'right':
            start_x = x
            end_x = min(x + int(width * (percentage / 100)), width - 1)  # Ensure end_x does not go off screen
            start_y = end_y = y  # Keep the swipe at the same vertical level
        elif direction.lower() == 'left':
            start_x = x
            end_x = max(x - int(width * (percentage / 100)), 0)  # Ensure end_x does not go off screen
            start_y = end_y = y
        elif direction.lower() == 'up':
            start_y = y
            end_y = max(y - int(height * (percentage / 100)), 0)
            start_x = end_x = x
        elif direction.lower() == 'down':
            start_y = y
            end_y = min(y + int(height * (percentage / 100)), height - 1)
            start_x = end_x = x
        else:
            raise ValueError(f"Unsupported swipe direction: {direction}")

        # Perform the swipe
        self.driver.swipe(start_x, start_y, end_x, end_y, 500)

