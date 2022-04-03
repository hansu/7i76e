import os, subprocess
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QApplication, QMenu, QAction

inputs = [{'Not Used':'Select'},
	{'Homing':['Joint 0 Home', 'Joint 1 Home', 'Joint 2 Home',
		'Joint 3 Home', 'Joint 4 Home', 'Joint 5 Home',
		'Joint 6 Home', 'Joint 7 Home', 'Joint 8 Home', 'Home All']},
	{'Limits':[
		{'Joint 0':['Joint 0 Plus', 'Joint 0 Minus', 'Joint 0 Both']},
		{'Joint 1':['Joint 1 Plus', 'Joint 1 Minus', 'Joint 1 Both']},
		{'Joint 2':['Joint 2 Plus', 'Joint 2 Minus', 'Joint 2 Both']},
		{'Joint 3':['Joint 3 Plus', 'Joint 3 Minus', 'Joint 3 Both']},
		{'Joint 4':['Joint 4 Plus', 'Joint 4 Minus', 'Joint 4 Both']},
		{'Joint 5':['Joint 5 Plus', 'Joint 5 Minus', 'Joint 5 Both']},
		{'Joint 6':['Joint 6 Plus', 'Joint 6 Minus', 'Joint 6 Both']},
		{'Joint 7':['Joint 7 Plus', 'Joint 7 Minus', 'Joint 7 Both']},
		{'Joint 8':['Joint 8 Plus', 'Joint 8 Minus', 'Joint 8 Both']}]},
	{'Jog':[{'X Axis':['X Plus', 'X Minus', 'X Enable']},
		{'Y Axis':['Y Plus', 'Y Minus', 'Y Enable']},
		{'Z Axis':['Z Plus', 'Z Minus', 'X Enable']},
		{'A Axis':['A Plus', 'A Minus', 'A Enable']},
		{'B Axis':['B Plus', 'B Minus', 'B Enable']},
		{'C Axis':['C Plus', 'C Minus', 'C Enable']},
		{'U Axis':['U Plus', 'U Minus', 'U Enable']},
		{'V Axis':['V Plus', 'V Minus', 'V Enable']},
		{'W Axis':['W Plus', 'W Minus', 'W Enable']}
	]},
	{'I/O Control':['Flood', 'Mist', 'Lube Level', 'Tool Changed',
		'Tool Prepared', 'External E-Stop']},
	{'Motion':['Probe Input', 'Digital 0', 'Digital 1', 'Digital 2', 'Digital 3']}
]

# {'':['', ]},
# '', 
outputs = [{'Not Used':'Select'},
	{'Spindle':['Spindle On', 'Spindle CW', 'Spindle CCW', 'Spindle Brake']},
	{'I/O Control':['Coolant Flood', 'Coolant Mist', 'Lube Pump',
		'Tool Change', 'Tool Prepare', 'E Stop Out']},
	{'Digital Out':['Digital Out 0', 'Digital Out 1', 'Digital Out 2', 'Digital Out 3', ]}
]


def isNumber(s):
	try:
		s[-1].isdigit()
		float(s)
		return True
	except ValueError:
		return False

def checks(parent):
	try:
		subprocess.check_output('mesaflash', encoding='UTF-8')
	except FileNotFoundError:
		t = ('Mesaflash not found go to\n'
			'https://github.com/LinuxCNC/mesaflash\n'
			'for installation instructions.')
		parent.machinePTE.appendPlainText(t)
		parent.readpdPB.setEnabled(False)
		parent.readhmidPB.setEnabled(False)
		parent.flashPB.setEnabled(False)
		parent.reloadPB.setEnabled(False)

def axisChanged(parent):
	joint = parent.sender().objectName()[-1]
	axis = parent.sender().currentText()
	if axis in ['X', 'Y', 'Z', 'U', 'V', 'W']:
		getattr(parent, f'axisType_{joint}').setText('LINEAR')
	elif axis in ['A', 'B', 'C']:
		getattr(parent, f'axisType_{joint}').setText('ANGULAR')
	else:
		getattr(parent, f'axisType_{joint}').setText('')
	coordList = []
	for i in range(parent.card['joints']):
		axisLetter = getattr(parent, f'axisCB_{i}').currentText()
		if axisLetter != 'Select':
			coordList.append(axisLetter)
		parent.coordinatesLB.setText(''.join(coordList))
		parent.axes = len(parent.coordinatesLB.text())

def configNameChanged(parent, text):
	if text:
		parent.configNameUnderscored = text.replace(' ','_').lower()
		parent.configPath = os.path.expanduser('~/linuxcnc/configs') + '/' + parent.configNameUnderscored
		parent.pathLabel.setText(parent.configPath)
	else:
		parent.pathLabel.setText('')

def maxVelChanged(parent, text):
	if text:
		if isNumber(text):
			val = float(text)
			parent.maxVelMinLB.setText(F'{val * 60} units/min')
		else:
			parent.maxVelMinLB.setText('ERROR')
	else:
		parent.maxVelMinLB.setText('  units/min')

def pidSetDefault(parent):
	tab = parent.sender().objectName()[-1]
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Machine Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	p = int(1000/(int(parent.servoPeriodSB.cleanText())/1000000))
	getattr(parent, 'p_' + tab).setText(f'{p}')
	getattr(parent, 'i_' + tab).setText('0')
	getattr(parent, 'd_' + tab).setText('0')
	getattr(parent, 'ff0_' + tab).setText('0')
	getattr(parent, 'ff1_' + tab).setText('1')
	getattr(parent, 'ff2_' + tab).setText('0.00013')
	getattr(parent, 'bias_' + tab).setText('0')
	getattr(parent, 'maxOutput_' + tab).setText('0')
	if parent.linearUnitsCB.itemData(parent.linearUnitsCB.currentIndex()) == 'inch':
		maxError = '0.0005'
	else:
		maxError = '0.0127'
	getattr(parent, 'maxError_' + tab).setText(maxError)
	getattr(parent, 'deadband_' + tab).setText('0')

def firmwareChanged(parent):
	if parent.firmwareCB.currentData():
		path = os.path.splitext(parent.firmwareCB.currentData())[0]
		bitfile = os.path.join(path + '.pin')
		if os.path.exists(bitfile):
			with open(bitfile, 'r') as file:
				data = file.read()
			parent.machinePTE.clear()
			parent.machinePTE.setPlainText(data)
		else:
			parent.machinePTE.clear()
			parent.machinePTE.setPlainText(f'No pin file found for {parent.firmwareCB.currentText()}')
	else:
		parent.machinePTE.clear()

def spindlePidDefault(parent):
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Machine Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	if parent.spindleMaxRpm.text() == '':
		QMessageBox.warning(parent,'Warning', 'Spindle Tab\nMax RPM\nmust be specified', QMessageBox.Ok)
		return
	if not isNumber(parent.spindleMaxRpm.text()):
		QMessageBox.warning(parent,'Warning', 'Spindle Tab\nMax RPM\nnot a valid number', QMessageBox.Ok)
		return
	getattr(parent, 'p_s').setText('0.0')
	getattr(parent, 'i_s').setText('0.0')
	getattr(parent, 'd_s').setText('0.0')
	getattr(parent, 'ff0_s').setText('1.0')
	getattr(parent, 'ff1_s').setText('0.0')
	getattr(parent, 'ff2_s').setText('0.0')
	getattr(parent, 'bias_s').setText('0.0')
	getattr(parent, 'deadband_s').setText('0.0')
	getattr(parent, 'maxOutput_s').setText(f'{parent.spindleMaxRpm.text()}')

def driveChanged(parent):
	timing = parent.sender().itemData(parent.sender().currentIndex())
	joint = parent.sender().objectName()[-1]
	if timing:
		getattr(parent, 'stepTime_' + joint).setText(timing[0])
		getattr(parent, 'stepSpace_' + joint).setText(timing[1])
		getattr(parent, 'dirSetup_' + joint).setText(timing[2])
		getattr(parent, 'dirHold_' + joint).setText(timing[3])
		getattr(parent, 'stepTime_' + joint).setEnabled(False)
		getattr(parent, 'stepSpace_' + joint).setEnabled(False)
		getattr(parent, 'dirSetup_' + joint).setEnabled(False)
		getattr(parent, 'dirHold_' + joint).setEnabled(False)
	else:
		getattr(parent, 'stepTime_' + joint).setEnabled(True)
		getattr(parent, 'stepSpace_' + joint).setEnabled(True)
		getattr(parent, 'dirSetup_' + joint).setEnabled(True)
		getattr(parent, 'dirHold_' + joint).setEnabled(True)

def plcOptions():
	return ['ladderRungsSB', 'ladderBitsSB', 'ladderWordsSB',
	'ladderTimersSB', 'iecTimerSB', 'ladderMonostablesSB', 'ladderCountersSB',
	'ladderInputsSB', 'ladderOutputsSB', 'ladderExpresionsSB',
	'ladderSectionsSB', 'ladderSymbolsSB', 'ladderS32InputsSB',
	'ladderS32OuputsSB', 'ladderFloatInputsSB', 'ladderFloatOutputsSB']

def updateAxisInfo(parent):
	if parent.sender().objectName() == 'actionOpen':
		return
	joint = parent.sender().objectName()[-1]
	scale = getattr(parent, 'scale_' + joint).text()
	if scale and isNumber(scale):
		scale = float(scale)
	else:
		return

	maxVelocity = getattr(parent, 'maxVelocity_' + joint).text()
	if maxVelocity and isNumber(maxVelocity):
		maxVelocity = float(maxVelocity)
	else:
		return

	maxAccel = getattr(parent, 'maxAccel_' + joint).text()
	if maxAccel and isNumber(maxAccel):
		maxAccel = float(maxAccel)
	else:
		return

	if not parent.linearUnitsCB.currentData():
		parent.errorMsg('Machine Tab:\nLinear Units must be selected', 'Error')
		return
	accelTime = maxVelocity / maxAccel
	getattr(parent, 'timeJoint_' + joint).setText(f'{accelTime:.2f} seconds')
	accelDistance = accelTime * 0.5 * maxVelocity
	getattr(parent, 'distanceJoint_' + joint).setText(f'{accelDistance:.2f} {parent.linearUnitsCB.currentData()}')
	stepRate = scale * maxVelocity
	getattr(parent, 'stepRateJoint_' + joint).setText(f'{abs(stepRate):.0f} pulses')


def spindleTypeChanged(parent):
	if parent.spindleTypeCB.currentData():
		parent.spindleGB.setEnabled(True)
		parent.spindleInfoGB.setEnabled(True)
		parent.encoderGB.setEnabled(True)
		parent.spindlepidGB.setEnabled(True)
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '1':
			parent.spindleInfo1Lbl.setText("PWM on Step 4")
			parent.tb2p3LB.setText("PWM +")
			parent.tb2p2LB.setText("PWM -")
			parent.spindleInfo2Lbl.setText("Direction on Dir 4")
			parent.tb2p5LB.setText("Direction +")
			parent.tb2p4LB.setText("Direction -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '2':
			parent.spindleInfo1Lbl.setText("UP on Step 4")
			parent.tb2p3LB.setText("UP +")
			parent.tb2p2LB.setText("UP -")
			parent.spindleInfo2Lbl.setText("Down on Dir 4")
			parent.tb2p5LB.setText("DOWN +")
			parent.tb2p4LB.setText("DOWN -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '3':
			parent.spindleInfo1Lbl.setText("PDM on Step 4")
			parent.tb2p3LB.setText("PDM +")
			parent.tb2p2LB.setText("PDM -")
			parent.spindleInfo2Lbl.setText("Direction on Dir 4")
			parent.tb2p5LB.setText("Direction +")
			parent.tb2p4LB.setText("Direction -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '4':
			parent.spindleInfo1Lbl.setText("Direction on Step 4")
			parent.tb2p3LB.setText("Direction +")
			parent.tb2p2LB.setText("Direction -")
			parent.spindleInfo2Lbl.setText("PWM on Dir 4")
			parent.tb2p5LB.setText("PWM +")
			parent.tb2p4LB.setText("PWM -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")

	else:
		parent.spindleGB.setEnabled(False)
		parent.spindleInfoGB.setEnabled(False)
		parent.encoderGB.setEnabled(False)
		parent.spindlepidGB.setEnabled(False)
		parent.spindleInfo1Lbl.setText("No Spindle")
		parent.spindleInfo2Lbl.setText("")
		parent.spindleInfo3Lbl.setText("")
		parent.spindleInfo4Lbl.setText("")

def ssCardChanged(parent):
	sscards = {
	'Select':'No Card Selected',
	'7i64':'24 Outputs, 24 Inputs',
	'7i69':'48 Digital I/O Bits',
	'7i70':'48 Inputs',
	'7i71':'48 Sourcing Outputs',
	'7i72':'48 Sinking Outputs',
	'7i73':'Pendant Card',
	'7i84':'32 Inputs 16 Outputs',
	'7i87':'8 Analog Inputs'
	}

	sspage = {
	'Select':0,
	'7i64':1,
	'7i69':2,
	'7i70':3,
	'7i71':4,
	'7i72':5,
	'7i73':6,
	'7i84':7,
	'7i87':8
	}
	parent.smartSerialInfoLbl.setText(sscards[parent.ssCardCB.currentText()])
	parent.smartSerialSW.setCurrentIndex(sspage[parent.ssCardCB.currentText()])


def ss7i73Changed(parent):
	if parent.ss7i73lcdCB.currentData() == 'w7d': # no LCD
		parent.ss7i73w7Lbl.setText('W7 Down')
		lcd = False
	elif parent.ss7i73lcdCB.currentData() == 'w7u': # LCD
		parent.ss7i73w7Lbl.setText('W7 Up')
		lcd = True
	if parent.ss7i73_keypadCB.currentData()[0] == 'w5d':
		if parent.ss7i73_keypadCB.currentData()[1] == 'w6d': # no keypad
			parent.ss7i73w5Lbl.setText('W5 Down')
			parent.ss7i73w6Lbl.setText('W6 Down')
			keypad = False
		elif parent.ss7i73_keypadCB.currentData()[1] == 'w6u': # 4x8 keypad
			parent.ss7i73w5Lbl.setText('W5 Down')
			parent.ss7i73w6Lbl.setText('W6 Up')
			keypad = True
			keys = '4x8'
	elif parent.ss7i73_keypadCB.currentData()[0] == 'w5u': # 8x8 keypad
			parent.ss7i73w5Lbl.setText('W5 Up')
			parent.ss7i73w6Lbl.setText('W6 Down')
			keypad = True
			keys = '8x8'

	# No LCD No Keypad
	if not lcd and not keypad:
		for i in range(8):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,16):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Input {i+8}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)
		for i in range(8):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,12):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

	# LCD No Keypad
	if lcd and not keypad:
		for i in range(8):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,16):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Input {i+8}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)
		for i in range(4):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# LCD 4x8 Keypad
	if lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# LCD 8x8 Keypad
	if lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# No LCD 4x8 Keypad
	if not lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(8):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

	# No LCD 8x8 Keypad
	if not lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(12):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

def backupFiles(parent):
	if not os.path.exists(parent.configPath):
		parent.machinePTE.setPlainText('Nothing to Back Up')
		return
	backupDir = os.path.join(parent.configPath, 'backups')
	if not os.path.exists(backupDir):
		os.mkdir(backupDir)
	p1 = subprocess.Popen(['find',parent.configPath,'-maxdepth','1','-type','f','-print'], stdout=subprocess.PIPE)
	backupFile = os.path.join(backupDir, f'{datetime.now():%m-%d-%y-%H:%M:%S}')
	p2 = subprocess.Popen(['zip','-j',backupFile,'-@'], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	parent.machinePTE.appendPlainText('Backing up Confguration')
	output = p2.communicate()[0]
	parent.machinePTE.appendPlainText(output.decode())

def fileNew(parent):
	parent.errorMsgOk('Close the Tool,\n Then open', 'Info!')

def fileSaveAs(parent):
	parent.errorMsgOk('Change the Name,\n Then Save', 'Info!')

def copyOutput(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.machinePTE.toPlainText())
	parent.statusbar.showMessage('Output copied to clipboard')

def add_menu(data, menu_obj):
	if isinstance(data, dict):
		for k, v in data.items():
			sub_menu = QMenu(k, menu_obj)
			menu_obj.addMenu(sub_menu)
			add_menu(v, sub_menu)
	elif isinstance(data, list):
		for element in data:
			add_menu(element, menu_obj)
	else:
		action = menu_obj.addAction(data)
		action.setIconVisibleInMenu(False)
