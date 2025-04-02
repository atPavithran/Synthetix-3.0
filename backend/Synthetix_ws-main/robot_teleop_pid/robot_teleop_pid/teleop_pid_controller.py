import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class TeleopPIDController(Node):
    def __init__(self):
        super().__init__('teleop_pid_controller')
        
        # Declare parameters
        self.declare_parameter('active_robot', 0)  # Default to all robots
        self.declare_parameter('kp', 23.0)
        self.declare_parameter('ki', 0.5)
        self.declare_parameter('kd', 1.0)
        
        # Get parameters
        self.active_robot = self.get_parameter('active_robot').value
        self.Kp = self.get_parameter('kp').value
        self.Ki = self.get_parameter('ki').value
        self.Kd = self.get_parameter('kd').value
        
        # Log the active robot
        self.get_logger().info(f"Active robot: {self.active_robot} (0=all, 1-5=specific robot)")
        self.get_logger().info(f"PID parameters: Kp={self.Kp}, Ki={self.Ki}, Kd={self.Kd}")
        
        # Create publishers for robot cmd_vel
        self.r1_vel_pub = self.create_publisher(Twist, '/robot1/cmd_vel', 10)
        self.r2_vel_pub = self.create_publisher(Twist, '/robot2/cmd_vel', 10)
        self.r3_vel_pub = self.create_publisher(Twist, '/robot3/cmd_vel', 10)
        self.r4_vel_pub = self.create_publisher(Twist, '/robot4/cmd_vel', 10)
        self.r5_vel_pub = self.create_publisher(Twist, '/robot5/cmd_vel', 10)
        
        # Subscribe to teleop commands
        self.teleop_sub = self.create_subscription(
            Twist,
            '/teleop_key/cmd_vel',  # Standard teleop keyboard topic
            self.teleop_callback,
            10
        )
        
        # Subscribe to odometry for each robot
        self.r1_odom_sub = self.create_subscription(Odometry, '/robot1/odom', self.r1_odom_callback, 10)
        self.r2_odom_sub = self.create_subscription(Odometry, '/robot2/odom', self.r2_odom_callback, 10)
        self.r3_odom_sub = self.create_subscription(Odometry, '/robot3/odom', self.r3_odom_callback, 10)
        self.r4_odom_sub = self.create_subscription(Odometry, '/robot4/odom', self.r4_odom_callback, 10)
        self.r5_odom_sub = self.create_subscription(Odometry, '/robot5/odom', self.r5_odom_callback, 10)
        
        # Current yaw angles for each robot
        self.r1_yaw = 0.0
        self.r2_yaw = 0.0
        self.r3_yaw = 0.0
        self.r4_yaw = 0.0
        self.r5_yaw = 0.0
        
        # Target yaw angles (set by teleop)
        self.r1_target_yaw = 0.0
        self.r2_target_yaw = 0.0
        self.r3_target_yaw = 0.0
        self.r4_target_yaw = 0.0
        self.r5_target_yaw = 0.0
        
        # Error storage for PID
        self.r1_error = 0.0
        self.r2_error = 0.0
        self.r3_error = 0.0
        self.r4_error = 0.0
        self.r5_error = 0.0
        
        # Previous error for D term
        self.r1_prev = 0.0
        self.r2_prev = 0.0
        self.r3_prev = 0.0
        self.r4_prev = 0.0
        self.r5_prev = 0.0
        
        # Error sum for I term
        self.r1_error_sum = 0.0
        self.r2_error_sum = 0.0
        self.r3_error_sum = 0.0
        self.r4_error_sum = 0.0
        self.r5_error_sum = 0.0
        
        # Robot linear speeds (set by teleop)
        self.r1_speed = 0.0
        self.r2_speed = 0.0
        self.r3_speed = 0.0
        self.r4_speed = 0.0
        self.r5_speed = 0.0
        
        # Last teleop command
        self.last_linear_x = 0.0
        self.last_angular_z = 0.0
        
        # Timer for publishing control outputs
        self.timer = self.create_timer(0.1, self.publish_cmd_vel)
        
        # Print instructions
        self.get_logger().info("Teleop PID Controller started")
        self.get_logger().info("Press 1-5 to select a specific robot (0 for all robots)")
        self.get_logger().info("Use standard teleop keys to drive")
    
    def teleop_callback(self, msg):
        # Extract linear and angular velocity from teleop
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # Store for debugging
        self.last_linear_x = linear_x
        self.last_angular_z = angular_z
        
        # Check for robot selection commands
        # (This would require custom teleop or additional inputs)
        # For now, we'll assume all robots are controlled together
        
        # Update speeds based on teleop linear x
        if self.active_robot == 0 or self.active_robot == 1:
            self.r1_speed = linear_x
        if self.active_robot == 0 or self.active_robot == 2:
            self.r2_speed = linear_x
        if self.active_robot == 0 or self.active_robot == 3:
            self.r3_speed = linear_x
        if self.active_robot == 0 or self.active_robot == 4:
            self.r4_speed = linear_x
        if self.active_robot == 0 or self.active_robot == 5:
            self.r5_speed = linear_x
        
        # Update target yaw based on teleop angular z
        # Instead of directly applying angular velocity, we adjust the target yaw
        yaw_change = angular_z * 0.1  # Scale based on timer interval
        
        if self.active_robot == 0 or self.active_robot == 1:
            self.r1_target_yaw += yaw_change
            self.r1_target_yaw = self.normalize_angle(self.r1_target_yaw)
        if self.active_robot == 0 or self.active_robot == 2:
            self.r2_target_yaw += yaw_change
            self.r2_target_yaw = self.normalize_angle(self.r2_target_yaw)
        if self.active_robot == 0 or self.active_robot == 3:
            self.r3_target_yaw += yaw_change
            self.r3_target_yaw = self.normalize_angle(self.r3_target_yaw)
        if self.active_robot == 0 or self.active_robot == 4:
            self.r4_target_yaw += yaw_change
            self.r4_target_yaw = self.normalize_angle(self.r4_target_yaw)
        if self.active_robot == 0 or self.active_robot == 5:
            self.r5_target_yaw += yaw_change
            self.r5_target_yaw = self.normalize_angle(self.r5_target_yaw)
        
        self.get_logger().info(f"Teleop: linear_x={linear_x:.2f}, angular_z={angular_z:.2f}")
        self.get_logger().info(f"Target yaw: R1={self.r1_target_yaw:.2f}, R2={self.r2_target_yaw:.2f}")
    
    def normalize_angle(self, angle):
        # Normalize angle to [-π, π]
        return ((angle + math.pi) % (2 * math.pi)) - math.pi
    
    def extract_yaw(self, msg):
        # Extract yaw from quaternion
        x = msg.pose.pose.orientation.x
        y = msg.pose.pose.orientation.y
        z = msg.pose.pose.orientation.z
        w = msg.pose.pose.orientation.w
        
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        
        return yaw
    
    def publish_cmd_vel(self):
        # Create twist messages for each robot
        r1_twist = Twist()
        r2_twist = Twist()
        r3_twist = Twist()
        r4_twist = Twist()
        r5_twist = Twist()
        
        # Set linear velocities from stored speeds based on active_robot
        if self.active_robot == 0 or self.active_robot == 1:
            r1_twist.linear.x = self.r1_speed
        else:
            r1_twist.linear.x = 0.0  # Stop if not active
            
        if self.active_robot == 0 or self.active_robot == 2:
            r2_twist.linear.x = self.r2_speed
        else:
            r2_twist.linear.x = 0.0
            
        if self.active_robot == 0 or self.active_robot == 3:
            r3_twist.linear.x = self.r3_speed
        else:
            r3_twist.linear.x = 0.0
            
        if self.active_robot == 0 or self.active_robot == 4:
            r4_twist.linear.x = self.r4_speed
        else:
            r4_twist.linear.x = 0.0
            
        if self.active_robot == 0 or self.active_robot == 5:
            r5_twist.linear.x = self.r5_speed
        else:
            r5_twist.linear.x = 0.0
        
        # Calculate PID corrections for robot 1
        if (self.active_robot == 0 or self.active_robot == 1) and abs(self.r1_speed) > 0.01:
            r1_p_term = self.Kp * self.r1_error
            self.r1_error_sum += self.r1_error * 0.1  # 0.1 is timer period
            r1_i_term = self.Ki * self.r1_error_sum
            r1_error_change = self.r1_error - self.r1_prev
            r1_d_term = self.Kd * r1_error_change / 0.1
            r1_angular_correction = r1_p_term + r1_i_term + r1_d_term
            r1_twist.angular.z = r1_angular_correction
        elif (self.active_robot == 0 or self.active_robot == 1) and self.last_angular_z != 0.0:
            # When stopped but turning, apply teleop angular directly with a scaling factor
            r1_twist.angular.z = self.last_angular_z * 2.0
            self.r1_error_sum = 0.0  # Reset I term when stopped
        else:
            r1_twist.angular.z = 0.0
            self.r1_error_sum = 0.0
        
        # Calculate PID corrections for robot 2
        if (self.active_robot == 0 or self.active_robot == 2) and abs(self.r2_speed) > 0.01:
            r2_p_term = self.Kp * self.r2_error
            self.r2_error_sum += self.r2_error * 0.1
            r2_i_term = self.Ki * self.r2_error_sum
            r2_error_change = self.r2_error - self.r2_prev
            r2_d_term = self.Kd * r2_error_change / 0.1
            r2_angular_correction = r2_p_term + r2_i_term + r2_d_term
            r2_twist.angular.z = r2_angular_correction
        elif (self.active_robot == 0 or self.active_robot == 2) and self.last_angular_z != 0.0:
            r2_twist.angular.z = self.last_angular_z * 2.0
            self.r2_error_sum = 0.0
        else:
            r2_twist.angular.z = 0.0
            self.r2_error_sum = 0.0
        
        # Calculate PID corrections for robot 3
        if (self.active_robot == 0 or self.active_robot == 3) and abs(self.r3_speed) > 0.01:
            r3_p_term = self.Kp * self.r3_error
            self.r3_error_sum += self.r3_error * 0.1
            r3_i_term = self.Ki * self.r3_error_sum
            r3_error_change = self.r3_error - self.r3_prev
            r3_d_term = self.Kd * r3_error_change / 0.1
            r3_angular_correction = r3_p_term + r3_i_term + r3_d_term
            r3_twist.angular.z = r3_angular_correction
        elif (self.active_robot == 0 or self.active_robot == 3) and self.last_angular_z != 0.0:
            r3_twist.angular.z = self.last_angular_z * 2.0
            self.r3_error_sum = 0.0
        else:
            r3_twist.angular.z = 0.0
            self.r3_error_sum = 0.0
        
        # Calculate PID corrections for robot 4
        if (self.active_robot == 0 or self.active_robot == 4) and abs(self.r4_speed) > 0.01:
            r4_p_term = self.Kp * self.r4_error
            self.r4_error_sum += self.r4_error * 0.1
            r4_i_term = self.Ki * self.r4_error_sum
            r4_error_change = self.r4_error - self.r4_prev
            r4_d_term = self.Kd * r4_error_change / 0.1
            r4_angular_correction = r4_p_term + r4_i_term + r4_d_term
            r4_twist.angular.z = r4_angular_correction
        elif (self.active_robot == 0 or self.active_robot == 4) and self.last_angular_z != 0.0:
            r4_twist.angular.z = self.last_angular_z * 2.0
            self.r4_error_sum = 0.0
        else:
            r4_twist.angular.z = 0.0
            self.r4_error_sum = 0.0
        
        # Calculate PID corrections for robot 5
        if (self.active_robot == 0 or self.active_robot == 5) and abs(self.r5_speed) > 0.01:
            r5_p_term = self.Kp * self.r5_error
            self.r5_error_sum += self.r5_error * 0.1
            r5_i_term = self.Ki * self.r5_error_sum
            r5_error_change = self.r5_error - self.r5_prev
            r5_d_term = self.Kd * r5_error_change / 0.1
            r5_angular_correction = r5_p_term + r5_i_term + r5_d_term
            r5_twist.angular.z = r5_angular_correction
        elif (self.active_robot == 0 or self.active_robot == 5) and self.last_angular_z != 0.0:
            r5_twist.angular.z = self.last_angular_z * 2.0
            self.r5_error_sum = 0.0
        else:
            r5_twist.angular.z = 0.0
            self.r5_error_sum = 0.0
        
        # Store previous errors for next cycle
        self.r1_prev = self.r1_error
        self.r2_prev = self.r2_error
        self.r3_prev = self.r3_error
        self.r4_prev = self.r4_error
        self.r5_prev = self.r5_error
        
        # Log info about currently controlled robot(s)
        if self.active_robot == 0:
            self.get_logger().debug("Controlling all robots")
        else:
            self.get_logger().debug(f"Controlling robot {self.active_robot}")
            
        # Log debugging info for active robots
        if self.active_robot == 0 or self.active_robot == 1:
            self.get_logger().debug(f"R1: speed={self.r1_speed:.2f}, error={self.r1_error:.2f}, angular={r1_twist.angular.z:.2f}")
        if self.active_robot == 0 or self.active_robot == 2:
            self.get_logger().debug(f"R2: speed={self.r2_speed:.2f}, error={self.r2_error:.2f}, angular={r2_twist.angular.z:.2f}")
        
        # Publish to all robots
        self.r1_vel_pub.publish(r1_twist)
        self.r2_vel_pub.publish(r2_twist)
        self.r3_vel_pub.publish(r3_twist)
        self.r4_vel_pub.publish(r4_twist)
        self.r5_vel_pub.publish(r5_twist)
    
    # Odometry callbacks to update current yaw and calculate error
    def r1_odom_callback(self, msg):
        self.r1_yaw = self.extract_yaw(msg)
        self.r1_error = self.normalize_angle(self.r1_target_yaw - self.r1_yaw)
    
    def r2_odom_callback(self, msg):
        self.r2_yaw = self.extract_yaw(msg)
        self.r2_error = self.normalize_angle(self.r2_target_yaw - self.r2_yaw)
    
    def r3_odom_callback(self, msg):
        self.r3_yaw = self.extract_yaw(msg)
        self.r3_error = self.normalize_angle(self.r3_target_yaw - self.r3_yaw)
    
    def r4_odom_callback(self, msg):
        self.r4_yaw = self.extract_yaw(msg)
        self.r4_error = self.normalize_angle(self.r4_target_yaw - self.r4_yaw)
    
    def r5_odom_callback(self, msg):
        self.r5_yaw = self.extract_yaw(msg)
        self.r5_error = self.normalize_angle(self.r5_target_yaw - self.r5_yaw)


def main(args=None):
    rclpy.init(args=args)
    node = TeleopPIDController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()