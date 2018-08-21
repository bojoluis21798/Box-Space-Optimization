import csv

class Model:
    def __init__(self, filename):
        csv_file = csv.reader(open('./data/metadata.csv', 'r'), delimiter=',')
        # id is filename
        self.id = 'wss.'+str.split(filename, '.')[0]
        self.filename = 'data/models/'+filename

        # find row based on id in metadata
        for row in csv_file:
            if(self.id == row[0]):
                # Populate instance variables based on columns in the metadata
                self.name = row[14]
                self.category = row[1]
                self.up = row[4]
                self.front = row[5]

                if row[6] == "":
                    self.unit = 1
                else:
                    self.unit = float(row[6])

                self.dimX = 0 if row[7] == "" else float(str.split(row[7], ',')[0])
                self.dimY = 0 if row[7] == "" else float(str.split(row[7], ',')[1])
                self.dimZ = 0 if row[7] == "" else float(str.split(row[7], ',')[2])

                self.isContainer = True if row[8] == "TRUE" else False
                self.surfaceVolume = 0.0 if row[9] == "" else float(row[9])
                self.solidVolume = 0.0 if row[10] == "" else float(row[10])
                self.supportSurfaceArea = 0.0 if row[11] == "" else float(row[11])
                self.weight = 0.0 if row[12] == "" else float(row[12])
                self.staticFriction = 0.0 if row[13] == "" else float(row[13])

                break
