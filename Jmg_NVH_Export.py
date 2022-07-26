#---------------------------------------------------------------------
#Name: JMG_NVH_export.py
#Menu-en: NVH Force Export
#Type: Python
#Create: February 25, 2019 JSOL Corporation
#Comment-en: Export toque and force to the CSV file for motor NVH.
#---------------------------------------------------------------------
# -*- coding: utf-8 -*-

import locale
import os
import designer

CSV_VERSION = "1.0.0"
OUTPUT_FILE_PATH = "outputFilePath"
SET_PREFIX = "prefix"
TORQUE_COND_TITLE = "condition_title"
NUM_POLES = "numPoles"
COORD_TYPE = "coord_type"
USE_COPY_CYCLE = "use_copy_cycle"
OUTPUT_FORMAT_TYPE = "output_format_type"
OUTPUT_CASE_TYPE = "output_case_type"
SPECIFIED_CASES = "specified_cases"
EPSILON = 0.000001
OUTPUT_DIMENSION = 3

app = designer.GetApplication()

def main():
	app.SetShowProgressDialog(False)
	if (check_model(app) == False):
		return
	
	parameters = get_parameters_from_dialog(app)
	if (check_dialog_parameters(app, parameters) == False):
		return
	
	output_csv(app, parameters)

def check_model(app):

	model = app.GetCurrentModel()
	study = app.GetCurrentStudy()

	if (model.IsValid() == False):
		message = "No model."
		message_jp = "���f���������܂����B"
		show_error_message(message, message_jp)
		return False

	setList = model.GetSetList()
	if (setList.NumSet()<1):
		message = "There is no set."
		message_jp = "�Z�b�g�������܂����B"
		show_error_message(message, message_jp)
		return False

	if (study.IsValid() == False):
		message = "No study."
		message_jp = "�X�^�f�B�������܂����B"
		show_error_message(message, message_jp)
		return False
	
	motionList = get_conditions(study, "RotationMotion")
	if (len(motionList)<1):
		message = "Current study has no rotation motion condition."
		message_jp = "���X�^�f�B�͉��]�^�������������܂����B"
		show_error_message(message, message_jp)
		return False
	
	torqueList = get_conditions(study, "Torque")
	if (len(torqueList)<1):
		message = "Current study has no torque condition."
		message_jp = "���X�^�f�B�̓g���N�����������܂����B"
		show_error_message(message, message_jp)
		return False
	
	forceList = get_conditions(study, "Force")
	if (len(forceList)<1):
		message = "Current study has no force condition."
		message_jp = "���X�^�f�B�͓d���͏����������܂����B"
		show_error_message(message, message_jp)
		return False
	
	if (study.AnyCaseHasResult() == False):
		message = "Current study has no result."
		message_jp = "���X�^�f�B�͌��ʂ������܂����B"
		show_error_message(message, message_jp)
		return False
	
	if (has_zero_speed(app)==True):
		message = "There is the case that rotation speed is zero. Please review setting."
		message_jp = "���]���x���[���̃P�[�X�������܂��B�ݒ����������Ă��������B"
		show_error_message(message, message_jp)
		return False
	
	return True

def show_error_message(message, message_jp):
	msgdlg = app.CreateDialogBox()
	title = "Error"
	title_jp = "�G���["
	msgdlg.SetTranslation(title, title_jp)
	msgdlg.SetTranslation(message, message_jp)
	msgdlg.SetCancelButtonVisible(False)
	msgdlg.SetTitle(title)
	msgdlg.AddLabel(message)
	msgdlg.Show()

def show_warning_message(message, message_jp):
	msgdlg = app.CreateDialogBox()
	title = "Warning"
	title_jp = "�x��"
	msgdlg.SetTranslation(title, title_jp)
	msgdlg.SetTranslation(message, message_jp)
	msgdlg.SetCancelButtonVisible(False)
	msgdlg.SetTitle(title)
	msgdlg.AddLabel(message)
	msgdlg.Show()

def get_parameters_from_dialog(app):
	dialog = app.CreateDialogBox()
	setup_param_input_dialog(app, dialog)
	dialog.Show()
	return dialog

def setup_param_input_dialog(app, dialog):
	dialogTitle = "JMAG-Designer: NVH Force Export Setting"
	dialogTitle_jp = "JMAG-Designer: NVH�d���͏o�͐ݒ�"
	dialog.SetTranslation(dialogTitle, dialogTitle_jp)

	label_1 = "Output File:"
	label_1_jp = "�o�̓t�@�C��:"
	dialog.SetTranslation(label_1, label_1_jp)

	label_2 = "Set Prefix:"
	label_2_jp = "�Z�b�g�̐擪����:"
	dialog.SetTranslation(label_2, label_2_jp)

	label_3 = "Torque Condition:"
	label_3_jp = "�g���N����:"
	dialog.SetTranslation(label_3, label_3_jp)

	label_4 = "Number of Poles:"
	label_4_jp = "�ɐ�:"
	dialog.SetTranslation(label_4, label_4_jp)

#	label_5 = "Force Coordinates:"
#	label_5_jp = "�ߓ_�͂̍��W�n:"
#	dialog.SetTranslation(label_5, label_5_jp)

	label_5 = "Cycle:"
	label_5_jp = "����:"
	dialog.SetTranslation(label_5, label_5_jp)

	label_6 = "Rectangular"
	label_6_jp = "�������W�n"
	dialog.SetTranslation(label_6, label_6_jp)

#	label_7 = "Cylindrical"
#	label_7_jp = "�~�����W�n"
#	dialog.SetTranslation(label_7, label_7_jp)

	label_8 = "Copy 1 electrical cycle to mechanical cycle"
	label_8_jp = "�d�C�p1���������R�s�[���ċ@�B�p1�������ɂ���"
	dialog.SetTranslation(label_8, label_8_jp)

	label_9 = "Output Cases:"
	label_9_jp = "�o�̓P�[�X:"
	dialog.SetTranslation(label_9, label_9_jp)

	label_10 = "All Cases"
	label_10_jp = "�S�P�[�X"
	dialog.SetTranslation(label_10, label_10_jp)

	label_11 = "Specified Cases (Example: 1, 2, 5-8)"
	label_11_jp = "�w���P�[�X(��: 1, 2, 5-8)"
	dialog.SetTranslation(label_11, label_11_jp)

	label_12 = "Output Format:"
	label_12_jp = "�o�̓t�H�[�}�b�g:"
	dialog.SetTranslation(label_12, label_12_jp)

	label_13 = "Single File Including Torque(Force Coordinates=Cylindrical)"
	label_13_jp = "�g���N�f�[�^�܂�1�t�@�C���o��(�ߓ_�͂̍��W�n=�~�����W�n)"
	dialog.SetTranslation(label_13, label_13_jp)

	label_14 = "File Per Case: Time Domain Tooth Forces(Force Coordinates=Rectangular)"
	label_14_jp = "�P�[�X���ƂɃt�@�C���o��:�����ˑ����e�B�[�X�d����(�ߓ_�͂̍��W�n=�������W�n)"
	dialog.SetTranslation(label_14, label_14_jp)

	label_15 = "File Per Case: Frequency Domain Tooth Forces(Force Coordinates=Rectangular)"
	label_15_jp = "�P�[�X���ƂɃt�@�C���o��:���g���ˑ����e�B�[�X�d����(�ߓ_�͂̍��W�n=�������W�n)"
	dialog.SetTranslation(label_15, label_15_jp)

	dialog.SetTitle(dialogTitle)
	dialog.AddLabel(label_1, 0, 1)
	dialog.AddSaveFilename(OUTPUT_FILE_PATH, "", "", "*.csv", 1, 1)
	dialog.AddLabel(label_2, 0, 1)
	dialog.AddString(SET_PREFIX, "", "TOOTH", 1, 1)
	dialog.AddLabel(label_3, 0, 1)
	dialog.AddComboBox(TORQUE_COND_TITLE, "", torque_condition_title_list(app), 0, 1)
	dialog.AddLabel(label_4, 0, 1)
	dialog.AddInteger(NUM_POLES, "", 4, 1, 1)
	dialog.AddLabel(label_5)
	#dialog.AddRadio(COORD_TYPE, label_7, 1, 1)
	#dialog.AddRadio(COORD_TYPE, label_6, 0, 1)
	dialog.AddCheckBox(USE_COPY_CYCLE, label_8, True, 1, 1)
	dialog.AddLabel("", 0, 1)
	dialog.AddLabel(label_12, 0, 1)
	dialog.AddRadio(OUTPUT_FORMAT_TYPE, label_13, 0, 1)
	dialog.AddRadio(OUTPUT_FORMAT_TYPE, label_14, 1, 1)
	dialog.AddRadio(OUTPUT_FORMAT_TYPE, label_15, 2, 1)
	dialog.AddLabel("", 0, 1)
	dialog.AddLabel(label_9, 0, 1)
	dialog.AddRadio(OUTPUT_CASE_TYPE, label_10, 0, 1)
	dialog.AddRadio(OUTPUT_CASE_TYPE, label_11, 1, 1)
	dialog.AddLabel("", 0, 1)
	dialog.AddIntegerList(SPECIFIED_CASES, "", "1", 1, 1)

def check_dialog_parameters(app, parameters):
	if (parameters.WasCancelled()):
		return False
	if (parameters.GetValue(OUTPUT_FILE_PATH)==""):
		message = "Output file path is invalid."
		message_jp = "�o�̓t�@�C���p�X���s���ł��B"
		show_error_message(message, message_jp)
		return False
	
	model = app.GetCurrentModel()
	setList = model.GetSetList()
	targetSetList = get_target_set(model, parameters)
	if (len(targetSetList)<1):
		message = "Can not find set by the specified prefix."
		message_jp = "�w�肳�ꂽ�������ł̓Z�b�g���������܂����ł����B"
		show_error_message(message, message_jp)
		return False
	
	if (parameters.GetValue(NUM_POLES) % 2 != 0):
		message = "The number of poles is invalid. Please set even number."
		message_jp = "�ɐ����s���ł��B�������ݒ肵�Ă��������B"
		show_error_message(message, message_jp)
		return False
	
	outputCaseType = parameters.GetValue(OUTPUT_CASE_TYPE)
	if (outputCaseType == 1): # Specified Cases
		study = app.GetCurrentStudy()
		caseNoList = parameters.GetValueAsIntegerList(SPECIFIED_CASES)
		caseIndexList = get_caseIndexList_from_caseNoList(study, caseNoList)
		if (len(caseIndexList)==0):
			message = "There is no valid case. Please review the setting on Specified Cases."
			message_jp = "�L���ȃP�[�X�������܂����B�w���P�[�X�̐ݒ����������Ă��������B"
			show_error_message(message, message_jp)
			return False
	
	hasNot1CycleStepCases = False
	hasNot1CycleStepCases = check_has_not_1cycle_step_cases(app, parameters)
	if (hasNot1CycleStepCases):
		message = "Insufficient number of result time steps. The file output must have more than one cycle mechanical angle or more than one cycle electrical angle time step number. Please check the results of the specified cases."
		message_jp = "���ʂ̎��ԃX�e�b�v�����s�\���ł��B�t�@�C���o�͂ɂ�1�����@�B�p���܂���1�����d�C�p���̎��ԃX�e�b�v���ȏ��̌��ʂ��K�v�ł��B�w���P�[�X�̌��ʂ��������Ă��������B"
		show_error_message(message, message_jp)
		return False
	
	return True

def output_csv(app, dialog):
	outputFormatType = dialog.GetValue(OUTPUT_FORMAT_TYPE)
	
	if (outputFormatType == 0):
		output_single_file_including_torque(app, dialog)
	elif (outputFormatType == 1):
		output_time_domain_tooth_forces(app, dialog)
	elif (outputFormatType == 2):
		output_frequency_domain_tooth_forces(app, dialog)
	

def output_single_file_including_torque(app, dialog):
	outputPath = dialog.GetValue(OUTPUT_FILE_PATH)
	file = open(outputPath.decode('utf-8'), 'w')
	
	write_header(file, app, dialog)
	[caseIndexList, noResultCaseIndexList, speedList, avTorqList, startIndices, outX, outYT] = create_torque_data(app, dialog)
	write_torque(file, speedList, avTorqList, outX, outYT)
	wasCanceled = write_force(file, app, dialog, caseIndexList, speedList, avTorqList, startIndices, outX)
	
	file.close()
	
	ShowFinishMessage(app, wasCanceled)

def output_time_domain_tooth_forces(app, dialog):

	## Get app data
	isJap = is_japanese(app)
	targetStudy = app.GetCurrentStudy()
	targetModel = app.GetCurrentModel()

	## Get dialog values
	useElectricCycle = dialog.GetValue(USE_COPY_CYCLE)
	numPoles = dialog.GetValue(NUM_POLES)
	coordType = 0 # Fixed to Global Rectangular
	targetSetList = get_target_set(targetModel, dialog)
	setPrefix = dialog.GetValue(SET_PREFIX).decode('utf-8')

	## Setup parameters
	outputDimension = OUTPUT_DIMENSION
	modelDimension = targetModel.GetDimension()
	is2D = (modelDimension == 2)
	thickness = 0
	useMultiSlice = False
	numSlice = 1
	if (is2D):
		thickness = targetStudy.GetStudyProperties().GetValueWithUnit("ModelThickness", "m")
		useMultiSlice = use_multi_slice(targetStudy)
		numSlice = get_slice_number(targetStudy)
		if (useMultiSlice):
			thickness = 1.0*thickness/numSlice
	caseIndexList = get_case_index_list(dialog, targetStudy)
	periodicity = get_periodicity(targetStudy)
	needConvertTwice = (not is2D) and has_symmetry_boundary_on_XYPlane(targetStudy)

	## Setup progress dialog
	setup_progress(app, outputDimension, caseIndexList, numSlice, targetSetList)
	wasCanceled = False

	## Case loop
	numCases = len(caseIndexList)
	for caseLoopIndex in range(numCases):
		caseIndex = caseIndexList[caseLoopIndex]
		targetStudy.SetCurrentCase(caseIndex)
		removedList = get_removed_node_list_on_boundary(targetStudy, targetSetList)

		if (targetStudy.CaseHasResult(caseIndex) == False):
			continue

		## Slice loop
		for sliceIndex in range(numSlice):

			# Write file
			outputPath = create_file_name(dialog.GetValue(OUTPUT_FILE_PATH), numCases, caseIndex+1, useMultiSlice, sliceIndex+1)
			file = open(outputPath.decode('utf-8'), 'w')

			## Write header
			write_header_for_time_domain_tooth_force_only(file, setPrefix, len(targetSetList)*periodicity)
	
			## Get start index for last 1 cycle
			torqResultName = get_torq_result_name(app)
			dataset = targetStudy.GetDataSet(torqResultName, caseIndex+1)
			startIndex = get_last_1_cycle_start_index(dialog, targetStudy, dataset)
			timeData = list(dataset.GetColumn(0))
			timeData = timeData[startIndex:]
			timeData = create_1_electric_cycle_time_to_1_mechanical_cycle_time(useElectricCycle, numPoles, timeData)
	
			## Each Tooth loop
			fullModelF = []
			partialModelF = []
			for setIndex in range(len(targetSetList)):
				eachSetF = []
	
				## Component loop
				for compIndex in range(outputDimension):
					if (app.UserProgressWasCanceled()):
						app.UserProgressFinish()
						wasCanceled = True
						break
					
					##Setup probe
					title = "Probe"
					probe = create_probe(title, targetStudy, useMultiSlice, sliceIndex, isJap, coordType, compIndex)
					
					[data, wasCanceled] = calc_force(targetStudy, removedList[setIndex], probe)
					
					## Considering 1/2 model lengthwise if symmetry boundary is set on XY plane
					convertedData = convert_twice(needConvertTwice, data)
					
					## Get last 1 cycle data
					lastCycleF = convertedData[startIndex:]
					
					##Copy 1 electric cycle to 1 mechanical cycle
					lastCycleF = copy_1_electric_cycle_to_1_mechanical_cycle(useElectricCycle, numPoles, lastCycleF)
					
					##If 2D model times thickness
					if is2D:
						lastCycleF = [f * thickness for f in lastCycleF]
					
					##Add each component data
					eachSetF.append(lastCycleF)
					
					if (wasCanceled == False):
						app.UserProgressStep()
					
					targetStudy.DeleteProbe(title)
						
				partialModelF.append(eachSetF)
			
			##Add Time
			fullModelF.append(timeData)
			
			##Copy partial model teeth to full model
			for i in range (periodicity):
				fullModelF.append(partialModelF)
		
			##Write TOOTH value of full model
			WriteByAllComponentsInSetForOneCase(file, fullModelF)
			
			file.close()
	
	app.UserProgressFinish()
	
	ShowFinishMessage(app, wasCanceled)

def output_frequency_domain_tooth_forces(app, dialog):
	## Get app data
	isJap = is_japanese(app)
	targetStudy = app.GetCurrentStudy()
	targetModel = app.GetCurrentModel()
	dataManager = app.GetDataManager()

	## Get dialog values
	numPoles = dialog.GetValue(NUM_POLES)
	coordType = 0 # Fixed to Global Rectangular
	targetSetList = get_target_set(targetModel, dialog)
	setPrefix = dialog.GetValue(SET_PREFIX).decode('utf-8')

	## Setup parameters
	outputDimension = OUTPUT_DIMENSION
	modelDimension = targetModel.GetDimension()
	is2D = (modelDimension == 2)
	thickness = 0
	useMultiSlice = False
	numSlice = 1
	if (is2D):
		thickness = targetStudy.GetStudyProperties().GetValueWithUnit("ModelThickness", "m")
		useMultiSlice = use_multi_slice(targetStudy)
		numSlice = get_slice_number(targetStudy)
		if (useMultiSlice):
			thickness = 1.0*thickness/numSlice
	caseIndexList = get_case_index_list(dialog, targetStudy)
	periodicity = get_periodicity(targetStudy)
	needConvertTwice = (not is2D) and has_symmetry_boundary_on_XYPlane(targetStudy)

	## Setup progress dialog
	setup_progress(app, outputDimension, caseIndexList, numSlice, targetSetList)
	wasCanceled = False

	## Case loop
	numCases = len(caseIndexList)
	for caseLoopIndex in range(numCases):
		caseIndex = caseIndexList[caseLoopIndex]
		targetStudy.SetCurrentCase(caseIndex)
		removedList = get_removed_node_list_on_boundary(targetStudy, targetSetList)

		if (targetStudy.CaseHasResult(caseIndex) == False):
			continue

		## Slice loop
		for sliceIndex in range(numSlice):

			## Write file
			outputPath = create_file_name(dialog.GetValue(OUTPUT_FILE_PATH), numCases, caseIndex+1, useMultiSlice, sliceIndex+1)
			file = open(outputPath.decode('utf-8'), 'w')
	
			## Write header
			write_header_for_frequency_domain_tooth_force_only(file, setPrefix, len(targetSetList)*periodicity)
	
			## Get start index for last 1 cycle
			torqResultName = get_torq_result_name(app)
			dataset = targetStudy.GetDataSet(torqResultName, caseIndex+1)
			startIndex = get_last_1_cycle_start_index(dialog, targetStudy, dataset)
	
			## Each Tooth loop
			fullModelF = []
			partialModelF = []
			freqData = []
			for setIndex in range(len(targetSetList)):
				eachSetF = []
	
				## Component loop
				for compIndex in range(outputDimension):
					if (app.UserProgressWasCanceled()):
						app.UserProgressFinish()
						wasCanceled = True
						break
					
					## Setup probe
					title = "Probe"
					probe = create_probe(title, targetStudy, useMultiSlice, sliceIndex, isJap, coordType, compIndex)
					
					dataSetTitle = "fft_for_nvf_force_export"
					[fftDataSet, wasCanceled] = calc_force_with_FFT(dataManager, targetStudy, removedList[setIndex], probe, dataSetTitle, needConvertTwice, startIndex, is2D, thickness)
					
					## Real/Imaginary Loop
					numFFTColmuns = fftDataSet.GetCols()
					if (numFFTColmuns < 3):
						continue
					for realImagIndex in range(1, numFFTColmuns):
						data = list(fftDataSet.GetColumn(realImagIndex))
						##  Add each component data
						eachSetF.append(data)
					
					if (setIndex == 0 and compIndex == 0):
						freqData = list(fftDataSet.GetColumn(0))
					
					if (wasCanceled == False):
						app.UserProgressStep()
					
					targetStudy.DeleteProbe(title)
					dataManager.DeleteDataSet(dataSetTitle)
						
				partialModelF.append(eachSetF)
				
			## Add Time/Frequency
			fullModelF.append(freqData)
			
			## Copy partial model teeth to full model
			for i in range (periodicity):
				fullModelF.append(partialModelF)
	
			## Write TOOTH value of full model
			WriteByAllComponentsInSetForOneCase(file, fullModelF)
			
			file.close()
	
	app.UserProgressFinish()
	
	ShowFinishMessage(app, wasCanceled)

def write_header(file, app, dialog):
	targetModel = app.GetCurrentModel()
	targetStudy = app.GetCurrentStudy()
	is2D = (targetModel.GetDimension()==2)
	setList = targetModel.GetSetList()
	targetSetList = get_target_set(targetModel, dialog)
	numPoles = dialog.GetValue(NUM_POLES)
	dimString = "3D"
	coordString = get_coordName(1) # Fixed to cylindrical in V18.1
	periodicity = get_periodicity(targetStudy)
	numTeeth = int(len(targetSetList)*periodicity)
	modelThickness = 0
	numSlice = 1
	
	if (is2D):
		dimString = "2D"
		modelThickness = targetStudy.GetStudyProperties().GetValueWithUnit("ModelThickness", "mm")
		numSlice = get_slice_number(targetStudy)
	
	write_line2(file, "CSV Version", CSV_VERSION)
	write_line2(file, "Dimension", dimString)
	write_line2(file, "Coordinate", coordString)
	write_line2(file, "Teeth", str(numTeeth))
	if (is2D):
		write_line2(file, "StackLength(mm)", str(modelThickness))
		write_line2(file, "Slice", str(numSlice))
	file.write("\n")

def create_torque_data(app, dialog):
	##Initialize
	speedList = []
	avTorqList = []
	startIndices = []
	caseIndexList = []
	noResultCaseIndexList = []
	outX = []
	outYT = []
	
	##Get dialog parameters
	useElectricCycle = dialog.GetValue(USE_COPY_CYCLE)
	numPoles = dialog.GetValue(NUM_POLES)
	outputCaseType = dialog.GetValue(OUTPUT_CASE_TYPE)
	caseNoList = dialog.GetValueAsIntegerList(SPECIFIED_CASES)
	
	##Get app data
	targetStudy = app.GetCurrentStudy()
	torqResultName = get_torq_result_name(app)
		
	##Create output case list
	numCases = targetStudy.GetDesignTable().NumCases()
	if (outputCaseType == 0):	# Output all cases
		caseIndexList = range(numCases)
	elif (outputCaseType == 1): # Output specified cases
		caseIndexList = get_caseIndexList_from_caseNoList(targetStudy, caseNoList)
	
	##Create each case data
	for caseIndex in caseIndexList:
	
		if (targetStudy.CaseHasResult(caseIndex) == False):
			noResultCaseIndexList.append(caseIndex)
			continue
		
		##Calculate 1 mechanical cycle time from rotation speed
		targetStudy.SetCurrentCase(caseIndex)
		speed = get_speed(targetStudy)
		if (useElectricCycle):
			T = 60.0/speed/numPoles*2
		else :
			T = 60.0/speed
		
		##Get torque data for 1 last cycle
		lastCycleTorq = []
		dataset = targetStudy.GetDataSet(torqResultName, caseIndex+1)
		numSteps = dataset.GetRows()
		if (dataset.GetCols()!=2 or numSteps==0):
			noResultCaseIndexList.append(caseIndex)
			continue
		time = list(dataset.GetColumn(0))
		torque = get_target_torque(dataset, dialog)
		
		lastCycleStartTime = time[-1] - T
		index = len(time)-1
		t = time[index]
		while t > lastCycleStartTime - EPSILON:
			lastCycleTorq.insert(0, torque[index])
			index -= 1
			if (index < 0 or len(time) <= index):
				break
			t = time[index]
		
		##Calculate average torque
		aveTorq = sum(lastCycleTorq)/len(lastCycleTorq)
		
		##Copy 1 electric cycle to 1 mechanical cycle
		lastCycleTorq = copy_1_electric_cycle_to_1_mechanical_cycle(useElectricCycle, numPoles, lastCycleTorq)
		
		##Create angle data
		angleData = []
		deltaAngle = 360.0/(len(lastCycleTorq)-1)
		for i in range(len(lastCycleTorq)):
			angleData.append(deltaAngle*i)
		
		##Set each case data
		speedList.append(speed)
		avTorqList.append(aveTorq)
		startIndices.append(index+1)
		outX.append(angleData)
		outYT.append(lastCycleTorq)
	
	##Remove no result case
	for index in noResultCaseIndexList:
		caseIndexList.remove(index)
	
	return (caseIndexList, noResultCaseIndexList, speedList, avTorqList, startIndices, outX, outYT)

def write_torque(file, speed, aveTorq, outX, outYT):
	##Write torque header
	write_line(file, "*Torque")
	
	##Write torque data per case
	for i in range(len(speed)):
		write_line2(file, "Speed(RPM)", str(speed[i]))
		write_line2(file, "Torque(Nm)", str(aveTorq[i]))
		for j in range(len(outX[i])):
			write_line2(file, str(outX[i][j]), str(outYT[i][j]))
		file.write("\n")

def write_force(file, app, dialog, caseIndexList, speedList, avTorqList, startIndices, outX):
	##Get Study value
	targetModel = app.GetCurrentModel()
	targetStudy = app.GetCurrentStudy()
	isJap = is_japanese(app)
	is2D = (targetModel.GetDimension()==2)
	thickness = 0
	if (is2D):
		thickness = targetStudy.GetStudyProperties().GetValueWithUnit("ModelThickness", "m")
	periodicity = get_periodicity(targetStudy)
	useMultiSlice = use_multi_slice(targetStudy)
	numSlice = 1
	if (useMultiSlice):
		numSlice = get_slice_number(targetStudy)
		thickness = 1.0*thickness/numSlice
	needConvertTwice = (not is2D) and has_symmetry_boundary_on_XYPlane(targetStudy)
	
	##Get dialog parameters
	useElectricCycle = dialog.GetValue(USE_COPY_CYCLE)
	numPoles = dialog.GetValue(NUM_POLES)
	coordType = 1 # Fixed to cylindrical in V18.1
	
	##Pick up target set list
	targetSetList = get_target_set(targetModel, dialog)
	
	
	##Create data for each component and each case
	dimension = app.GetCurrentModel().GetDimension()
	numCases = targetStudy.GetDesignTable().NumCases()
	
	##Setup progress dialog
	setup_progress(app, dimension, caseIndexList, numSlice, targetSetList)
	wasCanceled = False
	
	for compIndex in range(dimension):
		write_line2(file, "*Force", str(compIndex+1))

		for outputIndex in range(len(caseIndexList)):
			caseIndex = caseIndexList[outputIndex]
			targetStudy.SetCurrentCase(caseIndex)
			##Get nodeIds on each set
			removedList = get_removed_node_list_on_boundary(targetStudy, targetSetList)
			
			write_line2(file, "Speed(RPM)", str(speedList[outputIndex]))
			write_line2(file, "Torque(Nm)", str(avTorqList[outputIndex]))
			
			fullModelF=[]
			for sliceIndex in range(numSlice):
				
				##Set probe
				title = "Probe"
				probe = create_probe(title, targetStudy, useMultiSlice, sliceIndex, isJap, coordType, compIndex)
				
				##Calculate TOOTH value
				partialModelF = []
				for setIndex in range(len(targetSetList)):
					if (app.UserProgressWasCanceled()):
						app.UserProgressFinish()
						file.close()
						return True
					
					[data, wasCanceled] = calc_force(targetStudy, removedList[setIndex], probe)
					
					##Considering 1/2 model lengthwise if symmetry boundary is set on XY plane
					convertedData = convert_twice(needConvertTwice, data)
					
					##Get last 1 cycle data
					lastCycleF = convertedData[startIndices[outputIndex]:]
					
					##Copy 1 electric cycle to 1 mechanical cycle
					lastCycleF = copy_1_electric_cycle_to_1_mechanical_cycle(useElectricCycle, numPoles, lastCycleF)
					
					##If 2D model times thickness (How about multi-slice model?)
					if is2D:
						lastCycleF = [f * thickness for f in lastCycleF]
					
					##Add each set data
					partialModelF.append(lastCycleF)
					
					if (wasCanceled == False):
						app.UserProgressStep()
				
				##Copy partial model teeth to full model
				for i in range (periodicity):
					for j in range (len(targetSetList)):
						fullModelF.append(partialModelF[j])
				
				targetStudy.DeleteProbe(title)
				
				if (wasCanceled):
					file.close()
					return True
				
			##Write TOOTH value
			for i in range(len(fullModelF[0])):
				file.write(str(outX[outputIndex][i]) + ",")
				for j in range(len(fullModelF)):
					file.write(str(fullModelF[j][i]))
					if j == len(fullModelF)-1:
						file.write("\n")
					else:
						file.write(",")
			file.write("\n")
	
	app.UserProgressFinish()
	
	return wasCanceled

def write_line(file, str1):
	file.write(str1)
	file.write("\n")

def write_line2(file, str1, str2):
	file.write(str1)
	file.write(",")
	file.write(str2)
	file.write("\n")

def get_speed(targetStudy):
	result = 0;
	motionList = get_conditions(targetStudy, "RotationMotion")
	motion = motionList[0]
	return motion.GetValue("AngularVelocity")

def torque_condition_title_list(app):
	result = []
	torqueList = get_conditions(app.GetCurrentStudy(), "Torque")
	for cond in torqueList:
		result.append(cond.GetName())
	return result

def get_periodicity(targetStudy):
	result=1
	for i in range(targetStudy.NumConditions()):
		cond = targetStudy.GetCondition(i)
		if cond.GetScriptTypeName()=="RotationPeriodicBoundary":
			result = 360//int(cond.GetValue(u"Angle"))
			break
	return result

def get_coordName(coordType):
	result = "Global Rectangular"
	if (coordType == 0):	# 0: Rectangular
		result = "Global Rectangular"
	elif (coordType == 1):		# 1: Cylindrical
		result = "Cylindrical"
	return result

def get_component(coordType, compIndex):
	result = "X"
	if (coordType == 0):	# 0: Rectangular
		if (compIndex==0):
			result = "X"
		elif (compIndex==1):
			result = "Y"
		elif (compIndex==2):
			result = "Z"
	elif (coordType == 1):		# 1: Cylindrical
		if (compIndex==0):
			result = "Radial"
		elif (compIndex==1):
			result = "Theta"
		elif (compIndex==2):
			result = "Z"
	return result

def get_caseIndexList_from_caseNoList(targetStudy, caseNoList):
	result = []
	numCases = targetStudy.GetDesignTable().NumCases()
	for no in caseNoList:
		index = no-1
		if (index>-1 and index<numCases):
			result.append(index)
	return result

def calc_force(targetStudy, removed, probe):
	result = []
	wasCanceled = False
	
	##Set probe on the nodeIds
	if (len(removed)<1):
		return (result, wasCanceled)
	
	tmp = []
	for i in range(len(removed)):
		
		if (app.UserProgressWasCanceled()):
			wasCanceled = True
			return (result, wasCanceled)
		
		id = removed[i]
		probe.ClearPoints()
		probe.SetId(0, id)
		probe.RenamePoint(0, "Node_"+str(id))
		probe.Build()
		dataProbe = probe.GetDataSet()
		
		##Sum on all nodes
		if (dataProbe.GetCols()>1):
			tmp = list(dataProbe.GetColumn(1))
			if (i==0):
				result = tmp
			else :
				result = [x+y for (x,y) in zip(result, tmp)]
	
	return (result, wasCanceled)

def calc_force_with_FFT(dataManager, targetStudy, removed, probe, dataSetTitle, needConvertTwice, startIndex, is2D, thickness):
	wasCanceled = False
	forceData = []
	
	##Set probe on the nodeIds
	if (len(removed)<1):
		return (probe.GetDataSet(), wasCanceled)
	
	tmp = []
	for i in range(len(removed)):
		
		if (app.UserProgressWasCanceled()):
			wasCanceled = True
			return (probe.GetDataSet(), wasCanceled)
		
		id = removed[i]
		probe.ClearPoints()
		probe.SetId(0, id)
		probe.RenamePoint(0, "Node_"+str(id))
		probe.Build()
		dataProbe = probe.GetDataSet()
		
		##Sum on all nodes
		if (dataProbe.GetCols()>1):
			tmp = list(dataProbe.GetColumn(1))
			if (i==0):
				forceData = tmp
			else :
				forceData = [x+y for (x,y) in zip(forceData, tmp)]
	
	## Considering 1/2 model lengthwise if symmetry boundary is set on XY plane
	convertedForceData = convert_twice(needConvertTwice, forceData)
	
	## Get last 1 cycle data
	lastCycleF = convertedForceData[startIndex:]
	timeData = list(dataProbe.GetColumn(0))
	lastCycleT = timeData[startIndex:]
	
	## If 2D model times thickness
	if is2D:
		lastCycleF = [f * thickness for f in lastCycleF]
	
	xData = lastCycleT
	yData = lastCycleF
	xyPairList = []
	xyPair = []
	
	for i in range(len(xData)):
		xyPair = [xData[i],yData[i]]
		xyPairList.append(xyPair)
	dataSet = dataManager.CreateFromDataSet(dataSetTitle, "xtitle", "ytitle", xyPairList)
	fftDataSet = dataManager.CreateFFT(dataSet, 0, "RealAndImaginary", 0, xData[0], xData[-1])
	
	return (fftDataSet, wasCanceled)

def remove_nodes_on_boundary(study, nodeIds):
	condList = get_conditions(study, "RotationPeriodicBoundary")
	if (len(condList)==0):
		return nodeIds
	
	result = []
	cond = condList[0]
	for id in nodeIds:
		if (cond.NodeIsOnTarget(id)==False):
			result.append(id)
	return result

def get_conditions(study, condScriptTypeName):
	result = []
	for i in range(study.NumConditions()):
		cond = study.GetCondition(i)
		typeName = cond.GetScriptTypeName()
		if (typeName == condScriptTypeName):
			result.append(cond)
	return result

def use_multi_slice(study):
	condList = get_ms_conditions(study)
	return len(condList) > 0

def get_ms_conditions(study):
	result = []
	for i in range(study.NumConditions()):
		cond = study.GetCondition(i)
		typeName = cond.GetScriptTypeName()
		if (typeName == "MultiSlice"):
			result.append(cond)
	return result

def get_slice_number(study):
	result = 1
	condList = get_ms_conditions(study)
	if (len(condList)>0):
		cond = condList[0]
		if (cond.IsValid()):
			result = int(cond.GetValue("NumberOfSlices"))
	return result

def get_target_set(targetModel, dialog):
	targetSetList = []
	prefix = dialog.GetValue(SET_PREFIX).decode('utf-8')
	setList = targetModel.GetSetList()
	if (setList.IsValid() == False):
		return targetSetList
	
	for i in range(setList.NumSet()):
		set = setList.GetSet(i)
		if set.IsValid():
			setName = set.GetName()
			if sys.version_info.major == 2:
				setName = setName.decode('utf-8')
			if setName.startswith(prefix):
				targetSetList.append(set)
	return targetSetList

def is_japanese(app):
	lang = app.GetPreference("Language").decode('utf-8')
	if (lang == "Japanese"):
		return True
	elif (lang == "System"):
		localeInfo = locale.getdefaultlocale()
		if ("ja" in localeInfo[0].lower()):
			return True
		else:
			return False
	return False

def get_target_torque(dataset, dialog):
	result = []
	selectedIndex = dialog.GetValue(TORQUE_COND_TITLE)
	titleList = torque_condition_title_list(app)
	targetName = titleList[selectedIndex]
	for i in range(dataset.GetCols()):
		if (dataset.GetColumnName(i)==targetName):
			result = list(dataset.GetColumn(i))
	return result

def has_zero_speed(app):
	targetStudy = app.GetCurrentStudy()
	numCases = targetStudy.GetDesignTable().NumCases()
	for caseIndex in range(numCases):
		targetStudy.SetCurrentCase(caseIndex)
		if (targetStudy.HasResult()==False):
			continue
		motionList = get_conditions(targetStudy, "RotationMotion")
		motion = motionList[0]
		speed = motion.GetValue("AngularVelocity")
		if (speed==0.0):
			return True
	
	return False

def has_symmetry_boundary_on_XYPlane(study):
	condList = get_conditions(study, "SymmetryBoundary")
	for symmetry in condList:
		if symmetry.HasTargetOnXYPlane():
			return True
	return False

def get_case_index_list(dialog, targetStudy):
	caseIndexList = []
	caseNoList = dialog.GetValueAsIntegerList(SPECIFIED_CASES)
	outputCaseType = dialog.GetValue(OUTPUT_CASE_TYPE)
	numCases = targetStudy.GetDesignTable().NumCases()
	if (outputCaseType == 0):	# Output all cases
		caseIndexList = range(numCases)
	elif (outputCaseType == 1): # Output specified cases
		caseIndexList = get_caseIndexList_from_caseNoList(targetStudy, caseNoList)
	return caseIndexList

def check_has_not_1cycle_step_cases(app, parameters):
	result = False
	useElectricCycle = parameters.GetValue(USE_COPY_CYCLE)
	numPoles = parameters.GetValue(NUM_POLES)
	targetStudy = app.GetCurrentStudy()
	torqResultName = get_torq_result_name(app)
	
	caseIndexList = get_case_index_list(parameters, targetStudy)
	for caseIndex in caseIndexList:
		if (targetStudy.CaseHasResult(caseIndex) == False):
			continue
		
		##Calculate 1 mechanical cycle time from rotation speed
		targetStudy.SetCurrentCase(caseIndex)
		speed = get_speed(targetStudy)
		T = get_1_mechanical_cycle_time(speed, useElectricCycle, numPoles)
		
		##Get torque data for 1 last cycle
		lastCycleTorq = []
		dataset = targetStudy.GetDataSet(torqResultName, caseIndex+1)
		numSteps = dataset.GetRows()
		if (dataset.GetCols()!=2 or numSteps==0):
			continue
		time = list(dataset.GetColumn(0))
		if (len(time)<=1):
			result = True
			break
		
		lastCycleStartTime = time[-1] - T + time[1]
		timeScale = time[1]
		if (lastCycleStartTime < -EPSILON * T):
			result = True
			break
	
	return result

def get_torq_result_name(app):
	targetStudy = app.GetCurrentStudy()
	useMultiSlice = use_multi_slice(targetStudy)
	result = "Torque"
	numSlice = 1
	if (useMultiSlice):
		numSlice = get_slice_number(targetStudy)
		if (is_japanese(app)):
			result = "�g���N <���f���S��>"
		else:
			result = "Torque <Whole Model>"
	return result

def get_removed_node_list_on_boundary(targetStudy, targetSetList):
	removedList = []
	for curset in targetSetList:
		selectedIds = []
		sel = curset.GetSelection()
		if sel.NumEdges()>0:
			for i in range(sel.NumEdges()):
				selectedIds.append(sel.EdgeID(i))
		elif sel.NumFaces()>0:
			for i in range(sel.NumFaces()):
				selectedIds.append(sel.FaceID(i))
		
		nodeIds = []
		for entityId in selectedIds:
			if sel.NumEdges()>0:
				nodeIds.extend(targetStudy.GetNodeIdsOnEdge(entityId))
			elif sel.NumFaces()>0:
				nodeIds.extend(targetStudy.GetNodeIdsOnFace(entityId))
		
		##Remove duplicate nodes
		nodeIds = list(set(nodeIds))
		##Remove nodes on boundary
		removedList.append(remove_nodes_on_boundary(targetStudy, nodeIds))

	return removedList

def create_file_name(originalFilePath, numCases, caseNo, useMultiSlice, sliceNo):
	if (useMultiSlice):
		if (numCases > 1):
			absFilePathWithoutExt = os.path.splitext(originalFilePath)[0]
			postFixLabel = b"_Case%d_Slice%d.csv" % (caseNo, sliceNo)
			return (absFilePathWithoutExt + postFixLabel)
		else:
			absFilePathWithoutExt = os.path.splitext(originalFilePath)[0]
			sliceLabel = b"_Slice%d.csv" % sliceNo
			return (absFilePathWithoutExt + sliceLabel)
	else:
		if (numCases > 1):
			absFilePathWithoutExt = os.path.splitext(originalFilePath)[0]
			caseLabel = b"_Case%d.csv" % caseNo
			return (absFilePathWithoutExt + caseLabel)
		else:
			return originalFilePath

def get_1_mechanical_cycle_time(speed, useElectricCycle, numPoles):
	if (speed == 0.0 or numPoles == 0):
		 return 0

	if (useElectricCycle):
		T = 60.0/speed/numPoles*2
	else :
		T = 60.0/speed

	return T

def setup_progress(app, dimension, caseIndexList, numSlice, targetSetList):
	progressLabel = "Exporting to CSV File..."
	if (is_japanese(app)):
		progressLabel = "CSV�t�@�C���֏o�͒�..."
	app.SetupUserProgress(progressLabel)
	app.SetUserProgressUseCancel(True)
	maxSteps = dimension * len(caseIndexList) * numSlice * len(targetSetList)
	app.SetUserProgressMaxSteps(maxSteps)
	app.UserProgressStart()

def create_probe(title, targetStudy, useMultiSlice, sliceIndex, isJap, coordType, compIndex):
	probe = targetStudy.CreateProbe(title)
	probe.SetAutoRecalculate(False)
	subTitle = ""
	if (useMultiSlice):
		if (isJap):
			subTitle = " <�f�� " + str(sliceIndex+1) + ">"
		else:
			subTitle = " <Slice " + str(sliceIndex+1) + ">"
	probe.SetResultType("NodalForce", subTitle)
	probe.SetResultCoordinate(get_coordName(coordType))
	probe.SetComponent(get_component(coordType, compIndex))
	probe.ClearPoints()
	probe.SetProbeType(1)
	probe.SetUseElementValue(True)
	probe.SetMoveWithPart(True)
	return probe

def convert_twice(needConvertTwice, data):
	convertedData = []
	if needConvertTwice:
		convertedData = [n*2 for n in data]
	else:
		convertedData = data
	return convertedData

def copy_1_electric_cycle_to_1_mechanical_cycle(useElectricCycle, numPoles, originalData):
	result = []
	if (useElectricCycle):
		for i in range(numPoles//2):
			if (i == 0):
				result.extend(originalData)
			else:
				result.extend(originalData[1:])
	else:
		result = originalData
	return result

def create_1_electric_cycle_time_to_1_mechanical_cycle_time(useElectricCycle, numPoles, originalData):
	result = []
	offsetData = []
	numSize = len(originalData)
	if (numSize) < 2:
		return result
	
	deltaT = originalData[1] - originalData[0]
	startTime = originalData[0]
	offsetData = []
	for i in range(len(originalData)):
		offsetData.append(i*deltaT)
	lastT = offsetData[-1]

	if (useElectricCycle):
		for i in range(numPoles//2):
			tmp = []
			if (i == 0):
				tmp = offsetData
			else:
				offsetTime = lastT + deltaT
				tmp = [n + offsetTime for n in offsetData][:-1]
				lastT = tmp[-1]
			result.extend(tmp)
	else:
		result = originalData
	return result

def WriteByAllComponentsInSetForOneCase(file, fullModelF):
	for timeIndex in range(len(fullModelF[0])):
		for periodicIndex in range(len(fullModelF)):
			if (periodicIndex == 0): # 0 is time column
				file.write(str(fullModelF[periodicIndex][timeIndex]))
				file.write(",")
			else:
				for eachSetIndex in range(len(fullModelF[periodicIndex])):
					for eachCompIndex in range(len(fullModelF[periodicIndex][eachSetIndex])):
						file.write(str(fullModelF[periodicIndex][eachSetIndex][eachCompIndex][timeIndex]))
						if (periodicIndex == len(fullModelF)-1 and eachSetIndex == len(fullModelF[periodicIndex])-1 and eachCompIndex == len(fullModelF[periodicIndex][eachSetIndex])-1):
							file.write("\n")
						else:
							file.write(",")

def get_last_1_cycle_start_index(dialog, targetStudy, dataset):
	startIndex = 0

	##Get dialog parameters
	useElectricCycle = dialog.GetValue(USE_COPY_CYCLE)
	numPoles = dialog.GetValue(NUM_POLES)

	##Calculate 1 mechanical cycle time from rotation speed
	speed = get_speed(targetStudy)
	T = get_1_mechanical_cycle_time(speed, useElectricCycle, numPoles)
	
	##Get torque data for 1 last cycle
	lastCycleTorq = []
	numSteps = dataset.GetRows()
	if (dataset.GetCols()!=2 or numSteps==0):
		return 0
	time = list(dataset.GetColumn(0))
	
	##Search last 1 cycle start index
	lastCycleStartTime = time[-1] - T
	index = len(time)-1
	t = time[index]
	while t > lastCycleStartTime - EPSILON:
		index -= 1
		if (index < 0 or len(time) <= index):
			break
		t = time[index]
	
	startIndex = index + 1
	return startIndex

def write_header_for_time_domain_tooth_force_only(file, setPrefix, numFullModelSets):
	numComponents = OUTPUT_DIMENSION
	file.write(",")

	##Write a line for set names
	for setIndex in range(numFullModelSets):
		for componentIndex in range(numComponents):
			if (componentIndex == 0):
				setName = setPrefix + " " + str(setIndex+1)
				file.write(setName)
				file.write(",")
			elif (setIndex == numFullModelSets-1 and componentIndex == numComponents-1):
				file.write("\n")
			else:
				file.write(",")

	##Write a line for time and each set components
	file.write("Time")
	file.write(",")
	for setIndex in range(numFullModelSets):
		for componentIndex in range(numComponents):
			componentName = "F" + get_component(0, componentIndex).lower()
			file.write(componentName)

			if (setIndex == numFullModelSets-1 and componentIndex == numComponents-1):
				file.write("\n")
			else:
				file.write(",")

def write_header_for_frequency_domain_tooth_force_only(file, setPrefix, numFullModelSets):
	numComponents = OUTPUT_DIMENSION
	file.write(",")

	##Write a line for set names
	for setIndex in range(numFullModelSets):
		for componentIndex in range(numComponents):
			for realImagIndex in range(2):
				if (componentIndex == 0 and realImagIndex == 0):
					setName = setPrefix + " " + str(setIndex+1)
					file.write(setName)
					file.write(",")
				elif (setIndex == numFullModelSets-1 and componentIndex == numComponents-1 and realImagIndex == 1):
					file.write("\n")
				else:
					file.write(",")

	##Write a line for time and each set components
	file.write("Frequency")
	file.write(",")
	for setIndex in range(numFullModelSets):
		for componentIndex in range(numComponents):
			coordComponentName = "F" + get_component(0, componentIndex).lower()
			for realImagIndex in range(2):
				if (realImagIndex == 0):
					componentName = coordComponentName + "(real)"
				else:
					componentName = coordComponentName + "(imag)"
				file.write(componentName)
				if (setIndex == numFullModelSets-1 and componentIndex == numComponents-1 and realImagIndex == 1):
					file.write("\n")
				else:
					file.write(",")

def ShowFinishMessage(app, wasCanceled):
	message = "The csv file was created.\n"
	message_jp = "CSV�t�@�C�����쐬�����܂����B"
	if (wasCanceled==True):
		message = "The csv file export was canceled.\n"
		message_jp = "CSV�t�@�C���o�͂��L�����Z�������܂����B"
	confirmation = app.CreateDialogBox()
	confirmation.SetTranslation(message, message_jp)
	confirmation.AddLabel(message, 0, 2)
	confirmation.SetCancelButtonVisible(False)
	confirmation.Show()


main()
