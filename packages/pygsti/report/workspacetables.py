from __future__ import division, print_function, absolute_import, unicode_literals
#*****************************************************************
#    pyGSTi 0.9:  Copyright 2015 Sandia Corporation
#    This Software is released under the GPL license detailed
#    in the file "license.txt" in the top-level pyGSTi directory
#*****************************************************************
""" Classes corresponding to tables within a Workspace context."""

import warnings           as _warnings
import numpy              as _np
import scipy.stats        as _stats
import scipy.linalg       as _spl

from .. import algorithms as _alg
from .. import tools      as _tools
from .. import objects    as _objs
from . import reportables as _reportables

from .table import ReportTable as _ReportTable

from .workspace import WorkspaceTable
from . import workspaceplots as _wp

class BlankTable(WorkspaceTable):
    def __init__(self, ws):
        """A completely blank placeholder table."""
        super(BlankTable,self).__init__(ws, self._create)

    def _create(self):
        table = _ReportTable(['Blank'], [None])
        table.finish()
        return table

    
class SpamTable(WorkspaceTable):
    def __init__(self, ws, gatesets, titles=None, confidenceRegionInfo=None,
                 includeHSVec=True):
        """
        A table of one or more gateset's SPAM elements.
    
        Parameters
        ----------
        gatesets : GateSet or list of GateSets
            The GateSet(s) whose SPAM elements should be displayed. If
            multiple GateSets are given, they should have the same gates.

    
        titles : list of strs, optional
            Titles correponding to elements of `gatesets`, e.g. `"Target"`.
    
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals.
    
        includeHSVec : boolean, optional
            Whether or not to include Hilbert-Schmidt
            vector representation columns in the table.    
        """
        super(SpamTable,self).__init__(ws, self._create, gatesets,
                                       titles, confidenceRegionInfo,
                                       includeHSVec)

    def _create(self, gatesets, titles, confidenceRegionInfo, includeHSVec):
        if isinstance(gatesets, _objs.GateSet):
            gatesets = [gatesets]

        rhoLabels = list(gatesets[0].preps.keys()) #use labels of 1st gateset
        ELabels = list(gatesets[0].effects.keys()) #use labels of 1st gateset
            
        if titles is None:
            titles = ['']*len(gatesets)

        colHeadings = ['Operator']
        for gateset,title in zip(gatesets,titles):
            colHeadings.append( '%sMatrix' % (title+' ' if title else '') )
        for gateset,title in zip(gatesets,titles):
            colHeadings.append( '%sEigenvals' % (title+' ' if title else '') )

        formatters = [None]*len(colHeadings)

        if includeHSVec:
            gateset = gatesets[-1] #only show HSVec for last gateset
            #mxBasis    = gateset.basis.name
            mxBasis = gateset.basis.name
            mxBasisDim = gateset.basis.dim.blockDims
            #mxBasisDim = gateset.basis.dim.blockDims
            basisNm    = _objs.basis_longname(mxBasis)
            colHeadings.append( 'Hilbert-Schmidt vector (%s basis)' % basisNm )
            formatters.append( None )
            
            if confidenceRegionInfo is not None:
                colHeadings.append('%g%% C.I. half-width' % confidenceRegionInfo.level)
                formatters.append( 'Conversion' )

                
        table = _ReportTable(colHeadings, formatters, confidenceRegionInfo=confidenceRegionInfo)
    
        for lbl in rhoLabels:
            rowData = [lbl]; rowFormatters = ['Rho']

            for gateset in gatesets:
                # basisNm = gateset.basis.name
                # TEMPORARY: TO USE DEPRECATED RIGETTI DATA FOR REPORT
                basisNm = gateset.basis.name
                rhoMx = _tools.vec_to_stdmx(gateset.preps[lbl], basisNm)            
                rowData.append( rhoMx )
                rowFormatters.append('Brackets')

            for gateset in gatesets:
                basisNm = gateset.basis.name
                #basisNm = gateset.basis.name
                rhoMx = _tools.vec_to_stdmx(gateset.preps[lbl], basisNm)
                evals = _np.linalg.eigvals(rhoMx)
                rowData.append( evals )
                rowFormatters.append('Brackets')

                
            if includeHSVec:
                rowData.append( gatesets[-1].preps[lbl] )
                rowFormatters.append('Normal')
    
                if confidenceRegionInfo is not None:
                    intervalVec = confidenceRegionInfo.get_profile_likelihood_confidence_intervals(lbl)[:,None]
                    if intervalVec.shape[0] == gatesets[-1].get_dimension()-1:
                        #TP constrained, so pad with zero top row
                        intervalVec = _np.concatenate( (_np.zeros((1,1),'d'),intervalVec), axis=0 )
                    rowData.append( intervalVec ); rowFormatters.append('Normal')
    
            #Note: no dependence on confidence region (yet) when HS vector is not shown...
            table.addrow(rowData, rowFormatters)


        for lbl in ELabels:
            rowData = [lbl]; rowFormatters = ['Effect']

            for gateset in gatesets:
                #basisNm = gateset.basis.name
                basisNm = gateset.basis.name
                EMx = _tools.vec_to_stdmx(gateset.effects[lbl], basisNm)
                rowData.append( EMx )
                rowFormatters.append('Brackets')

            for gateset in gatesets:
                #basisNm = gateset.basis.name
                basisNm = gateset.basis.name
                EMx = _tools.vec_to_stdmx(gateset.effects[lbl], basisNm)
                evals = _np.linalg.eigvals(EMx)
                rowData.append( evals )
                rowFormatters.append('Brackets')
    
            if includeHSVec:
                rowData.append( gatesets[-1].effects[lbl] )
                rowFormatters.append('Normal')
    
                if confidenceRegionInfo is not None:
                    intervalVec = confidenceRegionInfo.get_profile_likelihood_confidence_intervals(lbl)[:,None]
                    rowData.append( intervalVec ); rowFormatters.append('Normal')
    
            #Note: no dependence on confidence region (yet) when HS vector is not shown...
            table.addrow(rowData, rowFormatters)
    
        table.finish()
        return table



#def get_gateset_spam_parameters_table(gateset, confidenceRegionInfo=None):
class SpamParametersTable(WorkspaceTable):
    def __init__(self, ws, gateset, confidenceRegionInfo=None):
        """
        Create a table for gateset's "SPAM parameters", that is, the
        dot products of prep-vectors and effect-vectors.
    
        Parameters
        ----------
        gateset : GateSet
            The GateSet
    
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals.
    
        Returns
        -------
        ReportTable
        """
        super(SpamParametersTable,self).__init__(ws, self._create, gateset, confidenceRegionInfo)

    def _create(self, gateset, confidenceRegionInfo):
        colHeadings = [''] + list(gateset.get_effect_labels())
        formatters  = [None] + [ 'Effect' ]*len(gateset.get_effect_labels())
    
        table       = _ReportTable(colHeadings, formatters, confidenceRegionInfo=confidenceRegionInfo)
    
        #spamDotProdsQty = _reportables.compute _gateset_qty("Spam DotProds", gateset, confidenceRegionInfo)
        spamDotProdsQty = _reportables.spam_dotprods(gateset, confidenceRegionInfo)
        DPs, DPEBs      = spamDotProdsQty.get_value_and_err_bar()
    
        formatters      = [ 'Rho' ] + [ 'Normal' ]*len(gateset.get_effect_labels()) #for rows below
    
        for ii,prepLabel in enumerate(gateset.get_prep_labels()): # ii enumerates rhoLabels to index DPs
            rowData = [prepLabel]
            for jj,_ in enumerate(gateset.get_effect_labels()): # jj enumerates eLabels to index DPs
                if confidenceRegionInfo is None:
                    rowData.append((DPs[ii,jj],None))
                else:
                    rowData.append((DPs[ii,jj],DPEBs[ii,jj]))
            table.addrow(rowData, formatters)
    
        table.finish()
        return table
    
    
#def get_gateset_gates_table(gateset, confidenceRegionInfo=None):
class GatesTable(WorkspaceTable):
    def __init__(self, ws, gatesets, titles=None, display_as="boxes",
                 confidenceRegionInfo=None):
        """
        Create a table showing a gateset's raw gates.
    
        Parameters
        ----------
        gatesets : GateSet or list of GateSets
            The GateSet(s) whose gates should be displayed.  If multiple
            GateSets are given, they should have the same gate labels.

        titles : list of strings, optional
            A list of titles corresponding to the gate sets, used to 
            prefix the column(s) for that gate set. E.g. `"Target"`.
    
        display_as : {"numbers", "boxes"}, optional
            How to display the gate matrices, as either numerical
            grids (fine for small matrices) or as a plot of colored
            boxes (space-conserving and better for large matrices).

        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals for the *final*
            element of `gatesets`.
    
        Returns
        -------
        ReportTable
        """
        super(GatesTable,self).__init__(ws, self._create, gatesets, titles,
                                        display_as, confidenceRegionInfo)

        
    def _create(self, gatesets, titles, display_as, confidenceRegionInfo):

        if isinstance(gatesets, _objs.GateSet):
            gatesets = [gatesets]

        gateLabels = list(gatesets[0].gates.keys()) #use labels of 1st gateset

        if titles is None:
            titles = ['']*len(gatesets)

        colHeadings = ['Gate']
        for gateset,title in zip(gatesets,titles):
            #basisNm = gateset.basis.name
            basisNm = gateset.basis.name
            #basisDims = gateset.basis.dim.blockDims
            basisDims = gateset.basis.dim.blockDims
            basisLongNm = _objs.basis_longname(basisNm)
            pre = (title+' ' if title else '')
            colHeadings.append('%sSuperoperator (%s basis)' % (pre,basisLongNm))
        formatters = [None]*len(colHeadings)

        if confidenceRegionInfo is not None:
            #Only use confidence region for the *final* gateset.
            colHeadings.append('%g%% C.I. half-width' % confidenceRegionInfo.level)
            formatters.append('Conversion')
    
        table = _ReportTable(colHeadings, formatters, confidenceRegionInfo=confidenceRegionInfo)

        for gl in gateLabels:
            #Note: currently, we don't use confidence region...
            row_data = [gl]
            row_formatters = [None]
    
            for gateset in gatesets:
                #basisNm = gateset.basis.name
                basisNm = gateset.basis.name
                #basisDims = gateset.basis.dim.blockDims
                basisDims = gateset.basis.dim.blockDims

                if display_as == "numbers":
                    row_data.append(gateset.gates[gl])
                    row_formatters.append('Brackets')
                elif display_as == "boxes":
                    fig = _wp.GateMatrixPlot(self.ws, gateset.gates[gl],
                                             colorbar=False,
                                             mxBasis=basisNm,
                                             mxBasisDims=basisDims)
                    row_data.append( fig )
                    row_formatters.append('Figure')
                else:
                    raise ValueError("Invalid 'display_as' argument: %s" % display_as)

            if confidenceRegionInfo is not None:
                intervalVec = confidenceRegionInfo.get_profile_likelihood_confidence_intervals(gl)[:,None]
                if isinstance(gatesets[-1].gates[gl], _objs.FullyParameterizedGate):
                    #then we know how to reshape into a matrix
                    gate_dim   = gatesets[-1].get_dimension()
                    basisNm = gatesets[-1].basis.name
                    basisDims = gatesets[-1].basis.dim.blockDims
                    intervalMx = intervalVec.reshape(gate_dim,gate_dim)
                elif isinstance(gatesets[-1].gates[gl], _objs.TPParameterizedGate):
                    #then we know how to reshape into a matrix
                    gate_dim   = gatesets[-1].get_dimension()
                    basisNm = gatesets[-1].basis.name
                    basisDims = gatesets[-1].basis.dim.blockDims
                    intervalMx = _np.concatenate( ( _np.zeros((1,gate_dim),'d'),
                                                    intervalVec.reshape(gate_dim-1,gate_dim)), axis=0 )
                else:
                    # we don't know how best to reshape
                    # vector of parameter intervals, so just don't unless needed for boxes
                    intervalMx = intervalVec.reshape(len(intervalVec),1) #col of boxes
                    basisNm = basisDims = None #we don't know how to label the params

                if display_as == "numbers":
                    row_data.append(intervalMx)
                    row_formatters.append('Brackets')
                    
                elif display_as == "boxes":
                    fig = _wp.GateMatrixPlot(self.ws, intervalMx,
                                             colorbar=False,
                                             mxBasis=basisNm,
                                             mxBasisDims=basisDims)
                    row_data.append( fig )
                    row_formatters.append('Figure')
                else:
                    assert(False)
                
            table.addrow(row_data, row_formatters)
    
        table.finish()
        return table
        
    
#    def get_gateset_choi_table(gateset, confidenceRegionInfo=None):
class ChoiTable(WorkspaceTable):
    def __init__(self, ws, gatesets, titles=None,
                 confidenceRegionInfo=None,
                 display=("matrix","eigenvalues","barplot")):
        """
        Create a table of the Choi matrices and/or their eigenvalues of
        a gateset's gates.
    
        Parameters
        ----------
        gatesets : GateSet or list of GateSets
            The GateSet(s) whose Choi info should be displayed.  If multiple
            GateSets are given, they should have the same gate labels.

        titles : list of strings, optional
            A list of titles corresponding to the gate sets, used to 
            prefix the column(s) for that gate set. E.g. `"Target"`.
    
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display eigenvalue error intervals for the
            *final* GateSet in `gatesets`.

        display : tuple or list of {"matrices","eigenvalues","barplot"}
            Which columns to display: the Choi matrices (as numerical grids),
            the Choi matrix eigenvalues (as a numerical list), and/or the
            eigenvalues on a bar plot.

    
        Returns
        -------
        ReportTable
        """
        super(ChoiTable,self).__init__(ws, self._create, gatesets, titles,
                                       confidenceRegionInfo, display)

        
    def _create(self, gatesets, titles, confidenceRegionInfo, display):
        if isinstance(gatesets, _objs.GateSet):
            gatesets = [gatesets]

        gateLabels = list(gatesets[0].gates.keys()) #use labels of 1st gateset

        if titles is None:
            titles = ['']*len(gatesets)
        
        qtysList = []
        for gateset in gatesets:
            gateLabels = list(gateset.gates.keys()) # gate labels
            #qtys_to_compute = []
            if 'matrix' in display:
                choiMxs = [_reportables.choi_matrix(gateset, gl) for gl in gateLabels]
            else:
                choiMxs = None
            if 'eigenvalues' in display or 'barplot' in display:
                evals   = [_reportables.choi_evals(gateset, gl) for gl in gateLabels]
            else:
                evals = None
            qtysList.append((choiMxs, evals))
        colHeadings = ['Gate']
        for disp in display:
            if disp == "matrix":
                for gateset,title in zip(gatesets,titles):
                    basisNm = gateset.basis.name
                    basisDims = gateset.basis.dim.blockDims
                    basisLongNm = _objs.basis_longname(basisNm)
                    pre = (title+' ' if title else '')
                    colHeadings.append('%sChoi matrix (%s basis)' % (pre,basisLongNm))
            elif disp == "eigenvalues":
                for gateset,title in zip(gatesets,titles):
                    pre = (title+' ' if title else '')
                    colHeadings.append('%sEigenvalues' % pre)
            elif disp == "barplot":
                for gateset,title in zip(gatesets,titles):
                    pre = (title+' ' if title else '')
                    colHeadings.append('%sEigenvalue Magnitudes' % pre)
            else:
                raise ValueError("Invalid element of `display`: %s" % disp)                    
        formatters = [None]*len(colHeadings)

        
        table = _ReportTable(colHeadings, formatters, confidenceRegionInfo=confidenceRegionInfo)

        for i, gl in enumerate(gateLabels):
            #Note: currently, we don't use confidence region...
            row_data = [gl]
            row_formatters = [None]

            for disp in display:
                if disp == "matrix":
                    for gateset, (choiMxs, _) in zip(gatesets, qtysList):
                        choiMx, _ = choiMxs[i].get_value_and_err_bar()
                        row_data.append(choiMx)
                        row_formatters.append('Brackets')
        
                elif disp == "eigenvalues":
                    for gateset, (_, evals) in zip(gatesets, qtysList):
                        evals, evalsEB = evals[i].get_value_and_err_bar()
                        try:
                            evals = evals.reshape(evals.size//4, 4)
                              #assumes len(evals) is multiple of 4!
                        except: # if it isn't try 3 (qutrits)
                            evals = evals.reshape(evals.size//3, 3)
                              #assumes len(evals) is multiple of 3!

                        if confidenceRegionInfo is None:
                            row_data.append(evals)
                            row_formatters.append('Normal')
                        else:
                            try:    evalsEB = evalsEB.reshape(evalsEB.size//4, 4)
                            except: evalsEB = evalsEB.reshape(evalsEB.size//3, 3)
                            row_data.append( (evals,evalsEB) )
                            row_formatters.append('Vec')
                            
                elif disp == "barplot":
                    for gateset in gatesets:
                        for gateset, (_, evals) in zip(gatesets,qtysList):
                            evals, evalsEB = evals[i].get_value_and_err_bar()
                            fig = _wp.ChoiEigenvalueBarPlot(self.ws, evals, evalsEB)
                            row_data.append(fig)
                            row_formatters.append('Figure')
            table.addrow(row_data, row_formatters)
        table.finish()
        return table
    
    
#    def get_gates_vs_target_table(gateset, targetGateset, confidenceRegionInfo=None):
class GatesVsTargetTable(WorkspaceTable):
    def __init__(self, ws, gateset, targetGateset, confidenceRegionInfo=None):
        """
        Create a table comparing a gateset's gates to a target gateset using
        the infidelity, diamond-norm distance, and trace distance.
    
        Parameters
        ----------
        gateset, targetGateset : GateSet
            The gate sets to compare
    
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals.    
    
        Returns
        -------
        ReportTable
        """
        super(GatesVsTargetTable,self).__init__(ws, self._create, gateset,
                                                targetGateset, confidenceRegionInfo)
    
    def _create(self, gateset, targetGateset, confidenceRegionInfo):
    
        gateLabels  = list(gateset.gates.keys())  # gate labels
    
        colHeadings = ('Gate', "Process|Infidelity", "1/2 Trace|Distance", "1/2 Diamond-Norm") #, "Frobenius|Distance"
        formatters  = (None,'Conversion','Conversion','Conversion') # ,'Conversion'
    
        infidelities = [_reportables.process_infidelity(gateset, targetGateset, gl, confidenceRegionInfo) for gl in gateLabels]
        jt_diffs     = [_reportables.jt_diff(gateset, targetGateset, gl, confidenceRegionInfo)            for gl in gateLabels]
        dnorms       = [_reportables.half_diamond_norm(gateset, targetGateset, gl, confidenceRegionInfo)  for gl in gateLabels]

        table = _ReportTable(colHeadings, formatters, colHeadingLabels=colHeadings, confidenceRegionInfo=confidenceRegionInfo)
    
        formatters = [None] + [ 'Normal' ] * (len(colHeadings) - 1)
    
        for rowData in _reportables.labeled_data_rows(gateLabels, confidenceRegionInfo,
                                                      infidelities, jt_diffs, dnorms):
            table.addrow(rowData, formatters)
        table.finish()
        return table
        
    
#    def get_spam_vs_target_table(gateset, targetGateset, confidenceRegionInfo=None):
class SpamVsTargetTable(WorkspaceTable):
    def __init__(self, ws, gateset, targetGateset, confidenceRegionInfo=None):
        """
        Create a table comparing a gateset's SPAM operations to a target gateset
        using state infidelity and trace distance.
    
        Parameters
        ----------
        gateset, targetGateset : GateSet
            The gate sets to compare
    
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals.
    
        Returns
        -------
        ReportTable
        """
        super(SpamVsTargetTable,self).__init__(ws, self._create, gateset,
                                               targetGateset, confidenceRegionInfo)
    
    def _create(self, gateset, targetGateset, confidenceRegionInfo):
    
        prepLabels   = gateset.get_prep_labels()
        effectLabels = gateset.get_effect_labels()
    
        colHeadings  = ('Prep/POVM', "State|Infidelity", "1/2 Trace|Distance")
        formatters   = (None,'Conversion','Conversion')
    
        table = _ReportTable(colHeadings, formatters, confidenceRegionInfo=confidenceRegionInfo)
    
        formatters = [ 'Rho' ] + [ 'Normal' ] * (len(colHeadings) - 1)
        prepInfidelities = [_reportables.vec_infidelity(gateset, targetGateset, l, 
                                                        'prep', confidenceRegionInfo)
                            for l in prepLabels]
        prepTraceDists   = [_reportables.vec_tr_diff(gateset, targetGateset, l, 
                                                        'prep', confidenceRegionInfo)
                            for l in prepLabels]
        for rowData in _reportables.labeled_data_rows(prepLabels, confidenceRegionInfo,
                                                      prepInfidelities, prepTraceDists):
            table.addrow(rowData, formatters)
    
        formatters = [ 'Effect' ] + [ 'Normal' ] * (len(colHeadings) - 1)
        effectInfidelities = [_reportables.vec_infidelity(gateset, targetGateset, l, 
                                                        'effect', confidenceRegionInfo)
                            for l in effectLabels]
        effectTraceDists   = [_reportables.vec_tr_diff(gateset, targetGateset, l, 
                                                        'effect', confidenceRegionInfo)
                            for l in effectLabels]
        for rowData in _reportables.labeled_data_rows(effectLabels, confidenceRegionInfo, 
                                                      effectInfidelities, effectTraceDists):
            table.addrow(rowData, formatters)
    
        table.finish()
        return table
    
    

#    def get_gates_vs_target_err_gen_table(gateset, targetGateset, confidenceRegionInfo=None, genType="logG-logT"):
class ErrgenTable(WorkspaceTable):
    def __init__(self, ws, gateset, targetGateset, confidenceRegionInfo=None,
                 display=("errgen","H","S"), display_as="boxes",
                 genType="logTiG"):
                 
        """
        Create a table listing the error generators obtained by
        comparing a gateset's gates to a target gateset.
    
        Parameters
        ----------
        gateset, targetGateset : GateSet
            The gate sets to compare

        display : tuple of {"errgen","H","S"}
            Specifes which columns to include: the error generator itself,
            the projections of the generator onto Hamiltoian-type error
            generators, and/or the projections onto Stochastic-type errors.

        display_as : {"numbers", "boxes"}, optional
            How to display the requested matrices, as either numerical
            grids (fine for small matrices) or as a plot of colored boxes
            (space-conserving and better for large matrices).
    
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals.
    
        genType : {"logG-logT", "logTiG"}
            The type of error generator to compute.  Allowed values are:
            
            - "logG-logT" : errgen = log(gate) - log(target_gate)
            - "logTiG" : errgen = log( dot(inv(target_gate), gate) )
        
        Returns
        -------
        ReportTable
        """
        super(ErrgenTable,self).__init__(ws, self._create, gateset,
                                         targetGateset, confidenceRegionInfo,
                                         display, display_as, genType)
    
    def _create(self, gateset, targetGateset, 
                confidenceRegionInfo, display, display_as, genType):
    
        gateLabels  = list(gateset.gates.keys())  # gate labels
        basisNm = gateset.basis.name
        #basisNm = gateset.basis.name
        #basisDims = gateset.basis.dim.blockDims
        basisDims = gateset.basis.dim.blockDims
        colHeadings = ['Gate']

        for disp in display:
            if disp == "errgen":
                colHeadings.append('Error Generator')
            elif disp == "H":
                colHeadings.append('Hamiltonian Projections')
            elif disp == "S":
                colHeadings.append('Stochastic Projections')
            else: raise ValueError("Invalid display element: %s" % disp)

        assert(display_as == "boxes" or display_as == "numbers")
        table = _ReportTable(colHeadings, (None,)*len(colHeadings) , confidenceRegionInfo=confidenceRegionInfo)

        errgens = {'M': []}
        hamProjs = {'M': []}
        stoProjs = {'M': []}

        def getMinMax(max_lst, M):
            #return a [min,max] already in list if there's one within an order of magnitude
            for mx in max_lst:
                if (abs(M) >= 1e-6 and 0.9999 < mx/M < 10) or (abs(mx)<1e-6 and abs(M)<1e-6):
                    return -mx,mx
            return None
                
        def addMax(max_lst, M):
            if not getMinMax(max_lst,M):
                max_lst.append(M)
    
        #Do computation, so shared color scales can be computed
        for gl in gateLabels:
            gate = gateset.gates[gl]
            targetGate = targetGateset.gates[gl]

            errgens[gl] = _tools.error_generator(gate, targetGate,
                                                 targetGateset.basis, genType)
            absMax = _np.max(_np.abs(errgens[gl]))
            addMax(errgens['M'], absMax)

            if "H" in display:
                hamProjs[gl] = _tools.std_errgen_projections(
                    errgens[gl], "hamiltonian", basisNm, basisNm)
                absMax = _np.max(_np.abs(hamProjs[gl]))
                addMax(hamProjs['M'], absMax)

            if "S" in display:
                stoProjs[gl] = _tools.std_errgen_projections(
                    errgens[gl], "stochastic", basisNm, basisNm)
                absMax = _np.max(_np.abs(stoProjs[gl]))
                addMax(stoProjs['M'], absMax)
    
        #Do plotting
        for gl in gateLabels:
            row_data = [gl]
            row_formatters = [None]
            
            for disp in display:
                if disp == "errgen":
                    if display_as == "boxes":
                        m,M = getMinMax(errgens['M'],_np.max(_np.abs(errgens[gl])))
                        errgen_fig =  _wp.GateMatrixPlot(self.ws, errgens[gl], m,M,
                                                         basisNm,basisDims)
                        row_data.append(errgen_fig)
                        row_formatters.append('Figure')
                    else:
                        row_data.append(errgens[gl])
                        row_formatters.append('Brackets')

                elif disp == "H":
                    if display_as == "boxes":
                        m,M = getMinMax(hamProjs['M'],_np.max(_np.abs(hamProjs[gl])))
                        hamdecomp_fig = _wp.ProjectionsBoxPlot(
                            self.ws, hamProjs[gl], basisNm, m, M, boxLabels=True)
                        row_data.append(hamdecomp_fig)
                        row_formatters.append('Figure')
                    else:
                        row_data.append(hamProjs[gl])
                        row_formatters.append('Brackets')


                elif disp == "S":
                    if display_as == "boxes":
                        m,M = getMinMax(stoProjs['M'],_np.max(_np.abs(stoProjs[gl])))
                        stodecomp_fig = _wp.ProjectionsBoxPlot(
                            self.ws, stoProjs[gl], basisNm, m, M, boxLabels=True)
                        row_data.append(stodecomp_fig)
                        row_formatters.append('Figure')
                    else:
                        row_data.append(stoProjs[gl])
                        row_formatters.append('Brackets')

            table.addrow(row_data, row_formatters)
    
        table.finish()
        return table
    
    
    
#    def get_gates_vs_target_angles_table(gateset, targetGateset, confidenceRegionInfo=None):
class old_RotationAxisVsTargetTable(WorkspaceTable):
    def __init__(self, ws, gateset, targetGateset, confidenceRegionInfo=None):
        """
        Create a table comparing the rotation axes of the single-qubit gates in
        `gateset` with those in `targetGateset`.  Differences are shown as
        angles between the rotation axes of corresponding gates.
    
        Parameters
        ----------
        gateset, targetGateset : GateSet
            The gate sets to compare.  Must be single-qubit.
    
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals.
    
        Returns
        -------
        ReportTable
        """
        super(RotationAxisVsTargetTable,self).__init__(
            ws, self._create, gateset, targetGateset, confidenceRegionInfo)

        
    def _create(self, gateset, targetGateset, confidenceRegionInfo):
    
        gateLabels  = list(gateset.gates.keys())  # gate labels
    
        colHeadings = ('Gate', "Angle between|rotation axes")
        formatters  = (None,'Conversion')
    
        anglesList = [_reportables.gateset_gateset_angles_btwn_axes(gateset, targetGateset, gl, confidenceRegionInfo) for gl in gateLabels]

        table = _ReportTable(colHeadings, formatters, confidenceRegionInfo=confidenceRegionInfo)
    
        formatters = [None] + ['Pi']
    
        for gl, angle in zip(gateLabels, anglesList):
            rowData = [gl] + [angle]
            table.addrow(rowData, formatters)
    
        table.finish()
        return table
        
    
#    def get_gateset_decomp_table(gateset, confidenceRegionInfo=None):
class GateDecompTable(WorkspaceTable):
    def __init__(self, ws, gateset, targetGateset, confidenceRegionInfo=None):
        """
        Create table for decomposing a gateset's gates.

        This table interprets the Hamiltonian projection of the log
        of the gate matrix to extract a rotation angle and axis.

        Parameters
        ----------
        gateset : GateSet
            The estimated gate set.

        targetGateset : GateSet
            The target gate set, used to help disambiguate the matrix
            logarithms that are used in the decomposition.
    
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals.
    
        Returns
        -------
        ReportTable
        """
        super(GateDecompTable,self).__init__(ws, self._create, gateset,
                                             targetGateset, confidenceRegionInfo)

        
    def _create(self, gateset, targetGateset, confidenceRegionInfo):
        gateLabels = list(gateset.gates.keys())  # gate labels
        basisNm   = gateset.basis.name
        basisDims = gateset.basis.dim.blockDims

        colHeadings = ('Gate','Ham. Evals.','Rotn. angle','Rotn. axis','Log Error') + tuple( [ "Axis angle w/%s" % gl for gl in gateLabels] )
        formatters = [None]*len(colHeadings)

        table = _ReportTable(colHeadings, formatters, 
                             colHeadingLabels=colHeadings, confidenceRegionInfo=confidenceRegionInfo)
        formatters = (None, 'Pi','Pi', 'Normal', 'Normal') + ('Pi',)*len(gateLabels)

        axes = {}; angles = {}; inexact = {}; hamEvals = {}
        for gl in gateLabels:
            gate = gateset.gates[gl]
            target_logG = _tools.unitary_superoperator_matrix_log(targetGateset.gates[gl],targetGateset.basis)
            logG = _tools.approximate_matrix_log(gate, target_logG)
            inexact[gl] = _np.linalg.norm(_spl.expm(logG)-gate)
            
            hamProjs, hamGens = _tools.std_errgen_projections(
                logG, "hamiltonian", basisNm, basisNm, return_generators=True)
            norm = _np.linalg.norm(hamProjs)
            axes[gl] = hamProjs / norm if (norm > 1e-15) else hamProjs
            #angles[gl] = norm * (gateset.dim**0.25 / 2.0) / _np.pi
               # const factor to undo sqrt( sqrt(dim) ) basis normalization (at
               # least of Pauli products) and divide by 2# to be consistent with
               # convention:  rotn(theta) = exp(i theta/2 * PauliProduct ), with
               # theta in units of pi.

            angles[gl] = norm * (2.0/gateset.dim)**0.5 / _np.pi
               #Scratch...
               # 1Q dim=4 -> sqrt(2) / 2.0 = 1/sqrt(2) ^4= 1/4  ^2 = 1/2 = 2/dim
               # 2Q dim=16 -> 2.0 / 2.0 but need  1.0 / (2 sqrt(2)) ^4= 1/64 ^2= 1/8 = 2/dim
               # so formula that works for 1 & 2Q is sqrt(2/dim), perhaps
               # b/c convention is sigma-mxs in exponent, which are Pauli's/2.0 but our
               # normalized paulis are just /sqrt(2), so need to additionally divide by
               # sqrt(2)**nQubits == 2**(log2(dim)/4) == dim**0.25  ( nQubits = log2(dim)/2 )
               # and convention adds another sqrt(2)**nQubits / sqrt(2) => dim**0.5 / sqrt(2) (??)

            basis_mxs = gateset.basis.get_composite_matrices()
            scalings = [ ( _np.linalg.norm(hamGens[i]) / _np.linalg.norm(_tools.hamiltonian_to_lindbladian(mx))
                           if _np.linalg.norm(hamGens[i]) > 1e-10 else 0.0 )
                         for i,mx in enumerate(basis_mxs) ]
            hamMx = sum([s*c*bmx for s,c,bmx in zip(scalings,hamProjs,basis_mxs)])
            hamEvals[gl] = _np.linalg.eigvals(hamMx)

        for gl in gateLabels:            
            rowData = [gl, hamEvals[gl]/_np.pi, angles[gl], axes[gl], inexact[gl] ]

            for j,gl_other in enumerate(gateLabels):
                rotnAngle = angles[gl]
                rotnAngle_other = angles[gl_other]
    
                if gl_other == gl:
                    rowData.append( "" )
                elif abs(rotnAngle) < 1e-4 or abs(rotnAngle_other) < 1e-4:
                    rowData.append( "--" )
                else:
                    real_dot = _np.clip( _np.real(_np.dot(axes[gl].flatten(), axes[gl_other].flatten())), -1.0, 1.0)
                    angle = _np.arccos( real_dot ) / _np.pi
                    rowData.append( angle )

            table.addrow(rowData, formatters)
    
        table.finish()
        return table
    

class old_GateDecompTable(WorkspaceTable):
    def __init__(self, ws, gateset, confidenceRegionInfo=None):
        """
        Create table for decomposing a single-qubit gateset's gates.

        This table interprets the eigenvectors and eigenvalues of the
        gates to extract a rotation angle, axis, and various decay
        coefficients.
    
        Parameters
        ----------
        gateset : GateSet
            A single-qubit `GateSet`.
    
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals.
    
        Returns
        -------
        ReportTable
        """
        super(old_GateDecompTable,self).__init__(ws, self._create, gateset, confidenceRegionInfo)

        
    def _create(self, gateset, confidenceRegionInfo):

        gateLabels = list(gateset.gates.keys())  # gate labels
        colHeadings = ('Gate','Eigenvalues','Fixed pt','Rotn. axis','Diag. decay','Off-diag. decay')
        formatters = [None]*6
    
        decomps = [_reportables.decomposition(gateset, gl) for gl in gateLabels]
        decompNames = ('fixed point',
                       'axis of rotation',
                       'decay of diagonal rotation terms',
                       'decay of off diagonal rotation terms')

        table = _ReportTable(colHeadings, formatters, confidenceRegionInfo=confidenceRegionInfo)
    
        formatters = (None, 'Vec', 'Normal', 'Normal', 'Normal', 'Normal')

        for decomp, gl in zip(decomps, gateLabels):
            evals = _reportables.eigenvalues(gateset, gl)
            decomp, decompEB = decomp.get_value_and_err_bar()
    
            rowData = [gl, evals] + [decomp.get(x,'X') for x in decompNames[0:2] ] + \
                [(decomp.get(x,'X'),decompEB) for x in decompNames[2:4] ]
    
            table.addrow(rowData, formatters)
    
        table.finish()
        return table

    
#    def get_gateset_rotn_axis_table(gateset, confidenceRegionInfo=None, showAxisAngleErrBars=True):
class old_RotationAxisTable(WorkspaceTable):
    def __init__(self, ws, gateset, confidenceRegionInfo=None, showAxisAngleErrBars=True):
        """
        Create a table of the angle between a gate rotation axes for
        gates belonging to a single-qubit gateset.
    
        Parameters
        ----------
        gateset : GateSet
            A single-qubit `GateSet`.
    
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals.
    
        showAxisAngleErrBars : bool, optional
            Whether or not table should include error bars on the angles
            between rotation axes (doing so makes the table take up more
            space).
    
        Returns
        -------
        ReportTable
        """
        super(RotationAxisTable,self).__init__(ws, self._create, gateset, confidenceRegionInfo, showAxisAngleErrBars)

        
    def _create(self, gateset, confidenceRegionInfo, showAxisAngleErrBars):
    
        gateLabels = list(gateset.gates.keys())
    
        decomps = [_reportables.decomposition(gateset, gl) for gl in gateLabels]
    
        colHeadings = ("Gate","Angle") + tuple( [ "RAAW(%s)" % gl for gl in gateLabels] )
        nCols = len(colHeadings)
        formatters = [None] * nCols

        table = "tabular"
        latex_head =  "\\begin{%s}[l]{%s}\n\hline\n" % (table, "|c" * nCols + "|")
        latex_head += "\\multirow{2}{*}{Gate} & \\multirow{2}{*}{Angle} & " + \
                      "\\multicolumn{%d}{c|}{Angle between Rotation Axes} \\\\ \cline{3-%d}\n" % (len(gateLabels),nCols)
        latex_head += " & & %s \\\\ \hline\n" % (" & ".join(gateLabels))
    
        table = _ReportTable(colHeadings, formatters,
                             customHeader={'latex': latex_head}, confidenceRegionInfo=confidenceRegionInfo)
    
        formatters = [None, 'Pi'] + ['Pi'] * len(gateLabels)
    
        rotnAxisAngles, rotnAxisAnglesEB = _reportables.angles_btwn_rotn_axes(gateset, confidenceRegionInfo)
        rotnAngles = [ qtys['%s decomposition' % gl].get_value().get('pi rotations','X') \
                           for gl in gateLabels ]
    
        for i,gl in enumerate(gateLabels):
            decomp, decompEB = decomps[i].get_value_and_err_bar()
            rotnAngle = decomp.get('pi rotations','X')
    
            angles_btwn_rotn_axes = []
            for j,gl_other in enumerate(gateLabels):
                decomp_other, _ = decomps[j].get_value_and_err_bar()
                rotnAngle_other = decomp_other.get('pi rotations','X')
    
                if gl_other == gl:
                    angles_btwn_rotn_axes.append( ("",None) )
                elif str(rotnAngle) == 'X' or abs(rotnAngle) < 1e-4 or \
                     str(rotnAngle_other) == 'X' or abs(rotnAngle_other) < 1e-4:
                    angles_btwn_rotn_axes.append( ("--",None) )
                elif not _np.isnan(rotnAxisAngles[i,j]):
                    if showAxisAngleErrBars and rotnAxisAnglesEB is not None:
                        angles_btwn_rotn_axes.append( (rotnAxisAngles[i,j], rotnAxisAnglesEB[i,j]) )
                    else:
                        angles_btwn_rotn_axes.append( (rotnAxisAngles[i,j], None) )
                else:
                    angles_btwn_rotn_axes.append( ("X",None) )
    
            if confidenceRegionInfo is None or decompEB is None: #decompEB is None when gate decomp failed
                rowData = [gl, (rotnAngle,None)] + angles_btwn_rotn_axes
            else:
                rowData = [gl, (rotnAngle,decompEB.get('pi rotations','X'))] + angles_btwn_rotn_axes
            table.addrow(rowData, formatters)
    
        table.finish()
        return table
    
    
#    def get_gateset_eigenval_table(gateset, targetGateset, figFilePrefix, maxWidth=6.5, maxHeight=8.0,
#                                   confidenceRegionInfo=None):
class GateEigenvalueTable(WorkspaceTable):
    def __init__(self, ws, gateset, targetGateset=None,
                 confidenceRegionInfo=None,
                 display=('evals','rel','log-evals','log-rel','polar','relpolar') ):
        """
        Create table which lists and displays (using a polar plot)
        the eigenvalues of a gateset's gates.
    
        Parameters
        ----------
        gateset : GateSet
            The GateSet
    
        targetGateset : GateSet, optional
            The target gate set.  If given, the target's eigenvalue will
            be plotted alongside `gateset`'s gate eigenvalue, the
            "relative eigenvalues".
        
        confidenceRegionInfo : ConfidenceRegion, optional
            If not None, specifies a confidence-region
            used to display error intervals.

        display : tuple of {"evals", "rel", "log-evals", "log-rel", "polar", "relpolar"}
            Specifies which columns are displayed in the table: a list of the
            eigenvalues, a list of the relative eigenvalues, the (complex)
            logarithm of the eigenvalues and relative eigenvalues, a polar plot of
            the eigenvalues, and/or a polar plot of the relative eigenvalues.
            If `targetGateset` is None, then `"rel"`, `"log-rel"` and `"relpolar"`
            will be silently ignored.
    
        Returns
        -------
        ReportTable
        """
        super(GateEigenvalueTable,self).__init__(ws, self._create, gateset,
                                                 targetGateset,
                                                 confidenceRegionInfo, display)
        
    def _create(self, gateset, targetGateset,               
                confidenceRegionInfo, display):
        
        gateLabels = list(gateset.gates.keys())  # gate labels
        colHeadings = ['Gate']
        for disp in display:
            if disp == "evals":
                colHeadings.append('Eigenvalues')
            elif disp == "rel":
                if(targetGateset is not None): #silently ignore
                    colHeadings.append('Rel. Evals')
            elif disp == "log-evals":
                colHeadings.append('Real log(eval)')
                colHeadings.append('Imag log(eval)')
            elif disp == "log-rel":
                colHeadings.append('Real log(rel. eval)')
                colHeadings.append('Imag log(rel. eval)')
            elif disp == "polar":
                colHeadings.append('Eigenvalues')
            elif disp == "relpolar":
                if(targetGateset is not None): #silently ignore
                    colHeadings.append('Rel. Evals')
            else:
                raise ValueError("Invalid display element: %s" % disp)

        formatters = [None]*len(colHeadings)
    
        def format_evals(evals,evalsEB):
            evals = evals.reshape(evals.size, 1)
            if evalsEB is not None:
                evalsEB = evalsEB.reshape(evalsEB.size, 1)
            #OLD: format to 2-columns - but polar plots are big, so just stick to 1col now
            #try: evals = evals.reshape(evals.size//2, 2) #assumes len(evals) is even!
            #except: evals = evals.reshape(evals.size, 1)
            #if evalsEB is not None:
            #    try: evalsEB = evalsEB.reshape(evalsEB.size//2, 2)
            #    except: evalsEB = evalsEB.reshape(evalsEB.size, 1)
            return evals, evalsEB
    
        table = _ReportTable(colHeadings, formatters, confidenceRegionInfo=confidenceRegionInfo)
    
        for gl in gateLabels:
            row_data = [gl]
            row_formatters = [None]

            evals, evalsEB = _reportables.eigenvalues(gateset, gl).get_value_and_err_bar()
            #evals, evalsEB = qtys['%s eigenvalues' % gl].get_value_and_err_bar()

            if targetGateset is not None:
                gate = gateset.gates[gl]
                targetGate = targetGateset.gates[gl]
                target_evals = _np.linalg.eigvals(targetGate)
                rel_gate = _np.dot(_np.linalg.inv(targetGate), gate) #TODO: function for this?
                rel_evals = _np.linalg.eigvals(rel_gate)

            for disp in display:
                if disp == "evals":
                    evals,evalsEB = format_evals(evals,evalsEB)
                    row_data.append( (evals,evalsEB) )
                    row_formatters.append('Vec')

                elif disp == "rel" and targetGateset is not None:
                    rel_evals,_ = format_evals(rel_evals,None)
                    row_data.append( (rel_evals,None) )
                    row_formatters.append('Vec')

                elif disp == "log-evals":
                    evals,evalsEB = format_evals(evals,evalsEB)
                    if evalsEB is not None:
                        logevals, logevalsEB = _np.log(evals), _np.log(evalsEB)
                        row_data.append( (_np.real(logevals),_np.real(logevalsEB)) )
                        row_data.append( (_np.imag(logevals)/_np.pi,_np.imag(logevalsEB)/_np.pi) )
                        row_formatters.append('Vec')
                        row_formatters.append('Pi')
            
                    else:
                        logevals = _np.log(evals)
                        row_data.append( (_np.real(logevals),None) )
                        row_data.append( (_np.imag(logevals)/_np.pi,None) )
                        row_formatters.append('Vec') 
                        row_formatters.append('Pi')  


                elif disp == "log-rel":
                    rel_evals,_ = format_evals(rel_evals,None)
                    log_relevals = _np.log(rel_evals)
                    row_data.append( (_np.real(log_relevals),None) )
                    row_data.append( (_np.imag(log_relevals)/_np.pi,None) )
                    row_formatters.append('Vec') 
                    row_formatters.append('Pi')  

                    
                elif disp == "polar":
                    if targetGateset is None:
                        fig = _wp.PolarEigenvaluePlot(
                            self.ws,[evals],["blue"],centerText=gl)
                    else:
                        fig = _wp.PolarEigenvaluePlot(
                            self.ws,[target_evals,evals],
                            ["black","blue"],["target","gate"], centerText=gl)
                    row_data.append( fig )
                    row_formatters.append('Figure')

                elif disp == "relpolar" and targetGateset is not None:
                    fig = _wp.PolarEigenvaluePlot(
                        self.ws,[rel_evals],["red"],["rel"],centerText=gl)
                    row_data.append( fig )
                    row_formatters.append('Figure')
            table.addrow(row_data, row_formatters)
        table.finish()
        return table
    
        
    
#    def get_dataset_overview_table(dataset, target, maxlen=10, fixedLists=None,
#                                   maxLengthList=None):
class DataSetOverviewTable(WorkspaceTable):
    def __init__(self, ws, dataset, maxLengthList=None):
        """
        Create a table that gives a summary of the properties of `dataset`.
    
        Parameters
        ----------
        dataset : DataSet
            The DataSet
        
        maxLengthList : list of ints, optional
            A list of the maximum lengths used, if available.
    
        Returns
        -------
        ReportTable
        """
        super(DataSetOverviewTable,self).__init__(ws, self._create, dataset, maxLengthList)
    
    def _create(self, dataset, maxLengthList):
    
        colHeadings = ('Quantity','Value')
        formatters = (None,None)
    
        table = _ReportTable(colHeadings, formatters)
    
        minN = round(min([ row.total() for row in dataset.itervalues()]))
        maxN = round(max([ row.total() for row in dataset.itervalues()]))
        cntStr = "[%d,%d]" % (minN,maxN) if (minN != maxN) else "%d" % round(minN)
    
        table.addrow(("Number of strings", str(len(dataset))), (None,None))
        table.addrow(("Gate labels", ", ".join(dataset.get_gate_labels()) ), (None,None))
        table.addrow(("SPAM labels",  ", ".join(dataset.get_spam_labels()) ), (None,None))
        table.addrow(("Counts per string", cntStr  ), (None,None))

        if maxLengthList is not None:
            table.addrow(("Max. Lengths", ", ".join(map(str,maxLengthList)) ), (None,None))
        if hasattr(dataset,'comment') and dataset.comment is not None:
            commentLines = dataset.comment.split('\n')
            for i,commentLine in enumerate(commentLines,start=1):
                table.addrow(("User comment %d" % i, commentLine  ), (None,'Verbatim'))
    
        table.finish()
        return table
    
    
#    def get_chi2_progress_table(Ls, gatesetsByL, gateStringsByL, dataset,
#                                gateLabelAliases=None):
class FitComparisonTable(WorkspaceTable):
    def __init__(self, ws, Xs, gssByX, gatesetByX, dataset, objective="logl",
                 Xlabel='L', NpByX=None):
        """
        Create a table showing how the chi^2 or log-likelihood changed with
        successive GST iterations.
    
        Parameters
        ----------
        Xs : list of integers
            List of X-values. Typically these are the maximum lengths or
            exponents used to index the different iterations of GST.

        gssByX : list of LsGermsStructure
            Specifies the set (& structure) of the gate strings used at each X.

        gatesetByX : list of GateSets
            `GateSet`s corresponding to each X value.
    
        dataset : DataSet
            The data set to compare each gate set against.
    
        objective : {"logl", "chi2"}, optional
            Whether to use log-likelihood or chi^2 values.

        Xlabel : str, optional
            A label for the 'X' variable which indexes the different gate sets.
            This string will be the header of the first table column.

        NpByX : list of ints, optional
            A list of parameter counts to use for each X.  If None, then
            the number of non-gauge parameters for each gate set is used.
        
        
        Returns
        -------
        ReportTable
        """
        super(FitComparisonTable,self).__init__(ws, self._create, Xs, gssByX, gatesetByX,
                                                dataset, objective, Xlabel, NpByX)
    
    def _create(self, Xs, gssByX, gatesetByX, dataset, objective, Xlabel, NpByX):

        if objective == "chi2":
            colHeadings = {
                'latex': (Xlabel,'$\\chi^2$','$k$','$\\chi^2-k$','$\sqrt{2k}$',
                          '$N_\\sigma$','$N_s$','$N_p$', 'Rating'),
                'html': (Xlabel,'&chi;<sup>2</sup>','k','&chi;<sup>2</sup>-k',
                         '&radic;<span style="text-decoration:overline;">2k</span>',
                         'N<sub>sigma</sub>','N<sub>s</sub>','N<sub>p</sub>', 'Rating'),
                'text': (Xlabel,'chi^2','k','chi^2-k','sqrt{2k}','N_{sigma}','N_s','N_p', 'Rating')
                }
                
        elif objective == "logl":
            colHeadings = {
                'latex': (Xlabel,'$2\Delta\\log(\\mathcal{L})$','$k$','$2\Delta\\log(\\mathcal{L})-k$',
                          '$\sqrt{2k}$','$N_\\sigma$','$N_s$','$N_p$', 'Rating'),
                'html': (Xlabel,'2&Delta;(log L)','k','2&Delta;(log L)-k',
                         '&radic;<span style="text-decoration:overline;">2k</span>',
                         'N<sub>sigma</sub>','N<sub>s</sub>','N<sub>p</sub>', 'Rating'),
                'text': (Xlabel,'2*Delta(log L)','k','2*Delta(log L)-k','sqrt{2k}',
                                               'N_{sigma}','N_s','N_p', 'Rating')
                }
        else:
            raise ValueError("Invalid `objective` argument: %s" % objective)

        if NpByX is None:
            NpByX = [ gs.num_nongauge_params() for gs in gatesetByX ]

        table = _ReportTable(colHeadings, None)
        
        for X,gs,gss,Np in zip(Xs,gatesetByX,gssByX,NpByX):
            gstrs = gss.allstrs
            
            if objective == "chi2":
                fitQty = _tools.chi2( dataset, gs, gstrs,
                                    minProbClipForWeighting=1e-4,
                                    gateLabelAliases=gss.aliases )
            elif objective == "logl":
                logL_upperbound = _tools.logl_max(dataset, gstrs, gateLabelAliases=gss.aliases)
                logl = _tools.logl( gs, dataset, gstrs, gateLabelAliases=gss.aliases)
                fitQty = 2*(logL_upperbound - logl) # twoDeltaLogL
                if(logL_upperbound < logl):
                    raise ValueError("LogL upper bound = %g but logl = %g!!" % (logL_upperbound, logl))

            Ns = len(gstrs)*(len(dataset.get_spam_labels())-1) #number of independent parameters in dataset
            k = max(Ns-Np,0) #expected chi^2 or 2*(logL_ub-logl) mean
            Nsig = (fitQty-k)/_np.sqrt(2*k)
            #pv = 1.0 - _stats.chi2.cdf(chi2,k) # reject GST model if p-value < threshold (~0.05?)
    
            if   (fitQty-k) < _np.sqrt(2*k): rating = 5
            elif (fitQty-k) < 2*k: rating = 4
            elif (fitQty-k) < 5*k: rating = 3
            elif (fitQty-k) < 10*k: rating = 2
            else: rating = 1
            table.addrow(
                        (str(X),fitQty,k,fitQty-k,_np.sqrt(2*k),Nsig,Ns,Np,"<STAR>"*rating),
                        (None,'Normal','Normal','Normal','Normal','Rounded','Normal','Normal','Conversion'))
    
        table.finish()
        return table
        
    
#    def get_gatestring_multi_table(gsLists, titles, commonTitle=None):
class GatestringTable(WorkspaceTable):
    def __init__(self, ws, gsLists, titles, nCols=1, commonTitle=None):
        """
        Creates a table of enumerating one or more sets of gate strings.
    
        Parameters
        ----------
        gsLists : GateString list or list of GateString lists
            List(s) of gate strings to put in table.
    
        titles : string or list of strings
            The title(s) for the different string lists.  These are displayed in
            the relevant table columns containing the strings.

        nCols : int, optional
            The number of *data* columns, i.e. those containing
            gate strings, for each string list.
    
        commonTitle : string, optional
            A single title string to place in a cell spanning across
            all the other column headers.
    
        Returns
        -------
        ReportTable
        """
        super(GatestringTable,self).__init__(ws, self._create, gsLists, titles,
                                             nCols, commonTitle)

        
    def _create(self, gsLists, titles, nCols, commonTitle):

        if isinstance(gsLists[0], _objs.GateString) or \
           (isinstance(gsLists[0], tuple) and _tools.isstr(gsLists[0][0])):
            gsLists = [ gsLists ]

        if _tools.isstr(titles): titles = [ titles ]*len(gsLists)
            
        colHeadings = (('#',) + tuple(titles))*nCols
        formatters = (('Conversion',) + ('Normal',)*len(titles))*nCols
    
        if commonTitle is None:
            table = _ReportTable(colHeadings, formatters)
        else:
            table = "tabular"
            colHeadings = ('#',) + tuple(titles)
            latex_head  = "\\begin{%s}[l]{%s}\n\hline\n" % (table, "|c" * len(colHeadings) + "|")
            latex_head += " & \multicolumn{%d}{c|}{%s} \\\\ \hline\n" % (len(colHeadings)-1,commonTitle)
            latex_head += "%s \\\\ \hline\n" % (" & ".join(colHeadings))
    
            html_head = '<table class="%(tableclass)s" id="%(tableid)s" ><thead>'
            html_head += '<tr><th></th><th colspan="%d">%s</th></tr>\n' % (len(colHeadings)-1,commonTitle)
            html_head += "<tr><th> %s </th></tr>" % (" </th><th> ".join(colHeadings))
            html_head += "</thead><tbody>"
            table = _ReportTable(colHeadings, formatters,
                                 customHeader={'latex': latex_head,
                                               'html': html_head})
    
        formatters = (('Normal',) + ('GateString',)*len(gsLists))*nCols

        maxListLength = max(list(map(len,gsLists)))
        nRows = (maxListLength+(nCols-1)) // nCols #ceiling
    
        #for i in range( max([len(gsl) for gsl in gsLists]) ):
        for i in range(nRows):
            rowData = []
            for k in range(nCols):
                l = i+nRows*k #index of gatestring
                rowData.append( l+1 )
                for gsList in gsLists:
                    if l < len(gsList):
                        rowData.append( gsList[l] )
                    else:
                        rowData.append( None ) #empty string
            table.addrow(rowData, formatters)
    
        table.finish()
        return table
        
    
#    def get_projected_err_gen_comparison_table(gateset, targetGateset,
#                                               compare_with="target",
#                                               genType="logG-logT"):
class GatesSingleMetricTable(WorkspaceTable):
    def __init__(self, ws, gatesets, titles, targetGateset,
                 metric="infidelity"):
        """
        Create a table comparing the gates of various gate sets (`gatesets`) to
        those of `targetGateset` using the metric named by `metric`.
    
        Parameters
        ----------
        gatesets : list of GateSets
            The gate sets to compare with `targetGateset`

        titles : list of strs
            A list of titles used to describe each element of `gatesets`.

        targetGateset : GateSet
            The gate set to compare against.
    
        metric : {"infidelity","diamond","jtrace"}
            Specifies which metric to compute and display.
    
        Returns
        -------
        ReportTable
        """
        super(GatesSingleMetricTable,self).__init__(
            ws, self._create, gatesets, titles, targetGateset, metric)
    
    def _create(self, gatesets, titles, targetGateset, metric):
    
        gateLabels = list(targetGateset.gates.keys())  # use target's gate labels
        basisNm = targetGateset.basis.name
        basisDims = targetGateset.basis.dim.blockDims

        #Check that all gatesets are in the same basis as targetGateset
        for title,gateset in zip(titles,gatesets):
            if basisNm != gateset.basis.name:
                raise ValueError("Basis mismatch between '%s' gateset (%s) and target (%s)!"\
                                 % (title, gateset.basis.name, basisNm))

        #Do computation first
        metricVals = [] #one element per row (gate label)
        for gl in gateLabels:
            cmpGate = targetGateset.gates[gl]
            dct = {}
            for title,gateset in zip(titles,gatesets):
                gate = gateset.gates[gl]
                if metric == "infidelity":
                    dct[title] = 1-_tools.process_fidelity(gate, cmpGate, basisNm)
                elif metric == "diamond":
                    dct[title] = _tools.jtracedist(gate, cmpGate, basisNm)
                elif metric == "jtrace":
                    dct[title] = 0.5 * _tools.diamonddist(gate, cmpGate, basisNm)
                else: raise ValueError("Invalid `metric` argument: %s" % metric)
            metricVals.append(dct)

            
        if metric == "infidelity":
            niceNm = "Process Infidelity"
        elif metric == "diamond":
            niceNm = "1/2 Diamond-Norm"
        elif metric == "jtrace":
            niceNm = "1/2 Trace Distance"
        else: raise ValueError("Invalid `metric` argument: %s" % metric)

        def mknice(x):
            if x == "H": return "$\mathcal{H}$"
            if x == "S": return "$\mathcal{H}$"
            if x in ("H + S","H+S"): return "$\mathcal{H} + \mathcal{S}$"
            return x
        
        colHeadings = ("Gate",) + \
                      tuple( [ "%s(%s)" % (niceNm,title) for title in titles] )
        nCols = len(colHeadings)
        formatters = [None] + ['GatesetType']*(nCols-1)

        latex_head =  "\\begin{tabular}[l]{%s}\n\hline\n" % ("|c" * nCols + "|")
        latex_head += "\\multirow{2}{*}{Gate} & " + \
                      "\\multicolumn{%d}{c|}{%s} \\\\ \cline{2-%d}\n" % (len(titles),niceNm,nCols)
        latex_head += " & " + " & ".join([mknice(t) for t in titles]) + "\\\\ \hline\n"

        html_head = '<table class="%(tableclass)s" id="%(tableid)s" ><thead>'
        html_head += '<tr><th rowspan="2"></th>' + \
                     '<th colspan="%d">%s</th></tr>\n' % (len(titles),niceNm)
        html_head += "<tr><th>" +  " </th><th> ".join([mknice(t) for t in titles]) + "</th></tr>\n"
        html_head += "</thead><tbody>"
    
        table = _ReportTable(colHeadings, formatters,
                             customHeader={'latex': latex_head,
                                           'html': html_head} )

        for gl,dct in zip(gateLabels,metricVals):
            row_data = [gl] + [ dct[t] for t in titles ]
            row_formatters = [None] + ['Normal']*len(titles)
            table.addrow(row_data, row_formatters)
    
        table.finish()
        return table
    
    
#    def get_err_gen_projector_boxes_table(gateset_dim, projection_type,
#                                          projection_basis, figFilePrefix,
#                                          maxWidth=6.5, maxHeight=8.0):
class StandardErrgenTable(WorkspaceTable):
    def __init__(self, ws, gateset_dim, projection_type,
                 projection_basis):
        """
        Create a table of the "standard" gate error generators, such as those
        which correspond to Hamiltonian or Stochastic errors.  Each generator
        is shown as grid of colored boxes.
    
        Parameters
        ----------
        gateset_dim : int
            The dimension of the gate set, which equals the number of 
            rows (or columns) in a gate matrix (e.g., 4 for a single qubit).
    
        projection_type : {"hamiltonian", "stochastic"}
            The type of error generator projectors to create a table for.
            If "hamiltonian", then use the Hamiltonian generators which take a
            density matrix rho -> -i*[ H, rho ] for basis matrix H.
            If "stochastic", then use the Stochastic error generators which take
            rho -> P*rho*P for basis matrix P (recall P is self adjoint).
    
        projection_basis : {'std', 'gm', 'pp', 'qt'}
          Which basis is used to construct the error generators.  Allowed
          values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp)
          and Qutrit (qt).
        
        Returns
        -------
        ReportTable
        """
        super(StandardErrgenTable,self).__init__(
            ws, self._create, gateset_dim, projection_type,
            projection_basis)
    

    def _create(self,  gateset_dim, projection_type,
                projection_basis):
    
        d2 = gateset_dim # number of projections == dim of gate
        d = int(_np.sqrt(d2)) # dim of density matrix
        nQubits = _np.log2(d)
    
        #Get a list of the d2 generators (in corresspondence with the
        #  given basis matrices)
        lindbladMxs = _tools.std_error_generators(d2, projection_type,
                                                  projection_basis) # in std basis
    
        if not _np.isclose(round(nQubits),nQubits): 
            #Non-integral # of qubits, so just show as a single row
            yd,xd = 1,d
            xlabel = ""; ylabel = ""        
        if nQubits == 1:
            yd,xd = 1,2 # y and x pauli-prod *basis* dimensions
            xlabel = "Q1"; ylabel = ""
        elif nQubits == 2:
            yd,xd = 2,2
            xlabel = "Q2"; ylabel="Q1"
        else:
            yd,xd = 2,d/2
            xlabel = "Q*"; ylabel="Q1"
    
        topright = "%s \\ %s" % (ylabel,xlabel) if (len(ylabel) > 0) else ""
        colHeadings=[topright] + \
            [("%s" % x) if len(x) else "" \
                 for x in _tools.basis_element_labels(projection_basis,xd)]
        rowLabels=[("%s" % x) if len(x) else "" \
                     for x in _tools.basis_element_labels(projection_basis,yd)]
    
        xLabels = _tools.basis_element_labels(projection_basis,xd)
        yLabels = _tools.basis_element_labels(projection_basis,yd)
    
        table = _ReportTable(colHeadings,["Conversion"]+[None]*(len(colHeadings)-1))
            
        iCur = 0
        for i,ylabel  in enumerate(yLabels):
            rowData = [rowLabels[i]]
            rowFormatters = [None]
    
            for j,xlabel in enumerate(xLabels):
                projector = lindbladMxs[iCur]; iCur += 1
                projector = _tools.change_basis(projector,"std",projection_basis)
                m,M = -_np.max(_np.abs(projector)), _np.max(_np.abs(projector))
                fig = _wp.GateMatrixPlot(self.ws, projector, m,M,
                                         projection_basis, d)
    
                rowData.append(fig)
                rowFormatters.append('Figure')
    
            table.addrow(rowData, rowFormatters)
    
        table.finish()
        return table
    
    
    
#    def get_gaugeopt_params_table(gaugeOptArgs):
class GaugeOptParamsTable(WorkspaceTable):
    def __init__(self, ws, gaugeOptArgs):
        """
        Create a table displaying a list of gauge
        optimzation parameters.
    
        Parameters
        ----------
        gaugeOptArgs : dict
            A dictionary specifying values for zero or more of the
            *arguments* of pyGSTi's :func:`gaugeopt_to_target` function.
    
        Returns
        -------
        ReportTable
        """
        super(GaugeOptParamsTable,self).__init__(ws, self._create, gaugeOptArgs)
    
    def _create(self, gaugeOptArgs):
        
        colHeadings = ('Quantity','Value')
        formatters = ('Bold','Bold')
    
        table = _ReportTable(colHeadings, formatters)
        
        if gaugeOptArgs == False: #signals *no* gauge optimization
            gaugeOptArgs = {'Method': "No gauge optimization was performed" }
    
        if 'method' in gaugeOptArgs:
            table.addrow(("Method", str(gaugeOptArgs['method'])), (None,None))
        if 'TPpenalty' in gaugeOptArgs:
            table.addrow(("TP penalty factor", str(gaugeOptArgs['TPpenalty'])), (None,None))
        if 'CPpenalty' in gaugeOptArgs:
            table.addrow(("CP penalty factor", str(gaugeOptArgs['CPpenalty'])), (None,None))
        if 'validSpamPenalty' in gaugeOptArgs:
            table.addrow(("Valid-SPAM constrained", str(gaugeOptArgs['validSpamPenalty'])), (None,None))
        if 'gatesMetric' in gaugeOptArgs:
            table.addrow(("Metric for gate-to-target", str(gaugeOptArgs['gatesMetric'])), (None,None))
        if 'spamMetric' in gaugeOptArgs:
            table.addrow(("Metric for SPAM-to-target", str(gaugeOptArgs['spamMetric'])), (None,None))
        if 'itemWeights' in gaugeOptArgs:
            if gaugeOptArgs['itemWeights']:
                table.addrow(("Item weighting", ", ".join([("%s=%.2g" % (k,v)) 
                               for k,v in gaugeOptArgs['itemWeights'].items()])), (None,None))
        if 'gauge_group' in gaugeOptArgs:
            table.addrow(("Gauge group", str(gaugeOptArgs['gauge_group'])), (None,None))
    
        table.finish()
        return table
    
    
    
#    def get_metadata_table(gateset, result_options, result_params):
class MetadataTable(WorkspaceTable):
    def __init__(self, ws, gateset, params):
        """
        Create a table of parameters and options from a `Results` object.
    
        Parameters
        ----------
        gateset : GateSet
            The gateset (usually the final estimate of a GST computation) to 
            show information for (e.g. the types of its gates).
    
        params: dict
            A parameter dictionary to display
    
        Returns
        -------
        ReportTable
        """
        super(MetadataTable,self).__init__(ws, self._create, gateset, params)
    
    def _create(self, gateset, params_dict):
    
        colHeadings = ('Quantity','Value')
        formatters = ('Bold','Bold')
    
        #custom latex header for maximum width imposed on 2nd col
        latex_head =  "\\begin{tabular}[l]{|c|p{3in}|}\n\hline\n"
        latex_head += "\\textbf{Quantity} & \\textbf{Value} \\\\ \hline\n"
        table = _ReportTable(colHeadings, formatters,
                             customHeader={'latex': latex_head} )
        
        for key in sorted(list(params_dict.keys())):
            if key in ['L,germ tuple base string dict', 'profiler']: continue #skip these
            if key == 'gaugeOptParams':
                if isinstance(params_dict[key],dict):
                    val = params_dict[key].copy()
                    if 'targetGateset' in val:
                        del val['targetGateset'] #don't print this!
                                
                elif isinstance(params_dict[key],list):
                    val = []
                    for go_param_dict in params_dict[key]:
                        if isinstance(go_param_dict,dict): #to ensure .copy() exists
                            val.append(go_param_dict.copy())
                            if 'targetGateset' in val[-1]:
                                del val[-1]['targetGateset'] #don't print this!
            else:
                val = params_dict[key]
            table.addrow((key, str(val)), (None,'Verbatim'))
    
    
        for lbl,vec in gateset.preps.items():
            if isinstance(vec, _objs.StaticSPAMVec): paramTyp = "static"
            elif isinstance(vec, _objs.FullyParameterizedSPAMVec): paramTyp = "full"
            elif isinstance(vec, _objs.TPParameterizedSPAMVec): paramTyp = "TP"
            else: paramTyp = "unknown"
            table.addrow((lbl + " parameterization", paramTyp), (None,'Verbatim'))
    
        for lbl,vec in gateset.effects.items():
            if isinstance(vec, _objs.StaticSPAMVec): paramTyp = "static"
            elif isinstance(vec, _objs.FullyParameterizedSPAMVec): paramTyp = "full"
            elif isinstance(vec, _objs.TPParameterizedSPAMVec): paramTyp = "TP"
            else: paramTyp = "unknown"
            table.addrow((lbl + " parameterization", paramTyp), (None,'Verbatim'))
    
        #Not displayed since the POVM identity is always fully parameterized,
        # even through it doesn't contribute to the gate set parameters (a special case)
        #if gateset.povm_identity is not None:
        #    vec = gateset.povm_identity
        #    if isinstance(vec, _objs.StaticSPAMVec): paramTyp = "static"
        #    elif isinstance(vec, _objs.FullyParameterizedSPAMVec): paramTyp = "full"
        #    elif isinstance(vec, _objs.TPParameterizedSPAMVec): paramTyp = "TP"
        #    else: paramTyp = "unknown"
        #    table.addrow(("POVM identity parameterization", paramTyp), (None,'Verbatim'))
    
        for gl,gate in gateset.gates.items():
            if isinstance(gate, _objs.StaticGate): paramTyp = "static"
            elif isinstance(gate, _objs.FullyParameterizedGate): paramTyp = "full"
            elif isinstance(gate, _objs.TPParameterizedGate): paramTyp = "TP"
            elif isinstance(gate, _objs.LinearlyParameterizedGate): paramTyp = "linear"
            elif isinstance(gate, _objs.EigenvalueParameterizedGate): paramTyp = "eigenvalue"
            elif isinstance(gate, _objs.LindbladParameterizedGate):
                paramTyp = "Lindblad"
                if gate.cptp: paramTyp += " CPTP "
                paramTyp += "(%d, %d params)" % (gate.ham_basis_size, gate.other_basis_size)
            else: paramTyp = "unknown"
            table.addrow((gl + " parameterization", paramTyp), (None,'Verbatim'))
            
        
        table.finish()
        return table
    
    
#    def get_software_environment_table():
class SoftwareEnvTable(WorkspaceTable):
    def __init__(self, ws):
        """
        Create a table displaying the software environment relevant to pyGSTi.
    
        Returns
        -------
        ReportTable
        """
        super(SoftwareEnvTable,self).__init__(ws, self._create)
    
    def _create(self):
    
        import platform
        
        def get_version(moduleName):
            if moduleName == "cvxopt":
                #special case b/c cvxopt can be weird...
                try:
                    mod = __import__("cvxopt.info")
                    return str(mod.info.version)
                except Exception: pass #try the normal way below
    
            try:
                mod = __import__(moduleName)
                return str(mod.__version__)
            except ImportError:
                return "missing"
            except AttributeError:
                return "ver?"
            except Exception:
                return "???"
            
        colHeadings = ('Quantity','Value')
        formatters = ('Bold','Bold')
    
        #custom latex header for maximum width imposed on 2nd col
        latex_head =  "\\begin{tabular}[l]{|c|p{3in}|}\n\hline\n"
        latex_head += "\\textbf{Quantity} & \\textbf{Value} \\\\ \hline\n"
        table = _ReportTable(colHeadings, formatters, 
                             customHeader={'latex': latex_head} )
        
        #Python package information
        from .._version import __version__ as pyGSTi_version
        table.addrow(("pyGSTi version", str(pyGSTi_version)), (None,'Verbatim'))
    
        packages = ['numpy','scipy','matplotlib','pyparsing','cvxopt','cvxpy',
                    'nose','PIL','psutil']
        for pkg in packages:
            table.addrow((pkg, get_version(pkg)), (None,'Verbatim'))
    
        #Python information
        table.addrow(("Python version", str(platform.python_version())), (None,'Verbatim'))
        table.addrow(("Python type", str(platform.python_implementation())), (None,'Verbatim'))
        table.addrow(("Python compiler", str(platform.python_compiler())), (None,'Verbatim'))
        table.addrow(("Python build", str(platform.python_build())), (None,'Verbatim'))
        table.addrow(("Python branch", str(platform.python_branch())), (None,'Verbatim'))
        table.addrow(("Python revision", str(platform.python_revision())), (None,'Verbatim'))
    
        #Platform information
        (system, node, release, version, machine, processor) = platform.uname()
        table.addrow(("Platform summary", str(platform.platform())), (None,'Verbatim'))
        table.addrow(("System", str(system)), (None,'Verbatim'))
        #table.addrow(("Sys Node", str(node)), (None,'Verbatim')) #seems unnecessary
        table.addrow(("Sys Release", str(release)), (None,'Verbatim'))
        table.addrow(("Sys Version", str(version)), (None,'Verbatim'))
        table.addrow(("Machine", str(machine)), (None,'Verbatim'))
        table.addrow(("Processor", str(processor)), (None,'Verbatim'))
    
        table.finish()
        return table
