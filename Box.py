

class box:
    #Tehdessä oliota luokasta box, tulee laatikon sijainti(location) ja koko(size) asettaa listamuodossa
    def __init__(self, location, size, colour):
        super().__init__()
        self.location = location
        self.size = size
        self.colour = colour
        self.grab_position = False

    #Funktio jolla tartutaan laatioksta, kun grab-painiketta painetaan. Funktio tarkastaa vielä onko työkalupiste laatikon ääriviivojen sisäpuolella
    def grab(self, tooltip_location):
        if (tooltip_location[0] - self.size / 2 < self.location[0] < tooltip_location[0] + self.size / 2) and (
                tooltip_location[1] - self.size / 2 < self.location[1] < tooltip_location[1] + self.size / 2):
            self.grab_position = [self.location[0] - tooltip_location[0], self.location[1] - tooltip_location[1]]
        else:
            self.grab_position = False
    #Funktion grab, boolean arvo milloin voidaan tarttua laatikosta
    def grab_boolean(self, tooltip_location):
        if (tooltip_location[0] - self.size / 2 < self.location[0] < tooltip_location[0] + self.size / 2) and (
                tooltip_location[1] - self.size / 2 < self.location[1] < tooltip_location[1] + self.size / 2):
            return True
        else:
            return False

    def ungrab(self):
        self.grab_position = False

    #Funktio jolla määritellään suorakulmion sijainti ja koko
    def Rect(self):
        return [int(self.location[0] - self.size / 2), int(self.location[1] - self.size / 2), int(self.size), int(self.size)]

    #Kun laatikosta on otettu kiinni, niin tämän funktion avulla sen koordinaatit x ja y vaihtuu työkalupisteen
    #mukaan, eli suorakulmio liikkuu näytöllä.
    def tooltip_moving(self, tooltip_location):
        if self.grab_position:
            self.location = [tooltip_location[2] + self.grab_position[0], tooltip_location[3] + self.grab_position[1]]
