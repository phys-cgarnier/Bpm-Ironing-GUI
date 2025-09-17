import epics
from edef import BSABuffer
from  datetime import datetime
import time
import numpy as np
from global_config import LOGGER
class BpmBSABuffer():
    def __init__(self,num_measurements:int,dest_masks:str,dest_mode:str,bpm_list:list,*args,**kwargs):
        self.bpm_bsa_buffer = BSABuffer(name='Chris BPM Testing', user= 'cgarnier')
        self.buffer_num = self.bpm_bsa_buffer.number
        LOGGER.info('Buffer # : %s', self.buffer_num)
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
        LOGGER.info('waiting for buffer  %s', datetime.now())
        while epics.caget(f'BSA:SYS0:{self.buffer_num}:HST_READY') == 0:
            LOGGER.info('buffer not ready yet %s', datetime.now())
            time.sleep(.5)
        LOGGER.info('end waiting for buffer %s', datetime.now())

    def release_buffer(self):
        self.bpm_bsa_buffer.release()

    def convert_chrg_to_tmit(self,val_in_pc):
        val_in_c = val_in_pc/(np.power(10,12))
        val_in_nel = val_in_c*(6.24257 * np.power(10,18))
        return val_in_nel

    def get_tmit_buffers(self) -> dict:
        # Output structures
        self.bpm_tmit_dictionary = {}
        self.bpm_tmit_averages_dictionary = {}
        self.active_bpm_tmit_pvs = []
        self.pulse_id_data = {}
        self.failed_devices = {}
        bpm_tmit_pvs = []

        # Step 1: Build list of measurement PVs
        for bpm in self.bpm_list:
            prefix = bpm.split(':', 2)[0]
            if prefix == 'BPMS':
                bpm_tmit_pvs.append(bpm + ':TMIT')
            elif prefix == 'TORO':
                bpm_tmit_pvs.append(bpm + ':CHRG')
            else:
                reason = "Unknown prefix (not BPMS or TORO)"
                LOGGER.warning('%s: %s', bpm, reason)
                self.failed_devices[bpm] = reason

        LOGGER.info('Attempting caget_many on %d PVs...', len(bpm_tmit_pvs))
        try:
            got_list = epics.caget_many(bpm_tmit_pvs)
            if got_list is None:
                reason = "caget_many returned None (CA server may be down)"
                for pv in bpm_tmit_pvs:
                    self.failed_devices[pv] = reason
                return {}, {}, {}
        except Exception as e:
            for pv in bpm_tmit_pvs:
                self.failed_devices[pv] = f"Exception during caget_many: {e}"
            return {}, {}, {}

        # Step 2: Check which PVs returned usable values
        for pv, val in zip(bpm_tmit_pvs, got_list):
            if val is not None:
                self.active_bpm_tmit_pvs.append(pv)
            else:
                reason = "Initial caget returned None"
                LOGGER.warning('%s: %s', pv, reason)
                self.failed_devices[pv] = reason

        if not self.active_bpm_tmit_pvs:
            LOGGER.error("No active BPM TMIT PVs found.")
            return {}, {}, {}, self.failed_devices

        LOGGER.info('%d active PVs found. Fetching BSA data...', len(self.active_bpm_tmit_pvs))

        # Step 3: Get buffer data
        for pv in self.active_bpm_tmit_pvs:
            try:
                tmit_buffer = self.bpm_bsa_buffer.get_data_buffer(pv)
                epics_tmit_buffer = epics.caget(f"{pv}HST{self.buffer_num}",timeout=1.5)
                if tmit_buffer is None or len(tmit_buffer) == 0:
                    LOGGER.info(f"{pv} with tmit_buffer {tmit_buffer} and epics buffer {epics_tmit_buffer}")
                    reason = "Empty or None tmit buffer"
                    LOGGER.warning(f"{pv}: {reason}")
                    self.failed_devices[pv] = reason
                    continue

                prefix = pv.split(':', 2)[0]

                if prefix == 'BPMS':
                    ave_tmit = np.mean(tmit_buffer)
                    self.bpm_tmit_dictionary[pv] = tmit_buffer
                    self.bpm_tmit_averages_dictionary[pv] = ave_tmit
                    pid_pv = pv + 'PIDHST' + str(self.buffer_num)

                elif prefix == 'TORO':
                    toro_tmit_pv = pv.rsplit(':', 1)[0] + ':TMIT'
                    converted = [self.convert_chrg_to_tmit(val_in_pc) for val_in_pc in tmit_buffer if val_in_pc is not None]

                    if len(converted) == 0:
                        reason = "All CHRG values were None or failed conversion"
                        LOGGER.warning(f" {pv}: {reason}")
                        self.failed_devices[pv] = reason
                        continue

                    ave_tmit = np.mean(converted)
                    self.bpm_tmit_dictionary[toro_tmit_pv] = converted
                    self.bpm_tmit_averages_dictionary[toro_tmit_pv] = ave_tmit
                    pid_pv = pv + 'PIDHST' + str(self.buffer_num)

                try:
                    pid_data = epics.caget(pid_pv, timeout=1.5)
                    if pid_data is not None:
                        self.pulse_id_data[pid_pv] = pid_data
                    else:
                        self.failed_devices[pid_pv] = "Pulse ID caget returned None"
                except Exception as e:
                    self.failed_devices[pid_pv] = f"Pulse ID caget exception: {e}"

            except Exception as e:
                self.failed_devices[pv] = f"Exception during data buffer fetch: {e}"

        LOGGER.info('Done at %s', datetime.now())
        if self.failed_devices:
            LOGGER.warning("[SUMMARY] Failed Devices:")
            for k, v in self.failed_devices.items():
                LOGGER.warning("  - %s: %s", k, v)

        return (self.bpm_tmit_dictionary,
                self.bpm_tmit_averages_dictionary,
                self.pulse_id_data,
                self.failed_devices)