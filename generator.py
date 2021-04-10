from PIL import Image, ImageDraw, ImageFont
import os, sys, csv

def getAllBadges():
    badgePath = os.path.join(sys.path[0], "badge")
    badgeFiles = [f for f in os.listdir(badgePath) if os.path.isfile(os.path.join(badgePath, f))]
    return badgeFiles

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

def drawPlate(currentPlate, text, fontSize, flag, badgeChoice, side):

    #Obtain Parameters
    text = str(text)
    draw = ImageDraw.Draw(currentPlate)
    currentPlateSize = currentPlate.size

    #Set Plate Font
    plateFont = ImageFont.truetype(os.path.join(sys.path[0], "uknumberplate.ttf"), fontSize)
    plateFontSize = plateFont.getsize(text)

    if flag:

        #Add Badge
        badgeFile = os.path.join(os.path.join(sys.path[0], "badge"), badgeChoice) + ".png"
        badge = Image.open(badgeFile, 'r')
        #badge = addCorners(badge, 10, side)
        badgeOffset = (4, 4)
        currentPlate.paste(badge, badgeOffset)

        #Add Text
        x = 92 + (currentPlateSize[0] - 92 - plateFontSize[0]) / 2
        y = (currentPlateSize[1] - plateFontSize[1]) / 2
        draw.text((x, y), text, font=plateFont, fill=(0, 0, 0))

    else:

        #Add Text
        x = (currentPlateSize[0] - plateFontSize[0]) / 2
        y = (currentPlateSize[1] - plateFontSize[1]) / 2
        draw.text((x, y), text, font=plateFont, fill=(0, 0, 0))
 
def generatePlate(text, badge, badgeChoice):

    #Default Parameters for UK Licence Plate
    width = 520 * 2
    height = 111 * 2
    fontSize = 111 * 2
    frontPlteColour = (244, 244, 244, 255)
    rearPlateColour = (239, 220, 4, 255)

    #Create Image
    frontPlate = Image.new('RGBA', (int(width), int(height)), frontPlteColour)
    rearPlate = Image.new('RGBA', (int(width), int(height)), rearPlateColour)

    #Draw Iamge
    drawPlate(frontPlate, text, fontSize, badge, badgeChoice, "front")
    drawPlate(rearPlate, text, fontSize, badge, badgeChoice, "rear")

    #Round Plate Corners
    #Dunno why it causes problems
    #frontPlate = addCorners(frontPlate, 10, "front")
    #rearPlate = addCorners(rearPlate, 10, "rear")

    #Save File Path
    platePath = os.path.join(sys.path[0], "output")
    platePath = os.path.join(platePath, text)
    frontPlatePath = platePath + " Front.png"
    rearPlatePath = platePath + " Rear.png"

    #Save File
    frontPlate.save(frontPlatePath)
    rearPlate.save(rearPlatePath)
    del frontPlate
    del rearPlate

if '__main__' == __name__:
    choice = int(input("Manual entry [0] / Auto import [1]: "))
    if choice == 0:

        #Manual Entry
        stop = False
        while not stop:
            newPlate = str(input("Plate number: "))
            if newPlate == "STOP" or newPlate == "stop":
                stop = True
            else:
                newPlateBadge = int(input("No badge [0] /GB badge [1]: "))
                generatePlate(newPlate, newPlateBadge, "legal_eustars_GB")
    if choice == 1:

        #Auto Import
        LicenceDataPath = os.path.join(sys.path[0], "licence.csv")
        with open(LicenceDataPath) as licenceData:
            licenceDataReader = csv.reader(licenceData)
            next(licenceDataReader, None)
            for row in licenceDataReader:
                generatePlate(str(row[0]), int(row[1]), "legal_eustars_GB")