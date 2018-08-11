import csv

csv_file = csv.reader(open('./data/metadata.csv', 'r'), delimiter=',')

class Model:
    def __init__(self, filename):

        if filename == "":
            self.id = 'null'
        else:
            # id is filename
            self.id = 'wss.'+str.split(filename, '.')[0]

            # find row based on id in metadata
            for row in csv_file:
                if(self.id == row[0]):
                    # Populate instance variables based on columns in the metadata
                    self.convertionFactor = 10                                                                      #convert cm to mm
                    self.name = row[14]
                    self.category = row[1]
                    self.up = row[4]
                    self.front = row[5]
                    self.dimX = int( float(str.split(row[7], ',')[0]) * float(row[6]) * self.convertionFactor )     #convert dimensionX to nearest mm
                    self.dimY = int( float(str.split(row[7], ',')[1]) * float(row[6]) * self.convertionFactor )     #convert dimensionY to nearest mm
                    self.dimZ = int( float(str.split(row[7], ',')[2]) * float(row[6]) * self.convertionFactor )     #convert dimensionZ to nearest mm
                    self.isContainer = True if row[8] == "TRUE" else False
                    self.surfaceVolume = 0.0 if row[9] == "" else float(row[9]) #questionable
                    self.solidVolume = 0.0 if row[10] == "" else float(row[10]) #questionable
                    self.supportSurfaceArea = 0.0 if row[11] == "" else float(row[11])
                    self.weight = 0.0 if row[12] == "" else float(row[12])
                    self.staticFriction = 0.0 if row[13] == "" else float(row[13])

                    break
