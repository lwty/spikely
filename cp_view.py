""" Creates an MVC view-control for constructing the active pipeline model.

The Construct Pipeline view/control consists of widgets responsible for
constructing the active pipeline by inserting, deleting, or moving elements
within the active pipeline.
"""

import sys
import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg

from pi_model import SpikePipeline  # The model for this controller
# from el_factory.py import ElementFactory 

class ConstructPipelineView(qw.QGroupBox):
    """GroupBox of widgets capable of constructing active pipeline.

    No public methods other than constructor.  All other activites
    of object are triggered by user interaction with sub widgets.
    """

    def __init__(self, spike_pipe):
        super().__init__("Construct Pipeline")
        self.spike_pipe = spike_pipe
        self._init_ui()

    def _init_ui(self):
        """ Builds composite UI consisting of Controllers for adding 
        and maninpulating active pipeline elements and a View of the 
        in-construction active pipeline.
        """

        # Lay out controllers and view from top to bottom of group box
        cp_layout = qw.QVBoxLayout()
        self.setLayout(cp_layout)

        # Selection: Lay out view-controllers in frame from left to right
        sel_layout = qw.QHBoxLayout()
        sel_frame = qw.QFrame()
        sel_frame.setLayout(sel_layout)

        stage_cbx = qw.QComboBox()
        for stage in ["Extraction", "Pre-Processing", "Sorting", "Post-Processing"] :
            stage_cbx.addItem(stage)
        sel_layout.addWidget(stage_cbx)
        
        ele_cbx = qw.QComboBox()
        sel_layout.addWidget(ele_cbx)
        
        sel_layout.addWidget(qw.QPushButton("Add Element"))
        cp_layout.addWidget(sel_frame)

        # Display: Hierarchical (Tree) view of in-construction pipeline

        self.pipe_view = qw.QTreeWidget(self)
        self.pipe_view.setColumnCount(1)
        self.pipe_view.header().hide()
        
        # self.pipe_view.itemClicked.connect(self.clicked)
        # self.pipe_view.setItemsExpandable(False)

        for stage in ["Stage 1: Extraction", "Stage 2: Pre-Processing", 
            "Stage 3: Sorting", "Stage 4: Post-Processing"]:
            an_item = qw.QTreeWidgetItem(self.pipe_view)
            an_item.setText(0, stage)
            an_item.setForeground(0,qg.QBrush(qg.QColor("gray")))
            an_item.setExpanded(True)
            # child = qw.QTreeWidgetItem()
            # child.setText(0, "Sample Element")
            # an_item.addChild(child)

        cp_layout.addWidget(self.pipe_view)

        # Manipulate: Controls to reorder/delete elements in pipeline

        self.up_btn, self.delete_btn, self.down_btn = (qw.QPushButton("Move Up"),
            qw.QPushButton("Delete"), qw.QPushButton("Move Down"))
        pec_box = qw.QFrame()
        hbox = qw.QHBoxLayout()
        hbox.addWidget(self.up_btn)
        hbox.addWidget(self.delete_btn)
        hbox.addWidget(self.down_btn)
        pec_box.setLayout(hbox)

        cp_layout.addWidget(pec_box)