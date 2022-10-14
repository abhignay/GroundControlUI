import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqtgraph import *
import pyqtgraph as pg
from random import randint
import serial

class GUI(QWidget):
    def __init__(self):
        super(GUI, self).__init__()

        # runs window setup, where the main gui window is initialized and all other functions are run
        self.window_setup()

        # timer 
        self.timer = QtCore.QTimer()  # type: ignore
        self.timer.setInterval(60)

        # updates data in every 60 milliseconds
        self.timer.timeout.connect(self.break_data)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.timeout.connect(self.update_tlmText_data)
        self.timer.timeout.connect(self.state_Box)
        self.timer.start()
        
    def window_setup(self):
        # window setup
        self.setStyleSheet("background-color: gray;" "QLabel{font-size: 24pt;}")
        self.setWindowTitle("TFAC Ground Control")
        self.setGeometry(0, 0, 1250, 725)

        # run all our functions
        self.raw_telem_boxes()
        self.graph_boxes()
        self.date_time()
        self.TFAC_times()
        self.alt_vel_acc()
        self.alt_vel_acc_graph()
        self.gnss_gyro_graph()
        self.not_all_telem()
        self.all_telem_pt2()
        self.main_telem()

        # show the main window    
        self.show()

    def raw_telem_boxes(self):
        # this is the "box" for the date, time
        Datebox = QLabel('   ', self) # nothing 
        Datebox.move(5, 10)
        Datebox.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        Datebox.resize(300, 51)

        # this is the box where alt, vel and acc are displayed 
        importantTLM_box = QLabel('   ', self) # nothing 
        importantTLM_box.move(5, 69)
        importantTLM_box.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        importantTLM_box.resize(300, 108)

        # all raw telemetry
        allTLM = QLabel('   ', self) # nothing 
        allTLM.move(5, 190)
        allTLM.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        allTLM.resize(300, 355) 

        # the box for the state and fire pyro buttons
        midBox = QLabel('   ', self) # nothing 
        midBox.move(425, 260)
        midBox.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        midBox.resize(400, 400) 

    def graph_boxes(self):
        # box for my mans the altitude graph
        alt_graph_boxieboi = QLabel('   ', self) # nothing 
        alt_graph_boxieboi.move(318, 10)
        alt_graph_boxieboi.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        alt_graph_boxieboi.resize(300, 169)

        # box for vel graph
        velGraph_box = QLabel('   ', self) # nothing 
        velGraph_box.move(630, 10)
        velGraph_box.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        velGraph_box.resize(300, 169)

        # box for acc graph
        accGraph_box = QLabel('   ', self) # nothing 
        accGraph_box.move(942, 10)
        accGraph_box.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        accGraph_box.resize(300, 169)

        # box for lat/lon graph
        coordinates_box = QLabel('   ', self) # nothing 
        coordinates_box.move(942, 190)
        coordinates_box.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        coordinates_box.resize(300, 169)

        # box for gyro (rps) graph
        gyro_box = QLabel('   ', self) # nothing 
        gyro_box.move(942, 370)
        gyro_box.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        gyro_box.resize(300, 169)

        # box for SIV graph
        SIV_box = QLabel('   ', self) # nothing 
        SIV_box.move(942, 550)
        SIV_box.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        SIV_box.resize(300, 169)

        # box for GNSS altitude
        gpsAlt_box = QLabel('   ', self) # nothing 
        gpsAlt_box.move(5, 550)
        gpsAlt_box.setStyleSheet( "background-color: #FFFFFF;"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "border-radius :5px")
        gpsAlt_box.resize(300, 169)

    def date_time(self):
        # everything for the date lmao
        DatePlaceHolder = QLabel('Date: ', self)
        DatePlaceHolder.move(17, 14)
        DatePlaceHolder.setStyleSheet("background-color: #00FFFFFF") # is this the best way to do it? idk, does it work. Yes

        self.actualdate = QLabel('0000-00-00', self)
        self.actualdate.move(56, 14)
        self.actualdate.setStyleSheet("background-color: #00FFFFFF")

        # Time, same thing as date
        TimePlaceHolder = QLabel('Time: ', self)
        TimePlaceHolder.move(17, 40)
        TimePlaceHolder.setStyleSheet("background-color: #00FFFFFF")

        self.TimeUTC = QLabel('00:00:00', self)
        self.TimeUTC.move(56, 40)
        self.TimeUTC.setStyleSheet("background-color: #00FFFFFF")

        UTCLabel = QLabel('UTC', self)
        UTCLabel.move(118, 40)
        UTCLabel.setStyleSheet("background-color: #00FFFFFF")

    def TFAC_times(self):
        # tfac is the name of my flight computer, this function basically shows the on time and flight time sent by the fc

        # on time
        OnTimeLabel = QLabel('On Time:', self) 
        OnTimeLabel.move(169, 14)
        OnTimeLabel.setStyleSheet("background-color: #00FFFFFF")

        self.RealOnTime = QLabel('1328.5', self)
        self.RealOnTime.move(235, 14)
        self.RealOnTime.setStyleSheet("background-color: #00FFFFFF")

        OntimeSecLabel = QLabel('s', self)
        OntimeSecLabel.move(270, 14)
        OntimeSecLabel.setStyleSheet("background-color: #00FFFFFF")

        # flight time
        Flight_TimeLabel = QLabel('Flight Time:', self)
        Flight_TimeLabel.move(169, 40)
        Flight_TimeLabel.setStyleSheet("background-color: #00FFFFFF")

        self.ActualFltTime = QLabel('47', self)
        self.ActualFltTime.move(255, 40)
        self.ActualFltTime.setStyleSheet("background-color: #00FFFFFF")

        Flt_Time_secLabel = QLabel('s', self)
        Flt_Time_secLabel.move(280, 40)
        Flt_Time_secLabel.setStyleSheet("background-color: #00FFFFFF")

    def alt_vel_acc(self):
        # altitude
        altLabel = QLabel('Alt:', self) 
        altLabel.setFont(QFont('default', 14))
        altLabel.move(20, 82)
        altLabel.setStyleSheet("background-color: #00FFFFFF")

        self.realAlt = QLabel("-180.13", self)
        self.realAlt.setFont(QFont('default', 14))
        self.realAlt.move(55, 82)
        self.realAlt.setStyleSheet("background-color: #00FFFFFF")

        meterLabel = QLabel('m', self)
        meterLabel.setFont(QFont('default', 14))
        meterLabel.move(125, 82)
        meterLabel.setStyleSheet("background-color: #00FFFFFF")

        # velocity
        velLabel = QLabel('Vel:', self) 
        velLabel.setFont(QFont('default', 14))
        velLabel.move(20, 112)
        velLabel.setStyleSheet("background-color: #00FFFFFF")

        self.realVel = QLabel("-123.65", self)
        self.realVel.setFont(QFont('default', 14))
        self.realVel.move(59, 112)
        self.realVel.setStyleSheet("background-color: #00FFFFFF")

        velUnit = QLabel('m/s', self)
        velUnit.setFont(QFont('default', 14))
        velUnit.move(125, 112)
        velUnit.setStyleSheet("background-color: #00FFFFFF")

        # acceleration
        accLabel = QLabel('Acc:', self) 
        accLabel.setFont(QFont('default', 14))
        accLabel.move(20, 142)
        accLabel.setStyleSheet("background-color: #00FFFFFF")

        self.realAcc = QLabel("-121.34", self)
        self.realAcc.move(59, 142)
        self.realAcc.setStyleSheet("background-color: #00FFFFFF;" "font-size: 16pt;")

        accUnit = QLabel('m/s^2', self)
        accUnit.setFont(QFont('default', 14))
        accUnit.move(125, 142)
        accUnit.setStyleSheet("background-color: #00FFFFFF")

    def alt_vel_acc_graph(self):
        # god bless the pyqtgraph documentation gods

        time = list(range(0, 100))  # type: ignore # 100 points for the "time"

        # altitude
        self.AltGraph = pg.PlotWidget(self)
        self.AltGraph.setGeometry(328, 11, 280, 165)
        self.AltGraph.setTitle('Altitude', size="10pt")
        self.AltGraph.setLabel('left', 'meters (AGL)', **styles)
        self.AltGraph.setLabel('bottom', 'Time (sec)', **styles)

        # we do this for every graph, 100 points for time and 100 random points for the actual value
        self.altVal = [randint(-10,1000) for _ in range(100)]

        # plot the altitude value and time
        self.altGraphLine = self.AltGraph.plot(time, self.altVal)

        # velocity
        self.velGraph = pg.PlotWidget(self)
        self.velGraph.setGeometry(633, 11, 280, 165)
        self.velGraph.setTitle('Velocity', size="10pt")
        self.velGraph.setLabel('left', 'm/s', **styles)
        self.velGraph.setLabel('bottom', 'Time (sec)', **styles)

        self.velVal = [randint(-100,1000) for _ in range(100)]

        self.velGraphLine = self.velGraph.plot(time, self.velVal)

        # acceleration
        self.accGraph = pg.PlotWidget(self)
        self.accGraph.setGeometry(945, 11, 280, 165)
        self.accGraph.setTitle('Acceleration', size="10pt")
        self.accGraph.setLabel('left', 'm/s^2', **styles)
        self.accGraph.setLabel('bottom', 'Time (sec)', **styles)

        self.accVal = [randint(-100.00,1000.00) for _ in range(100)]# type: ignore

        self.accGraphLine = self.accGraph.plot(time, self.accVal)

    def gnss_gyro_graph(self):
        # state
        self.state_Graph = pg.PlotWidget(self)
        self.state_Graph.setGeometry(945, 191, 294, 165)
        self.state_Graph.setTitle('System State', size="10pt")

        time = list(range(0, 100))  # type: ignore # 100 points for the "time"
        self.stateVal = [randint(1,1000) for _ in range(100)]

        self.stateLine = self.state_Graph.plot(time, self.stateVal)

        # gyro
        self.gyros_graph = pg.PlotWidget(self)
        self.gyros_graph.setGeometry(945, 373, 280, 165)
        self.gyros_graph.setTitle('Gyroscopes', size="10pt")
        self.gyros_graph.setLabel('left', 'rad/s', **styles)
        self.gyros_graph.setLabel('bottom', 'Time (sec)', **styles)

        self.gXVal = [randint(-100,1000) for _ in range(100)]
        self.gYVal = [randint(-100,1000) for _ in range(100)]
        self.gZVal = [randint(-100,1000) for _ in range(100)]

        self.gXLine = self.gyros_graph.plot(time, self.gXVal, pen='r')
        self.gYLine = self.gyros_graph.plot(time, self.gYVal, pen='b')
        self.gZLine = self.gyros_graph.plot(time, self.gZVal, pen='g')

        # SIV
        self.siv_graph = pg.PlotWidget(self)
        self.siv_graph.setGeometry(945, 553, 280, 165)
        self.siv_graph.setTitle('SIV', size="10pt")
        self.siv_graph.setLabel('left', 'SIV', **styles)
        self.siv_graph.setLabel('bottom', 'Time (sec)', **styles)

        self.sivVal = [randint(1,1000) for _ in range(100)]

        self.SIVLine = self.siv_graph.plot(time, self.sivVal)

        # gps altitude
        self.gnssAltGraph = pg.PlotWidget(self)
        self.gnssAltGraph.setGeometry(7, 552, 280, 165)
        self.gnssAltGraph.setTitle('GNSS Altitude', size="10pt")
        self.gnssAltGraph.setLabel('left', 'meters (MSL)', **styles)
        self.gnssAltGraph.setLabel('bottom', 'Time (sec)', **styles)

        self.gpsaltVal = [randint(-1000,100000) for _ in range(100)]

        self.gpsAltLine = self.gnssAltGraph.plot(time, self.gpsaltVal)

    def not_all_telem(self):
        #heading
        rawTLM_label = QLabel('Raw Telem', self) 
        rawTLM_label.setFont(QFont('Arial', 14))
        rawTLM_label.move(85, 200)
        rawTLM_label.setStyleSheet("background-color: #00FFFFFF")

        # the entire raw telemetry heading doesn't seem to render so we do this
        pt2_label = QLabel('etry', self) 
        pt2_label.setFont(QFont('Arial', 14))
        pt2_label.move(178, 200)
        pt2_label.setStyleSheet("background-color: #00FFFFFF")

        allTLM1 = QLabel('aX: aY: aZ: gX: gY: gZ: vX: vY: vZ: SIV: lat: lon: alt:', self) 
        allTLM1.move(10, 230)
        allTLM1.setStyleSheet("border : 1px solid white;"
                            "background-color: #00FFFFFF")
        allTLM1.setGeometry(10, 230, 30, 245)
        allTLM1.setWordWrap(True)

        self.allTLM1_data = QLabel('-1002.3 \n -1002.3 \n -1002.3 \n -1002.3 \n -1002.3 \n -1002.3 \n -1002.3 \n -1002.3 \n -1002.3 \n  100 \n  32.1236933 \n  23.8001853 \n -1002.3', self) 
        self.allTLM1_data.move(36, 242)                                                                                                                                                              
        self.allTLM1_data.setStyleSheet("background-color: #00FFFFFF")

        allTLM1_units =  QLabel(' mss \n mss \n mss \n rps \n rps \n rps \n m/s \n m/s \n m/s \n \n \n \n m', self) 
        allTLM1_units.move(83, 240)
        allTLM1_units.setStyleSheet("background-color: #00FFFFFF")

        allTLM1_units2 =  QLabel(' ° \n °', self) 
        allTLM1_units2.move(110, 415)
        allTLM1_units2.setStyleSheet("background-color: #00FFFFFF")

        # gawd damn thats a lot of code, this is prolly uber inefficient

        allTLM2 = QLabel('GAlt: GPSVX: GPSVY: GPSVZ:', self)
        allTLM2.move(15, 230)
        allTLM2.setStyleSheet("border : solid white;"
                            "background-color: #00FFFFFF")
        allTLM2.setGeometry(11, 458, 65 , 80)
        allTLM2.setWordWrap(True)

        self.gnssAlt_label = QLabel('9999.34', self)
        self.gnssAlt_label.move(54, 464)
        self.gnssAlt_label.setStyleSheet("background-color: #00FFFFFF")

        self.allTLM2_data = QLabel(' -148.9 \n -112.2 \n  -420.0', self)
        self.allTLM2_data.move(63, 480)
        self.allTLM2_data.setStyleSheet("background-color: #00FFFFFF")
        self.allTLM2_data.setWordWrap(True)

        allTLM2_unit = QLabel(' m \n m/s \n m/s \n m/s', self)
        allTLM2_unit.move(108, 463)
        allTLM2_unit.setStyleSheet("background-color: #00FFFFFF")
        allTLM2_unit.setWordWrap(True)

    def all_telem_pt2(self):
        allTLM3 = QLabel('BrdT: AmbT: pDOP: PY1S: PY2S: kVX: kVY: kVZ: rAlt: AccG: P1Alt: P2Alt: State: Bat:', self) 
        allTLM3.move(10, 230)
        allTLM3.setStyleSheet("border : solid white;"
                            "background-color: #00FFFFFF")
        allTLM3.setGeometry(150, 240, 50, 245)
        allTLM3.setWordWrap(True)

        self.allTLM3_value = QLabel('28.1 \n 32.3 \n 2 \n 0 \n 0 \n 124.5 \n 9.3 \n 1.2 \n 54.6 \n 1.3 \n 150 \n 0 \n 10 \n 11.1', self) 
        self.allTLM3_value.move(194, 244)
        self.allTLM3_value.setStyleSheet("background-color: #00FFFFFF")
        self.allTLM3_value.setWordWrap(True)

        allTLM3_unit = QLabel('°C \n°C', self) 
        allTLM3_unit.move(234, 243)
        allTLM3_unit.setStyleSheet("background-color: #00FFFFFF")
        allTLM3_unit.setWordWrap(True)

        allTLM3_unit2 = QLabel('m/s \n m/s \n m/s \n m \n G \n m \n m \n \n V', self) 
        allTLM3_unit2.move(234, 329)
        allTLM3_unit2.setStyleSheet("background-color: #00FFFFFF")
        allTLM3_unit2.setWordWrap(True)

        spaceFiller = QLabel('idk what to', self) 
        spaceFiller.move(150, 495)
        spaceFiller.setStyleSheet("background-color: #00FFFFFF")

        spaceFiller2 = QLabel('put here', self) 
        spaceFiller2.move(230, 495)
        spaceFiller2.setStyleSheet("background-color: #00FFFFFF")

    def main_telem(self):
        self.sysState = QLabel("INIT", self) 
        self.sysState.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore
        self.sysState.move(520, 275)
        self.sysState.setStyleSheet( "background-color:" + "#FFC0CB" + ";"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "font-size: 14pt;"
                                    "border-radius :5px")
        self.sysState.resize(200, 60) 

        # I haven't added any code to know if the fire pyro buttons are clicked, plan on adding it soon
        py1Box = QPushButton('Fire Pyro 1', self)
        py1Box.setFont(QFont("Futura", 16))
        py1Box.setStyleSheet("background-color: #FFA500")
        py1Box.resize(290, 75)
        py1Box.move(477,420)

        py2Box = QPushButton('Fire Pyro 2', self)
        py2Box.setFont(QFont("Futura", 16))
        py2Box.setStyleSheet("background-color: #FFA500")
        py2Box.resize(290, 75)
        py2Box.move(477,520)
 
    def break_data(self):
        # pre splitting stuff
        allData = ser.readline()
        allData = allData.decode()
        allData = allData.strip()
        
        # split data
        allData = str(allData)
        
        # your data should be printed to the serial monitor in this order (seperated by semi-colons) acc X, acc Y, acc Z, kalman alt, kalman vel x, kalmen vel y, kalman vel z, gyro X, gyro Y, gyro Z, on time, flight time, imu temp, baro temp, PY1 state, PY2 state, raw alt, vert acc in G, system state, GNSS data, GNSS time, SIV, latitude, longitude, GNSS alt, GNSS vel X, GNSS vel Y, GNSS vel Z, pDOP 
        # print each data packet in one line (use Serial.print(); for everything except the last value)
        self.accX, self.accY, self.accZ, self.alt, self.kvelX, self.kvelY, self.kvelZ, self.gyroX, self.gyroY, self.gyroZ, self.on_Time, self.FLT_time, self.imuTemp, self.baroTemp, self.py1S, self.py2S, self.rALT, self.accX_G, self.state, self.gpsDate, self.gpsTime, self.sats, self.lat, self.lon, self.gps_alt, self.gpsVX, self.gpsVY, self.gpsVZ, self.pDOP = allData.split(';')  # type: ignore

    def update_plot_data(self):
        # acceleration plot
        self.accVal = self.accVal[1:]  # type: ignore # Remove the first
        self.accVal.append(float(self.accX))  # type: ignore
        self.accGraphLine.setData(self.accVal)  # Update the data.

        # vel plot
        self.velVal = self.velVal[1:]  # type: ignore # Remove the first
        self.velVal.append(float(self.kvelX))  # type: ignore
        self.velGraphLine.setData(self.velVal)  # Update the data.

        # alt plot
        self.altVal = self.altVal[1:]  # type: ignore # Remove the first
        self.altVal.append(float(self.alt))  # type: ignore
        self.altGraphLine.setData(self.altVal)  # Update the data.

        # gyro plot
        self.gXVal = self.gXVal[1:]  # type: ignore # Remove the first
        self.gXVal.append(float(self.gyroX))  # type: ignore
        self.gXLine.setData(self.gXVal)  # Update the data.

        self.gYVal = self.gYVal[1:]  # type: ignore # Remove the first
        self.gYVal.append(float(self.gyroY))  # type: ignore
        self.gYLine.setData(self.gYVal)  # Update the data.

        self.gZVal = self.gZVal[1:]  # type: ignore # Remove the first
        self.gZVal.append(float(self.gyroZ))  # type: ignore
        self.gZLine.setData(self.gZVal)  # Update the data.

        # state plot
        self.stateVal = self.stateVal[1:]  # type: ignore # Remove the first
        self.stateVal.append(float(self.state))  # type: ignore
        self.stateLine.setData(self.stateVal)  # Update the data.

        # SIV plot
        self.sivVal = self.sivVal[1:]  # type: ignore # Remove the first
        self.sivVal.append(float(self.sats))  # type: ignore
        self.SIVLine.setData(self.sivVal)  # Update the data.

        # gnss alt plot
        self.gpsaltVal = self.gpsaltVal[1:]  # type: ignore # Remove the first
        self.gpsaltVal.append(float(self.gps_alt))  # type: ignore
        self.gpsAltLine.setData(self.gpsaltVal)  # Update the data.

    def update_tlmText_data(self):
        # times
        self.actualdate.setText(self.gpsDate)
        self.TimeUTC.setText(self.gpsTime)
        self.RealOnTime.setText(str(self.on_Time))
        self.ActualFltTime.setText(str(self.FLT_time))

        # main TLM box data
        self.realAlt.setText(str(self.alt))
        self.realVel.setText(str(self.kvelX))
        self.realAcc.setText(str(self.accX))

        # all tlm box data
        # aX: aY: aZ: gX: gY: gZ: vX: vY: vZ: SIV: lat: lon: alt:
        self.allTLM1_data.setText(str(self.accX) + ' \n ' + str(self.accY) + ' \n ' + str(self.accZ) + ' \n ' + str(self.gyroX) + ' \n ' + str(self.gyroY) + ' \n ' + 
                                  str(self.gyroZ) + ' \n ' + str(self.kvelX) + ' \n ' + str(self.kvelY) + ' \n ' + 
                                  str(self.kvelZ) + ' \n ' + str(self.sats) + ' \n ' + str(self.lat) + ' \n ' + str(self.lon) + ' \n ' + str(self.alt))


        self.gnssAlt_label.setText(str(self.gps_alt))

        # GPSVelX: GPSVelY: GPSVelZ:
        self.allTLM2_data.setText(str(self.gpsVX) + ' \n ' + str(self.gpsVY) + ' \n ' + str(self.gpsVZ))

        # BrdT: AmbT: pDOP: PY1S: PY2S: kVX: kVY: kVZ: rAlt: AccG: P1Alt: P2Alt: State: Bat:
        self.allTLM3_value.setText(str(self.imuTemp) + ' \n' + str(self.baroTemp) + '\n' + str(self.pDOP) + '\n' + str(self.py1S) + '\n' + str(self.py2S) + '\n' + 
                                  str(self.kvelX) + '\n' + str(self.kvelY) + ' \n' + str(self.kvelZ) + ' \n' + str(self.rALT) + ' \n' + str(self.accX_G) + ' \n' + '150 \n 0 \n' + str(self.state) + '\n 11.1')

    def state_Box(self):
        # the system states on my flight computer, you can replace the values with your flight computer's states
        statestr = " "
        color = " "

        if (int(self.state) == 0):
            statestr = "INIT"
            color = "#FFC0CB" # hot pink
        elif (int(self.state) == 1):
            statestr = "IDLE"
            color = "#90EE90" # green
        elif (int(self.state) == 2):
            statestr = "ASCENT"
            color =  "#ADD8E6" # light blue
        elif (int(self.state) == 3):
            statestr = "DESCENT"
            color = "#FFC933" # yellow
        elif (int(self.state) == 4 or int(self.state) == 5):
            statestr = "LANDED"
            color = "#64EDD2" # teal

        self.sysState.setText(statestr) 
        self.sysState.setStyleSheet( "background-color:" + color + ";"
                                    "border-style: solid;"
                                    "border-width: 1px;"
                                    "border-color: #000000;"
                                    "font-size: 14pt;"
                                    "border-radius :5px")

ser = serial.Serial('/dev/ttyACM0') # replace with your COM port

# style, font and colors for all the plots
pg.setConfigOption('background', 'white')
pg.setConfigOption('foreground', 'k')
styles = {'color':'black', 'font-size':'12px'}

app = QApplication(sys.argv)
window = GUI()
window.show()

sys.exit(app.exec_())