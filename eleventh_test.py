from eleventh import *

def test_rect_room_init():
    room = RectangularRoom(2, 3)
    assert room.getNumTiles() == 6
    assert room.isTileCleaned(0, 0) == False
    assert room.isPositionInRoom(Position(0, 1)) == True
    assert room.isPositionInRoom(Position(0, 3)) == False

def test_rect_room_clean_tile():
    room = RectangularRoom(2, 1)
    room.cleanTileAtPosition(Position(0, 0))
    assert room.isTileCleaned(0, 0) == True
    assert room.getNumCleanedTiles() == 1

def test_robot_clean_and_update():
    room = RectangularRoom(6, 6)
    robot = Robot(room, 1)
    robot.updatePositionAndClean()
    assert room.getNumCleanedTiles() == 1

def test_simple_simulation():
    avg_ticks = average(runSimulation(1, 1, 10, 10, .9, 10, Robot, False))
    assert avg_ticks <= 360
    assert avg_ticks >= 250

def test_random_walk_robot():
    avg_ticks = average(runSimulation(1, 1, 10, 10, .9, 10, RandomWalkRobot, False))
    assert avg_ticks <= 900
    assert avg_ticks >= 500
