import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

import math


class MultiRobotVelocityPublisher(Node):
    def __init__(self):
        super().__init__('multi_robot_cmd_vel_publisher')

        self.robot_namespaces = ["robot1", "robot2", "robot3", "robot4", "robot5"]

        self.r1_vel_pub = self.create_publisher(Twist, '/robot1/cmd_vel', 10)
        self.r2_vel_pub = self.create_publisher(Twist, '/robot2/cmd_vel', 10)
        self.r3_vel_pub = self.create_publisher(Twist, '/robot3/cmd_vel', 10)
        self.r4_vel_pub = self.create_publisher(Twist, '/robot4/cmd_vel', 10)
        self.r5_vel_pub = self.create_publisher(Twist, '/robot5/cmd_vel', 10)

        self.r1_odom_sub = self.create_subscription(Odometry, '/robot1/odom', self.r1_odom_callback, 10)
        self.r2_odom_sub = self.create_subscription(Odometry, '/robot2/odom', self.r2_odom_callback, 10)
        self.r3_odom_sub = self.create_subscription(Odometry, '/robot3/odom', self.r3_odom_callback, 10)
        self.r4_odom_sub = self.create_subscription(Odometry, '/robot4/odom', self.r4_odom_callback, 10)
        self.r5_odom_sub = self.create_subscription(Odometry, '/robot5/odom', self.r5_odom_callback, 10)

        self.r1_yaw = 0.0
        self.r2_yaw = 0.0
        self.r3_yaw = 0.0
        self.r4_yaw = 0.0
        self.r5_yaw = 0.0

        self.yaw = [0.0]*5

        self.robot_poses = [[0.0,0.0] for i in range(5)]
        self.robot_states = ["1"]*5 #state 1

        self.target_x = [20.0]*5
        self.target_y = [-36.0,-18.0,0.0,18.0,36.0]

        # self.r1_target_yaw = 0.0
        # self.r2_target_yaw = 0.0
        # self.r3_target_yaw = 0.0
        # self.r4_target_yaw = 0.0
        # self.r5_target_yaw = 0.0

        self.target_yaw = [0.0]*5

        # self.r1_error = 0.0
        # self.r2_error = 0.0
        # self.r3_error = 0.0
        # self.r4_error = 0.0
        # self.r5_error = 0.0

        self.error = [0.0]*5

        self.prev = [0.0]*5

        # self.r1_prev = 0.0
        # self.r2_prev = 0.0
        # self.r3_prev = 0.0
        # self.r4_prev = 0.0
        # self.r5_prev = 0.0

        self.speed = [0.4]*5

        self.Kp = 18.0
        self.Ki = 0.5
        self.Kd = 1.0

        self.timer = self.create_timer(0.1, self.fsm_update)
        self.timer = self.create_timer(0.1, self.publish_cmd_vel)

    def yaw_calc(self, msg):
        x = msg.pose.pose.orientation.x
        y = msg.pose.pose.orientation.y 
        z = msg.pose.pose.orientation.z 
        w = msg.pose.pose.orientation.w 
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return yaw

    def publish_cmd_vel(self):
        twists = [Twist() for _ in range(5)]
        publishers = [self.r1_vel_pub, self.r2_vel_pub, self.r3_vel_pub, self.r4_vel_pub, self.r5_vel_pub]
        
        # Initialize error_sum array if it doesn't exist
        if not hasattr(self, 'error_sum'):
            self.error_sum = [0.0] * 5
        
        for i in range(5):
            if self.error[i] < -1.0:
                self.error[i] = 1.0
            elif self.error[i] > 1.0:
                self.error[i] = 1.0

        for i in range(5):
            # Set linear speed
            twists[i].linear.x = self.speed[i]
            
            # Calculate PID terms
            p_term = self.Kp * self.error[i]
            
            self.error_sum[i] += self.error[i] * 0.1  # 0.1 is the timer period
            i_term = self.Ki * self.error_sum[i]
            
            error_change = self.error[i] - self.prev[i]
            d_term = self.Kd * error_change / 0.1  # 0.1 is the timer period
            

            angular_correction = p_term + i_term + d_term
            if angular_correction > 2.0:
                angular_correction = 2.0
            elif angular_correction < -2.0:
                angular_correction = -2.0

            twists[i].angular.z = angular_correction
            
            # self.get_logger().info(f"Robot {i+1} correction: {angular_correction}, error: {self.error[i]}")

            # publishers[i].publish(twists[i])
            self.r1_vel_pub.publish(twists[0])
            self.r2_vel_pub.publish(twists[1])
            self.r3_vel_pub.publish(twists[2])
            self.r4_vel_pub.publish(twists[3])
            self.r5_vel_pub.publish(twists[4])

    #P term is error
    #I term is sum of error
    #D term is diff of error
    def fsm_update(self):

        for i in range(5):
            x = self.robot_poses[i][0]
            y = self.robot_poses[i][1]
            if self.robot_states[i] == '1' and abs(x - self.target_x[i])<0.5:
                self.robot_states[i] = '2'
                self.speed[i] = 0.0
                self.target_yaw[i] = - math.pi/2
                self.error_sum[i] = 0.0
                # self.target_y = y + 15.0
            elif self.robot_states[i] == '2' and abs(self.error[i]) < 0.5:
                self.robot_states[i] = '3'
                self.speed[i] = 0.4
                self.target_y[i] = y - 15.0
                self.error_sum[i] = 0.0
            elif self.robot_states[i] == '3' and abs(y - self.target_y[i])<0.5:
                self.robot_states[i] = '4'
                self.speed[i] = 0.0
                self.target_yaw[i] = math.pi
                self.error_sum[i] = 0.0
            elif self.robot_states[i] == '4' and abs(self.error[i]) < 0.4:
                self.robot_states[i] = '5'
                self.speed[i] = 0.4
                self.target_x[i] = x - 20.0
                self.error_sum[i] = 0.0
            elif self.robot_states[i] == '5' and abs(x - self.target_x[i])<1.5:
                self.error[i] = 0
                self.prev[i] = 0
                self.robot_states[i] = '6'
                self.speed[i] = 0.0
                self.target_yaw[i] = math.pi/2
                self.error_sum[i] = 0.0
            elif self.robot_states[i] == '6' and abs(self.error[i])<0.5:
                self.robot_states[i] = '7'
                self.speed[i] = 0.4
                self.target_y[i] = y + 15.0
                self.error_sum[i] = 0.0
            elif self.robot_states[i] == '7' and abs(y - self.target_y[i])<0.5:
                self.robot_states[i] = '8'
                self.speed[i] = 0.0
                self.target_yaw[i] = 0.0
                self.error_sum[i] = 0.0
            elif self.robot_states[i] == '8' and abs(self.error[i])<0.5:
                self.robot_states[i] = '1'
                self.speed[i] = 0.4
                self.target_x[i] = x + 20.0 
                self.error_sum[i] = 0.0

            if self.robot_states[i] == '5':
                self.get_logger().info(f"{abs(x-self.target_x[i])}")

    def r1_odom_callback(self, msg):
        self.yaw[0] = self.yaw_calc(msg)
        self.robot_poses[0][0] = msg.pose.pose.position.x
        self.robot_poses[0][1] = msg.pose.pose.position.y
        # self.get_logger().info(f"r1 yaw = {self.r1_yaw}")
        self.prev[0] = self.error[0]
        self.error[0] = self.target_yaw[0] - self.yaw[0]
        # self.r1_prev = self.r1_error
        # self.r1_error = self.r1_target_yaw - self.r1_yaw


    def r2_odom_callback(self, msg):
        self.yaw[1] = self.yaw_calc(msg)
        self.robot_poses[1][0] = msg.pose.pose.position.x
        self.robot_poses[1][1] = msg.pose.pose.position.y
        # self.get_logger().info(f"r2 yaw = {self.r2_yaw}")
        self.prev[1] = self.error[1]
        self.error[1] = self.target_yaw[1] - self.yaw[1]

    def r3_odom_callback(self, msg):
        self.yaw[2] = self.yaw_calc(msg)
        self.robot_poses[2][0] = msg.pose.pose.position.x
        self.robot_poses[2][1] = msg.pose.pose.position.y
        # self.get_logger().info(f"r2 yaw = {self.r2_yaw}")
        self.prev[2] = self.error[2]
        self.error[2] = self.target_yaw[2] - self.yaw[2]

    def r4_odom_callback(self, msg):
        self.yaw[3] = self.yaw_calc(msg)
        self.robot_poses[3][0] = msg.pose.pose.position.x
        self.robot_poses[3][1] = msg.pose.pose.position.y
        # self.get_logger().info(f"r2 yaw = {self.r2_yaw}")
        self.prev[3] = self.error[3]
        self.error[3] = self.target_yaw[3] - self.yaw[3]

    def r5_odom_callback(self, msg):
        self.yaw[4] = self.yaw_calc(msg)
        self.robot_poses[4][0] = msg.pose.pose.position.x
        self.robot_poses[4][1] = msg.pose.pose.position.y
        # self.get_logger().info(f"r2 yaw = {self.r2_yaw}")
        self.prev[4] = self.error[4]
        self.error[4] = self.target_yaw[4] - self.yaw[4]


def main(args=None):
    rclpy.init(args=args)
    node = MultiRobotVelocityPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()