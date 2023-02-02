
# coding: utf-8

# In[1]:


import numpy as np
from collections import OrderedDict

import warnings
warnings.filterwarnings('ignore')

import qiskit_metal as metal
from qiskit_metal import designs, draw
from qiskit_metal import MetalGUI, Dict
import matplotlib.pyplot as plt

from qiskit_metal.toolbox_metal import math_and_overrides

from qiskit_metal.qlibrary.core import QComponent

from qiskit_metal.qlibrary.tlines.meandered import RouteMeander
from qiskit_metal.qlibrary.tlines.pathfinder import RoutePathfinder
from qiskit_metal.qlibrary.tlines.anchored_path import RouteAnchors
from qiskit_metal.qlibrary.tlines.mixed_path import RouteMixed


from qiskit_metal.qlibrary.qubits.fluxoniumLOM import FluxoniumPocket

from qiskit_metal.qlibrary.terminations.launchpad_wb import LaunchpadWirebond

from qiskit_metal.qlibrary.terminations.open_to_ground_v2 import OpenToGround
from qiskit_metal.renderers.renderer_ansys.ansys_renderer import QAnsysRenderer


# In[2]:


design = designs.DesignPlanar()
design.chips.main.material = 'silicon'

design.variables['cpw_width'] = '15 um'
design.variables['cpw_gap'] = '8.733 um'
design._chips['main']['size']['size_x'] = '9mm'
design._chips['main']['size']['size_y'] = '9mm'


# In[3]:


design.overwrite_enabled = True

gui = MetalGUI(design)


# In[4]:


from qiskit_metal.qlibrary.qubits.fluxoniumLOM import FluxoniumPocket

gds_cell_name_jj = 'junction_0'
gds_cell_name_inductor = 'jj_array0'

# Q1 details
options = dict(chip='main', nanowire = True, 
            orientation =270, pos_x = '-0.7mm', pos_y = '0mm',
               
    flux_bias_line_options=Dict(make_fbl = True,
                        fbl_sep='150um',), 
               
    charge_line_options=Dict(loc_H = +1, make_cl = True,cl_length ='179um',
            cl_sep ='-10um'),
    readout_line_options=Dict(loc_H = -1, make_rol = True, 
            pad_width = '300um', pad_height = '80um',
            pad_sep='60um', 
              ) )
               
q1 = FluxoniumPocket(design,'Q1', options = dict(
             **options))

# Q2 details
options = dict(chip='main', nanowire = True,
    orientation =270, pos_x = '0.7mm', pos_y = '0mm',
               
    flux_bias_line_options=Dict(make_fbl = True,
                        fbl_sep='150um'), 
               
    charge_line_options=Dict(loc_H = -1, make_cl = True,cl_length ='179um',
            cl_sep ='-10um',
                            ), 
    readout_line_options=Dict(loc_H = +1, make_rol = True, 
            pad_width = '300um', pad_height = '80um',
            pad_sep='60um', 
              ) )
q2 = FluxoniumPocket(design,'Q2', options = dict(
        **options))

gui.rebuild()
gui.autoscale()


# In[5]:


gui.screenshot()


# In[6]:


from qiskit_metal.qlibrary.qubits.transmon_cross_fl import TransmonCrossFL

xmon_options = dict(
    connection_pads=dict(
        #a = dict( connector_location = '0', connector_type = '0'),
        readout_line = dict(connector_location = '90', connector_type = '0'),
        #c = dict(connector_location = '180', connector_type = '1'),
    ),
)

# Create a new Transmon Cross object with name 'Q3'
q3 = TransmonCrossFL(design, 'Q3', options=dict(pos_x = '0mm', pos_y = '-0.06mm', **xmon_options))

gui.rebuild()  # rebuild the design and plot
gui.autoscale() #resize GUI to see QComponent


# In[7]:


#Setup the launchpad1 location and orientation

## Read In launch pad
launch_options = dict(chip='main', pos_x='-4.0mm', pos_y='-1.0325mm', orientation='0',
        lead_length='30um', pad_width='200um',
        pad_height='200um', pad_gap='112um',
                    )
lp = LaunchpadWirebond(design, 'LPReadIn', options = launch_options)


# Read Out launch pad
launch_options = dict(chip='main', pos_x='4.0mm', pos_y='-1.0325mm', orientation='180',
                      lead_length='30um', pad_width='200um',
        pad_height='200um', pad_gap='112um',
                    )
lp = LaunchpadWirebond(design, 'LPReadOut', options = launch_options)


# Transmission_Line = {'pin_inputs':
#            {'start_pin': {'component': 'LPReadIn', 'pin': 'tie'},
#              'end_pin': {'component': 'LPReadOut', 'pin': 'tie'}},
#             'lead': {'start_straight': '3970um', 'end_straight': '3970um',
#                     # 'start_jogged_extension': jogs_in,
#                     # 'anchors': anchors1,
#                     }, 
#                     'total_length': '8mm', 'fillet': "90um"
#             }

# TransLine = RoutePathfinder(design, 'TL', Transmission_Line)


gui.rebuild()


# In[8]:


ops=dict(fillet='90um')


# In[9]:


from collections import OrderedDict


anchors = OrderedDict()
anchors[0] = np.array([-3.5, 1.0])
anchors[1] = np.array([-2.5, 3.0])
anchors[2] = np.array([2.5, 3.0])
anchors[3] = np.array([3.5, 1.0])

between_anchors = OrderedDict() # S, M, PF
between_anchors[0] = "S"
between_anchors[1] = "PF"

options = {'pin_inputs': 
            {'start_pin': {'component': 'LPReadIn', 'pin': 'tie'}, 
             'end_pin': {'component': 'LPReadOut', 'pin': 'tie'}},
            'lead': {'start_straight': '91um', 'end_straight': '90um'},
            'step_size': '0.25mm',
            'anchors': anchors,
            'between_anchors': between_anchors,
            **ops
           }

#Transmission_Line = RoutePathfinder(design, 'line', options)
Transmission_Line = RouteMixed(design, 'line', options)


gui.rebuild()
gui.autoscale()


# In[30]:


## Q1 flux-bias and charge line's lauch pad
# launch_options = dict(chip='main', pos_x='-4.0mm', pos_y='-1.33mm', orientation='0',
#                       lead_length='30um', pad_width='200um',
#         pad_height='200um', pad_gap='112um',
#                     )
# lp = LaunchpadWirebond(design, 'LPCL1', options = launch_options)

launch_options = dict(chip='main', pos_x='-4.0mm', pos_y='-3.0mm', orientation='0',
                     lead_length='30um', pad_width='200um',
        pad_height='200um', pad_gap='112um',
                    )
lp = LaunchpadWirebond(design, 'LPFB1', options = launch_options)
gui.rebuild()


# In[31]:


## Q2 flux-bias and charge line's lauch pad
# launch_options = dict(chip='main', pos_x='4.0mm', pos_y='-1.33mm', orientation='180',
#                       lead_length='30um', pad_width='200um',
#         pad_height='200um', pad_gap='112um',
#                     )
# lp = LaunchpadWirebond(design, 'LPCL2', options = launch_options)

launch_options = dict(chip='main', pos_x='4.0mm', pos_y='-3.0mm', orientation='180',
                     lead_length='30um', pad_width='200um',
        pad_height='200um', pad_gap='112um',
                    )
lp = LaunchpadWirebond(design, 'LPFB2', options = launch_options)

gui.rebuild()


# In[27]:


launch_options = dict(chip='main', pos_x='0.0mm', pos_y='-4.0mm', orientation='90',
                     lead_length='30um', pad_width='200um',
        pad_height='200um', pad_gap='112um',
                    )
lp = LaunchpadWirebond(design, 'LPFB3', options = launch_options)

gui.rebuild()


# In[10]:


# Charge Line for Q1

# XYCharge_LineQ1 = RoutePathfinder(design, 'XY_Gate1', 
#         options = dict(chip='main', fillet='99um',
#             lead=dict(start_straight='150um', end_straight='600um', 
#                       ),
#                          pin_inputs=Dict( start_pin=Dict(
#                                           component='Q1',
#                                                pin='charge_line'),
#                                                 end_pin=Dict(
#                                             component='LPCL1',
#                                             pin='tie')
#                                             )))

# gui.rebuild()


# In[17]:


# Flux Bias Line for Q1

ZFluxBias_LineQ1 = RoutePathfinder(design, 'Z_Gate1', 
        options = dict(chip='main', fillet='99um',
            lead=dict(start_straight='200um', 
        end_straight='400um', ),
        pin_inputs=Dict(start_pin=Dict(component='Q1', 
              pin='flux_bias_line'),
          end_pin=Dict(component='LPFB1', pin='tie')
                                   )))

gui.rebuild()


# In[12]:


# Charge Lıne for Q2

# XYCharge_LineQ2 = RoutePathfinder(design, 'XY_Gate2', options = dict(chip='main',
#                         fillet='80um',
#                 lead=dict(start_straight='150um', end_straight='850um'),
#                                             pin_inputs=Dict(
#                                                 start_pin=Dict(
#                                                     component='Q2',
#                                                     pin='charge_line'),
#                                                 end_pin=Dict(
#                                                     component='LPCL2',
#                                                     pin='tie')
#                                             )))

# gui.rebuild()


# In[18]:


# Flux Bias Line for Q2

ZFluxBias_LineQ2 = RoutePathfinder(design, 'Z_Gate2', options = dict(chip='main',
             fillet='99um',
          lead=dict(start_straight='250um', end_straight='250um'),
                                            pin_inputs=Dict(
                                                start_pin=Dict(
                                                    component='Q2',
                                                    pin='flux_bias_line'),
                                                end_pin=Dict(
                                                    component='LPFB2',
                                                    pin='tie')
                                            )))

gui.rebuild()


# In[33]:


# Flux Bias Line for Q3

ZFluxBias_LineQ2 = RoutePathfinder(design, 'Z_Gate3', options = dict(chip='main',
             fillet='99um',
          lead=dict(start_straight='250um', end_straight='250um'),
                                            pin_inputs=Dict(
                                                start_pin=Dict(
                                                    component='Q3',
                                                    pin='flux_line'),
                                                end_pin=Dict(
                                                    component='LPFB3',
                                                    pin='tie')
                                            )))

gui.rebuild()


# In[21]:


# Lambda/2 resonators - Resonator1
otg1 = OpenToGround(design, 'otg1s', options=dict(chip='main', 
                 pos_x='-3.462267mm', pos_y='0mm', orientation='90'))
rt_meander = RouteMeander(design, 'cavity1',  Dict(meander=Dict(spacing='200um'),
        total_length='7.21mm',
        hfss_wire_bonds = True,
        fillet='99um',
        lead = dict(start_straight='250um'),
        pin_inputs=Dict(
            start_pin=Dict(component='otg1s', pin='open'),
            end_pin=Dict(component='Q1', pin='readout_line')), ))

gui.rebuild()


# In[22]:


# Lambda/2 resonators - Resonator2
otg2 = OpenToGround(design, 'otg2s', options=dict(chip='main', pos_x='3.462267mm',  pos_y='0mm', orientation='90'))
rt_meander = RouteMeander(design, 'cavity2',  Dict(meander=Dict(spacing='200um'),
        total_length='7.21mm',
        hfss_wire_bonds = True,
        fillet='99um',
        lead = dict(start_straight='250um'),
        pin_inputs=Dict(
            start_pin=Dict(component='otg2s', pin='open'),
            end_pin=Dict(component='Q2', pin='readout_line')), ))

gui.rebuild()


# In[35]:


# Lambda/2 resonators - Resonator3
otg3 = OpenToGround(design, 'otg3s', options=dict(chip='main', pos_x='0mm',  pos_y='2.962267mm', orientation='180'))
rt_meander = RouteMeander(design, 'cavity3',  Dict(meander=Dict(spacing='200um'),
        total_length='10.21mm',
        hfss_wire_bonds = True,
        fillet='99um',
        lead = dict(start_straight='0um'),
        pin_inputs=Dict(
            start_pin=Dict(component='otg3s', pin='open'),
            end_pin=Dict(component='Q3', pin='readout_line')), ))

gui.rebuild()


# In[36]:


#Save screenshot as a .png formatted file.
gui.screenshot()


# In[38]:


from qiskit_metal.analyses.quantization import LOManalysis
c1 = LOManalysis(design, "q3d")


# In[39]:


c1.sim.setup


# In[40]:


# example: update single setting
c1.sim.setup.max_passes = 15
# example: update multiple settings

c1.sim.setup_update(solution_order = 'Medium', auto_increase_solution_order = 'False')

c1.sim.setup


# In[41]:


c1.sim.run(components=['Q1'], open_terminations=[('Q1', 'charge_line'), ('Q1', 'flux_bias_line'), ('Q1', 'fake_flux_bias_line'), ('Q1', 'readout_line')])
c1.sim.capacitance_matrix


# In[ ]:


# capacitance with pocket-height=650um

Cpad_top = 
Cpad_bot = 
Creadout_bot = 
Ccharge_top = 
Cfluxpad_top = 
Cfluxpad_bot = 

C_pads =

C_top = Cpad_top + Ccharge_top + Cfluxpad_top
C_bot = Cpad_bot + Creadout_bot + Cfluxpad_bot

Csigma = C_pads + C_top*C_bot/(C_top+C_bot)
print('Total Capacitance:', Csigma, 'fF')


# In[44]:


c1.sim.run(components=['Q2'], open_terminations=[('Q2', 'charge_line'), ('Q2', 'flux_bias_line'), ('Q2', 'fake_flux_bias_line'), ('Q2', 'readout_line')])
c1.sim.capacitance_matrix


# In[45]:


c1.sim.run(components=['Q3'], open_terminations=[('Q3', 'flux_line'),  ('Q3', 'readout_line')])
c1.sim.capacitance_matrix

