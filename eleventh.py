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

def average(stats):
    return sum([len(s) for s in stats]) / len(stats)

# === Problem 4
def showPlot1():
    pylab.title('Time to clean 75% of a square room with 1 robot, for various room sizes at speed 1')
    pylab.xlabel('Room Area')
    pylab.ylabel('Timesteps')
    rooms = [(5, 5), (10, 10), (20, 20), (25, 25)]
    times = [average(runSimulation(1, 1, width, height, 0.75, 10, Robot, False)) for width, height in rooms]
    areas = [width * height for width, height in rooms]
    pylab.plot(areas, times)
    pylab.show()

def showPlot2():
    pylab.title('Time to clean 75% of a 25 x 25 room with 1 to 10 robots')
    pylab.xlabel('Robots')
    pylab.ylabel('Timesteps')
    robots = range(1, 11)
    times = [average(runSimulation(num_robots, 1, 25, 25, 0.75, 10, Robot, False)) for num_robots in robots]
    pylab.plot(robots, times)
    pylab.show()

def showPlot3():
    pylab.title('Time to clean 75% of room with 2 robots, for various width to height ratios')
    pylab.xlabel('Width/Height')
    pylab.ylabel('Timesteps')
    rooms = [(20, 20), (25, 16), (40, 10), (80, 5), (100, 4)]
    times = [average(runSimulation(2, 1, width, height, 0.75, 10, Robot, False)) for width, height in rooms]
    ratios = [width * 1.0 / height for width, height in rooms]
    pylab.plot(ratios, times)
    pylab.show()

def times_for(values):
    return range (1, len(values) + 1)

def showPlot4():
    pylab.title('Time to clean 25 x 25 room with 1 to 5 robots')
    pylab.xlabel('Percentage cleaned')
    pylab.ylabel('Timesteps')
    robots = range(1, 6)
    means = [computeMeans(runSimulation(num_robots, 1, 25, 25, 1, 10, Robot, False)) for num_robots in robots]
    current_robots = 1
    for mean in means:
        pylab.plot(mean, times_for(mean), label='{0} robots'.format(current_robots))
        current_robots += 1
    pylab.legend(loc=1)
    pylab.show()

# === Problem 5

class RandomWalkRobot(BaseRobot):
    def updatePositionAndClean(self):
        position = self.getRobotPosition()
        room = self.getRoom()
        room.cleanTileAtPosition(position)
        direction = random_angle()
        self.setRobotDirection(direction)
        new_position = position.getNewPosition(direction, self.speed)
        if room.isPositionInRoom(new_position):
            self.setRobotPosition(new_position)

# === Problem 6
'''
Much bigger fluctuations can be observed in random walk robot and it takes much longer to clean the room fully
'''
def showPlot5():
    pylab.title('Random vs Simple robot to clean 25 x 25 room')
    pylab.xlabel('Percentage cleaned')
    pylab.ylabel('Timesteps')
    mean_random = computeMeans(runSimulation(1, 1, 25, 25, 1, 10, RandomWalkRobot, False))
    mean_simple = computeMeans(runSimulation(1, 1, 25, 25, 1, 10, Robot, False))
    pylab.plot(mean_random, times_for(mean_random), label='Random')
    pylab.plot(mean_simple, times_for(mean_simple), label='Simple')
    pylab.legend(loc=1)
    pylab.show()

