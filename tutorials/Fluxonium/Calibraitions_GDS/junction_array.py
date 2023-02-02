"""
TO DO: Store JJ locations in a dict for future reference.

Check HFSS rendering

Check GDS rendering
"""

import matplotlib.pyplot as plt
import numpy as np
import pprint



import qiskit_metal as metal
from qiskit_metal import designs, draw
from qiskit_metal import Dict, open_docs , Headings

from qiskit_metal.qlibrary.qubits.JJ_Manhattan import jj_manhattan


from qiskit_metal.toolbox_metal import math_and_overrides
from qiskit_metal.qlibrary.core import QComponent


# from array_unit_cell import SingleArrayCell_v2
# from array_claw_coupler import ArrayClawCoupler

class JunctionArray(QComponent):
    """
    Inherits 'QComponent' class.

    Description:
        TO ADD

    Options:
    TO  Check JJ rendering and modify



    """

    default_options=Dict(
        chip='main',
        ground_gap_x='20um',
        ground_gap_y='20um',
        array_unit=Dict(
            array_pad_x='20um',
            array_pad_y='50um',
            array_gap_y='10um',
            junction_thickness = '10um',
            n_junction='10')
        )


    def make(self):

        self.make_jj_array()
        self.make_buffer_ground()


    def make_jj_array(self, name='jj_array'):

        p = self.parse_options()  # Parse the string options into numbers

        parray  = p.array_unit
        # print(p.array_unit)
        chip = p.chip



        ## -------------------- JJ array pad

        jj_pad = draw.box(-parray.array_pad_x/2, -parray.array_pad_y/2,
                            parray.array_pad_x/2, parray.array_pad_y/2)

        jj_pad = draw.rotate(jj_pad,p.orientation, origin=(0, 0))
        jj_pad = draw.translate(jj_pad,p.pos_x,p.pos_y)

        junction_width = parray.junction_thickness
        rect_jj = draw.LineString([(0, 0), (0, +parray.array_gap_y)])
        yoff_junction_elem1 = parray.array_pad_y/2
        rect_jj = draw.translate(rect_jj,0, yoff_junction_elem1)
        #
        #
        # #  ## --------------------------------------------------------
        #  ## ------------------- Create JJ array
        #  ## --------------------------------------------------------
        junc_yoff=0  ## Initiate shift at zero value
        for idx in range (int(parray.n_junction+1)):

            pad_junc = draw.translate(jj_pad, xoff=0,
                                    yoff=(junc_yoff))

            self.add_qgeometry('poly', {'jj_pad_{:d}'.format(idx):pad_junc},
                    layer=p.layer,
                    chip=chip)

            sim_junction = draw.translate(rect_jj,0, junc_yoff)
            sim_junction = draw.rotate(sim_junction,p.orientation, origin=(0, 0))
            sim_junction = draw.translate(sim_junction,p.pos_x,p.pos_y)

            if idx !=parray.n_junction:
                ## GDS cell name changed
                self.add_qgeometry('junction',
                   dict({'rect_jj_{:d}'.format(idx):sim_junction}),
                   width=junction_width,
                   chip=chip,
                   gds_cell_name='FakeJunction_0{:d}'.format((idx+1))
                   )

                # GDS cell name not changed
                # self.add_qgeometry('junction',
                #    dict({'rect_jj_{:d}'.format(idx):sim_junction}),
                #    width=junction_width,
                #    chip=chip
                #    )



            y_increment = parray.array_pad_y + parray.array_gap_y
            junc_yoff = junc_yoff + y_increment



    def make_buffer_ground(self, name='ground_etch'):
        p = self.parse_options()  # Parse the string options into numbers

        parray  = p.array_unit
        chip = p.chip

        ground_width = parray.array_pad_x + 2*p.ground_gap_x
        ground_height =  int(parray.n_junction+1)*(parray.array_pad_y) \
            + int(parray.n_junction)*(parray.array_gap_y) \
            +2*p.ground_gap_y

        ground_bottom_y = -parray.array_pad_y/2 -p.ground_gap_y
        ground_etch = draw.box(-ground_width/2, ground_bottom_y,
                            ground_width/2, ground_bottom_y+ground_height)


        ground_etch = draw.rotate(ground_etch, p.orientation, origin=(0, 0))
        ground_etch = draw.translate(ground_etch, p.pos_x, p.pos_y)

        self.add_qgeometry('poly', {'ground_etch':ground_etch},
                layer=p.layer,
                chip=chip,
                subtract=True)

## =============================================================================
## --------------------------- END
## =============================================================================
