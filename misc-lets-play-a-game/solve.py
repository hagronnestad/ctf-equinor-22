from pwn import *
import cv2
import numpy as np
from matplotlib import pyplot as plt
import base64
import re
from webcolors import rgb_to_name

def GetShapes(img):
    # converting image into grayscale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # setting threshold of gray image
    # _, threshold = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # using a findContours() function
    contours, _ = cv2.findContours(
        gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0

    shapes = []

    # list for storing names of shapes
    for contour in contours:
        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        # using drawContours() function
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)

        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
            r = img[y, x, 2]
            g = img[y, x, 1]
            b = img[y, x, 0]

            named_color = rgb_to_name((r, g, b), spec='css3')
            # named_color = ""

        # putting shape name at center of each shape
        if len(approx) == 3:
            cv2.putText(img, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            shapes.append(["triangle", (x, y), PosToString((x,y)), named_color, (r, g, b)])

        elif len(approx) == 4:
            cv2.putText(img, 'Quadrilateral', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            shapes.append(["rectangle", (x, y), PosToString((x,y)), named_color, (r, g, b)])

        elif len(approx) == 5:
            cv2.putText(img, 'Pentagon', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            shapes.append(["pentagon", (x, y), PosToString((x,y)), named_color, (r, g, b)])

        elif len(approx) == 6:
            cv2.putText(img, 'Hexagon', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            shapes.append(["hexagon", (x, y), PosToString((x,y)), named_color, (r, g, b)])

        else:
            cv2.putText(img, 'circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            shapes.append(["circle", (x, y), PosToString((x,y)), named_color, (r, g, b)])

    return shapes



def PosToString(pos):
    x, y = pos

    s = ""

    if (y < 256):
        s += "n"
    else:
        s += "s"

    if (x < 256):
        s += "w"
    else:
        s += "e"

    return s


io = connect("io.ept.gg", 30047)

print(io.recvuntil(b"Are you ready?\n").decode())
io.sendline()
cnt = 0

while True:
    cnt += 1
    print(f"Iteration: {cnt}")

    if (cnt == 201):
        io.interactive()

    io.recvuntil("Where is the ")

    where_is_shape = io.recvuntil(" (", True).decode()
    print(where_is_shape)
    io.recvline()

    imageb64 = io.recvline().decode()

    img = base64.b64decode(imageb64)
    npimg = np.fromstring(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)

    shapes = GetShapes(source)
    print(shapes)

    color = None

    if (where_is_shape.find(" ") > -1):
        parts = where_is_shape.split(" ")
        color = parts[0]
        where_is_shape = parts[1]

    # print(imageb64)

    if (color == None):
        shape = next(s for s in shapes if s[0] == where_is_shape)
    else:
        shape = next(s for s in shapes if s[0] == where_is_shape and s[3] == color)

    print(f"Pos: {shape[2]}")
    io.sendline(shape[2])

    print(io.recvline().decode())
