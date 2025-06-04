import pyqtgraph as pg
from qtpy import QtCore
from qtpy.QtWidgets import QGridLayout
from typing import Dict, List, Any
class PlotGrid(QGridLayout):
    def __init__(self, y_data=None,y_ave_data = None,num_meas = None,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.tmit_vs_bsa_plot = pg.PlotWidget()
        self.ironed_tmit_plot = pg.PlotWidget()
        self.t1 = pg.PlotWidget()
        self.t2 = pg.PlotWidget()
        self.ave_tmit_vs_z_splot = pg.ScatterPlotItem()
        self.ratios_vs_z_splot = pg.ScatterPlotItem()
        self.t1.addItem(self.ave_tmit_vs_z_splot)
        self.t2.addItem(self.ratios_vs_z_splot)
        self.addWidget(self.tmit_vs_bsa_plot,0,0)
        self.addWidget(self.ironed_tmit_plot,0,1)
        self.addWidget(self.t1,1,0)
        self.addWidget(self.t2,1,1)
        self.setup_plot_titles()

    def setup_plot_titles(self):
        styles_b= {'color':'b', 'font-size':'20px'}
        self.tmit_vs_bsa_plot.setTitle('TMIT vs Time', color='b',size ='27pt')
        self.tmit_vs_bsa_plot.setLabel('left','TMIT (Nel)')
        self.tmit_vs_bsa_plot.setLabel('bottom', 'Pulse #')
    
        styles_r = {'color':'r', 'font-size':'20px'}
        self.t1.setTitle('Average TMIT vs Z', color='r',size ='27pt')
        self.t1.setLabel('left','Average TMIT (Nel)')
        self.t1.setLabel('bottom', 'Z Position of Device')

        styles_g = {'color':'g', 'size':'20px'}
        self.t2.setTitle('TMIT Scale Change vs Z', color='g',size ='27pt')
        self.t2.setLabel('left','TMIT Scale Change')
        self.t2.setLabel('bottom', 'Z Position of Device')
        
        styles_y= {'color':'y', 'font-size':'20px'}
        self.ironed_tmit_plot.setTitle('Ironed TMIT vs Time', color='y',size ='27pt')
        self.ironed_tmit_plot.setLabel('left','Ironed TMIT (Nel)')
        self.ironed_tmit_plot.setLabel('bottom', 'Pulse #')

    def update_plots( self,tmit:Dict[str,List[float]],tmit_ave:Dict[str,float],
                      ratios:Dict[str,float],z_pos:Dict[str,float],ref_bpm:str ):
        self.tmit_vs_bsa_plot.clear()
        self.ave_tmit_vs_z_splot.clear()
        self.ratios_vs_z_splot.clear()
        t_keys = list(tmit.keys())
        num_points = len(tmit[t_keys[0]])
        x_data = []
        for i in range(num_points):
            x_data.append(i)
        for i in range(len(t_keys)):
            try:
                if ref_bpm in t_keys[i]:
                    continue
                else:
                    self.tmit_vs_bsa_plot.plot(x_data,tmit[t_keys[i]],pen=(i,len(t_keys)))
            except Exception:
                print(tmit[t_keys[i]])
        mk_pen = pg.mkPen(color = (255,255,255), width = 5, style = QtCore.Qt.DashLine)
        self.tmit_vs_bsa_plot.plot(x_data,tmit[ref_bpm+':TMIT'],pen=mk_pen)
        self.ave_tmit_vs_z_splot.setData(list(z_pos.values()),list(tmit_ave.values()))
        self.ratios_vs_z_splot.setData(list(z_pos.values()),list(ratios.values()))

    def update_ironed_plot(self,updated_tmit_dict:Dict[str,List[float]],ref_bpm:str):
        self.ironed_tmit_plot.clear()
        t_keys = list(updated_tmit_dict.keys())
        num_points = len(updated_tmit_dict[t_keys[0]])
        x_data = []
        for i in range(num_points):
            x_data.append(i)
        for i in range(len(t_keys)):
            try:
                if ref_bpm in t_keys[i]:
                    continue
                else:
                    self.ironed_tmit_plot.plot(x_data,updated_tmit_dict[t_keys[i]],pen=(i,len(t_keys)))
            except Exception:
                print(updated_tmit_dict[t_keys[i]])
        mk_pen = pg.mkPen(color = (255,255,255), width = 5, style = QtCore.Qt.DashLine)
        self.ironed_tmit_plot.plot(x_data,updated_tmit_dict[ref_bpm+':TMIT'],pen=mk_pen)

    def update_ironed_plot_single(self,updated_tmit_dict,ref_bpm,dev):
        self.ironed_tmit_plot.clear()
        bpms_to_plot = []
        bpms_to_plot.append(ref_bpm+':TMIT')
        bpms_to_plot.append(dev+':TMIT')
        num_points = len(updated_tmit_dict[bpms_to_plot[0]])
        x_data = []
        for i in range(num_points):
            x_data.append(i)
        for i in range(len(bpms_to_plot)):
            self.ironed_tmit_plot.plot(x_data,updated_tmit_dict[bpms_to_plot[i]],pen=(i,len(bpms_to_plot))) 