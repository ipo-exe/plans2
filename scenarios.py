# ________________________________________________________________________
#       UFRGS - UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL
#           IPH - INSTITUTO DE PESQUISAS HIDRAULICAS
#
#     Research Group in Water Resources Management and Planning - WARP
#                    https://www.ufrgs.br/warp
#           Porto Alegre, Rio Grande do Sul, Brazil
# ________________________________________________________________________
#
# Author: IPORA BRITO POSSANTTI, Environmental Engineer
# Contact: possantti@gmail.com
# Date: March of 2020
# Description:
# this package contains all scenario building functions for Plans2

import numpy as np
from scipy import stats
import pandas as pd
from tools import save


def lin_normalize(p0):
    def_in_array = np.array(p0)
    def_min = np.min(def_in_array)
    def_max = np.max(def_in_array)
    def_a = 1 / (def_max - def_min)
    def_b = - def_a * def_min
    def_out_array = (def_a * def_in_array) + def_b
    return def_out_array


def get_nearest_idx(p0, p1):
    """

    :param p0: searching array
    :param p1: reference array
    :return: array of indexes of nearests values in reference array
    """
    srch = np.array(p0)
    ref = np.array(p1)
    aux_lst = list()
    for i in range(0, len(srch)):
        lcl_id = np.argmin(np.abs(ref - srch[i]))
        aux_lst.append(lcl_id)
    return np.array(aux_lst)


def get_blocks_len(p0):
    """

    :param p0: boolean array
    :return:
    """
    bool = p0
    def_aux_lst = list()
    count = 0
    for def_j in range(0, len(bool)):
        if def_j < len(bool) - 1:
            if bool[def_j] == 1 and bool[def_j + 1] == 1:
                count = count + 1
            elif bool[def_j] == 1 and bool[def_j + 1] == 0:
                count = count + 1
                def_aux_lst.append(count)
                count = 0
            else:
                pass
        else:
            if count == 0 and bool[def_j] == 1:
                count = count + 1
                def_aux_lst.append(count)
    return def_aux_lst


def built_prj_climate(p0, p1, p2):
    """

    :param p0: reference projection dates array
    :param p1: projection p timeseries by year in array
    :param p2: projection pet timeseries by year in array
    :return: tuple with p and pet ajusted timeseries arrays
    """
    # print()
    size = len(p0)
    # print(size)
    p = list()
    pet = list()
    for i in range(0, len(p1)):
        for j in range(0, len(p1[i])):
            p.append(p1[i][j])
            pet.append(p2[i][j])
    # print(len(p))
    # print(len(pet))
    diff = size - len(p)
    # print(diff)
    if diff == 0:
        pass
    elif diff > 0:
        # dates is higher, so we must increase p and pet
        for i in range(0, diff):
            p.append(p1[-1][i])
            pet.append(p2[-1][i])
        diff = size - len(p)
    else:
        # p and pet are higher, so we must descrease p and pet
        p = p[:size]
        pet = pet[:size]
        diff = size - len(p)
    ret_p = np.array(p)
    ret_pet = np.array(pet)
    # print(len(ret_p))
    # print(len(ret_pet))
    return (ret_p, ret_pet)


def built_wetindex_naive(p0, p1, p2):
    """
    this function built a WETNESS INDEX (wet index) for each observer year
    The wetness is considered the average of 3 sub indexes: (1) total precip., (2) number of rainy days and
    average length of rain events.
    :param p0: dates string array (daily)
    :param p1: p array (daily)
    :param p2: pet array (daily)
    :return:
    """
    # build list of observed years: (this is needed in case of missing years in the time series)
    yr_lst = list()
    for i in range(0, len(p0)):
        lcl_yr = int(p0[i][6:])  # get local year in date array
        if i == 0:  # first condition exception
            yr_lst.append(lcl_yr)
        else:  # bulk condition
            last_lcl_yr = int(p0[i - 1][6:])  # get last local year
            if lcl_yr > last_lcl_yr:  # next year condition
                yr_lst.append(lcl_yr)
    yr_lst = np.array(yr_lst)  # convert list to np.array
    #
    #
    # disaggregate time series by year:
    def_p_lst = list()
    def_pet_lst = list()
    def_dates_lst = list()
    def_p_by_year = list()
    def_pet_by_year = list()
    def_dates_by_year = list()
    count = 0
    recount = 0
    for i in range(0, len(yr_lst)):
        srch_yr = yr_lst[i]  # get searching year
        # print('Year: {}'.format(srch_yr))
        # start a loop.
        # this is pretty much fucked up to explain. all you need to know is that it disagregate the
        # series year by year. At the end you have a list of arrays
        count = recount
        while True:
            lcl_yr = int(p0[count][6:])
            # print('Local Year: {}. Searching for {}, \tCount: {}, MaxLen:{}:'.format(lcl_yr, srch_yr, count, len(p0)-1))
            if lcl_yr == srch_yr:
                def_pet_lst.append(p2[count])
                def_p_lst.append(p1[count])
                def_dates_lst.append(p0[count])
                recount = count
                count = count + 1
                if count == len(p0):
                    break
            elif lcl_yr > srch_yr:
                break
            else:
                count = count + 1
        def_pet_by_year.append(np.array(def_pet_lst[:]))  #
        def_p_by_year.append(np.array(def_p_lst[:]))
        def_dates_by_year.append(def_dates_lst[:])
        def_pet_lst.clear()
        def_p_lst.clear()
        def_dates_lst.clear()
    #
    #
    #
    # total accumulated precip. (AP) index procedure:
    def_aux_lst = list()
    for i in range(0, len(yr_lst)):
        ap = np.sum(def_p_by_year[i])
        # print('Year: {} Total acumulated: {}'.format(yr_lst[i], ap))
        def_aux_lst.append(ap)
    def_ap_lst = np.array(def_aux_lst)
    def_aux_lst.clear()
    # get ap_index
    ap_index = lin_normalize(def_ap_lst)
    #
    #
    # total rainy days (TRD):
    def_aux_lst = list()
    for i in range(0, len(yr_lst)):
        trd = np.sum(((np.array(def_p_by_year[i]) > 0)* 1))
        # print('Year: {} Total number of rainy days: {}'.format(yr_lst[i], trd))
        def_aux_lst.append(trd)
    def_trd_lst = np.array(def_aux_lst)
    def_aux_lst.clear()
    # get trd_index
    trd_index = lin_normalize(def_trd_lst)
    #
    #
    # average length for rainy blocks (ARB):
    def_aux_lst = list()
    for i in range(0, len(yr_lst)):
        rain_bool = (np.array(def_p_by_year[i]) > 0) * 1
        count = 0
        def_aux_lst2 = get_blocks_len(rain_bool)
        arb = sum(def_aux_lst2) / len(def_aux_lst2)
        # print('Year: {} Avg length of rain (days): {}'.format(yr_lst[i], arb))
        def_aux_lst.append(arb)
        def_aux_lst2.clear()
    def_arb_lst = np.array(def_aux_lst)
    def_aux_lst.clear()
    arb_index = lin_normalize(def_arb_lst)
    #
    #
    #
    # calculate wet index
    wet_index = (ap_index + trd_index + arb_index) / 3
    #
    #
    # return a dictionary
    r_dct = {'Yrs_obs':yr_lst, 'P_yr':def_p_by_year, 'PET_yr':def_pet_by_year, 'Dt_yr':def_dates_by_year, 'Wet_id':wet_index, 'AP_yr':def_ap_lst,
             'AP_id':ap_index, 'ARB_yr':def_arb_lst, 'ARB_id':arb_index, 'TRD_yr':def_trd_lst, 'TRD_id':trd_index}
    return r_dct


def get_parenthesis_str(p0):
    return p0.split('(')[1].split(')')[0].strip()


def polyprj(xprj, coefs):
    polyclass = np.poly1d(coefs)
    yprj = polyclass(xprj)
    return yprj


def polyfit(xobs, yobs, ord, fixed=False, fixp=0):
    """

    :param xobs:
    :param yobs:
    :param ord:
    :param fixed:
    :param fixp:
    :return:
    """
    if fixed:  # fixar em um ponto específico!
        aux_int = len(xobs) * 100000
        z = np.linspace(0, 0, aux_int) + fixp
        xobs2 = np.append(z, xobs)
        yobs2 = np.append(z, yobs)
        fitparams = np.polyfit(xobs2, yobs2, ord, full=True)
    else:
        fitparams = np.polyfit(xobs, yobs, ord, full=True)
    coefs = fitparams[0]
    residuals = round(float(fitparams[1]), 3)
    polyclass = np.poly1d(coefs)
    yfit = polyclass(xobs)
    return_dct = {'yfit':yfit, 'coefs':coefs, 'residuals':residuals}
    return return_dct


def get_r2_poly(xobs, yobs, ord):
    # linearize y:
    if ord > 1:
        ylin = yobs ** (1 / ord)
    else:
        ylin = yobs
    slp, intcp, rval, pval, serr = stats.linregress(xobs, ylin)
    r2 = rval ** 2
    return r2


def get_r2_exp(xobs, yobs):
    # linearize y:
    ylin = np.log(yobs)
    slp, intcp, rval, pval, serr = stats.linregress(xobs, ylin)
    r2 = rval ** 2
    return r2


def get_r2_log(xobs, yobs):
    # linearize x:
    xlin = np.log(xobs)
    slp, intcp, rval, pval, serr = stats.linregress(xlin, yobs)
    r2 = rval ** 2
    return r2


def climate(p1, p2, p4, p5):
    """

    :param p1: projection years tuple
    :param p2: scenario type key
    :param p4: observed data file path
    :param p5: tuple of scenarios options
    :return:
    """
    # load observed data:
    def_import_file = p4
    # print('load observed data from {}'.format(def_import_file))
    def_df = pd.read_csv(def_import_file, sep=';')
    # get arrays:
    dates_obs_str = def_df.T.values[0]  # get arrays
    p_obs = def_df.T.values[1]  # get arrays
    pet_obs = def_df.T.values[2]  # get arrays
    #
    # build wetness index:
    wetid_dct = built_wetindex_naive(dates_obs_str, p_obs, pet_obs)
    wetid_obs = wetid_dct['Wet_id']
    dt_obs_by_yr = wetid_dct['Dt_yr']
    p_obs_by_yr = wetid_dct['P_yr']
    pet_obs_by_yr = wetid_dct['PET_yr']
    ap_obs = wetid_dct['AP_yr']
    trd_obs = wetid_dct['TRD_yr']
    arb_obs = wetid_dct['ARB_yr']
    #
    # projection type:
    def_key = p2
    #
    # get projection date series:
    start_date_prj = '01/01/' + str(p1[0])
    end_date_prj = '01/01/' + str(p1[-1])
    dates_prj = pd.date_range(start=start_date_prj, end=end_date_prj)
    #
    # find which type of projection is:
    if def_key == 'Stat':
        # create array of wet index:
        wetid_prj_percnt = np.random.uniform(1, 99, size=p1[-1] - p1[0])
        # wetid_prj_percnt = np.random.normal(50, 20, size=p1[-1] - p1[0])
    elif def_key == 'Dry':
        # create array of wet index:
        wetid_prj_percnt = np.random.uniform(20, 30, size=p1[-1] - p1[0])
    elif def_key == 'DryX':
        # create array of wet index:
        wetid_prj_percnt = np.random.uniform(5, 15, size=p1[-1] - p1[0])
    elif def_key == 'DryXX':
        # create array of wet index:
        wetid_prj_percnt = np.random.uniform(1, 5, size=p1[-1] - p1[0])
    elif def_key == 'ToDryX':
        # create array of wet index:
        wetid_prj_percnt = np.linspace(35, 5, p1[-1] - p1[0])
    elif def_key == 'ToDry':
        # create array of wet index:
        wetid_prj_percnt = np.linspace(40, 10, p1[-1] - p1[0])
    elif def_key == 'ToWet':
        # create array of wet index:
        wetid_prj_percnt = np.linspace(50, 80, p1[-1] - p1[0])
    elif def_key == 'ToWetX':
        # create array of wet index:
        wetid_prj_percnt = np.linspace(65, 95, p1[-1] - p1[0])
    elif def_key == 'WetXX':
        # create array of wet index:
        wetid_prj_percnt = np.random.uniform(94, 99, size=p1[-1] - p1[0])
    # print(wetid_prj_percnt)
    # print(len(wetid_prj_percnt))
    #
    wetid_prj_raw = np.percentile(wetid_obs, wetid_prj_percnt)  #
    wetid_prj_idx = get_nearest_idx(wetid_prj_raw, wetid_obs)  # array of indices
    #
    # get projected proxy variables:
    ap_prj = list()
    trd_prj = list()
    arb_prj = list()
    for def_idx in wetid_prj_idx:
        ap_prj.append(ap_obs[def_idx])
        trd_prj.append(trd_obs[def_idx])
        arb_prj.append(arb_obs[def_idx])
    ap_prj = np.array(ap_prj)
    trd_prj = np.array(trd_prj)
    arb_prj = np.array(arb_prj)

    # get projected climate series:
    p_obs_chosen = list()
    pet_obs_chosen = list()
    for idx in wetid_prj_idx:
        p_obs_chosen.append(p_obs_by_yr[idx][:])
        pet_obs_chosen.append(pet_obs_by_yr[idx][:])
    # fit series:
    climate_tpl = built_prj_climate(dates_prj, p_obs_chosen, pet_obs_chosen)
    p_prj = climate_tpl[0]
    pet_prj = climate_tpl[1]
    return_dct = {'Dts_prj':dates_prj, 'P_prj':p_prj, 'PET_prj':pet_prj,
                  'Dts_obs_yr':dt_obs_by_yr, 'P_obs_yr':p_obs_by_yr, 'PET_obs_yr':pet_obs_by_yr,
                  'AP_obs':ap_obs, 'AP_prj':ap_prj, 'TRD_obs':trd_obs,
                  'TRD_prj':trd_prj, 'ARB_obs':arb_obs, 'ARB_prj':arb_prj}
    return return_dct


def yearly_variable(p1, p2, p4, p5):
    """

    :param p1: projecting years tuple
    :param p2: scenario type key
    :param p4: observed data file path
    :param p5: tuple of scenario types options
    :return:
    """
    # load observed data:
    def_import_file = p4
    # print('load observed data from {}'.format(def_import_file))
    def_df = pd.read_csv(def_import_file, sep=';')
    x_obs = def_df.T.values[0]  # get arrays
    y_obs = def_df.T.values[1]  # get arrays

    # years to project:
    x_prj = np.array(p1)
    # print(x_prj)

    # fit model to observed data based on spec key:
    def_key_tpl = p5
    # print('Key options: {}'.format(def_key_tpl))
    def_key = p2
    # print('Key: {}'.format(def_key))

    # handle projection type:
    model_msg = 'Model successfully fitted'
    if def_key[0:4] == 'Cons':
        model_param = get_parenthesis_str(def_key)
        if model_param == 'Avg':
            poly_order = int(0)
            poly_dct = polyfit(x_obs, y_obs, poly_order)
            model_coefs = poly_dct['coefs']
            model_residuals = poly_dct['residuals']
            y_obs_fit = poly_dct['yfit']
            y_prj = polyprj(x_prj, model_coefs)
            model_r2 = get_r2_poly(x_obs, y_obs_fit, poly_order)
            model_type = 'Observed average, Avg= ' + str(model_coefs)
        elif model_param == 'Last':
            model_coefs = y_obs[-1]
            y_obs_fit = (x_obs * 0) + model_coefs
            y_prj = (x_prj * 0) + model_coefs
            diffs = y_obs - y_obs_fit
            model_residuals = np.sum(np.power(diffs, 2))
            model_r2 = get_r2_poly(x_obs, y_obs_fit, 0)
            model_type = 'Constant, C=' + str(model_coefs)
        elif model_param == 'Min':
            model_coefs = min(y_obs)
            y_obs_fit = (x_obs * 0) + model_coefs
            y_prj = (x_prj * 0) + model_coefs
            diffs = y_obs - y_obs_fit
            model_residuals = np.sum(np.power(diffs, 2))
            model_r2 = get_r2_poly(x_obs, y_obs_fit, 0)
            model_type = 'Constant, C=' + str(model_coefs)
        elif model_param == 'Max':
            model_coefs = max(y_obs)
            y_obs_fit = (x_obs * 0) + model_coefs
            y_prj = (x_prj * 0) + model_coefs
            diffs = y_obs - y_obs_fit
            model_residuals = np.sum(np.power(diffs, 2))
            model_r2 = get_r2_poly(x_obs, y_obs_fit, 0)
            model_type = 'Constant, C=' + str(model_coefs)
        else:
            model_coefs = float(model_param)
            y_obs_fit = (x_obs * 0) + model_coefs
            y_prj = (x_prj * 0) + model_coefs
            diffs = y_obs - y_obs_fit
            model_residuals = np.sum(np.power(diffs, 2))
            model_r2 = get_r2_poly(x_obs, y_obs_fit, 0)
            model_type = 'Constant, C=' + str(model_coefs)
    # Linear:
    elif def_key == 'Lin':
        poly_order = int(1)
        poly_dct = polyfit(x_obs, y_obs, poly_order)
        model_coefs = poly_dct['coefs']
        model_residuals = poly_dct['residuals']
        model_r2 = get_r2_poly(x_obs, y_obs, poly_order)
        y_obs_fit = poly_dct['yfit']
        y_prj = polyprj(x_prj, model_coefs)
        model_type = 'Linear fit'
    # Polynomial:
    elif def_key[0:4] == 'Poly':
        poly_order = int(get_parenthesis_str(def_key))
        poly_dct = polyfit(x_obs, y_obs, poly_order)
        model_coefs = poly_dct['coefs']
        model_residuals = poly_dct['residuals']
        model_r2 = get_r2_poly(x_obs, y_obs, poly_order)
        y_obs_fit = poly_dct['yfit']
        y_prj = polyprj(x_prj, model_coefs)
        model_type = 'Polynomial fit, order=' + str(poly_order)
    # Log:
    elif def_key == 'Log':
        poly_order = int(1)
        # linearize y:
        y_obs_lin = np.exp(y_obs)
        poly_dct = polyfit(x_obs, y_obs_lin, poly_order)
        model_coefs = poly_dct['coefs']
        model_residuals = poly_dct['residuals']
        model_r2 = get_r2_log(x_obs, y_obs_lin)
        # for log,  using y = a* ln(x) + b
        y_obs_fit = (model_coefs[0] * np.log(x_obs)) + model_coefs[1]
        y_prj = (model_coefs[0] * np.log(x_prj)) + model_coefs[1]
        # y_obs_fit = poly_dct['yfit']
        # y_prj = polyprj(np.log(x_prj), model_coefs)
        model_type = 'Log fit'
    # Exponential:
    elif def_key == 'Exp':
        poly_order = int(1)
        # linearize y:
        y_obs_lin = np.log(y_obs)
        poly_dct = polyfit(x_obs, y_obs_lin, poly_order)
        model_coefs = poly_dct['coefs']
        model_residuals = poly_dct['residuals']
        model_r2 = get_r2_exp(x_obs, y_obs_lin)
        # for exponential, using y = e^b * e^(ax)
        y_obs_fit = np.exp(model_coefs[1]) * np.exp(model_coefs[0] * x_obs)
        y_prj = np.exp(model_coefs[1]) * np.exp(model_coefs[0] * x_prj)
        model_type = 'Exponential fit'
    # Logistic:
    elif def_key[0:5] == 'Logis':
        model_msg = 'Model fitting failed. Key type not found.'
        model_coefs = (0, 0, 0)
        model_residuals = 0
        model_r2 = 0
        # mirror values:
        y_obs_fit = x_obs
        y_prj = x_prj
        model_type = 'Logistic fit'
    # Power:
    elif def_key == 'Pow':
        poly_order = int(1)
        # linearize y and x:
        x_obs_lin = np.log10(x_obs)
        y_obs_lin = np.log10(y_obs)
        poly_dct = polyfit(x_obs_lin, y_obs_lin, poly_order)
        model_coefs = poly_dct['coefs']
        model_residuals = poly_dct['residuals']
        model_r2 = get_r2_exp(x_obs_lin, y_obs_lin)
        # for power, using y = 10^b * (x^a)
        y_obs_fit = np.power(10, model_coefs[1]) * (np.power(x_obs, model_coefs[0]))
        y_prj = np.power(10, model_coefs[1]) * (np.power(x_prj, model_coefs[0]))
        model_type = 'Power fit'
    # in case of type error
    else:
        model_msg = 'Model fitting failed. Key type not found.'
        model_coefs = (0, 0, 0)
        model_residuals = 0
        model_r2 = 0
        # mirror values:
        y_obs_fit = x_obs
        y_prj = x_prj
        model_type = 'Error'

    def_return = {'x_obs':x_obs, 'y_obs':y_obs, 'y_obs_fit':y_obs_fit, 'x_prj':x_prj, 'y_prj':y_prj,
                  'Coefs':model_coefs, 'Residuals':model_residuals,'R2':model_r2, 'Msg':model_msg, 'Type':model_type}
    return def_return

