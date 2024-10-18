OOB_MESSAGE = "out-of-bounds with check interval=%d, reverting to last know in-bounds point and setting interval=1 **"

def custom_leastsq(obj_fn, jac_fn, x0, f_norm2_tol=1e-6, jac_norm_tol=1e-6,
                   rel_ftol=1e-6, rel_xtol=1e-6, max_iter=100, num_fd_iters=0,
                   max_dx_scale=1.0, damping_mode="identity", damping_basis="diagonal_values",
                   damping_clip=None, use_acceleration=False, uphill_step_threshold=0.0,
                   init_munu="auto", oob_check_interval=0, oob_action="reject", oob_check_mode=0,
                   resource_alloc=None, arrays_interface=None, serial_solve_proc_threshold=100,
                   x_limits=None, verbosity=0, profiler=None):
    """
    An implementation of the Levenberg-Marquardt least-squares optimization algorithm customized for use within pyGSTi.

    This general purpose routine mimic to a large extent the interface used by
    `scipy.optimize.leastsq`, though it implements a newer (and more robust) version
    of the algorithm.

    Parameters
    ----------
    obj_fn : function
        The objective function.  Must accept and return 1D numpy ndarrays of
        length N and M respectively.  Same form as scipy.optimize.leastsq.

    jac_fn : function
        The jacobian function (not optional!).  Accepts a 1D array of length N
        and returns an array of shape (M,N).

    x0 : numpy.ndarray
        Initial evaluation point.

    f_norm2_tol : float, optional
        Tolerace for `F^2` where `F = `norm( sum(obj_fn(x)**2) )` is the
        least-squares residual.  If `F**2 < f_norm2_tol`, then mark converged.

    jac_norm_tol : float, optional
        Tolerance for jacobian norm, namely if `infn(dot(J.T,f)) < jac_norm_tol`
        then mark converged, where `infn` is the infinity-norm and
        `f = obj_fn(x)`.

    rel_ftol : float, optional
        Tolerance on the relative reduction in `F^2`, that is, if
        `d(F^2)/F^2 < rel_ftol` then mark converged.

    rel_xtol : float, optional
        Tolerance on the relative value of `|x|`, so that if
        `d(|x|)/|x| < rel_xtol` then mark converged.

    max_iter : int, optional
        The maximum number of (outer) interations.

    num_fd_iters : int optional
        Internally compute the Jacobian using a finite-difference method
        for the first `num_fd_iters` iterations.  This is useful when `x0`
        lies at a special or singular point where the analytic Jacobian is
        misleading.

    max_dx_scale : float, optional
        If not None, impose a limit on the magnitude of the step, so that
        `|dx|^2 < max_dx_scale^2 * len(dx)` (so elements of `dx` should be,
        roughly, less than `max_dx_scale`).

    damping_mode : {'identity', 'JTJ', 'invJTJ', 'adaptive'}
        How damping is applied.  `'identity'` means that the damping parameter mu
        multiplies the identity matrix.  `'JTJ'` means that mu multiplies the
        diagonal or singular values (depending on `scaling_mode`) of the JTJ
        (Fischer information and approx. hessaian) matrix, whereas `'invJTJ'`
        means mu multiplies the reciprocals of these values instead.  The
        `'adaptive'` mode adaptively chooses a damping strategy.

    damping_basis : {'diagonal_values', 'singular_values'}
        Whether the the diagonal or singular values of the JTJ matrix are used
        during damping.  If `'singular_values'` is selected, then a SVD of the
        Jacobian (J) matrix is performed and damping is performed in the basis
        of (right) singular vectors.  If `'diagonal_values'` is selected, the
        diagonal values of relevant matrices are used as a proxy for the the
        singular values (saving the cost of performing a SVD).

    damping_clip : tuple, optional
        A 2-tuple giving upper and lower bounds for the values that mu multiplies.
        If `damping_mode == "identity"` then this argument is ignored, as mu always
        multiplies a 1.0 on the diagonal if the identity matrix.  If None, then no
        clipping is applied.

    use_acceleration : bool, optional
        Whether to include a geodesic acceleration term as suggested in
        arXiv:1201.5885.  This is supposed to increase the rate of
        convergence with very little overhead.  In practice we've seen
        mixed results.

    uphill_step_threshold : float, optional
        Allows uphill steps when taking two consecutive steps in nearly
        the same direction.  The condition for accepting an uphill step
        is that `(uphill_step_threshold-beta)*new_objective < old_objective`,
        where `beta` is the cosine of the angle between successive steps.
        If `uphill_step_threshold == 0` then no uphill steps are allowed,
        otherwise it should take a value between 1.0 and 2.0, with 1.0 being
        the most permissive to uphill steps.

    init_munu : tuple, optional
        If not None, a (mu, nu) tuple of 2 floats giving the initial values
        for mu and nu.

    oob_check_interval : int, optional
        Every `oob_check_interval` outer iterations, the objective function
        (`obj_fn`) is called with a second argument 'oob_check', set to True.
        In this case, `obj_fn` can raise a ValueError exception to indicate
        that it is Out Of Bounds.  If `oob_check_interval` is 0 then this
        check is never performed; if 1 then it is always performed.

    oob_action : {"reject","stop"}
        What to do when the objective function indicates (by raising a ValueError
        as described above).  `"reject"` means the step is rejected but the
        optimization proceeds; `"stop"` means the optimization stops and returns
        as converged at the last known-in-bounds point.

    oob_check_mode : int, optional
        An advanced option, expert use only.  If 0 then the optimization is
        halted as soon as an *attempt* is made to evaluate the function out of bounds.
        If 1 then the optimization is halted only when a would-be *accepted* step
        is out of bounds.

    resource_alloc : ResourceAllocation, optional
        When not None, an resource allocation object used for distributing the computation
        across multiple processors.

    arrays_interface : ArraysInterface
        An object that provides an interface for creating and manipulating data arrays.

    serial_solve_proc_threshold : int optional
        When there are fewer than this many processors, the optimizer will solve linear
        systems serially, using SciPy on a single processor, rather than using a parallelized
        Gaussian Elimination (with partial pivoting) algorithm coded in Python. Since SciPy's
        implementation is more efficient, it's not worth using the parallel version until there
        are many processors to spread the work among.

    x_limits : numpy.ndarray, optional
        A (num_params, 2)-shaped array, holding on each row the (min, max) values for the corresponding
        parameter (element of the "x" vector).  If `None`, then no limits are imposed.

    verbosity : int, optional
        Amount of detail to print to stdout.

    profiler : Profiler, optional
        A profiler object used for to track timing and memory usage.

    Returns
    -------
    x : numpy.ndarray
        The optimal solution.
    converged : bool
        Whether the solution converged.
    msg : str
        A message indicating why the solution converged (or didn't).
    """
    resource_alloc = _ResourceAllocation.cast(resource_alloc)
    comm = resource_alloc.comm
    printer = _VerbosityPrinter.create_printer(verbosity, comm)
    ari = arrays_interface  # shorthand

    msg = ""
    converged = False
    global_x = x0.copy()
    f = obj_fn(global_x)  # 'E'-type array
    norm_f = ari.norm2_f(f)  # _np.linalg.norm(f)**2
    half_max_nu = 2**62  # what should this be??
    tau = 1e-3
    alpha = 0.5  # for acceleration
    nu = 2
    mu = 1  # just a guess - initialized on 1st iter and only used if rejected

    #Allocate potentially shared memory used in loop
    JTJ = ari.allocate_jtj()
    JTf = ari.allocate_jtf()
    x = ari.allocate_jtf()
    #x_for_jac = ari.allocate_x_for_jac()
    if num_fd_iters > 0:
        fdJac = ari.allocate_jac()

    ari.allscatter_x(global_x, x)

    if x_limits is not None:
        x_lower_limits = ari.allocate_jtf()
        x_upper_limits = ari.allocate_jtf()
        ari.allscatter_x(x_limits[:, 0], x_lower_limits)
        ari.allscatter_x(x_limits[:, 1], x_upper_limits)

    if damping_basis == "singular_values":
        Jac_V = ari.allocate_jtj()

    if damping_mode == 'adaptive':
        dx_lst = [ari.allocate_jtf(), ari.allocate_jtf(), ari.allocate_jtf()]
        new_x_lst = [ari.allocate_jtf(), ari.allocate_jtf(), ari.allocate_jtf()]
        global_new_x_lst = [global_x.copy() for i in range(3)]
    else:
        dx = ari.allocate_jtf()
        new_x = ari.allocate_jtf()
        global_new_x = global_x.copy()
        if use_acceleration:
            dx1 = ari.allocate_jtf()
            dx2 = ari.allocate_jtf()
            df2_x = ari.allocate_jtf()
            JTdf2 = ari.allocate_jtf()
            global_accel_x = global_x.copy()

    # don't let any component change by more than ~max_dx_scale
    if max_dx_scale:
        max_norm_dx = (max_dx_scale**2) * len(global_x)
    else: max_norm_dx = None

    if not _np.isfinite(norm_f):
        msg = "Infinite norm of objective function at initial point!"

    if len(global_x) == 0:  # a model with 0 parameters - nothing to optimize
        msg = "No parameters to optimize"; converged = True
    #num_fd_iters = 1000000 # DEBUG: use finite difference iterations instead
    # print("DEBUG: setting num_fd_iters == 0!");  num_fd_iters = 0 # DEBUG
    last_accepted_dx = None
    min_norm_f = 1e100  # sentinel
    best_x = ari.allocate_jtf()
    best_x[:] = x[:]  # like x.copy() -the x-value corresponding to min_norm_f ('P'-type)

    spow = 0.0  # for damping_mode == 'adaptive'
    if damping_clip is not None:
        def dclip(ar): return _np.clip(ar, damping_clip[0], damping_clip[1])
    else:
        def dclip(ar): return ar

    if init_munu != "auto":
        mu, nu = init_munu
    best_x_state = (mu, nu, norm_f, f.copy(), spow, None)  # need f.copy() b/c f is objfn mem
    rawJTJ_scratch = None
    jtj_buf = ari.allocate_jtj_shared_mem_buf()

    try:

        for k in range(max_iter):  # outer loop
            # assume global_x, x, f, fnorm hold valid values

            if len(msg) > 0:
                break  # exit outer loop if an exit-message has been set

            if norm_f < f_norm2_tol:
                if oob_check_interval <= 1:
                    msg = "Sum of squares is at most %g" % f_norm2_tol
                    converged = True; break
                else:
                    printer.log("** Converged with " + (OOB_MESSAGE % oob_check_interval), 2)
                    oob_check_interval = 1
                    x[:] = best_x[:]
                    mu, nu, norm_f, f[:], spow, _ = best_x_state
                    continue  # can't make use of saved JTJ yet - recompute on nxt iter

            if profiler: profiler.memory_check("custom_leastsq: begin outer iter *before de-alloc*")
            Jac = None

            if profiler: profiler.memory_check("custom_leastsq: begin outer iter")

            # unnecessary b/c global_x is already valid: ari.allgather_x(x, global_x)
            if k >= num_fd_iters:
                Jac = jac_fn(global_x)  # 'EP'-type, but doesn't actually allocate any more mem (!)
            else:
                # Note: x holds only number of "fine"-division params - need to use global_x, and
                # Jac only holds a subset of the derivative and element columns and rows, respectively.
                f_fixed = f.copy()  # a static part of the distributed `f` resturned by obj_fn - MUST copy this.

                pslice = ari.jac_param_slice(only_if_leader=True)
                eps = 1e-7
                #Don't do this: for ii, i in enumerate(range(pslice.start, pslice.stop)): (must keep procs in sync)
                for i in range(len(global_x)):
                    x_plus_dx = global_x.copy()
                    x_plus_dx[i] += eps
                    fd = (obj_fn(x_plus_dx) - f_fixed) / eps
                    if pslice.start <= i < pslice.stop:
                        fdJac[:, i - pslice.start] = fd
                    #if comm is not None: comm.barrier()  # overkill for shared memory leader host barrier
                Jac = fdJac

            if profiler: profiler.memory_check("custom_leastsq: after jacobian:"
                                               + "shape=%s, GB=%.2f" % (str(Jac.shape),
                                                                        Jac.nbytes / (1024.0**3)))
            Jnorm = _np.sqrt(ari.norm2_jac(Jac))
            xnorm = _np.sqrt(ari.norm2_x(x))
            printer.log("--- Outer Iter %d: norm_f = %g, mu=%g, |x|=%g, |J|=%g" % (k, norm_f, mu, xnorm, Jnorm))

            tm = _time.time()

            # Riley note: fill_JTJ is the first place where we try to access J as a dense matrix.
            ari.fill_jtj(Jac, JTJ, jtj_buf)
            ari.fill_jtf(Jac, f, JTf)  # 'P'-type

            if profiler: profiler.add_time("custom_leastsq: dotprods", tm)

            idiag = ari.jtj_diag_indices(JTJ)
            norm_JTf = ari.infnorm_x(JTf)
            norm_x = ari.norm2_x(x)  # _np.linalg.norm(x)**2
            undamped_JTJ_diag = JTJ[idiag].copy()  # 'P'-type
            #max_JTJ_diag = JTJ.diagonal().copy()

            JTf *= -1.0; minus_JTf = JTf  # use the same memory for -JTf below (shouldn't use JTf anymore)
            #Maybe just have a minus_JTf variable?

            # FUTURE TODO: keep tallying allocated memory, i.e. array_types (stopped here)

            if damping_basis == "singular_values":
                # Jac = U * s * Vh; J.T * J = conj(V) * s * U.T * U * s * Vh = conj(V) * s^2 * Vh
                # Jac_U, Jac_s, Jac_Vh = _np.linalg.svd(Jac, full_matrices=False)
                # Jac_V = _np.conjugate(Jac_Vh.T)

                global_JTJ = ari.gather_jtj(JTJ)
                if comm is None or comm.rank == 0:
                    global_Jac_s2, global_Jac_V = _np.linalg.eigh(global_JTJ)
                    ari.scatter_jtj(global_Jac_V, Jac_V)
                    comm.bcast(global_Jac_s2, root=0)
                else:
                    ari.scatter_jtj(None, Jac_V)
                    global_Jac_s2 = comm.bcast(None, root=0)
                #if min(global_Jac_s2) < -1e-4 and (comm is None or comm.rank == 0):
                #    print("WARNING: min Jac s^2 = %g (max = %g)" % (min(global_Jac_s2), max(global_Jac_s2)))
                assert(min(global_Jac_s2) / abs(max(global_Jac_s2)) > -1e-6), "JTJ should be positive!"
                global_Jac_s = _np.sqrt(_np.clip(global_Jac_s2, 1e-12, None))  # eigvals of JTJ must be >= 0
                global_Jac_VT_mJTf = ari.global_svd_dot(Jac_V, minus_JTf)  # = dot(Jac_V.T, minus_JTf)

            if norm_JTf < jac_norm_tol:
                if oob_check_interval <= 1:
                    msg = "norm(jacobian) is at most %g" % jac_norm_tol
                    converged = True; break
                else:
                    printer.log("** Converged with " + (OOB_MESSAGE % oob_check_interval), 2)
                    oob_check_interval = 1
                    x[:] = best_x[:]
                    mu, nu, norm_f, f[:], spow, _ = best_x_state
                    continue  # can't make use of saved JTJ yet - recompute on nxt iter

            if k == 0:
                if init_munu == "auto":
                    if damping_mode == 'identity':
                        mu = tau * ari.max_x(undamped_JTJ_diag)  # initial damping element
                        #mu = min(mu, MU_TOL1)
                    else:
                        # initial multiplicative damping element
                        #mu = tau # initial damping element - but this seem to low, at least for termgap...
                        mu = min(1.0e5, ari.max_x(undamped_JTJ_diag) / norm_JTf)  # Erik's heuristic
                        #tries to avoid making mu so large that dx is tiny and we declare victory prematurely
                else:
                    mu, nu = init_munu
                rawJTJ_scratch = JTJ.copy()  # allocates the memory for a copy of JTJ so only update mem elsewhere
                best_x_state = mu, nu, norm_f, f.copy(), spow, rawJTJ_scratch  # update mu,nu,JTJ of initial best state
            else:
                #on all other iterations, update JTJ of best_x_state if best_x == x, i.e. if we've just evaluated
                # a previously accepted step that was deemed the best we've seen so far
                if _np.allclose(x, best_x):
                    rawJTJ_scratch[:, :] = JTJ[:, :]  # use pre-allocated memory
                    rawJTJ_scratch[idiag] = undamped_JTJ_diag  # no damping; the "raw" JTJ
                    best_x_state = best_x_state[0:5] + (rawJTJ_scratch,)  # update mu,nu,JTJ of initial "best state"

            #determing increment using adaptive damping
            while True:  # inner loop

                if profiler: profiler.memory_check("custom_leastsq: begin inner iter")

                if damping_mode == 'identity':
                    assert(damping_clip is None), "damping_clip cannot be used with damping_mode == 'identity'"
                    if damping_basis == "singular_values":
                        reg_Jac_s = global_Jac_s + mu

                        #Notes:
                        #Previously we computed inv_JTJ here and below computed dx:
                        #inv_JTJ = _np.dot(Jac_V, _np.dot(_np.diag(1 / reg_Jac_s**2), Jac_V.T))
                        # dx = _np.dot(Jac_V, _np.diag(1 / reg_Jac_s**2), global_Jac_VT_mJTf
                        #But now we just compute reg_Jac_s here, and so the rest below.
                    else:
                        # ok if assume fine-param-proc.size == 1 (otherwise need to sync setting local JTJ)
                        JTJ[idiag] = undamped_JTJ_diag + mu  # augment normal equations

                elif damping_mode == 'JTJ':
                    if damping_basis == "singular_values":
                        reg_Jac_s = global_Jac_s + mu * dclip(global_Jac_s)
                    else:
                        add_to_diag = mu * dclip(undamped_JTJ_diag)
                        JTJ[idiag] = undamped_JTJ_diag + add_to_diag  # ok if assume fine-param-proc.size == 1

                elif damping_mode == 'invJTJ':
                    if damping_basis == "singular_values":
                        reg_Jac_s = global_Jac_s + mu * dclip(1.0 / global_Jac_s)
                    else:
                        add_to_diag = mu * dclip(1.0 / undamped_JTJ_diag)
                        JTJ[idiag] = undamped_JTJ_diag + add_to_diag  # ok if assume fine-param-proc.size == 1

                elif damping_mode == 'adaptive':
                    if damping_basis == "singular_values":
                        reg_Jac_s_lst = [global_Jac_s + mu * dclip(global_Jac_s**(spow + 0.1)),
                                         global_Jac_s + mu * dclip(global_Jac_s**spow),
                                         global_Jac_s + mu * dclip(global_Jac_s**(spow - 0.1))]
                    else:
                        add_to_diag_lst = [mu * dclip(undamped_JTJ_diag**(spow + 0.1)),
                                           mu * dclip(undamped_JTJ_diag**spow),
                                           mu * dclip(undamped_JTJ_diag**(spow - 0.1))]
                else:
                    raise ValueError("Invalid damping mode: %s" % damping_mode)

                try:
                    if profiler: profiler.memory_check("custom_leastsq: before linsolve")
                    tm = _time.time()
                    success = True

                    if damping_basis == 'diagonal_values':
                        if damping_mode == 'adaptive':
                            for ii, add_to_diag in enumerate(add_to_diag_lst):
                                JTJ[idiag] = undamped_JTJ_diag + add_to_diag  # ok if assume fine-param-proc.size == 1
                                #dx_lst.append(_scipy.linalg.solve(JTJ, -JTf, sym_pos=True))
                                #dx_lst.append(custom_solve(JTJ, -JTf, resource_alloc))
                                _custom_solve(JTJ, minus_JTf, dx_lst[ii], ari, resource_alloc,
                                              serial_solve_proc_threshold)
                        else:
                            #dx = _scipy.linalg.solve(JTJ, -JTf, sym_pos=True)
                            _custom_solve(JTJ, minus_JTf, dx, ari, resource_alloc, serial_solve_proc_threshold)

                    elif damping_basis == 'singular_values':
                        #Note: above solves JTJ*x = -JTf => x = inv_JTJ * (-JTf)
                        # but: J = U*s*Vh => JTJ = (VhT*s*UT)(U*s*Vh) = VhT*s^2*Vh, and inv_Vh = V b/c V is unitary
                        # so inv_JTJ = inv_Vh * 1/s^2 * inv_VhT = V * 1/s^2 * VT  = (N,K)*(K,K)*(K,N) if use psuedoinv

                        if damping_mode == 'adaptive':
                            #dx_lst = [_np.dot(ijtj, minus_JTf) for ijtj in inv_JTJ_lst]  # special case
                            for ii, s in enumerate(reg_Jac_s_lst):
                                ari.fill_dx_svd(Jac_V, (1 / s**2) * global_Jac_VT_mJTf, dx_lst[ii])
                        else:
                            # dx = _np.dot(inv_JTJ, minus_JTf)
                            ari.fill_dx_svd(Jac_V, (1 / reg_Jac_s**2) * global_Jac_VT_mJTf, dx)
                    else:
                        raise ValueError("Invalid damping_basis = '%s'" % damping_basis)

                    if profiler: profiler.add_time("custom_leastsq: linsolve", tm)
                #except _np.linalg.LinAlgError:
                except _scipy.linalg.LinAlgError:  # DIST TODO - a different kind of exception caught?
                    success = False

                if success and use_acceleration:  # Find acceleration term:
                    assert(damping_mode != 'adaptive'), "Cannot use acceleration in adaptive mode (yet)"
                    assert(damping_basis != 'singular_values'), "Cannot use acceleration w/singular-value basis (yet)"
                    df2_eps = 1.0
                    try:
                        #df2 = (obj_fn(x + df2_dx) + obj_fn(x - df2_dx) - 2 * f) / \
                        #    df2_eps**2  # 2nd deriv of f along dx direction
                        # Above line expanded to reuse shared memory
                        df2 = -2 * f
                        df2_x[:] = x + df2_eps * dx
                        ari.allgather_x(df2_x, global_accel_x)
                        df2 += obj_fn(global_accel_x)
                        df2_x[:] = x - df2_eps * dx
                        ari.allgather_x(df2_x, global_accel_x)
                        df2 += obj_fn(global_accel_x)
                        df2 /= df2_eps**2
                        f[:] = df2; df2 = f  # use `f` as an appropriate shared-mem object for fill_jtf below

                        ari.fill_jtf(Jac, df2, JTdf2)
                        JTdf2 *= -0.5  # keep using JTdf2 memory in solve call below
                        #dx2 = _scipy.linalg.solve(JTJ, -0.5 * JTdf2, sym_pos=True)  # Note: JTJ not init w/'adaptive'
                        _custom_solve(JTJ, JTdf2, dx2, ari, resource_alloc, serial_solve_proc_threshold)
                        dx1[:] = dx[:]
                        dx += dx2  # add acceleration term to dx
                    except _scipy.linalg.LinAlgError:
                        print("WARNING - linear solve failed for acceleration term!")
                        # but ok to continue - just stick with first order term
                    except ValueError:
                        print("WARNING - value error during computation of acceleration term!")

                reject_msg = ""
                if profiler: profiler.memory_check("custom_leastsq: after linsolve")
                if success:  # linear solve succeeded
                    #dx = _hack_dx(obj_fn, x, dx, Jac, JTJ, JTf, f, norm_f)

                    if damping_mode != 'adaptive':
                        new_x[:] = x + dx
                        norm_dx = ari.norm2_x(dx)  # _np.linalg.norm(dx)**2

                        #ensure dx isn't too large - don't let any component change by more than ~max_dx_scale
                        if max_norm_dx and norm_dx > max_norm_dx:
                            dx *= _np.sqrt(max_norm_dx / norm_dx)
                            new_x[:] = x + dx
                            norm_dx = ari.norm2_x(dx)  # _np.linalg.norm(dx)**2

                        #apply x limits (bounds)
                        if x_limits is not None:
                            # Approach 1: project x into valid space by simply clipping out-of-bounds values
                            for i, (x_el, lower, upper) in enumerate(zip(x, x_lower_limits, x_upper_limits)):
                                if new_x[i] < lower:
                                    new_x[i] = lower
                                    dx[i] = lower - x_el
                                elif new_x[i] > upper:
                                    new_x[i] = upper
                                    dx[i] = upper - x_el
                            norm_dx = ari.norm2_x(dx)  # _np.linalg.norm(dx)**2

                            # Approach 2: by scaling back dx (seems less good, but here in case we want it later)
                            # # minimally reduce dx s.t. new_x = x + dx so that x_lower_limits <= x+dx <= x_upper_limits
                            # # x_lower_limits - x <= dx <= x_upper_limits - x.  Note: use potentially updated dx from
                            # # max_norm_dx block above.  For 0 <= scale <= 1,
                            # # 1) require x + scale*dx - x_upper_limits <= 0 => scale <= (x_upper_limits - x) / dx
                            # #    [Note: above assumes dx > 0 b/c if not it moves x away from bound and scale < 0]
                            # #    so if scale >= 0, then scale = min((x_upper_limits - x) / dx, 1.0)
                            # scale = None
                            # new_x[:] = (x_upper_limits - x) / dx
                            # new_x_min = ari.min_x(new_x)
                            # if 0 <= new_x_min < 1.0:
                            #     scale = new_x_min
                            #
                            # # 2) require x + scale*dx - x_lower_limits <= 0 => scale <= (x - x_lower_limits) / (-dx)
                            # new_x[:] = (x_lower_limits - x) / dx
                            # new_x_min = ari.min_x(new_x)
                            # if 0 <= new_x_min < 1.0:
                            #     scale = new_x_min if (scale is None) else min(new_x_min, scale)
                            #
                            # if scale is not None:
                            #     dx *= scale
                            # new_x[:] = x + dx
                            # norm_dx = ari.norm2_x(dx)  # _np.linalg.norm(dx)**2

                    else:
                        for dx, new_x in zip(dx_lst, new_x_lst):
                            new_x[:] = x + dx
                        norm_dx_lst = [ari.norm2_x(dx) for dx in dx_lst]

                        #ensure dx isn't too large - don't let any component change by more than ~max_dx_scale
                        if max_norm_dx:
                            for i, norm_dx in enumerate(norm_dx_lst):
                                if norm_dx > max_norm_dx:
                                    dx_lst[i] *= _np.sqrt(max_norm_dx / norm_dx)
                                    new_x_lst[i][:] = x + dx_lst[i]
                                    norm_dx_lst[i] = ari.norm2_x(dx_lst[i])

                        #apply x limits (bounds)
                        if x_limits is not None:
                            for i, (dx, new_x) in enumerate(zip(dx_lst, new_x_lst)):
                                # Do same thing as above for each possible dx in dx_lst
                                # Approach 1:
                                for ii, (x_el, lower, upper) in enumerate(zip(x, x_lower_limits, x_upper_limits)):
                                    if new_x[ii] < lower:
                                        new_x[ii] = lower
                                        dx[ii] = lower - x_el
                                    elif new_x[ii] > upper:
                                        new_x[ii] = upper
                                        dx[ii] = upper - x_el
                                norm_dx_lst[i] = ari.norm2_x(dx)  # _np.linalg.norm(dx)**2

                                # Approach 2:
                                # scale = None
                                # new_x[:] = (x_upper_limits - x) / dx
                                # new_x_min = ari.min_x(new_x)
                                # if 0 <= new_x_min < 1.0:
                                #     scale = new_x_min
                                #
                                # new_x[:] = (x_lower_limits - x) / dx
                                # new_x_min = ari.min_x(new_x)
                                # if 0 <= new_x_min < 1.0:
                                #     scale = new_x_min if (scale is None) else min(new_x_min, scale)
                                #
                                # if scale is not None:
                                #     dx *= scale
                                # new_x[:] = x + dx
                                # norm_dx_lst[i] = ari.norm2_x(dx)

                        norm_dx = norm_dx_lst[1]  # just use center value for printing & checks below

                    printer.log("  - Inner Loop: mu=%g, norm_dx=%g" % (mu, norm_dx), 2)
                    #MEM if profiler: profiler.memory_check("custom_leastsq: mid inner loop")

                    if norm_dx < (rel_xtol**2) * norm_x:  # and mu < MU_TOL2:
                        if oob_check_interval <= 1:
                            msg = "Relative change, |dx|/|x|, is at most %g" % rel_xtol
                            converged = True; break
                        else:
                            printer.log("** Converged with " + (OOB_MESSAGE % oob_check_interval), 2)
                            oob_check_interval = 1
                            x[:] = best_x[:]
                            mu, nu, norm_f, f[:], spow, _ = best_x_state
                            break

                    if norm_dx > (norm_x + rel_xtol) / (_MACH_PRECISION**2):
                        msg = "(near-)singular linear system"; break

                    if oob_check_interval > 0 and oob_check_mode == 0:
                        if k % oob_check_interval == 0:
                            #Check to see if objective function is out of bounds

                            in_bounds = []
                            if damping_mode == 'adaptive':
                                new_f_lst = []
                                for new_x, global_new_x in zip(new_x_lst, global_new_x_lst):
                                    ari.allgather_x(new_x, global_new_x)
                                    try:
                                        new_f = obj_fn(global_new_x, oob_check=True)
                                    except ValueError:  # Use this to mean - "not allowed, but don't stop"
                                        in_bounds.append(False)
                                        new_f_lst.append(None)  # marks OOB attempts that shouldn't be considered
                                    else:  # no exception raised
                                        in_bounds.append(True)
                                        new_f_lst.append(new_f.copy())
                            else:
                                ari.allgather_x(new_x, global_new_x)
                                try:
                                    new_f = obj_fn(global_new_x, oob_check=True)
                                except ValueError:  # Use this to mean - "not allowed, but don't stop"
                                    in_bounds.append(False)
                                else:
                                    in_bounds.append(True)

                            if any(in_bounds):  # In adaptive mode, proceed if *any* cases are in-bounds
                                new_x_is_allowed = True
                                new_x_is_known_inbounds = True
                            else:
                                MIN_STOP_ITER = 1  # the minimum iteration where an OOB objective stops the optimization
                                if oob_action == "reject" or k < MIN_STOP_ITER:
                                    new_x_is_allowed = False  # (and also not in bounds)
                                elif oob_action == "stop":
                                    if oob_check_interval == 1:
                                        msg = "Objective function out-of-bounds! STOP"
                                        converged = True; break
                                    else:  # reset to last know in-bounds point and not do oob check every step
                                        printer.log(
                                            ("** Hit out-of-bounds with check interval=%d, reverting to last "
                                             "know in-bounds point and setting interval=1 **") % oob_check_interval, 2)
                                        oob_check_interval = 1
                                        x[:] = best_x[:]
                                        mu, nu, norm_f, f[:], spow, _ = best_x_state  # can't make use of saved JTJ yet
                                        break  # restart next outer loop
                                else:
                                    raise ValueError("Invalid `oob_action`: '%s'" % oob_action)
                        else:  # don't check this time

                            if damping_mode == 'adaptive':
                                new_f_lst = []
                                for new_x, global_new_x in zip(new_x_lst, global_new_x_lst):
                                    ari.allgather_x(new_x, global_new_x)
                                    new_f_lst.append(obj_fn(global_new_x).copy())
                            else:
                                ari.allgather_x(new_x, global_new_x)
                                new_f = obj_fn(global_new_x, oob_check=False)

                            new_x_is_allowed = True
                            new_x_is_known_inbounds = False
                    else:
                        #Just evaluate objective function normally; never check for in-bounds condition
                        if damping_mode == 'adaptive':
                            new_f_lst = []
                            for new_x, global_new_x in zip(new_x_lst, global_new_x_lst):
                                ari.allgather_x(new_x, global_new_x)
                                new_f_lst.append(obj_fn(global_new_x).copy())
                        else:
                            ari.allgather_x(new_x, global_new_x)
                            new_f = obj_fn(global_new_x)

                        new_x_is_allowed = True
                        new_x_is_known_inbounds = bool(oob_check_interval == 0)  # consider "in bounds" if not checking

                    if new_x_is_allowed:

                        if damping_mode == 'adaptive':
                            norm_new_f_lst = [ari.norm2_f(new_f) if (new_f is not None) else 1e100
                                              for new_f in new_f_lst]  # 1e100 so we don't choose OOB adaptive cases
                            if any([not _np.isfinite(norm_new_f) for norm_new_f in norm_new_f_lst]):  # avoid inf loop
                                msg = "Infinite norm of objective function!"; break

                            #iMin = _np.argmin(norm_new_f_lst)  # pick lowest (best) objective
                            gain_ratio_lst = [(norm_f - nnf) / ari.dot_x(dx, mu * dx + minus_JTf)
                                              for (nnf, dx) in zip(norm_new_f_lst, dx_lst)]
                            iMin = _np.argmax(gain_ratio_lst)  # pick highest (best) gain ratio
                            # but expected decrease is |f|^2 = grad(fTf) * dx = (grad(fT)*f + fT*grad(f)) * dx
                            #                                                 = (JT*f + fT*J) * dx
                            # <<more explanation>>
                            norm_new_f = norm_new_f_lst[iMin]
                            new_f = new_f_lst[iMin]
                            new_x = new_x_lst[iMin]
                            global_new_x = global_new_x_lst[iMin]
                            dx = dx_lst[iMin]
                            if iMin == 0: spow = min(1.0, spow + 0.1)
                            elif iMin == 2: spow = max(-1.0, spow - 0.1)
                            printer.log("ADAPTIVE damping => i=%d b/c fs=[%s] gains=[%s] => spow=%g" % (
                                iMin, ", ".join(["%.3g" % v for v in norm_new_f_lst]),
                                ", ".join(["%.3g" % v for v in gain_ratio_lst]), spow))

                        else:
                            norm_new_f = ari.norm2_f(new_f)  # _np.linalg.norm(new_f)**2
                            if not _np.isfinite(norm_new_f):  # avoid infinite loop...
                                msg = "Infinite norm of objective function!"; break

                        # dL = expected decrease in ||F||^2 from linear model
                        dL = ari.dot_x(dx, mu * dx + minus_JTf)
                        dF = norm_f - norm_new_f      # actual decrease in ||F||^2

                        if dF <= 0 and uphill_step_threshold > 0:
                            beta = 0 if last_accepted_dx is None else \
                                (ari.dot_x(dx, last_accepted_dx)
                                    / _np.sqrt(ari.norm2_x(dx) * ari.norm2_x(last_accepted_dx)))
                            uphill_ok = (uphill_step_threshold - beta) * norm_new_f < min(min_norm_f, norm_f)
                        else:
                            uphill_ok = False

                        if use_acceleration:
                            accel_ratio = 2 * _np.sqrt(ari.norm2_x(dx2) / ari.norm2_x(dx1))
                            printer.log("      (cont): norm_new_f=%g, dL=%g, dF=%g, reldL=%g, reldF=%g aC=%g" %
                                        (norm_new_f, dL, dF, dL / norm_f, dF / norm_f, accel_ratio), 2)

                        else:
                            printer.log("      (cont): norm_new_f=%g, dL=%g, dF=%g, reldL=%g, reldF=%g" %
                                        (norm_new_f, dL, dF, dL / norm_f, dF / norm_f), 2)
                            accel_ratio = 0.0

                        if dL / norm_f < rel_ftol and dF >= 0 and dF / norm_f < rel_ftol \
                           and dF / dL < 2.0 and accel_ratio <= alpha:
                            if oob_check_interval <= 1:  # (if 0 then no oob checking is done)
                                msg = "Both actual and predicted relative reductions in the" + \
                                    " sum of squares are at most %g" % rel_ftol
                                converged = True; break
                            else:
                                printer.log("** Converged with " + (OOB_MESSAGE % oob_check_interval), 2)
                                oob_check_interval = 1
                                x[:] = best_x[:]
                                mu, nu, norm_f, f[:], spow, _ = best_x_state  # can't make use of saved JTJ yet
                                break

                        if (dL > 0 and dF > 0 and accel_ratio <= alpha) or uphill_ok:
                            #Check whether an otherwise acceptable solution is in-bounds
                            if oob_check_mode == 1 and oob_check_interval > 0 and k % oob_check_interval == 0:
                                #Check to see if objective function is out of bounds
                                try:
                                    obj_fn(global_new_x, oob_check=True)  # don't actually need return val (== new_f)
                                    new_f_is_allowed = True
                                    new_x_is_known_inbounds = True
                                except ValueError:  # Use this to mean - "not allowed, but don't stop"
                                    MIN_STOP_ITER = 1  # the minimum iteration where an OOB objective can stops the opt.
                                    if oob_action == "reject" or k < MIN_STOP_ITER:
                                        new_f_is_allowed = False  # (and also not in bounds)
                                    elif oob_action == "stop":
                                        if oob_check_interval == 1:
                                            msg = "Objective function out-of-bounds! STOP"
                                            converged = True; break
                                        else:  # reset to last know in-bounds point and not do oob check every step
                                            printer.log("** Hit " + (OOB_MESSAGE % oob_check_interval), 2)
                                            oob_check_interval = 1
                                            x[:] = best_x[:]
                                            mu, nu, norm_f, f[:], spow, _ = best_x_state  # can't use of saved JTJ yet
                                            break  # restart next outer loop
                                    else:
                                        raise ValueError("Invalid `oob_action`: '%s'" % oob_action)
                            else:
                                new_f_is_allowed = True

                            if new_f_is_allowed:
                                # reduction in error: increment accepted!
                                t = 1.0 - (2 * dF / dL - 1.0)**3  # dF/dL == gain ratio
                                # always reduce mu for accepted step when |dx| is small
                                mu_factor = max(t, 1.0 / 3.0) if norm_dx > 1e-8 else 0.3
                                mu *= mu_factor
                                nu = 2
                                x[:] = new_x[:]; f[:] = new_f[:]; norm_f = norm_new_f
                                global_x[:] = global_new_x[:]
                                printer.log("      Accepted%s! gain ratio=%g  mu * %g => %g"
                                            % (" UPHILL" if uphill_ok else "", dF / dL, mu_factor, mu), 2)
                                last_accepted_dx = dx.copy()
                                if new_x_is_known_inbounds and norm_f < min_norm_f:
                                    min_norm_f = norm_f
                                    best_x[:] = x[:]
                                    best_x_state = (mu, nu, norm_f, f.copy(), spow, None)
                                    #Note: we use rawJTJ=None above because the current `JTJ` was evaluated
                                    # at the *last* x-value -- we need to wait for the next outer loop
                                    # to compute the JTJ for this best_x_state

                                break  # exit inner loop normally
                            else:
                                reject_msg = " (out-of-bounds)"
                    else:
                        reject_msg = " (out-of-bounds)"

                else:
                    reject_msg = " (LinSolve Failure)"

                # if this point is reached, either the linear solve failed
                # or the error did not reduce.  In either case, reject increment.

                #Increase damping (mu), then increase damping factor to
                # accelerate further damping increases.
                mu *= nu
                if nu > half_max_nu:  # watch for nu getting too large (&overflow)
                    msg = "Stopping after nu overflow!"; break
                nu = 2 * nu
                printer.log("      Rejected%s!  mu => mu*nu = %g, nu => 2*nu = %g"
                            % (reject_msg, mu, nu), 2)
            #end of inner loop

        #end of outer loop
        else:
            #if no break stmt hit, then we've exceeded max_iter
            msg = "Maximum iterations (%d) exceeded" % max_iter
            converged = True  # call result "converged" even in this case, but issue warning:
            printer.warning("Treating result as *converged* after maximum iterations (%d) were exceeded." % max_iter)

    except KeyboardInterrupt:
        if comm is not None:
            # ensure all procs agree on what best_x is (in case the interrupt occurred around x being updated)
            comm.Bcast(best_x, root=0)
            printer.log("Rank %d caught keyboard interrupt!  Returning the current solution as being *converged*."
                        % comm.Get_rank())
        else:
            printer.log("Caught keyboard interrupt!  Returning the current solution as being *converged*.")
        msg = "Keyboard interrupt!"
        converged = True

    if comm is not None:
        comm.barrier()  # Just to be safe, so procs stay synchronized and we don't free anything too soon

    ari.deallocate_jtj(JTJ)
    ari.deallocate_jtf(JTf)
    ari.deallocate_jtf(x)
    ari.deallocate_jtj_shared_mem_buf(jtj_buf)
    #ari.deallocate_x_for_jac(x_for_jac)

    if x_limits is not None:
        ari.deallocate_jtf(x_lower_limits)
        ari.deallocate_jtf(x_upper_limits)

    if damping_basis == "singular_values":
        ari.deallocate_jtj(Jac_V)

    if damping_mode == 'adaptive':
        for xx in dx_lst: ari.deallocate_jtf(xx)
        for xx in new_x_lst: ari.deallocate_jtf(xx)
    else:
        ari.deallocate_jtf(dx)
        ari.deallocate_jtf(new_x)
        if use_acceleration:
            ari.deallocate_jtf(dx1)
            ari.deallocate_jtf(dx2)
            ari.deallocate_jtf(df2_x)
            ari.deallocate_jtf(JTdf2)

    if num_fd_iters > 0:
        ari.deallocate_jac(fdJac)

    ari.allgather_x(best_x, global_x)
    ari.deallocate_jtf(best_x)

    #JTJ[idiag] = undampled_JTJ_diag #restore diagonal
    mu, nu, norm_f, f[:], spow, rawJTJ = best_x_state

    global_f = _np.empty(ari.global_num_elements(), 'd')
    ari.allgather_f(f, global_f)

    return global_x, converged, msg, mu, nu, norm_f, global_f, rawJTJ

