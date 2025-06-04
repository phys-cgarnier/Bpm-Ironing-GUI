class BsaNordComparison():
    ### meant to get perform all PID tasks, returns a list of signals that fail PID tests
    def __init__(self, pid_dictionary,num_measurements):
        self.pid_dictionary = pid_dictionary
        self.num_measurements = num_measurements
       
    def find_failures(self):

        #
        self.failures = 0
        self.failures_list = []
        self.failing_devices = []
        self.wrong_size_pid = {}
        self.pid_bpm_counts = {}
        #
        pulse_key_list = list(self.pid_dictionary.keys())

        for key in range(len(pulse_key_list)):
            if len(self.pid_dictionary[key]) != self.num_measurements:
                self.wrong_size_pid[key] = len(self.pid_dictionary[key])
                print(key, ' does not match the measurement num')

        
        for i in self.num_measurements:
            temp = {}
            for j in range(len(pulse_key_list)):
                if self.pid_dictionary[pulse_key_list[j]][i] in temp.keys():
                    temp[self.pid_dictionary[pulse_key_list[j]][i]] +=1
                else:
                    temp[self.pid_dictionary[pulse_key_list[j]][i]] =1
                    print(pulse_key_list[j])
    @staticmethod
    def check_size(pulse_id_dict,num_measurements):
        wrong_size_pid = {}
        pulse_key_list = list(pulse_id_dict.keys())
        for key in pulse_key_list:
            #print(key, ' ', len(pulse_id_dict[key]))
            if len(pulse_id_dict[key]) != num_measurements:
                wrong_size_pid[key] = len(pulse_id_dict[key])
        return wrong_size_pid    
    @staticmethod
    def pop_elems(pop_list,pop_dict):
        for item in pop_list:
            pop_dict.pop(item)
        return pop_dict
    @staticmethod
    def check_pulse_ids(pulse_id_dict,num_measurements):
        ###write some logic here to make sure no undersizes - happens for DIAG0
        pulse_key_list = list(pulse_id_dict.keys())

        bpm_counts_per_pid = {}
        failed_match_dictionary = {}
        
        for i in range(num_measurements):
            temp_counts = {}
            temp_bpms = {}
            
            for j in range(len(pulse_key_list)):
                temp_array = []
                if pulse_id_dict[pulse_key_list[j]][i] in temp_counts.keys():
                    temp_counts[pulse_id_dict[pulse_key_list[j]][i]] +=1
                    temp_bpms[pulse_id_dict[pulse_key_list[j]][i]].append(pulse_key_list[j])

                else:
                    temp_counts[pulse_id_dict[pulse_key_list[j]][i]] =1  
                    temp_bpms[pulse_id_dict[pulse_key_list[j]][i]] = temp_array
                    temp_bpms[pulse_id_dict[pulse_key_list[j]][i]].append(pulse_key_list[j])
               
            bpm_counts_per_pid[i] = temp_counts
            failed_match_dictionary[i] = temp_bpms

        return bpm_counts_per_pid,failed_match_dictionary    
    @staticmethod 
    def get_total_dev_failures(wrong_pid_dict,dev_vs_pid_dict):
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