import csv
import sys

csv_file = csv.reader(open('./data/metadata.csv', 'r'), delimiter=',')

class Model:
    def __init__(self, filename):

        if filename == "":
            self.id = sys.maxsize
        else:
            # id is filename
            self.id = 'wss.'+str.split(filename, '.')[0]
            self.modelNum = None

            # find row based on id in metadata
            for row in csv_file:
                if(self.id == row[0]):
                    # Populate instance variables based on columns in the metadata
                    self.name = row[14]
                    self.category = row[1]
                    self.up = row[4]
                    self.front = row[5]
                    self.dimX = int( float(str.split(row[7], ',')[0]) * float(row[6]) )     # assuming dimX is mm
                    self.dimY = int( float(str.split(row[7], ',')[1]) * float(row[6]) )     # assuming dimY is mm
                    self.dimZ = int( float(str.split(row[7], ',')[2]) * float(row[6]) )     # assuming dimZ is mm
                    self.isContainer = True if row[8] == "TRUE" else False
                    self.surfaceVolume = 0.0 if row[9] == "" else float(row[9]) #questionable
                    self.solidVolume = 0.0 if row[10] == "" else float(row[10]) #questionable
                    self.supportSurfaceArea = 0.0 if row[11] == "" else float(row[11])
                    self.weight = 0.0 if row[12] == "" else float(row[12])
                    self.staticFriction = 0.0 if row[13] == "" else float(row[13])

                    break
