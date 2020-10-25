import math

class Robot():
    def __init__(self, pos):
        self.pos = pos
        self.size = (10, 10)
        self.rotation = 0 # 0 - 360
        self.detector_pos = self.pos #(self.pos[0], self.pos[1] - (self.size[1] / 2) - 3)
        self.range = 1000
        self.detection_points = [self.pos]

    def set_detector_pos(self):
        self.detector_pos = self.pos #(self.pos[0], self.pos[1] - (self.size[1] / 2) - 3)

    def set_detection_point(self):
        self.detection_point = [(self.pos[0], self.pos[1] - self.range)]

    def getDistance(self, point):
        x1 = self.pos[0]
        y1 = self.pos[1]
        x2 = point[0]
        y2 = point[1]
        return math.hypot(x2 - x1, y2 - y1)

    def contruct_arrays(self):
        self.set_detection_point()
        for deg in range(1, 360):
            self.detection_points.append(self.rotate(self.detector_pos, self.detection_points[0], math.radians(deg)))
        return

    def rotate(self, origin, point, angle):
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return (int(qx), int(qy))

    def drive(self):
        #TODO: DRIIIVE
        return
            
    def get_distance_from_detection_points(self):
        return [math.dist(self.pos, detection_point) for detection_point in self.detection_points]