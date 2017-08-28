# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import pylab
from random import *
import eleventh_visualize

# === Provided classes

class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)
    def __str__(self):
        return 'X: {0}, Y: {1}'.format(self.getX(), self.getY())


# === Problems 1 and 2

class RectangularRoom(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cleaned = [[False] * width for i in range(height)]
    def cleanTileAtPosition(self, pos):
        self.cleaned[int(pos.getY())][int(pos.getX())] = True
        print self.cleaned
    def isTileCleaned(self, m, n):
        return self.cleaned[m][n]
    def getNumTiles(self):
        return self.width * self.height
    def getNumCleanedTiles(self):
        return len([True for x in range(self.width) for y in range(self.height) if self.cleaned[y][x]])
    def percentileCleaned(self):
        return float(self.getNumCleanedTiles()) / self.getNumTiles()
    def getRandomPosition(self):
        return Position(randrange(self.width), randrange(self.height))
    def isPositionInRoom(self, pos):
        return 0 <= pos.getX() < self.width and 0 <= pos.getY() < self.height

def random_angle():
    return randrange(360)

class BaseRobot(object):
    def __init__(self, room, speed):
        self.room = room
        self.speed = speed
        self.direction = random_angle()
        self.position = room.getRandomPosition()
    def getRoom(self):
        return self.room
    def getRobotPosition(self):
        return self.position
    def getRobotDirection(self):
        return self.direction
    def setRobotPosition(self, position):
        self.position = position
    def setRobotDirection(self, direction):
        self.direction = direction


class Robot(BaseRobot):
    def updatePositionAndClean(self):
        position = self.getRobotPosition()
        print 'cleanded', str(position)
        room = self.getRoom()
        room.cleanTileAtPosition(position)
        new_position = position.getNewPosition(self.direction, self.speed)
        if not room.isPositionInRoom(new_position):
            self.setRobotDirection(random_angle())
        else:
            self.setRobotPosition(new_position)


# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials, robot_type, visualize):
    stats = []
    for i in range(num_trials):
        trial = []
        room = RectangularRoom(width, height)
        robots = [robot_type(room, speed) for i in range(num_robots)]
        if visualize:
            anim = eleventh_visualize.RobotVisualization(num_robots, width, height)
        while room.percentileCleaned() < min_coverage:
            for robot in robots:
                robot.updatePositionAndClean()
            trial.append(room.percentileCleaned() * 100)
            if visualize:
                anim.update(room, robots)
        stats.append(trial)
        if visualize:
            anim.done()
    return stats

# === Provided function
def computeMeans(list_of_lists):
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means


# === Problem 4
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    # TODO: Your code goes here

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    # TODO: Your code goes here

def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    # TODO: Your code goes here

def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    # TODO: Your code goes here


# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    # TODO: Your code goes here


# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    # TODO: Your code goes here
