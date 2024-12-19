import cv2
import numpy as np


def is_contained(box1, box2):
    """
    Check if bbox1 is completely contained within bbox2.
    """
    return (
        box1[0] >= box2[0] and
        box1[1] >= box2[1] and
        box1[2] <= box2[2] and
        box1[3] <= box2[3]
    )


def union_boxes(box1, box2):
    """
    Union two bounding boxes to create one encompassing box.
    """
    x1 = min(box1[0], box2[0])
    y1 = min(box1[1], box2[1])
    # Bottom-right corner of the new box
    x2 = max(box1[0] + box1[2], box2[0] + box2[2])
    y2 = max(box1[1] + box1[3], box2[1] + box2[3])
    # New width and height
    new_width = x2 - x1
    new_height = y2 - y1
    # New area
    new_area = new_width * new_height
    return [x1, y1, new_width, new_height, new_area]


def is_near(box1, box2, distance_threshold):
    """
    Determine if two bounding boxes are near each other based on a distance threshold.
    """
    # Calculate the Euclidean distance between the centers of the boxes
    center1 = ((box1[0] + box1[2]) / 2, (box1[1] + box1[3]) / 2)
    center2 = ((box2[0] + box2[2]) / 2, (box2[1] + box2[3]) / 2)
    distance = np.linalg.norm(np.array(center1) - np.array(center2))
    return distance < distance_threshold


def merge_near_detections(detections, distance_threshold):
    """
    Merge detections that are near each other.
    """
    merged_detections = []
    while len(detections) > 0:
        current = detections.pop(0)  # Take the first box
        remaining_detections = []
        for det in detections:
            if is_near(current, det, distance_threshold):
                # If near, union them and replace the current with the union
                current = union_boxes(current, det)
            else:
                remaining_detections.append(det)  # Keep the other detections
        # After processing, add the final merged box
        merged_detections.append(current)
        detections = remaining_detections  # Update remaining detections

    return np.array(merged_detections)


def perform_nms(detections, overlap_threshold):
    """
    Apply Non-Maximal Suppression to the list of detections.
    """
    # Sort detections by the area of the bounding boxes (large to small)
    indices = np.argsort([-d[4] for d in detections])
    detections = detections[indices]

    final_detections = []
    while len(detections) > 0:
        # Pick the largest bounding box (by area)
        current = detections[0]
        final_detections.append(current)

        # Compute overlap with the remaining detections
        remaining = detections[1:]
        remaining_indices = []
        for i, det in enumerate(remaining):
            # Calculate the intersection area
            x1 = max(current[0], det[0])
            y1 = max(current[1], det[1])
            x2 = min(current[2], det[2])
            y2 = min(current[3], det[3])

            # Calculate overlap ratio
            intersection_area = max(0, x2 - x1) * max(0, y2 - y1)
            union_area = current[4] + det[4] - intersection_area
            overlap_ratio = intersection_area / union_area

            # Keep detections with low overlap
            if overlap_ratio < overlap_threshold:
                remaining_indices.append(i)

        # Only keep the detections that do not have high overlap
        detections = remaining[remaining_indices]

    return np.array(final_detections)


def get_contour_detections(mask, thresh=400, suppression_thresh=0.3, distance_threshold=55):
    # get mask contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        if area > thresh:  # hyperparameter
            detections.append([x, y, x + w, y + h, area])
    detections = np.array(detections)

    if len(detections) == 0:
        return np.array([])

    # Remove contained bounding boxes
    non_contained_detections = []
    for i, box1 in enumerate(detections):
        contained = False
        for j, box2 in enumerate(detections):
            if i != j and is_contained(box1, box2):
                contained = True
                break
        if not contained:
            non_contained_detections.append(box1)

    non_contained_detections = np.array(non_contained_detections)
    # Perform Non-Maximal Suppression
    nms_detections = perform_nms(non_contained_detections, suppression_thresh)
    final_detections = merge_near_detections(nms_detections.tolist(), distance_threshold)

    return final_detections


def draw_contours(frame, detections):
    if len(detections) == 0:
        return frame
    # separate bboxes and areas
    bboxes = detections[:, :4]

    for box in bboxes:
        x1, y1, x2, y2 = box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

    return frame
