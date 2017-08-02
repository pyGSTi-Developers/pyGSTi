from __future__ import division, print_function, absolute_import, unicode_literals
#*****************************************************************
#    pyGSTi 0.9:  Copyright 2015 Sandia Corporation
#    This Software is released under the GPL license detailed
#    in the file "license.txt" in the top-level pyGSTi directory
#*****************************************************************
"""
Variables for working with the 2-qubit gate set containing the gates
I*X(pi/2), I*Y(pi/2), X(pi/2)*I, Y(pi/2)*I, and CPHASE.
"""

from . import gatestringconstruction as _strc
from . import gatesetconstruction as _setc
from . import spamspecconstruction as _spamc
from collections import OrderedDict as _OrderedDict

description = "I*I, I*X(pi/2), I*Y(pi/2), X(pi/2)*I, Y(pi/2)*I, X(pi/2)*X(pi/2), Y(pi/2)*Y(pi/2), X(pi/2)*Y(pi/2), and Y(pi/2)*X(pi/2) gates"

gates = ['Gii','Gix','Giy','Gxi','Gyi','Gxx','Gyy','Gxy','Gyx']

fiducials16 = _strc.gatestring_list(
    [ (), ('Gix',), ('Giy',), ('Gix','Gix'),
      ('Gxi',), ('Gxi','Gix'), ('Gxi','Giy'), ('Gxi','Gix','Gix'),
      ('Gyi',), ('Gyi','Gix'), ('Gyi','Giy'), ('Gyi','Gix','Gix'),
      ('Gxi','Gxi'), ('Gxi','Gxi','Gix'), ('Gxi','Gxi','Giy'), ('Gxi','Gxi','Gix','Gix') ] )

fiducials36 = _strc.gatestring_list(
    [ (), ('Gix',), ('Giy',), ('Gix','Gix'), ('Gix','Gix','Gix'), ('Giy','Giy','Giy'),
      ('Gxi',), ('Gxi','Gix'), ('Gxi','Giy'), ('Gxi','Gix','Gix'), ('Gxi','Gix','Gix','Gix'), ('Gxi','Giy','Giy','Giy'),
      ('Gyi',), ('Gyi','Gix'), ('Gyi','Giy'), ('Gyi','Gix','Gix'), ('Gyi','Gix','Gix','Gix'), ('Gyi','Giy','Giy','Giy'),
      ('Gxi','Gxi'), ('Gxi','Gxi','Gix'), ('Gxi','Gxi','Giy'), ('Gxi','Gxi','Gix','Gix'), ('Gxi','Gxi','Gix','Gix','Gix'),
      ('Gxi','Gxi','Giy','Giy','Giy'), ('Gxi','Gxi','Gxi'), ('Gxi','Gxi','Gxi','Gix'), ('Gxi','Gxi','Gxi','Giy'),
      ('Gxi','Gxi','Gxi','Gix','Gix'), ('Gxi','Gxi','Gxi','Gix','Gix','Gix'), ('Gxi','Gxi','Gxi','Giy','Giy','Giy'),
      ('Gyi','Gyi','Gyi'), ('Gyi','Gyi','Gyi','Gix'), ('Gyi','Gyi','Gyi','Giy'), ('Gyi','Gyi','Gyi','Gix','Gix'),
      ('Gyi','Gyi','Gyi','Gix','Gix','Gix'), ('Gyi','Gyi','Gyi','Giy','Giy','Giy') ] )

fiducials = fiducials16
prepStrs = fiducials16

effectStrs = _strc.gatestring_list(
    [(), ('Gix',), ('Giy',), 
     ('Gix','Gix'), ('Gxi',), 
     ('Gyi',), ('Gxi','Gxi'), 
     ('Gxi','Gix'), ('Gxi','Giy'), 
     ('Gyi','Gix'), ('Gyi','Giy')] )

germs = _strc.gatestring_list( 
    [ ('Gii',),
      ('Gxi',),
      ('Gyi',),
      ('Gix',),
      ('Giy',),
      ('Gxx',),
      ('Gyy',),
      ('Gxy',),
      ('Gyx',),
      ('Gxi', 'Gyi'),
      ('Gix', 'Giy'),
      ('Giy', 'Gxi'),
      ('Gix', 'Gxi'),
      ('Gii', 'Gix'),
      ('Gxy', 'Gyx'),
      ('Gxx', 'Gyy'),
      ('Gxx', 'Gxy'),
      ('Gyy', 'Gyx'),
      ('Gxi', 'Gyi', 'Gii'),
      ('Gxi', 'Gii', 'Gyi'),
      ('Gxi', 'Gii', 'Gii'),
      ('Gyi', 'Gii', 'Gii'),
      ('Gix', 'Giy', 'Gii'),
      ('Gix', 'Gii', 'Giy'),
      ('Gix', 'Gii', 'Gii'),
      ('Giy', 'Gii', 'Gii'),
      ('Gii', 'Gyi', 'Giy'),
      ('Gix', 'Gyi', 'Giy'),
      ('Gxx', 'Gyy', 'Gxy'),
      ('Gyy', 'Gyx', 'Gxy'),
      ('Gxx', 'Gyx', 'Gxy'),
      ('Giy', 'Gxx', 'Gyx'),
      ('Gxi', 'Gyx', 'Gxx'),
      ('Gyi', 'Gxx', 'Gyx'),
      ('Gix', 'Gxx', 'Gxy'),
      ('Giy', 'Gxx', 'Gyy'),
      ('Gxx', 'Gyy', 'Gyy'),
      ('Gyy', 'Gxy', 'Gyx'),
      ('Gxx', 'Gyy', 'Gyx'),
      ('Gxy', 'Gyx', 'Gyx'),
      ('Gxi', 'Gyy', 'Gyy'),
      ('Gxi', 'Gxy', 'Gyy'),
      ('Gxi', 'Gyx', 'Gyx'),
      ('Gxx', 'Gxy', 'Gyx'),
      ('Gxy', 'Gxy', 'Gyx'),
      ('Gxx', 'Gxy', 'Gyy'),
      ('Giy', 'Gyx', 'Gyy'),
      ('Gix', 'Gxy', 'Gxx'),
      ('Giy', 'Gyx', 'Gyx'),
      ('Gyi', 'Gxx', 'Gxx'),
      ('Gyy', 'Gxy', 'Gxy'),
      ('Gyi', 'Gyy', 'Gxy'),
      ('Gxx', 'Gyx', 'Gyy'),
      ('Giy', 'Gxy', 'Gxx'),
      ('Gix', 'Gyy', 'Gyx'),
      ('Gxx', 'Gxx', 'Gyy'),
      ('Gyi', 'Gyx', 'Gxx'),
      ('Giy', 'Gxx', 'Gxy'),
      ('Giy', 'Gxx', 'Gxx'),
      ('Gix', 'Gyx', 'Giy'),
      ('Gyi', 'Gxy', 'Gxy'),
      ('Giy', 'Gyx', 'Gxx'),
      ('Gyi', 'Gxy', 'Gyy'),
      ('Giy', 'Gyy', 'Gyx'),
      ('Gxi', 'Gxx', 'Gyx'),
      ('Gix', 'Gyi', 'Gxy'),
      ('Gix', 'Gxy', 'Gxy'),
      ('Gxi', 'Gxi', 'Gii', 'Gyi'),
      ('Gxi', 'Gyi', 'Gyi', 'Gii'),
      ('Gix', 'Gix', 'Gii', 'Giy'),
      ('Gix', 'Giy', 'Giy', 'Gii'),
      ('Gix', 'Gyi', 'Gix', 'Gyi'),
      ('Gyi', 'Gyi', 'Giy', 'Gyi'),
      ('Gix', 'Gix', 'Gxi', 'Gix'),
      ('Giy', 'Gix', 'Gix', 'Gix'),
      ('Gix', 'Gyi', 'Gyi', 'Gyi'),
      ('Gix', 'Gii', 'Gii', 'Gxi'),
      ('Gix', 'Gii', 'Gyi', 'Gii'),
      ('Gxx', 'Gxy', 'Gyx', 'Gyx'),
      ('Gxi', 'Gix', 'Gxy', 'Giy'),
      ('Gyx', 'Gxx', 'Gxy', 'Gxx'),
      ('Gyx', 'Gyx', 'Gyy', 'Gyy'),
      ('Gyi', 'Gxx', 'Gyy', 'Gyi'),
      ('Gix', 'Gxy', 'Gix', 'Gyx'),
      ('Gyx', 'Gix', 'Gxy', 'Gxi'),
      ('Giy', 'Giy', 'Gxi', 'Gyi', 'Gxi'),
      ('Giy', 'Giy', 'Giy', 'Gix', 'Gxi'),
      ('Gix', 'Gxi', 'Gyi', 'Gxi', 'Giy'),
      ('Gyx', 'Gxy', 'Gxi', 'Gxy', 'Gxy'),
      ('Gii', 'Gyy', 'Gxy', 'Gyy', 'Gyy'),
      ('Gyy', 'Gyx', 'Giy', 'Gyy', 'Gxx'),
      ('Gyy', 'Gyy', 'Gxi', 'Gyx', 'Gyi'),
      ('Gxy', 'Gyx', 'Gxy', 'Gix', 'Gxx'),
      ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'),
      ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'),
      ('Gix', 'Giy', 'Gix', 'Giy', 'Gix', 'Gyi'),
      ('Gyi', 'Gii', 'Giy', 'Gxi', 'Gxi', 'Giy'),
      ('Gxi', 'Gix', 'Giy', 'Gxi', 'Giy', 'Gyi'),
      ('Giy', 'Gii', 'Gii', 'Gxi', 'Giy', 'Gxi'),
      ('Gxi', 'Gix', 'Giy', 'Gix', 'Giy', 'Gix'),
      ('Gxy', 'Gyi', 'Gyi', 'Gxy', 'Gxy', 'Gyy'),
      ('Gxy', 'Gxi', 'Gxx', 'Gyy', 'Gxy', 'Gyy'),
      ('Gix', 'Giy', 'Gix', 'Gyi', 'Gxi', 'Gii', 'Gxi'),
      ('Gxi', 'Gyi', 'Gyi', 'Gix', 'Giy', 'Gxi', 'Giy'),
      ('Giy', 'Gii', 'Gyi', 'Gyi', 'Gix', 'Gxi', 'Giy'),
      ('Giy', 'Gyi', 'Gxi', 'Gyi', 'Gix', 'Gix', 'Giy'),
      ('Gxi', 'Giy', 'Gxi', 'Gyi', 'Gix', 'Gii', 'Gxi'),
      ('Gxi', 'Giy', 'Gix', 'Gyi', 'Gix', 'Gix', 'Gii'),
      ('Giy', 'Gii', 'Gii', 'Giy', 'Giy', 'Gii', 'Giy'),
      ('Gxi', 'Gii', 'Giy', 'Gxi', 'Gyi', 'Giy', 'Gii'),
      ('Giy', 'Gxi', 'Gyi', 'Giy', 'Gyi', 'Gxi', 'Gii'),
      ('Gii', 'Gxi', 'Giy', 'Gyi', 'Gyi', 'Gix', 'Gyi'),
      ('Gix', 'Giy', 'Giy', 'Gyi', 'Gii', 'Gxi', 'Giy'),
      ('Gyi', 'Gix', 'Gxi', 'Gyi', 'Gxi', 'Gii', 'Giy'),
      ('Gix', 'Gyi', 'Gii', 'Gix', 'Gix', 'Gxi', 'Gyi'),
      ('Giy', 'Gxi', 'Gix', 'Giy', 'Gyi', 'Giy', 'Gxi'),
      ('Gyy', 'Gyx', 'Gyx', 'Gxi', 'Gxx', 'Gxx', 'Gyi'),
      ('Gyi', 'Gxx', 'Gxy', 'Gyi', 'Gyx', 'Gyy', 'Gix'),
      ('Gxx', 'Gxx', 'Gyy', 'Gxy', 'Giy', 'Gix', 'Gxx'),
      ('Gxx', 'Gyy', 'Giy', 'Gxi', 'Gxy', 'Gxx', 'Gyy'),
      ('Giy', 'Gii', 'Gxi', 'Gxi', 'Gix', 'Gii', 'Gyi', 'Giy'),
      ('Gxi', 'Giy', 'Gix', 'Gyi', 'Gix', 'Gii', 'Gxi', 'Giy'),
      ('Giy', 'Gix', 'Gii', 'Gyi', 'Gii', 'Gyi', 'Gxi', 'Giy'),
      ('Giy', 'Gyi', 'Gix', 'Gix', 'Gxi', 'Gxi', 'Gxi', 'Gyi'),
      ('Gii', 'Gii', 'Gyi', 'Giy', 'Gix', 'Giy', 'Gix', 'Gxi'),
      ('Gxi', 'Gii', 'Gii', 'Gix', 'Giy', 'Gxi', 'Gyi', 'Gix'),
      ('Gyi', 'Gxi', 'Giy', 'Gxi', 'Gix', 'Gxi', 'Gyi', 'Giy'),
      ('Gyi', 'Gii', 'Gix', 'Gyi', 'Gyi', 'Gxi', 'Gix', 'Giy'),
      ('Gyy', 'Gxx', 'Giy', 'Gyx', 'Giy', 'Gix', 'Gxx', 'Gyi'),
      ('Gyy', 'Gyy', 'Gxy', 'Gxx', 'Giy', 'Gxy', 'Giy', 'Gyy'),
      ('Gyx', 'Gxy', 'Gyx', 'Gix', 'Gyi', 'Gyx', 'Gxx', 'Gxy'),
      ('Gyx', 'Gix', 'Giy', 'Gxy', 'Gyx', 'Gyy', 'Gxi', 'Gyi'),
      ('Gxx', 'Gyi', 'Gyi', 'Gxi', 'Gxy', 'Gix', 'Gyy', 'Gyy') 
      ] )
      
#Construct the target gateset
gs_target = _setc.build_gateset(
    [4], [('Q0','Q1')],['Gii','Gix','Giy','Gxi','Gyi','Gxx','Gyy','Gxy','Gyx'],
    [ "I(Q0):I(Q1)", "I(Q0):X(pi/2,Q1)", "I(Q0):Y(pi/2,Q1)", "X(pi/2,Q0):I(Q1)",
      "Y(pi/2,Q0):I(Q1)", "X(pi/2,Q0):X(pi/2,Q1)", "Y(pi/2,Q0):Y(pi/2,Q1)",
      "X(pi/2,Q0):Y(pi/2,Q1)", "Y(pi/2,Q0):X(pi/2,Q1)" ],
    prepLabels=['rho0'], prepExpressions=["0"],
    effectLabels=['E0','E1','E2'], effectExpressions=["0","1","2"],
    spamdefs={'upup': ('rho0','E0'), 'updn': ('rho0','E1'),
              'dnup': ('rho0','E2'), 'dndn': ('rho0','remainder') }, basis="pp")


specs16x10 = _spamc.build_spam_specs(
    prepStrs=prepStrs,
    effectStrs=effectStrs,
    prep_labels=gs_target.get_prep_labels(),
    effect_labels=gs_target.get_effect_labels() )

specs16 = _spamc.build_spam_specs(
    fiducials16,
    prep_labels=gs_target.get_prep_labels(),
    effect_labels=gs_target.get_effect_labels() )

specs36 = _spamc.build_spam_specs(
    fiducials36,
    prep_labels=gs_target.get_prep_labels(),
    effect_labels=gs_target.get_effect_labels() )

specs = specs16x10 #use smallest specs set as "default"

clifford_compilation = _OrderedDict()
clifford_compilation['Gc0c0'] = ['Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c1'] = ['Giy', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c2'] = ['Gix', 'Gix', 'Gix', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc0c3'] = ['Gix', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c4'] = ['Giy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc0c5'] = ['Gix', 'Giy', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c6'] = ['Giy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c7'] = ['Giy', 'Giy', 'Giy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c8'] = ['Gix', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c9'] = ['Gix', 'Gix', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c10'] = ['Giy', 'Gix', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c11'] = ['Gix', 'Gix', 'Gix', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c12'] = ['Giy', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c13'] = ['Gix', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c14'] = ['Gix', 'Giy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc0c15'] = ['Giy', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c16'] = ['Gix', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c17'] = ['Gix', 'Giy', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c18'] = ['Giy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc0c19'] = ['Gix', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c20'] = ['Gix', 'Giy', 'Giy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc0c21'] = ['Giy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc0c22'] = ['Gix', 'Gix', 'Gix', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc0c23'] = ['Gix', 'Giy', 'Gix', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc1c0'] = ['Gyi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c1'] = ['Gyy', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c2'] = ['Gyx', 'Gxx', 'Gix', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc1c3'] = ['Gyx', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c4'] = ['Gyy', 'Gxy', 'Giy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc1c5'] = ['Gyx', 'Gxy', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c6'] = ['Gyy', 'Gxy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c7'] = ['Gyy', 'Gxy', 'Giy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c8'] = ['Gyx', 'Gxy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c9'] = ['Gyx', 'Gxx', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c10'] = ['Gyy', 'Gxx', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c11'] = ['Gyx', 'Gxx', 'Gix', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c12'] = ['Gyy', 'Gxx', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c13'] = ['Gyx', 'Gxx', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c14'] = ['Gyx', 'Gxy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc1c15'] = ['Gyy', 'Gxy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c16'] = ['Gyx', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c17'] = ['Gyx', 'Gxy', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c18'] = ['Gyy', 'Gxy', 'Giy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc1c19'] = ['Gyx', 'Gxy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c20'] = ['Gyx', 'Gxy', 'Giy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc1c21'] = ['Gyy', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc1c22'] = ['Gyx', 'Gxx', 'Gix', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc1c23'] = ['Gyx', 'Gxy', 'Gix', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc2c0'] = ['Gxi', 'Gxi', 'Gxi', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c1'] = ['Gxy', 'Gxx', 'Gxi', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c2'] = ['Gxx', 'Gxx', 'Gxx', 'Gyy', 'Gyy', 'Gyy', 'Gii']   
clifford_compilation['Gc2c3'] = ['Gxx', 'Gxx', 'Gxi', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c4'] = ['Gxy', 'Gxy', 'Gxy', 'Gyx', 'Gyx', 'Gyx', 'Gii']   
clifford_compilation['Gc2c5'] = ['Gxx', 'Gxy', 'Gxy', 'Gyy', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c6'] = ['Gxy', 'Gxy', 'Gxi', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c7'] = ['Gxy', 'Gxy', 'Gxy', 'Gyx', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c8'] = ['Gxx', 'Gxy', 'Gxi', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c9'] = ['Gxx', 'Gxx', 'Gxy', 'Gyy', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c10'] = ['Gxy', 'Gxx', 'Gxx', 'Gyx', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c11'] = ['Gxx', 'Gxx', 'Gxx', 'Gyy', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c12'] = ['Gxy', 'Gxx', 'Gxx', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c13'] = ['Gxx', 'Gxx', 'Gxx', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c14'] = ['Gxx', 'Gxy', 'Gxy', 'Gyy', 'Gyx', 'Gyx', 'Gix']   
clifford_compilation['Gc2c15'] = ['Gxy', 'Gxy', 'Gxy', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c16'] = ['Gxx', 'Gxi', 'Gxi', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c17'] = ['Gxx', 'Gxy', 'Gxx', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c18'] = ['Gxy', 'Gxy', 'Gxy', 'Gyx', 'Gyx', 'Gyi', 'Gii']   
clifford_compilation['Gc2c19'] = ['Gxx', 'Gxy', 'Gxy', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c20'] = ['Gxx', 'Gxy', 'Gxy', 'Gyy', 'Gyx', 'Gyi', 'Gii']   
clifford_compilation['Gc2c21'] = ['Gxy', 'Gxi', 'Gxi', 'Gyi', 'Gyi', 'Gyi', 'Gii']   
clifford_compilation['Gc2c22'] = ['Gxx', 'Gxx', 'Gxx', 'Gyy', 'Gyy', 'Gyi', 'Gii']   
clifford_compilation['Gc2c23'] = ['Gxx', 'Gxy', 'Gxx', 'Gyx', 'Gyx', 'Gyi', 'Gii']   
clifford_compilation['Gc3c0'] = ['Gxi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c1'] = ['Gxy', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c2'] = ['Gxx', 'Gxx', 'Gix', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc3c3'] = ['Gxx', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c4'] = ['Gxy', 'Gxy', 'Giy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc3c5'] = ['Gxx', 'Gxy', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c6'] = ['Gxy', 'Gxy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c7'] = ['Gxy', 'Gxy', 'Giy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c8'] = ['Gxx', 'Gxy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c9'] = ['Gxx', 'Gxx', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c10'] = ['Gxy', 'Gxx', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c11'] = ['Gxx', 'Gxx', 'Gix', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c12'] = ['Gxy', 'Gxx', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c13'] = ['Gxx', 'Gxx', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c14'] = ['Gxx', 'Gxy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc3c15'] = ['Gxy', 'Gxy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c16'] = ['Gxx', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c17'] = ['Gxx', 'Gxy', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c18'] = ['Gxy', 'Gxy', 'Giy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc3c19'] = ['Gxx', 'Gxy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c20'] = ['Gxx', 'Gxy', 'Giy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc3c21'] = ['Gxy', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc3c22'] = ['Gxx', 'Gxx', 'Gix', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc3c23'] = ['Gxx', 'Gxy', 'Gix', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc4c0'] = ['Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c1'] = ['Gyy', 'Gyx', 'Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c2'] = ['Gyx', 'Gyx', 'Gyx', 'Gxy', 'Gxy', 'Gxy', 'Gii']   
clifford_compilation['Gc4c3'] = ['Gyx', 'Gyx', 'Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c4'] = ['Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gxx', 'Gxx', 'Gii']   
clifford_compilation['Gc4c5'] = ['Gyx', 'Gyy', 'Gyy', 'Gxy', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c6'] = ['Gyy', 'Gyy', 'Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c7'] = ['Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c8'] = ['Gyx', 'Gyy', 'Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c9'] = ['Gyx', 'Gyx', 'Gyy', 'Gxy', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c10'] = ['Gyy', 'Gyx', 'Gyx', 'Gxx', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c11'] = ['Gyx', 'Gyx', 'Gyx', 'Gxy', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c12'] = ['Gyy', 'Gyx', 'Gyx', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c13'] = ['Gyx', 'Gyx', 'Gyx', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c14'] = ['Gyx', 'Gyy', 'Gyy', 'Gxy', 'Gxx', 'Gxx', 'Gix']   
clifford_compilation['Gc4c15'] = ['Gyy', 'Gyy', 'Gyy', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c16'] = ['Gyx', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c17'] = ['Gyx', 'Gyy', 'Gyx', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c18'] = ['Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gxx', 'Gxi', 'Gii']   
clifford_compilation['Gc4c19'] = ['Gyx', 'Gyy', 'Gyy', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c20'] = ['Gyx', 'Gyy', 'Gyy', 'Gxy', 'Gxx', 'Gxi', 'Gii']   
clifford_compilation['Gc4c21'] = ['Gyy', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii']   
clifford_compilation['Gc4c22'] = ['Gyx', 'Gyx', 'Gyx', 'Gxy', 'Gxy', 'Gxi', 'Gii']   
clifford_compilation['Gc4c23'] = ['Gyx', 'Gyy', 'Gyx', 'Gxx', 'Gxx', 'Gxi', 'Gii']   
clifford_compilation['Gc5c0'] = ['Gxi', 'Gyi', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c1'] = ['Gxy', 'Gyx', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c2'] = ['Gxx', 'Gyx', 'Gyx', 'Gyy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc5c3'] = ['Gxx', 'Gyx', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c4'] = ['Gxy', 'Gyy', 'Gyy', 'Gyx', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc5c5'] = ['Gxx', 'Gyy', 'Gyy', 'Gyy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c6'] = ['Gxy', 'Gyy', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c7'] = ['Gxy', 'Gyy', 'Gyy', 'Gyx', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c8'] = ['Gxx', 'Gyy', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c9'] = ['Gxx', 'Gyx', 'Gyy', 'Gyy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c10'] = ['Gxy', 'Gyx', 'Gyx', 'Gyx', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c11'] = ['Gxx', 'Gyx', 'Gyx', 'Gyy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c12'] = ['Gxy', 'Gyx', 'Gyx', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c13'] = ['Gxx', 'Gyx', 'Gyx', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c14'] = ['Gxx', 'Gyy', 'Gyy', 'Gyy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc5c15'] = ['Gxy', 'Gyy', 'Gyy', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c16'] = ['Gxx', 'Gyi', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c17'] = ['Gxx', 'Gyy', 'Gyx', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c18'] = ['Gxy', 'Gyy', 'Gyy', 'Gyx', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc5c19'] = ['Gxx', 'Gyy', 'Gyy', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c20'] = ['Gxx', 'Gyy', 'Gyy', 'Gyy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc5c21'] = ['Gxy', 'Gyi', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc5c22'] = ['Gxx', 'Gyx', 'Gyx', 'Gyy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc5c23'] = ['Gxx', 'Gyy', 'Gyx', 'Gyx', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc6c0'] = ['Gyi', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c1'] = ['Gyy', 'Gyx', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c2'] = ['Gyx', 'Gyx', 'Gix', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc6c3'] = ['Gyx', 'Gyx', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c4'] = ['Gyy', 'Gyy', 'Giy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc6c5'] = ['Gyx', 'Gyy', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c6'] = ['Gyy', 'Gyy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c7'] = ['Gyy', 'Gyy', 'Giy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c8'] = ['Gyx', 'Gyy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c9'] = ['Gyx', 'Gyx', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c10'] = ['Gyy', 'Gyx', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c11'] = ['Gyx', 'Gyx', 'Gix', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c12'] = ['Gyy', 'Gyx', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c13'] = ['Gyx', 'Gyx', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c14'] = ['Gyx', 'Gyy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc6c15'] = ['Gyy', 'Gyy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c16'] = ['Gyx', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c17'] = ['Gyx', 'Gyy', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c18'] = ['Gyy', 'Gyy', 'Giy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc6c19'] = ['Gyx', 'Gyy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c20'] = ['Gyx', 'Gyy', 'Giy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc6c21'] = ['Gyy', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc6c22'] = ['Gyx', 'Gyx', 'Gix', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc6c23'] = ['Gyx', 'Gyy', 'Gix', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc7c0'] = ['Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c1'] = ['Gyy', 'Gyx', 'Gyi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c2'] = ['Gyx', 'Gyx', 'Gyx', 'Gxy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc7c3'] = ['Gyx', 'Gyx', 'Gyi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c4'] = ['Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc7c5'] = ['Gyx', 'Gyy', 'Gyy', 'Gxy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c6'] = ['Gyy', 'Gyy', 'Gyi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c7'] = ['Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c8'] = ['Gyx', 'Gyy', 'Gyi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c9'] = ['Gyx', 'Gyx', 'Gyy', 'Gxy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c10'] = ['Gyy', 'Gyx', 'Gyx', 'Gxx', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c11'] = ['Gyx', 'Gyx', 'Gyx', 'Gxy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c12'] = ['Gyy', 'Gyx', 'Gyx', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c13'] = ['Gyx', 'Gyx', 'Gyx', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c14'] = ['Gyx', 'Gyy', 'Gyy', 'Gxy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc7c15'] = ['Gyy', 'Gyy', 'Gyy', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c16'] = ['Gyx', 'Gyi', 'Gyi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c17'] = ['Gyx', 'Gyy', 'Gyx', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c18'] = ['Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc7c19'] = ['Gyx', 'Gyy', 'Gyy', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c20'] = ['Gyx', 'Gyy', 'Gyy', 'Gxy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc7c21'] = ['Gyy', 'Gyi', 'Gyi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc7c22'] = ['Gyx', 'Gyx', 'Gyx', 'Gxy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc7c23'] = ['Gyx', 'Gyy', 'Gyx', 'Gxx', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc8c0'] = ['Gxi', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c1'] = ['Gxy', 'Gyx', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c2'] = ['Gxx', 'Gyx', 'Gix', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc8c3'] = ['Gxx', 'Gyx', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c4'] = ['Gxy', 'Gyy', 'Giy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc8c5'] = ['Gxx', 'Gyy', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c6'] = ['Gxy', 'Gyy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c7'] = ['Gxy', 'Gyy', 'Giy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c8'] = ['Gxx', 'Gyy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c9'] = ['Gxx', 'Gyx', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c10'] = ['Gxy', 'Gyx', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c11'] = ['Gxx', 'Gyx', 'Gix', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c12'] = ['Gxy', 'Gyx', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c13'] = ['Gxx', 'Gyx', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c14'] = ['Gxx', 'Gyy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc8c15'] = ['Gxy', 'Gyy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c16'] = ['Gxx', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c17'] = ['Gxx', 'Gyy', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c18'] = ['Gxy', 'Gyy', 'Giy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc8c19'] = ['Gxx', 'Gyy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c20'] = ['Gxx', 'Gyy', 'Giy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc8c21'] = ['Gxy', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc8c22'] = ['Gxx', 'Gyx', 'Gix', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc8c23'] = ['Gxx', 'Gyy', 'Gix', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc9c0'] = ['Gxi', 'Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c1'] = ['Gxy', 'Gxx', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c2'] = ['Gxx', 'Gxx', 'Gyx', 'Gyy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc9c3'] = ['Gxx', 'Gxx', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c4'] = ['Gxy', 'Gxy', 'Gyy', 'Gyx', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc9c5'] = ['Gxx', 'Gxy', 'Gyy', 'Gyy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c6'] = ['Gxy', 'Gxy', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c7'] = ['Gxy', 'Gxy', 'Gyy', 'Gyx', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c8'] = ['Gxx', 'Gxy', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c9'] = ['Gxx', 'Gxx', 'Gyy', 'Gyy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c10'] = ['Gxy', 'Gxx', 'Gyx', 'Gyx', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c11'] = ['Gxx', 'Gxx', 'Gyx', 'Gyy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c12'] = ['Gxy', 'Gxx', 'Gyx', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c13'] = ['Gxx', 'Gxx', 'Gyx', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c14'] = ['Gxx', 'Gxy', 'Gyy', 'Gyy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc9c15'] = ['Gxy', 'Gxy', 'Gyy', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c16'] = ['Gxx', 'Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c17'] = ['Gxx', 'Gxy', 'Gyx', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c18'] = ['Gxy', 'Gxy', 'Gyy', 'Gyx', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc9c19'] = ['Gxx', 'Gxy', 'Gyy', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c20'] = ['Gxx', 'Gxy', 'Gyy', 'Gyy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc9c21'] = ['Gxy', 'Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc9c22'] = ['Gxx', 'Gxx', 'Gyx', 'Gyy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc9c23'] = ['Gxx', 'Gxy', 'Gyx', 'Gyx', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc10c0'] = ['Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c1'] = ['Gyy', 'Gxx', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c2'] = ['Gyx', 'Gxx', 'Gxx', 'Gxy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc10c3'] = ['Gyx', 'Gxx', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c4'] = ['Gyy', 'Gxy', 'Gxy', 'Gxx', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc10c5'] = ['Gyx', 'Gxy', 'Gxy', 'Gxy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c6'] = ['Gyy', 'Gxy', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c7'] = ['Gyy', 'Gxy', 'Gxy', 'Gxx', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c8'] = ['Gyx', 'Gxy', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c9'] = ['Gyx', 'Gxx', 'Gxy', 'Gxy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c10'] = ['Gyy', 'Gxx', 'Gxx', 'Gxx', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c11'] = ['Gyx', 'Gxx', 'Gxx', 'Gxy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c12'] = ['Gyy', 'Gxx', 'Gxx', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c13'] = ['Gyx', 'Gxx', 'Gxx', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c14'] = ['Gyx', 'Gxy', 'Gxy', 'Gxy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc10c15'] = ['Gyy', 'Gxy', 'Gxy', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c16'] = ['Gyx', 'Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c17'] = ['Gyx', 'Gxy', 'Gxx', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c18'] = ['Gyy', 'Gxy', 'Gxy', 'Gxx', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc10c19'] = ['Gyx', 'Gxy', 'Gxy', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c20'] = ['Gyx', 'Gxy', 'Gxy', 'Gxy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc10c21'] = ['Gyy', 'Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc10c22'] = ['Gyx', 'Gxx', 'Gxx', 'Gxy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc10c23'] = ['Gyx', 'Gxy', 'Gxx', 'Gxx', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc11c0'] = ['Gxi', 'Gxi', 'Gxi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c1'] = ['Gxy', 'Gxx', 'Gxi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c2'] = ['Gxx', 'Gxx', 'Gxx', 'Gyy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc11c3'] = ['Gxx', 'Gxx', 'Gxi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c4'] = ['Gxy', 'Gxy', 'Gxy', 'Gyx', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc11c5'] = ['Gxx', 'Gxy', 'Gxy', 'Gyy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c6'] = ['Gxy', 'Gxy', 'Gxi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c7'] = ['Gxy', 'Gxy', 'Gxy', 'Gyx', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c8'] = ['Gxx', 'Gxy', 'Gxi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c9'] = ['Gxx', 'Gxx', 'Gxy', 'Gyy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c10'] = ['Gxy', 'Gxx', 'Gxx', 'Gyx', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c11'] = ['Gxx', 'Gxx', 'Gxx', 'Gyy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c12'] = ['Gxy', 'Gxx', 'Gxx', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c13'] = ['Gxx', 'Gxx', 'Gxx', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c14'] = ['Gxx', 'Gxy', 'Gxy', 'Gyy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc11c15'] = ['Gxy', 'Gxy', 'Gxy', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c16'] = ['Gxx', 'Gxi', 'Gxi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c17'] = ['Gxx', 'Gxy', 'Gxx', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c18'] = ['Gxy', 'Gxy', 'Gxy', 'Gyx', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc11c19'] = ['Gxx', 'Gxy', 'Gxy', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c20'] = ['Gxx', 'Gxy', 'Gxy', 'Gyy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc11c21'] = ['Gxy', 'Gxi', 'Gxi', 'Gyi', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc11c22'] = ['Gxx', 'Gxx', 'Gxx', 'Gyy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc11c23'] = ['Gxx', 'Gxy', 'Gxx', 'Gyx', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc12c0'] = ['Gyi', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c1'] = ['Gyy', 'Gxx', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c2'] = ['Gyx', 'Gxx', 'Gxx', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc12c3'] = ['Gyx', 'Gxx', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c4'] = ['Gyy', 'Gxy', 'Gxy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc12c5'] = ['Gyx', 'Gxy', 'Gxy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c6'] = ['Gyy', 'Gxy', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c7'] = ['Gyy', 'Gxy', 'Gxy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c8'] = ['Gyx', 'Gxy', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c9'] = ['Gyx', 'Gxx', 'Gxy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c10'] = ['Gyy', 'Gxx', 'Gxx', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c11'] = ['Gyx', 'Gxx', 'Gxx', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c12'] = ['Gyy', 'Gxx', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c13'] = ['Gyx', 'Gxx', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c14'] = ['Gyx', 'Gxy', 'Gxy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc12c15'] = ['Gyy', 'Gxy', 'Gxy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c16'] = ['Gyx', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c17'] = ['Gyx', 'Gxy', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c18'] = ['Gyy', 'Gxy', 'Gxy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc12c19'] = ['Gyx', 'Gxy', 'Gxy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c20'] = ['Gyx', 'Gxy', 'Gxy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc12c21'] = ['Gyy', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc12c22'] = ['Gyx', 'Gxx', 'Gxx', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc12c23'] = ['Gyx', 'Gxy', 'Gxx', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc13c0'] = ['Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c1'] = ['Gxy', 'Gxx', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c2'] = ['Gxx', 'Gxx', 'Gxx', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc13c3'] = ['Gxx', 'Gxx', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c4'] = ['Gxy', 'Gxy', 'Gxy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc13c5'] = ['Gxx', 'Gxy', 'Gxy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c6'] = ['Gxy', 'Gxy', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c7'] = ['Gxy', 'Gxy', 'Gxy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c8'] = ['Gxx', 'Gxy', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c9'] = ['Gxx', 'Gxx', 'Gxy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c10'] = ['Gxy', 'Gxx', 'Gxx', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c11'] = ['Gxx', 'Gxx', 'Gxx', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c12'] = ['Gxy', 'Gxx', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c13'] = ['Gxx', 'Gxx', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c14'] = ['Gxx', 'Gxy', 'Gxy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc13c15'] = ['Gxy', 'Gxy', 'Gxy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c16'] = ['Gxx', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c17'] = ['Gxx', 'Gxy', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c18'] = ['Gxy', 'Gxy', 'Gxy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc13c19'] = ['Gxx', 'Gxy', 'Gxy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c20'] = ['Gxx', 'Gxy', 'Gxy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc13c21'] = ['Gxy', 'Gxi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc13c22'] = ['Gxx', 'Gxx', 'Gxx', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc13c23'] = ['Gxx', 'Gxy', 'Gxx', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc14c0'] = ['Gxi', 'Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c1'] = ['Gxy', 'Gyx', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c2'] = ['Gxx', 'Gyx', 'Gyx', 'Gyy', 'Gxy', 'Gxy', 'Gxi']   
clifford_compilation['Gc14c3'] = ['Gxx', 'Gyx', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c4'] = ['Gxy', 'Gyy', 'Gyy', 'Gyx', 'Gxx', 'Gxx', 'Gxi']   
clifford_compilation['Gc14c5'] = ['Gxx', 'Gyy', 'Gyy', 'Gyy', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c6'] = ['Gxy', 'Gyy', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c7'] = ['Gxy', 'Gyy', 'Gyy', 'Gyx', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c8'] = ['Gxx', 'Gyy', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c9'] = ['Gxx', 'Gyx', 'Gyy', 'Gyy', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c10'] = ['Gxy', 'Gyx', 'Gyx', 'Gyx', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c11'] = ['Gxx', 'Gyx', 'Gyx', 'Gyy', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c12'] = ['Gxy', 'Gyx', 'Gyx', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c13'] = ['Gxx', 'Gyx', 'Gyx', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c14'] = ['Gxx', 'Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gxx', 'Gxx']   
clifford_compilation['Gc14c15'] = ['Gxy', 'Gyy', 'Gyy', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c16'] = ['Gxx', 'Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c17'] = ['Gxx', 'Gyy', 'Gyx', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c18'] = ['Gxy', 'Gyy', 'Gyy', 'Gyx', 'Gxx', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c19'] = ['Gxx', 'Gyy', 'Gyy', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c20'] = ['Gxx', 'Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c21'] = ['Gxy', 'Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c22'] = ['Gxx', 'Gyx', 'Gyx', 'Gyy', 'Gxy', 'Gxi', 'Gxi']   
clifford_compilation['Gc14c23'] = ['Gxx', 'Gyy', 'Gyx', 'Gyx', 'Gxx', 'Gxi', 'Gxi']   
clifford_compilation['Gc15c0'] = ['Gyi', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c1'] = ['Gyy', 'Gyx', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c2'] = ['Gyx', 'Gyx', 'Gyx', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc15c3'] = ['Gyx', 'Gyx', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c4'] = ['Gyy', 'Gyy', 'Gyy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc15c5'] = ['Gyx', 'Gyy', 'Gyy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c6'] = ['Gyy', 'Gyy', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c7'] = ['Gyy', 'Gyy', 'Gyy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c8'] = ['Gyx', 'Gyy', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c9'] = ['Gyx', 'Gyx', 'Gyy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c10'] = ['Gyy', 'Gyx', 'Gyx', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c11'] = ['Gyx', 'Gyx', 'Gyx', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c12'] = ['Gyy', 'Gyx', 'Gyx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c13'] = ['Gyx', 'Gyx', 'Gyx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c14'] = ['Gyx', 'Gyy', 'Gyy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc15c15'] = ['Gyy', 'Gyy', 'Gyy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c16'] = ['Gyx', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c17'] = ['Gyx', 'Gyy', 'Gyx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c18'] = ['Gyy', 'Gyy', 'Gyy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc15c19'] = ['Gyx', 'Gyy', 'Gyy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c20'] = ['Gyx', 'Gyy', 'Gyy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc15c21'] = ['Gyy', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc15c22'] = ['Gyx', 'Gyx', 'Gyx', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc15c23'] = ['Gyx', 'Gyy', 'Gyx', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc16c0'] = ['Gxi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c1'] = ['Gxy', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c2'] = ['Gxx', 'Gix', 'Gix', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc16c3'] = ['Gxx', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c4'] = ['Gxy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc16c5'] = ['Gxx', 'Giy', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c6'] = ['Gxy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c7'] = ['Gxy', 'Giy', 'Giy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c8'] = ['Gxx', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c9'] = ['Gxx', 'Gix', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c10'] = ['Gxy', 'Gix', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c11'] = ['Gxx', 'Gix', 'Gix', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c12'] = ['Gxy', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c13'] = ['Gxx', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c14'] = ['Gxx', 'Giy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc16c15'] = ['Gxy', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c16'] = ['Gxx', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c17'] = ['Gxx', 'Giy', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c18'] = ['Gxy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc16c19'] = ['Gxx', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c20'] = ['Gxx', 'Giy', 'Giy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc16c21'] = ['Gxy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc16c22'] = ['Gxx', 'Gix', 'Gix', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc16c23'] = ['Gxx', 'Giy', 'Gix', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc17c0'] = ['Gxi', 'Gyi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c1'] = ['Gxy', 'Gyx', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c2'] = ['Gxx', 'Gyx', 'Gxx', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc17c3'] = ['Gxx', 'Gyx', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c4'] = ['Gxy', 'Gyy', 'Gxy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc17c5'] = ['Gxx', 'Gyy', 'Gxy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c6'] = ['Gxy', 'Gyy', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c7'] = ['Gxy', 'Gyy', 'Gxy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c8'] = ['Gxx', 'Gyy', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c9'] = ['Gxx', 'Gyx', 'Gxy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c10'] = ['Gxy', 'Gyx', 'Gxx', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c11'] = ['Gxx', 'Gyx', 'Gxx', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c12'] = ['Gxy', 'Gyx', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c13'] = ['Gxx', 'Gyx', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c14'] = ['Gxx', 'Gyy', 'Gxy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc17c15'] = ['Gxy', 'Gyy', 'Gxy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c16'] = ['Gxx', 'Gyi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c17'] = ['Gxx', 'Gyy', 'Gxx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c18'] = ['Gxy', 'Gyy', 'Gxy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc17c19'] = ['Gxx', 'Gyy', 'Gxy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c20'] = ['Gxx', 'Gyy', 'Gxy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc17c21'] = ['Gxy', 'Gyi', 'Gxi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc17c22'] = ['Gxx', 'Gyx', 'Gxx', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc17c23'] = ['Gxx', 'Gyy', 'Gxx', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc18c0'] = ['Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c1'] = ['Gyy', 'Gyx', 'Gyi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c2'] = ['Gyx', 'Gyx', 'Gyx', 'Gxy', 'Gxy', 'Giy', 'Gii']   
clifford_compilation['Gc18c3'] = ['Gyx', 'Gyx', 'Gyi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c4'] = ['Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gxx', 'Gix', 'Gii']   
clifford_compilation['Gc18c5'] = ['Gyx', 'Gyy', 'Gyy', 'Gxy', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c6'] = ['Gyy', 'Gyy', 'Gyi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c7'] = ['Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c8'] = ['Gyx', 'Gyy', 'Gyi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c9'] = ['Gyx', 'Gyx', 'Gyy', 'Gxy', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c10'] = ['Gyy', 'Gyx', 'Gyx', 'Gxx', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c11'] = ['Gyx', 'Gyx', 'Gyx', 'Gxy', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c12'] = ['Gyy', 'Gyx', 'Gyx', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c13'] = ['Gyx', 'Gyx', 'Gyx', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c14'] = ['Gyx', 'Gyy', 'Gyy', 'Gxy', 'Gxx', 'Gix', 'Gix']   
clifford_compilation['Gc18c15'] = ['Gyy', 'Gyy', 'Gyy', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c16'] = ['Gyx', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c17'] = ['Gyx', 'Gyy', 'Gyx', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c18'] = ['Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gxx', 'Gii', 'Gii']   
clifford_compilation['Gc18c19'] = ['Gyx', 'Gyy', 'Gyy', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c20'] = ['Gyx', 'Gyy', 'Gyy', 'Gxy', 'Gxx', 'Gii', 'Gii']   
clifford_compilation['Gc18c21'] = ['Gyy', 'Gyi', 'Gyi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc18c22'] = ['Gyx', 'Gyx', 'Gyx', 'Gxy', 'Gxy', 'Gii', 'Gii']   
clifford_compilation['Gc18c23'] = ['Gyx', 'Gyy', 'Gyx', 'Gxx', 'Gxx', 'Gii', 'Gii']   
clifford_compilation['Gc19c0'] = ['Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c1'] = ['Gxy', 'Gyx', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c2'] = ['Gxx', 'Gyx', 'Gyx', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc19c3'] = ['Gxx', 'Gyx', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c4'] = ['Gxy', 'Gyy', 'Gyy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc19c5'] = ['Gxx', 'Gyy', 'Gyy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c6'] = ['Gxy', 'Gyy', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c7'] = ['Gxy', 'Gyy', 'Gyy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c8'] = ['Gxx', 'Gyy', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c9'] = ['Gxx', 'Gyx', 'Gyy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c10'] = ['Gxy', 'Gyx', 'Gyx', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c11'] = ['Gxx', 'Gyx', 'Gyx', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c12'] = ['Gxy', 'Gyx', 'Gyx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c13'] = ['Gxx', 'Gyx', 'Gyx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c14'] = ['Gxx', 'Gyy', 'Gyy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc19c15'] = ['Gxy', 'Gyy', 'Gyy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c16'] = ['Gxx', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c17'] = ['Gxx', 'Gyy', 'Gyx', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c18'] = ['Gxy', 'Gyy', 'Gyy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc19c19'] = ['Gxx', 'Gyy', 'Gyy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c20'] = ['Gxx', 'Gyy', 'Gyy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc19c21'] = ['Gxy', 'Gyi', 'Gyi', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc19c22'] = ['Gxx', 'Gyx', 'Gyx', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc19c23'] = ['Gxx', 'Gyy', 'Gyx', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc20c0'] = ['Gxi', 'Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c1'] = ['Gxy', 'Gyx', 'Gyi', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c2'] = ['Gxx', 'Gyx', 'Gyx', 'Gyy', 'Gxy', 'Giy', 'Gii']   
clifford_compilation['Gc20c3'] = ['Gxx', 'Gyx', 'Gyi', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c4'] = ['Gxy', 'Gyy', 'Gyy', 'Gyx', 'Gxx', 'Gix', 'Gii']   
clifford_compilation['Gc20c5'] = ['Gxx', 'Gyy', 'Gyy', 'Gyy', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c6'] = ['Gxy', 'Gyy', 'Gyi', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c7'] = ['Gxy', 'Gyy', 'Gyy', 'Gyx', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c8'] = ['Gxx', 'Gyy', 'Gyi', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c9'] = ['Gxx', 'Gyx', 'Gyy', 'Gyy', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c10'] = ['Gxy', 'Gyx', 'Gyx', 'Gyx', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c11'] = ['Gxx', 'Gyx', 'Gyx', 'Gyy', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c12'] = ['Gxy', 'Gyx', 'Gyx', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c13'] = ['Gxx', 'Gyx', 'Gyx', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c14'] = ['Gxx', 'Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gix', 'Gix']   
clifford_compilation['Gc20c15'] = ['Gxy', 'Gyy', 'Gyy', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c16'] = ['Gxx', 'Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c17'] = ['Gxx', 'Gyy', 'Gyx', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c18'] = ['Gxy', 'Gyy', 'Gyy', 'Gyx', 'Gxx', 'Gii', 'Gii']   
clifford_compilation['Gc20c19'] = ['Gxx', 'Gyy', 'Gyy', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c20'] = ['Gxx', 'Gyy', 'Gyy', 'Gyy', 'Gxx', 'Gii', 'Gii']   
clifford_compilation['Gc20c21'] = ['Gxy', 'Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc20c22'] = ['Gxx', 'Gyx', 'Gyx', 'Gyy', 'Gxy', 'Gii', 'Gii']   
clifford_compilation['Gc20c23'] = ['Gxx', 'Gyy', 'Gyx', 'Gyx', 'Gxx', 'Gii', 'Gii']   
clifford_compilation['Gc21c0'] = ['Gyi', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c1'] = ['Gyy', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c2'] = ['Gyx', 'Gix', 'Gix', 'Giy', 'Giy', 'Giy', 'Gii']   
clifford_compilation['Gc21c3'] = ['Gyx', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c4'] = ['Gyy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gix', 'Gii']   
clifford_compilation['Gc21c5'] = ['Gyx', 'Giy', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c6'] = ['Gyy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c7'] = ['Gyy', 'Giy', 'Giy', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c8'] = ['Gyx', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c9'] = ['Gyx', 'Gix', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c10'] = ['Gyy', 'Gix', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c11'] = ['Gyx', 'Gix', 'Gix', 'Giy', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c12'] = ['Gyy', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c13'] = ['Gyx', 'Gix', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c14'] = ['Gyx', 'Giy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gix']   
clifford_compilation['Gc21c15'] = ['Gyy', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c16'] = ['Gyx', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c17'] = ['Gyx', 'Giy', 'Gix', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c18'] = ['Gyy', 'Giy', 'Giy', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc21c19'] = ['Gyx', 'Giy', 'Giy', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c20'] = ['Gyx', 'Giy', 'Giy', 'Giy', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc21c21'] = ['Gyy', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gii']   
clifford_compilation['Gc21c22'] = ['Gyx', 'Gix', 'Gix', 'Giy', 'Giy', 'Gii', 'Gii']   
clifford_compilation['Gc21c23'] = ['Gyx', 'Giy', 'Gix', 'Gix', 'Gix', 'Gii', 'Gii']   
clifford_compilation['Gc22c0'] = ['Gxi', 'Gxi', 'Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c1'] = ['Gxy', 'Gxx', 'Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c2'] = ['Gxx', 'Gxx', 'Gxx', 'Gyy', 'Gyy', 'Giy', 'Gii']   
clifford_compilation['Gc22c3'] = ['Gxx', 'Gxx', 'Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c4'] = ['Gxy', 'Gxy', 'Gxy', 'Gyx', 'Gyx', 'Gix', 'Gii']   
clifford_compilation['Gc22c5'] = ['Gxx', 'Gxy', 'Gxy', 'Gyy', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c6'] = ['Gxy', 'Gxy', 'Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c7'] = ['Gxy', 'Gxy', 'Gxy', 'Gyx', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c8'] = ['Gxx', 'Gxy', 'Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c9'] = ['Gxx', 'Gxx', 'Gxy', 'Gyy', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c10'] = ['Gxy', 'Gxx', 'Gxx', 'Gyx', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c11'] = ['Gxx', 'Gxx', 'Gxx', 'Gyy', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c12'] = ['Gxy', 'Gxx', 'Gxx', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c13'] = ['Gxx', 'Gxx', 'Gxx', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c14'] = ['Gxx', 'Gxy', 'Gxy', 'Gyy', 'Gyx', 'Gix', 'Gix']   
clifford_compilation['Gc22c15'] = ['Gxy', 'Gxy', 'Gxy', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c16'] = ['Gxx', 'Gxi', 'Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c17'] = ['Gxx', 'Gxy', 'Gxx', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c18'] = ['Gxy', 'Gxy', 'Gxy', 'Gyx', 'Gyx', 'Gii', 'Gii']   
clifford_compilation['Gc22c19'] = ['Gxx', 'Gxy', 'Gxy', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c20'] = ['Gxx', 'Gxy', 'Gxy', 'Gyy', 'Gyx', 'Gii', 'Gii']   
clifford_compilation['Gc22c21'] = ['Gxy', 'Gxi', 'Gxi', 'Gyi', 'Gyi', 'Gii', 'Gii']   
clifford_compilation['Gc22c22'] = ['Gxx', 'Gxx', 'Gxx', 'Gyy', 'Gyy', 'Gii', 'Gii']   
clifford_compilation['Gc22c23'] = ['Gxx', 'Gxy', 'Gxx', 'Gyx', 'Gyx', 'Gii', 'Gii']   
clifford_compilation['Gc23c0'] = ['Gxi', 'Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c1'] = ['Gxy', 'Gyx', 'Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c2'] = ['Gxx', 'Gyx', 'Gxx', 'Gxy', 'Gxy', 'Giy', 'Gii']   
clifford_compilation['Gc23c3'] = ['Gxx', 'Gyx', 'Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c4'] = ['Gxy', 'Gyy', 'Gxy', 'Gxx', 'Gxx', 'Gix', 'Gii']   
clifford_compilation['Gc23c5'] = ['Gxx', 'Gyy', 'Gxy', 'Gxy', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c6'] = ['Gxy', 'Gyy', 'Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c7'] = ['Gxy', 'Gyy', 'Gxy', 'Gxx', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c8'] = ['Gxx', 'Gyy', 'Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c9'] = ['Gxx', 'Gyx', 'Gxy', 'Gxy', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c10'] = ['Gxy', 'Gyx', 'Gxx', 'Gxx', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c11'] = ['Gxx', 'Gyx', 'Gxx', 'Gxy', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c12'] = ['Gxy', 'Gyx', 'Gxx', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c13'] = ['Gxx', 'Gyx', 'Gxx', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c14'] = ['Gxx', 'Gyy', 'Gxy', 'Gxy', 'Gxx', 'Gix', 'Gix']   
clifford_compilation['Gc23c15'] = ['Gxy', 'Gyy', 'Gxy', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c16'] = ['Gxx', 'Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c17'] = ['Gxx', 'Gyy', 'Gxx', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c18'] = ['Gxy', 'Gyy', 'Gxy', 'Gxx', 'Gxx', 'Gii', 'Gii']   
clifford_compilation['Gc23c19'] = ['Gxx', 'Gyy', 'Gxy', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c20'] = ['Gxx', 'Gyy', 'Gxy', 'Gxy', 'Gxx', 'Gii', 'Gii']   
clifford_compilation['Gc23c21'] = ['Gxy', 'Gyi', 'Gxi', 'Gxi', 'Gxi', 'Gii', 'Gii']   
clifford_compilation['Gc23c22'] = ['Gxx', 'Gyx', 'Gxx', 'Gxy', 'Gxy', 'Gii', 'Gii']   
clifford_compilation['Gc23c23'] = ['Gxx', 'Gyy', 'Gxx', 'Gxx', 'Gxx', 'Gii', 'Gii'] 
