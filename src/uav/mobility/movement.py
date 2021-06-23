
class Movement:


    def __init__(self):
        self.startPosX = 0
        self.startPosY = 0
        self.lastPosX = 0
        self.lastPosY = 0
        self.startTime = 0
        self.orientationX = 0
        self.orientationY = 0
        self.directionY = 0
        self.directionX = 0
        self.speed = 0
        pass

    def setStart(self, startPosX, startPosY, startTime):
        self.startPosX = startPosX
        self.startPosY = startPosY
        self.startTime = startTime

    def setDirectionByTarget(self, targetX, targetY):
        self.directionX = targetX - startPosX
        self.directionY = targetY - startPosY

        direction /= direction.length();
