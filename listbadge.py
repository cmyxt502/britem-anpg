from os import listdir
from os.path import isfile, join
import os, sys
from PIL import Image, ImageDraw, ImageFont
def addCorners(im, rad, side):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

badgePath = os.path.join(sys.path[0], "badge")
onlyfiles = [f for f in listdir(badgePath) if isfile(join(badgePath, f))]
newfiles = []
for i in onlyfiles:
    newfiles.append(i.replace(".png", ""))
    with Image.open(os.path.join(badgePath, i)) as currentBadge:
        currentBadge = addCorners(currentBadge, 10, "side")
        currentBadge.save(os.path.join(badgePath, i))
    