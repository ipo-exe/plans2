import pandas as pd
import numpy as np
import random
from hydrology import run_hydro, run_hydro_hru, find_cfc, find_cn, find_cns, find_rzdf
from tools import stringsf


'''
develop: 


'''

def find_pv(p0, p1, p2):
    """

    :param p0: future value
    :param p1: number of years
    :param p2: yearly return rate in % (0 to 100)
    :return: present value
    """
    def_r = p2 / 100
    def_pv = p0 / ((1 + def_r)**p1)
    return round(def_pv, 2)


def find_xc(p0, p1, p2, p3, p4, p5, p6):
    """

    :param p0: LOCAL LULC tuple (w, u, f, p, c, nbsf, nbsp, nbsc)
    :param p1: watershed area in km2
    :param p2: cycle in years
    :param p3: operation data tuple
    :param p4: expansion set (nbsf, nbsp, nbsc)
    :param p5: available area in km2
    :param p6: installation data tuple
    :return:
    """
    # get data
    avail_area_ha = p5 * 100
    watershed_area_ha = p1 * 100
    cycle = p2
    # operation costs data
    oprt_nbsf_a = p3[0]
    oprt_nbsf_b = p3[1]
    oprt_nbsp_a = p3[2]
    oprt_nbsp_b = p3[3]
    oprt_nbsc_a = p3[4]
    oprt_nbsc_b = p3[5]
    oprt_nbsf_area = watershed_area_ha * p0[5] / 100
    oprt_nbsp_area = watershed_area_ha * p0[6] / 100
    oprt_nbsc_area = watershed_area_ha * p0[7] / 100
    # operation cost model xc_oprt = A * Area + B
    xc_oprt_nbsf = (oprt_nbsf_a * oprt_nbsf_area) + oprt_nbsf_b
    xc_oprt_nbsp = (oprt_nbsp_a * oprt_nbsp_area) + oprt_nbsp_b
    xc_oprt_nbsc = (oprt_nbsc_a * oprt_nbsc_area) + oprt_nbsc_b
    #
    xc_oprt = cycle * (xc_oprt_nbsf + xc_oprt_nbsp + xc_oprt_nbsc) * 0.1
    #
    # installation costs data
    inst_nbsf_a = p6[0]
    inst_nbsf_b = p6[1]
    inst_nbsp_a = p6[2]
    inst_nbsp_b = p6[3]
    inst_nbsc_a = p6[4]
    inst_nbsc_b = p6[5]
    inst_nbsf_area = avail_area_ha * p4[0] / 100
    inst_nbsp_area = avail_area_ha * p4[1] / 100
    inst_nbsc_area = avail_area_ha * p4[2] / 100
    # installation cost model xc_inst = A * Area + B
    xc_inst_nbsf = (inst_nbsf_a * inst_nbsf_area) + inst_nbsf_b
    xc_inst_nbsp = (inst_nbsp_a * inst_nbsp_area) + inst_nbsp_b
    xc_inst_nbsc = (inst_nbsc_a * inst_nbsc_area) + inst_nbsc_b
    #
    xc_inst = xc_inst_nbsf + xc_inst_nbsp + xc_inst_nbsc
    #
    xc = round(xc_oprt + xc_inst, 2)
    # xc = round(0.0 + xc_inst, 2)
    # print('>>>>> XC: {}'.format(xc))
    #
    return xc


def find_q(area, p, pet, lulc, soils, param):
    """

    :param p: p tuple
    :param pet: pet tuple
    :param lulc: %lulc tuple (u, w, f, p, c, nbsf, nbsp, nbsc)
    :param soils: (a, b, c, d) x (u, w, f, p, c, nbsf, nbsp, nbsc)
    :param param: (iaf, swmax, gwmax, knash, nnash)
    :return:
    """
    # run hydrology model and get stream flow
    # given lulc and soil, find CN
    cns = find_cns(lulc, soils)
    # print('CN: {}'.format(cn))
    ''' # given lulc, find rzdf
    rzdf = find_rzdf(lulc)'''
    # print('Rzdf: {}'.format(rzdf))
    #
    #q = run_hydro(area, p, pet, cn, rzdf, param[0], param[1], param[2], param[3], param[4])
    q = run_hydro_hru(area, p, pet, lulc, cns, param[0], param[1], param[2], param[3], param[4], export='')
    #
    # find q90:
    cfc = find_cfc(q['Q'])
    q90 = cfc[1][10]
    return (q['Q'], q['CN'][0], q['Rzd'][0], q90, q['Qb'])


def find_sc(q, wp, pp, a, b, k=1, e=-0.17, type='lin', full=False):
    #
    # convert streamflow from m3/s to m3/d
    q = q * 86400
    #
    # this is the water scarcity time series:
    w_sc = (wp - q) * ((wp - q) > 0)
    #
    if type == 'lin':
        # water price time series under scarcity:
        p = ((w_sc - b) / a) * (w_sc > 0)  # from W = A*P + B
        # differences in water price and projected tariff
        diff_p = (p - pp) * (w_sc > 0)
        # Integrate de area under the curve
        # For linear model: SC=(P - Pp)*(Q - Wp)/2  is just a rectangular triangle
        sc_cost_ts = diff_p * w_sc / 2
    elif type == 'exp':
        # print('develop code')
        sc_cost_ts = list()
        for i in range(0, len(q)):
            # p = (w / K) ** (1 / e)
            # numerical integration procedure
            if q[i] < wp:
                print('Scarcity condition Q: {}\tWp: {}'.format(q[i], wp))
                w1 = q[i]
                w2 = wp
                n_delta = 1000
                delta = (w2 - w1) / n_delta
                w_array = np.linspace(w1, w2, n_delta)
                p_array = np.power(w_array / k, 1 / e)
                sc_cost_lcl = np.sum(p_array * delta) - ((w2 - w1) * pp)
                sc_cost_ts.append(sc_cost_lcl)
            else:
                sc_cost_ts.append(0)
        sc_cost_ts = np.array(sc_cost_ts)
    #
    # total scarcity cost:
    sc_cost = np.sum(sc_cost_ts)
    # sc_cost = 0.0
    #
    # finally, get some stats:
    sc_n = np.sum((wp - q) > 0)
    total_n = len(q)
    sc_risk = 100 * sc_n / total_n
    #
    # output full dict:
    if full:
        out = {'SC':sc_cost, 'SC_ts':sc_cost_ts, 'WSC_ts':w_sc, 'Q_ts':q, 'P_ts':p, 'Diff_P_ts':diff_p, 'Risk':sc_risk}
    else:
        out = {'SC': sc_cost, 'Risk':sc_risk}
    # printing section:
    prt = False
    if prt:
        ext = 10
        print('Available water m3:\t{}'.format(q[:ext]))
        print('Water scarcity m3: \t{}'.format(w_sc[:ext]))
        print('Prices  $/m3:      \t{}'.format(p[:ext]))
        print('Loss $/m3:         \t{}'.format(diff_p[:ext]))
        print('Scarcity cost ts $:\t{}'.format(sc_cost_ts[:ext]))
        print('\nScarcity cost $: {}'.format(sc_cost))
        print('Scarcity risck :{}%'.format(sc_risk * 100))
    #
    return out


def find_tc(q, qb, wp, lulc, a, b):
    # get scf from lulc:
    scfa = lulc[2] + lulc[5] + lulc[6] + lulc[7]
    scf = 100 * scfa / sum(lulc)
    #
    # get the curent TCunitary
    tcu = a / pow(scf, b)
    tcu_qb = a / pow(100, b)
    # get qbf array
    qbf = qb/q
    '''print('scf: {}'.format(scf))
    print('tcu: {}'.format(tcu))
    print('tcu_qb: {}'.format(tcu_qb))
    print('qbf: {}'.format(qbf[:6]))'''
    #
    # get treated water
    q =  q * 86400  # convert m3/s to m3/d
    tw = q * (q < wp) + wp * (q >= wp)  # treatment water array
    tc_array = tw * ((qbf * tcu_qb) + ((1 - qbf) * tcu))  # treatment cost array
    tc = np.sum(tc_array)
    prt = False
    if prt:
        print('Soil conservation area fraction: {}%'.format(scf))
        print('Unitary treatment cost: {}$/m3'.format(tcu))
        print('Treatment cost: ${}'.format(tc))
    return tc


def find_lulc(p0, p1, p2, p3=1):
    """

    :param p0: last lulc tuple
    :param p1: decision set tuple
    :param p2: available area, in % of total area
    :return: tuple of lulc
    """

    # get local available area:
    lcl_avail_area = p0[3] + p0[4]

    if lcl_avail_area <= 0:  # it can`t expand! So the LULC doesnt change
        return p0
    else:
        # find % of NBS in lulc
        new_x_nbsf = p1[0] * p2 / 100
        new_x_nbsp = p1[1] * p2 / 100
        new_x_nbsc = p1[2] * p2 / 100

        # update nbs % in lulc:
        new_nbsf = new_x_nbsf + p0[5]
        new_nbsp = new_x_nbsp + p0[6]
        new_nbsc = new_x_nbsc + p0[7]

        # find total % of converted area
        conv_area = new_x_nbsp + new_x_nbsf + new_x_nbsc

        # Expansion partition
        '''
        here we assume the conversion area of pasture and crops to be
        proportinal to relative pasture and crops partition
        this is a limitation once is not the optimal conversion set
        a best approach would priorize land class conversions 
        '''
        ratio_p = p0[3] / (p0[3] + p0[4])
        ratio_c = p0[4] / (p0[3] + p0[4])

        # get the pasture and crops update areas
        new_p = p0[3] - (conv_area * ratio_p)
        new_c = p0[4] - (conv_area * ratio_c)

        def_output = (round(p0[0], p3),
                      round(p0[1], p3),
                      round(p0[2], p3),
                      round(new_p, p3),
                      round(new_c, p3),
                      round(new_nbsf, p3),
                      round(new_nbsp, p3),
                      round(new_nbsc, p3))
        # prints:
        '''
        print('% avail area in Stage 0: {}'.format(p2))
        print('Expansion X = {}% >> {}'.format(sum(p1), p1))
        print('% total area expanded = {}'.format(conv_area))
    
        print('NBSf = {}'.format(new_nbsf))
        print('NBSp = {}'.format(new_nbsp))
        print('NBSc = {}'.format(new_nbsc))
        print('sum = {}'.format(new_nbsf + new_nbsc + new_nbsp))
    
        print('ratio of pasture area/local available area = {}'.format(round(ratio_p, 3)))
        print('ratio of crops area/local available area = {}'.format(round(ratio_c, 3)))
        
        '''
        return def_output


def get_lulc(p0, p1=1):
    lst = list()
    s = sum(p0)
    for elem in p0:
        lcl = round(100 * elem / s, p1)
        lst.append(lcl)
    return tuple(lst)


def get_dp_status(p0, p1, p2=3.3):
    def_flt = 100 * p0 / p1
    aux_len = len(str(p1))
    if aux_len <= 3:
        def_str = 'DP Status: {:>7.2f}%    Batch: {:>4} of {:<4}    ' \
                  'Enlapsed time: {:8>.1f} secs'.format(def_flt, p0, p1, p2)
    else:
        def_str = 'DP Status: {:>7.3f}%    Batch: {:>8} of {:<8}    ' \
                  'Enlapsed time: {:8>.1f} secs'.format(def_flt, p0, p1, p2)
    return def_str


def slice_ts(ts, stg):
    # print(len(stg))
    chunks = len(stg) - 1
    sliced_lst = [(0)]  # 0 array to trick the algorithm
    slice_id = 0
    slice_size = int(len(ts) / chunks)
    for i in range(1, len(stg) - 1):
        lcl_ts = ts[slice_id: slice_size + slice_id]
        sliced_lst.append(lcl_ts[:])
        slice_id = slice_id + slice_size
    lcl_ts = ts[slice_id:]
    sliced_lst.append(lcl_ts[:])
    return tuple(sliced_lst)


def size_dp(p0, p1, p2):
    """

    :param p0: tuple of all xds
    :param p1: tuple of states
    :param p2: tuple of stages
    :return: number of dp simulation batches
    """
    size = 0
    for i in range(0, len(p2[1:])):
        # print('Stage: {}'.format(p2[1:][i]))
        if i == 0:
            for j in range(0, len(p1)):
                npx = len(p0[j])
                size = size + npx
                # print('\tState: {}'.format(p1[j]))
                # print('\t\tX: {}'.format(p1[j]), end='\t')
                # print('\tNumber of possible xds: {}'.format(npx), end='\t')
                # print('Size: {}'.format(size))
            pass
        else:
            for j in range(0, len(p1)):
                # print('\tState: {}'.format(p1[j]))
                for k in range(0, len(p1[:j + 1])):
                    npx = len(p0[k])
                    size = size + npx
                    # print('\t\tX: {}'.format(p1[k]), end='\t')
                    # print('\tNumber of possible xds: {}'.format(npx), end='\t')
                    # print('Size: {}'.format(size))
    return size


def get_xds(p0, p1):
    """

    :param p0: X decision value
    :param p1: Y state step
    :return: tuple with all possible xds in sub tuples of (nbs_forest, nbs_pasture, nbs_crops)
    """
    def_xds = list()  # list to store all possible states
    for def_nbsf in range(0, p0 + 1, p1):
        for def_nbsp in range(0, p0 + 1, p1):
            for def_nbsc in range(0, p0 + 1, p1):
                s = def_nbsf + def_nbsp + def_nbsc
                if s == p0:
                    # (nbs_forest, nbs_pasture, nbs_crops)
                    def_row = (def_nbsf, def_nbsp, def_nbsc)
                    def_xds.append(def_row)
    def_output = tuple(def_xds[:])
    def_xds.clear()
    return def_output


def get_all_xds(p0, p1):
    """

    :param p0: tuple with all possible X (the same as possible States)
    :param p1: State step Y
    :return: tuple with all possible Xds by X
    """
    def_xds_lst = list()
    for def_e in p0:
        def_lcl_xds = get_xds(def_e, p1)
        def_xds_lst.append(def_lcl_xds[:])
    def_output = tuple(def_xds_lst[:])
    def_xds_lst.clear()
    return def_output


def set_dp(p0, p1, p2, p3):
    """
    DP settings function
    :param p0: year of start of planning horizon
    :param p1: years of planning cycle
    :param p2: number of planning cycles
    :param p3: index of Y (state step)
    :return: tuple of stage tuple and state tuple
    """
    # State settings
    y_possible = (1, 2, 5, 10, 20, 25)
    Y = y_possible[p3]  # chose from tuple
    nstt = int(100 / Y)  # number of possible states

    # built list of all possible states:
    aux_int = 0
    def_stt = [0]
    for i in range(0, nstt):
        aux_int = aux_int + Y
        def_stt.append(aux_int)
    # pass it to a tuple:
    def_stt_tpl = tuple(def_stt)
    # clear state list:
    def_stt.clear()

    # Stage settings
    nstg = p2  # number of stages
    ystg = p1  # years in stage period
    ystg0 = p0  # year in stage = 0

    # built list of all stages:
    def_stg = list()
    for i in range(0, nstg):
        aux_int = ystg0 + i * ystg
        def_stg.append(aux_int)
    # pass it to a tuple:
    def_stg_tpl = tuple(def_stg)
    # clear state list:
    def_stt.clear()

    # built list of decision sets
    def_all_xds =  get_all_xds(def_stt_tpl, Y)
    # size the DP number of simulations:
    size = size_dp(def_all_xds, def_stt_tpl, def_stg_tpl)
    def_output = (def_stg_tpl, def_stt_tpl, Y, size, def_all_xds)

    return def_output


def run_sim(setts, data, pol, sim=False, prt_sts=False):
    """
    run DP for NBS expansion optimization
    :param setts: tuple with dp parameters (settings)
    :param data: dp data
    :param prt_sts: boolean to control status screen printouts
    :return:
    """
    import time
    sim_policy = pol
    drifter = 1
    if sim:
        drifter = 1000 * 1000 * 1000
    baseline_bool = False
    simpol_bool = False
    # get current time:
    dp_t0 = time.time()
    # get run timestamp
    run_ts = stringsf.nowsep()
    #
    # get parameters:
    stg = setts[0]  # get stages tuple
    stt = setts[1]  # get states tuple
    y = setts[2]  # get Y from settings
    size = setts[3]  # get size of dp
    all_xds = setts[4]  # get all decisions sets
    cycle = stg[1] - stg[0]  # get cycle in years
    #
    # get data:
    lulc0A = data['Lulc0']  # in km2
    area = sum(lulc0A)  # in km2
    availarea = lulc0A[3] + lulc0A[4]  # in km2
    lulc0 = get_lulc(lulc0A)  # in %
    availareaf = lulc0[3] + lulc0[4]  # in %
    soils = data['Soils']
    dp_rr = data['RR']  # in %
    # get time series:
    p_ts = data['P']
    pet_ts = data['PET']
    #
    # get Scarcity model parameters:
    sc_a_p = data['SC_param'][0] # array by stg
    sc_b_p = data['SC_param'][1]
    sc_k_p = data['SC_param'][2]
    sc_e_p = data['SC_param'][3]
    trf = data['Tariff']
    wconsr = data['Wconsr']
    #
    # slice time series to suit dp stages
    p_stg = slice_ts(p_ts, stg)
    pet_stg = slice_ts(pet_ts, stg)
    #
    # hydrology hard parameters
    hydro_p = data['Hydro_p']
    hy_iaf = hydro_p['iaf']
    hy_swmax = hydro_p['swmax']
    hy_gwmax = hydro_p['gwmax']
    hy_knash = hydro_p['knash']
    hy_nnash = int(hydro_p['nnash'])
    hy_param = (hy_iaf, hy_swmax, hy_gwmax, hy_knash, hy_nnash)
    cn0 = hydro_p['CN']
    rzdf0 = hydro_p['Rzdf']
    q90_0 = hydro_p['q90']
    #
    # treatment cost model parameters
    tc_p = data['TC_p']
    tc_p_a = tc_p['A']
    tc_p_b = tc_p['B']
    #
    # operation cost parameters
    oprt_p_nbsf = data['Oprt_p'][0]
    oprt_p_nbsp = data['Oprt_p'][1]
    oprt_p_nbsc = data['Oprt_p'][2]
    oprt_nbsf_a = oprt_p_nbsf['A']
    oprt_nbsf_b = oprt_p_nbsf['B']
    oprt_nbsp_a = oprt_p_nbsp['A']
    oprt_nbsp_b = oprt_p_nbsp['B']
    oprt_nbsc_a = oprt_p_nbsc['A']
    oprt_nbsc_b = oprt_p_nbsc['B']
    oprt_data = (oprt_nbsf_a, oprt_nbsf_b, oprt_nbsp_a, oprt_nbsp_b, oprt_nbsc_a, oprt_nbsc_b)
    #
    # installation cost parameters
    inst_p_nbsf = data['Inst_p'][0]
    inst_p_nbsp = data['Inst_p'][1]
    inst_p_nbsc = data['Inst_p'][2]
    inst_nbsf_a = inst_p_nbsf['A']
    inst_nbsf_b = inst_p_nbsf['B']
    inst_nbsp_a = inst_p_nbsp['A']
    inst_nbsp_b = inst_p_nbsp['B']
    inst_nbsc_a = inst_p_nbsc['A']
    inst_nbsc_b = inst_p_nbsc['B']
    inst_data = (inst_nbsf_a, inst_nbsf_b, inst_nbsp_a, inst_nbsp_b, inst_nbsc_a, inst_nbsc_b)
    #
    # set counter:
    dp_counter = 0
    #
    # create lists to store repost sections:
    header_lst = ['\n\n****** PLANS - DYNAMIC PROGRAMMING PROCEDURE ******\n\n']
    param_lst = ['\n\n\nDP MODELS PARAMETERS\n\n']
    output_lst = ['\n\n\nDP OUTPUT\n\n']
    policy_lst = ['\n\n\nDP GLOBAL POLICY OUTLOOK\n\n']
    log_lst = ['\n\n\nDP LOG Report\n\n']
    #
    # report header prints:
    while True:  # loop here is just to better organize
        aux_str1 = 'Timestamp:' + run_ts
        aux_str2 = '\n\nStages: ' + str(stg) + '\nStates: ' + str(stt) + \
                   '\nReturn rate (%): ' + str(dp_rr) +  \
                   '\n\nDP size: ' + str(size) + ' batches\n'
        aux_str3 = '\nWatershed area in km2: {}\nLULC in Stage 0:'.format(area)
        aux_tpl = ('urban', 'water', 'forest', 'pasture', 'crops', 'nbs_forest', 'nbs_pasture', 'nbs_crops')
        df = pd.DataFrame({'Area in km2': lulc0A}, index=aux_tpl)
        aux_str4 = df.to_string()
        aux_str5 = 'Available area (pasture + crops): ' + str(availarea) + ' km2\n'
        df = pd.DataFrame({'% of Watershed Area': lulc0}, index=aux_tpl)
        aux_str4a = df.to_string()
        aux_str5b = 'Available area (pasture + crops): ' + str(availareaf) + '%\n'
        aux_str6 = '\n\nHydrology hard parameters:' \
                   '\nIaf: {}\nSwmax: {}\nGWmax: {}\nK-Nash: {}' \
                   '\nN-Nash: {}\n'.format(hy_iaf, hy_swmax, hy_gwmax, hy_knash, hy_nnash)
        aux_str7 = '\nTreatment cost model parameters:' \
                   '\nTC model parameter A: {}\nTC model parameter B: {}\n'.format(tc_p_a, tc_p_b)
        aux_str8 = '\nInstallation cost model parameters:\n' \
                   'NBS forest:\n\tParameter A: {}\n\tParameter B: {}\n' \
                   'NBS pasture:\n\tParameter A: {}\n\tParameter B: {}\n' \
                   'NBS crops:\n\tParameter A: {}\n\tParameter B: {}\n'.format(inst_nbsf_a, inst_nbsf_b, inst_nbsp_a,
                                                                               inst_nbsp_b, inst_nbsc_a, inst_nbsc_b)
        aux_str9 = '\nOperation cost model parameters:\n' \
                   'NBS forest:\n\tParameter A: {}\n\tParameter B: {}\n' \
                   'NBS pasture:\n\tParameter A: {}\n\tParameter B: {}\n' \
                   'NBS crops:\n\tParameter A: {}\n\tParameter B: {}\n'.format(inst_nbsf_a, inst_nbsf_b, inst_nbsp_a,
                                                                               inst_nbsp_b, inst_nbsc_a, inst_nbsc_b)
        param_lst.append(aux_str1)
        param_lst.append(aux_str2)
        param_lst.append(aux_str3)
        param_lst.append(aux_str4)
        param_lst.append(aux_str5)
        param_lst.append(aux_str4a)
        param_lst.append(aux_str5b)
        param_lst.append(aux_str6)
        param_lst.append(aux_str7)
        param_lst.append(aux_str8)
        param_lst.append(aux_str9)
        break
    #
    #
    # create baseline scenario (do-nothing) setup:
    c0 = [(0, 0, 0, (0, 0, 0), (0, 0, 0), (q90_0, cn0, rzdf0), 0)]
    #
    #
    # create empty list of policies:
    glb_policy = list()
    for t in range(0, len(stg)):
        glb_policy.append([(0, 0, 0, 0, (0, 0, 0), lulc0, 0, (0, (0, 0, 0)), (0, (0, 0, 0)), q90_0, cn0, rzdf0, 0)])
    #
    #
    cn_lst = list()
    rzdf_lst = list()
    q90_lst = list()
    #
    # get DP procedure starting time
    dp_t1 = time.time()
    #
    #
    # forward movement loop (simulation happens here):
    for t in range(1, len(stg)):
        # printing section
        log_str = '\n\n\nStage #' + str(t) + ' (' + str(stg[t]) + ')'
        log_lst.append(log_str)
        # get last stage list of best policies
        last_stg_policy = glb_policy[t - 1]
        # populate list of local best policies
        stg_best_policy = list()
        # Not recursive section. One-to-go stage, stg =1:
        if t == 1:
            # loop in all states
            for s in range(0, len(stt)):
                # last lulc:
                last_lulc = lulc0
                # populate all possible decisions
                x = stt[s]  # is just one here
                xds = all_xds[s]  # get decision sets - index s is the same as the state index
                # printing section:
                log_str = '\n\nStage #' + str(t) + '\tState #' + str(s) + ':\t S= ' \
                           + str(stt[s]) + '\t\tXps= ' + str(x)
                log_lst.append(log_str)
                # load lists:
                fps = list()  # possible fs
                xps = list()  # possible xs
                xdps = list()  # possible xdps
                lulcps = list()  # possible lulcs
                last_sttps = list()  # possible last states
                cfvs = list()  # possible local costs in fv
                cpvs = list()  # possible local costs in pv
                q90s = list()
                cns = list()
                rzdfs = list()
                risks = list()
                # loop in all decision sets:
                for e in xds:
                    # not recursive section
                    # checkers:
                    if s == 0 and sum(e) == 0:
                        baseline_bool = True
                    else:
                        baseline_bool = False
                    #
                    if e == sim_policy[t]:
                        simpol_bool = True
                        print('{} = {}'.format(e, sim_policy[t]))
                    else:
                        simpol_bool = False
                    # find lulc
                    lulc_lcl = find_lulc(last_lulc, e, availareaf)
                    #
                    # find q:
                    q_tpl = find_q(area, p_stg[t], pet_stg[t], lulc_lcl, soils, hy_param)
                    # get values:
                    q_lcl = q_tpl[0]  # array
                    cn_lcl = q_tpl[1]
                    rzdf_lcl = q_tpl[2]
                    q90_lcl = q_tpl[3]
                    qb_lcl = q_tpl[4]
                    #
                    # find costs:
                    # here the simulations batch happens:
                    c_lcl_xcfv = find_xc(lulc_lcl, area, cycle, oprt_data, e, availarea, inst_data)  # expansion cost
                    #
                    # scarcity cost batch
                    c_lcl_scfv_dct = find_sc(q_lcl, wconsr[t - 1], trf[t - 1], sc_a_p[t -1], sc_b_p[t -1],
                                             sc_k_p[t -1], sc_e_p[t -1])
                    c_lcl_scfv = c_lcl_scfv_dct['SC']  # scarcity cost
                    sc_risk_lcl = c_lcl_scfv_dct['Risk']  # scarcity risk
                    #
                    # treatment cost batch:
                    c_lcl_tcfv = find_tc(q_lcl, qb_lcl, wconsr[t - 1], lulc_lcl, tc_p_a, tc_p_b)  # treatment cost
                    #
                    # local costs in fv (scarcity, treatment, expansion):
                    c_lcl_fv = (round(c_lcl_scfv + c_lcl_tcfv + c_lcl_xcfv, 2), (c_lcl_scfv, c_lcl_tcfv, c_lcl_xcfv))
                    #
                    c_lcl_xcpv = find_pv(c_lcl_xcfv, stg[t] - stg[0], dp_rr)  # get present value
                    c_lcl_scpv = find_pv(c_lcl_scfv, stg[t] - stg[0], dp_rr)  # get present value
                    c_lcl_tcpv = find_pv(c_lcl_tcfv, stg[t] - stg[0], dp_rr)  # get present value
                    #
                    # total cost:
                    c_lcl = round(c_lcl_xcpv + c_lcl_scpv + c_lcl_tcpv, 2)
                    #
                    # local costs in pv (scarcity, treatment, expansion):
                    c_lcl_pv = (c_lcl, (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv))
                    #
                    f_lcl = c_lcl  # no recursion
                    #
                    # baseline checker:
                    if baseline_bool:
                        c0.append((f_lcl, c_lcl_fv[0], c_lcl_pv[0],
                                   (c_lcl_scfv, c_lcl_tcfv, c_lcl_xcfv), (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv),
                                   (q90_lcl, cn_lcl, rzdf_lcl), sc_risk_lcl))
                    # policy simulation checker:
                    if simpol_bool:
                        # total cost:
                        c_lcl = round(c_lcl_xcpv + c_lcl_scpv + c_lcl_tcpv, 2)
                        #
                        # local costs in pv (scarcity, treatment, expansion):
                        c_lcl_pv = (c_lcl, (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv))
                        #
                        f_lcl = c_lcl  # no recursion
                    else:
                        # total cost:
                        c_lcl = round(c_lcl_xcpv + c_lcl_scpv + c_lcl_tcpv, 2) * drifter
                        #
                        # local costs in pv (scarcity, treatment, expansion):
                        c_lcl_pv = (c_lcl, (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv))
                        #
                        f_lcl = c_lcl  # no recursion
                    #
                    # get last state
                    last_stt = stt[s] - x
                    #
                    # append to lists:
                    fps.append(f_lcl)
                    xps.append(x)
                    xdps.append(e[:])
                    lulcps.append(lulc_lcl[:])
                    last_sttps.append(last_sttps)
                    cfvs.append(c_lcl_fv[:])
                    cpvs.append(c_lcl_pv[:])
                    q90s.append(q90_lcl)
                    cns.append(cn_lcl)
                    rzdfs.append(rzdf_lcl)
                    risks.append(sc_risk_lcl)
                    #
                    #
                    # append to outer lists:
                    cn_lst.append(cn_lcl)
                    rzdf_lst.append(rzdf_lcl)
                    q90_lst.append(q90_lcl)
                    #
                    #
                    # update counter:
                    dp_counter = dp_counter + 1
                    # printing section:
                    aux_flt = time.time() - dp_t1
                    log_str = get_dp_status(dp_counter, size, aux_flt)
                    log_lst.append(log_str)
                    if prt_sts:
                        print(log_str)
                #
                # get the best f from list:
                best_f = min(fps)
                # get best f index:
                f_id = fps.index(best_f)
                #
                # retrieve best variables using f_id:
                best_x = xps[f_id]  # best x
                best_xd = xdps[f_id]  # best xd decision set
                best_lcl_lulc = lulcps[f_id]  # best lulc
                best_cfv = cfvs[f_id]
                best_cpv = cpvs[f_id]
                best_q90 = q90s[f_id]
                best_cn = cns[f_id]
                best_rzdf = rzdfs[f_id]
                best_risk = risks[f_id]
                #
                # append policy list:
                lcl_best_policy = (t, stt[s], best_f, best_x, best_xd, best_lcl_lulc, last_stt, best_cfv, best_cpv,
                                   best_q90, best_cn, best_rzdf, best_risk)
                stg_best_policy.append(lcl_best_policy)  # local best stage policy: f, state, decision
                #
                # printing section:
                df = pd.DataFrame({'Decision X':xps, 'Decision set Xd':xdps, 'f value':fps, 'LULC':lulcps})
                log_str = df.to_string()
                log_lst.append('')
                log_lst.append(log_str)
                log_lst.append('')
                aux_tpl = ('State S(t)', 'Best f value', 'Best Decision X', 'Best Decision Set Xd', 'Best LULC',
                           'Coming from S(t-1)', 'Costs* in FV', 'Costs* in PV', 'q90 (m3/s)', 'CN', 'Rzdf', 'Risk')
                df = pd.DataFrame({'Best Policy': lcl_best_policy[1:]}, index=aux_tpl)
                log_str = df.to_string()
                log_lst.append(log_str)
                #
                # clear loop lists:
                fps.clear()
                xps.clear()
                xdps.clear()
                lulcps.clear()
                last_sttps.clear()
                cfvs.clear()
                cpvs.clear()
                q90s.clear()
                cns.clear()
                rzdfs.clear()
                risks.clear()
        # Recursive section. stg > 1:
        else:
            # loop all states
            for s in range(0, len(stt)):
                # populate all possible decisions
                xs = stt[:s + 1]
                # printing section:
                log_str = '\n\nStage #' + str(t) + '\tState #' + str(s) + ':\t S= ' \
                          + str(stt[s]) + '\t\tXps= ' + str(xs)
                log_lst.append(log_str)
                # loop in all possible decisions:
                fps = list()  # possible fs
                xps = list()  # possible xs
                xdps = list()  # possible xdps
                lulcps = list()  # possible lulcs
                last_sttps = list()  # possible last states
                cfvs = list()  # possible local costs in fv
                cpvs = list()  # possible local costs in pv
                lps = list()  # last local policies (for printing only)
                q90s = list()
                cns = list()
                rzdfs = list()
                risks = list()
                for xp in range(0, len(xs)):
                    # get local last policy
                    last_stt = stt[s] - xs[xp]  # last state given current state and decision
                    last_stt_id = stt.index(last_stt)
                    last_lcl_policy = last_stg_policy[last_stt_id]  # retrieve last policy from stage policies list
                    # last lulc:
                    last_lulc = last_lcl_policy[5]  # retrieve from last lcl policy
                    # populate all possible decision sets:
                    xds = all_xds[xp]
                    # loop in all decision sets:
                    for e in xds:
                        # recursive section
                        # checkers:
                        if s == 0 and sum(e) == 0:
                            baseline_bool = True
                        else:
                            baseline_bool = False
                        #
                        if e == sim_policy[t]:
                            simpol_bool = True
                            print('{} = {}'.format(e, sim_policy[t]))
                        else:
                            simpol_bool = False
                        # find lulc:
                        lulc_lcl = find_lulc(last_lulc, e, availareaf)
                        #
                        # find q:
                        q_tpl = find_q(area, p_stg[t], pet_stg[t], lulc_lcl, soils, hy_param)
                        # get values:
                        q_lcl = q_tpl[0]  # array
                        cn_lcl = q_tpl[1]
                        rzdf_lcl = q_tpl[2]
                        q90_lcl = q_tpl[3]
                        qb_lcl = q_tpl[4]
                        #
                        # find costs:
                        # here the simulations batch happens:
                        c_lcl_xcfv = find_xc(lulc_lcl, area, cycle, oprt_data, e, availarea, inst_data)  # expansion cost
                        #
                        # scarcity cost batch
                        c_lcl_scfv_dct = find_sc(q_lcl, wconsr[t - 1], trf[t - 1], sc_a_p[t - 1], sc_b_p[t - 1],
                                                 sc_k_p[t -1], sc_e_p[t -1])
                        c_lcl_scfv = c_lcl_scfv_dct['SC']  # scarcity cost
                        sc_risk_lcl = c_lcl_scfv_dct['Risk']  # scarcity risk
                        #
                        # treatment cost batch:
                        c_lcl_tcfv = find_tc(q_lcl, qb_lcl, wconsr[t - 1], lulc_lcl, tc_p_a, tc_p_b)  # treatment cost
                        #
                        # local costs in fv (scarcity, treatment, expansion):
                        c_lcl_fv = (round(c_lcl_scfv + c_lcl_tcfv + c_lcl_xcfv, 2), (c_lcl_scfv, c_lcl_tcfv, c_lcl_xcfv))
                        c_lcl_xcpv = find_pv(c_lcl_xcfv, stg[t] - stg[0], dp_rr)  # get present value
                        c_lcl_scpv = find_pv(c_lcl_scfv, stg[t] - stg[0], dp_rr)  # get present value
                        c_lcl_tcpv = find_pv(c_lcl_tcfv, stg[t] - stg[0], dp_rr)  # get present value
                        #
                        #
                        # total cost:
                        c_lcl = round(c_lcl_xcpv + c_lcl_scpv + c_lcl_tcpv, 2)
                        # local costs in pv (scarcity, treatment, expansion):
                        c_lcl_pv = (c_lcl, (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv))
                        # recursion happens here:
                        f_lcl = round(c_lcl + last_lcl_policy[2], 2)  # index 2 is the f value index
                        #
                        # baseline checker:
                        if baseline_bool:
                            c0.append((f_lcl, c_lcl_fv[0], c_lcl_pv[0],
                                       (c_lcl_scfv, c_lcl_tcfv, c_lcl_xcfv), (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv),
                                       (q90_lcl, cn_lcl, rzdf_lcl), sc_risk_lcl))
                        # policy simulation checker:
                        if simpol_bool:
                            # total cost:
                            c_lcl = round(c_lcl_xcpv + c_lcl_scpv + c_lcl_tcpv, 2)
                            # local costs in pv (scarcity, treatment, expansion):
                            c_lcl_pv = (c_lcl, (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv))
                            # recursion happens here:
                            f_lcl = round(c_lcl + last_lcl_policy[2], 2)  # index 2 is the f value index
                        else:
                            # total cost:
                            c_lcl = round(c_lcl_xcpv + c_lcl_scpv + c_lcl_tcpv, 2) * drifter
                            # local costs in pv (scarcity, treatment, expansion):
                            c_lcl_pv = (c_lcl, (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv))
                            # recursion happens here:
                            f_lcl = round(c_lcl + last_lcl_policy[2], 2)  # index 2 is the f value index
                        # append to DP lists:
                        fps.append(f_lcl)
                        xps.append(xs[xp])
                        xdps.append(e[:])
                        lulcps.append(lulc_lcl[:])
                        last_sttps.append(last_stt)
                        cfvs.append(c_lcl_fv[:])
                        cpvs.append(c_lcl_pv[:])
                        lps.append(last_lcl_policy[:])
                        q90s.append(q90_lcl)
                        cns.append(cn_lcl)
                        rzdfs.append(rzdf_lcl)
                        risks.append(sc_risk_lcl)
                        #
                        #
                        # append to outer lists:
                        cn_lst.append(cn_lcl)
                        rzdf_lst.append(rzdf_lcl)
                        q90_lst.append(q90_lcl)
                        #
                        # update counter:
                        dp_counter = dp_counter + 1
                        # printing section:
                        aux_flt = time.time() - dp_t1
                        log_str = get_dp_status(dp_counter, size, aux_flt)
                        log_lst.append(log_str)
                        if prt_sts:
                            print(log_str)
                # get the best f from list:
                best_f = min(fps)
                # get best f index:
                f_id = fps.index(best_f)
                #
                # retrieve best variables using f_id:
                best_x = xps[f_id]  # best x
                best_xd = xdps[f_id]  # best xd decision set
                best_lcl_lulc = lulcps[f_id]  # best lulc
                best_cfv = cfvs[f_id]
                best_cpv = cpvs[f_id]
                best_q90 = q90s[f_id]
                best_cn = cns[f_id]
                best_rzdf = rzdfs[f_id]
                best_risk = risks[f_id]
                #
                # get last best state
                last_stt = stt[s] - best_x
                #
                # local best stage policy: f, state, decision
                lcl_best_policy = (t, stt[s], best_f, best_x, best_xd, best_lcl_lulc, last_stt, best_cfv, best_cpv,
                                   best_q90, best_cn, best_rzdf, best_risk)
                stg_best_policy.append(lcl_best_policy)
                #
                # printing section:
                df = pd.DataFrame({'Decision X': xps, 'Decision set Xd': xdps, 'f value': fps, 'LULC': lulcps})
                log_str = df.to_string()
                log_lst.append('')
                log_lst.append(log_str)
                log_lst.append('')
                aux_tpl = ('State S(t)', 'Best f value', 'Best Decision X', 'Best Decision Set Xd', 'Best LULC',
                           'Coming from S(t-1)', 'Costs* in FV', 'Costs* in PV', 'q90 (m3/s)', 'CN', 'Rzdf', 'Risk')
                df = pd.DataFrame({'Best Policy': lcl_best_policy[1:]}, index=aux_tpl)
                log_str = df.to_string()
                log_lst.append(log_str)
                #
                # clear loop lists:
                fps.clear()
                xps.clear()
                xdps.clear()
                lulcps.clear()
                last_sttps.clear()
                cfvs.clear()
                cpvs.clear()
                q90s.clear()
                cns.clear()
                rzdfs.clear()
                risks.clear()
                lps.clear()
        # append
        glb_policy[t] = tuple(stg_best_policy[:])
        # clear
        stg_best_policy.clear()
    #
    #
    # policies printing section:
    for t in range(0, len(glb_policy)):
        log_str = '\nStage #' + str(t) + ' (' + str(stg[t]) + '):'
        aux_tpl = ('Stage t', 'State S(t)', 'f value', 'Decision X*', 'Decision set Xd* ', 'LULC*', 'Last State S(t-1)',
                   'Costs* in FV', 'Costs* in PV', 'q90 (m3/s)', 'CN', 'Rzdf', 'Risk')
        df = pd.DataFrame(glb_policy[t], columns=aux_tpl)
        policy_lst.append(log_str)
        policy_lst.append(df.to_string())
    #
    #
    # Retrieve from global policies the best path:
    log_str = '\n\n****** DP Backward Look ******\n'
    policy_lst.append(log_str)
    #
    # output lists:
    f_out = list()
    stt_out = list()
    x_out = list()
    xd_out = list()
    lulc_out = list()
    cfv_out = list()
    cpv_out = list()
    q90_out = list()
    cn_out = list()
    rzdf_out = list()
    risk_out = list()
    #
    #
    # backward loop:
    for t in range(len(stg) - 1, -1, -1):
        # printing section:
        log_str = '\nStage #' + str(t) + '\t(' + str(stg[t]) + ')'
        policy_lst.append(log_str)
        # get data from stage policy
        aux_tpl = ('Stage t', 'State S(t)', 'f value', 'Decision X*', 'Decision set Xd* ', 'LULC*', 'Last State S(t-1)',
                   'Costs* in FV', 'Costs* in PV', 'q90 (m3/s)', 'CN', 'Rzdf', 'Risk')
        df = pd.DataFrame(glb_policy[t], columns=aux_tpl)
        df_t = df.T
        # get ss, xs, and fs , etc values:
        stg_ss = tuple(df_t.values[1])
        stg_fs = tuple(df_t.values[2])
        stg_xs = tuple(df_t.values[3])
        stg_xds = tuple(df_t.values[4])
        stg_lulcs = tuple(df_t.values[5])
        stg_cfvs = tuple(df_t.values[7])
        stg_cpvs = tuple(df_t.values[8])
        stg_q90s = tuple(df_t.values[9])
        stg_cns = tuple(df_t.values[10])
        stg_rzdfs = tuple(df_t.values[11])
        stg_risks = tuple(df_t.values[12])
        # start in the last stage:
        if t == len(stg) - 1:
            # use best f to find the starting place
            # find best f:
            best_f = min(stg_fs)
            #
            # find best f id:
            best_f_id = stg_fs.index(best_f)
            #
            # find corresponding S and X:
            best_stt = stg_ss[best_f_id]
            best_x = stg_xs[best_f_id]
            best_xd = stg_xds[best_f_id]
            best_lulc = stg_lulcs[best_f_id]
            best_cfv = stg_cfvs[best_f_id]
            best_cpv = stg_cpvs[best_f_id]
            best_q90 = stg_q90s[best_f_id]
            best_cn = stg_cns[best_f_id]
            best_rzdf = stg_rzdfs[best_f_id]
            best_risk = stg_risks[best_f_id]
            #
            # printing section,
            log_str = 'Best f=' + str(best_f) + '\tf id=' + str(best_f_id) + '\tS=' + str(best_stt) + \
                      '\tX=' + str(best_x) + '\tXd=' + str(best_xd) + '\tLULC=' + str(best_lulc) +\
                      '\tC* FV=' + str(best_cfv) + '\tC* PV=' + str(best_cpv) + '\tq90* =' + str(best_q90) + \
                      '\tCN*=' + str(best_cn) + '\tRzdf*=' + str(best_rzdf) + '\tRisk*=' + str(best_risk)
            policy_lst.append(log_str)
        else:
            # use state to find path
            best_stt = best_last_stt
            best_stt_id = stg_ss.index(best_stt)
            best_f = stg_fs[best_stt_id]
            best_x = stg_xs[best_stt_id]
            best_xd = stg_xds[best_stt_id]
            best_lulc = stg_lulcs[best_stt_id]
            best_cfv = stg_cfvs[best_stt_id]
            best_cpv = stg_cpvs[best_stt_id]
            best_q90 = stg_q90s[best_stt_id]
            best_cn = stg_cns[best_stt_id]
            best_rzdf = stg_rzdfs[best_stt_id]
            best_risk = stg_risks[best_stt_id]
            #
            # printing section
            log_str = 'S=' + str(best_stt) + '\tS id=' + str(best_stt_id) + \
                      '\tf=' + str(best_f) + '\tX=' + str(best_x) + '\tXd=' + str(best_xd) + \
                      '\tLULC=' + str(best_lulc) + '\tC* FV=' + str(best_cfv) + '\tC* PV=' + str(best_cpv) + \
                      '\tq90* =' + str(best_q90) + '\tCN*=' + str(best_cn) + \
                      '\tRzdf*=' + str(best_rzdf) + '\tRisk*=' + str(best_risk)
            policy_lst.append(log_str)
        # store f and S in output lists
        f_out.insert(0, best_f)
        stt_out.insert(0, best_stt)
        x_out.insert(0, best_x)
        xd_out.insert(0, best_xd)
        lulc_out.insert(0, best_lulc)
        cfv_out.insert(0, best_cfv)
        cpv_out.insert(0, best_cpv)
        q90_out.insert(0, best_q90)
        cn_out.insert(0, best_cn)
        rzdf_out.insert(0, best_rzdf)
        risk_out.insert(0, best_risk)
        # find last S(t-1)
        best_last_stt = best_stt - best_x
    #
    #
    #
    # output settings
    # 'Baseline' is: (F, FV, PV, STXfv, STXpv)
    out_dct = {'Stage t': stg,
               'State S(t)': stt_out,
               'Cost f(t) $PV': f_out,
               'Decision X(t)': x_out,
               'Decision Set Xd(t)': xd_out,
               'LULC %':lulc_out,
               'Costs STX $FV': cfv_out,
               'Costs STX $PV': cpv_out,
               'q90': q90_out,
               'CN': cn_out,
               'Rzdf': rzdf_out,
               'Risk': risk_out,
               'Baseline': c0}
    # dp_output = (stg, stt_out, f_out, x_out, xd_out, lulc_out, cfv_out, cpv_out, c0)
    df = pd.DataFrame(out_dct)
    output_lst.append('\nGeneral outlook:')
    output_str = df[['Stage t', 'State S(t)', 'Cost f(t) $PV']].to_string()
    output_lst.append(output_str)
    output_lst.append('\nDecisions outlook:')
    output_str = df[['Stage t', 'State S(t)', 'Decision X(t)', 'Decision Set Xd(t)']].to_string()
    output_lst.append(output_str)
    output_lst.append('\nLULC change outlook:')
    output_str = df[['Stage t', 'State S(t)', 'LULC %']].to_string()
    output_lst.append(output_str)
    output_lst.append('\nCosts outlook:')
    output_str = df[['Stage t', 'State S(t)', 'Costs STX $FV', 'Costs STX $PV']].to_string()
    output_lst.append(output_str)
    output_lst.append('\nHydrological outlook:')
    output_str = df[['Stage t', 'q90', 'CN', 'Rzdf', 'Risk']].to_string()
    output_lst.append(output_str)
    output_lst.append('\nBaseline outlook (f, fv, pv, (stx_fv), (stx_pv), (q90, CN, Rzdf), Risk):')
    output_str = df[['Stage t', 'Baseline']].to_string()
    output_lst.append(output_str)
    #
    # footnote prints:
    log_str = '\n\n****** END OF DP PROCEDURE ******\n\n'
    log_lst.append(log_str)
    # find DP elapsed time:
    dp_t2 = time.time()
    dp_procedure_et = dp_t2 - dp_t1
    header_str = 'Elapsed time: ' + str(dp_procedure_et) + ' seconds'
    header_lst.append(header_str)
    #
    # DP logs:
    out_logs = (header_lst, param_lst, output_lst, policy_lst, log_lst)
    #
    # Outer data:
    out_cloud = {'CN':cn_lst[:], 'Rzdf':rzdf_lst[:], 'q90':q90_lst[:]}
    #
    return out_dct, out_logs, run_ts, out_cloud


def run_dp(setts, data, prt_sts=False):
    """
    simulate NBS expansion
    :param setts: tuple with dp parameters (settings)
    :param data: dp data
    :param prt_sts: boolean to control status screen printouts
    :return:
    """
    import time

    # get current time:
    dp_t0 = time.time()
    # get run timestamp
    run_ts = stringsf.nowsep()
    #
    # get parameters:
    stg = setts[0]  # get stages tuple
    stt = setts[1]  # get states tuple
    y = setts[2]  # get Y from settings
    size = setts[3]  # get size of dp
    all_xds = setts[4]  # get all decisions sets
    cycle = stg[1] - stg[0]  # get cycle in years
    #
    # get data:
    lulc0A = data['Lulc0']  # in km2
    area = sum(lulc0A)  # in km2
    availarea = lulc0A[3] + lulc0A[4]  # in km2
    lulc0 = get_lulc(lulc0A)  # in %
    availareaf = lulc0[3] + lulc0[4]  # in %
    soils = data['Soils']
    dp_rr = data['RR']  # in %
    # get time series:
    p_ts = data['P']
    pet_ts = data['PET']
    #
    # get Scarcity model parameters:
    sc_a_p = data['SC_param'][0] # array by stg
    sc_b_p = data['SC_param'][1]
    sc_k_p = data['SC_param'][2]
    sc_e_p = data['SC_param'][3]
    trf = data['Tariff']
    wconsr = data['Wconsr']
    #
    # slice time series to suit dp stages
    p_stg = slice_ts(p_ts, stg)
    pet_stg = slice_ts(pet_ts, stg)
    #
    # hydrology hard parameters
    hydro_p = data['Hydro_p']
    hy_iaf = hydro_p['iaf']
    hy_swmax = hydro_p['swmax']
    hy_gwmax = hydro_p['gwmax']
    hy_knash = hydro_p['knash']
    hy_nnash = int(hydro_p['nnash'])
    hy_param = (hy_iaf, hy_swmax, hy_gwmax, hy_knash, hy_nnash)
    cn0 = hydro_p['CN']
    rzdf0 = hydro_p['Rzdf']
    q90_0 = hydro_p['q90']
    #
    # treatment cost model parameters
    tc_p = data['TC_p']
    tc_p_a = tc_p['A']
    tc_p_b = tc_p['B']
    #
    # operation cost parameters
    oprt_p_nbsf = data['Oprt_p'][0]
    oprt_p_nbsp = data['Oprt_p'][1]
    oprt_p_nbsc = data['Oprt_p'][2]
    oprt_nbsf_a = oprt_p_nbsf['A']
    oprt_nbsf_b = oprt_p_nbsf['B']
    oprt_nbsp_a = oprt_p_nbsp['A']
    oprt_nbsp_b = oprt_p_nbsp['B']
    oprt_nbsc_a = oprt_p_nbsc['A']
    oprt_nbsc_b = oprt_p_nbsc['B']
    oprt_data = (oprt_nbsf_a, oprt_nbsf_b, oprt_nbsp_a, oprt_nbsp_b, oprt_nbsc_a, oprt_nbsc_b)
    #
    # installation cost parameters
    inst_p_nbsf = data['Inst_p'][0]
    inst_p_nbsp = data['Inst_p'][1]
    inst_p_nbsc = data['Inst_p'][2]
    inst_nbsf_a = inst_p_nbsf['A']
    inst_nbsf_b = inst_p_nbsf['B']
    inst_nbsp_a = inst_p_nbsp['A']
    inst_nbsp_b = inst_p_nbsp['B']
    inst_nbsc_a = inst_p_nbsc['A']
    inst_nbsc_b = inst_p_nbsc['B']
    inst_data = (inst_nbsf_a, inst_nbsf_b, inst_nbsp_a, inst_nbsp_b, inst_nbsc_a, inst_nbsc_b)
    #
    # set counter:
    dp_counter = 0
    #
    # create lists to store repost sections:
    header_lst = ['\n\n****** PLANS - DYNAMIC PROGRAMMING PROCEDURE ******\n\n']
    param_lst = ['\n\n\nDP MODELS PARAMETERS\n\n']
    output_lst = ['\n\n\nDP OUTPUT\n\n']
    policy_lst = ['\n\n\nDP GLOBAL POLICY OUTLOOK\n\n']
    log_lst = ['\n\n\nDP LOG Report\n\n']
    #
    # report header prints:
    while True:  # loop here is just to better organize
        aux_str1 = 'Timestamp:' + run_ts
        aux_str2 = '\n\nStages: ' + str(stg) + '\nStates: ' + str(stt) + \
                   '\nReturn rate (%): ' + str(dp_rr) +  \
                   '\n\nDP size: ' + str(size) + ' batches\n'
        aux_str3 = '\nWatershed area in km2: {}\nLULC in Stage 0:'.format(area)
        aux_tpl = ('urban', 'water', 'forest', 'pasture', 'crops', 'nbs_forest', 'nbs_pasture', 'nbs_crops')
        df = pd.DataFrame({'Area in km2': lulc0A}, index=aux_tpl)
        aux_str4 = df.to_string()
        aux_str5 = 'Available area (pasture + crops): ' + str(availarea) + ' km2\n'
        df = pd.DataFrame({'% of Watershed Area': lulc0}, index=aux_tpl)
        aux_str4a = df.to_string()
        aux_str5b = 'Available area (pasture + crops): ' + str(availareaf) + '%\n'
        aux_str6 = '\n\nHydrology hard parameters:' \
                   '\nIaf: {}\nSwmax: {}\nGWmax: {}\nK-Nash: {}' \
                   '\nN-Nash: {}\n'.format(hy_iaf, hy_swmax, hy_gwmax, hy_knash, hy_nnash)
        aux_str7 = '\nTreatment cost model parameters:' \
                   '\nTC model parameter A: {}\nTC model parameter B: {}\n'.format(tc_p_a, tc_p_b)
        aux_str8 = '\nInstallation cost model parameters:\n' \
                   'NBS forest:\n\tParameter A: {}\n\tParameter B: {}\n' \
                   'NBS pasture:\n\tParameter A: {}\n\tParameter B: {}\n' \
                   'NBS crops:\n\tParameter A: {}\n\tParameter B: {}\n'.format(inst_nbsf_a, inst_nbsf_b, inst_nbsp_a,
                                                                               inst_nbsp_b, inst_nbsc_a, inst_nbsc_b)
        aux_str9 = '\nOperation cost model parameters:\n' \
                   'NBS forest:\n\tParameter A: {}\n\tParameter B: {}\n' \
                   'NBS pasture:\n\tParameter A: {}\n\tParameter B: {}\n' \
                   'NBS crops:\n\tParameter A: {}\n\tParameter B: {}\n'.format(inst_nbsf_a, inst_nbsf_b, inst_nbsp_a,
                                                                               inst_nbsp_b, inst_nbsc_a, inst_nbsc_b)
        param_lst.append(aux_str1)
        param_lst.append(aux_str2)
        param_lst.append(aux_str3)
        param_lst.append(aux_str4)
        param_lst.append(aux_str5)
        param_lst.append(aux_str4a)
        param_lst.append(aux_str5b)
        param_lst.append(aux_str6)
        param_lst.append(aux_str7)
        param_lst.append(aux_str8)
        param_lst.append(aux_str9)
        break
    #
    #
    # create baseline scenario (do-nothing) setup:
    c0 = [(0, 0, 0, (0, 0, 0), (0, 0, 0), (q90_0, cn0, rzdf0), 0)]
    #
    #
    # create empty list of policies:
    glb_policy = list()
    for t in range(0, len(stg)):
        glb_policy.append([(0, 0, 0, 0, (0, 0, 0), lulc0, 0, (0, (0, 0, 0)), (0, (0, 0, 0)), q90_0, cn0, rzdf0, 0)])
    #
    #
    cn_lst = list()
    rzdf_lst = list()
    q90_lst = list()
    #
    # get DP procedure starting time
    dp_t1 = time.time()
    #
    #
    # forward movement loop (simulation happens here):
    for t in range(1, len(stg)):
        # printing section
        log_str = '\n\n\nStage #' + str(t) + ' (' + str(stg[t]) + ')'
        log_lst.append(log_str)
        # get last stage list of best policies
        last_stg_policy = glb_policy[t - 1]
        # populate list of local best policies
        stg_best_policy = list()
        # Not recursive section. One-to-go stage, stg =1:
        if t == 1:
            # loop in all states
            for s in range(0, len(stt)):
                # last lulc:
                last_lulc = lulc0
                # populate all possible decisions
                x = stt[s]  # is just one here
                xds = all_xds[s]  # get decision sets - index s is the same as the state index
                # printing section:
                log_str = '\n\nStage #' + str(t) + '\tState #' + str(s) + ':\t S= ' \
                           + str(stt[s]) + '\t\tXps= ' + str(x)
                log_lst.append(log_str)
                # load lists:
                fps = list()  # possible fs
                xps = list()  # possible xs
                xdps = list()  # possible xdps
                lulcps = list()  # possible lulcs
                last_sttps = list()  # possible last states
                cfvs = list()  # possible local costs in fv
                cpvs = list()  # possible local costs in pv
                q90s = list()
                cns = list()
                rzdfs = list()
                risks = list()
                # loop in all decision sets:
                for e in xds:
                    # not recursive section
                    # find lulc
                    lulc_lcl = find_lulc(last_lulc, e, availareaf)
                    #
                    # find q:
                    q_tpl = find_q(area, p_stg[t], pet_stg[t], lulc_lcl, soils, hy_param)
                    # get values:
                    q_lcl = q_tpl[0]  # array
                    cn_lcl = q_tpl[1]
                    rzdf_lcl = q_tpl[2]
                    q90_lcl = q_tpl[3]
                    qb_lcl = q_tpl[4]
                    #
                    # find costs:
                    # here the simulations batch happens:
                    c_lcl_xcfv = find_xc(lulc_lcl, area, cycle, oprt_data, e, availarea, inst_data)  # expansion cost
                    #
                    # scarcity cost batch
                    c_lcl_scfv_dct = find_sc(q_lcl, wconsr[t - 1], trf[t - 1], sc_a_p[t -1], sc_b_p[t -1],
                                             sc_k_p[t -1], sc_e_p[t -1])
                    c_lcl_scfv = c_lcl_scfv_dct['SC']  # scarcity cost
                    sc_risk_lcl = c_lcl_scfv_dct['Risk']  # scarcity risk
                    #
                    # treatment cost batch:
                    c_lcl_tcfv = find_tc(q_lcl, qb_lcl, wconsr[t - 1], lulc_lcl, tc_p_a, tc_p_b)  # treatment cost
                    #
                    # local costs in fv (scarcity, treatment, expansion):
                    c_lcl_fv = (round(c_lcl_scfv + c_lcl_tcfv + c_lcl_xcfv, 2), (c_lcl_scfv, c_lcl_tcfv, c_lcl_xcfv))
                    #
                    c_lcl_xcpv = find_pv(c_lcl_xcfv, stg[t] - stg[0], dp_rr)  # get present value
                    c_lcl_scpv = find_pv(c_lcl_scfv, stg[t] - stg[0], dp_rr)  # get present value
                    c_lcl_tcpv = find_pv(c_lcl_tcfv, stg[t] - stg[0], dp_rr)  # get present value
                    #
                    # total cost:
                    c_lcl = round(c_lcl_xcpv + c_lcl_scpv + c_lcl_tcpv, 2)
                    #
                    # local costs in pv (scarcity, treatment, expansion):
                    c_lcl_pv = (c_lcl, (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv))
                    #
                    f_lcl = c_lcl  # no recursion
                    #
                    # get last state
                    last_stt = stt[s] - x
                    #
                    # append to lists:
                    fps.append(f_lcl)
                    xps.append(x)
                    xdps.append(e[:])
                    lulcps.append(lulc_lcl[:])
                    last_sttps.append(last_sttps)
                    cfvs.append(c_lcl_fv[:])
                    cpvs.append(c_lcl_pv[:])
                    q90s.append(q90_lcl)
                    cns.append(cn_lcl)
                    rzdfs.append(rzdf_lcl)
                    risks.append(sc_risk_lcl)
                    #
                    # baseline checker:
                    if s == 0 and sum(e) == 0:
                        c0.append((f_lcl, c_lcl_fv[0], c_lcl_pv[0],
                                  (c_lcl_scfv, c_lcl_tcfv, c_lcl_xcfv), (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv),
                                   (q90_lcl, cn_lcl, rzdf_lcl), sc_risk_lcl))
                    #
                    #
                    # append to outer lists:
                    cn_lst.append(cn_lcl)
                    rzdf_lst.append(rzdf_lcl)
                    q90_lst.append(q90_lcl)
                    #
                    #
                    # update counter:
                    dp_counter = dp_counter + 1
                    # printing section:
                    aux_flt = time.time() - dp_t1
                    log_str = get_dp_status(dp_counter, size, aux_flt)
                    log_lst.append(log_str)
                    if prt_sts:
                        print(log_str)
                #
                # get the best f from list:
                best_f = min(fps)
                # get best f index:
                f_id = fps.index(best_f)
                #
                # retrieve best variables using f_id:
                best_x = xps[f_id]  # best x
                best_xd = xdps[f_id]  # best xd decision set
                best_lcl_lulc = lulcps[f_id]  # best lulc
                best_cfv = cfvs[f_id]
                best_cpv = cpvs[f_id]
                best_q90 = q90s[f_id]
                best_cn = cns[f_id]
                best_rzdf = rzdfs[f_id]
                best_risk = risks[f_id]
                #
                # append policy list:
                lcl_best_policy = (t, stt[s], best_f, best_x, best_xd, best_lcl_lulc, last_stt, best_cfv, best_cpv,
                                   best_q90, best_cn, best_rzdf, best_risk)
                stg_best_policy.append(lcl_best_policy)  # local best stage policy: f, state, decision
                #
                # printing section:
                df = pd.DataFrame({'Decision X':xps, 'Decision set Xd':xdps, 'f value':fps, 'LULC':lulcps})
                log_str = df.to_string()
                log_lst.append('')
                log_lst.append(log_str)
                log_lst.append('')
                aux_tpl = ('State S(t)', 'Best f value', 'Best Decision X', 'Best Decision Set Xd', 'Best LULC',
                           'Coming from S(t-1)', 'Costs* in FV', 'Costs* in PV', 'q90 (m3/s)', 'CN', 'Rzdf', 'Risk')
                df = pd.DataFrame({'Best Policy': lcl_best_policy[1:]}, index=aux_tpl)
                log_str = df.to_string()
                log_lst.append(log_str)
                #
                # clear loop lists:
                fps.clear()
                xps.clear()
                xdps.clear()
                lulcps.clear()
                last_sttps.clear()
                cfvs.clear()
                cpvs.clear()
                q90s.clear()
                cns.clear()
                rzdfs.clear()
                risks.clear()
        # Recursive section. stg > 1:
        else:
            # loop all states
            for s in range(0, len(stt)):
                # populate all possible decisions
                xs = stt[:s + 1]
                # printing section:
                log_str = '\n\nStage #' + str(t) + '\tState #' + str(s) + ':\t S= ' \
                          + str(stt[s]) + '\t\tXps= ' + str(xs)
                log_lst.append(log_str)
                # loop in all possible decisions:
                fps = list()  # possible fs
                xps = list()  # possible xs
                xdps = list()  # possible xdps
                lulcps = list()  # possible lulcs
                last_sttps = list()  # possible last states
                cfvs = list()  # possible local costs in fv
                cpvs = list()  # possible local costs in pv
                lps = list()  # last local policies (for printing only)
                q90s = list()
                cns = list()
                rzdfs = list()
                risks = list()
                for xp in range(0, len(xs)):
                    # get local last policy
                    last_stt = stt[s] - xs[xp]  # last state given current state and decision
                    last_stt_id = stt.index(last_stt)
                    last_lcl_policy = last_stg_policy[last_stt_id]  # retrieve last policy from stage policies list
                    # last lulc:
                    last_lulc = last_lcl_policy[5]  # retrieve from last lcl policy
                    # populate all possible decision sets:
                    xds = all_xds[xp]
                    # loop in all decision sets:
                    for e in xds:
                        # recursive section
                        # find lulc:
                        lulc_lcl = find_lulc(last_lulc, e, availareaf)
                        #
                        # find q:
                        q_tpl = find_q(area, p_stg[t], pet_stg[t], lulc_lcl, soils, hy_param)
                        # get values:
                        q_lcl = q_tpl[0]  # array
                        cn_lcl = q_tpl[1]
                        rzdf_lcl = q_tpl[2]
                        q90_lcl = q_tpl[3]
                        qb_lcl = q_tpl[4]
                        #
                        # find costs:
                        # here the simulations batch happens:
                        c_lcl_xcfv = find_xc(lulc_lcl, area, cycle, oprt_data, e, availarea, inst_data)  # expansion cost
                        #
                        # scarcity cost batch
                        c_lcl_scfv_dct = find_sc(q_lcl, wconsr[t - 1], trf[t - 1], sc_a_p[t - 1], sc_b_p[t - 1],
                                                 sc_k_p[t -1], sc_e_p[t -1])
                        c_lcl_scfv = c_lcl_scfv_dct['SC']  # scarcity cost
                        sc_risk_lcl = c_lcl_scfv_dct['Risk']  # scarcity risk
                        #
                        # treatment cost batch:
                        c_lcl_tcfv = find_tc(q_lcl, qb_lcl, wconsr[t - 1], lulc_lcl, tc_p_a, tc_p_b)  # treatment cost
                        #
                        # local costs in fv (scarcity, treatment, expansion):
                        c_lcl_fv = (round(c_lcl_scfv + c_lcl_tcfv + c_lcl_xcfv, 2), (c_lcl_scfv, c_lcl_tcfv, c_lcl_xcfv))
                        c_lcl_xcpv = find_pv(c_lcl_xcfv, stg[t] - stg[0], dp_rr)  # get present value
                        c_lcl_scpv = find_pv(c_lcl_scfv, stg[t] - stg[0], dp_rr)  # get present value
                        c_lcl_tcpv = find_pv(c_lcl_tcfv, stg[t] - stg[0], dp_rr)  # get present value
                        # total cost:
                        c_lcl = round(c_lcl_xcpv + c_lcl_scpv + c_lcl_tcpv, 2)
                        # local costs in pv (scarcity, treatment, expansion):
                        c_lcl_pv = (c_lcl, (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv))
                        # recursion happens here:
                        f_lcl = round(c_lcl + last_lcl_policy[2], 2) # index 2 is the f value index
                        # append to DP lists:
                        fps.append(f_lcl)
                        xps.append(xs[xp])
                        xdps.append(e[:])
                        lulcps.append(lulc_lcl[:])
                        last_sttps.append(last_stt)
                        cfvs.append(c_lcl_fv[:])
                        cpvs.append(c_lcl_pv[:])
                        lps.append(last_lcl_policy[:])
                        q90s.append(q90_lcl)
                        cns.append(cn_lcl)
                        rzdfs.append(rzdf_lcl)
                        risks.append(sc_risk_lcl)
                        #
                        # baseline checker:
                        if s == 0 and sum(e) == 0:
                            c0.append((f_lcl, c_lcl_fv[0], c_lcl_pv[0],
                                       (c_lcl_scfv, c_lcl_tcfv, c_lcl_xcfv),
                                       (c_lcl_scpv, c_lcl_tcpv, c_lcl_xcpv), (q90_lcl, cn_lcl, rzdf_lcl), sc_risk_lcl))
                        #
                        #
                        # append to outer lists:
                        cn_lst.append(cn_lcl)
                        rzdf_lst.append(rzdf_lcl)
                        q90_lst.append(q90_lcl)
                        #
                        # update counter:
                        dp_counter = dp_counter + 1
                        # printing section:
                        aux_flt = time.time() - dp_t1
                        log_str = get_dp_status(dp_counter, size, aux_flt)
                        log_lst.append(log_str)
                        if prt_sts:
                            print(log_str)
                # get the best f from list:
                best_f = min(fps)
                # get best f index:
                f_id = fps.index(best_f)
                #
                # retrieve best variables using f_id:
                best_x = xps[f_id]  # best x
                best_xd = xdps[f_id]  # best xd decision set
                best_lcl_lulc = lulcps[f_id]  # best lulc
                best_cfv = cfvs[f_id]
                best_cpv = cpvs[f_id]
                best_q90 = q90s[f_id]
                best_cn = cns[f_id]
                best_rzdf = rzdfs[f_id]
                best_risk = risks[f_id]
                #
                # get las best state
                last_stt = stt[s] - best_x
                #
                # local best stage policy: f, state, decision
                lcl_best_policy = (t, stt[s], best_f, best_x, best_xd, best_lcl_lulc, last_stt, best_cfv, best_cpv,
                                   best_q90, best_cn, best_rzdf, best_risk)
                stg_best_policy.append(lcl_best_policy)
                #
                # printing section:
                df = pd.DataFrame({'Decision X': xps, 'Decision set Xd': xdps, 'f value': fps, 'LULC': lulcps})
                log_str = df.to_string()
                log_lst.append('')
                log_lst.append(log_str)
                log_lst.append('')
                aux_tpl = ('State S(t)', 'Best f value', 'Best Decision X', 'Best Decision Set Xd', 'Best LULC',
                           'Coming from S(t-1)', 'Costs* in FV', 'Costs* in PV', 'q90 (m3/s)', 'CN', 'Rzdf', 'Risk')
                df = pd.DataFrame({'Best Policy': lcl_best_policy[1:]}, index=aux_tpl)
                log_str = df.to_string()
                log_lst.append(log_str)
                #
                # clear loop lists:
                fps.clear()
                xps.clear()
                xdps.clear()
                lulcps.clear()
                last_sttps.clear()
                cfvs.clear()
                cpvs.clear()
                q90s.clear()
                cns.clear()
                rzdfs.clear()
                risks.clear()
                lps.clear()
        # append
        glb_policy[t] = tuple(stg_best_policy[:])
        # clear
        stg_best_policy.clear()
    #
    #
    # policies printing section:
    for t in range(0, len(glb_policy)):
        log_str = '\nStage #' + str(t) + ' (' + str(stg[t]) + '):'
        aux_tpl = ('Stage t', 'State S(t)', 'f value', 'Decision X*', 'Decision set Xd* ', 'LULC*', 'Last State S(t-1)',
                   'Costs* in FV', 'Costs* in PV', 'q90 (m3/s)', 'CN', 'Rzdf', 'Risk')
        df = pd.DataFrame(glb_policy[t], columns=aux_tpl)
        policy_lst.append(log_str)
        policy_lst.append(df.to_string())
    #
    #
    # Retrieve from global policies the best path:
    log_str = '\n\n****** DP Backward Look ******\n'
    policy_lst.append(log_str)
    #
    # output lists:
    f_out = list()
    stt_out = list()
    x_out = list()
    xd_out = list()
    lulc_out = list()
    cfv_out = list()
    cpv_out = list()
    q90_out = list()
    cn_out = list()
    rzdf_out = list()
    risk_out = list()
    #
    #
    # backward loop:
    for t in range(len(stg) - 1, -1, -1):
        # printing section:
        log_str = '\nStage #' + str(t) + '\t(' + str(stg[t]) + ')'
        policy_lst.append(log_str)
        # get data from stage policy
        aux_tpl = ('Stage t', 'State S(t)', 'f value', 'Decision X*', 'Decision set Xd* ', 'LULC*', 'Last State S(t-1)',
                   'Costs* in FV', 'Costs* in PV', 'q90 (m3/s)', 'CN', 'Rzdf', 'Risk')
        df = pd.DataFrame(glb_policy[t], columns=aux_tpl)
        df_t = df.T
        # get ss, xs, and fs , etc values:
        stg_ss = tuple(df_t.values[1])
        stg_fs = tuple(df_t.values[2])
        stg_xs = tuple(df_t.values[3])
        stg_xds = tuple(df_t.values[4])
        stg_lulcs = tuple(df_t.values[5])
        stg_cfvs = tuple(df_t.values[7])
        stg_cpvs = tuple(df_t.values[8])
        stg_q90s = tuple(df_t.values[9])
        stg_cns = tuple(df_t.values[10])
        stg_rzdfs = tuple(df_t.values[11])
        stg_risks = tuple(df_t.values[12])
        # start in the last stage:
        if t == len(stg) - 1:
            # use best f to find the starting place
            # find best f:
            best_f = min(stg_fs)
            #
            # find best f id:
            best_f_id = stg_fs.index(best_f)
            #
            # find corresponding S and X:
            best_stt = stg_ss[best_f_id]
            best_x = stg_xs[best_f_id]
            best_xd = stg_xds[best_f_id]
            best_lulc = stg_lulcs[best_f_id]
            best_cfv = stg_cfvs[best_f_id]
            best_cpv = stg_cpvs[best_f_id]
            best_q90 = stg_q90s[best_f_id]
            best_cn = stg_cns[best_f_id]
            best_rzdf = stg_rzdfs[best_f_id]
            best_risk = stg_risks[best_f_id]
            #
            # printing section,
            log_str = 'Best f=' + str(best_f) + '\tf id=' + str(best_f_id) + '\tS=' + str(best_stt) + \
                      '\tX=' + str(best_x) + '\tXd=' + str(best_xd) + '\tLULC=' + str(best_lulc) +\
                      '\tC* FV=' + str(best_cfv) + '\tC* PV=' + str(best_cpv) + '\tq90* =' + str(best_q90) + \
                      '\tCN*=' + str(best_cn) + '\tRzdf*=' + str(best_rzdf) + '\tRisk*=' + str(best_risk)
            policy_lst.append(log_str)
        else:
            # use state to find path
            best_stt = best_last_stt
            best_stt_id = stg_ss.index(best_stt)
            best_f = stg_fs[best_stt_id]
            best_x = stg_xs[best_stt_id]
            best_xd = stg_xds[best_stt_id]
            best_lulc = stg_lulcs[best_stt_id]
            best_cfv = stg_cfvs[best_stt_id]
            best_cpv = stg_cpvs[best_stt_id]
            best_q90 = stg_q90s[best_stt_id]
            best_cn = stg_cns[best_stt_id]
            best_rzdf = stg_rzdfs[best_stt_id]
            best_risk = stg_risks[best_stt_id]
            #
            # printing section
            log_str = 'S=' + str(best_stt) + '\tS id=' + str(best_stt_id) + \
                      '\tf=' + str(best_f) + '\tX=' + str(best_x) + '\tXd=' + str(best_xd) + \
                      '\tLULC=' + str(best_lulc) + '\tC* FV=' + str(best_cfv) + '\tC* PV=' + str(best_cpv) + \
                      '\tq90* =' + str(best_q90) + '\tCN*=' + str(best_cn) + \
                      '\tRzdf*=' + str(best_rzdf) + '\tRisk*=' + str(best_risk)
            policy_lst.append(log_str)
        # store f and S in output lists
        f_out.insert(0, best_f)
        stt_out.insert(0, best_stt)
        x_out.insert(0, best_x)
        xd_out.insert(0, best_xd)
        lulc_out.insert(0, best_lulc)
        cfv_out.insert(0, best_cfv)
        cpv_out.insert(0, best_cpv)
        q90_out.insert(0, best_q90)
        cn_out.insert(0, best_cn)
        rzdf_out.insert(0, best_rzdf)
        risk_out.insert(0, best_risk)
        # find last S(t-1)
        best_last_stt = best_stt - best_x
    #
    #
    #
    # output settings
    # 'Baseline' is: (F, FV, PV, STXfv, STXpv)
    out_dct = {'Stage t': stg,
               'State S(t)': stt_out,
               'Cost f(t) $PV': f_out,
               'Decision X(t)': x_out,
               'Decision Set Xd(t)': xd_out,
               'LULC %':lulc_out,
               'Costs STX $FV': cfv_out,
               'Costs STX $PV': cpv_out,
               'q90': q90_out,
               'CN': cn_out,
               'Rzdf': rzdf_out,
               'Risk': risk_out,
               'Baseline': c0}
    # dp_output = (stg, stt_out, f_out, x_out, xd_out, lulc_out, cfv_out, cpv_out, c0)
    df = pd.DataFrame(out_dct)
    output_lst.append('\nGeneral outlook:')
    output_str = df[['Stage t', 'State S(t)', 'Cost f(t) $PV']].to_string()
    output_lst.append(output_str)
    output_lst.append('\nDecisions outlook:')
    output_str = df[['Stage t', 'State S(t)', 'Decision X(t)', 'Decision Set Xd(t)']].to_string()
    output_lst.append(output_str)
    output_lst.append('\nLULC change outlook:')
    output_str = df[['Stage t', 'State S(t)', 'LULC %']].to_string()
    output_lst.append(output_str)
    output_lst.append('\nCosts outlook:')
    output_str = df[['Stage t', 'State S(t)', 'Costs STX $FV', 'Costs STX $PV']].to_string()
    output_lst.append(output_str)
    output_lst.append('\nHydrological outlook:')
    output_str = df[['Stage t', 'q90', 'CN', 'Rzdf', 'Risk']].to_string()
    output_lst.append(output_str)
    output_lst.append('\nBaseline outlook (f, fv, pv, (stx_fv), (stx_pv), (q90, CN, Rzdf), Risk):')
    output_str = df[['Stage t', 'Baseline']].to_string()
    output_lst.append(output_str)
    #
    # footnote prints:
    log_str = '\n\n****** END OF DP PROCEDURE ******\n\n'
    log_lst.append(log_str)
    # find DP elapsed time:
    dp_t2 = time.time()
    dp_procedure_et = dp_t2 - dp_t1
    header_str = 'Elapsed time: ' + str(dp_procedure_et) + ' seconds'
    header_lst.append(header_str)
    #
    # DP logs:
    out_logs = (header_lst, param_lst, output_lst, policy_lst, log_lst)
    #
    # Outer data:
    out_cloud = {'CN':cn_lst[:], 'Rzdf':rzdf_lst[:], 'q90':q90_lst[:]}
    #
    return out_dct, out_logs, run_ts, out_cloud

