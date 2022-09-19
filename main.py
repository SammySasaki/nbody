from body import Body
from utils import G, deltaTime, softening_factor
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox, Button



# stores all bodies in system
allBodies = []

# calculate accelation of body
def calculateAcc(body, bodies):
    fx = 0
    fy = 0
    for otherBody in bodies:
        if otherBody != body:
            bodyPos = body.getPos()
            otherPos = otherBody.getPos()
            rx = otherPos[0] - bodyPos[0]
            ry = otherPos[1] - bodyPos[1]
            d = math.sqrt(rx**2 + ry**2 + softening_factor)
            f = G * body.getMass() * otherBody.getMass() / (d**2)
            theta = math.atan2(ry, rx)
            fx += math.cos(theta) * f
            fy += math.sin(theta) * f
            print(fx, fy)
    xacc = fx / body.getMass()
    yacc = fy / body.getMass()
    return xacc, yacc

# update the positions and velocities of all bodies based on timestep dt
def updateBodies(dt):
    for body in allBodies:
        xacc, yacc = calculateAcc(body, allBodies)
        body.setAcc(xacc, yacc)
    for body in allBodies:
        body.update(dt)

# add a new body to system
def addBody(x, y, mass, radius, xspd, yspd):
    newBody = Body(x, y, mass, radius, xspd, yspd)
    allBodies.append(newBody)

# check if a body is valid to add
def isValidBody(x, y, mass, radius):
    if mass <= 0:
        return False
    for body in allBodies:
        pos = body.getPos()
        dx = x - pos[0]
        dy = y - pos[1]
        d = math.sqrt(dx**2 + dy**2)
        if d < radius:
            return False
    return True

if __name__ == "__main__":
    pause = True
    fig = plt.figure()
    ax = plt.axes(xlim =(-50, 50), ylim =(-50, 50)) 
    plt.subplots_adjust(bottom=0.25) 
    plt.subplots_adjust(top=0.9)

    # addBody(0,0,100.0,1,0.0,0.0)
    # addBody(-10,0,10.0,0.5,0.0,-1.0)
    # addBody(0,10,50.0,0.75,-1.0,0.0)
    
    axbox = fig.add_axes([0.08, 0.1, 0.1, 0.075])
    axbox2 = fig.add_axes([0.26, 0.1, 0.1, 0.075])
    axbox3 = fig.add_axes([0.5, 0.1, 0.1, 0.075])
    axbox4 = fig.add_axes([0.77, 0.1, 0.1, 0.075])
    axbox5 = fig.add_axes([0.88, 0.1, 0.11, 0.075])
    axbox6 = fig.add_axes([0.4, 0.01, 0.2, 0.075])
    massText = TextBox(axbox, 'Mass', initial="")
    radiusText = TextBox(axbox2, 'Radius', initial="")
    posText = TextBox(axbox3, 'Position(x,y)', initial="")
    velText = TextBox(axbox4, 'Velocity(vx,vy)', initial="")
    addButton = Button(axbox5, "Add Body")
    circles = []
    def add(event):
        mass = float(massText.text)
        radius = float(radiusText.text)
        pos = posText.text
        posArray = pos.split(",")
        x = int(posArray[0])
        y = int(posArray[1])
        vel = velText.text
        velArray = vel.split(",")
        vx = int(velArray[0])
        vy = int(velArray[1])
        if isValidBody(x, y, mass, radius):
            addBody(x, y, mass, radius, vx, vy)
            circle = plt.Circle((x, y), radius)
            circles.append(circle)
            ax.add_patch(circle)
        else:
            print("invalid body, try again")
    addButton.on_clicked(add)
    startButton = Button(axbox6, "Start!")

    def start(event):
        global pause
        pause = False

    startButton.on_clicked(start)
    def updatePlot(frame):
        if not pause:
            updateBodies(deltaTime)
            for circle, body in zip(circles, allBodies):
                circle.center = body.getPos()
            return circles
    
    anim = animation.FuncAnimation(fig, updatePlot, interval = 100)

    plt.show()