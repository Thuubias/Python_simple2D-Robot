
import math



# Tässä luokassa määritellään itse robottikäsi ja sen funktionaalisuuteen liittyvät toiminnot.

class Robotarm():

    # l1 on robottikäden ensimmäisen varren pituus ja l2 toisen.
    # self.a1 on ensimmäisen nivelen kulma radiaaneina ja self.a2 toisen.
    # Syötetään uutta robotarmia luodessa kuitenkin kulmat asteina.
    def __init__(self, l1, l2):
        self.l1 = l1*100
        self.l2 = l2*100
        self.x0 = 490
        self.y0 = 450
        self.a1 = 0
        self.a2 = 0

        self.coordinate_points = []

        self.coordinatepoint_distance = 10

    #Funktio, joka muuttaa asteet radiaaneiksi
    def degrees_to_radians(self, angle):
        return angle * (math.pi / 180)
    #Funktio joka muuttaa radiaanit takaisin asteiksi
    def radians_to_degrees(self, angle):
        return (angle * 180)/math.pi

    #Lasketaan työkalupisteen sijainti, suoran kinematiikan avulla
    def tooltip_pos(self, angle1, angle2):
        x1 = int(self.x0 + self.l1 * math.cos(self.degrees_to_radians(360-angle1)))
        y1 = int(self.y0 + self.l1 * math.sin(self.degrees_to_radians(360-angle1)))

        x_coord = int(x1 + self.l2 * math.cos(self.degrees_to_radians((360-angle1)+angle2)))
        y_coord = int(y1 + self.l2 * math.sin(self.degrees_to_radians((360-angle1)+angle2)))
        return [x1, y1, x_coord, y_coord]

    #Luodaan lista johon tulee työkalupisteen koordinaatit: [x, y]
    def tooltip_coords(self):
        coords = [self.tooltip_pos(self.a1, self.a2)[2], self.tooltip_pos(self.a1, self.a2)[3]]
        return coords

    #Alla oleva funktio laskee käänteistä kinematiikkaa käyttäen robottikäden nivelille oikeat kulmat, kun työkalu-
    #piste halutaan paikkaan [x, y]. Funktion palautusarvo on lista, jossa alpha1 on nivelen 1 kulma ja alpha2 nievelen 2.
    def inverse_kinematics(self, coordinates):
        x = coordinates[0] - self.x0
        y = min(550 - self.y0, coordinates[1] - self.y0)

        #Tarkastetaan yltääkö käsivarsi tavoitekoordinaatteihin
        r = math.sqrt(x**2 + y**2)
        if r > self.l1 + self.l2:
            return [self.a1, self.a2]

        #Tarkastetaan ovatko tavoitekoordinaatit oikeassapuolitasossa ja lasketaan toisen nivelen kulma
        if coordinates[0] > self.x0:
            alpha2 = math.acos((x**2 + y**2 - (self.l1**2) - (self.l2**2))/(2 * self.l1 * self.l2))
        else:
            alpha2 = 2*math.pi - math.acos((x ** 2 + y ** 2 - (self.l1 ** 2) - (self.l2 ** 2)) / (2 * self.l1 * self.l2))
        #Lasketaan ensimmäisen nivelen kulma
        if math.sin(alpha2) != 0:
            alpha1 = math.atan2(y, x) - math.atan2(self.l2*math.sin(alpha2), self.l1 + self.l2*math.cos(alpha2))
            alpha1_2 = math.atan2(y, x) - math.atan2(self.l2 * math.sin(alpha2), self.l1 + self.l2 * math.cos(alpha2))
        else:
            alpha1 = math.atan2(y - self.l2 * math.sin(alpha2), x - self.l1 - self.l2 * math.cos(alpha2))
            alpha1_2 = None
        #Kun tavoitekoordinaatit ovat vasemmassa puolitasossa:
        if (x < 0 and alpha1_2 is not None):
            return [int(-self.radians_to_degrees(alpha1_2)), int(self.radians_to_degrees(alpha2))]

        return [int(-self.radians_to_degrees(alpha1)), int(self.radians_to_degrees(alpha2))]

    #Trajektorigeneraattori, joka laskee reittipisteet työkalupisteen ja maalikoordinaattien (coordinatepoint) väliltä
    def trajectory_generator(self, coordinatepoint):
        if (len(self.coordinate_points) > 0):
            last_coordinatepoint = self.coordinate_points[len(self.coordinate_points) - 1]
        else:
            last_coordinatepoint = self.tooltip_coords()

        errorLocation = [coordinatepoint[0] - last_coordinatepoint[0], coordinatepoint[1] - last_coordinatepoint[1]]

        distance = max(0.1, math.sqrt(errorLocation[0] ** 2 + errorLocation[1] ** 2))
        dataPoint_amount = math.ceil(distance / self.coordinatepoint_distance)

        for i in range(0, dataPoint_amount + 1):
            newWaypoint = [last_coordinatepoint[0] + errorLocation[0] * i / dataPoint_amount, last_coordinatepoint[1] + errorLocation[1] * i / dataPoint_amount]

            waypointDistanceToRobotBase = math.sqrt((newWaypoint[0] - self.x0)**2 + (newWaypoint[1] - self.y0)**2)
            if waypointDistanceToRobotBase < self.l1 + self.l2:
                self.coordinate_points.append([(last_coordinatepoint[0] + errorLocation[0] * i / dataPoint_amount), (last_coordinatepoint[1] + errorLocation[1] * i / dataPoint_amount)])


    #Funktio käskee käsivartta liikkumaan
    def go_to_coordinate_point(self):
        if len(self.coordinate_points) > 0:
            self.gotoLocation(self.coordinate_points[0])
            if self.atTargetAngles():
                self.coordinate_points.pop(0)

    #Funktio tarkastelee tavoitekoordinaatteihin vaadittavia kulmaeroja nykyiseen hetkeen ja palauttaa lopuksi boolean arvon,
    #jonka avulla saadaan tietää ollaanko vielä tavoite pisteessä
    def gotoLocation(self, targetCoords):
        self.targetAngles = self.inverse_kinematics(targetCoords)
        angle1Error = self.targetAngles[0] - self.a1
        angle2Error = self.targetAngles[1] - self.a2

        self.a1 += angle1Error
        self.a2 += angle2Error

        return self.atTargetAngles()

    #Funktio, joka tarkastaa onko työkalupiste tavoitekoordinaateissa
    def atTargetAngles(self):
        return abs(self.a1 - self.targetAngles[0]) < 1 and abs(self.a2 - self.targetAngles[1]) < 1