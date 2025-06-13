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

    def update_plots(self, tmit: Dict[str, List[float]], tmit_ave: Dict[str, float],
                     ratios: Dict[str, float], z_pos: Dict[str, float], ref_bpm: str):
        try:
            self.tmit_vs_bsa_plot.clear()
            self.ave_tmit_vs_z_splot.clear()
            self.ratios_vs_z_splot.clear()

            t_keys = list(tmit.keys())
            if not t_keys:
                print("No TMIT keys to plot.")
                return

            num_points = len(tmit.get(t_keys[0], []))
            x_data = list(range(num_points))

            for i, key in enumerate(t_keys):
                try:
                    if ref_bpm in key:
                        continue
                    self.tmit_vs_bsa_plot.plot(x_data, tmit[key], pen=(i, len(t_keys)))
                except Exception as e:
                    print(f"[Plot Error] Could not plot {key}: {e}")

            try:
                ref_key = f"{ref_bpm}:TMIT"
                mk_pen = pg.mkPen(color=(255, 255, 255), width=5, style=QtCore.Qt.DashLine)
                self.tmit_vs_bsa_plot.plot(x_data, tmit[ref_key], pen=mk_pen)
            except Exception as e:
                print(f"[Ref Plot Error] {ref_key} missing or malformed: {e}")

            try:
                self.ave_tmit_vs_z_splot.setData(list(z_pos.values()), list(tmit_ave.values()))
            except Exception as e:
                print(f"[Ave TMIT Plot Error] {e}")

            try:
                self.ratios_vs_z_splot.setData(list(z_pos.values()), list(ratios.values()))
            except Exception as e:
                print(f"[Ratios Plot Error] {e}")

        except Exception as e:
            print(f"[Update Plots Error] {e}")



    def update_ironed_plot(self, updated_tmit_dict: Dict[str, List[float]], ref_bpm: str):
        try:
            self.ironed_tmit_plot.clear()
            t_keys = list(updated_tmit_dict.keys())
            if not t_keys:
                print("No keys in updated_tmit_dict.")
                return

            num_points = len(updated_tmit_dict.get(t_keys[0], []))
            x_data = list(range(num_points))

            for i, key in enumerate(t_keys):
                try:
                    if ref_bpm in key:
                        continue
                    self.ironed_tmit_plot.plot(x_data, updated_tmit_dict[key], pen=(i, len(t_keys)))
                except Exception as e:
                    print(f"[Ironed Plot Error] Key: {key}, Error: {e}")

            try:
                ref_key = f"{ref_bpm}:TMIT"
                mk_pen = pg.mkPen(color=(255, 255, 255), width=5, style=QtCore.Qt.DashLine)
                self.ironed_tmit_plot.plot(x_data, updated_tmit_dict[ref_key], pen=mk_pen)
            except Exception as e:
                print(f"[Ref Ironed Plot Error] {ref_key} missing or malformed: {e}")

        except Exception as e:
            print(f"[Update Ironed Plot Error] {e}")


    def update_ironed_plot_single(self, updated_tmit_dict: Dict[str, List[float]], ref_bpm: str, dev: str):
        try:
            self.ironed_tmit_plot.clear()
            bpms_to_plot = [f"{ref_bpm}:TMIT", f"{dev}:TMIT"]

            num_points = len(updated_tmit_dict.get(bpms_to_plot[0], []))
            x_data = list(range(num_points))

            for i, key in enumerate(bpms_to_plot):
                try:
                    self.ironed_tmit_plot.plot(x_data, updated_tmit_dict[key], pen=(i, len(bpms_to_plot)))
                except Exception as e:
                    print(f"[Single Ironed Plot Error] {key}: {e}")

        except Exception as e:
            print(f"[Update Ironed Single Plot Error] {e}")