from __future__ import division, print_function, absolute_import, unicode_literals
#*****************************************************************
#    pyGSTi 0.9:  Copyright 2015 Sandia Corporation
#    This Software is released under the GPL license detailed
#    in the file "license.txt" in the top-level pyGSTi directory
#*****************************************************************
"""
Variables for working with the 2-qubit gate set containing the gates
I*X(pi/2), I*Y(pi/2), I*Z(pi/2), X(pi/2)*I, Y(pi/2)*I, Z(pi/2)*I and CNOT.
"""

import numpy as _np
from . import gatestringconstruction as _strc
from . import gatesetconstruction as _setc
from . import spamspecconstruction as _spamc
from ..tools import gatetools as _gt

description = "I*X(pi/2), I*Y(pi/2), I*Z(pi/2), X(pi/2)*I, Y(pi/2)*I, Z(pi/2)*I and CNOT gates"

gates = ['Gix','Giy','Giz','Gxi','Gyi','Gzi','Gcnot']

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

germs = _strc.gatestring_list( [
        ('Gii',),
        ('Gxi',),
        ('Gyi',),
        ('Gzi',),
        ('Gix',),
        ('Giy',),
        ('Giz',),
        ('Gxi', 'Gyi'),
        ('Gix', 'Giy'),
        ('Gyi', 'Gcnot'),
        ('Gix', 'Gyi'),
        ('Giy', 'Gxi'),
        ('Gix', 'Gxi'),
        ('Gii', 'Gcnot'),
        ('Giz', 'Gyi'),
        ('Gxi', 'Gxi', 'Gyi'),
        ('Gxi', 'Gxi', 'Gzi'),
        ('Gxi', 'Gyi', 'Gyi'),
        ('Gxi', 'Gyi', 'Gzi'),
        ('Gxi', 'Gzi', 'Gzi'),
        ('Gyi', 'Gyi', 'Gzi'),
        ('Gyi', 'Gzi', 'Gzi'),
        ('Gix', 'Gix', 'Giy'),
        ('Gix', 'Gix', 'Giz'),
        ('Gix', 'Giy', 'Giy'),
        ('Gix', 'Giy', 'Giz'),
        ('Gix', 'Giz', 'Giz'),
        ('Giy', 'Giy', 'Giz'),
        ('Giy', 'Giz', 'Giz'),
        ('Gxi', 'Gyi', 'Gii'),
        ('Gxi', 'Gii', 'Gyi'),
        ('Gxi', 'Gii', 'Gii'),
        ('Gyi', 'Gii', 'Gii'),
        ('Gix', 'Giy', 'Gii'),
        ('Gix', 'Gii', 'Giy'),
        ('Gix', 'Gii', 'Gii'),
        ('Giy', 'Gii', 'Gii'),
        ('Giy', 'Gxi', 'Gcnot'),
        ('Giy', 'Gcnot', 'Gxi'),
        ('Gix', 'Gix', 'Gcnot'),
        ('Giy', 'Gcnot', 'Gyi'),
        ('Gix', 'Gyi', 'Gxi'),
        ('Giy', 'Gyi', 'Gcnot'),
        ('Gxi', 'Gcnot', 'Gcnot'),
        ('Gix', 'Giy', 'Gcnot'),
        ('Gii', 'Gcnot', 'Gcnot'),
        ('Gii', 'Gxi', 'Giy'),
        ('Giy', 'Gyi', 'Gxi'),
        ('Gii', 'Gyi', 'Gix'),
        ('Gii', 'Gzi', 'Giy'),
        ('Giz', 'Gcnot', 'Gxi'),
        ('Gzi', 'Gzi', 'Gcnot'),
        ('Gxi', 'Gzi', 'Gcnot'),
        ('Giz', 'Gcnot', 'Gyi'),
        ('Gii', 'Gzi', 'Giz'),
        ('Gix', 'Gcnot', 'Gzi'),
        ('Giz', 'Gxi', 'Gcnot'),
        ('Gyi', 'Gcnot', 'Gzi'),
        ('Gxi', 'Gxi', 'Gii', 'Gyi'),
        ('Gxi', 'Gyi', 'Gyi', 'Gii'),
        ('Gix', 'Gix', 'Gii', 'Giy'),
        ('Gix', 'Giy', 'Giy', 'Gii'),
        ('Gcnot', 'Gcnot', 'Giy', 'Gcnot'),
        ('Giy', 'Gix', 'Gyi', 'Giy'),
        ('Gii', 'Gxi', 'Gxi', 'Gcnot'),
        ('Gxi', 'Gyi', 'Gcnot', 'Gcnot'),
        ('Giy', 'Gcnot', 'Gxi', 'Giy'),
        ('Giz', 'Gzi', 'Gxi', 'Giz'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gzi'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Giz'),
        ('Gxi', 'Gii', 'Gcnot', 'Giy', 'Gix'),
        ('Gyi', 'Gyi', 'Giy', 'Gcnot', 'Giy'),
        ('Gyi', 'Gcnot', 'Giy', 'Gix', 'Giy'),
        ('Giy', 'Gxi', 'Gcnot', 'Gxi', 'Gxi'),
        ('Giy', 'Gyi', 'Gii', 'Giy', 'Gyi'),
        ('Gix', 'Gcnot', 'Gxi', 'Gxi', 'Giy'),
        ('Gyi', 'Gcnot', 'Gix', 'Gyi', 'Gxi'),
        ('Gyi', 'Gix', 'Gix', 'Giy', 'Giy'),
        ('Giz', 'Giz', 'Gyi', 'Gzi', 'Gyi'),
        ('Gyi', 'Gyi', 'Giz', 'Gcnot', 'Giz'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gxi'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gxi', 'Gzi'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gyi', 'Gzi'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gix'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gix', 'Giz'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Giy', 'Giz'),
        ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'),
        ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'),
        ('Gii', 'Gyi', 'Giy', 'Gyi', 'Gcnot', 'Gxi'),
        ('Gxi', 'Giy', 'Giy', 'Gyi', 'Giy', 'Gcnot'),
        ('Gyi', 'Gxi', 'Giy', 'Gyi', 'Gcnot', 'Gyi'),
        ('Gix', 'Gyi', 'Giy', 'Giy', 'Gxi', 'Gxi'),
        ('Gcnot', 'Gii', 'Gxi', 'Gyi', 'Gyi', 'Giy'),
        ('Gcnot', 'Gii', 'Gxi', 'Gcnot', 'Gix', 'Gxi'),
        ('Gyi', 'Gix', 'Gxi', 'Gix', 'Giy', 'Giy'),
        ('Gix', 'Giy', 'Giy', 'Giy', 'Giy', 'Gcnot'),
        ('Gyi', 'Gcnot', 'Gii', 'Gcnot', 'Gix', 'Giy'),
        ('Gii', 'Gzi', 'Giz', 'Gyi', 'Gcnot', 'Gxi'),
        ('Gzi', 'Gxi', 'Giz', 'Gzi', 'Gcnot', 'Gyi'),
        ('Gcnot', 'Gcnot', 'Gcnot', 'Gxi', 'Gix', 'Gii', 'Giy'),
        ('Gii', 'Gyi', 'Gxi', 'Gcnot', 'Gcnot', 'Gix', 'Gcnot'),
        ('Giy', 'Gxi', 'Gyi', 'Gxi', 'Gcnot', 'Gyi', 'Gix'),
        ('Gxi', 'Gyi', 'Gyi', 'Gcnot', 'Gix', 'Gix', 'Giy'),
        ('Gxi', 'Giy', 'Gix', 'Gcnot', 'Giy', 'Gix', 'Gii'),
        ('Gix', 'Giy', 'Gix', 'Gyi', 'Gxi', 'Gii', 'Gxi'),
        ('Gii', 'Gii', 'Gxi', 'Gcnot', 'Gii', 'Giy', 'Gcnot'),
        ('Giy', 'Gix', 'Gxi', 'Gix', 'Gii', 'Gxi', 'Gii'),
        ('Giy', 'Giy', 'Gix', 'Gii', 'Gix', 'Gxi', 'Gxi'),
        ('Giy', 'Gxi', 'Giy', 'Gxi', 'Gxi', 'Gyi', 'Gyi'),
        ('Gzi', 'Gii', 'Giz', 'Gzi', 'Gcnot', 'Gxi', 'Gii'),
        ('Gzi', 'Gcnot', 'Gzi', 'Gxi', 'Gix', 'Gii', 'Giz'),
        ('Gxi', 'Giy', 'Gix', 'Gcnot', 'Gii', 'Gyi', 'Gyi', 'Giy'),
        ('Gcnot', 'Gix', 'Gix', 'Gcnot', 'Gcnot', 'Gyi', 'Giy', 'Giy'),
        ('Gxi', 'Gix', 'Gcnot', 'Gix', 'Gxi', 'Giy', 'Gyi', 'Giy'),
        ('Giy', 'Gcnot', 'Gxi', 'Gcnot', 'Gix', 'Gxi', 'Gxi', 'Gyi'),
        ('Gxi', 'Gcnot', 'Gix', 'Giy', 'Gyi', 'Gyi', 'Gyi', 'Gcnot'),
        ('Gxi', 'Giy', 'Giy', 'Giy', 'Gcnot', 'Gix', 'Gyi', 'Gyi'),
        ('Gix', 'Gix', 'Gix', 'Gyi', 'Giy', 'Gxi', 'Giy', 'Giy'),
        ('Gcnot', 'Gyi', 'Gxi', 'Gyi', 'Giy', 'Gyi', 'Gyi', 'Giy'),
        ('Gii', 'Gzi', 'Gzi', 'Giz', 'Gii', 'Gzi', 'Gyi', 'Gcnot'),
        ('Gxi', 'Giz', 'Giz', 'Giz', 'Gzi', 'Gix', 'Gyi', 'Gyi'),
        ('Gcnot', 'Gyi', 'Gxi', 'Gyi', 'Giz', 'Gyi', 'Gzi', 'Giz') 
        ])

#Construct the target gateset
gs_target = _setc.build_gateset(
    [4], [('Q0','Q1')],['Gii', 'Gix','Giy','Giz','Gxi','Gyi','Gzi','Gcnot'],
    [  "I(Q0):I(Q1)", "I(Q0):X(pi/2,Q1)", "I(Q0):Y(pi/2,Q1)", "I(Q0):Z(pi/2,Q1)",
       "X(pi/2,Q0):I(Q1)", "Y(pi/2,Q0):I(Q1)", "Z(pi/2,Q0):I(Q1)", "CNOT(Q0,Q1)"],
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
