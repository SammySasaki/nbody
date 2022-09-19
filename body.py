class Body:
    def __init__(self, x, y, mass, radius, xspd, yspd):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.xspd = xspd
        self.yspd = yspd
        self.xacc = 0
        self.yacc = 0

    # update body position based on timestep dt and current speed/acceleration
    def update(self, dt):
        self.xspd = self.xspd + self.xacc * dt
        self.yspd = self.yspd + self.yacc * dt
        self.x = self.x + self.xspd * dt
        self.y = self.y + self.yspd * dt

    # setter for acceleration
    def setAcc(self, xacc, yacc):
        self.xacc = xacc
        self.yacc = yacc

    # getter for position
    def getPos(self):
        return (self.x, self.y)

    # getter for mass
    def getMass(self):
        return self.mass

    #getter for radius
    def getRadius(self):
        return self.radius
