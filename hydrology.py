import numpy as np


def cn_table(cls='forest'):
    """
    values of CN according to soil type (A, B, C, D). Current source: USDA, 1986
    :param cls:
    :return:
    """
    # order: A, B, C, D
    cn_tbl = {'urban': (77, 85, 90, 92),
              'water': (100, 100, 100, 100),
              'forest': (30, 55, 70, 77),
              'pasture': (68, 79, 86, 89),
              'crops': (72, 81, 88, 91),
              'nbs_forest': (36, 60, 73, 79),
              'nbs_pasture': (39, 61, 74, 80),
              'nbs_crops': (62, 71, 78, 81)}
    return np.array(cn_tbl[cls])


def find_cn(lulc, soils):
    """

    :param lulc: tuple of lulc classes weights (can be anything: percent or area)
    :param soils: tuple of lulc classes soils weights np.arrays (can be anything: percent or area)
    :return: average CN float number
    """
    lulc_w = np.array(lulc)
    if np.sum(lulc_w) == 0:  # avoiding division by zero
        lulc_w = lulc_w + 1
    #
    urban_cn = np.sum(cn_table('urban') * soils[0] / np.sum(soils[0]))
    water_cn = np.sum(cn_table('water') * soils[1] / np.sum(soils[1]))
    forest_cn = np.sum(cn_table('forest') * soils[2] / np.sum(soils[2]))
    pasture_cn = np.sum(cn_table('pasture') * soils[3] / np.sum(soils[3]))
    crops_cn = np.sum(cn_table('crops') * soils[4] / np.sum(soils[4]))
    nbs_forest_cn = np.sum(cn_table('nbs_forest') * soils[5] / np.sum(soils[5]))
    nbs_pasture_cn = np.sum(cn_table('nbs_pasture') * soils[6] / np.sum(soils[6]))
    nbs_crops_cn = np.sum(cn_table('nbs_crops') * soils[7] / np.sum(soils[7]))
    #
    lulc_cn = np.array((urban_cn, water_cn, forest_cn, pasture_cn, crops_cn,
                        nbs_forest_cn, nbs_pasture_cn, nbs_crops_cn))
    #
    cn = np.sum(lulc_w * lulc_cn / np.sum(lulc_w))
    return round(cn, 2)


def find_cns(lulc, soils):
    lulc_w = list()
    for i in range(0, len(lulc)):
        aux_array = np.array(lulc) * 0
        if lulc[i] == 0:
            aux_array[i] = 1
        else:
            aux_array[i] = lulc[i]
        lulc_w.append(aux_array)
    cns = list()
    for i in range(0, len(lulc)):
        aux_flt = find_cn(lulc_w[i], soils)
        cns.append(aux_flt)
    return cns


def find_rzdf(lulc):
    """
    Finds the averaged root zone depth
    :param lulc: list of lulc classes weights or areas
    :return: float average root zone depth
    """
    lulc_w = np.array(lulc)
    # this is the following assumption based on the Kc Method of FAO
    rzdf_a = np.array((0, 0, 1, 0.1, 0.05, 0.5, 0.1, 0.05))
    rzdf = np.sum(lulc_w * rzdf_a / np.sum(lulc_w))
    return round(rzdf, 3)


def find_rzdf_hru(lulc):
    """
    Finds the averaged root zone depth
    :param lulc: list of lulc classes weights or areas
    :return: float average root zone depth
    """
    lulc_w = np.array(lulc)
    #
    rzdf_a = np.array((0, 0, 1, 0.1, 0.05, 0.5, 0.1, 0.05))
    rzdf = np.sum(lulc_w * rzdf_a / np.sum(lulc_w))
    return round(rzdf, 3)


def find_nse(qobs, qsim, type='lin'):
    """
    Nash-Sutcliffe efficiency of 2 arrays of same length
    :param qobs: observed array
    :param qsim: simulated array
    :param type: 'log' for NSElog10
    :return: float number of NSE
    """
    qavg = qobs * 0.0 + np.mean(qsim)
    if type == 'log':
        qobs = np.log10(qobs)
        qsim = np.log10(qsim)
        qavg = np.log10(qavg)
    nse = 1 - (np.sum(np.power(qobs - qsim, 2))/ np.sum((qobs - qavg)))
    return nse


def find_pbias(qobs, qsim):
    '''
    Percent bias coefficient (PBIAS)
    :param qobs:
    :param qsim:
    :return:
    '''
    pbias = 100 * np.sum(qobs - qsim) / np.sum(qobs)
    return pbias


def find_rmse(qobs, qsim, type='lin'):
    """
    Root of mean squared error of 2 arrays of same length
    :param qobs: observed array
    :param qsim: simulated array
    :param type: log' for RMSElog10
    :return: float
    """
    if type == 'log':
        qobs = np.log10(qobs)
        qsim = np.log10(qsim)
    rmse = np.sqrt(np.mean(np.power(qobs - qsim, 2)))
    return rmse


def find_cfc(a):
    """

    :param a: array
    :return: tuple with exeedance probability (%) and CFC values from input array
    """
    ptles = np.arange(0, 101, 1)
    cfc = np.percentile(a, ptles)
    exeed = 100 - ptles
    return (exeed, cfc)


def calib4(area, qobs, p, pet, cn, rzdf, nnash, ranges, segf=100, size=10, tui=True):
    import time
    from tools import stringsf
    #
    def get_climb4_lst():
        climb_lst = list()
        for i in range(-1, 2):
            for j  in range(-1, 2):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        lcl = np.array((i, j, k, l))
                        # print(lcl)
                        climb_lst.append(lcl)
        return climb_lst
    #
    # get current time:
    dp_t0 = time.time()
    #
    # get step list
    step_lst = get_climb4_lst()
    print(len(step_lst))
    #
    # get deltas
    iaf_delta = (ranges[0][1] - ranges[0][0]) / segf
    swmax_delta = (ranges[1][1] - ranges[1][0]) / segf
    gwmax_delta = (ranges[2][1] - ranges[2][0]) / segf
    knash_delta = (ranges[3][1] - ranges[3][0]) / segf
    #
    # get delta array
    deltas = np.array((iaf_delta, swmax_delta, gwmax_delta, knash_delta))
    #
    # get lower bound array
    lower_bound = np.array((ranges[0][0], ranges[1][0], ranges[2][0], ranges[3][0]))
    # get upper bound array
    upper_bound = np.array((ranges[0][1], ranges[1][1], ranges[2][1], ranges[3][1]))
    #
    # create lists to store plotting data
    x_iaf_lst = list()
    y_swmax_lst = list()
    z_gwmax_lst = list()
    w_knash_lst = list()
    m_lst = list()
    #
    # create list to store states and metrics
    chosen_states = list()
    chosen_metrics = list()
    #
    # Get CFC obs:
    cfc_obs = find_cfc(qobs)
    #
    # random walks loop:
    for walk in range(0, size):
        # reset random state using time
        now = int(stringsf.now()[-6:])
        np.random.seed(now)
        # get a starting point
        seed = np.random.randint(0, segf, 4)
        current_state =  (seed * deltas) + lower_bound
        # run model:
        run = run_hydro(area, p, pet, cn, rzdf, current_state[0], current_state[1],
                        current_state[2], current_state[3], nnash, export='none')
        qsim = run['Q'] + 0.001
        # compute CFC sim
        cfc_sim = find_cfc(qsim)
        # current_metric = np.sum(current_state)  # get metrics
        current_metric = find_rmse(cfc_obs[1][1:-1], cfc_sim[1][1:-1], 'log')  # get metrics
        if tui:
            print('\nWalk # {}'.format(walk + 1))
            print('Starting point in hyperspace: {:6.3f}  {:6.3f}  {:6.3f}  {:6.3f}'
                  '\t\tMetric: {:6.3f}'.format(current_state[0], current_state[1], current_state[2], current_state[3],
                                               current_metric))
        counter = 0
        while True:
            # to get out the loop only if all possibilities were exausted
            if counter == len(step_lst):
                # append
                chosen_states.append(current_state)
                chosen_metrics.append(current_metric)
                if tui:
                    print('End of local walk')
                break
            # compute sample state
            sample_state = current_state + (step_lst[counter] * deltas)
            # check if state inside search hyperspace:
            check = np.prod((sample_state  >= lower_bound) * (sample_state <= upper_bound))
            if check == 1:
                #
                # un model:
                run = run_hydro(area, p, pet, cn, rzdf, sample_state[0], sample_state[1],
                                sample_state[2], sample_state[3], nnash, export='none')
                qsim = run['Q'] + 0.001
                # compute CFC sim
                cfc_sim = find_cfc(qsim)
                # current_metric = np.sum(current_state)  # get metrics
                sample_metric = find_rmse(cfc_obs[1][1:-1], cfc_sim[1][1:-1], 'log')  # get metrics
                #
                # if best, reset search
                if sample_metric < current_metric:
                    # store data:
                    x_iaf_lst.append(sample_state[0])
                    y_swmax_lst.append(sample_state[1])
                    z_gwmax_lst.append(sample_state[2])
                    w_knash_lst.append(sample_state[3])
                    m_lst.append(sample_metric)
                    #
                    current_metric = sample_metric  # update metric
                    current_state = sample_state  # updade state
                    # reset step list:
                    step_lst = step_lst[counter:] + step_lst[:counter]
                    aux_flt = time.time() - dp_t0
                    if tui:
                        print('Walk {} of {}'.format(walk + 1, size), end='\t\t')
                        print('Sample state: {:8.3f}  '
                              '{:8.3f}  {:8.3f}  {:8.3f}'.format(current_state[0], current_state[1], current_state[2],
                                                           current_state[3]), end='\t')
                        print('Metric: {:<10.4f}'.format(sample_metric), end='\t\t')
                        print('Elapsed time: {:8.2f} s'.format(aux_flt))
                    # reset counter:
                    counter = 0
                else:
                    # keep searching in local list
                    counter = counter + 1
            else:
                # keep searching in local list
                counter = counter + 1
    # find best metric of all walks:
    best_metric = min(chosen_metrics)
    # retrieve from lists:
    best_metric_id = chosen_metrics.index(best_metric)
    best_state = chosen_states[best_metric_id]
    #
    #
    # finally, run model, get all other metrics and stuff:
    series = run_hydro(area, p, pet, cn, rzdf, best_state[0], best_state[1],
                       best_state[2], best_state[3], nnash, export='full')
    qsim = series['Q'] + 0.001
    # compute CFC sim
    cfc_sim = find_cfc(qsim)
    # nse:
    nse = find_nse(qobs, qsim)
    nselog = find_nse(qobs, qsim, 'log')
    # pbias:
    pbias = find_pbias(qobs, qsim)
    # rmse:
    rmse = find_rmse(qobs, qsim)
    # rmselog:
    rmselog = find_rmse(qobs, qsim, 'log')
    # r:
    r = np.corrcoef(qobs, qsim)[0, 1]
    # rmse_cfc:
    rmse_cfc = find_rmse(cfc_obs[1][1:-1], cfc_sim[1][1:-1])
    # rmse_cfc_log:
    rmselog_cfc = find_rmse(cfc_obs[1][1:-1], cfc_sim[1][1:-1], 'log')
    # r cfc:
    r_cfc = np.corrcoef(cfc_obs[1][1:-1], cfc_sim[1][1:-1])[0, 1]
    #
    #
    # output dict:
    calibp = {'Iaf':best_state[0], 'Swmax':best_state[1], 'Gwmax': best_state[2],
              'Knash':best_state[3], 'Metric': best_metric}
    metrics = {'R':r, 'RMSE':rmse, 'RMSELOG':rmselog, 'NSE':nse, 'NSELOG':nselog, 'PBias':pbias, 'RMSE_CFC':rmse_cfc,
               'RMSELOG_CFC':rmselog_cfc, 'R_CFC':r_cfc}
    cloud = {'x': np.array(x_iaf_lst), 'y': np.array(y_swmax_lst), 'z': np.array(z_gwmax_lst),
             'w': np.array(w_knash_lst), 'm': np.array(m_lst)}
    series['Qobs'] = qobs  # add to it the new series

    curves = {'CFCobs': cfc_obs[1][1:-1], 'CFCsim': cfc_sim[1][1:-1], 'Exeed':cfc_sim[0][1:-1]}

    return calibp, metrics, cloud, series, curves


def run_hydro(area, p, pet, cn, rzdf, iaf, swmax, gwmax, knash, nnash, export='full'):
    """
    run the simulation model
    :param area: area in km2
    :param p: daily time series of precipitation in mm
    :param pet: daily time series of PET in mm
    :param cn: SCS CN value computed from LULC and Soil types
    :param rdzf: float
    :param iaf: float
    :param swmax: float
    :param gwmax: float
    :param knash: float
    :param nnash: int
    :return: dict of all simulation results
    """
    from scipy.ndimage import gaussian_filter

    def find_roff(pia, p):
        r = 0.0
        if p > pia:
            r = p - pia
        else:
            r = 0.0
        return r

    def find_ev(pet1, sfw1):
        if sfw1 < pet1:
            ev = sfw1
        else:
            ev = pet1
        return ev

    def find_inf(pinf, sfw2):
        if sfw2 < pinf:
            inf = sfw2
        else:
            inf = pinf
        return inf

    def find_ptp(sw1, swmax, rzd):
        if sw1 > swmax - rzd:
            ptp = sw1 - (swmax - rzd)
        else:
            ptp = 0.0
        return ptp

    def find_tp(pet2, ptp):
        if pet2 < ptp:
            tp = pet2
        else:
            tp = ptp
        return tp

    def find_gw(gwmax, swmax, sw2):
        gw = gwmax * sw2 / swmax
        return round(gw, 4)

    def find_qb(gw, area):
        qb = gw * area * 1000 / 86400
        return qb

    # get iamax:
    iamax = iaf * ((25400 / cn) - 254)
    # get rzd:
    rzd = rzdf * swmax
    # get steps array
    stp = np.arange(1, len(p) + 1, 1)
    # parameters array:
    iamax_a = (stp * 0.0) + iamax
    swmax_a = (stp * 0.0) + swmax
    rzd_a = (stp * 0.0) + rzd
    # generate flow variables array
    q = stp * 0.0
    qb = stp * 0.0
    qs = stp * 0.0
    inf = stp * 0.0
    ev = stp * 0.0
    tp = stp * 0.0
    gw = stp * 0.0
    roff = stp * 0.0
    # generate stock variables array
    sfw = stp * 0.0
    sw = stp * 0.0
    et = stp * 0.0
    vnash = np.zeros((len(stp), int(nnash)))  # nash cascade array
    # aux arrays:
    sfw1 = stp * 0.0
    sfw2 = stp * 0.0
    sw1 = stp * 0.0
    sw2 = stp * 0.0
    pet1 = stp * 0.0
    pet2 = stp * 0.0
    pet3 = stp * 0.0
    pia = stp * 0.0
    pinf = stp * 0.0
    ptp = stp * 0.0
    #
    # land phase loop:
    for t in range(1, len(stp)):
        t0 = t - 1
        # surface water balance:
        # first, discount runoff:
        pia[t0] = iamax_a[t0] - sfw[t0]  # available stock in surface
        roff[t0] = find_roff(pia[t0], p[t0])
        sfw1[t0] = sfw[t0] + p[t0] - roff[t0]
        # second, discount infiltration:
        pinf[t0] = swmax_a[t0] - sw[t0]  # available stock in subsoil
        inf[t0] = find_inf(pinf[t0], sfw1[t0])
        sfw2[t0] = sfw1[t0] - inf[t0]
        # last, discount evaporation:
        pet1[t0] = pet[t0]  # available stock in atmosphere
        ev[t0] = find_ev(pet1[t0], sfw2[t0])
        pet2[t0] = pet1[t0] - ev[t0]  # remaining available stock in atmosphere
        #
        # update surface water stock
        sfw[t] = sfw2[t0] - ev[t0]
        #
        # subsurface water balance
        # first include infiltration
        sw1[t0] = sw[t0] + inf[t0]
        # second, discount transpiration
        ptp[t0] = find_ptp(sw1[t0], swmax_a[t0], rzd)
        tp[t0] = find_tp(pet2[t0], ptp[t0])
        sw2[t0] = sw1[t0] - tp[t0]
        pet3[t0] = pet2[t0] - tp[t0]  # remaining available stock in atmosphere
        et[t0] = ev[t0] + tp[t0]  # real ET
        # last, discount growndwater flow
        gw[t0] = find_gw(gwmax, swmax, sw2[t0])
        #
        # update sw:
        sw[t] = sw2[t0] - gw[t0]
    #
    # apply gaussian filter to smooth baseflow:
    qb = gw * area * 1000 / 86400  # convert to discharge
    qb = gaussian_filter(qb, 1)  # gaussian filter
    #
    # Channel transport phase:
    vroff = roff * area * 1000
    for t in range(1, len(stp)):
        t0 = t - 1
        vin = vroff[t0]
        # loop across Nash Cascade:
        for v in range(0, len(vnash[t0])):
            # validate volumes to prevent numeric overflow:
            minvalue = 0.00001
            if vnash[t0][v] <= minvalue:
                vnash[t0][v] = minvalue
            if vnash[t0][v - 1] <= minvalue:
                vnash[t0][v - 1] = minvalue
            if v == 0:
                vnash[t][v] = vnash[t0][v] + vin - (vnash[t0][v] / knash)
            else:
                vnash[t][v] = vnash[t0][v] + (vnash[t0][v - 1] / knash) - (vnash[t0][v] / knash)
        vout = vnash[t0][nnash - 1] / knash  # extract outflow from last bucket
        qs[t0] = vout / 86400
    #
    # Sum stream flow:
    q = qb + qs
    #
    # export dictionay:
    if export == 'full':
        out = {'Step': stp, 'Iafmax':iamax_a, 'Swmax':swmax_a, 'Rzd':rzd_a,
               'P': p, 'PET': pet, 'Q': q, 'Qb': qb, 'Qs': qs,
               'Sfw': sfw, 'Sfw1': sfw1, 'Sfw2': sfw2,
               'Sw':sw, 'Ev': ev, 'Tp': tp, 'ET':et}
    else:
        out = {'Step': stp, 'Q': q,}
    return out


def load_hydro_data(qobsf, lulcf, soilsf, paramf, full=False, extent=600):
    """

    :param qobsf: observed timeseries file path string (qobs, p and pet, in mm)
    :param lulcf: lulc areas file path string
    :param soilsf: soils distribution file path string
    :param paramf: parameters file path string
    :param full: boolean control for full load of timeseries (True = load all the timeseries)
    :param extent: int
    :return: dict of all results
    """
    import pandas as pd
    if full:
        extent = -1
    # Observed flows
    q_file = qobsf
    df = pd.read_csv(q_file, sep=';')
    dates = tuple(df.T.values[0][:extent])
    q = np.array(tuple(df.T.values[1][:extent]))
    p = np.array(tuple(df.T.values[2][:extent]))
    pet = np.array(tuple(df.T.values[3][:extent]))
    # LULC
    lulc_file = lulcf
    df = pd.read_csv(lulc_file, sep=';')
    lulcA = tuple(df.T.values[1])
    lulc_w = list()
    # Soils
    soils_file = soilsf
    df = pd.read_csv(soils_file, sep=';')
    soils = (df.values[0][1:], df.values[1][1:],
             df.values[2][1:], df.values[3][1:],
             df.values[4][1:], df.values[5][1:],
             df.values[6][1:], df.values[7][1:])
    # area:
    area = sum(lulcA)
    # CN
    cn = find_cn(lulcA, soils)  # averaged
    # Rzdf
    rzdf = find_rzdf(lulcA)
    # hard param
    obs_file = paramf
    df = pd.read_csv(obs_file, sep=';')
    aux_tpl = tuple(df.T.values[1])
    iaf = aux_tpl[3]
    swmax = aux_tpl[4]
    gwmax = aux_tpl[5]
    knash = aux_tpl[6]
    nnash = aux_tpl[7]
    out = {'Dates': dates, 'Qobs': q, 'P': p, 'PET': pet, 'LULC': lulcA, 'Soils': soils,
           'Area': area, 'CN': cn, 'Rzdf': rzdf, 'Iaf': iaf, 'Swmax': swmax,
           'Gwmax': gwmax, 'Knash': knash, 'Nnash': int(nnash)}
    return out


def calib4_hru(area, qobs, p, pet, lulc, cns, nnash, ranges, segf=100, size=10, tui=True):
    import time
    from tools import stringsf
    #
    def get_climb4_lst():
        climb_lst = list()
        for i in range(-1, 2):
            for j  in range(-1, 2):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        lcl = np.array((i, j, k, l))
                        # print(lcl)
                        climb_lst.append(lcl)
        return climb_lst
    #
    # get current time:
    dp_t0 = time.time()
    #
    # get step list
    step_lst = get_climb4_lst()
    # print(len(step_lst))
    #
    # get deltas
    iaf_delta = (ranges[0][1] - ranges[0][0]) / segf
    swmax_delta = (ranges[1][1] - ranges[1][0]) / segf
    gwmax_delta = (ranges[2][1] - ranges[2][0]) / segf
    knash_delta = (ranges[3][1] - ranges[3][0]) / segf
    #
    # get delta array
    deltas = np.array((iaf_delta, swmax_delta, gwmax_delta, knash_delta))
    #
    # get lower bound array
    lower_bound = np.array((ranges[0][0], ranges[1][0], ranges[2][0], ranges[3][0]))
    # get upper bound array
    upper_bound = np.array((ranges[0][1], ranges[1][1], ranges[2][1], ranges[3][1]))
    #
    # create lists to store plotting data
    x_iaf_lst = list()
    y_swmax_lst = list()
    z_gwmax_lst = list()
    w_knash_lst = list()
    m_lst = list()
    #
    # create list to store states and metrics
    chosen_states = list()
    chosen_metrics = list()
    #
    # Get CFC obs:
    cfc_obs = find_cfc(qobs)
    #
    # random walks loop:
    for walk in range(0, size):
        # reset random state using time
        now = int(stringsf.now()[-6:])
        np.random.seed(now)
        # get a starting point
        seed = np.random.randint(0, segf, 4)
        current_state =  (seed * deltas) + lower_bound
        #
        # run model:
        run = run_hydro_hru(area, p, pet, lulc, cns, current_state[0], current_state[1],
                        current_state[2], current_state[3], nnash, export='none')
        qsim = run['Q'] + 0.001
        # compute CFC sim
        cfc_sim = find_cfc(qsim)
        # current_metric = np.sum(current_state)  # get metrics
        current_metric = find_rmse(cfc_obs[1][1:-1], cfc_sim[1][1:-1], 'log')  # get metrics
        if tui:
            print('\nWalk # {}'.format(walk + 1))
            print('Starting point in hyperspace: {:6.3f}  {:6.3f}  {:6.3f}  {:6.3f}'
                  '\t\tMetric: {:6.3f}'.format(current_state[0], current_state[1], current_state[2], current_state[3],
                                               current_metric))
        counter = 0
        while True:
            # to get out the loop only if all possibilities were exausted
            if counter == len(step_lst):
                # append
                chosen_states.append(current_state)
                chosen_metrics.append(current_metric)
                if tui:
                    print('End of local walk')
                break
            # compute sample state
            sample_state = current_state + (step_lst[counter] * deltas)
            # check if state inside search hyperspace:
            check = np.prod((sample_state  >= lower_bound) * (sample_state <= upper_bound))
            if check == 1:
                #
                # run model:
                run = run_hydro_hru(area, p, pet, lulc, cns, sample_state[0], sample_state[1],
                                    sample_state[2], sample_state[3], nnash, export='none')
                qsim = run['Q'] + 0.001
                # compute CFC sim
                cfc_sim = find_cfc(qsim)
                # current_metric = np.sum(current_state)  # get metrics
                sample_metric = find_rmse(cfc_obs[1][1:-1], cfc_sim[1][1:-1], 'log')  # get metrics
                #
                # if best, reset search
                if sample_metric < current_metric:
                    # store data:
                    x_iaf_lst.append(sample_state[0])
                    y_swmax_lst.append(sample_state[1])
                    z_gwmax_lst.append(sample_state[2])
                    w_knash_lst.append(sample_state[3])
                    m_lst.append(sample_metric)
                    #
                    current_metric = sample_metric  # update metric
                    current_state = sample_state  # updade state
                    # reset step list:
                    step_lst = step_lst[counter:] + step_lst[:counter]
                    aux_flt = time.time() - dp_t0
                    if tui:
                        print('Walk {} of {}'.format(walk + 1, size), end='\t\t')
                        print('Sample state: {:8.3f}  '
                              '{:8.3f}  {:8.3f}  {:8.3f}'.format(current_state[0], current_state[1], current_state[2],
                                                           current_state[3]), end='\t')
                        print('Metric: {:<10.4f}'.format(sample_metric), end='\t\t')
                        print('Elapsed time: {:8.2f} s'.format(aux_flt))
                    # reset counter:
                    counter = 0
                else:
                    # keep searching in local list
                    counter = counter + 1
            else:
                # keep searching in local list
                counter = counter + 1
    # find best metric of all walks:
    best_metric = min(chosen_metrics)
    # retrieve from lists:
    best_metric_id = chosen_metrics.index(best_metric)
    best_state = chosen_states[best_metric_id]
    #
    #
    # finally, run model, get all other metrics and stuff:
    series = run_hydro_hru(area, p, pet, lulc, cns, sample_state[0], sample_state[1],
                           sample_state[2], sample_state[3], nnash, export='full')
    qsim = series['Q'] + 0.001
    # compute CFC sim
    cfc_sim = find_cfc(qsim)
    # nse:
    nse = find_nse(qobs, qsim)
    nselog = find_nse(qobs, qsim, 'log')
    # pbias:
    pbias = find_pbias(qobs, qsim)
    # rmse:
    rmse = find_rmse(qobs, qsim)
    # rmselog:
    rmselog = find_rmse(qobs, qsim, 'log')
    # r:
    r = np.corrcoef(qobs, qsim)[0, 1]
    # rmse_cfc:
    rmse_cfc = find_rmse(cfc_obs[1][1:-1], cfc_sim[1][1:-1])
    # rmse_cfc_log:
    rmselog_cfc = find_rmse(cfc_obs[1][1:-1], cfc_sim[1][1:-1], 'log')
    # r cfc:
    r_cfc = np.corrcoef(cfc_obs[1][1:-1], cfc_sim[1][1:-1])[0, 1]
    #
    #
    # output dict:
    calibp = {'Iaf':best_state[0], 'Swmax':best_state[1], 'Gwmax': best_state[2],
              'Knash':best_state[3], 'Metric': best_metric}
    metrics = {'R':r, 'RMSE':rmse, 'RMSELOG':rmselog, 'NSE':nse, 'NSELOG':nselog, 'PBias':pbias, 'RMSE_CFC':rmse_cfc,
               'RMSELOG_CFC':rmselog_cfc, 'R_CFC':r_cfc}
    cloud = {'x': np.array(x_iaf_lst), 'y': np.array(y_swmax_lst), 'z': np.array(z_gwmax_lst),
             'w': np.array(w_knash_lst), 'm': np.array(m_lst)}
    series['Qobs'] = qobs  # add to it the new series

    curves = {'CFCobs': cfc_obs[1][1:-1], 'CFCsim': cfc_sim[1][1:-1], 'Exeed':cfc_sim[0][1:-1]}

    return calibp, metrics, cloud, series, curves


def run_hydro_hru(area, p, pet, lulc, cns, iaf, swmax, gwmax, knash, nnash, export='full'):
    """
    run the simulation model using land use and land cover classes as hydrologic response units
    :param area: total area in sq km
    :param p: daily time series of precipitation in mm
    :param pet: daily time series of PET in mm
    :param lulc: list of lulc classes areas or ratios for weighting
    :param cns: list of SCS CN values computed from LULC and Soil types for each LULC classes
    :param iaf: float
    :param swmax: float
    :param gwmax: float
    :param knash: float
    :param nnash: int
    :return: dict of all simulation results
    """
    from scipy.ndimage import gaussian_filter

    def find_roff(pia, p):
        r = 0.0
        if p > pia:
            r = p - pia
        else:
            r = 0.0
        return r

    def find_ev(pet1, sfw2):
        if sfw2 < pet1:
            ev = sfw2
        else:
            ev = pet1
        return ev

    def find_inf(pinf, sfw1):
        if sfw1 < pinf:
            inf = sfw1
        else:
            inf = pinf
        return inf

    def find_ptp(sw1, swmax, rzd):
        if sw1 > swmax - rzd:
            ptp = sw1 - (swmax - rzd)
        else:
            ptp = 0.0
        return ptp

    def find_tp(pet2, ptp):
        if pet2 < ptp:
            tp = pet2
        else:
            tp = ptp
        return tp

    def find_gw(gwmax, swmax, sw2):
        gw = gwmax * sw2 / swmax
        return round(gw, 4)

    # areas list:
    areas = lulc
    areas_bol = np.array(lulc) > 0
    # weighting factor array:
    areasf = np.array(areas)/np.sum(np.array(areas))
    #print(areasf)
    #
    # VERY CRITICAL MODEL ASSUMPTIONS:
    # get iamax HRU array:
    iamax = iaf * ((25400 / np.array(cns)) - 254)  # from the SCS method
    #
    # get rzd HRU array:
    rzd = (iamax * (iamax <= swmax)) + (swmax * (iamax > swmax))  # rzd = iamax ->> the symmetry principle
    #
    #
    # get steps array
    stp = np.arange(1, len(p) + 1, 1)
    # generate flow variables arrays
    q = stp * 0.0
    qs = stp * 0.0
    qb = stp * 0.0
    roff_full = stp * 0.0
    inf_full = stp * 0.0
    gw_full = stp * 0.0
    ev_full = stp * 0.0
    tp_full = stp * 0.0
    et_full = stp * 0.0
    #
    # HRU flow variables list of arrays:
    inf = [stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0]
    ev = [stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0]
    tp = [stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0]
    et = [stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0]
    gw = [stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0]
    roff = [stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0]
    # generate HRU stock variables arrays
    sfw = [stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0]
    sw = [stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0, stp * 0.0]
    sfw_avg = stp * 0.0
    sw_avg = stp * 0.0
    rzd_avg = np.sum(rzd * areasf) + stp * 0.0
    iamax_avg = np.sum(iamax * areasf) + stp * 0.0
    swmax_avg = np.sum(swmax * areasf) + stp * 0.0
    cn_avg = np.sum(np.array(cns) * areasf) + stp * 0.0
    #
    # nash cascade array
    vnash = np.zeros((len(stp), int(nnash)))
    #
    #
    # HRU loop:
    hru_lbl = ['urban', 'water', 'forest', 'pasture', 'crops', 'nbsf', 'nbsp', 'nbsc']
    for u in range(0, len(hru_lbl)):
        # print('\nHRU:' + hru_lbl[u], end=' Index: ')
        # print(u)
        # reset aux arrays:
        sfw1 = stp * 0.0
        sfw2 = stp * 0.0
        sw1 = stp * 0.0
        sw2 = stp * 0.0
        pet1 = stp * 0.0
        pet2 = stp * 0.0
        pet3 = stp * 0.0
        pia = stp * 0.0
        pinf = stp * 0.0
        ptp = stp * 0.0
        #
        # land phase loop for each HRU:
        for t in range(1, len(stp)):
            t0 = t - 1
            pu = p[t0] * areas_bol[u]
            # print()
            # print('P: {}'.format(pu))
            # surface water balance:
            #
            # first, discount runoff:
            pia[t0] = iamax[u] - sfw[u][t0]  # available stock in surface
            roff[u][t0] = find_roff(pia[t0], pu)
            sfw1[t0] = sfw[u][t0] + pu - roff[u][t0]
            # print('IAmax: {:.2f}\tPIA: {:.2f}'.format(iamax[u], pia[t0]))
            # print('Runoff: {:.2f}'.format(roff[u][t0]))
            # print('Sfw1: {:.2f}'.format(sfw1[t0]))

            # second, discount infiltration:
            pinf[t0] = swmax - sw[u][t0]  # available stock in subsoil
            inf[u][t0] = find_inf(pinf[t0], sfw1[t0])
            sfw2[t0] = sfw1[t0] - inf[u][t0]
            # print('SWmax: {:.2f}\tSW: {:.2f}\tPinf: {:.2f}'.format(swmax, sw[u][t0], pinf[t0]))
            # print('Inf: {:.2f}'.format(inf[u][t0]))
            # print('Sfw2: {:.2f}'.format(sfw2[t0]))

            # last, discount evaporation:
            pet1[t0] = pet[t0]  # available stock in atmosphere
            ev[u][t0] = find_ev(pet1[t0], sfw2[t0])
            pet2[t0] = pet1[t0] - ev[u][t0]  # remaining available stock in atmosphere
            # print('PET1: {:.2f}'.format(pet1[t0]))
            # print('EV: {:.2f}'.format(ev[u][t0]))
            # print('PET2: {:.2f}'.format(pet2[t0]))
            #
            # update surface water stock
            sfw[u][t] = sfw2[t0] - ev[u][t0]
            # print('Sfw: {:.2f}'.format(sfw[u][t]))
            #
            # subsurface water balance
            #
            # first include infiltration
            sw1[t0] = sw[u][t0] + inf[u][t0]
            # second, discount transpiration
            ptp[t0] = find_ptp(sw1[t0], swmax, rzd[u])
            tp[u][t0] = find_tp(pet2[t0], ptp[t0])
            sw2[t0] = sw1[t0] - tp[u][t0]
            pet3[t0] = pet2[t0] - tp[u][t0]  # remaining available stock in atmosphere
            et[u][t0] = ev[u][t0] + tp[u][t0]  # real ET
            # last, discount growndwater flow
            gw[u][t0] = find_gw(gwmax, swmax, sw2[t0])
            #
            # update sw:
            sw[u][t] = sw2[t0] - gw[u][t0]
            #print('{}\t\t{}\t\t{}'.format(p[t0], sfw[u][t0], sw[u][t0]))
        #
        # print(roff[u])
    #
    # Aggregate off-land flow variables:
    for u in range(len(hru_lbl)):
        roff_full = roff_full + roff[u] * areasf[u]
        inf_full = inf_full + inf[u] * areasf[u]
        ev_full = ev_full + ev[u] * areasf[u]
        tp_full = tp_full + tp[u] * areasf[u]
        et_full = et_full + et[u] * areasf[u]
        gw_full = gw_full + gw[u] * areasf[u]
        sfw_avg = sfw_avg + sfw[u] * areasf[u]
        sw_avg = sw_avg + sw[u] * areasf[u]
    #
    #
    # apply gaussian filter to smooth baseflow:
    qb = gw_full * area * 1000 / 86400  # convert to discharge
    qb = gaussian_filter(qb, 1)  # gaussian filter to smooth (this may be removed)
    # Channel transport phase:
    # convert runoff to volume:
    vroff = roff_full * area * 1000  # convert to volume
    for t in range(1, len(stp)):
        t0 = t - 1
        vin = vroff[t0]
        # loop across Nash Cascade:
        for v in range(0, len(vnash[t0])):
            # validate volumes to prevent numeric overflow:
            minvalue = 0.00001
            if vnash[t0][v] <= minvalue:
                vnash[t0][v] = minvalue
            if vnash[t0][v - 1] <= minvalue:
                vnash[t0][v - 1] = minvalue
            if v == 0:
                vnash[t][v] = vnash[t0][v] + vin - (vnash[t0][v] / knash)
            else:
                vnash[t][v] = vnash[t0][v] + (vnash[t0][v - 1] / knash) - (vnash[t0][v] / knash)
        vout = vnash[t0][nnash - 1] / knash  # extract outflow from last bucket
        qs[t0] = vout / 86400
    #
    #
    # Sum stream flow:
    q = qb + qs
    #
    # export dictionay:
    if export == 'full':
        out = {'Step': stp, 'P': p, 'PET': pet, 'Q': q, 'Qb': qb, 'Qs': qs, 'Sw': sw_avg, 'Sfw': sfw_avg,
               'Ev': ev_full, 'Tp': tp_full, 'ET':et_full, 'Gw': gw_full, 'Roff': roff_full, 'Inf': inf_full,
               'Iamax': iamax_avg, 'Swmax': swmax_avg, 'Rzd': rzd_avg, 'CN': cn_avg,
               'Sfw_urban': sfw[0], 'Sfw_water':sfw[1], 'Sfw_forest':sfw[2], 'Sfw_pasture': sfw[3],
               'Sfw_crops': sfw[4], 'Sfw_nbsf': sfw[5], 'Sfw_nbsp': sfw[6], 'Sfw_nbsc': sfw[7],
               'Sw_urban': sw[0], 'Sw_water': sw[1], 'Sw_forest': sw[2], 'Sw_pasture': sw[3],
               'Sw_crops': sw[4], 'Sw_nbsf': sw[5], 'Sw_nbsp': sw[6], 'Sw_nbsc': sw[7],
               'R_urban': roff[0], 'R_water': roff[1], 'R_forest': roff[2], 'R_pasture': roff[3],
               'R_crops': roff[4], 'R_nbsf': roff[5], 'R_nbsp': roff[6], 'R_nbsc': roff[7],
               'Inf_urban': inf[0], 'Inf_water': inf[1], 'Inf_forest': inf[2], 'Inf_pasture': inf[3],
               'Inf_crops': inf[4], 'Inf_nbsf': inf[5], 'Inf_nbsp': inf[6], 'Inf_nbsc': inf[7],
               'Gw_urban': gw[0], 'Gw_water': gw[1], 'Gw_forest': gw[2], 'Gw_pasture': gw[3],
               'Gw_crops': gw[4], 'Gw_nbsf': gw[5], 'Gw_nbsp': gw[6], 'Gw_nbsc': gw[7],
               'ET_urban': et[0], 'ET_water': et[1], 'ET_forest': et[2], 'ET_pasture': et[3],
               'ET_crops': et[4], 'ET_nbsf': et[5], 'ET_nbsp': et[6], 'ET_nbsc': et[7],
               'Ev_urban': ev[0], 'Ev_water': ev[1], 'Ev_forest': ev[2], 'Ev_pasture': ev[3],
               'Ev_crops': ev[4], 'Ev_nbsf': ev[5], 'Ev_nbsp': ev[6], 'Ev_nbsc': ev[7],
               'Tp_urban': tp[0], 'Tp_water': tp[1], 'Tp_forest': tp[2], 'Tp_pasture': tp[3],
               'Tp_crops': tp[4], 'Tp_nbsf': tp[5], 'Tp_nbsp': tp[6], 'Tp_nbsc': tp[7]
               }
    else:
        out = {'Step': stp, 'Q': q, 'Qb': qb, 'Rzd': rzd_avg, 'CN': cn_avg}
    return out


def load_hydro_data_hru(qobsf, lulcf, soilsf, paramf, full=False, extent=600):
    """
    Load data for the LULC-based HRU model
    :param qobsf: observed timeseries file path string (qobs, p and pet, in mm)
    :param lulcf: lulc areas file path string
    :param soilsf: soils distribution file path string
    :param paramf: parameters file path string
    :param full: boolean control for full load of timeseries (True = load all the timeseries)
    :param extent: int
    :return: dict of all results
    """
    import pandas as pd
    if full:
        extent = -1
    # Observed flows
    q_file = qobsf
    df = pd.read_csv(q_file, sep=';')
    dates = tuple(df.T.values[0][:extent])
    q = np.array(tuple(df.T.values[1][:extent]))
    p = np.array(tuple(df.T.values[2][:extent]))
    pet = np.array(tuple(df.T.values[3][:extent]))
    # LULC
    lulc_file = lulcf
    df = pd.read_csv(lulc_file, sep=';')
    lulcA = tuple(df.T.values[1])
    # Soils
    soils_file = soilsf
    df = pd.read_csv(soils_file, sep=';')
    soils = (df.values[0][1:], df.values[1][1:],
             df.values[2][1:], df.values[3][1:],
             df.values[4][1:], df.values[5][1:],
             df.values[6][1:], df.values[7][1:])
    # hard param
    obs_file = paramf
    df = pd.read_csv(obs_file, sep=';')
    aux_tpl = tuple(df.T.values[1])
    area = aux_tpl[0]
    iaf = aux_tpl[3]
    swmax = aux_tpl[4]
    gwmax = aux_tpl[5]
    knash = aux_tpl[6]
    nnash = aux_tpl[7]
    # CN
    cn = find_cn(lulcA, soils)  # averaged
    cns = find_cns(lulcA, soils)
    #out
    out = {'Dates': dates, 'Qobs': q, 'P': p, 'PET': pet, 'LULC': lulcA, 'Soils': soils,
           'Area': area, 'CNs': cns, 'CN': cn, 'Iaf': iaf, 'Swmax': swmax,
           'Gwmax': gwmax, 'Knash': knash, 'Nnash': int(nnash)}
    return out


def sal_hru(area, p, pet, lulc, cns, iaf, swmax, gwmax, knash, nnash):
    # lulc sensitivity scenarios:
    lulcf_tpl = ('lulc_ref', 'lulc_nbsf', 'lulc_nbsp', 'lulc_nbsc', 'lulc_d50', 'lulc_d90')
    lulc_ref = lulc
    lulc_nbsf = (lulc[0], lulc[1], lulc[2], 0.0, 0.0, lulc[3] + lulc[4], 0.0, 0.0)
    lulc_nbsp = (lulc[0], lulc[1], lulc[2], 0.0, 0.0, 0.0, lulc[3] + lulc[4], 0.0)
    lulc_nbsc = (lulc[0], lulc[1], lulc[2], 0.0, 0.0, 0.0, 0.0,  lulc[3] + lulc[4])
    lulc_d50 = (lulc[0], lulc[1], lulc[2]/2, lulc[3], lulc[4] + lulc[2]/2, 0.0, 0.0, 0.0)
    lulc_d90 = (lulc[0], lulc[1], lulc[2] * 0.1, lulc[3], lulc[4] + lulc[2] * 0.9, 0.0, 0.0, 0.0)
    sal_lulcs = (lulc_ref, lulc_nbsf, lulc_nbsp, lulc_nbsc, lulc_d50, lulc_d90)
    series_dct = dict()
    cfc_dct = dict()
    #
    for i in range(len(sal_lulcs)):
        # print(lulcf_tpl[i])
        run = run_hydro_hru(area, p, pet, sal_lulcs[i], cns, iaf, swmax, gwmax, knash, nnash)
        lcl_cfc_q = find_cfc(run['Q'])
        lcl_cfc_qs = find_cfc(run['Qs'])
        lcl_cfc_qb = find_cfc(run['Qb'])
        lcl_cfc_qbf = find_cfc(100 * run['Qb']/run['Q'])
        series_dct[lulcf_tpl[i] + '_Q'] = run['Q'][:]
        series_dct[lulcf_tpl[i] + '_Qs'] = run['Qs'][:]
        series_dct[lulcf_tpl[i] + '_Qb'] = run['Qb'][:]
        series_dct[lulcf_tpl[i] + '_ET'] = run['ET'][:]
        series_dct[lulcf_tpl[i] + '_Ev'] = run['Ev'][:]
        series_dct[lulcf_tpl[i] + '_Tp'] = run['Tp'][:]
        series_dct[lulcf_tpl[i] + '_Roff'] = run['Roff'][:]
        series_dct[lulcf_tpl[i] + '_Gw'] = run['Gw'][:]
        series_dct[lulcf_tpl[i] + '_Inf'] = run['Inf'][:]
        cfc_dct[lulcf_tpl[i] + '_' + 'Q'] = lcl_cfc_q[1][:]
        cfc_dct[lulcf_tpl[i] + '_' + 'Qb'] = lcl_cfc_qb[1][:]
        cfc_dct[lulcf_tpl[i] + '_' + 'Qs'] = lcl_cfc_qs[1][:]
        cfc_dct[lulcf_tpl[i] + '_' + 'Qbf'] = lcl_cfc_qbf[1][:]
        if i == 0:
            cfc_dct['Exeed'] = lcl_cfc_q[0][:]
    #
    return series_dct, cfc_dct

