import rclpy
from rclpy.node import Node

from custom_interfaces.msg import Waypoint


class WaypointPublisher(Node):

    def __init__(self):
        super().__init__('waypoint_publisher')
        self.publisher_ = self.create_publisher(Waypoint, 'global_waypoint', 1)
        
        ONE_SECOND = 1
        self.timer = self.create_timer(ONE_SECOND, self.waypoint_callback)

    def waypoint_callback(self):
        wp = Waypoint()
        wp.x, wp.y, wp.z, wp.radius = 25, 25, 0, 2
        print(wp)
        self.publisher_.publish(wp)


def main(args=None):
    rclpy.init(args=args)

    waypoint_publisher = WaypointPublisher()

    rclpy.spin(waypoint_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    waypoint_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
