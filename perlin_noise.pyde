add_library('toxiclibs')
add_library('hemesh')
import random, time
add_library('queasycam')

noiseGrid = []
heightGrid = []
mesh = []
trees = []
scaled = 10
generating = True
waterHeight = .3
sandLevel = .32
stoneLevel = .7
grassLevel = .5

def setup():
    global cam
    size(800, 800, P3D)
    #worldwidth = 800
    #worldHeight = 800
    #cam = Camera(this)

    cam = QueasyCam(this)
    #cam.sensitivity = 0.5
    #cam.speed = 5
    
    #cam.lookAt(0, 0, 0)
    
    #camera(0,100,0, width/2, 0, height/2, 0, -1, 0)
    background(0)
    
    
    generate_noise()
    generate_mesh_verts()
    sphereDetail(1)
    #print(mesh)
def draw():
    lights()
    ambientLight(50,50,50)

    background(255)

    newPosY = retrieveHeight()-20
    #print(newPosY)
    posChangeY = cam.position.y - newPosY
    cam.position.y -= posChangeY
    #cam.tilt=(0)
    
    #print(cam.getForward(), cam.position.x, cam.position.z)
    #draw_noise()
    draw_points()
    #print(len(mesh), len(noiseGrid))
    for tree in trees:
        tree.renderTree()

def retrieveHeight():
    camx = cam.position.x
    camz = cam.position.z

    if camx >= 0 and camz >= 0 and camx <= width and camz <= height:
        gridx = camx // scaled
        gridz = (camz // scaled)+1
        gridindex = gridz*(width/scaled)+gridx
        #print(cam.velocity)
        return heightGrid[int(gridindex)]
    else:
        return heightGrid[0]


def display():
    textSize(24)
    fill(255,0,0)
    text("x: %d" % cam.position.x, 10, 50)
    #text(life_count, 10, 150)
    
def generate_noise():
    noiseScale = .05
    x_off = 0
    y_off = 0
    for y in range(height/scaled):
        y_off = y*noiseScale
        for x in range(width/scaled):
            x_off = x*noiseScale
            noiseGrid.append(noise(x_off,y_off))
            heightGrid.append(-((noise(x_off,y_off)*10)**2.5))

def generate_mesh_verts():
    global mesh
    z = 0
    x = 0
    
    for n in noiseGrid:
        
        n_mag = -(map(n,0,1,0,10))**2.5
        mesh.append([x, n_mag/2, z])
        #mesh.append([x, n_mag/2, z])
        x+=scaled
        if x == width:
            z += scaled
            x = 0
def draw_points():
    fill(200)
    #noStroke()
    beginShape(QUAD_STRIP)
    for i, vert in enumerate(mesh):
        
        #pushMatrix()
        vertex(vert[0], vert[1], vert[2])
    
        if i < len(mesh)-width/scaled:
            vertex(mesh[i+width/scaled][0], mesh[i+width/scaled][1], mesh[i+width/scaled][2])
        else:
            continue
    
        
        #popMatrix()
    endShape()
    
def draw_noise():
    
    #translate(-width/2, 0, -width/2)
    global generating
    z = 0
    x = 0
    topWaterHeight = -(waterHeight*10)**2.5
    #beginShape(TRIANGLE_STRIP)
    for count, n in enumerate(noiseGrid):
        pushMatrix()
        n_mag = -(map(n,0,1,0,10))**2.5
        #
        translate(x, n_mag/2, z)
        noStroke()
        fill(terrainClassifier(n))
        #noFill()
        box(scaled, n_mag, scaled)
        #print(n_mag)
        popMatrix()
        pushMatrix()
        if n < waterHeight:
            #print(n, n_mag, topWaterHeight)
            translate(x,topWaterHeight, z)
            fill(0,100,255)
            box(scaled, 1, scaled)
        if generating:
            if terrainClassifier(n) == -16736768:
                #if random.uniform(0,1) < .2:
               
                if n > ((grassLevel - sandLevel)/2)+sandLevel:
                    if random.uniform(0,1) < .1:
                        trees.append(Tree(x, n_mag, z))
        popMatrix()
        x += scaled
        if x == width:
            z += scaled
            x = 0
        #endShape()
    generating = False
    
        
def terrainClassifier(n):
    water = color(0, 0, 255)
    grass = color(0, 158, 0)
    stone = color(149, 148, 139)
    snow = color(255,255,255)
    sand = color (255, 242, 127)
    if n < waterHeight:
        return water
    elif n < sandLevel:
        return sand
    elif n < grassLevel:
        return grass
    elif n < stoneLevel:
        return stone
    else:
        return snow
    
class Tree():
    def __init__(self, x, y, z):
        self.pos = PVector(x, y, z)
        self.tHeight = -(scaled*random.randint(3,5))
        self.leafHeight = -(random.randint(2,6))
        self.leafwidth = random.uniform(scaled/4, scaled/2)
    def renderTree(self):
        #render trunk
        pushMatrix()
        translate(self.pos.x, self.pos.y, self.pos.z)
        fill(83,53,10)
        box(scaled/4, self.tHeight, scaled/4)
        #render leaves
        translate(0, self.tHeight/2+(self.leafHeight/2), 0)
        fill(0,200,0)
        box(self.leafwidth, self.leafHeight, self.leafwidth)
        popMatrix()
        pushMatrix()
        #left and right leaves
        translate(self.pos.x + scaled/8, self.pos.y+self.tHeight/2, self.pos.z)
        box(self.leafwidth, self.leafHeight, self.leafwidth)
        translate(-scaled/4, 0, 0)
        box(self.leafwidth, self.leafHeight, self.leafwidth)
        #up and down leaves
        translate(scaled/4, 0, scaled/8)
        box(self.leafwidth, self.leafHeight, self.leafwidth)
        translate(0, 0, -scaled/4)
        box(self.leafwidth, self.leafHeight, self.leafwidth)
        popMatrix()
        


    

        
            
