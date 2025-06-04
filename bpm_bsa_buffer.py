import epics
from edef import BSABuffer
from  datetime import datetime
import time
import numpy as np
class BpmBSABuffer():
    def __init__(self,num_measurements:int,dest_masks:str,dest_mode:str,bpm_list:list,*args,**kwargs):
        self.bpm_bsa_buffer = BSABuffer('Chris BPM Testing', user= 'cgarnier')
        self.buffer_num = self.bpm_bsa_buffer.number
        print('Buffer # : ' ,self.buffer_num)
        self.bpm_bsa_buffer.destination_masks = dest_masks
        self.bpm_bsa_buffer.n_measurements = num_measurements
        # maybe change to self.bsa_destmode_pv and do something with self.put
        self.put_pv = f'BSA:SYS0:1:{self.buffer_num}:DESTMODE'
        self.put = epics.caput(self.put_pv,dest_mode)
        self.bpm_list = bpm_list   

    def update_bpm_list(self,new_bpm_list):
        self.bpm_list = new_bpm_list

    def start_buffer(self):
        self.bpm_bsa_buffer.start()
        print('waiting for buffer  ', datetime.now())
        while epics.caget(f'BSA:SYS0:{self.buffer_num}:HST_READY') == 0:
            time.sleep(.1)
        print('end waiting for buffer ', datetime.now())

    def release_buffer(self):
        self.bpm_bsa_buffer.release()

    def convert_chrg_to_tmit(self,val_in_pc):
        val_in_c = val_in_pc/(np.power(10,12))
        val_in_nel = val_in_c*(6.24257 * np.power(10,18))
        return val_in_nel

    def get_tmit_buffers(self)-> dict: 

        # set up class attributes
        self.bpm_tmit_dictionary = {}
        self.bpm_tmit_averages_dictionary = {}
        self.active_bpm_tmit_pvs = []
        self.pulse_id_data = {}
        #
        bpm_tmit_pvs = []
        # get a list of connected bpms (also toros)
        for bpm in self.bpm_list:
            if bpm.split(':',2)[0] == 'BPMS':
                bpm_tmit_pvs.append(bpm+':TMIT')
            elif bpm.split(':',2)[0] == 'TORO':
                bpm_tmit_pvs.append(bpm+':CHRG')
            else:
                pass
        
        print(bpm_tmit_pvs)

        got_list=epics.caget_many(bpm_tmit_pvs)

        for i in range(len(got_list)):
            if got_list[i] is not None:
                self.active_bpm_tmit_pvs.append(bpm_tmit_pvs[i])
            else:
                print(bpm_tmit_pvs[i], ' ', got_list[i])



        # get tmit data buffer, take the average, and store both in class attributes
        # also store the PID info in class attributes
        print('start getting pids ' , datetime.now())
        for i in range(len(self.active_bpm_tmit_pvs)):
            temp = self.bpm_bsa_buffer.get_data_buffer(self.active_bpm_tmit_pvs[i])
            ### sometimes taking mean of empty obj
            if self.active_bpm_tmit_pvs[i].split(':',2)[0] == 'BPMS':
                ave_tmit = np.mean(temp)
                self.bpm_tmit_dictionary[self.active_bpm_tmit_pvs[i]] = temp
                self.bpm_tmit_averages_dictionary[self.active_bpm_tmit_pvs[i]] = ave_tmit   
                self.pulse_id_data[self.active_bpm_tmit_pvs[i]] = epics.caget(self.active_bpm_tmit_pvs[i]+'PIDHST'+str(self.buffer_num),timeout = 1.5) 

            elif self.active_bpm_tmit_pvs[i].split(':',2)[0] == 'TORO':
                print('Converting bsa data for toroid charge pv from charge in pico-couloumbs to number of electrons.')
                toro_tmit_pv = self.active_bpm_tmit_pvs[i].rsplit(':',1)[0] +':TMIT'
                toro_tmits_from_chrg = []
                for val_in_pc in temp:
                    toro_tmits_from_chrg.append(self.convert_chrg_to_tmit(val_in_pc))

                ave_tmit = np.mean(toro_tmits_from_chrg)
                self.bpm_tmit_dictionary[toro_tmit_pv] = toro_tmits_from_chrg
                self.bpm_tmit_averages_dictionary[toro_tmit_pv] = ave_tmit
                self.pulse_id_data[toro_tmit_pv] = epics.caget(self.active_bpm_tmit_pvs[i]+'PIDHST'+str(self.buffer_num),timeout = 1.5) 
            
        print('end getting pids ', datetime.now())

        return self.bpm_tmit_dictionary, self.bpm_tmit_averages_dictionary, self.pulse_id_data