class DetectionSystem():
    def __init__(self, robot, imArray, collision_range):
        self.robot = robot
        self.imArray = imArray
        self.collision_range = collision_range
        self.collision_value = 0
    
    def get_collided_distance(self):
        print(len(self.imArray[0]))
        collision_point = (int(self.robot.detector_pos[0]), int(self.robot.detector_pos[1]))
        # just look up
        for ystep in range(0, 500):
            collision_point = (collision_point[0], collision_point[1] - 2)
            print(collision_point)
            # TODO: Whats going on with the xpos of the robot
            if collision_point[1] >= im_y or collision_point[1] <= 0:
                print("End of Map reached")
                break
            
            value_in_array = self.imArray[collision_point[1]][collision_point[0]] # TODO: Check me out     
            if value_in_array == self.collision_value:
                print("Collided")
                print(self.robot.detector_pos)
                print(self.robot.getDistance(collision_point))
                break   
        return