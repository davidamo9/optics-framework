import cv2
import numpy as np
from pathlib import Path
import os


def find_template(frame, templates, rule='any', confidence_level=0.75, min_inliers=10):
    """
    Match template images within a single frame image using SIFT and FLANN-based matching.

    Parameters:
    - frame: The frame image as a numpy array.
    - templates: A list of paths to template images.
    - rule (str): 'any' (return True on first match) or 'all' (return True only if all templates match).
    - confidence_level (float): Confidence level for the ratio test (default is 0.75).
    - min_inliers (int): Minimum number of inliers required to consider a match valid (default is 10).

    Returns:
    - bool: True if the templates are found according to the rule, False otherwise.
    """

    # Create SIFT object
    sift = cv2.SIFT_create()

    # Create FLANN object with parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    if frame is None:
        print("Error: Cannot read the images.")
        return False

    # Detect keypoints and descriptors for frame
    kp_frame, des_frame = sift.detectAndCompute(frame, None)

    # Initialize a flag to track if all templates were matched (for the 'all' rule)
    all_matched = True
    annotated_frame = frame.copy()

    for template in templates:
        template_path = Path(os.path.abspath(__file__)).resolve().parent.parent / "Resources" / "elements" / template
        template_img = cv2.imread(str(template_path))

        if template_img is None:
            print(f"Error: {template} is unreadable or does not exist.")
            all_matched = False
            if rule == 'all':
                return False
            continue

        # Detect keypoints and descriptors for templates
        kp_template, des_template = sift.detectAndCompute(template_img, None)

        if des_template is None or des_frame is None:
            all_matched = False
            if rule == 'all':
                return False
            continue

        try:
            matches = flann.knnMatch(des_template, des_frame, k=2)
        except cv2.error:
            all_matched = False
            if rule == 'all':
                return False
            continue

        # Apply ratio test to filter good matches
        good_matches = []
        for m, n in matches:
            if m.distance < confidence_level * n.distance:
                good_matches.append(m)

        if len(good_matches) < min_inliers:
            all_matched = False
            if rule == 'all':
                return False
            continue

        # If enough good matches are found, calculate homography
        src_pts = np.float32([kp_template[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()

        # Check the number of inliers
        inliers = np.sum(matches_mask)
        if inliers < min_inliers:
            all_matched = False
            if rule == 'all':
                return False
            continue

        h, w = template_img.shape[:2]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

        try:
            dst = cv2.perspectiveTransform(pts, M)
            annotated_frame = cv2.polylines(annotated_frame, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
            if rule == 'any':
                return True, annotated_frame
        except cv2.error:
            all_matched = False
            if rule == 'all':
                return False
            continue

    return all_matched if rule == 'all' else False, annotated_frame

frame_path = 'vivologo/screen.jpg'
# frame = cv2.imread(frame_path)
templates = ['vivologo/vivotemp.jpg']
find_template(frame_path,templates,rule='all')