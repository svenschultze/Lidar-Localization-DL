import random
import math

from PIL import Image, ImageDraw
import numpy as np

# Image Size
im_x = 1920
im_y = 1080

## Draw in two different colors (drivable/non-driveable) and background color
wall_col = "#000000" #black
floor_col = "#FFFFFF" #white
back_col = "#808080" #gray
mark_col = "#008000" # green


class ImageGenerator:
    def __init__(self, layout, backgroundColor):
        self.layout = layout
        self.backgroundColor = backgroundColor
        self.image = None
        self.draw = None
    
    def draw_image(self):
        print("Start Drawing")
        # Use Layout for Room Data
        rooms = self.layout.rooms
        im_x = self.layout.size[0]
        im_y = self.layout.size[1]

        # Define Image-Area
        im = Image.new("RGB", (im_x, im_y), back_col)
        # Drawing
        self.draw = ImageDraw.Draw(im)

        for room in rooms:
            # Draw Doors at the end
            center = room.central_xy
            # Draws the floor
            upper_left_x = center[0] - (room.width / 2)
            upper_left_y = center[1] - (room.height / 2)
            lower_right_x = center[0] + (room.width / 2)
            lower_right_y = center[1] + (room.height / 2)

            self.draw.rectangle((upper_left_x,
                            upper_left_y,
                            lower_right_x,
                            lower_right_y),
                            fill=floor_col,
                            width=room.wallWidth,
                            outline=wall_col) #(Upper left x coordinate, upper left y coordinate, lower right x coordinate, lower right y coordinate)
            
            # Draws doors
            for index, adj in enumerate(room.adjacentRooms):
                if adj == True:
                    doorPos = room.central_xy
                    if index == 0: # up
                        doorPos = (center[0], upper_left_y)
                        self.draw.line((doorPos[0] - room.doorSize, doorPos[1], doorPos[0] + room.doorSize, doorPos[1]), fill=floor_col)
                    elif index == 1: # right
                        doorPos = (lower_right_x, center[1])
                        self.draw.line((doorPos[0], doorPos[1] - room.doorSize, doorPos[0], doorPos[1] + room.doorSize), fill=floor_col)
                    elif index == 2: # down
                        doorPos = (center[0], lower_right_y)
                        self.draw.line((doorPos[0] - room.doorSize, doorPos[1], doorPos[0] + room.doorSize, doorPos[1]), fill=floor_col)
                    elif index == 3: # left
                        doorPos = (upper_left_x, center[1])
                        self.draw.line((doorPos[0], doorPos[1] - room.doorSize, doorPos[0], doorPos[1] + room.doorSize), fill=floor_col)

            # Draw Objects
            if self.layout.robot is not None:
                robot = self.layout.robot
                self.draw.ellipse((robot.pos[0] - (robot.size[0] / 2),
                                robot.pos[1] - (robot.size[1] / 2),
                                robot.pos[0] + (robot.size[0] / 2),
                                robot.pos[1] + (robot.size[1] / 2)),
                                fill=back_col,
                                width=room.wallWidth,
                                outline=back_col)

                self.draw.rectangle((robot.detector_pos[0] - 1,
                                robot.detector_pos[1] - 1,
                                robot.detector_pos[0] + 1,
                                robot.detector_pos[1] + 1),
                                fill=wall_col,
                                width=0,
                                outline=wall_col)


                print(robot.detector_pos)
                print(robot.detection_point)
                for point in range(0, len(robot.detection_points)):
                    self.draw.line((robot.detector_pos[0],
                            robot.detector_pos[1],
                            robot.detection_points[point][0],
                            robot.detection_points[point][1]),
                            fill=wall_col,
                            width=0)


            for obj in self.layout.objects:
                self.draw.rectangle((obj.pos[0] - (obj.size[0] / 2),
                                obj.pos[1] - (obj.size[1] / 2),
                                obj.pos[0] + (obj.size[0] / 2),
                                obj.pos[1] + (obj.size[1] / 2)),
                                fill=wall_col,
                                width=room.wallWidth,
                                outline=wall_col)


        new_array = np.asarray(im)[:, :, 0]
        print(len(new_array))
        #self.get_corners(new_array)
        self.image = im
        return new_array

    def show_image(self):
        self.image.show()

    def draw_more(self, pos_array):
        for dot in pos_array:
            self.draw.rectangle((dot[0] - 1,
                                    dot[1] - 1,
                                    dot[0] + 1,
                                    dot[1] + 1),
                                    fill=mark_col,
                                    width=1,
                                    outline=mark_col)
        
