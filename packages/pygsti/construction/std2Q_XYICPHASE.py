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

import numpy as _np
from . import gatestringconstruction as _strc
from . import gatesetconstruction as _setc
from . import spamspecconstruction as _spamc
from ..tools import gatetools as _gt

description = "I*X(pi/2), I*Y(pi/2), X(pi/2)*I, Y(pi/2)*I, and CPHASE gates"

gates = ['Gix','Giy','Gxi','Gyi','Gcphase']

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
  ('Gxi', 'Gyi'),
  ('Gix', 'Giy'),
  ('Gxi', 'Gcphase'),
  ('Gix', 'Gcphase'),
  ('Gix', 'Gyi'),
  ('Gix', 'Gxi'),
  ('Gxi', 'Gyi', 'Gii'),
  ('Gxi', 'Gii', 'Gyi'),
  ('Gxi', 'Gii', 'Gii'),
  ('Gyi', 'Gii', 'Gii'),
  ('Gix', 'Giy', 'Gii'),
  ('Gix', 'Gii', 'Giy'),
  ('Gix', 'Gii', 'Gii'),
  ('Giy', 'Gii', 'Gii'),
  ('Gix', 'Gyi', 'Gcphase'),
  ('Giy', 'Gcphase', 'Gyi'),
  ('Giy', 'Gxi', 'Gcphase'),
  ('Gyi', 'Gyi', 'Gcphase'),
  ('Gix', 'Gcphase', 'Gyi'),
  ('Gix', 'Gyi', 'Giy'),
  ('Gix', 'Gcphase', 'Gxi'),
  ('Gii', 'Gcphase', 'Gcphase'),
  ('Giy', 'Gyi', 'Gcphase'),
  ('Gii', 'Giy', 'Gxi'),
  ('Gxi', 'Gcphase', 'Gcphase'),
  ('Gix', 'Gcphase', 'Gcphase'),
  ('Gix', 'Gyi', 'Gxi'),
  ('Gii', 'Gcphase', 'Giy'),
  ('Gix', 'Gcphase', 'Giy'),
  ('Gii', 'Giy', 'Gyi'),
  ('Gxi', 'Gxi', 'Gii', 'Gyi'),
  ('Gxi', 'Gyi', 'Gyi', 'Gii'),
  ('Gix', 'Gix', 'Gii', 'Giy'),
  ('Gix', 'Giy', 'Giy', 'Gii'),
  ('Gcphase', 'Gcphase', 'Giy', 'Gcphase'),
  ('Giy', 'Gcphase', 'Gxi', 'Giy'),
  ('Giy', 'Gix', 'Gyi', 'Giy'),
  ('Gyi', 'Gix', 'Gix', 'Gcphase', 'Gxi'),
  ('Gix', 'Gcphase', 'Gxi', 'Gxi', 'Giy'),
  ('Gyi', 'Gyi', 'Giy', 'Gcphase', 'Giy'),
  ('Gcphase', 'Gcphase', 'Gcphase', 'Gix', 'Gxi'),
  ('Giy', 'Gxi', 'Gcphase', 'Gxi', 'Gxi'),
  ('Gyi', 'Gcphase', 'Giy', 'Gix', 'Giy'),
  ('Gyi', 'Gcphase', 'Gix', 'Gyi', 'Gxi'),
  ('Gcphase', 'Gix', 'Gyi', 'Gii', 'Gii'),
  ('Gcphase', 'Gyi', 'Giy', 'Gcphase', 'Gyi'),
  ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'),
  ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'),
  ('Gxi', 'Giy', 'Giy', 'Gyi', 'Giy', 'Gcphase'),
  ('Gyi', 'Gxi', 'Giy', 'Gyi', 'Gcphase', 'Gyi'),
  ('Gcphase', 'Gyi', 'Gii', 'Gix', 'Gxi', 'Gix'),
  ('Gix', 'Gyi', 'Giy', 'Giy', 'Gxi', 'Gxi'),
  ('Gyi', 'Gcphase', 'Gii', 'Gix', 'Gxi', 'Gii'),
  ('Gcphase', 'Gii', 'Gxi', 'Gyi', 'Gyi', 'Giy'),
  ('Gcphase', 'Gii', 'Gxi', 'Gcphase', 'Gix', 'Gxi'),
  ('Gxi', 'Gyi', 'Gyi', 'Gcphase', 'Gix', 'Gix', 'Giy'),
  ('Gcphase', 'Gcphase', 'Gcphase', 'Gxi', 'Gix', 'Gii', 'Giy'),
  ('Giy', 'Gxi', 'Gxi', 'Gcphase', 'Gii', 'Gxi', 'Gxi'),
  ('Gyi', 'Gii', 'Giy', 'Gyi', 'Gcphase', 'Gxi', 'Gii'),
  ('Gix', 'Giy', 'Gix', 'Gyi', 'Gxi', 'Gii', 'Gxi'),
  ('Gxi', 'Giy', 'Gix', 'Gcphase', 'Giy', 'Gix', 'Gii'),
  ('Giy', 'Gxi', 'Gyi', 'Gxi', 'Gcphase', 'Gyi', 'Gix'),
  ('Giy', 'Giy', 'Gix', 'Gii', 'Gix', 'Gxi', 'Gxi'),
  ('Gii', 'Gyi', 'Gxi', 'Gcphase', 'Gcphase', 'Gix', 'Gcphase'),
  ('Gcphase', 'Gyi', 'Gcphase', 'Gix', 'Gxi', 'Gcphase', 'Gxi', 'Gcphase'),
  ('Giy', 'Gcphase', 'Gxi', 'Gcphase', 'Gix', 'Gxi', 'Gxi', 'Gyi'),
  ('Gxi', 'Giy', 'Giy', 'Giy', 'Gcphase', 'Gix', 'Gyi', 'Gyi'),
  ('Gii', 'Gii', 'Gcphase', 'Gxi', 'Gix', 'Gxi', 'Gix', 'Gyi'),
  ('Gxi', 'Giy', 'Gix', 'Gcphase', 'Gii', 'Gyi', 'Gyi', 'Giy'),
  ('Gyi', 'Gyi', 'Gcphase', 'Gxi', 'Gix', 'Gyi', 'Gix', 'Gyi'),
  ('Gii', 'Giy', 'Gix', 'Gcphase', 'Gcphase', 'Gii', 'Gyi', 'Gxi'),
  ('Gix', 'Gii', 'Gxi', 'Gix', 'Gii', 'Giy', 'Gxi', 'Gii')
  ])

germs_XYnested = _strc.gatestring_list(
[ ('Gii',),
  ('Gxi',),
  ('Gyi',),
  ('Gix',),
  ('Giy',),
  ('Gcphase',),
  ('Gxi', 'Gyi'),
  ('Gix', 'Giy'),
  ('Giy', 'Gyi'),
  ('Gix', 'Gyi'),
  ('Gyi', 'Gcphase'),
  ('Giy', 'Gcphase'),
  ('Gxi', 'Gyi', 'Gii'),
  ('Gxi', 'Gii', 'Gyi'),
  ('Gxi', 'Gii', 'Gii'),
  ('Gyi', 'Gii', 'Gii'),
  ('Gix', 'Giy', 'Gii'),
  ('Gix', 'Gii', 'Giy'),
  ('Gix', 'Gii', 'Gii'),
  ('Giy', 'Gii', 'Gii'),
  ('Gxi', 'Gcphase', 'Gcphase'),
  ('Giy', 'Gxi', 'Gcphase'),
  ('Giy', 'Gcphase', 'Gyi'),
  ('Giy', 'Gyi', 'Gcphase'),
  ('Gix', 'Gxi', 'Gcphase'),
  ('Giy', 'Giy', 'Gcphase'),
  ('Giy', 'Gcphase', 'Gxi'),
  ('Gix', 'Giy', 'Gcphase'),
  ('Giy', 'Gxi', 'Gyi'),
  ('Gix', 'Giy', 'Gyi'),
  ('Gii', 'Gxi', 'Gix'),
  ('Gxi', 'Gxi', 'Gii', 'Gyi'),
  ('Gxi', 'Gyi', 'Gyi', 'Gii'),
  ('Gix', 'Gix', 'Gii', 'Giy'),
  ('Gix', 'Giy', 'Giy', 'Gii'),
  ('Gyi', 'Gyi', 'Gyi', 'Gxi'),
  ('Giy', 'Giy', 'Giy', 'Gix'),
  ('Gxi', 'Gyi', 'Gix', 'Giy'),
  ('Gcphase', 'Gix', 'Gyi', 'Gyi'),
  ('Gcphase', 'Gix', 'Gix', 'Gcphase'),
  ('Gxi', 'Gcphase', 'Gyi', 'Gyi'),
  ('Gyi', 'Gyi', 'Gyi', 'Gix'),
  ('Gii', 'Giy', 'Gxi', 'Gcphase'),
  ('Gyi', 'Gii', 'Giy', 'Gii'),
  ('Giy', 'Gii', 'Gcphase', 'Gii'),
  ('Gix', 'Gix', 'Giy', 'Gcphase', 'Gcphase'),
  ('Gcphase', 'Giy', 'Giy', 'Gix', 'Giy'),
  ('Gyi', 'Gcphase', 'Gix', 'Giy', 'Gyi'),
  ('Giy', 'Gxi', 'Gcphase', 'Gxi', 'Gcphase'),
  ('Gyi', 'Gcphase', 'Gxi', 'Gcphase', 'Gxi'),
  ('Gcphase', 'Gix', 'Gyi', 'Gii', 'Gii'),
  ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'),
  ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'),
  ('Gyi', 'Gxi', 'Gyi', 'Gxi', 'Gxi', 'Gxi'),
  ('Gyi', 'Gxi', 'Gyi', 'Gyi', 'Gxi', 'Gxi'),
  ('Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gyi', 'Gxi'),
  ('Giy', 'Gix', 'Giy', 'Gix', 'Gix', 'Gix'),
  ('Giy', 'Gix', 'Giy', 'Giy', 'Gix', 'Gix'),
  ('Giy', 'Giy', 'Giy', 'Gix', 'Giy', 'Gix'),
  ('Gcphase', 'Gyi', 'Giy', 'Gxi', 'Gix', 'Gcphase'),
  ('Gxi', 'Giy', 'Gxi', 'Gcphase', 'Gyi', 'Gix'),
  ('Gxi', 'Giy', 'Giy', 'Giy', 'Gcphase', 'Gxi'),
  ('Gcphase', 'Gxi', 'Gcphase', 'Gxi', 'Giy', 'Gix'),
  ('Gyi', 'Gix', 'Gyi', 'Gix', 'Gxi', 'Gxi'),
  ('Gix', 'Gcphase', 'Gxi', 'Gix', 'Gxi', 'Gcphase'),
  ('Gxi', 'Giy', 'Gyi', 'Gxi', 'Gcphase', 'Gcphase'),
  ('Gyi', 'Gcphase', 'Gii', 'Gix', 'Gxi', 'Gii'),
  ('Gix', 'Gix', 'Giy', 'Gcphase', 'Giy', 'Gcphase', 'Gxi'),
  ('Giy', 'Gxi', 'Gcphase', 'Gix', 'Gix', 'Giy', 'Giy'),
  ('Gxi', 'Gcphase', 'Giy', 'Gyi', 'Gxi', 'Gix', 'Giy'),
  ('Gcphase', 'Gcphase', 'Gix', 'Gxi', 'Giy', 'Gxi', 'Gxi'),
  ('Gxi', 'Gix', 'Giy', 'Gyi', 'Gix', 'Gix', 'Gix'),
  ('Gxi', 'Gix', 'Gyi', 'Gix', 'Gyi', 'Giy', 'Gyi'),
  ('Gix', 'Gix', 'Gix', 'Gix', 'Gxi', 'Gxi', 'Gyi'),
  ('Giy', 'Gcphase', 'Gxi', 'Gyi', 'Gyi', 'Gcphase', 'Gix', 'Gcphase'),
  ('Gxi', 'Gyi', 'Gxi', 'Giy', 'Gxi', 'Giy', 'Gix', 'Giy'),
  ('Giy', 'Giy', 'Gyi', 'Gix', 'Gcphase', 'Gxi', 'Gyi', 'Gyi'),
  ('Gxi', 'Gix', 'Gcphase', 'Gyi', 'Gix', 'Gcphase', 'Gix', 'Giy'),
  ('Gix', 'Gxi', 'Gxi', 'Giy', 'Gxi', 'Gyi', 'Gix', 'Gcphase'),
  ('Gix', 'Gix', 'Gyi', 'Gxi', 'Giy', 'Gix', 'Gcphase', 'Gyi'),
  ('Gix', 'Giy', 'Gix', 'Gxi', 'Gix', 'Giy', 'Gxi', 'Gxi'),
  ('Giy', 'Gix', 'Gcphase', 'Gxi', 'Gcphase', 'Gxi', 'Gcphase', 'Gyi'),
  ('Gxi', 'Giy', 'Gix', 'Gix', 'Gxi', 'Giy', 'Gxi', 'Gcphase'),
  ('Gyi', 'Gyi', 'Gyi', 'Gyi', 'Gix', 'Giy', 'Gix', 'Gyi')
  ])

#Construct the target gateset
gs_target = _setc.build_gateset(
    [4], [('Q0','Q1')],['Gii','Gix','Giy','Gxi','Gyi','Gcphase'],
    [ "I(Q0):I(Q1)", "I(Q0):X(pi/2,Q1)", "I(Q0):Y(pi/2,Q1)", "X(pi/2,Q0):I(Q1)", "Y(pi/2,Q0):I(Q1)", "CPHASE(Q0,Q1)" ],
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

#Wrong CPHASE (bad 1Q phase factor)
legacy_gs_target = _setc.build_gateset(
    [4], [('Q0','Q1')],['Gix','Giy','Gxi','Gyi','Gcphase'],
    [ "I(Q0):X(pi/2,Q1)", "I(Q0):Y(pi/2,Q1)", "X(pi/2,Q0):I(Q1)", "Y(pi/2,Q0):I(Q1)", "CZ(pi,Q0,Q1)" ],
    prepLabels=['rho0'], prepExpressions=["0"],
    effectLabels=['E0','E1','E2'], effectExpressions=["0","1","2"],
    spamdefs={'upup': ('rho0','E0'), 'updn': ('rho0','E1'),
              'dnup': ('rho0','E2'), 'dndn': ('rho0','remainder') }, basis="pp")
