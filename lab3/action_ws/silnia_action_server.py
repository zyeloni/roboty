import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from action_tutorials_interfaces.action import Fibonacci
import time


class FibonacciActionServer(Node):
    def __init__(self):
        self.bufor = {}
        super().__init__('silniai_action_server')
        self._action_server = ActionServer(self,Fibonacci,'silnia',self.execute_callback)

    def silnia(self,n):
        if n > 1:
            return n*self.silnia(n-1)
        return 1

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = []
        
        for i in range(0, goal_handle.request.order):
            if i not in self.bufor or i == goal_handle.request.order - 1:
                temp = self.silnia(i)
                self.bufor[i] = temp
                feedback_msg.partial_sequence.append(temp)
                self.get_logger().info('Feedback:{0}'.format(feedback_msg.partial_sequence))
                goal_handle.publish_feedback(feedback_msg)

            time.sleep(1)
            
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)
if __name__ == '__main__':
    main()