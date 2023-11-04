from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

from robotarm import Robotarm
from Box import box


new_box = box([700, 511], 75, "")
robot_arm = Robotarm(2, 2)

class Widget(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.setMouseTracking(True)
        self.width = width
        self.height = height
        self.setWindowTitle("Robottikäsi")
        self.resize(self.width, self.height)
        self.UI()
        self.show()
        self.timer = QTimer()
        self.timer.setInterval(int(1000 / 60))  # 60 fps
        self.timer.timeout.connect(self.updateCanvas)
        self.timer.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 20, Qt.SolidLine))
        robot_arm.go_to_coordinate_point()

        x0 = robot_arm.x0
        y0 = robot_arm.y0
        #Nivelten 1 ja 2 kulmat
        angle1 = robot_arm.a1
        angle2 = robot_arm.a2

        #Käsivarren 1 koordinaatit
        x1 = robot_arm.tooltip_pos(angle1, angle2)[0]
        y1 = robot_arm.tooltip_pos(angle1, angle2)[1]

        #työkalupisteen koordinaatit
        x2 = robot_arm.tooltip_pos(angle1, angle2)[2]
        y2 = robot_arm.tooltip_pos(angle1, angle2)[3]

        #Liikuteltavan suorakulmion grafiikka
        rect_bounds = new_box.Rect()
        new_box.tooltip_moving(robot_arm.tooltip_pos(angle1, angle2))
        painter.setBrush(QBrush(Qt.gray, Qt.Dense5Pattern))
        painter.setPen(Qt.black)
        painter.drawRect(rect_bounds[0], rect_bounds[1], rect_bounds[2], rect_bounds[3])

        #Arm1
        painter.setPen(QPen(Qt.black, 20, Qt.SolidLine))
        painter.drawLine(int(x0), int(y0), int(x1), int(y1))
        #Arm2
        painter.setPen(QPen(Qt.black, 15, Qt.SolidLine))
        painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        #Nivel1
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawEllipse(470, 430, 40, 40)

        #Nivel 2
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawEllipse(int(x1)-15, int(y1)-15, 30, 30)

        #Työkalupiste
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawEllipse(int(robot_arm.tooltip_coords()[0]) - 10, int(robot_arm.tooltip_coords()[1]) - 10, 20, 20)

        #Lattia
        floor_height = self.height - 10
        painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        painter.setPen(QPen(Qt.gray, 2, Qt.SolidLine))
        painter.drawRect(0, floor_height, self.width, self.height)


        #Robottikäden alusta
        box_width = 110
        box_height = 110
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.setPen(Qt.black)
        painter.drawRect(int((self.width/2) - (box_width/2)), (self.height - box_height), box_width, box_height)

        #Piirtää trajektorigeneraattorin määrittämän reitin näkyville
        i = 1
        for coordinate_point in robot_arm.coordinate_points:
            painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
            painter.drawEllipse(int(coordinate_point[0]), int(coordinate_point[1]), 2, 2)
            i += 1

    def UI(self):

        #Luodaan tartu nappula
        self.grab_button = QPushButton("Grab: OFF", self)
        self.grab_button.setCheckable(True)
        self.grab_button.move(10, 200)
        self.grab_button.resize(100, 50)
        self.grab_button.clicked.connect(self.grab_button_clicked)

        #Robotin liikkumisnopeuden liukusäädin
        self.sld = QSlider(Qt.Orientation.Vertical, self)
        self.sld.setRange(1, 100)
        self.sld.setValue(100)
        self.sld.move(100, 50)
        self.sld.valueChanged.connect(self.update_speedSlider)

        #Liukusäätimet nivelille 1 ja 2.
        sld1 = QSlider(Qt.Orientation.Vertical, self)
        sld1.setRange(0, 180)
        sld1.setPageStep(1)

        sld2 = QSlider(Qt.Orientation.Vertical, self)
        sld2.setRange(0, 360)
        sld2.setPageStep(1)
        sld2.setValue(0)

        sld1.move(0, 50)
        sld2.move(50, 50)

        sld1.valueChanged.connect(self.updateAngle1)
        sld2.valueChanged.connect(self.updateAngle2)

        self.label = QLabel('0', self)
        self.label2 = QLabel('0', self)
        self.label3 = QLabel('A1', self)
        self.label4 = QLabel('A2', self)
        self.label5 = QLabel('Speed', self)
        self.label6 = QLabel(str(self.sld.value()), self)

        #Nivelten 1 ja 2, kulmien arvot
        self.label.move(0, 150)
        self.label2.move(50, 150)
        self.label.setMinimumWidth(80)
        self.label2.setMinimumWidth(80)

        #Nivel1 merkki 'A1'
        self.label3.move(0, 0)

        #Nivel2 merkki 'A2'
        self.label4.move(50, 0)

        #Käden nopeuden liukusäätimen merkki 'Speed'
        self.label5.move(100, 0)
        self.label6.move(100, 150)
        self.setGeometry(0, 0, self.width, self.height)

    #Tartu nappula, kun sitä painetaan
    def grab_button_clicked(self):
        if self.grab_button.isChecked() and new_box.grab_boolean(robot_arm.tooltip_coords()):
            self.grab_button.setText("Grab: ON")
            self.grab_button.setStyleSheet("background-color: red")
            new_box.grab(robot_arm.tooltip_coords())
        else:
            self.grab_button.setText("Grab: OFF")
            self.grab_button.setStyleSheet("background-color: None")
            new_box.ungrab()

    def mousePressEvent(self, QMouseEvent):
        robot_arm.trajectory_generator([QMouseEvent.x(), QMouseEvent.y()])
        x = QMouseEvent.x()
        y = QMouseEvent.y()
        angles = robot_arm.inverse_kinematics([x, y])
        self.label.setText(str(int(angles[0])))
        self.label2.setText(str(int(angles[1])))

    def updateAngle1(self, angle1):
        self.label.setText(str(angle1))
        robot_arm.a1 = int(angle1)

    def update_speedSlider(self):
        sliderValue = self.sld.value()
        robot_arm.coordinatepoint_distance = sliderValue / 10
        self.label6.setText(str(sliderValue))

    def updateAngle2(self, angle2):
        self.label2.setText(str(angle2))
        robot_arm.a2 = int(angle2)


    def updateCanvas(self):
        self.update()

