from .spike_element import SpikeElement


class Sorter(SpikeElement):
    """Preprocessor class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.sorter_name)

    def run(self, input_payload, next_element):
        base_sorter_param_dict = {}
        sub_sorter_param_dict = {}
        base_sorter_param_dict['recording'] = input_payload
        output_folder = None
        
        params = self._params
        for param in params:
            param_name = param['name']
            param_value = param['value']
            if 'base_param' in param:
                base_sorter_param_dict[param_name] = param_value
                if(param_name == 'output_folder'):
                    output_folder_string = param_value
            else:
                sub_sorter_param_dict[param_name] = param_value
            
        sorter = self._interface_class(**base_sorter_param_dict)
        sorter.set_params(**sub_sorter_param_dict)
        sorter.run()
        return sorter.get_result_list(), output_folder_string, input_payload
