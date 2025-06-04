import math
from typing import Dict, List, Any
import pprint
import copy
class IroningCleaningTool():
    def __init__(self,pulse_id_dict: dict,tmit_dict:dict, tmit_aves_dict:dict, num_measurements:int)->dict:
        self.pulse_id_dict = pulse_id_dict
        self.tmit_dict = tmit_dict
        self.num_measurements = num_measurements
        self.tmit_aves_dict = tmit_aves_dict

    def clean_signals(self):
        # nord is number of measurements in array 
        ###check for wrong sized nords return them as dictionary, pop the keys of that dictionary from pulse_id_dict and tmit_dict
        self.wrong_size_nord_dictionary = self.check_nord_equals_num_measurements(self.pulse_id_dict,self.num_measurements)
        pop_wrong_size_nord_list = [key for key in self.wrong_size_nord_dictionary]
        #print(pop_wrong_size_nord_list)
        self.pop_elems(pop_wrong_size_nord_list,self.pulse_id_dict)
        self.pop_elems(pop_wrong_size_nord_list,self.tmit_dict)
        self.pop_elems(pop_wrong_size_nord_list,self.tmit_aves_dict)

        # check for mismatching pids return them as dictionary, pop the keys of that dictionary from pulse_id_dict and tmit_dict
        self.bpm_pid_counts_by_meas, self.bpm_pid_devs_by_meas = self.check_pids(self.pulse_id_dict,self.num_measurements)
        # code is working up until this point for future reference.

        pop_bad_pid_list = self.get_pid_failures(self.bpm_pid_counts_by_meas, self.bpm_pid_devs_by_meas)
        pid_failures_dict = {'pid_failures':pop_bad_pid_list}
        self.pop_elems(pop_bad_pid_list,self.pulse_id_dict)
        self.pop_elems(pop_bad_pid_list,self.tmit_dict)
        self.pop_elems(pop_bad_pid_list,self.tmit_aves_dict)
        # this is what should be uncommented first

        ###check for out of bounds return them as dictionary, pop the keys of that dictionary from pulse_id_dict and tmit_dict
        pop_tmit_out_range_list = self.find_tmit_out_range(self.tmit_aves_dict,2.9*(10**8))
        tmit_failures_dict = {'tmit_failures':pop_tmit_out_range_list}
        self.pop_elems(pop_tmit_out_range_list,self.pulse_id_dict)
        self.pop_elems(pop_tmit_out_range_list,self.tmit_dict)
        self.pop_elems(pop_tmit_out_range_list,self.tmit_aves_dict)
        # do I need to pop from other dictionaries? probably not.

        self.total_failures = self.wrong_size_nord_dictionary | pid_failures_dict | tmit_failures_dict

    def return_all_dictionaries(self):
        return ( self.wrong_size_nord_dictionary, self.pulse_id_dict, self.tmit_dict, 
                 self.tmit_aves_dict, self.bpm_pid_counts_by_meas, self.bpm_pid_devs_by_meas, self.total_failures)

    @staticmethod
    def check_nord_equals_num_measurements(pulse_id_dict:Dict[str,List[float]],num_measurements:int)->dict:
        '''
        Given pulse_id_dict whose keys are pv names and values are arrays of PIDs of length nord
        iterate over keys and check the length of the value array is equal to the number of measurements requested.
        Return a dictionary where the keys are pv names who fail this check and the value is the of the wrong sized nord.
        e.g:
        if num_measurent = 25
        {
            'BPMS:GUNB:314:TMIT': 18
            'BPMS:HTR:120:TMIT': 38,
            'BPMS:HTR:320:TMIT': 38,
            'BPMS:HTR:365:TMIT': 18,
            'BPMS:HTR:460:TMIT': 38,
            'BPMS:HTR:540:TMIT': 20000
        }
        '''
        wrong_size_nord_dictionary : Dict[str,int] = {} #this is a type hint, for the reader if you didn't know that
        for key_is_pv_name, val_array_of_len_nord in pulse_id_dict.items():
            #print(key_is_pv_name , '  ', len(val_array_of_len_nord))
            if len(val_array_of_len_nord) != num_measurements:
                wrong_size_nord_dictionary[key_is_pv_name] = len(val_array_of_len_nord)
        return wrong_size_nord_dictionary
    
    @staticmethod
    def check_pids(pulse_id_dict:dict,num_measurements:int)->dict:
        #potential undersize issue, hopefully already popped out of the list
        pulse_key_list = [key for key in pulse_id_dict]

        dev_counts_per_pid = {} #TODO: maybe type hint all these dictionaries
        devs_per_pid = {}

        for i in range(num_measurements):
            temp_counts_per_pid = {}
            temp_devs_per_pid = {}

            for j in range(len(pulse_key_list)):
                temp_array = []

                #take the pid of the i-th measurement on j-th device
                if pulse_id_dict[pulse_key_list[j]][i] in temp_counts_per_pid.keys():

                    #if the take the pid of the i-th measurement on j-th device is in the temporary
                    #dictionary with pulse_ids as keys increment the count of devices with that pid
                    temp_counts_per_pid[pulse_id_dict[pulse_key_list[j]][i]] +=1

                    #append that dev to the list of devs associated with that key, note the list is instantiated on new pulse id then only appended too here
                    temp_devs_per_pid[pulse_id_dict[pulse_key_list[j]][i]].append(pulse_key_list[j])
                else:
                    #if the take the pid of the i-j is not in the temporary dictionary
                    #with pulse_ids as keys add a new key that is the pid and count 1
                    temp_counts_per_pid[pulse_id_dict[pulse_key_list[j]][i]] =1

                    #make a new dictionary key for temp_devs_per_pid with a blank array as value,
                    # this array will get appended any j-th dev name
                    #that match this version of i-th pid measurement (each i-th measurement can have different pids if BSA is not working correctly)
                    temp_devs_per_pid[pulse_id_dict[pulse_key_list[j]][i]]=temp_array

                    #append the first device to this list that generated the new key
                    temp_devs_per_pid[pulse_id_dict[pulse_key_list[j]][i]].append(pulse_key_list[j])

            dev_counts_per_pid[i] = temp_counts_per_pid
            devs_per_pid[i] = temp_devs_per_pid

        return  dev_counts_per_pid, devs_per_pid

    @staticmethod
    def get_pid_failures(dev_counts_per_pid:dict, devs_per_pid:dict)->list:
        
        ### return the highest count pulse id per measurement in new dictionary
        ### {0: 140777554720214.0,
        #    1: 140777554811214.0       
        #    2: 140777554902214.0
        #    .
        #    .
        #    .
        #    }
        # pprint.pprint(devs_per_pid)
        highest_dev_count_pid_per_meas = {}
        for key_is_ith_measurement, val_is_pids_vs_pv_counts in  dev_counts_per_pid.items():
            temp_count = 0
            temp_pid_at_ith_measurement = None
            if isinstance(val_is_pids_vs_pv_counts,dict):
                # val_key_list = [key for key in val_is_pids_vs_pv_counts]
                for key_is_pid, val_is_pv_counts in val_is_pids_vs_pv_counts.items():
                    if val_is_pv_counts > temp_count:
                        temp_count = val_is_pv_counts
                        temp_pid_at_ith_measurement= key_is_pid
            else:
                print('bad data in get nord id failures value is not a dictionary it is of type: ',type(val_is_pids_vs_pv_counts))
            #print(f'highest count is {temp_count} with pid {temp_pid_at_ith_measurement}')
  
            highest_dev_count_pid_per_meas[key_is_ith_measurement] = temp_pid_at_ith_measurement

        temp_dict = copy.deepcopy(devs_per_pid)
        temp_list = [] 
        for meas_num, pulse_id_value in highest_dev_count_pid_per_meas.items():
           
            if pulse_id_value in temp_dict[meas_num]:
                del temp_dict[meas_num][pulse_id_value]


            for bad_pids, pvs_from_bad_pids in temp_dict[meas_num].items():
                temp_list +=  pvs_from_bad_pids

        # remove duplicates
        failure_list = list(set(temp_list))
        #pprint.pprint(devs_per_pid)
        return failure_list

    @staticmethod
    def find_tmit_out_range(dict_to_scan,low_bound):
        out_of_range_list = []
        key_list = [key for key in dict_to_scan.keys()]
        for key in key_list:
            #TODO check for dict_to_scan[key] type or restrict the type of dictionary that can be passed.
            # might need to use dict_to_scan[key].all()
            if dict_to_scan[key] < low_bound or math.isnan(dict_to_scan[key]):
                out_of_range_list.append(key)
                print(f'{key} out of range')
        return out_of_range_list      

    @staticmethod
    def pop_elems(pop_list:List[str],pop_dict:Dict[str,Any])->Dict[str,Any]:
        ''' 
        Given a list (pop_list) the elements of that list from a dictionary (pop_dict) 
        '''
        for item in pop_list:
            pop_dict.pop(item,None)
        return pop_dict
    
    @staticmethod 
    def get_total_dev_failures(wrong_pid_dict,dev_vs_pid_dict):

        #### not needed I don't believe, I can just sum the lists.
        temp1 = []
        temp_keys = []
        d_list = []
        totals = []
        for key in wrong_pid_dict.keys():
            temp1.append(key)
        #print(dev_vs_pid_dict)
        nest_list = list(dev_vs_pid_dict.items())
        for i,j in nest_list:
            if isinstance(j,dict):
                k = j.copy()
                big_len = 0
                pop_key = None
                keys = list(k.keys())
                
                #print('len of keys is: ', len(keys))
                if len(keys) > 1:
                    for key in keys:
                        #print(key)
                        temp_len = len(k[key])
                        if temp_len> big_len:
                            pop_key = key
                            big_len = temp_len
                        else:
                            continue

                if pop_key is not None:
                    temp_keys.append(pop_key)
                    k.pop(pop_key)
                    for value in k.values():
                        if isinstance(value,list):
                            for val in value:
                                d_list.append(val)
                        else:
                            d_list.append(value)
        
        #print(d_list)

        temp = temp1 + d_list
        for dev in temp:
            if dev not in totals:
                totals.append(dev)
        print(totals)
        return totals