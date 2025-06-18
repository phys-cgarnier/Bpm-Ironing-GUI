import math
from typing import Dict, List, Any
import pprint
class BpmIroningTool():
    def __init__(self):
        print('Instantiating tool that has methods useful for ironing')
    #TODO: add checks for stuff

    @staticmethod
    def create_tmits_ratiod_dict(ref_bpm:str,tmit_aves_dict:Dict[str,float])->Dict[str,float]:
        ref_val_tmit = float('nan')
        tmit_ratios = {}
        
        for key_is_pv_name,val_is_tmit_ave in tmit_aves_dict.items():
            if ref_bpm in key_is_pv_name:
                #TODO: add case for when ref bpm not in key?
                ref_val_tmit = val_is_tmit_ave
                break
        tmit_aves_key_list = [key for key in tmit_aves_dict.keys()]
        for key_is_pv_name in tmit_aves_key_list:
            if math.isnan(tmit_aves_dict[key_is_pv_name]) or math.isnan(ref_val_tmit):
                #TODO: if nan then it pops an element and things might mismatch
                pass
            else:
                key_is_device = key_is_pv_name.rsplit(':',1)[0]
                ratios = ref_val_tmit/tmit_aves_dict[key_is_pv_name]
                tmit_ratios[key_is_device] = round(ratios, 3)
        return tmit_ratios
    
    @staticmethod
    def create_put_scl_vals_dict( tmit_ratios:Dict[str,float],
                                  scl_vals_dict:Dict[str,float],scl_ext:str,ref_bpm:str )->Dict[str,float]:
        put_scl_vals_dict = {}
        tmit_ratios_key_list = [key for key in tmit_ratios]
        for key in tmit_ratios_key_list:
            if 'TORO' in key:
                continue 
            elif ref_bpm in key:
                continue
            else:
                scl_key = key + scl_ext
                put_val = scl_vals_dict[scl_key] * tmit_ratios[key]
                put_scl_vals_dict[scl_key] = round(put_val, 3)
        return put_scl_vals_dict
    
    @staticmethod
    def iron_devices(put_scl_vals_dict:Dict[str,float])->None:
        for key_is_scl_pv, val in put_scl_vals_dict.items():
            try:
                print('c4put ', key_is_scl_pv, ' ', val)
            except:
                KeyError(f'PV: {key_is_scl_pv} not in put scale values dictionary')

    
    @staticmethod
    def iron_single_device(put_scl_vals_dict:Dict[str,float],target_dev:str,scl_ext:str)->None:
        scl_pv = target_dev + scl_ext
        try:
            print('c4put ', scl_pv, ' ', put_scl_vals_dict[scl_pv])
        except:
            KeyError(f'PV: {scl_pv} not in Put scale values dictionary')


