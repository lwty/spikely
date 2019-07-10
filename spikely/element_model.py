import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import PyQt5.QtWidgets as qw

import re

from . import config as cfg


# An MVC model representation of a SpikeInterface element
# used almost exclusively to expose parameters to UI Views
class ElementModel(qc.QAbstractTableModel):

    def __init__(self):
        self._element = None
        super().__init__()

    # Pythonic setters/getters
    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, element):
        # Ensures dependent Views are signaled on element changes
        self.beginResetModel()
        self._element = element
        self.endResetModel()

    #
    # QAbstractTableModel Methods
    #

    # Count of parameters associated with an element instance
    def rowCount(self, parent=qc.QModelIndex()):
        return 0 if self._element is None else len(self._element.params)

    # Number of display columns: Parameter, Type, Value
    def columnCount(self, parent=qc.QModelIndex()):
        return 3

    # Sets UI policy for columns in table view for element parameters
    def flags(self, mod_index):
        column_flags = qc.QAbstractTableModel.flags(self, mod_index)
        col = mod_index.column()

        # Parameter and Type column cells are read only
        if col == cfg.PARAM_COL or col == cfg.VTYPE_COL:
            column_flags ^= qc.Qt.ItemIsSelectable
        elif col == cfg.VALUE_COL:
            column_flags |= qc.Qt.ItemIsEditable
        return column_flags

    # Called by Views, gets element parameter data based on index and role
    def data(self, mod_index, role=qc.Qt.DisplayRole):
        col, row = mod_index.column(), mod_index.row()
        param_dict = self._element.params[row]

        # If no actual result return empty value indicator
        result = qc.QVariant()

        if role == qc.Qt.DisplayRole or role == qc.Qt.EditRole:
            if col == cfg.PARAM_COL:
                result = param_dict['name']
            elif col == cfg.VTYPE_COL:
                result = param_dict['type']
            elif col == cfg.VALUE_COL:
                if 'value' in param_dict.keys():
                    result = str(param_dict['value']).strip()
                    if not result and 'default' in param_dict.keys():
                        result = str(param_dict['default'])

        elif role == qc.Qt.ToolTipRole:
            if col == cfg.PARAM_COL and 'title' in param_dict.keys():
                result = param_dict['title']

        # Paints cell red if mandatory parameter value is missing.
        # Mandatory parameters are those with no default keys
        elif role == qc.Qt.BackgroundRole:
            if col == cfg.VALUE_COL:
                if ('value' not in param_dict.keys() and
                        'default' not in param_dict.keys()):
                    result = qg.QBrush(qg.QColor(255, 192, 192))

        return result

    def headerData(self, section, orientation, role):
        result = qc.QVariant()
        if (orientation == qc.Qt.Horizontal and
                (role == qc.Qt.DisplayRole or role == qc.Qt.EditRole)):
            result = ['Parameter', 'Type', 'Value'][section]

        return result

    # Called after user edits parameter value to keep model in sync
    def setData(self, mod_index, value, role=qc.Qt.EditRole):
        row = mod_index.row()
        param_dict = self._element.params[row]
        success = True

        # This is a little tricky - if user enters valid value assign it to
        # 'value' in the param dictionary.  If user enters nothing assign
        # 'default' to 'value' if 'default' exists, otherwise delete 'value'
        # from param dictionary.  Talk to Cole if you don't like this.
        if role == qc.Qt.EditRole:
            if value.strip():
                success, cvt_value = self._convert_value(
                    param_dict['type'], value)
                if success:
                    param_dict['value'] = cvt_value
            else:
                if 'default' in param_dict.keys():
                    param_dict['value'] = param_dict['default']
                else:
                    param_dict.pop('value', None)

        return success

    #
    # Helper Methods
    #

    def _convert_value(self, type_str, value):
        success, cvt_value = True, None
        try:
            if value == 'None':
                cvt_value = None
            elif type_str in ['str', 'path']:
                cvt_value = value
            elif type_str == 'int':
                cvt_value = int(value)
            elif type_str == 'float':
                cvt_value = float(value)
            elif type_str == 'int_list':
                cvt_value = []
                value = re.sub(r'[\[\]]', '', value)
                for i in value.split(','):
                    cvt_value.append(int(i))
            elif type_str == 'bool':
                if value.lower() in ['true', 'yes']:
                    cvt_value = True
                elif value.lower() in ['false', 'no']:
                    cvt_value = False
                else:
                    raise TypeError(f'{value} is not a valid bool type')
            else:
                raise TypeError(f'{type_str} is not a Spikely supported type')
        except (TypeError, ValueError) as err:
            qw.QMessageBox.warning(
                cfg.main_window, 'Type Conversion Error', repr(err))
            success = False

        return success, cvt_value