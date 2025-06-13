import os
from qtpy import QtCore,QtGui
from pydm import Display
from qtpy.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QScrollArea, QGridLayout,QSpacerItem, QSizePolicy, QComboBox,QTableWidget,QHeaderView,QTableWidgetItem,QCheckBox,QMessageBox, QRadioButton
from pydm.widgets import PyDMPushButton
from pydm.widgets.enum_button import PyDMEnumButton
from pydm.utilities.stylesheet import GLOBAL_STYLESHEET
from functools import partial
import epics
import numpy as np
from bpm_bsa_buffer import BpmBSABuffer
from bpm_ironing_cleaning_tool import IroningCleaningTool
from bsa_nord_comparison import BsaNordComparison
from bpm_ironing_tool import BpmIroningTool
from bpm_ironing_plot_grid import PlotGrid
import pprint
from typing import Dict,List,Any
sc_bpm_common_list =[
'BPMS:GUNB:314',
'TORO:GUNB:360',
'BPMS:GUNB:925',
'BPMS:L0B:0183',
'BPMS:HTR:120',
'BPMS:HTR:320',
'BPMS:HTR:365',
'BPMS:HTR:460',
'BPMS:HTR:540',
'BPMS:HTR:760',
'BPMS:HTR:830',
'BPMS:HTR:860',
'BPMS:HTR:960',
'BPMS:HTR:980',
'BPMS:COL0:135',
'BPMS:COL0:240',
'BPMS:COL0:260',
'BPMS:COL0:280',
'BPMS:COL0:320',
'BPMS:COL0:400',
'BPMS:COL0:480',
'BPMS:COL0:560',
'BPMS:COL0:640',
'BPMS:COL0:720',
'BPMS:COL0:800',
'BPMS:COL0:880',
'BPMS:COL0:940',
'BPMS:L1B:0283',
'BPMS:L1B:0383',
'BPMS:L1B:H183',
'BPMS:L1B:H283',
'BPMS:BC1B:125',
'BPMS:BC1B:440',
'BPMS:COL1:120',
'TORO:COL1:125',
'BPMS:COL1:260',
'BPMS:COL1:280',
'BPMS:COL1:320',
'BPMS:COL1:400',
'BPMS:COL1:480',
'BPMS:COL1:560',
'BPMS:COL1:640',
'BPMS:COL1:720',
'BPMS:COL1:800',
'BPMS:COL1:880',
'BPMS:COL1:960',
'BPMS:L2B:0483',
'BPMS:L2B:0583',
'BPMS:L2B:0683',
'BPMS:L2B:0783',
'BPMS:L2B:0883',
'BPMS:L2B:0983',
'BPMS:L2B:1083',
'BPMS:L2B:1183',
'BPMS:L2B:1283',
'BPMS:L2B:1383',
'BPMS:L2B:1483',
'BPMS:L2B:1583',
'BPMS:BC2B:150',
'BPMS:BC2B:530',
'BPMS:EMIT2:150',
'TORO:EMIT2:170',
'BPMS:EMIT2:300',
'BPMS:EMIT2:800',
'BPMS:EMIT2:900',
'BPMS:L3B:1683',
'BPMS:L3B:1783',
'BPMS:L3B:1883',
'BPMS:L3B:1983',
'BPMS:L3B:2083',
'BPMS:L3B:2183',
'BPMS:L3B:2283',
'BPMS:L3B:2383',
'BPMS:L3B:2483',
'BPMS:L3B:2583',
'BPMS:L3B:2683',
'BPMS:L3B:2783',
'BPMS:L3B:2883',
'BPMS:L3B:2983',
'BPMS:L3B:3083',
'BPMS:L3B:3183',
'BPMS:L3B:3283',
'BPMS:L3B:3383',
'BPMS:L3B:3483',
'BPMS:L3B:3583',
'BPMS:EXT:351',
'BPMS:EXT:748',
'BPMS:DOG:120',
'BPMS:DOG:135',
'BPMS:DOG:150',
'BPMS:DOG:165',
'BPMS:DOG:180',
'BPMS:DOG:200',
'BPMS:DOG:215',
'BPMS:DOG:230',
'BPMS:DOG:250',
'BPMS:DOG:280',
'BPMS:DOG:335',
'BPMS:DOG:355',
'BPMS:DOG:405',
'BPMS:DOG:575',
'BPMS:DOG:740',
'BPMS:DOG:910',
'BPMS:BPN13:400',
'BPMS:BPN14:400',
'BPMS:BPN15:400',
'BPMS:BPN16:400',
'BPMS:BPN17:400',
'BPMS:BPN18:400',
'BPMS:BPN19:400',
'BPMS:BPN20:400',
'BPMS:BPN21:400',
'BPMS:BPN22:400',
'BPMS:BPN23:400',
'BPMS:BPN24:400',
'BPMS:BPN25:400',
'BPMS:BPN26:400',
'BPMS:BPN27:400',
'BPMS:BPN28:200',
'BPMS:BPN28:400',
'BPMS:SPD:135']

sc_bsyd_list = [
'BPMS:SPD:255',
'BPMS:SPD:340',
'BPMS:SPD:420', 
'BPMS:SPD:525',
'TORO:SPD:695',
'BPMS:SPD:700',
'BPMS:SPD:955',
'BPMS:SLTD:625',
'BPMS:SLTD:895'
]

sc_diag0= [
'BPMS:DIAG0:210',
'BPMS:DIAG0:190',
'BPMS:DIAG0:230',
'BPMS:DIAG0:270',
'BPMS:DIAG0:285',
'BPMS:DIAG0:330',
'BPMS:DIAG0:370',
'BPMS:DIAG0:390',
'BPMS:DIAG0:470',
'BPMS:DIAG0:520',
'FARC:DIAG0:530'
]

sc_sxr_U_list= [
'BPMS:SPD:255',
'BPMS:SPD:340',
'BPMS:SPD:420',
'BPMS:SPS:572',
'BPMS:SPS:580',
'BPMS:SPS:640',
'BPMS:SPS:710',
'BPMS:SPS:770',
'BPMS:SPS:780',
'BPMS:SPS:830',
'BPMS:SPS:840',
'TORO:SPS:605',
'BPMS:SLTS:150',
'BPMS:SLTS:430',
'BPMS:SLTS:460'
]

sc_sxr_D_list = [
'BPMS:SLTS:460',
'BPMS:SPS:840',
'BPMS:BSYS:865',
'BPMS:LTUS:120',
'BPMS:LTUS:150',
'BPMS:LTUS:180',
'BPMS:LTUS:300',
'BPMS:LTUS:370',
'BPMS:LTUS:450',
'BPMS:LTUS:470',
'BPMS:LTUS:500',
'BPMS:LTUS:510',
'BPMS:LTUS:540',
'BPMS:LTUS:560',
'BPMS:LTUS:570',
'BPMS:LTUS:580',
'BPMS:LTUS:640',
'BPMS:LTUS:660',
'BPMS:LTUS:680',
'BPMS:LTUS:720',
'BPMS:LTUS:730',
'BPMS:LTUS:740',
'BPMS:LTUS:750',
'BPMS:LTUS:760',
'BPMS:LTUS:780',
'BPMS:LTUS:820',
'BPMS:LTUS:840',
'BPMS:LTUS:860',
'BPMS:LTUS:880',
'BPMS:UNDS:1690',
'BPMS:UNDS:1990',
'BPMS:UNDS:2190',
'BPMS:UNDS:2490',
'BPMS:UNDS:2590',
'BPMS:UNDS:2690',
'BPMS:UNDS:2790',
'BPMS:UNDS:2890',
'BPMS:UNDS:2990',
'BPMS:UNDS:3090',
'BPMS:UNDS:3190',
'BPMS:UNDS:3290',
'BPMS:UNDS:3390',
'BPMS:UNDS:3490',
'BPMS:UNDS:3590',
'BPMS:UNDS:3690',
'BPMS:UNDS:3790',
'BPMS:UNDS:3890',
'BPMS:UNDS:3990',
'BPMS:UNDS:4090',
'BPMS:UNDS:4190',
'BPMS:UNDS:4290',
'BPMS:UNDS:4390',
'BPMS:UNDS:4490',
'BPMS:UNDS:4590',
'BPMS:UNDS:4690',
'BPMS:UNDS:4790',
'BPMS:UNDS:5190',
'BPMS:DMPS:325',
'BPMS:DMPS:381',
'BPMS:DMPS:502',
'BPMS:DMPS:693']

sc_hxr_U_list = [
'BPMS:SPH:322',
'BPMS:SPH:345',
'TORO:SPH:365',
'BPMS:SPH:420',
'BPMS:SPH:450',
'BPMS:SPH:520',
'BPMS:SPH:600',
'BPMS:SPH:675',
'BPMS:SPH:760',
'BPMS:SPH:840',
'BPMS:SPH:915',
'BPMS:SPH:940',
'BPMS:SLTH:200',
'BPMS:SLTH:220'
]

sc_hxr_D_list= [
'BPMS:BSYH:445',
'BPMS:BSYH:465',
'BPMS:BSYH:640',
'BPMS:BSYH:735',
'BPMS:BSYH:910',
'BPMS:LTUH:110',
'BPMS:LTUH:120',
'BPMS:LTUH:130',
'BPMS:LTUH:150',
'BPMS:LTUH:170',
'BPMS:LTUH:180',
'BPMS:LTUH:190',
'BPMS:LTUH:250',
'BPMS:LTUH:290',
'BPMS:LTUH:350',
'BPMS:LTUH:390',
'BPMS:LTUH:450',
'BPMS:LTUH:550',
'BPMS:LTUH:640',
'BPMS:LTUH:660',
'BPMS:LTUH:720',
'BPMS:LTUH:730',
'BPMS:LTUH:760',
'BPMS:LTUH:770',
'BPMS:LTUH:860',
'BPMS:LTUH:880',
'BPMS:UNDH:1390',
'BPMS:UNDH:1490',
'BPMS:UNDH:1590',
'BPMS:UNDH:1690',
'BPMS:UNDH:1790',
'BPMS:UNDH:1890',
'BPMS:UNDH:1990',
'BPMS:UNDH:2090',
'BPMS:UNDH:2190',
'BPMS:UNDH:2290',
'BPMS:UNDH:2390',
'BPMS:UNDH:2490',
'BPMS:UNDH:2590',
'BPMS:UNDH:2690',
'BPMS:UNDH:2790',
'BPMS:UNDH:2890',
'BPMS:UNDH:2990',
'BPMS:UNDH:3090',
'BPMS:UNDH:3190',
'BPMS:UNDH:3290',
'BPMS:UNDH:3390',
'BPMS:UNDH:3490',
'BPMS:UNDH:3590',
'BPMS:UNDH:3690',
'BPMS:UNDH:3790',
'BPMS:UNDH:3890',
'BPMS:UNDH:3990',
'BPMS:UNDH:4090',
'BPMS:UNDH:4190',
'BPMS:UNDH:4290',
'BPMS:UNDH:4390',
'BPMS:UNDH:4490',
'BPMS:UNDH:4590',
'BPMS:UNDH:4690',
'BPMS:UNDH:4790',
'BPMS:UNDH:5190',
'BPMS:DMPH:325',
'BPMS:DMPH:381',
'BPMS:DMPH:502',
'BPMS:DMPH:693']

class MainDisplay(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(MainDisplay, self).__init__(parent=parent, args=args, macros=macros)
        self.default_size = (1425, 1250)
        self.setWindowTitle('BPM Ironing GUI')
        self.bpm_dir= os.path.dirname(os.path.realpath(__file__))
        self.bpm_stylesheet= os.path.join(self.bpm_dir, 'bpm_display_stylesheet.qss')
        self.app = QApplication.instance()
        self.app.installEventFilter(self)
        #self.append_stylesheet(self.bpm_stylesheet)
        if macros:
            self.class_macros = macros
            print(macros)
            self.macros()
        self.ref_bpm = 'BPMS:GUNB:314'
        self.target_bpm = 'BPMS:GUNB:314'
        self.target_area = 'GUNB'
        self.default_iron_mode = int(self.class_macros['iron_mode'])
        self.ironing_mode = self.default_iron_mode
        self.dest_mask = ['SC_BSYD']
        self.beamlines = ['SC_BSYD', 'SC_DIAG0','SC_HXR (GUNB-SLTH)', 'SC_HXR (BSYH-DMPH)','SC_SXR (GUNB-SLTS)', 'SC_SXR (SLTS-DMPS)']
        self.ironing_modes = ['All','Area','Single']
        self.run_modes = ['Inclusion','Exclusion','Disable']
        self.bpms_in_line = sc_bpm_common_list+sc_bsyd_list #### this gets updated when a beamline is chosen
        self.bpms_for_bsa = self.bpms_in_line
        self.bold_font = QtGui.QFont()
        self.bold_font.setBold(True)
        self.underlined_font = QtGui.QFont()
        self.underlined_font.setBold(True)
        self.underlined_font.setUnderline(True)
        self.signal_processing_enabled = True
        self.prepped_desk_mask = None

        self.setup_ui() #fine before rework
        self.resize(*self.default_size) #fine before rework
        self.setup_dropdown_info() # commented out signal to show new table
        self.setup_plot_grid() 
        self.setup_control_grid()

    #### main code for setting up ui
    def setup_header(self):
        header_label = QLabel('BPM IRONING')
        return header_label
    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.header_label = self.setup_header()
        self.main_layout.addWidget(self.header_label)
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_widget = QWidget()
        #self.main_widget.setStyleSheet("background-color: white;")
        self.side_widget = QWidget()
        #self.side_widget.setStyleSheet("background-color: white;")
        self.bottom_widget = QWidget()
        #self.bottom_widget.setStyleSheet("background-color: white;")
        self.scroll_layout.addWidget(self.main_widget,0,0,2,2)
        self.scroll_layout.addWidget(self.side_widget,2,1)
        self.scroll_layout.addWidget(self.bottom_widget,2,0)
        #self.scroll_layout.setRowStretch(0,2)
        #self.scroll_layout.setRowStretch(1,2)
        #self.scroll_layout.setColumnStretch(0,2)
        #self.scroll_layout.setColumnStretch(1,1)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)
    def setup_dropdown_info(self):

        self.side_widget_layout = QVBoxLayout()
        self.side_widget.setLayout(self.side_widget_layout)
        self.dropdown = QComboBox()
        self.dropdown.addItem('Average TMIT From BSA')
        self.dropdown.addItem('Wrong Size Nord')
        self.dropdown.addItem('Dev Names of PIDs by Measurement')
        self.dropdown.addItem('Counts of BPMs per Unique PID')
        self.dropdown.addItem('Cleaned TMIT Averages')
        self.dropdown.addItem('Cleaned FW QSCLS')
        self.dropdown.addItem('Cleaned SW QSCLS')
        self.dropdown.addItem('Cleaned TMIT Ratios')
        self.dropdown.addItem('Value of FW QSCL if Ironed')
        self.dropdown.addItem('Value of SW QSCL if Ironed')
        self.dropdown.addItem('Total Failures')
        self.dropdown.currentIndexChanged.connect(self.load_data_table_signal)
        self.side_widget_layout.addWidget(self.dropdown)
        self.data_table = QTableWidget()
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)      
        self.side_widget_layout.addWidget(self.data_table)
        # self.side_widget.installEventFilter(self)
    def setup_control_grid(self):
        ## instantiate and set layout
        self.bottom_widget_layout = QGridLayout()
        self.bottom_widget.setLayout(self.bottom_widget_layout)

        ### instantiate all widget items going into layout set their texts
        widget_header_label = QLabel('Ironing Controls')
        widget_reference_label = QLabel('Reference Device')
        widget_beamline_label = QLabel('Beamline')
        widget_buffer_number = QLabel('BSA Buffer # ')
        self.buffer_num_rdbk = QLabel('# Buffer')
        widget_checkbox_label  = QLabel('Display More Info')
        widget_run_mode_label = QLabel('Ironing Run Mode')
        self.beamline_combo_box = QComboBox()
        for line in self.beamlines:
            self.beamline_combo_box.addItem(line)


        self.radio_buttons = []
        self.radio_widget = QWidget()
        radio_horizontal_layout = QHBoxLayout()
        self.radio_widget.setLayout(radio_horizontal_layout)
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        for i in range(len(self.ironing_modes)):
            radio_button = QRadioButton(self.ironing_modes[i])
            self.radio_buttons.append(radio_button)
            radio_horizontal_layout.addWidget(radio_button)
            radio_button.clicked.connect(self.ironing_mode_toggle)
        radio_horizontal_layout.addItem(spacer_item)

        self.reference_device = QComboBox()
        self.setup_ref_combo_box()
        #self.reference_device.setText(self.ref_bpm)

        self.ironing_single_label = QLabel('Select BPM')
        self.target_device_combo_box = QComboBox()
        self.ironing_area_label = QLabel('Select BPMs by Area')
        self.target_area_combo_box = QComboBox()
        
        
        self.acquisition_ctrl_button = PyDMPushButton('Prepare Ironing')
        self.ironing_ctrl_button = PyDMPushButton('Iron BPMs')     
        self.dropdown_hider = QCheckBox()

        ####make widget setup calls and set additional properties
       
        self.setup_target_device_combo_box()
        self.setup_target_area_combo_box()
        
        self.ironing_single_label.hide()
        self.target_device_combo_box.hide()
        
        self.ironing_area_label.hide()
        self.target_area_combo_box.hide()

        self.dropdown_hider.setChecked(False)
        self.side_widget.hide()

        ### stylize all widgets 
        self.reference_device.setStyleSheet('border: 1px inset #000000; border-radius: 2px; background-color: rgb(236,236,236);')
        
        ### add widgets to layout
        self.bottom_widget_layout.addWidget(widget_header_label,0,0,1,2)
        self.bottom_widget_layout.addWidget(widget_buffer_number,1,0)
        self.bottom_widget_layout.addWidget(self.buffer_num_rdbk,1,1)
        self.bottom_widget_layout.addWidget(widget_reference_label,3,0)
        self.bottom_widget_layout.addWidget(self.reference_device,3,1)
        self.bottom_widget_layout.addWidget(widget_beamline_label,2,0)
        self.bottom_widget_layout.addWidget(self.beamline_combo_box,2,1)
        self.bottom_widget_layout.addWidget(widget_run_mode_label,4,0)
        self.bottom_widget_layout.addWidget(self.radio_widget,4,1)
        self.bottom_widget_layout.addWidget(self.ironing_single_label,5,0)
        self.bottom_widget_layout.addWidget(self.target_device_combo_box,5,1)
        self.bottom_widget_layout.addWidget(self.ironing_area_label,6,0)
        self.bottom_widget_layout.addWidget(self.target_area_combo_box,6,1)
        self.bottom_widget_layout.addWidget(self.acquisition_ctrl_button,7,0,1,2)
        self.bottom_widget_layout.addWidget(self.ironing_ctrl_button,8,0,1,2)
        self.bottom_widget_layout.addWidget(widget_checkbox_label,9,0)
        self.bottom_widget_layout.addWidget(self.dropdown_hider,9,1)

        #### give widgets signals 
        self.setup_default_ironing_mode() ## sets up default but should also trigger clicked
        self.dropdown_hider.stateChanged.connect(self.set_side_widget_vis)
        self.beamline_combo_box.currentIndexChanged.connect(self.set_dest_mask)


        self.reference_device.currentIndexChanged.connect(self.set_ref_bpm)
        
        self.acquisition_ctrl_button.clicked.connect(self.preparation_button_signal)
        self.target_device_combo_box.currentIndexChanged.connect(self.update_target_device)
        self.target_area_combo_box.currentIndexChanged.connect(self.update_target_area)
        self.ironing_ctrl_button.clicked.connect(self.ironing_button_signal)
        #self.ironing_single_target_ctrl_button.clicked.connect(self.ironing_single_signal)
    
    
    
    ### setup the gride for plots
    def setup_plot_grid(self):
        temp_num = int(self.class_macros['num'])
        self.plot_grid = PlotGrid()
        self.main_widget.setLayout(self.plot_grid)

    ##### signals for ctrls box
    ## for dest_mask
    def set_dest_mask(self):
        index = self.beamline_combo_box.currentIndex()
        dest_mask = self.beamline_combo_box.itemText(index)
        #print(dest_mask.split(' ',1)[0])
        self.dest_mask = [dest_mask.split(' ',1)[0]]
        print(self.dest_mask)
        if dest_mask == 'SC_BSYD':
            self.bpms_in_line = sc_bpm_common_list + sc_bsyd_list
            self.ref_bpm = self.bpms_in_line[0]
            #self.target_bpm = self.bpms_in_line[-1]
            self.setup_ref_combo_box()
            self.setup_target_device_combo_box()
            self.setup_target_area_combo_box()
        elif dest_mask == 'SC_DIAG0':
            self.bpms_in_line = sc_bpm_common_list + sc_diag0
            self.ref_bpm = self.bpms_in_line[0]
            #self.target_bpm = self.bpms_in_line[-1]
            self.setup_ref_combo_box()
            self.setup_target_device_combo_box()
            self.setup_target_area_combo_box()
        elif dest_mask == 'SC_SXR (GUNB-SLTS)':
            self.bpms_in_line = sc_bpm_common_list + sc_sxr_U_list
            self.ref_bpm = self.bpms_in_line[0]
            #self.target_bpm = self.bpms_in_line[-1]
            self.setup_ref_combo_box()
            self.setup_target_device_combo_box()
            self.setup_target_area_combo_box()
        elif dest_mask == 'SC_SXR (SLTS-DMPS)':
            self.bpms_in_line = sc_sxr_D_list
            self.ref_bpm = self.bpms_in_line[0]
            self.target_bpm = self.bpms_in_line[-1]
            self.setup_ref_combo_box()
            self.setup_target_device_combo_box()
            self.setup_target_area_combo_box()
        elif dest_mask == 'SC_HXR (GUNB-SLTH)':
            self.bpms_in_line = sc_bpm_common_list + sc_hxr_U_list
            self.ref_bpm = self.bpms_in_line[0]
            #self.target_bpm = self.bpms_in_line[-1]
            self.setup_ref_combo_box()
            self.setup_target_device_combo_box()
            self.setup_target_area_combo_box()
        elif dest_mask == 'SC_HXR (BSYH-DMPH)':
            self.bpms_in_line = sc_hxr_D_list
            self.ref_bpm = self.bpms_in_line[0]
            #self.target_bpm = self.bpms_in_line[-1]
            self.setup_ref_combo_box()
            self.setup_target_device_combo_box()
            self.setup_target_area_combo_box()
        print(self.ref_bpm)

    #### setup helper functions
    def setup_default_ironing_mode(self):
        self.radio_buttons[self.default_iron_mode].setChecked(True)
        self.ironing_mode_toggle()

    def setup_target_device_combo_box(self):
        self.target_device_combo_box.clear()
        temp_list = self.bpms_in_line
        for device in temp_list:
            #devices look like 'BPMS:GUNB:314' or 'TORO:COL1:125'
            #dev_type looks like 'BPMS' or 'TORO'
            dev_type = device.split(':',2)[0]
            if dev_type == 'BPMS':
                self.target_device_combo_box.addItem(device)
    
    def setup_target_area_combo_box(self):
        self.target_area_combo_box.clear()
        temp_list = self.bpms_in_line
        area_list = []
        for temp in temp_list:
            dev_type = temp.split(':',2)[0]
            if dev_type != 'BPMS':
                continue
            else:
                area = temp.split(':',2)[1]
                if area not in area_list:
                    if 'BPN' in area and 'BPN' not in area_list:
                        area_list.append('BPN')
                    elif 'BPN' in area and 'BPN' in area_list:
                        continue
                    else:
                        area_list.append(area)
        for area in area_list:
            self.target_area_combo_box.addItem(area)

    def ironing_mode_toggle(self):
        if self.radio_buttons[0].isChecked():
            self.ironing_mode = 0
            self.ironing_single_label.hide()
            self.target_device_combo_box.hide()
            self.ironing_area_label.hide()
            self.target_area_combo_box.hide()
            self.bpms_for_bsa = self.update_bpms_for_buffer(self.ironing_mode,self.ref_bpm,self.target_bpm,self.target_area)
            #print(self.bpms_for_bsa)
        elif self.radio_buttons[1].isChecked():
            self.ironing_mode = 1
            self.setup_target_area_combo_box()
            self.ironing_area_label.show()
            self.target_area_combo_box.show()
            self.ironing_single_label.hide()
            self.target_device_combo_box.hide()
            self.bpms_for_bsa = self.update_bpms_for_buffer(self.ironing_mode,self.ref_bpm,self.target_bpm,self.target_area)
        elif self.radio_buttons[2].isChecked():
            self.ironing_mode = 2
            self.setup_target_device_combo_box()
            self.ironing_single_label.show()
            self.target_device_combo_box.show()
            self.ironing_area_label.hide()
            self.target_area_combo_box.hide()  
            self.bpms_for_bsa = self.update_bpms_for_buffer(self.ironing_mode,self.ref_bpm,self.target_bpm,self.target_area)  

    ##for ref_bpm
    def set_ref_bpm(self):
        self.ref_bpm = self.reference_device.currentText()
        print('setting ref bpm')
        self.bpms_for_bsa = self.update_bpms_for_buffer(self.ironing_mode,self.ref_bpm,self.target_bpm,self.target_area)

    def setup_ref_combo_box(self):
        self.reference_device.clear()
        temp_list = self.bpms_in_line
        for device in temp_list:
            self.reference_device.addItem(device)

    ## for target_bpm
    def update_target_device(self):
        self.target_bpm = self.target_device_combo_box.currentText()
        self.bpms_for_bsa = self.update_bpms_for_buffer(self.ironing_mode,self.ref_bpm,self.target_bpm,self.target_area)

    ## or target area
    def update_target_area(self):
        self.target_area = self.target_area_combo_box.currentText()
        self.bpms_for_bsa = self.update_bpms_for_buffer(self.ironing_mode,self.ref_bpm,self.target_bpm,self.target_area)
    
    ## after selection of of ironing mode the signal will also call a function that updates the bpms passed to the BSABufferClass
    def update_bpms_for_buffer(self,mode,ref_device,target_device,target_area):
        #print('ironing mode = ', mode)
        #print('ref_device = ', ref_device)
        #print('target device= ', target_device)
        #print('target_area = ', target_area)
        if mode == 0:
            bpms = []
            bpms.append(ref_device)
            for device in self.bpms_in_line:
                if device.split(':',2)[0] == 'BPMS':
                    bpms.append(device)
        elif mode == 1:
            bpms = []
            bpms.append(ref_device)
            for bpm in self.bpms_in_line:
                if target_area in bpm.split(':',2)[1] and bpm.split(':',2)[0] == 'BPMS':
                    bpms.append(bpm)
        elif mode == 2:
            bpms = []
            bpms.append(ref_device)
            if ref_device != target_device:
                bpms.append(target_device)

        #print('list of devices to use!!: ',  bpms)
        return bpms   
    
    ##misc
    def set_side_widget_vis(self):
        if self.side_widget.isHidden():
            self.side_widget.show()
        else:
            self.side_widget.hide()
    def show_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Ironing Dialog Box')
        msg_box.setText('Warning!!\nThe device entered is not valid,\nplease select a valid device.')
        msg_box.setStandardButtons(QMessageBox.Ok)
        result = msg_box.exec()
    
    ##### loading functions for side widget dropdown box
    def load_data_table_signal(self,index):
        self.data_table.clearContents()
        selected_item = self.dropdown.currentText()
        if selected_item == 'Average TMIT From BSA':
            if hasattr(self.bsa_buffer,'bpm_tmit_averages_dictionary'):
                self.load_data_table_from_dictionary(self.bsa_buffer.bpm_tmit_averages_dictionary)
        if selected_item == 'Wrong Size Nord':
            if hasattr(self,'wrong_size_nord_dictionary'):
                self.load_data_table_from_dictionary(self.wrong_size_nord_dictionary)
        if selected_item  ==  'Counts of BPMs per Unique PID':
             if hasattr(self,'bpm_pid_counts_by_meas'):
                 self.load_data_table_from_nested_dictionary(self.bpm_pid_counts_by_meas)
        if selected_item  ==  'Dev Names of PIDs by Measurement':
            if hasattr(self,'bpm_pid_devs_by_meas'):
                self.load_data_table_from_nested_dictionary(self.bpm_pid_devs_by_meas)
        if selected_item == 'Cleaned TMIT Averages':
            if hasattr(self,'bpm_ave_tmits'):
                self.load_data_table_from_dictionary(self.bpm_ave_tmits)
        if selected_item == 'Cleaned FW QSCLS':
            if hasattr(self,'bpm_fw_scl_pvs'):
                self.load_data_table_from_dictionary(self.bpm_fw_scl_pvs)       
        if selected_item == 'Cleaned SW QSCLS':
            if hasattr(self,'bpm_sw_scl_pvs'):
                self.load_data_table_from_dictionary(self.bpm_sw_scl_pvs)
        if selected_item == 'Cleaned TMIT Ratios':
            if hasattr(self,'tmits_ratiod_to_ref'):
                self.load_data_table_from_dictionary(self.tmits_ratiod_to_ref)
        if selected_item == 'Value of FW QSCL if Ironed':
            if hasattr(self,'put_fwscl_vals'):
                self.load_data_table_from_dictionary(self.put_fwscl_vals) 
        if selected_item == 'Value of SW QSCL if Ironed':
            if hasattr(self,'put_swscl_vals'):
                self.load_data_table_from_dictionary(self.put_swscl_vals) 
        if selected_item == 'Total Failures':
            if hasattr(self,'total_failures'):
                # This does not load correctly for total failures.... despite total failures being a real dict.
                # recommend doeing something else
                self.load_data_table_from_nested_dictionary(self.total_failures) 
    def load_data_table_from_dictionary(self,pv_dict):
        ### will need to fix this to make it quicker but for now just do the same thing with QLabels
        self.data_table.setRowCount(len(pv_dict))
        self.data_table.setColumnCount(2)
        for row, (key,value) in enumerate(pv_dict.items()):
            key = str(key)
            value = str(value)
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(value)
            self.data_table.setItem(row,0,key_item)
            self.data_table.setItem(row,1,value_item)
        self.data_table.resizeColumnsToContents()
    def load_data_table_from_nested_dictionary(self,nested_dict):
        #print(nested_dict)
        
        self.data_table.setRowCount(len(nested_dict))
        self.data_table.setColumnCount(10)
        items = list(nested_dict.items())
        for i,j in items:
            if isinstance(j,dict):
                for row, (key,value) in enumerate(j.items()):
                    if isinstance(value,list):
                        key = str(key)
                        #value = str(value)
                        key_item = QTableWidgetItem(key)
                        value_item = QComboBox()
                        for dev in value:
                            str(dev)
                            value_item.addItem(dev)
                        self.data_table.setItem(i,2*row,key_item)
                        self.data_table.setCellWidget(i,2*row+1,value_item)
                    else:
                        key = str(key)
                        value = str(value)
                        key_item = QTableWidgetItem(key)
                        value_item = QTableWidgetItem(value)
                        self.data_table.setItem(i,2*row,key_item)
                        self.data_table.setItem(i,2*row+1,value_item)
                
        self.data_table.resizeColumnsToContents()  

    ##### functions for ironing and ironing preparation

    def preparation_button_signal(self):
        ''' 
        This function gathers all relevant device information and values, and stores them in dictionaries.
        The dictionaries are checked to ensure the data acquired is up the standard previously chosen by Sonya.
        If it isn't is is the device that has failed data is discarded from the list of BPMS to iron.
        '''
        self.acquisition_ctrl_button.setText('Processing... Please wait for plots to load')
        self.acquisition_ctrl_button.setEnabled(False)
        self.acquisition_ctrl_button.blockSignals(True)
        self.acquisition_ctrl_button.setStyleSheet('background-color:blue')
        self.acquisition_ctrl_button.repaint()
        ### before setup bsa buffer need to a function to grab only selected bpms. change the passing of self.bpms_in_line to the return of this function
        # set the prepped dest_mask used for determining if SW Ironing should also happen
        index = self.beamline_combo_box.currentIndex()
        self.prepped_desk_mask = self.beamline_combo_box.itemText(index)  
        self.setup_bsa_buffer()
        self.prep_all_assets()





        self.acquisition_ctrl_button.setStyleSheet('')
        self.acquisition_ctrl_button.setEnabled(True)
        self.acquisition_ctrl_button.blockSignals(False)
        self.acquisition_ctrl_button.setText('Prepare Ironing')


    def setup_bsa_buffer(self):
        '''
        Sets up a bsa buffer and gathers tmit information like average tmit of the device over the number of measurements taken. 
        self.bpm_tmits is 
        '''
        self.num = int(self.class_macros['num'])
        print('using: ', self.bpms_for_bsa)
        self.bsa_buffer = BpmBSABuffer( self.num,self.dest_mask,self.class_macros['mode'],self.bpms_for_bsa)
        self.buffer_num_rdbk.setText(str(self.bsa_buffer.buffer_num))
        self.buffer_num_rdbk.repaint()
        self.bsa_buffer.start_buffer()
        self.bpm_tmits, self.bpm_ave_tmits, self.pulse_id_data = self.bsa_buffer.get_tmit_buffers()
        #pprint.pprint(self.bpm_tmits)
        #pprint.pprint(self.bpm_ave_tmits)
        #pprint.pprint(self.pulse_id_data)
        self.bsa_buffer.release_buffer()
        
        ######
        #setup buffer should really only be setting up the buffer
        #prep all assets should handle all cleaning, and the cleaning should be done by one tool, not two.
        # need to combine cleaning from BPMIroningTool and BsaNordComparison into one tool
        # after combining and ensure it works. 
        # have the buffer acquisition happen on another thread and lock the button. 
        # the other thread will do the work and call back to the button to repaint
    def prep_all_assets(self):
        '''
        Sends pulse_id_data and bpm_tmit to IroningCleaningTool and returns dictionaries that are cleaned of all failures.
        These attributes are used in the dropdown menus.
        '''
        self.cleaning_tool = IroningCleaningTool(self.pulse_id_data,self.bpm_tmits,self.bpm_ave_tmits,self.num)
        self.cleaning_tool.clean_signals()
        #self.wrong_size_nord_dictionary = self.cleaning_tool.return_valid_dictionaries()
        ( self.wrong_size_nord_dictionary, self.cleaned_pid_dict, self.cleaned_tmit_dict, self.cleaned_ave_tmits_dict,
          self.bpm_pid_counts_by_meas, self.bpm_pid_devs_by_meas, self.total_failures ) = self.cleaning_tool.return_all_dictionaries()
        print('printing total failures')
        pprint.pprint(self.total_failures)
        #pprint.pprint(self.wrong_size_nord_dictionary)
        #pprint.pprint(self.cleaned_pid_dict)
        #pprint.pprint(self.cleaned_tmit_dict)
        #pprint.pprint(self.bpm_pid_counts_by_meas)
        #pprint.pprint(self.bpm_pid_devs_by_meas)

        self.create_scl_pv_dicts(self.cleaned_tmit_dict)

        self.ironing_tool = BpmIroningTool()
        #TODO: change the name of this functio call
        self.tmits_ratiod_to_ref = self.ironing_tool.create_tmits_ratiod_dict(self.ref_bpm,self.cleaned_ave_tmits_dict)
        pprint.pprint(self.tmits_ratiod_to_ref)
        #TODO: get ratios for plotting
        # then plot signals?
        self.plot_grid.update_plots( self.cleaned_tmit_dict,self.cleaned_ave_tmits_dict,
                                     self.tmits_ratiod_to_ref,self.z_pos_pvs,self.ref_bpm )
        self.put_fwscl_vals = self.ironing_tool.create_put_scl_vals_dict(self.tmits_ratiod_to_ref,self.bpm_fw_scl_pvs,':FW:QSCL',self.ref_bpm)
        self.put_swscl_vals = self.ironing_tool.create_put_scl_vals_dict(self.tmits_ratiod_to_ref,self.bpm_sw_scl_pvs,':QSCL',self.ref_bpm)
        pprint.pprint(self.put_fwscl_vals)
        pprint.pprint(self.put_swscl_vals)




    def create_scl_pv_dicts(self,tmit_dict:Dict[str,Any]):

        # set up class attributes for plotting
        self.z_pos_pvs = {}
        self.bpm_fw_scl_pvs = {}
        self.bpm_sw_scl_pvs = {}
        #
        z_pos_pvs = []
        fw_scl_pvs = []
        sw_scl_pvs = []

        tmit_dict_key_list = [key for key in tmit_dict.keys()]
        for key in tmit_dict_key_list:
            key = key.rsplit(':',1)[0]
            #TODO: do something about TOROIDS here
            z_pos_pvs.append(key + ':Z')
            fw_scl_pvs.append(key +':FW:QSCL')
            sw_scl_pvs.append(key +':QSCL')

        got_z_pos = epics.caget_many(z_pos_pvs,timeout = 1)  
        got_fw_scl =  epics.caget_many(fw_scl_pvs,timeout = 1) 
        got_sw_scl =  epics.caget_many(sw_scl_pvs,timeout = 1) 

        for i in range(len(got_z_pos)):
            self.z_pos_pvs[z_pos_pvs[i]]=got_z_pos[i]
            self.bpm_fw_scl_pvs[fw_scl_pvs[i]]=got_fw_scl[i]
            self.bpm_sw_scl_pvs[sw_scl_pvs[i]]=got_sw_scl[i]

        # pprint.pprint(self.z_pos_pvs)
        # pprint.pprint(self.bpm_fw_scl_pvs)
        # pprint.pprint(self.bpm_sw_scl_pvs)

        #TODO: should be no additionally None values here but it doesn't hurt to do a check anyways.
    '''print(len(self.bpm_tmits),' ',len(self.bpm_ave_tmits), ' ' ,len(self.bpm_fw_scls),' ' , len(self.bpm_sw_scls) )'''
    def ironing_button_signal(self):
        self.ironing_ctrl_button.setText('Processing... Please wait for plots to load')
        self.ironing_ctrl_button.setEnabled(False)
        self.ironing_ctrl_button.setStyleSheet('background-color:blue')
        self.ironing_ctrl_button.repaint()
        self.iron_bpms(self.ironing_mode)
        self.setup_bsa_buffer()
        # need to grab new bpm tmits from bsa? maybe clean here or maybe its unnecessary? 
        # TODO: maybe change how cleaning_tool.clean_signals work to take arbitrary dictionaries and clean them?
        self.plot_grid.update_ironed_plot(self.bpm_tmits,self.ref_bpm)

        self.ironing_ctrl_button.setStyleSheet('')
        self.ironing_ctrl_button.setEnabled(True)
        self.ironing_ctrl_button.setText('Iron BPMs')
    def iron_bpms(self,mode):
         # The dictionary should be different depending on mode 1 or 2, coul simplify or make it explicit its the same action
        if mode == 0:          
            self.ironing_tool.iron_devices(self.put_fwscl_vals)
            if self.prepped_desk_mask not in ['SC_SXR (SLTS-DMPS)','SC_HXR (BSYH-DMPH)']:            
                self.ironing_tool.iron_devices(self.put_swscl_vals)
            else:
                print('Do not attempt to iron downstream bpms')
        elif mode == 1:
            self.ironing_tool.iron_devices(self.put_fwscl_vals)
            if self.prepped_desk_mask not in ['SC_SXR (SLTS-DMPS)','SC_HXR (BSYH-DMPH)']:            
                self.ironing_tool.iron_devices(self.put_swscl_vals)
            else:
                print('Do not attempt to iron downstream bpms')
            #print(traceback.format_exc())
        elif mode == 2:
            self.ironing_tool.iron_single_device(self.put_fwscl_vals,self.target_bpm,':FW:QSCL')
            if self.prepped_desk_mask not in ['SC_SXR (SLTS-DMPS)','SC_HXR (BSYH-DMPH)']:
                self.ironing_tool.iron_single_device(self.put_swscl_vals,self.target_bpm,':QSCL')
            else:
                print('Do not attempt to iron the SW on downstream bpms')