# Ein Range finden, der den ganzen Raum erfasst
# Transformiere Pixel-Werte in richtigen Ranges

import random
import math
import json
import codecs

from robot import Robot
from image_generator import ImageGenerator
from image_analyzer import ImageAnalyzer
from shapely.geometry import Point, Polygon, LineString

from PIL import Image, ImageDraw
import numpy as np

np.set_printoptions(threshold=np.inf)

# Image Size
im_x = 1920
im_y = 1080

## Draw in two different colors (drivable/non-driveable) and background color
wall_col = "#000000" #black
floor_col = "#FFFFFF" #white
back_col = "#808080" #gray

# TODO:
# set random "realistic" door pos
# random room size

# place random objects in a room

class Layout:
    def __init__(self, size, roomcount):
        # init all necessary values
        self.size = size # (1920, 1080)
        self.roomcount = roomcount
        self.robot = None

        # Apartement
        self.rooms = []
        self.objects = []
        # Generate Rooms
        for x in range(roomcount):
            self.createRoom(x)

        self.get_interference()

    def createRoom(self, id):
        print("Create Room")
        # Define size of room - TODO: Random should be possible
        room_w = random.randint(200, 300)
        room_h = random.randint(200, 300)
        newRoom = Room(id, self.calcLayoutCenter(), room_w, room_h)

        if not self.rooms:
            self.rooms.append(newRoom)
            return

        # Check for availible space
        space_tuple = self.getRandomSpaceFromList(self.getAvailibleSpaces())
        room = self.getRoomById(space_tuple[0])

        # Set adjacentSpace to True if space is targeted
        room.adjacentRooms[space_tuple[1]] = True
        newRoom.adjacentRooms[self.getOppositeSide(space_tuple[1])] = True
        
        # Check out of bonds and interference
        newRoom.calcCenter(room, space_tuple[1])
        newRoom.calcCoordinates()
        if(not self.InBoundsCheck(newRoom)):
            return

        if(self.intersectCheck(space_tuple[1], newRoom)):
            return

        # TODO: place random objects if wanted
        # Robot
        robo_room = self.getRandomRoom()
        self.robot = Robot((0, 0))
        self.robot.pos = robo_room.getRandomPosInRoom(self.robot.size)
        self.robot.set_detector_pos()
        self.robot.set_detection_point()
        self.robot.contruct_arrays()

        # Room Objects
        objRoom = self.getRandomRoom()
        roomObj = RoomObject()
        roomObj.pos = objRoom.getRandomPosInRoom(roomObj.size)
        self.objects.append(roomObj)

        objRoom = self.getRandomRoom()
        roomObj = RoomObject()
        roomObj.pos = objRoom.getRandomPosInRoom(roomObj.size)
        self.objects.append(roomObj)

        objRoom = self.getRandomRoom()
        roomObj = RoomObject()
        roomObj.pos = objRoom.getRandomPosInRoom(roomObj.size)
        self.objects.append(roomObj)

        objRoom = self.getRandomRoom()
        roomObj = RoomObject()
        roomObj.pos = objRoom.getRandomPosInRoom(roomObj.size)
        self.objects.append(roomObj)


        # Set Adjacent Room to true
        self.rooms.append(newRoom)   
        return

    def getOppositeSide(self, id):
        return (id - 2) % 4


    def getRoomById(self, id):
        for room in self.rooms:
            if room.id == id:
                return room

        return None

    def getRandomRoom(self):
        room = self.rooms[random.randint(0, len(self.rooms) - 1)]
        return room

    def getRandomSpaceFromList(self, spaceList):
        ranNum = random.randint(0, len(spaceList) - 1)
        return spaceList[ranNum]


    def getAvailibleSpaces(self):
        availibleList = []
        for room in self.rooms:
            adjacentList = [(room.id, adjacent_index) for adjacent_index, adjacent in enumerate(room.adjacentRooms) if adjacent == False]
            availibleList = availibleList + adjacentList

        print(availibleList)
        return availibleList

    def checkForAvailibleSpace(self, newRoom):
        #return self.calcNewRoomCenter(room, 0, newRoom)
        # if interference with another room
        # if boundary is reached
        return

    def InBoundsCheck(self, room):
        upper_left_x = room.central_xy[0] - (room.width / 2)
        upper_left_y = room.central_xy[1] - (room.height / 2)
        lower_right_x = room.central_xy[0] + (room.width / 2)
        lower_right_y = room.central_xy[1] + (room.height / 2)
        if (upper_left_x < 0 or upper_left_y < 0):
            print("Out of Bounds")
            return False

        if (lower_right_x > im_x or lower_right_y > im_y):
            print("Out of Bounds")
            return False

        return True

    def intersectCheck(self, adjacent, newRoom):
        newRoomPoly = Polygon((newRoom.upper_left_xy, newRoom.lower_left_xy, newRoom.lower_right_xy, newRoom.upper_right_xy))
        # Check up, right, down, left
        for room in self.rooms:
            roomPoly = Polygon((room.upper_left_xy, room.lower_left_xy, room.lower_right_xy, room.upper_right_xy))
            if(newRoomPoly.intersects(roomPoly)):
                print("Intersect")
                return True

        return False

    # robot to walls
    def get_interference(self):
        # check for all walls
        for key, detection_point in enumerate(self.robot.detection_points):
            ray = [self.robot.pos, detection_point]
            closest = None
            record = 9999999
            # For every room
            for room in self.rooms:
                for wall in room.get_walls():
                    val = self.interference_check(wall, ray)
                    if val is not None:
                        distance = math.dist(self.robot.pos, val)
                        if distance < record:
                            record = distance
                            closest = val
                        
            # for every object
            for obj in self.objects:
                for hb in obj.get_hitbox():
                    val = self.interference_check(hb, ray)
                    if val is not None:
                        distance = math.dist(self.robot.pos, val)
                        if distance < record:
                            record = distance
                            closest = val


            if closest:
                self.robot.detection_points[key] = closest
        return 

    def interference_check(self, line1, line2):
        x1 = line1[0][0]
        y1 = line1[0][1]
        x2 = line1[1][0]
        y2 = line1[1][1]

        x3 = line2[0][0]
        y3 = line2[0][1]
        x4 = line2[1][0]
        y4 = line2[1][1]

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        
        if (t > 0 and t < 1 and u > 0):
            inter_x = x1 + t * (x2 - x1)
            inter_y = y1 + t * (y2 - y1)
            return (inter_x, inter_y)
        else:
            return

    # room which the new room is placed next to

    def calcLayoutCenter(self):
        return (self.size[0] / 2, self.size[1] / 2)

    def respawn_robot_and_calc_distances(self):
        # Respawn Robot
        robo_room = self.getRandomRoom()
        self.robot = Robot((0, 0))
        self.robot.pos = robo_room.getRandomPosInRoom(self.robot.size)
        self.robot.set_detector_pos()
        self.robot.set_detection_point()
        self.robot.contruct_arrays()

        # calc new ray distances
        
        self.get_interference()
        return 


class Room:
    def __init__(self, id, central_xy, width, height, wallWidth = 1):
        self.id = id
        self.central_xy = central_xy
        self.width = width
        self.height = height

        self.upper_left_xy = [self.central_xy[0] - ((self.width-1) / 2), self.central_xy[1] - ((self.height-1) / 2)]
        self.upper_right_xy = [self.central_xy[0] + ((self.width-1)  / 2), self.central_xy[1] - ((self.height-1) / 2)]
        self.lower_left_xy = [self.central_xy[0] - ((self.width-1)  / 2), self.central_xy[1] + ((self.height-1) / 2)]
        self.lower_right_xy = [self.central_xy[0] + ((self.width-1) / 2), self.central_xy[1] + ((self.height-1) / 2)]

        self.wallWidth = wallWidth
        self.doorSize = 20
        self.doorToWall = 10
        self.adjacentRooms = [False] * 4 # 0 - up, 1 - right, 2 - down, 3 - right

    def calcCoordinates(self):
        self.upper_left_xy = [self.central_xy[0] - ((self.width-1) / 2), self.central_xy[1] - ((self.height-1) / 2)]
        self.upper_right_xy = [self.central_xy[0] + ((self.width-1)  / 2), self.central_xy[1] - ((self.height-1) / 2)]
        self.lower_left_xy = [self.central_xy[0] - ((self.width-1)  / 2), self.central_xy[1] + ((self.height-1) / 2)]
        self.lower_right_xy = [self.central_xy[0] + ((self.width-1) / 2), self.central_xy[1] + ((self.height-1) / 2)]

    def get_walls(self):
        walls = []
        doorPos = self.central_xy # TODO: Random door position
        if self.adjacentRooms[0] == True:
            doorPos = [self.central_xy[0], self.upper_left_xy[1]]
            walls.append([self.upper_left_xy, [doorPos[0] - self.doorSize, doorPos[1]]])
            walls.append([[doorPos[0] + self.doorSize, doorPos[1]], self.upper_right_xy])
        else:
            walls.append([self.upper_left_xy, self.upper_right_xy])

        if self.adjacentRooms[1] == True:
            doorPos = (self.lower_right_xy[0], self.central_xy[1])
            walls.append([self.upper_right_xy, [doorPos[0], doorPos[1] - self.doorSize]])
            walls.append([[doorPos[0], doorPos[1]  + self.doorSize], self.lower_right_xy])
        else:
            walls.append([self.upper_right_xy, self.lower_right_xy])

        if self.adjacentRooms[2] == True:
            doorPos = (self.central_xy[0], self.lower_left_xy[1])
            walls.append([self.lower_left_xy, [doorPos[0] - self.doorSize, doorPos[1]]])
            walls.append([[doorPos[0] + self.doorSize, doorPos[1]], self.lower_right_xy])
        else:
            walls.append([self.lower_left_xy, self.lower_right_xy])

        if self.adjacentRooms[3] == True:
            doorPos = (self.upper_left_xy[0], self.central_xy[1])
            walls.append([self.upper_left_xy, [doorPos[0], doorPos[1] - self.doorSize]])
            walls.append([[doorPos[0], doorPos[1]  + self.doorSize], self.lower_left_xy])
        else:
            walls.append([self.upper_left_xy, self.lower_left_xy])

        # walls.append((self.upper_left_xy, self.upper_right_xy))
        # walls.append((self.upper_right_xy, self.lower_right_xy))
        # walls.append((self.lower_left_xy, self.lower_right_xy))
        # walls.append((self.upper_left_xy, self.lower_left_xy))

        return walls

    

    def calcCenter(self, room, adjId):
        if adjId == 0: # Up
            self.central_xy = (room.central_xy[0], room.central_xy[1] - ((room.height / 2) + (self.height / 2)))
        elif adjId == 1: # Right
            self.central_xy = (room.central_xy[0] + ((room.width / 2) + (self.width / 2)), room.central_xy[1])
        elif adjId == 2: # Down
            self.central_xy = (room.central_xy[0], room.central_xy[1] + ((room.height / 2) + (self.height / 2)))
        elif adjId == 3: # Left
            self.central_xy = (room.central_xy[0] - ((room.width / 2) + (self.width / 2)), room.central_xy[1])

    def getRandomPosInRoom(self, objSize):
        x_a = self.lower_left_xy[0] + objSize[0]
        x_b = self.upper_right_xy[0] - objSize[0]
        y_a = self.lower_left_xy[1] + objSize[1]
        y_b = self.upper_right_xy[1] + objSize[1]

        if x_a >= im_x:
            x_a = im_x

        if x_b >= im_x:
            x_b = im_x

        # TODO: check if object size isn't bigger as the room itself
        # TODO: check if object is already placed in objSize-Area
        #print("x_a: {x_a1}, x_b: {x_b1}".format(x_a1 = x_a, x_b1 = x_b))
        #print("y_a: {y_a1}, y_b: {y_b1}".format(y_a1 = y_a, y_b1 = y_b))
        random_x = random.randint(int(x_a), int(x_b))
        random_y = random.randint(int(y_b), int(y_a))
        return (random_x, random_y)

    def resize(self, minmaxWidth, minmaxHeight):
        #TODO: Set Random size
        self.width = 0
        self.height = 0
        return

    def setDoorArea(self):
        # TODO: Define corner to door range
        return

class RoomObject:
    def __init__(self):
        self.prop = "chair"
        self.pos = (0, 0)
        self.size = (15, 15)

    def setPos(self, range):
        self.pos = (0, 0)

    def get_hitbox(self):
        return [
            ((self.pos[0] - (self.size[0] / 2), self.pos[1] - (self.size[1] / 2)), (self.pos[0] + (self.size[0] / 2), self.pos[1] - (self.size[1] / 2))), # up
            ((self.pos[0] - (self.size[0] / 2), self.pos[1] - (self.size[1] / 2)), (self.pos[0] - (self.size[0] / 2), self.pos[1] + (self.size[1] / 2))), # left
            ((self.pos[0] + (self.size[0] / 2), self.pos[1] - (self.size[1] / 2)), (self.pos[0] + (self.size[0] / 2), self.pos[1] + (self.size[1] / 2))), # right
            ((self.pos[0] + (self.size[0] / 2), self.pos[1] + (self.size[1] / 2)), (self.pos[0] - (self.size[0] / 2), self.pos[1] + (self.size[1] / 2))), # down
        ]

def write_results(results, filename):
    f = open(filename + ".txt", "a")
    f.write(results)
    f.close()

def write_results_json(results, filename):
    # if type(results) is "ndarray":
    results = results.tolist() # from ndarray to list
    json_file = "{name}.json".format(name=filename)
    json.dump(results, codecs.open(json_file, 'w', encoding='utf_8'), indent=4)

def write_map_results_json(results, filename):
    json_file = "{name}.json".format(name=filename)
    json.dump(results, codecs.open(json_file, 'w', encoding='utf_8'), indent=4)


def generate_distances(times, filename):
    result_json = {
        'robot_pos': [],
        'distances': []
    }
    for i in range(0, times):
        # write them down
        layout.respawn_robot_and_calc_distances()
        result_json['robot_pos'].append(layout.robot.pos)
        result_json['distances'].append(layout.robot.get_distance_from_detection_points())

    write_map_results_json(result_json, filename)
        # write_results((str(layout.robot.pos)), "results2")
        # write_results(str(layout.robot.get_distance_from_detection_points()), "results2")


# Room Props
room_minmaxHeight = (30, 100)
room_minmaxWidth = (30, 100)


# Smol Room

# layout = Layout((1920, 1080), 3)
# #print(len(layout.robot.get_distance_from_detection_points()))

# imGen = ImageGenerator(layout, back_col)
# result_image = imGen.draw_image()
# write_results_json(result_image, "smol_map")

# generate_distances(50000, "smol_map_results")

# Big Room
layout = Layout((1920, 1080), 10)

imGen = ImageGenerator(layout, back_col)
result_image = imGen.draw_image()
write_results_json(result_image, "big_map_with_obstacles")

generate_distances(50000, "big_map_with_obstacles_results")
# imGen.show_image()

# for i in range(0, 50000):
#     # write them down
#     layout.respawn_robot_and_calc_distances()
#     write_results((str(layout.robot.pos)), "results3")
#     write_results(str(layout.robot.get_distance_from_detection_points()), "results3")


# for i in range(11, 20):
#     layout.respawn_robot_and_calc_distances()
#     result_image = imGen.draw_image(i)
    # imGen.show_image()


# Analyzing the corners
# imAna = ImageAnalyzer(imGen.draw_image())
# imGen.show_image()
# imAna.get_corners()
# imGen.draw_more(imAna.corners)
# imGen.show_image()
# write_results(str(np.transpose(imGen.draw_image())), "map2")


