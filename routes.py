from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import requests
from face_swap import swap_faces

swap_faces_api_bp = Blueprint('swap_faces_api', __name__)
swap_faces_client_bp = Blueprint('swap_faces_client', __name__)

@swap_faces_api_bp.route('/swap_faces', methods=['POST'])
def swap_faces_api():
    # Implementation of swap_faces_api route
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({'error': 'Please provide two image files.'}), 400
    
    # Read the input images
    img1 = cv2.imdecode(np.fromstring(request.files['image1'].read(), np.uint8), cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(np.fromstring(request.files['image2'].read(), np.uint8), cv2.IMREAD_COLOR)

    # Swap faces
    swapped_img1, swapped_img2 = swap_faces(img1, img2)

    cv2.imwrite('swappedimage1.jpg', swapped_img1)
    cv2.imwrite('swappedimage2.jpg', swapped_img2)

    return jsonify({'message': 'Faces swapped successfully.', 'swapped_images': ['swappedimage1.jpg', 'swappedimage2.jpg']}), 200

@swap_faces_client_bp.route('/swap_faces_client', methods=['POST'])
def swap_faces_client():
    # Implementation of swap_faces_client route
    if 'image1' not in request.form or 'image2' not in request.form:
        return jsonify({'error': 'Please provide two image URLs.'}), 400
    
    # Download images from URLs
    img1_url = request.form['image1']
    img2_url = request.form['image2']

    try:
        img1_response = requests.get(img1_url)
        img2_response = requests.get(img2_url)
        
        # Check if the responses success
        if img1_response.status_code != 200 or img2_response.status_code != 200:
            return jsonify({'error': 'Failed to download images. Make sure the URLs are correct and accessible.'}), 400
        
        
        img1_data = np.frombuffer(img1_response.content, dtype=np.uint8)
        img2_data = np.frombuffer(img2_response.content, dtype=np.uint8)
        
        
        img1 = cv2.imdecode(img1_data, cv2.IMREAD_COLOR)
        img2 = cv2.imdecode(img2_data, cv2.IMREAD_COLOR)

        # Swap faces
        swapped_img1, swapped_img2 = swap_faces(img1, img2)

        # Save swapped images locally
        cv2.imwrite('swappedimage1.jpg', swapped_img1)
        cv2.imwrite('swappedimage2.jpg', swapped_img2)

        return jsonify({'message': 'Faces swapped successfully.', 'swapped_images': ['swappedimage1.jpg', 'swappedimage2.jpg']}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to process images.', 'details': str(e)}), 500

