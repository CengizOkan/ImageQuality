"""
    Applies JPEG compression to the input image to modify its quality and simulate compression artifacts.
"""
import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.ImageQuality.src.utils.response import build_response
from components.ImageQuality.src.models.PackageModel import PackageModel

class JpegQuality(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        
        # Parse request with model
        self.request.model = PackageModel(**(self.request.data))
        
        # Extract parameters
        self.q_value = self.request.get_param("ConfigJpegQuality")
        
        # Extract inputs
        self.target_image = self.request.get_param("targetImage")
    
    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}
    
    def process_quality(self, img_matrix):
        """Compresses and decompresses image to apply target JPEG Q-factor"""
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.q_value]
        success, encoded_image = cv2.imencode('.jpg', img_matrix, encode_param)
        
        if success:
            decoded_image = cv2.imdecode(encoded_image, 1)
            return decoded_image
        return img_matrix
    
    def run(self):
        # Get image from Redis
        target = Image.get_frame(
            img=self.target_image, 
            redis_db=self.redis_db
        )
        
        # Process image matrix
        target.value = self.process_quality(np.array(target.value))
        
        # Store result to Redis
        self.target_image = Image.set_frame(
            img=target, 
            package_uID=self.uID, 
            redis_db=self.redis_db
        )
        
        # Build and return response
        package_model = build_response(context=self)
        return package_model

if "__main__" == __name__:
    Executor(sys.argv[1]).run()