from .spike_element import SpikeElement
import spikeextractors as se
from pathlib import Path
import spiketoolkit as st
import os


class Curator(SpikeElement):
    """Curator class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.curator_name)

    def run(self, input_payload, next_element):
        params_dict = {}
        params_dict['sorting'] = input_payload[0]
        output_folder_path = input_payload[1]
        recording = input_payload[2]

        params = self._params
        for param in params:
            param_name = param['name']
            # param_type = param['type']
            # param_title = param['title']
            param_value = param['value']
            params_dict[param_name] = param_value
        sorting = self._interface_class(**params_dict)
        if(next_element is None):
            curated_output_folder = output_folder_path/'curated_phy_results'
            if not curated_output_folder.is_dir():
                os.makedirs(str(curated_output_folder))
            print("Saving curated results....")
            st.postprocessing.export_to_phy(recording, sorting, curated_output_folder)#, grouping_property='group')
            print("Done!")
        return sorting, output_folder_path
