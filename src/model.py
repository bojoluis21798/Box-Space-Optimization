import csv

csv_file = csv.reader(open('./data/metadata.csv', 'r'), delimiter=',')

class Model:
    def __init__(self, filename):
        # id is filename
        self.id = 'wss.'+str.split(filename, '.')[0]

        # find row based on id in metadata and populate instance variables
        for row in csv_file:
            if(self.id == row[0]):

                self.name = row[14]
                self.category = row[1]
                self.up = row[4]
                self.front = row[5]
                self.dimX = str.split(row[7], ',')[0]
                self.dimY = str.split(row[7], ',')[1]
                self.dimZ = str.split(row[7], ',')[2]
                self.isContainer = True if row[8] == "TRUE" else False
                self.surfaceVolume = 0.0 if row[9] == "" else float(row[9])
                self.solidVolume = 0.0 if row[10] == "" else float(row[9])
                self.supportSurfaceArea = 0.0 if row[11] == "" else float(row[9])
                self.weight = 0.0 if row[12] == "" else float(row[9])
                self.staticFriction = 0.0 if row[13] == "" else float(row[9])

                break
