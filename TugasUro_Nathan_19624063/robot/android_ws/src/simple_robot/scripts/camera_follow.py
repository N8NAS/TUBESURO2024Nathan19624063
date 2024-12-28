#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraFollow(Node):
    def __init__(self):
        super().__init__('camera_follow')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.image_subscriber = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.bridge = CvBridge()
        self.get_logger().info('Camera follow node initialized')

    def image_callback(self, msg):
        # Convert ROS image message to OpenCV format
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

        # Find contours in the threshold image
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # If contours are detected, move the robot toward the largest contour
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                error_x = cx - cv_image.shape[1] // 2

                move_cmd = Twist()
                move_cmd.linear.x = 0.5
                move_cmd.angular.z = -0.005 * error_x
                self.publisher.publish(move_cmd)
            else:
                move_cmd = Twist()
                move_cmd.linear.x = 0
                move_cmd.angular.z = 0
                self.publisher.publish(move_cmd)

def main(args=None):
    rclpy.init(args=args)
    camera_follow = CameraFollow()
    rclpy.spin(camera_follow)
    camera_follow.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

