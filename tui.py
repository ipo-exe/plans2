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
# Date: 2020 (yes, during the pandemic)
# Description:
# this package contains a new main Terminal UI file for the PLANS

import pandas as pd
import plans2
from vizs import viz_dp_pannel, viz_hydro_sim, viz_hydro_hru_sim, viz_hydro_sal_cfcs
from tools import display, validate, stringsf, load, mytools, save
from dp import run_dp, run_sim, set_dp


def header_warp():
    """
    function to built the WARP header message
    :return: string with warp header message
    """
    def_int = 70
    def_str1 = stringsf.center('UFRGS - Universidade Federal do Rio Grande do Sul', def_int)
    def_str2 = stringsf.center('IPH - Instituto de Pesquisas Hidráulicas', def_int)
    def_str3 = stringsf.center('WARP - Research Group in Water Resources Management and Planning', def_int)
    def_str4 = stringsf.center('https://www.ufrgs.br/warp', def_int)
    def_str5 = stringsf.center('Porto Alegre, Rio Grande do Sul, Brazil', def_int)
    def_str = '\n\n' + def_str1 + '\n' + def_str2 + '\n' + def_str3 + '\n' + def_str4 + '\n' + def_str5 + '\n\n'
    return def_str


def header_plans():
    """
    built plans 2 header message
    :return: string with plans header msg
    """
    def_str0 = stringsf.title(p0='plans - planning nature-based solutions')
    def_str1 = 'Version: 2.0'
    def_str3 = 'This software is under the GNU GPL3.0 license'
    def_str4 = 'Source code repository: https://github.com/ipo-exe/plans/'
    def_str = def_str0 + '\n' + def_str1 + '\n' + def_str3 + '\n' + def_str4 + '\n\n'
    return def_str


def off_msg():
    """
    only display exiting message
    :return: none
    """
    display.str_title_clr('Exit PLANS')
    display.okinput(p1=0.6)


def newsess_msg():
    """
    display new session message
    :return: none
    """
    display.str_title_clr('PLANS new session')
    display.okinput(p1=0.6)


def msg_formats():
    """
    only display formatting requirements message
    :return: none
    """
    print('For formatting requirements, consult the documentation at:\n https://github.com/ipo-exe/plans/')


def load_dict(p0=True):
    """
    Load the dictionary iterable variable (a tuple)
    :param p0: boolean control to enter interactive menu
    :return: tuple with the language dictionary
    """
    display.str_subtitle_clr('language setup')
    # 1) get dct dataframe
    def_dct_df = pd.read_csv('dictionary.txt', ';')
    # 2) get languages names list
    def_lng_nm_tpl = tuple(def_dct_df.columns.tolist())
    # get DF array:
    def_dct_ary = tuple(def_dct_df.T.values)
    # # print(def_dct_ary[0])
    # Language menu:
    if p0:
        def_lng_nm = validate.string_menu(p0=def_lng_nm_tpl, p1='language setup')  # 3) get chosen language id
    # skip menu and go to English:
    else:
        print('Default mode on\n')
        def_lng_nm = 'English'
        def_aux_str = 'Language: ' + def_lng_nm
        display.okinput(def_aux_str)
    # 4) get language id
    def_lng_id = def_lng_nm_tpl.index(def_lng_nm)
    # 5) Find the dict
    def_dct = tuple(def_dct_ary[def_lng_id])
    # strip the chosen language dict from overall dict to tuple
    '''So here we have to wait until a fair amount of code is done to
    then manually substitute all strings into the key
    in the dictionary. But the language problem is now pretty much solved.'''
    return def_dct


def tui_open_menu(p0):
    """
    Open existing project function. An interactive menu is presented showing the projects found in the directy passed
    as the parameter.
    :param p0: PLANS2 root directory
    :return: project directory string and project file path with extension
    """
    project_ext = plans2.get_projectfile_ext()  # retrieving the project file extent
    proj_lst = plans2.list_all_projects(p0)  # listing all projects found in the directory
    aux_str1 = 'Import project from file'
    proj_lst.append(aux_str1)  # adding extra option to the menu list
    lst_menu = proj_lst[:]  # copying menu list
    # menu of available projects
    ans_menu = validate.string_menu(p0=lst_menu, p1='available projects', p2='Enter menu key: ')
    if ans_menu == aux_str1:  # importing from file option
        aux_str = project_ext + ' file'  # getting project file path
        # load from file
        pfile = load.filename_dialog(p0=project_ext, p1=aux_str, p2='select project file')
        pdir = plans2.getdata_metadata(pfile, 18) # retrieving from file path the project dir
    else:  # chosing an existing project in the directory
        pdir = p0 + '/' + ans_menu  # project directory
        pfile = pdir + '/' + ans_menu + '.' + project_ext  # project file path w/ extension
    return pdir, pfile


def tui_datasets_setup(p0, p1):
    """
    void function. It displays a menu and import the observed datasets input files
    :param p0: project file path
    :param p1: observed datasets dir
    :return: none
    """
    display.str_subtitle_clr('Import Data')  # section header
    msg_formats()  # formatting requirements
    # menu loop:
    while True:
        def_index = plans2.get_index(p0)  # get the index list
        # loop to built the list of options:
        def_lst_menu = list()
        for def_row in def_index:
            if def_row[1] == 'input':
                # built key:
                if def_row[5] == '':  # missing condition
                    def_lcl_key = 'Missing: ' + def_row[3] + ' [' + def_row[4] + '] '
                else:  # ok condition
                    def_lcl_key = '--OK-- : ' + def_row[3] + ' [' + def_row[4] + '] '
                # print(def_lcl_key)  # print inspection
                def_lst_menu.append(def_lcl_key[:])
        # display menu:
        def_aux_str2 = "Enter menu key [<e> to exit menu]: "
        def_data_key = validate.string_menu(def_lst_menu, 'data setup options', p2=def_aux_str2, p4=True)
        # exit or set data:
        if def_data_key == 'e':  # exitting
            break
        else:
            # get data label from chosen menu option
            def_data_lbl = def_data_key.split('[')[1].split(']')[0].strip()
            # loop to find in index the main line and local dir by the label:
            def_i = 0
            while True:
                if def_index[def_i][4] == def_data_lbl:
                    def_data_flnm = def_data_lbl + '.' + def_index[def_i][2]
                    def_data_line = 23 + int(def_index[def_i][0])
                    break
                else:
                    def_i = def_i + 1
            # permission protocol:
            validate.permission_protocol('Is the file ready?')
            # load file
            def_import_nm = load.filename_dialog()
            # get timestamp:
            def_import_ts = stringsf.nowsep()
            # copy file to datasets/observed directory
            def_export_nm = save.copy_file(def_import_nm, p1, def_data_flnm)
            # update fields in project file index:
            insert_str = '; ' + def_import_ts + ' ; ' + def_import_nm  # getting string to update
            # set data in project file
            plans2.set_indexdata(p0, insert_str, def_data_line)
    # display end messagem
    display.str_title_clr('end of system setup')


def tui_calibrate_models(p0, p1):
    """
    Void function. Interacive menu to calibrate the models of hydrology, treatment cost and expansion cost.
    :param p0: observed datasets directory
    :param p1: observed / visual directory
    :return: none
    """
    display.str_subtitle_clr('Calibration protocols section')  # header display
    # section menu loop:
    while True:
        # list of models to calibrate
        lst_menu = ['hydrology model [hydro_param]',
                    'treatment cost [tc_param]',
                    'expansion cost model [exp_param]']
        aux_str = "Enter menu key [<e> to exit menu]: "
        ans_menu = validate.string_menu(p0=lst_menu, p1='Calibration options', p2=aux_str, p4=True, p6='exit menu')
        #
        # exiting:
        if ans_menu == 'e':  # exiting
            break
        # calibrate hydrology:
        elif ans_menu == lst_menu[0]:
            validate.permission_protocol('Can we run? It may take a while!')
            plans2.calibrate_hydro(p0, p1, tui=True)
        #
        # calibrate treatment cost:
        elif ans_menu == lst_menu[1]:  # treatment
            plans2.calibrate_tc(p0, p1, True)
            #break
        # calibrate expansion:
        else:
            plans2.calibrate_exp(p0, p1, True)
            #


def tui_scn_setup(p0, p1, p2):
    """
    scenario setup protocol.
    :param p0: project file path
    :param p1: projected datasets dir
    :param p2: observer datasets dir
    :return: boolean
    """
    def_file_nms = ('scenario_specs', 'pop', 'wcons', 'p', 'pet', 'trff')
    display.str_title_clr('new scenario setup')
    msg_formats()
    validate.permission_protocol('Is the file ready?')
    # load file:
    def_import_nm = load.filename_dialog()
    # get scenario name
    def_scenario_nm = plans2.get_scenario_lst(def_import_nm)[0]
    print('Scenario Name: {}'.format(def_scenario_nm))
    # check if scenario name already exists:
    if plans2.check_scenario_name(p1, def_scenario_nm):
        plans2.set_new_scenario(p0=p1, p1=def_import_nm, p2=p0, p3=p2, tui=True)
        return True
    else:
        display.wrnginput('Scenario already existing!')
        print('>> A scenario with exact name in the project was found.')
        print('>> Edit spec file to change scenario name')
        def_aux_str = validate.string_ans(1, 'c', 'Type <c> to continue: ')
        return False


def tui_scn_reset(p0, p1, p2):
    """
    void protocol to reset scenarios
    :param p0: project file
    :param p1: projected datasets dir
    :param p2: observed datasets dir
    :return: none
    """
    display.str_title_clr('Reset scenario protocol')  # header
    def_aux_str = 'Reset All'  # key string to reset all
    def_scn_dir = tui_scn_picker(p0=p1, p1=def_aux_str)  # pick scenario
    if def_scn_dir == def_aux_str:  # resetting all
        validate.permission_protocol('Can we run? It may take a while!')  # validation protocol
        def_lst = plans2.list_all_scndirs(p1)  # list of all scenarios
        for def_e in def_lst:
            def_aux_str = 'Reset scenario: ' + def_e
            display.str_subtitle_clr(def_aux_str)
            def_lcl_scn_dir = p1 + '/' + def_e
            def_specs = def_lcl_scn_dir + '/' + plans2.get_scenario_files_dct()['Specfile'] + '.txt'
            plans2.reset_scenario(p0=p1, p1=def_specs, p2=p0, p3=p2, p4=def_lcl_scn_dir, tui=True)
    else:  # single scenario reset
        def_specs = def_scn_dir + '/' + plans2.get_scenario_files_dct()['Specfile'] + '.txt'
        plans2.reset_scenario(p0=p1, p1=def_specs, p2=p0, p3=p2, p4=def_scn_dir, tui=True)


def tui_show_scenarios(p0, full=False):
    """
    Void function. Just show scenarios stored at the project file
    :param p0: project file
    :param full: boolean for full display
    :return: none
    """
    tpl = plans2.get_index(p0, 77, p3=False)  # tuple of scenarios in project file
    df = pd.DataFrame(tpl[1:], columns=tpl[0])
    if full:
        print(df.to_string())
    else:
        print(df[['Name', 'Last Update']])
        print(df.to_string())


def tui_scn_picker(p0, p1='All', p2='Chose a scenario'):
    """
    a menu to pick an available scenario
    :param p0: projected datasets dir
    :param p1: string
    :param p2: string
    :return: string of scenario dir or p1 parameter string
    """
    aux_lst = plans2.list_all_scndirs(p0)
    aux_lst.append(p1)
    aux_str = ''
    aux_str = validate.string_menu(aux_lst, p2)  # menu
    if aux_str == p1:
        return p1
    else:
        return p0 + '/' + aux_str


def tui_dp_res_picker():
    """
    menu to chose the DP resolution
    :return: integer number of dp resolution (used as index in list)
    """
    dp_res = 3
    dp_res_menu = ['Fine', 'Moderate', 'Coarse']
    dp_res_str = validate.string_menu(dp_res_menu, 'Specify DP Resolution')
    if dp_res_str == dp_res_menu[0]:
        dp_res = 2
    elif dp_res_str == dp_res_menu[1]:
        dp_res = 3
    else:
        dp_res = 4
    return dp_res


def tui_dp_run(p0, p1, p2, p3):
    """
    Void function. Run DP protocol.
    :param p0: scenario dir
    :param p1: obs datasets dir
    :param p2: runbin dir
    :param p3: dp res
    :return: none
    """
    scn_dir = p0
    obs_dir = p1
    runbin_dir = p2
    dp_res = p3
    scn_nm = scn_dir.split('/')[-1]
    display.waiting(p1='loading DP data', p4=3)
    # get data
    dp_data = plans2.load_dp_data(obs_dir, scn_dir)
    # get setts
    scn_specsfile = scn_dir + '/specs.txt'
    # planning years
    prj_yrs = plans2.get_scenario_years_tpl(scn_specsfile)
    prj_yr1 = prj_yrs[0]
    prj_yr2 = prj_yrs[1]
    prj_yrs_stp = prj_yr2 - prj_yr1
    settings = set_dp(prj_yr1, prj_yrs_stp, len(prj_yrs), dp_res)
    # run
    display.okinput()
    validate.permission_protocol('Can we run? It may take a while!')
    # pol = ((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
    dp_output, dp_logs, run_ts, run_cloud = run_dp(setts=settings, data=dp_data, prt_sts=True)
    display.okinput()
    # create dp run directory:
    rundir = plans2.create_dp_rundir(runbin_dir, scn_nm, run_ts)
    # export dp report file:
    report_file = plans2.export_dp_report(dp_logs, rundir, run_ts)
    print('\nReport file sucessfully exported to: {}'.format(report_file))
    # export dp cloud file:
    output_file = plans2.export_dp_output(dp_output, rundir, run_ts)
    print('\nOutput file sucessfully exported to: {}'.format(output_file))
    # export dp cloud file:
    cloud_file = plans2.export_dp_cloud(run_cloud, rundir, run_ts)
    print('\nCloud file sucessfully exported to: {}'.format(cloud_file))
    # get visual
    aux_str = 'DP-pannel_' + run_ts
    viz_file = viz_dp_pannel(rundir, aux_str, data_dpin=settings, data_dpout=dp_output)
    print('\nVisual file sucessfully exported to: {}\n\n'.format(viz_file))


def tui_dp_sim(p0, p1, p2, p3, p4):
    """

    :param p0: scenario dir
    :param p1: obs datasets dir
    :param p2: runbin dir
    :param p3: dp res
    :param p4: policy tuple
    :return:
    """
    scn_dir = p0
    obs_dir = p1
    runbin_dir = p2
    dp_res = p3
    scn_nm = scn_dir.split('/')[-1]
    display.waiting(p1='loading DP data', p4=5)
    # get data
    dp_data = plans2.load_dp_data(obs_dir, scn_dir)
    # get setts
    scn_specsfile = scn_dir + '/specs.txt'
    # planning years
    prj_yrs = plans2.get_scenario_years_tpl(scn_specsfile)
    prj_yr1 = prj_yrs[0]
    prj_yr2 = prj_yrs[1]
    prj_yrs_stp = prj_yr2 - prj_yr1
    settings = set_dp(prj_yr1, prj_yrs_stp, len(prj_yrs), dp_res)
    # run
    display.okinput()
    validate.permission_protocol('Can we run? It may take a while!')
    dp_output, dp_logs, run_ts, run_cloud = run_sim(setts=settings, data=dp_data, pol=p4, sim=True, prt_sts=True)
    display.okinput()
    # create dp run directory:
    rundir = plans2.create_dp_rundir(runbin_dir, '_SIM_' + scn_nm, run_ts)
    # export dp report file:
    report_file = plans2.export_dp_report(dp_logs, rundir, run_ts)
    print('\nReport file sucessfully exported to: {}'.format(report_file))
    # export dp cloud file:
    output_file = plans2.export_dp_output(dp_output, rundir, run_ts)
    print('\nOutput file sucessfully exported to: {}'.format(output_file))
    # export dp cloud file:
    cloud_file = plans2.export_dp_cloud(run_cloud, rundir, run_ts)
    print('\nCloud file sucessfully exported to: {}'.format(cloud_file))
    # get visual
    aux_str = 'DP-pannel_' + run_ts
    viz_file = viz_dp_pannel(rundir, aux_str, data_dpin=settings, data_dpout=dp_output, sim=True)
    print('\nVisual file sucessfully exported to: {}\n\n'.format(viz_file))


# Plans2 TUI
def main():
    clr = False
    off = False
    #
    # 0) Open PLANS:
    print(header_warp())
    display.waiting(p1='loading terminal UI', p2=0.3, p4=5)
    print(header_plans())
    root_dir_nm = plans2.get_root_dir()
    print('Local PLANS Directory: {}'.format(root_dir_nm))
    # project file extent:
    project_ext = plans2.get_projectfile_ext()
    #
    # 1) Language setup:
    dct = load_dict(False)
    # # print(dct)
    display.str_title_clr('Project setup options')
    #
    # Enter main loop:
    while True:
        #
        # 1) Exit condition:
        if off:
            off_msg()
            break
        #
        # 2) New or Open:
        lst_menu = [dct[1], dct[2]]
        aux_str = validate.string_menu(p0=lst_menu, p1=dct[3], p2=dct[4], p3=dct[5], clr=clr)
        #
        # 3) Set new project:
        if aux_str == lst_menu[0]:
            display.str_title_clr(p0=dct[1], clr=clr)
            # get a valid project name:
            while True:
                # user input in UI:
                project_title = validate.string_filename(p0=10, p1='>>> Enter new project title: ', clr=clr)
                # check if project already exists:
                valid_check = plans2.check_valid_project_dir(root_dir_nm, project_title)
                if valid_check:
                    display.okinput()
                    break
                else:
                    display.wrnginput('Project already exists! Enter different project title')
            # set project dir structure and file
            project_dir, pfile_pth, pstruc = plans2.set_new_project(root_dir_nm, project_title)
            # get diretories from project structure
            datasets_dir = pstruc[0]
            observed_dir = pstruc[1]
            obs_visuals_dir = pstruc[2]
            projected_dir = pstruc[3]
            runbin_dir = pstruc[4]
            print('Project successfully created at: {}\n'.format(project_dir))
            print('Project file is located at: {}\n'.format(pfile_pth))
        #
        # 4) Open existing project:
        else:
            display.str_title_clr(p0=dct[2], clr=clr)
            # get directory and file path
            project_dir, pfile_pth = tui_open_menu(root_dir_nm)
            # get the project struct tuple
            pstruc = plans2.get_project_struc(project_dir)
            # get diretories from project structure
            datasets_dir = pstruc[0]
            observed_dir = pstruc[1]
            obs_visuals_dir = pstruc[2]
            projected_dir = pstruc[3]
            runbin_dir = pstruc[4]
            # update index of data sets
            plans2.update_obs_index(observed_dir, pfile_pth)
            display.waiting(p1='updating datasets', p2=0.3, p4=5)
            display.okinput('Datasets updated')
        # final statements..
        display.waiting(p1='loading project', p2=0.3, p4=3)
        display.okinput(p0='Project succesfully loaded')
        # open project
        project_title = plans2.getdata_metadata(pfile_pth, 15)
        display.str_title_clr(project_title)
        #
        # 5) PLANS MAIN MENU:
        while True:
            display.str_title_clr(p0='plans menu', clr=clr)
            lst_menu = ['System setup', 'Scenario setup', 'Run optimization', 'Run simulation', 'start a new session']
            aux_str2 = "Enter menu key [<e> to exit program]: "
            ans_menu = validate.string_menu(p0=lst_menu[:], p1='options', p2=aux_str2, p4=True, p6='exit program')
            #
            # 1) Simulation:
            if ans_menu == lst_menu[3]:
                display.str_title_clr(p0=lst_menu[0], clr=clr)
                # section loop:
                while True:
                    lst_menu2 = ['Simulate hydrology', 'Simulate LULC sensitivity', 'Simulate NBS expansion policy']
                    aux_str2 = 'Enter menu key [<e> to exit menu]: '
                    ans_menu2 = validate.string_menu(p0=lst_menu2, p1='Setup options',
                                                     p2=aux_str2, p4=True, p6='exit menu')
                    # exit:
                    if ans_menu2 == 'e':
                        break
                    # simulate hydrology
                    elif ans_menu2 == lst_menu2[0]:
                        # check if there is datasets available to run
                        datasets_check, datasets_check_msg = plans2.check_obs_datasets(pfile_pth, observed_dir, 'input')
                        if datasets_check:
                            print(datasets_check_msg)
                            ans = validate.string_ans(p1='yn', p2='Simulate new LULC condition?')
                            if ans == 'Y':
                                lulcfile = load.filename_dialog(p0='txt', p1='txt file', p2='select lulc file')
                                # call as plans2 function to run the simulation
                                print('Executing simulation ... ')
                                hydro_out = plans2.run_hydro_sim(observed_dir, lulcfile, True)
                            else:
                                print('Executing simulation ... ')
                                hydro_out = plans2.run_hydro_sim(observed_dir)
                            display.okinput(p0='Simulation succesfully executed')
                            #
                            # create run directory:
                            rundir = plans2.create_hydrosim_rundir(runbin_dir, run_ts=hydro_out['RUNTS'])
                            print('Run directory: {}'.format(rundir))
                            # store outputs to files:
                            # simulation output
                            print('Exporting simulation output ... ')
                            plans2.export_hydro_out(hydro_out['SIM'], rundir, hydro_out['RUNTS'])
                            display.okinput()
                            # cfc output
                            print('Exporting CFC output ... ')
                            plans2.export_hydro_cfc(hydro_out['CFC'], rundir, hydro_out['RUNTS'])
                            display.okinput()
                            # parameters output
                            print('Exporting parameters output ... ')
                            plans2.export_hydro_p(hydro_out['Params'], rundir, hydro_out['RUNTS'])
                            display.okinput()
                            # visual:
                            print('Exporting visual output ... ')
                            aux_str = 'HYviz_' + hydro_out['RUNTS']
                            viz_hydro_hru_sim(rundir, aux_str, hydro_out['SIM'], hydro_out['CFC'])
                            display.okinput()
                            break
                        else:
                            print(datasets_check_msg)
                            aux_str = validate.string_ans(1, 'c', 'Type <c> to continue: ')
                            break
                    elif ans_menu2 == lst_menu2[1]:
                        # check if there is datasets available to run
                        datasets_check, datasets_check_msg = plans2.check_obs_datasets(pfile_pth, observed_dir, 'input')
                        if datasets_check:
                            print(datasets_check_msg)
                            sal = plans2.run_hydro_sal(observed_dir)
                            display.okinput(p0='Simulation osuccesfully executed')
                            #
                            # create run directory:
                            rundir = plans2.create_hydrosal_rundir(runbin_dir, run_ts=sal['RUNTS'])
                            print('Run directory: {}'.format(rundir))
                            # store outputs to files:
                            # simulation output
                            print('Exporting series ... ')
                            plans2.export_hydro_sal_series(sal['Series'], rundir, sal['RUNTS'])
                            display.okinput()
                            # cfc output
                            print('Exporting CFC output ... ')
                            plans2.export_hydro_cfc(sal['CFCs'], rundir, sal['RUNTS'])
                            display.okinput()
                            # visual:
                            print('Exporting CFCs visual output ... ')
                            aux_str = 'HYSAL_CFCs_' + sal['RUNTS']
                            viz_hydro_sal_cfcs(rundir, aux_str, sal['CFCs'])
                            display.okinput()
                            break
                        else:
                            print(datasets_check_msg)
                            aux_str = validate.string_ans(1, 'c', 'Type <c> to continue: ')
                            break
                    # simulate policy:
                    else:
                        datasets_check, datasets_check_msg = plans2.check_obs_datasets(pfile_pth, observed_dir, 'input')
                        if datasets_check:
                            print(datasets_check_msg)
                            # ok 2
                            if plans2.check_scenarios(projected_dir):
                                print('simulate policy')
                                print('\n- - - import policy file - - - -\n')
                                msg_formats()
                                # permission protocol:
                                validate.permission_protocol('Is the file ready?')
                                # load file
                                policy_file = load.filename_dialog()
                                df = pd.read_csv(policy_file, sep=';')
                                # built policy tuple
                                aux_lst = list()
                                for row in df.values:
                                    aux_lst.append(tuple(row[1:]))
                                pol_tpl = tuple(aux_lst)
                                # chose DP resolution
                                dp_res = tui_dp_res_picker()
                                '''# nbs forest:
                                pol = ((0, 0, 0), (40, 0, 0), (20, 0, 0),
                                       (20, 20, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
                                # nbs agricultuire:
                                pol2 = ((0, 0, 0), (0, 20, 20), (0, 40, 0),
                                        (20, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))'''
                                aux_str = 'Run all'
                                scn_dir = tui_scn_picker(projected_dir, p1=aux_str, p2='Chose a scenario to run')
                                if scn_dir == aux_str:
                                    print('Run all scenarios protocol') # todo run all scenarios protocol
                                    validate.permission_protocol('Can we run? It may take a while!')
                                    print('run!')
                                    print('Call function')
                                    # load list of all scenarios
                                    scn_lst = ['Scn1', 'Scn2', 'Scn3']
                                    for scn in scn_lst:
                                        lcl_scn_dir = scn_dir + '/' + scn
                                        print('\nRunning scenario: {}'.format(scn))
                                        print('develop code')
                                        # tui_dp_run(lcl_scn_dir, observed_dir, runbin_dir, dp_res)
                                        display.okinput()
                                    break
                                else:
                                    print('Single scenario run protocol')
                                    print('Scenario dir: {}'.format(scn_dir))
                                    tui_dp_sim(scn_dir, observed_dir, runbin_dir, dp_res, pol_tpl)
                                    break
                            else:
                                display.wrnginput('No scenarios was found.')
                                print('>> Go to Scenario Setup to set a scenario.')
                                aux_str = validate.string_ans(1, 'c', 'Type <c> to continue: ')
                                break
                        else:
                            print(datasets_check_msg)
                            aux_str = validate.string_ans(1, 'c', 'Type <c> to continue: ')
                            break
            #
            # 2) Optimization:
            elif ans_menu == lst_menu[2]:
                display.str_title_clr(p0=lst_menu[1], clr=clr)
                datasets_check, datasets_check_msg = plans2.check_obs_datasets(pfile_pth, observed_dir, p2='param')
                # ok 1
                if datasets_check:
                    print(datasets_check_msg)
                    # ok 2
                    if plans2.check_scenarios(projected_dir):
                        dp_res = tui_dp_res_picker()
                        #
                        aux_str = 'Run all'
                        scn_dir = tui_scn_picker(projected_dir, p1=aux_str, p2='Chose a scenario to run')
                        if scn_dir == aux_str:
                            print('Run all scenarios protocol')
                            validate.permission_protocol('Can we run? It may take a while!')
                            print('run!')
                            print('Call function')
                            # load list of all scenarios
                            scn_lst = ['Scn1', 'Scn2', 'Scn3']
                            for scn  in scn_lst:
                                lcl_scn_dir = scn_dir + '/' + scn
                                print('\nRunning scenario: {}'.format(scn))
                                print('develop code')
                                # tui_dp_run(lcl_scn_dir, observed_dir, runbin_dir, dp_res)
                                display.okinput()
                        else:
                            print('Single scenario run protocol')
                            print('Scenario dir: {}'.format(scn_dir))
                            # needed param : scn dir, obs_dir, runbin_dir,
                            tui_dp_run(scn_dir, observed_dir, runbin_dir, dp_res)
                    else:
                        display.wrnginput('No scenarios was found.')
                        print('>> Go to Scenario Setup to set a scenario.')
                        aux_str = validate.string_ans(1, 'c', 'Type <c> to continue: ')
                else:
                    print(datasets_check_msg)
                    aux_str = validate.string_ans(1, 'c', 'Type <c> to continue: ')
            #
            # 3) System setup:
            elif ans_menu == lst_menu[0]:
                display.str_title_clr('System setup')
                # section loop:
                while True:
                    lst_menu2 = ['Import data', 'Calibrate models']
                    aux_str2 = "Enter menu key [<e> to exit menu]: "
                    ans_menu2 = validate.string_menu(p0=lst_menu2, p1='Setup options',
                                                     p2=aux_str2, p4=True, p6='exit menu')
                    # exit:
                    if ans_menu2 == 'e':
                        break
                    # import data:
                    elif ans_menu2 == lst_menu2[0]:
                        tui_datasets_setup(pfile_pth, observed_dir)
                        #break
                    # calibrate models:
                    else:
                        # check datasets availability first:
                        datasets_check, datasets_check_msg = plans2.check_obs_datasets(pfile_pth, observed_dir, 'input')
                        # Data OK condition:
                        if datasets_check:
                            print(datasets_check_msg)
                            tui_calibrate_models(observed_dir, obs_visuals_dir)
                            #break
                        # Data Not OK condition
                        else:
                            print(datasets_check_msg)
                            aux_str = validate.string_ans(1, 'c', 'Type <c> to continue: ')
                            #break
            #
            # 4) Scenario set
            elif ans_menu == lst_menu[1]:
                display.str_title_clr(p0=lst_menu[3], clr=clr)
                # checking datasets:
                datasets_check, datasets_check_msg = plans2.check_obs_datasets(pfile_pth, observed_dir)
                if datasets_check:
                    if plans2.check_scenarios(projected_dir):
                        # display scenarios
                        print('Available scenarios:\n')
                        tui_show_scenarios(pfile_pth, full=True)
                    # menu loop:
                    while True:
                        # ask for a new or reset existing scenario
                        lst_menu_scn = ['New scenario', 'Reset existing scenario']
                        # display menu:
                        def_aux_str = 'scenario setup options'
                        def_aux_str2 = "Enter menu key [<e> to exit menu]: "
                        scenario_menu_key = validate.string_menu(lst_menu_scn, def_aux_str, p2=def_aux_str2, p4=True)
                        # exit or set data:
                        if scenario_menu_key == 'e':
                            display.str_subtitle_clr('exit scenario setup menu')
                            break
                        elif scenario_menu_key == lst_menu_scn[0]:
                            # display.str_subtitle_clr(scenario_menu_key, clr=clr)
                            lcl_flag = tui_scn_setup(pfile_pth, projected_dir, observed_dir)
                            if lcl_flag:
                                break
                        else:
                            tui_scn_reset(pfile_pth, projected_dir, observed_dir)
                            break
                else:
                    print(datasets_check_msg)
                    aux_str = validate.string_ans(1, 'c', 'Type <c> to continue: ')
            #
            # 5) new session protocol
            elif ans_menu == lst_menu[4]:
                newsess_msg()
                break
            #
            # 6) exit protocol
            elif ans_menu == 'e':
                ans_menu = validate.string_ans(p2='Are you sure to exit?')  # double checking
                if ans_menu == 'Y':
                    off = True
                    break
        # -------- end of code --------- #
