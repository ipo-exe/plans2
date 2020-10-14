# ________________________________________________________________________
#       UFRGS - UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL
#           IPH - INSTITUTO DE PESQUISAS HIDRAULICAS
#
#     Research Group in Water Resources Management and Planning - WARP
#                    https://www.ufrgs.br/warp
#           Porto Alegre, Rio Grande do Sul, Brazil
# ________________________________________________________________________
#
# Author: IPORÃ BRITO POSSANTTI, Environmental Engineer
# Contact: possantti@gmail.com
# Date of creation: December of 2019

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def sample(p0, p1, p2='sample', title='Title', xlbl='X', ylbl='Y'):
    """

    :param p0: data
    :param p1: destination dir
    :param p2: file name
    :return:
    """
    x = p0
    n = np.random.normal(1, 2, size=np.shape(x))
    y = (x + n) * (x + n)
    afont = {'fontname': 'Arial'}  # font name
    fig, axs = plt.subplots(1, 1, figsize=(7, 6))
    axs.set_title(title, fontsize=12, fontweight='bold', **afont)
    axs.set_xlabel(xlbl, fontsize=12, **afont)
    axs.set_ylabel(ylbl, fontsize=12, **afont)
    axs.plot(x, y, 'ko')
    fig.tight_layout()
    def_aux_str = p1 + '/' + p2 + '.png'
    fig.savefig(def_aux_str)
    plt.close()


def viz_climate_scenario(p0, p1, data, ttl='Precipitation scenario', xlbl='Years', ylbl='mm'):
    fig = plt.figure(figsize=(9, 8))  # Width, Height
    gs = mpl.gridspec.GridSpec(3, 3, wspace=0.5, hspace=0.6)
    #
    afont = {'fontname': 'Arial'}
    fontttl = 11
    fontx = 10
    fonty = 10
    fontleg = 9
    dpi = 600
    #
    # P time series
    plt.subplot(gs[0, 0:])
    plt.title( r'$\bf{' + 'a.  ' + '}$' + 'Precipitation', fontsize=fontttl, loc='left', **afont)
    plt.ylabel(ylbl, **afont)
    plt.xlabel(xlbl, **afont)
    ymax_lst = list()
    xprj = data['Dts_prj']
    yprj = data['P_prj']
    ymax_lst.append(max(yprj))
    plt.plot(np.nan, '-', color='navy')  # fake line
    plt.plot(xprj, yprj, '-',color='tab:cyan')
    # plot obs data:
    for i in range(0, len(data['Dts_obs_yr'])):
        start = data['Dts_obs_yr'][i][0]
        end = data['Dts_obs_yr'][i][-1]
        lcl_x = pd.date_range(start, end)
        lcl_y = data['P_obs_yr'][i]
        ymax_lst.append(max(lcl_y))
        plt.plot(lcl_x, lcl_y, '-', color='navy')
    ymax = max(ymax_lst)
    plt.ylim(0, 1.333 * ymax)
    plt.legend(('Observed data', 'Model projection'), ncol=2, frameon=False, loc='upper left')
    #
    # box 1 accum
    plt.subplot(gs[1, 0])
    plt.boxplot((data['AP_obs'], data['AP_prj']))
    plt.title( r'$\bf{' + 'b.  ' + '}$' + 'Accumulated\n   precipitation', fontsize=fontttl, loc='left', **afont)
    plt.ylabel('mm/yr', **afont)
    plt.xticks((1, 2), ('Observed', 'Projected'))
    # box 2 accum
    plt.subplot(gs[1, 1])
    plt.boxplot((data['TRD_obs'], data['TRD_prj']))
    plt.title( r'$\bf{' + 'c.  ' + '}$' + 'Total rainy days', fontsize=fontttl, loc='left', **afont)
    plt.ylabel('days/yr', **afont)
    plt.xticks((1, 2), ('Observed', 'Projected'))
    # box 3 accum
    plt.subplot(gs[1, 2])
    plt.boxplot((data['ARB_obs'], data['ARB_prj']))
    plt.title( r'$\bf{' + 'd.  ' + '}$' + 'Mean event length', fontsize=fontttl, loc='left', **afont)
    plt.ylabel('days', **afont)
    plt.xticks((1, 2), ('Observed', 'Projected'))
    #
    # PET time series
    plt.subplot(gs[2, 0:])
    plt.title( r'$\bf{' + 'e.  ' + '}$' + 'Potential evapotranspiration', fontsize=fontttl, loc='left', **afont)
    plt.ylabel(ylbl, **afont)
    plt.xlabel(xlbl, **afont)
    ymax_lst = list()
    xprj = data['Dts_prj']
    yprj = data['PET_prj']
    ymax_lst.append(max(yprj))
    plt.plot(np.nan, '-', color='tab:red')
    plt.plot(xprj, yprj, '-', color='tab:orange')
    # plot obs data:
    for i in range(0, len(data['Dts_obs_yr'])):
        start = data['Dts_obs_yr'][i][0]
        end = data['Dts_obs_yr'][i][-1]
        lcl_x = pd.date_range(start, end)
        lcl_y = data['PET_obs_yr'][i]
        ymax_lst.append(max(lcl_y))
        plt.plot(lcl_x, lcl_y, '-', color='tab:red')
    ymax = max(ymax_lst)
    plt.ylim(0, 1.333 * ymax)
    plt.legend(('Observed data', 'Model projection'), ncol=2, frameon=False, loc='upper left')
    #
    # save
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=dpi)
    plt.close()
    return def_exp


def viz_scenario(p0, p1, xobs, yobs, yobsfit, xprj, yprj, ttl='title', xlbl='Years', ylbl='Y'):
    """

    :param p0: directory
    :param p1: filename
    :param xobs:
    :param yobs:
    :param yobsfit:
    :param xprj:
    :param yprj:
    :param ttl:
    :param xlbl:
    :param ylbl:
    :return:
    """
    fig, axs = plt.subplots(1, 1, figsize=(9, 4))
    afont = {'fontname': 'Arial'}  # font name
    axs.set_title(ttl, fontsize=12, fontweight='bold', **afont)
    axs.set_xlabel(xlbl, fontsize=12, **afont)
    axs.set_ylabel(ylbl, fontsize=12, **afont)
    axs.ticklabel_format(style='plain', axis='y')

    axs.plot(xobs, yobsfit, '-', color='tab:red')
    axs.plot(xprj, yprj, '--', color='tab:red')
    axs.plot(xobs, yobs, 'ko')
    plt.legend(('Model fit', 'Model projection', 'Observed data'))
    fig.tight_layout()
    def_exp = p0 + '/' + p1 + '.png'
    fig.savefig(def_exp, dpi=300)
    plt.close()
    return def_exp


def viz_dp(p0, p1, p3, p4, title='DP network', xlbl='Planning years', ylbl='Expansion of NBS (%)',
           d='./runbin', n='', dpi=400):
    """

    :param p0: stage list
    :param p1: state list
    :param p3: plot_links list
    :param p4: dp output pathway (states list S(t))
    :param title:
    :param xlbl:
    :param ylbl:
    :param d:
    :param n:
    :param dpi:
    :return:
    """
    fig, axs = plt.subplots(1, 1, figsize=(7, 6))
    afont = {'fontname': 'Arial'}  # font name
    axs.set_title(title, fontsize=12, fontweight='bold', **afont)
    axs.set_xlabel(xlbl, fontsize=12, **afont)
    axs.set_ylabel(ylbl, fontsize=12, **afont)
    # plot all links
    for e in p3:
        axs.plot(e[0], e[1], color='#7E7E7E', linewidth=1.5)
    # plot optimal expansion pathway
    axs.plot(p0, p4, color='#008300', linewidth=8)
    # plot grid overlay
    for t in p0:
        if t == p0[0]:
            axs.plot(t, p1[0], 'o', color='k', markersize=2)
        else:
            for s in p1:
                axs.plot(t, s, 'o', color='k', markersize=2)
    fig.tight_layout()
    aux_str = d + '/DP-viz01_' + n + '.png'
    fig.savefig(aux_str, dpi=dpi)
    plt.close()
    return aux_str


def viz_hydro_curves(p0, p1, data_curves, data_cn='1'):
    fig = plt.figure(figsize=(5, 5))
    gs = mpl.gridspec.GridSpec(1, 1, wspace=0.5, hspace=0.5, top=0.8, bottom=0.2, left=0.2, right=0.95)
    afont = {'fontname': 'Arial'}
    fontx = 10
    fonty = 10
    fontttl = 11
    fontleg = 9
    #
    # ys:
    '''x = np.linspace(1, 100, 1000)
    y1 = np.sort(np.random.uniform(500, 1000, size=np.shape(x)))
    y2 = np.sort(np.random.uniform(50, 1000, size=np.shape(x)))
    y3 = np.sort(np.random.uniform(300, 1000, size=np.shape(x)))
    y4 = np.sort(np.random.uniform(200, 1000, size=np.shape(x)))
    y5 = np.sort(np.random.uniform(10, 1000, size=np.shape(x)))
    y6 = np.sort(np.random.uniform(1, 1000, size=np.shape(x)))'''
    #
    x = data_curves['Exeed']
    y1 = data_curves['Ref']
    y2 = data_curves['Forest']
    y3 = data_curves['Grass']
    y4 = data_curves['Crops']
    y5 = data_curves['50']
    y6 = data_curves['90']
    #
    plt.subplot(gs[0, 0])
    plt.plot(x, y1, color='tab:blue', linewidth=3, label='Reference LULC')
    plt.plot(x, y2, color='forestgreen', label='Full NBS forest')
    plt.plot(x, y3, color='yellowgreen', label='Full NBS pasture')
    plt.plot(x, y4, color='olive', label='Full NBS crops')
    plt.plot(x, y5, color='goldenrod', label='50% deforest.')
    plt.plot(x, y6, color='tab:red', label='90% deforest.')
    plt.title('Simulated streamflow cumulative frequency ', fontsize=fontttl, **afont)
    plt.xlabel('Exceedance probability (%)', fontsize=fontx, **afont)
    plt.ylabel('m3/s', fontsize=fonty, **afont)
    aux_tpl = (y1, y2, y3, y4, y5, y6)
    plt.ylim(0.8 * np.min(aux_tpl), 3 * np.max(aux_tpl))
    plt.yscale('log')
    plt.legend(fontsize=fontleg, loc='best', ncol=1, frameon=False, framealpha=1)
    #plt.grid()
    # plt.show()
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=600)
    plt.close()
    return def_exp


def viz_hydro_sim(p0, p1, data_out, data_curves):
    fig = plt.figure(figsize=(9, 10)) # Width, Height
    gs = mpl.gridspec.GridSpec(5, 3, wspace=0.4, hspace=0.6, top=0.95, bottom=0.1, left=0.1, right=0.95)
    afont = {'fontname': 'Arial'}
    fontx = 9
    fonty = 9
    fontttl = 10
    fontleg = 8
    xlbls = 'Simulation period (days)'
    ylbls = ('mm', 'mm', 'mm', 'm3/s')
    #
    # get data
    x = data_out['Step']
    #
    ind = 0
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'a.  ' + '}$' + 'Observed precipitation'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.2 * np.max(data_out['P'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['P'], color='tab:blue')
    #
    ind = 1
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'b.  ' + '}$' + 'Simulated evapotranspiration'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['PET'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['PET'], color='maroon')
    plt.plot(x, data_out['ET'], color='tab:red')
    plt.legend(('Potential ET', 'Simulated ET'), ncol=2, fontsize=fontleg, loc='upper right', frameon=False)
    #
    # c. water stocks
    ind = 2
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'c.  ' + '}$' + 'Simulated land water stocks'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['Iafmax'] + data_out['Swmax'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['Swmax'], '-', color='wheat', linewidth=3.5)
    plt.plot(x, data_out['Iafmax'] + data_out['Swmax'], '--', color='tab:green')
    plt.plot(x, data_out['Swmax'] - data_out['Rzd'], '--', color='olive')
    plt.plot(x, data_out['Sfw'] + data_out['Swmax'], color='lightseagreen')
    plt.plot(x, data_out['Sw'], color='navy')
    plt.legend(('Surface level', 'Abstraction limit', 'Root zone limit', 'Surface water', 'Subsurface water'),
               ncol=5, fontsize=fontleg, loc='upper right', frameon=False)
    #
    # d.  Streamflow
    ind = 3
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'd.  ' + '}$' + 'Simulated streamflow'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['Q'])
    ymin = np.min(data_out['Q']) * 0.8
    plt.ylim(ymin, ymax)
    plt.plot(np.nan, color='tab:blue')
    plt.plot(x, data_out['Qb'] + 0.01, color='tab:cyan')
    plt.plot(x, data_out['Q'] + 0.01, color='tab:blue')
    # plt.yscale('log')
    plt.legend(('Simulated streamflow', 'Simulated baseflow'), fontsize=fontleg, ncol=3,
               loc='upper right', frameon=False)
    #
    # e.  Frequency curves (CFC)
    ind = 4
    plt.subplot(gs[ind, 0])
    aux_str = r'$\bf{' + 'e. ' + '}$' + 'Frequency curve (CFC)'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Exceedance probability (%)', fontsize=fontx, **afont)
    plt.ylabel('m3/s', fontsize=fonty, **afont)
    plt.yscale('log')
    ymax = 1.2 * np.max(data_curves['CFC'])
    ymin = np.min(data_curves['CFC'])
    plt.ylim(ymin, ymax)
    texty = (0.01 * ymax) + ymin
    textx = 0.05 * 100
    plt.plot(data_curves['Exeed'], data_curves['CFC'], color='tab:blue')
    #
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=600)
    plt.close()
    return def_exp


def viz_hydro_hru_sim(p0, p1, data_out, data_curves):
    fig = plt.figure(figsize=(9, 10)) # Width, Height
    gs = mpl.gridspec.GridSpec(5, 3, wspace=0.4, hspace=0.6, top=0.95, bottom=0.1, left=0.1, right=0.95)
    afont = {'fontname': 'Arial'}
    fontx = 9
    fonty = 9
    fontttl = 10
    fontleg = 8
    xlbls = 'Simulation period (days)'
    ylbls = ('mm', 'mm', 'mm', 'm3/s')
    #
    # get data
    x = data_out['Step']
    #
    ind = 0
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'a.  ' + '}$' + 'Observed precipitation'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.2 * np.max(data_out['P'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['P'], color='tab:blue')
    #
    ind = 1
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'b.  ' + '}$' + 'Simulated evapotranspiration'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['PET'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['PET'], color='maroon')
    plt.plot(x, data_out['ET'], color='tab:red')
    plt.legend(('Potential ET', 'Simulated ET'), ncol=2, fontsize=fontleg, loc='upper right', frameon=False)
    #
    # c. water stocks
    ind = 2
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'c.  ' + '}$' + 'Simulated land water stocks (averaged for all HRU)'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['Iamax'] + data_out['Swmax'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['Swmax'], '-', color='wheat', linewidth=3.5)
    plt.plot(x, data_out['Iamax'] + data_out['Swmax'], '--', color='tab:green')
    plt.plot(x, data_out['Swmax'] - data_out['Rzd'], '--', color='olive')
    plt.plot(x, data_out['Sfw'] + data_out['Swmax'], color='lightseagreen')
    plt.plot(x, data_out['Sw'], color='navy')
    plt.legend(('Surface level', 'Abstraction limit', 'Root zone limit', 'Surface water', 'Subsurface water'),
               ncol=5, fontsize=fontleg, loc='upper right', frameon=False)
    #
    # d.  Streamflow
    ind = 3
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'd.  ' + '}$' + 'Simulated streamflow'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['Q'])
    ymin = np.min(data_out['Q']) * 0.8
    plt.ylim(ymin, ymax)
    plt.plot(np.nan, color='tab:blue')
    plt.plot(x, data_out['Qb'] + 0.01, color='tab:cyan')
    plt.plot(x, data_out['Q'] + 0.01, color='tab:blue')
    # plt.yscale('log')
    plt.legend(('Simulated streamflow', 'Simulated baseflow'), fontsize=fontleg, ncol=3,
               loc='upper right', frameon=False)
    #
    # e.  Frequency curves (CFC)
    ind = 4
    plt.subplot(gs[ind, 0])
    aux_str = r'$\bf{' + 'e. ' + '}$' + 'Frequency curve (CFC)'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Exceedance probability (%)', fontsize=fontx, **afont)
    plt.ylabel('m3/s', fontsize=fonty, **afont)
    plt.yscale('log')
    ymax = 1.2 * np.max(data_curves['CFC'])
    ymin = np.min(data_curves['CFC'])
    plt.ylim(ymin, ymax)
    #plt.xlim(0, 100)
    texty = (0.01 * ymax) + ymin
    textx = 0.05 * 100
    plt.plot(data_curves['Exeed'][1:], data_curves['CFC'][1:], color='tab:blue')
    #
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=600)
    plt.close()
    return def_exp


def viz_hydro_pannel(p0, p1, data_out, data_metrics, data_curves):
    fig = plt.figure(figsize=(9, 10))
    gs = mpl.gridspec.GridSpec(5, 3, wspace=0.4, hspace=0.6, top=0.95, bottom=0.1, left=0.1, right=0.95)
    afont = {'fontname': 'Arial'}
    fontx = 9
    fonty = 9
    fontttl = 10
    fontleg = 8
    xlbls = 'Simulation period (days)'
    ylbls = ('mm', 'mm', 'mm', 'm3/s')
    #
    # get data
    x = data_out['Step']
    #
    ind = 0
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'a.  ' + '}$' + 'Observed precipitation'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.2 * np.max(data_out['P'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['P'], color='tab:blue')
    #
    ind = 1
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'b.  ' + '}$' + 'Simulated evapotranspiration'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['PET'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['PET'], color='maroon')
    plt.plot(x, data_out['ET'], color='tab:red')
    plt.legend(('Potential ET', 'Simulated ET'), ncol=2, fontsize=fontleg, loc='upper right', frameon=False)
    #
    # c. water stocks
    ind = 2
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'c.  ' + '}$' + 'Simulated land water stocks'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['Iafmax'] + data_out['Swmax'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['Swmax'], '-', color='wheat', linewidth=3.5)
    plt.plot(x, data_out['Iafmax'] + data_out['Swmax'], '--', color='tab:green')
    plt.plot(x, data_out['Swmax'] - data_out['Rzd'], '--', color='olive')
    plt.plot(x, data_out['Sfw'] + data_out['Swmax'], color='lightseagreen')
    plt.plot(x, data_out['Sw'], color='navy')
    plt.legend(('Surface level', 'Abstraction limit', 'Root zone limit', 'Surface water', 'Subsurface water'), ncol=5,
               fontsize=fontleg, loc='upper right', frameon=False)
    #
    # d.  Streamflow
    ind = 3
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'd.  ' + '}$' + 'Observed and simulated streamflow'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['Qobs'])
    ymin = np.min(data_out['Qobs']) * 0.8
    plt.ylim(ymin, ymax)
    texty = 0.5 * ymax
    textx = 0
    aux_str = 'NSE= {:.3f}\nNSE(log)= {:.3f}\nPBias= {:.1f}%\n'.format(data_metrics['NSE'], data_metrics['NSELOG'],
                                                                     data_metrics['PBias'])
    plt.annotate(s=aux_str, xy=(textx, texty), fontsize=fontx)
    plt.plot(x, data_out['Qobs'] + 0.01, color='tab:orange')
    plt.plot(np.nan, color='tab:blue')  # fake line
    plt.plot(x, data_out['Qb'] + 0.01, color='tab:cyan')
    plt.plot(x, data_out['Q'] + 0.01, color='tab:blue')
    # plt.yscale('log')
    plt.legend(('Observed streamflow', 'Simulated streamflow', 'Simulated baseflow'),
                 fontsize=fontleg, ncol=3, loc='upper right', frameon=False)
    #
    # e.  Flow correlation
    ind = 4
    plt.subplot(gs[ind, 0])
    aux_str = r'$\bf{' + 'e. ' + '}$' + 'Flow correlation'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Observed (m3/s)', fontsize=fontx, **afont)
    plt.ylabel('Simulated (m3/s)', fontsize=fonty, **afont)
    ymax = 1.2 * np.max((data_out['Q'], data_out['Qobs']))
    xmax = ymax
    plt.ylim(0, ymax)
    plt.xlim(0, xmax)
    texty = 0.9 * ymax
    textx = 0.05 * xmax
    plt.annotate(s='R= {:.3f}'.format(data_metrics['R']), xy=(textx, texty), fontsize=fontx)
    plt.plot(data_out['Qobs'], data_out['Qobs'], '-', color='tab:grey', alpha=0.5)
    plt.scatter(data_out['Qobs'], data_out['Q'], color='k', marker='.', alpha=0.25, edgecolors='none')
    #
    # f.  Frequency curves (CFC)
    ind = 4
    plt.subplot(gs[ind, 1])
    aux_str = r'$\bf{' + 'f. ' + '}$' + 'Frequency curves (CFC)'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Exceedance probability (%)', fontsize=fontx, **afont)
    plt.ylabel('m3/s', fontsize=fonty, **afont)
    plt.yscale('log')
    ymax = 1.2 * np.max((data_curves['CFCsim'], data_curves['CFCobs']))
    ymin = np.min((data_curves['CFCsim'], data_curves['CFCobs']))
    plt.ylim(ymin, ymax)
    texty = (0.01 * ymax) + ymin
    textx = 0.05 * 100
    plt.annotate(s='RMSE(log)= {:.3f}'.format(data_metrics['RMSELOG_CFC']), xy=(textx, texty), fontsize=fontx)
    plt.plot(data_curves['Exeed'], data_curves['CFCobs'], color='tab:orange')
    plt.plot(data_curves['Exeed'], data_curves['CFCsim'], color='tab:blue')
    plt.legend(('Observed CFC', 'Simulated CFC'), fontsize=fontleg, ncol=1, loc='upper right', frameon=False)
    #
    # g.  CFC correlation
    ind = 4
    plt.subplot(gs[ind, 2])
    aux_str = r'$\bf{' + 'g. ' + '}$' + 'CFC correlation'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Observed (m3/s)', fontsize=fontx, **afont)
    plt.ylabel('Simulated (m3/s)', fontsize=fonty, **afont)
    ymax = 1.2 * np.max((data_curves['CFCsim'], data_curves['CFCobs']))
    xmax = ymax
    plt.ylim(0, ymax)
    plt.xlim(0, xmax)
    texty = 0.9 * ymax
    textx = 0.05 * xmax
    plt.annotate(s='R= {:.3f}'.format(data_metrics['R_CFC']), xy=(textx, texty), fontsize=fontx)
    plt.scatter(data_curves['CFCobs'], data_curves['CFCsim'],
                color='navy', marker='.', alpha=0.3, edgecolors='none')
    plt.plot(data_curves['CFCobs'], data_curves['CFCobs'], '-', color='tab:grey', alpha=0.5)
    # plt.show()
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=600)
    plt.close()
    return def_exp


def viz_hydro_hru_pannel(p0, p1, data_out, data_metrics, data_curves):
    fig = plt.figure(figsize=(9, 10))
    gs = mpl.gridspec.GridSpec(5, 3, wspace=0.4, hspace=0.6, top=0.95, bottom=0.1, left=0.1, right=0.95)
    afont = {'fontname': 'Arial'}
    fontx = 9
    fonty = 9
    fontttl = 10
    fontleg = 8
    xlbls = 'Simulation period (days)'
    ylbls = ('mm', 'mm', 'mm', 'm3/s')
    #
    # get data
    x = data_out['Step']
    #
    ind = 0
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'a.  ' + '}$' + 'Observed precipitation'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.2 * np.max(data_out['P'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['P'], color='tab:blue')
    #
    ind = 1
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'b.  ' + '}$' + 'Simulated evapotranspiration'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['PET'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['PET'], color='maroon')
    plt.plot(x, data_out['ET'], color='tab:red')
    plt.legend(('Potential ET', 'Simulated ET'), ncol=2, fontsize=fontleg, loc='upper right', frameon=False)
    #
    # c. water stocks
    ind = 2
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'c.  ' + '}$' + 'Simulated land water stocks'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['Iamax'] + data_out['Swmax'])
    plt.ylim(0, ymax)
    plt.plot(x, data_out['Swmax'], '-', color='wheat', linewidth=3.5)
    plt.plot(x, data_out['Iamax'] + data_out['Swmax'], '--', color='tab:green')
    plt.plot(x, data_out['Swmax'] - data_out['Rzd'], '--', color='olive')
    plt.plot(x, data_out['Sfw'] + data_out['Swmax'], color='lightseagreen')
    plt.plot(x, data_out['Sw'], color='navy')
    plt.legend(('Surface level', 'Abstraction limit', 'Root zone limit', 'Surface water', 'Subsurface water'), ncol=5,
               fontsize=fontleg, loc='upper right', frameon=False)
    #
    # d.  Streamflow
    ind = 3
    plt.subplot(gs[ind, :])
    aux_str = r'$\bf{' + 'd.  ' + '}$' + 'Observed and simulated streamflow'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = 1.5 * np.max(data_out['Qobs'])
    ymin = np.min(data_out['Qobs']) * 0.8
    plt.ylim(ymin, ymax)
    texty = 0.5 * ymax
    textx = 0
    aux_str = 'NSE= {:.3f}\nNSE(log)= {:.3f}\nPBias= {:.1f}%\n'.format(data_metrics['NSE'], data_metrics['NSELOG'],
                                                                     data_metrics['PBias'])
    plt.annotate(s=aux_str, xy=(textx, texty), fontsize=fontx)
    plt.plot(x, data_out['Qobs'] + 0.01, color='tab:orange')
    plt.plot(np.nan, color='tab:blue')  # fake line
    plt.plot(x, data_out['Qb'] + 0.01, color='tab:cyan')
    plt.plot(x, data_out['Q'] + 0.01, color='tab:blue')
    # plt.yscale('log')
    plt.legend(('Observed streamflow', 'Simulated streamflow', 'Simulated baseflow'),
                 fontsize=fontleg, ncol=3, loc='upper right', frameon=False)
    #
    # e.  Flow correlation
    ind = 4
    plt.subplot(gs[ind, 0])
    aux_str = r'$\bf{' + 'e. ' + '}$' + 'Flow correlation'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Observed (m3/s)', fontsize=fontx, **afont)
    plt.ylabel('Simulated (m3/s)', fontsize=fonty, **afont)
    ymax = 1.2 * np.max((data_out['Q'], data_out['Qobs']))
    xmax = ymax
    plt.ylim(0, ymax)
    plt.xlim(0, xmax)
    texty = 0.9 * ymax
    textx = 0.05 * xmax
    plt.annotate(s='R= {:.3f}'.format(data_metrics['R']), xy=(textx, texty), fontsize=fontx)
    plt.plot(data_out['Qobs'], data_out['Qobs'], '-', color='tab:grey', alpha=0.5)
    plt.scatter(data_out['Qobs'], data_out['Q'], color='k', marker='.', alpha=0.25, edgecolors='none')
    #
    # f.  Frequency curves (CFC)
    ind = 4
    plt.subplot(gs[ind, 1])
    aux_str = r'$\bf{' + 'f. ' + '}$' + 'Frequency curves (CFC)'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Exceedance probability (%)', fontsize=fontx, **afont)
    plt.ylabel('m3/s', fontsize=fonty, **afont)
    plt.yscale('log')
    ymax = 1.2 * np.max((data_curves['CFCsim'], data_curves['CFCobs']))
    ymin = np.min((data_curves['CFCsim'], data_curves['CFCobs']))
    plt.ylim(ymin, ymax)
    texty = (0.01 * ymax) + ymin
    textx = 0.05 * 100
    plt.annotate(s='RMSE(log)= {:.3f}'.format(data_metrics['RMSELOG_CFC']), xy=(textx, texty), fontsize=fontx)
    plt.plot(data_curves['Exeed'], data_curves['CFCobs'], color='tab:orange')
    plt.plot(data_curves['Exeed'], data_curves['CFCsim'], color='tab:blue')
    plt.legend(('Observed CFC', 'Simulated CFC'), fontsize=fontleg, ncol=1, loc='upper right', frameon=False)
    #
    # g.  CFC correlation
    ind = 4
    plt.subplot(gs[ind, 2])
    aux_str = r'$\bf{' + 'g. ' + '}$' + 'CFC correlation'
    plt.title(aux_str, fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Observed (m3/s)', fontsize=fontx, **afont)
    plt.ylabel('Simulated (m3/s)', fontsize=fonty, **afont)
    ymax = 1.2 * np.max((data_curves['CFCsim'], data_curves['CFCobs']))
    xmax = ymax
    plt.ylim(0, ymax)
    plt.xlim(0, xmax)
    texty = 0.9 * ymax
    textx = 0.05 * xmax
    plt.annotate(s='R= {:.3f}'.format(data_metrics['R_CFC']), xy=(textx, texty), fontsize=fontx)
    plt.scatter(data_curves['CFCobs'], data_curves['CFCsim'],
                color='navy', marker='.', alpha=0.3, edgecolors='none')
    plt.plot(data_curves['CFCobs'], data_curves['CFCobs'], '-', color='tab:grey', alpha=0.5)
    # plt.show()
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=600)
    plt.close()
    return def_exp


def viz_hydro_sal_cfcs(p0, p1, cfcs):
    fig = plt.figure(figsize=(9, 6))
    gs = mpl.gridspec.GridSpec(2, 2, wspace=0.3, hspace=0.5, top=0.95, bottom=0.1, left=0.1, right=0.95)
    #
    afont = {'fontname': 'Arial'}
    fontttl = 11
    fontx = 10
    fonty = 10
    fontleg = 7
    dpi = 600
    line_base = 3.5
    aux_tpl = ('a. ', 'b. ', 'c. ', 'd. ')
    ttls = ('Streamflow Cumulative Freq. Curves (CFCs)', 'Stormflow CFCs', 'Baseflow CFCs', 'Baseflow/Streamflow Ratio CFCs')
    ylbls = ('m3/s', 'm3/s', 'm3/s', '%')
    leg_lbls = ('Reference LULC', 'Full NBS forest', 'Full NBS pasture',
                'Full NBS crops', '50% deforest.', '90% deforest.')
    leg_sufix = ('L0', 'L1', 'L2', 'L3', 'L4', 'L5')
    #
    slice = 1
    x = cfcs['Exeed'][slice:]
    #
    ind = 0
    plt.subplot(gs[0, 0])
    plt.title(r'$\bf{' + aux_tpl[ind] + '}$' + ttls[ind], fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Exceedance probability (%)', fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    plt.plot(x, cfcs['lulc_ref_Q'][slice:], color='tab:blue', linewidth=3, label=leg_sufix[0] + ' - '+ leg_lbls[0])
    plt.plot(x, cfcs['lulc_nbsf_Q'][slice:], color='forestgreen', label=leg_sufix[1] + ' - '+ leg_lbls[1])
    plt.plot(x, cfcs['lulc_nbsp_Q'][slice:], color='yellowgreen', label=leg_sufix[2] + ' - '+ leg_lbls[2])
    plt.plot(x, cfcs['lulc_nbsc_Q'][slice:], color='olive', label=leg_sufix[3] + ' - '+ leg_lbls[3])
    plt.plot(x, cfcs['lulc_d50_Q'][slice:], color='goldenrod', label=leg_sufix[4] + ' - '+ leg_lbls[4])
    plt.plot(x, cfcs['lulc_d90_Q'][slice:], color='tab:red', label=leg_sufix[5] + ' - '+ leg_lbls[5])
    plt.yscale('log')
    plt.legend(fontsize=fontleg, loc='best', ncol=1, frameon=False, framealpha=1)
    #
    ind = 1
    plt.subplot(gs[0, 1])
    plt.title(r'$\bf{' + aux_tpl[ind] + '}$' + ttls[ind], fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Exceedance probability (%)', fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    plt.plot(x, cfcs['lulc_ref_Qs'][slice:], color='tab:blue', linewidth=3, label=leg_sufix[0])
    plt.plot(x, cfcs['lulc_nbsf_Qs'][slice:], color='forestgreen', label=leg_sufix[1])
    plt.plot(x, cfcs['lulc_nbsp_Qs'][slice:], color='yellowgreen', label=leg_sufix[2])
    plt.plot(x, cfcs['lulc_nbsc_Qs'][slice:], color='olive', label=leg_sufix[3])
    plt.plot(x, cfcs['lulc_d50_Qs'][slice:], color='goldenrod', label=leg_sufix[4])
    plt.plot(x, cfcs['lulc_d90_Qs'][slice:], color='tab:red', label=leg_sufix[5])
    plt.ylim(1, np.max(cfcs['lulc_ref_Qs'][1:]))
    plt.yscale('log')
    plt.legend(fontsize=fontleg, loc='best', ncol=1, frameon=False, framealpha=1)
    #
    ind = 2
    plt.subplot(gs[1, 0])
    plt.title(r'$\bf{' + aux_tpl[ind] + '}$' + ttls[ind], fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Exceedance probability (%)', fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    plt.plot(x, cfcs['lulc_ref_Qb'][slice:], color='tab:blue', linewidth=3, label=leg_sufix[0])
    plt.plot(x, cfcs['lulc_nbsf_Qb'][slice:], color='forestgreen', label=leg_sufix[1])
    plt.plot(x, cfcs['lulc_nbsp_Qb'][slice:], color='yellowgreen', label=leg_sufix[2])
    plt.plot(x, cfcs['lulc_nbsc_Qb'][slice:], color='olive', label=leg_sufix[3])
    plt.plot(x, cfcs['lulc_d50_Qb'][slice:], color='goldenrod', label=leg_sufix[4])
    plt.plot(x, cfcs['lulc_d90_Qb'][slice:], color='tab:red', label=leg_sufix[5])
    plt.legend(fontsize=fontleg, loc='best', ncol=1, frameon=False, framealpha=1)
    # plt.yscale('log')
    ind = 3
    plt.subplot(gs[1, 1])
    plt.title(r'$\bf{' + aux_tpl[ind] + '}$' + ttls[ind], fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Exceedance probability (%)', fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    plt.plot(x, cfcs['lulc_ref_Qbf'][slice:], color='tab:blue', linewidth=3, label=leg_sufix[0])
    plt.plot(x, cfcs['lulc_nbsf_Qbf'][slice:], color='forestgreen', label=leg_sufix[1])
    plt.plot(x, cfcs['lulc_nbsp_Qbf'][slice:], color='yellowgreen', label=leg_sufix[2])
    plt.plot(x, cfcs['lulc_nbsc_Qbf'][slice:], color='olive', label=leg_sufix[3])
    plt.plot(x, cfcs['lulc_d50_Qbf'][slice:], color='goldenrod', label=leg_sufix[4])
    plt.plot(x, cfcs['lulc_d90_Qbf'][slice:], color='tab:red', label=leg_sufix[5])
    plt.legend(fontsize=fontleg, loc='best', ncol=1, frameon=False, framealpha=1)
    # plt.show()
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=600)
    plt.close()
    return def_exp


def viz_hydro_cloud(p0, p1, x, y, z, w, m):
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.set_xlabel("Iaf")
    ax.set_ylabel("SWmax")
    ax.set_zlabel("GWmax")
    ax.scatter3D(x, y, z, c=m, cmap='jet', marker='.')
    ax.grid(False)
    # second plot
    ax = fig.add_subplot(1, 2, 2, projection='3d')
    ax.set_xlabel("SWmax")
    ax.set_ylabel("GWmax")
    ax.set_zlabel("K-Nash")
    ax.scatter3D(y, z, w, c=m, cmap='jet', marker='.')
    ax.grid(False)
    #plt.show()
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=400)
    plt.close()
    return def_exp


def viz_dp_pannel(p0, p1, data_dpin, data_dpout, xlbls='Planning horizon (years)', sim=False):
    fig = plt.figure(figsize=(9, 8))
    gs = mpl.gridspec.GridSpec(3, 2, wspace=0.3, hspace=0.5, top=0.95, bottom=0.1, left=0.1, right=0.95)
    #
    afont = {'fontname': 'Arial'}
    fontttl = 11
    fontx = 10
    fonty = 10
    fontleg = 7
    dpi = 600
    line_base = 3.5
    curf = 1000000  # million
    aux_tpl = ('a. ', 'b. ', 'c. ', 'd. ', 'e. ', 'f. ')
    ttls = ('Total cost projection', 'Costs projections', 'Expansion pathway',
             'Optimal LULC change', 'Scarcity risk', 'Water availability')
    if sim:
        ttls = ('Total cost projection', 'Costs projections', 'Expansion pathway',
                'Simulated LULC change', 'Scarcity risk', 'Water availability')
    ylbls = ('Million $', 'Million $', '% of available area', '% of watershed area', 'ok5', 'ok6')
    #
    # dig up the data:
    x = data_dpout['Stage t']  # x = (2020, 2025, 2030, 2035, 2040, 2045, 2050)
    stt_out = data_dpout['State S(t)']
    cost_opt = list()
    cost_opt_lcl = list()
    cost_base = list()
    cost_base_lcl = list()
    cost_base_s = list()
    cost_base_t = list()
    q90_base = list()
    q90_opt = data_dpout['q90']
    risk_base = list()
    risk_opt = data_dpout['Risk']
    base = data_dpout['Baseline']
    # load baseline series
    for elem in base:
        cost_base_lcl.append(elem[1]/curf)
        cost_base_s.append(elem[3][0]/curf)
        cost_base_t.append(elem[3][1]/curf)
        q90_base.append(elem[5][0])
        risk_base.append(elem[6])
    stx_opt = data_dpout['Costs STX $FV']
    cost_opt_s = list()
    cost_opt_t = list()
    cost_opt_x = list()
    # load optimal costs in FV
    for elem in stx_opt:
        cost_opt_lcl.append(elem[0]/curf)
        cost_opt_s.append(elem[1][0]/curf)
        cost_opt_t.append(elem[1][1]/curf)
        cost_opt_x.append(elem[1][2]/curf)
    # get acum costs:
    aux_flt1 = 0
    aux_flt2 = 0
    for i in range(0, len(cost_opt_lcl)):
        aux_flt1 = aux_flt1 + cost_opt_lcl[i]
        aux_flt2 = aux_flt2 + cost_base_lcl[i]
        cost_opt.append(aux_flt1)
        cost_base.append(aux_flt2)
    # get lulc
    lulc = data_dpout['LULC %']
    lulc_pasture = list()
    lulc_crops = list()
    lulc_nbs_f = list()
    lulc_nbs_p = list()
    lulc_nbs_c = list()
    for elem in lulc:
        lulc_pasture.append(elem[3])
        lulc_crops.append(elem[4])
        lulc_nbs_f.append(elem[5])
        lulc_nbs_p.append(elem[6])
        lulc_nbs_c.append(elem[7])
    stt = data_dpin[1]
    #
    #
    # optimal cost versus baseline cost in FV
    ind = 0
    plt.subplot(gs[0, 0])
    plt.title( r'$\bf{' + 'a. ' + '}$' + ttls[ind], fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    #ymax = np.max((cost_opt, cost_base))
    ymax = 26.6
    plt.ylim(-0.05 * ymax, 1.333 * ymax)
    plt.plot(x[:], cost_base[:], color='tab:orange', marker='o', linewidth=line_base)
    plt.plot(x[:], cost_opt[:], color='tab:blue', marker='.')
    aux_tpl1 = ('Baseline Policy (BP)', 'Optimal Policy (OP)')
    if sim:
        aux_tpl1 = ('Baseline Policy (BP)', 'Optimal Policy (OP)')
    plt.legend(aux_tpl1, fontsize=fontleg, loc='upper left', ncol=2, frameon=False)
    #
    #
    # local STX costs in FV
    ind = 1
    plt.subplot(gs[0, 1])
    plt.title( r'$\bf{' + 'b. ' + '}$' + ttls[ind], fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    #ymax = np.max((cost_opt_s, cost_opt_t, cost_opt_x, cost_base_s, cost_base_t))
    ymax = 6.8
    plt.ylim(-0.05 * ymax, ymax)
    plt.plot(x[:], cost_base_s[:], color='lightblue', linewidth=line_base)
    plt.plot(x[:], cost_base_t[:], color='plum', linewidth=line_base)
    plt.plot(x[:], cost_opt_s[:], color='navy')
    plt.plot(x[:], cost_opt_t[:], color='purple')
    plt.plot(x[:], cost_opt_x[:], color='tab:green')
    aux_tpl1 = ('Scarcity BP', 'Treatment BP', 'Scarcity OP', 'Treatment OP', 'Expansion OP')
    if sim:
        aux_tpl1 = ('Scarcity BP', 'Treatment BP', 'Scarcity OP', 'Treatment OP', 'Expansion OP')
    plt.legend(aux_tpl1, fontsize=fontleg, ncol=2, frameon=False)
    #
    #
    # expansion pathway
    ind = 2
    plt.subplot(gs[1, 0])
    plt.title( r'$\bf{' + 'c. ' + '}$' + ttls[ind], fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    y2 = np.random.uniform(10, 100, size=np.shape(x)) * 0
    plt.plot(x, y2, color='tab:orange', marker='o', linewidth=line_base)
    plt.plot(x, stt_out, color='tab:green', marker='.')
    plt.ylim(-5, 130)
    plt.yticks((0, 20, 40, 60, 80, 100))
    # load grid above
    for i in range(0, len(x)):
        for j in range(0, len(stt)):
            plt.plot(x[i], stt[j], '.', color='tab:gray')
    plt.plot(x, y2, color='tab:orange', marker='o')
    plt.plot(x, stt_out, color='tab:green', marker='.')
    aux_tpl1 = ('Baseline', 'Optimal', 'DP Grid')
    if sim:
        aux_tpl1 = ('Baseline', 'Simulated', 'DP Grid')
    plt.legend(aux_tpl1, loc='upper left', fontsize=fontleg,
               framealpha=1, ncol=3)
    #
    #
    # LULC change
    ind = 3
    plt.subplot(gs[1, 1])
    plt.title( r'$\bf{' + 'd. ' + '}$' + ttls[ind], fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel(ylbls[ind], fontsize=fonty, **afont)
    ymax = max(lulc_pasture) + max(lulc_crops)
    plt.ylim(0, 1.5 * ymax)
    if ymax > 100:
        yticks = (0, 20, 40, 60, 80, 100)
        plt.yticks(yticks)
    c = ('forestgreen', 'yellowgreen', 'olive', 'gold', 'goldenrod')
    lbl = ('NBS forest', 'NBS pastures', 'NBS crops', 'Conv. pastures', 'Conv. crops')
    plt.stackplot(x, lulc_nbs_f, lulc_nbs_p, lulc_nbs_c, lulc_pasture, lulc_crops, labels=lbl, colors=c)
    plt.legend(fontsize=fontleg, loc='upper left', ncol=2, frameon=False)
    #
    #
    # Scarcity risk
    ind = 4
    # y1 = np.random.uniform(10, 20, size=np.shape(x))
    y1 = risk_opt
    # y1b = np.random.uniform(10, 20, size=np.shape(x))
    y1b = risk_base
    plt.subplot(gs[2, 0])
    plt.title( r'$\bf{' + 'e. ' + '}$' + ttls[ind], fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel('%', fontsize=fonty, **afont)
    aux_str = 'Scarcity risk (OP)'
    if sim:
        aux_str = 'Scarcity risk (OP)'
    plt.plot(x, y1,'-', color='tab:red', label=aux_str)
    plt.plot(x, y1b, '--', color='tab:red', label='Scarcity risk (BP)')
    plt.ylim(0.9 * np.min((y1, y1b)), 1.3333 * np.max((y1, y1b)))
    plt.legend(frameon=False, ncol=2, loc='upper left', fontsize=fontleg)
    #
    #
    # Water availability
    ind = 5
    # y1 = np.random.uniform(10, 20, size=np.shape(x))
    y1 = q90_opt
    # y1b = np.random.uniform(10, 20, size=np.shape(x))
    y1b = q90_base
    plt.subplot(gs[2, 1])
    plt.title( r'$\bf{' + 'f.  ' + '}$' + ttls[ind], fontsize=fontttl, loc='left', **afont)
    plt.xlabel(xlbls, fontsize=fontx, **afont)
    plt.ylabel('m3/s', fontsize=fonty, **afont)
    aux_str = 'Flow 90% exeed. (OP)'
    if sim:
        aux_str = 'Flow 90% exeed. (OP)'
    plt.plot(x, y1, '-', color='tab:blue', label=aux_str)
    plt.plot(x, y1b, '--', color='tab:blue', label='Flow 90% exeed. (BP)')
    # plt.ylim(0.9 * np.min((y1, y1b)), 1.3333 * np.max((y1, y1b)))
    plt.ylim(0, 1.3333 * np.max((y1, y1b)))
    plt.legend(frameon=False, ncol=2, loc='upper left', fontsize=fontleg)
    #
    #
    # save
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=400)
    plt.close()
    return def_exp


def viz_cons_pannel(p0, p1, yrs, pop, wcons, wconsr, trff, elast, sc_param):
    fig = plt.figure(figsize=(9, 8))
    gs = mpl.gridspec.GridSpec(4, 5, wspace=0.6, hspace=0.5, top=0.95, bottom=0.1, left=0.1, right=0.98)
    #
    afont = {'fontname':'Arial'}
    fontttl = 11
    fontx = 10
    fonty = 10
    fontleg = 9
    dpi = 600
    #
    # get data:
    x = yrs
    y = np.random.normal(100, 10, size=np.shape(x))
    #
    ind = 0
    plt.subplot(gs[ind, :3])
    plt.title( r'$\bf{' + 'a.  ' + '}$' + ' Population projection',fontsize=fontttl, loc='left', **afont)
    # plt.xlabel('X label', fontsize=fontx)
    if np.max(pop) > 1000000:
        pop = pop / 1000000
        plt.ylabel('Million habitants', fontsize=fonty, **afont)
    else:
        plt.ylabel('Habitants', fontsize=fonty, **afont)
    plt.ylim(0, 1.1 * np.max(pop))
    plt.plot(x, pop, color='tab:grey', marker='.')
    #
    ind = 1
    ax1 = fig.add_subplot(gs[ind, :3])
    # plt.subplot(gs[ind, :3])
    ax1.set_title(r'$\bf{' + 'b.  ' + '}$' + ' Water consumption projection', fontsize=fontttl, loc='left', **afont)
    # plt.xlabel('X label', fontsize=fontx)
    ax1.set_ylabel('L/hab./d', fontsize=fonty, **afont)
    ax1.set_ylim(0, 1.3333 * np.max(wcons))
    ax1.plot(x, wcons, color='tab:purple', label='Per capita (L/hab/d)', marker='.')
    ax2 = ax1.twinx()
    ax2.plot(x, wconsr, color='tab:blue', marker='.')
    ax1.plot(np.nan, '-', color='tab:blue', marker='.', label='Daily volume (m3/d)')
    ax2.set_ylabel('m3/d', fontsize=fonty, **afont)
    ax2.set_ylim(0, 1.4 * np.max(wconsr))
    ax1.legend(frameon=False, ncol=2, loc='upper left', fontsize=fontleg)
    #
    ind = 2
    plt.subplot(gs[ind, :3])
    plt.title(r'$\bf{' + 'c.  ' + '}$' +' Water tariff projection', fontsize=fontttl, loc='left', **afont)
    # plt.xlabel('X label', fontsize=fontx)
    plt.ylabel('$/m3', fontsize=fonty, **afont)
    plt.plot(x, trff, color='tab:red', marker='.')
    plt.ylim(0, 1.2 * np.max(trff))
    #
    ind = 3
    plt.subplot(gs[ind, :3])
    plt.title(r'$\bf{' + 'd.  ' + '}$' + 'Price elasticity projection', fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Planning horizon (years)', fontsize=fontx, **afont)
    plt.plot(x, elast, color='tab:orange', marker='.')
    #
    ind = 2
    plt.subplot(gs[ind:, 3:])
    plt.title(r'$\bf{' + 'e.  ' + '}$' + 'Marginal benefit models', fontsize=fontttl, loc='left', **afont)
    plt.xlabel('Consumed water (hm3)', fontsize=fontx, **afont)
    plt.ylabel('Marginal benefit ($/m3)', fontsize=fonty, **afont)
    # get parameters arrays:
    a_param = sc_param['A']
    b_param = sc_param['B']
    k_param = sc_param['K']
    hec3 = 100 * 100 * 100
    xmax = 2 * np.max(wconsr) / hec3
    x_w = np.linspace(10, 2 * np.max(wconsr), 100) / hec3
    # plot fake lines for legend:
    plt.plot(np.nan, '-', color='navy', label='Linear model')
    # plt.plot(np.nan, color='navy', label='Linear model')
    plt.plot(np.nan, '.', color='black', label='Calibration pts.')
    plt.legend(loc='upper right', frameon=False, fontsize=fontleg)
    '''# plot exp curves
    for t in range(0, len(yrs)):
        # P = (W/k)^(1/e)
        y_p = np.power((x_w * hec3) / k_param[t], 1 / elast[t])
        plt.plot(x_w, y_p, '--', color='silver', label='Log model')'''
    # plot linear curves & annotate
    for t in range(0, len(yrs)):
        # P = (W - b) / a
        y_p = ((x_w * hec3)  - b_param[t]) / a_param[t]
        plt.plot(x_w, y_p, color='navy', label='Linear model')
    # plot overlay points:
    for t in range(0, len(yrs)):
        if t == 0:
            x1 = wconsr[t] / hec3
            y1 = trff[t]
        if t == len(yrs) - 1 :
            x2 = wconsr[t] / hec3
            y2 = trff[t]
        plt.plot(wconsr[t] / hec3, trff[t], '.', color='black')
    plt.xlim(0, xmax)
    plt.ylim(0, 2 * np.max(trff))
    # annotate first year:
    xtxt = 0.3 * (x1)
    ytxt = y1 / 2
    plt.annotate(str(int(yrs[0])), xy=(x1, y1), xytext=(xtxt, ytxt), fontsize=fontleg,
                 arrowprops=dict(arrowstyle='->', connectionstyle='angle3, angleA=-20,angleB=40'))
    # annotate last year:
    xtxt = (0.3 * (xmax - x2)) + x2
    ytxt = 1.3 * y2
    plt.annotate(str(int(yrs[len(yrs) - 1])), xy=(x2, y2), xytext=(xtxt, ytxt), fontsize=fontleg,
                 arrowprops=dict(arrowstyle='->', connectionstyle='angle3, angleA=-20,angleB=40'))
    #
    # plt.show()
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=dpi)
    plt.close()
    return def_exp


def viz_exp_cost(p0, p1, data, ttl, xlbl, ylbl):
    fig = plt.figure(figsize=(9, 3))
    gs = mpl.gridspec.GridSpec(1, 3, wspace=0.5, hspace=0.5, top=0.8, bottom=0.2, left=0.15, right=0.95)
    for i in range(0, 3):
        plt.subplot(gs[0, i])
        plt.title(ttl[i], fontsize=12, fontweight='bold')
        plt.ylabel(ylbl)
        plt.xlabel(xlbl)
        xobs = data[i][0]
        yobs = data[i][1]
        yfit = data[i][2]
        plt.plot(xobs, yfit, '-', color='tab:red')
        plt.plot(xobs, yobs, 'ko')
        if i == 0:
            plt.legend(('Model', 'Data'))
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=600)
    plt.close()
    return def_exp


def viz_tc_cost(p0, p1, data, ttl='Treatment cost model', xlbl='% of forested area', ylbl='$/m3'):
    fig = plt.figure(figsize=(4, 4))
    gs = mpl.gridspec.GridSpec(1, 1, wspace=0.5, hspace=0.5, top=0.8, bottom=0.2, left=0.2, right=0.95)
    plt.subplot(gs[0, 0])
    plt.plot(data['TC_x_fit'], data['TC_y_fit'], '-', color='tab:red')
    plt.plot(data['TC_x'], data['TC_y'], 'ko')
    plt.xlim((0, 100))
    plt.ylim((0, np.max(data['TC_y'] * 1.2)))
    plt.title(ttl)
    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.legend(('Model', 'Data'))
    # plt.show()
    def_exp = p0 + '/' + p1 + '.png'
    plt.savefig(def_exp, dpi=600)
    plt.close()
    return def_exp


