import cv2
import time
import os
import numpy as np
from picamera2 import Picamera2

class DualCameraController:
    def __init__(self):
        # Initialize variables
        self.cameras = []
        self.active_camera = 0  # Index of the currently selected camera
        self.preview_active = True
        self.exposure_values = [0, 0]  # Exposure compensation for each camera
        self.brightness_values = [0, 0]  # Brightness adjustment for each camera
        self.resolution_options = [
            (640, 480),    # Low resolution
            (1280, 720),   # HD resolution
            (1920, 1080),  # Full HD resolution
            (2592, 1944)   # High resolution
        ]
        self.current_resolution_idx = 0  # Start with HD resolution
        self.save_directory = "camera_captures"
        self.setup_cameras()
        
    def setup_cameras(self):
        """Initialize and configure both cameras"""
        try:
            # Ensure the directory for saving images exists
            if not os.path.exists(self.save_directory):
                os.makedirs(self.save_directory)
                
            # Initialize both cameras
            for i in range(2):
                camera = Picamera2(i)
                # Configure camera with initial settings
                config = camera.create_preview_configuration(
                    main={"size": self.resolution_options[self.current_resolution_idx]},
                    lores={"size": (640, 480)},
                    display="lores"
                )
                camera.configure(config)
                camera.start()
                self.cameras.append(camera)
                
            print("Both cameras initialized successfully")
            
        except Exception as e:
            print(f"Error initializing cameras: {e}")
            exit(1)
    
    def capture_image(self, camera_idx):
        """Capture and save an image from the specified camera"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.save_directory}/camera{camera_idx+1}_{timestamp}.jpg"
        
        # Capture image with current settings
        img = self.cameras[camera_idx].capture_array()
        
        # Apply brightness adjustment if needed
        if self.brightness_values[camera_idx] != 0:
            img = cv2.convertScaleAbs(img, alpha=1, beta=self.brightness_values[camera_idx])
            
        # Save the image
        cv2.imwrite(filename, img)
        print(f"Image saved as {filename}")
        return filename
    
    def change_resolution(self):
        """Change resolution for both cameras"""
        self.current_resolution_idx = (self.current_resolution_idx + 1) % len(self.resolution_options)
        resolution = self.resolution_options[self.current_resolution_idx]
        
        # Reconfigure both cameras with new resolution
        for i, camera in enumerate(self.cameras):
            camera.stop()
            config = camera.create_preview_configuration(
                main={"size": resolution},
                lores={"size": (640, 480)},
                display="lores"
            )
            camera.configure(config)
            camera.start()
            
        print(f"Resolution changed to {resolution[0]}x{resolution[1]}")
    
    def adjust_exposure(self, camera_idx, direction):
        """Adjust exposure compensation for the specified camera"""
        step = 1
        if direction == "up":
            self.exposure_values[camera_idx] = min(8, self.exposure_values[camera_idx] + step)
        else:
            self.exposure_values[camera_idx] = max(-8, self.exposure_values[camera_idx] - step)
            
        # Apply exposure compensation
        self.cameras[camera_idx].set_controls({"ExposureValue": self.exposure_values[camera_idx]})
        print(f"Camera {camera_idx+1} exposure compensation: {self.exposure_values[camera_idx]}")
    
    def adjust_brightness(self, camera_idx, direction):
        """Adjust brightness for the specified camera"""
        step = 5
        if direction == "up":
            self.brightness_values[camera_idx] = min(100, self.brightness_values[camera_idx] + step)
        else:
            self.brightness_values[camera_idx] = max(-100, self.brightness_values[camera_idx] - step)
            
        print(f"Camera {camera_idx+1} brightness: {self.brightness_values[camera_idx]}")
    
    def add_info_overlay(self, frame, camera_idx):
        """Add information overlay to the frame"""
        height, width = frame.shape[:2]
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        resolution = f"{width}x{height}"
        
        # Define the information to display
        info_text = [
            f"Camera {camera_idx+1} {'(ACTIVE)' if camera_idx == self.active_camera else ''}",
            f"Time: {timestamp}",
            f"Resolution: {resolution}",
            f"Exposure: {self.exposure_values[camera_idx]}",
            f"Brightness: {self.brightness_values[camera_idx]}"
        ]
        
        # Add a semi-transparent black background for text
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 110), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Add text
        for i, text in enumerate(info_text):
            cv2.putText(frame, text, (20, 35 + i*20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
        # Highlight active camera with a colored border
        if camera_idx == self.active_camera:
            cv2.rectangle(frame, (0, 0), (width-1, height-1), (0, 255, 0), 2)
            
        return frame
    
    def run(self):
        """Main function to run the dual camera preview and control"""
        print("\nDual Camera Controller Started")
        print("--------------------------------")
        print("Controls:")
        print("  1, 2      - Select Camera 1 or 2")
        print("  s         - Save image from active camera")
        print("  d         - Save images from both cameras")
        print("  r         - Change resolution")
        print("  e/c       - Increase/decrease exposure of active camera")
        print("  b/v       - Increase/decrease brightness of active camera")
        print("  p         - Pause/resume preview")
        print("  q         - Quit application")
        print("--------------------------------")
        
        while True:
            # Capture frames from both cameras
            frames = []
            for i, camera in enumerate(self.cameras):
                frame = camera.capture_array()
                
                # Apply brightness adjustment
                if self.brightness_values[i] != 0:
                    frame = cv2.convertScaleAbs(frame, alpha=1, beta=self.brightness_values[i])
                
                # Add information overlay
                frame = self.add_info_overlay(frame, i)
                frames.append(frame)
            
            # Display frames if preview is active
            if self.preview_active:
                 # Stack the frames horizontally
                 combined_frame = np.hstack([cv2.cvtColor(f, cv2.COLOR_RGB2BGR) for f in frames])
                 cv2.imshow('Dual Camera Preview', combined_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                # Quit the application
                break
                
            elif key == ord('1'):
                # Select camera 1
                self.active_camera = 0
                print("Camera 1 selected")
                
            elif key == ord('2'):
                # Select camera 2
                self.active_camera = 1
                print("Camera 2 selected")
                
            elif key == ord('s'):
                # Save image from active camera
                self.capture_image(self.active_camera)
                
            elif key == ord('d'):
                # Save images from both cameras
                for i in range(2):
                    self.capture_image(i)
                    
            elif key == ord('r'):
                # Change resolution
                self.change_resolution()
                
            elif key == ord('e'):
                # Increase exposure of active camera
                self.adjust_exposure(self.active_camera, "up")
                
            elif key == ord('c'):
                # Decrease exposure of active camera
                self.adjust_exposure(self.active_camera, "down")
                
            elif key == ord('b'):
                # Increase brightness of active camera
                self.adjust_brightness(self.active_camera, "up")
                
            elif key == ord('v'):
                # Decrease brightness of active camera
                self.adjust_brightness(self.active_camera, "down")
                
            elif key == ord('p'):
                # Toggle preview
                self.preview_active = not self.preview_active
                if self.preview_active:
                    print("Preview resumed")
                else:
                    print("Preview paused")
        
        # Clean up
        cv2.destroyAllWindows()
        for camera in self.cameras:
            camera.stop()
        print("Application terminated")

if __name__ == "__main__":
    controller = DualCameraController()
    controller.run()