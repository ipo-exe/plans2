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
# Date: June of 2020
# Description:
# this package contains all backend (silent) functions to run PLANS

import os
import pandas as pd
import numpy as np
import scenarios, vizs, hydrology
from tools import save, stringsf, display


def get_root_dir():
    """
    function to get the root directory
    :return: root dir string
    """
    root_dir_nm = 'C:/Plans2'  # name of root dir
    # check if the main dir is already in disk
    if os.path.exists(root_dir_nm):  # existing condition
        pass
    else:
        root_dir_nm = save.create_new_dir(p0=root_dir_nm, p1=False)
    return root_dir_nm


def get_project_dirs():
    """
    return a tuple of the basic project directories names (not path)
    :return: tuple of dir names
    """
    def_tpl = ('datasets',
               'datasets/observed',
               'datasets/observed/visuals',
               'datasets/projected',
               'runbin')
    return def_tpl


def get_projectfile_ext():
    """
    return the project file extension
    :return: string of the project file extension
    """
    def_str = 'plns'
    return def_str


def check_is_project_dir(p0):
    """
    function to check if a given directory is a project's directory
    :param p0: directory path string
    :return: boolean (TRUE if is a project's directory)
    """
    def_dir = p0
    def_flag = False
    lst = os.listdir(def_dir)  # listing all elements in directory
    # loop to find out a project file. #todo make this more robust. Use _set_ python strucure
    def_c = 0
    while True:
        if len(lst[def_c].split('.')) == 2:
            if lst[def_c].split('.')[1] == get_projectfile_ext():
                def_flag = True
                break
        def_c = def_c + 1
        if def_c == len(lst):
            break
    return def_flag


def check_valid_project_dir(p0, p1):
    """
    function to check if project is already present in root dir
    :param p0: root dir
    :param p1: project title string
    :return: boolean
    """
    def_check = True
    def_lst = os.listdir(p0)
    try:
        def_lst.index(p1)
        def_check = False
        #print('found')
    except ValueError:
        #print('not found')
        pass
    return def_check


def check_scenarios(p0):
    """
    check if directory is a scenario directory (?) # todo wtf is this function?
    :param p0: directory string path
    :return: boolean (True if the dir is not empty)
    """
    # naive checker:
    def_int = len(os.listdir(p0))
    if def_int > 0:
        return True
    else:
        return False


def check_scenario_name(p0, p1):
    """
    a naive checker for scenario names
    :param p0: projected datasets dir
    :param p1: scenario name string
    :return: boolean (True if the scenario name is available for use)
    """
    def_check = True
    def_lst = os.listdir(p0)  # todo this can be way more robust.
    try:
        def_lst.index(p1)
        def_check = False
    except ValueError:
        pass
    return def_check


def check_obs_datasets(p0, p1, p2='input'):
    """
    Check if datasets are available based on class of dataset
    :param p0: observed dir
    :param p1: project file
    :param p2: class data
    :return: boolean (True if datasets are OK) and a string message
    """
    # list directory items
    def_dirlst = os.listdir(p1)
    def_index =  get_index(p0)
    # loop in index, collecting missing data
    def_lst = list()
    for def_row in def_index:
        if def_row[1] == p2:
            def_lcl_fln = def_row[4] + '.' + def_row[2]  # file name in index
            # loop the dir list to find it:
            def_c = 0
            def_flag = 'Not found'
            while True:
                if def_lcl_fln == def_dirlst[def_c]:
                    def_flag = 'Found'
                    break  # stop the search
                else:  # keep searching
                    def_c = def_c + 1
                    # end of search condition:
                    if def_c >= len(def_dirlst):
                        break
            # appending conditional:
            if def_flag == 'Not found':
                def_aux_str1 = 'Missing:\t' + def_row[3]
                def_lst.append(def_aux_str1)
        else:
            pass
    # return conditional
    if len(def_lst) > 0:
        if p2 == 'input':
            def_msg = 'Missing data found: ' + '\n' + '\n'.join(def_lst) + \
                      '\n\nGo to System Setup >> Import data to update missing data'
        elif p2 == 'param':
            def_msg = 'Missing data found: ' + '\n' + '\n'.join(def_lst) + \
                      '\n\nGo to System Setup >> Calibrate models to update missing data'
        else:
            def_msg = 'Missing data found: ' + '\n' + '\n'.join(def_lst) + \
                      '\n\nGo to System Setup to update missing data'
        return False, def_msg
    else:
        def_msg = 'Datasets are OK, no missing data files'
        return True, def_msg


def get_project_struc(p0):
    """
    function to get the project basic structure in iterable form (tuple)
    :param p0: project dir path string
    :return: tuple of the project directory strings
    """
    def_project_dir = p0
    def_dirs_names = get_project_dirs()
    def_lst = list()
    for def_e in def_dirs_names:
        def_lst.append(def_project_dir + '/' + def_e)
    def_tpl = tuple(def_lst)
    return def_tpl


def get_scenario_lst(p0):
    """
    Function to return the scenarios specs in a list
    :param p0: spec file
    :return: list of scenarios
    """
    # 1) get scenario name and scenario list from import file
    def_import_nm = p0
    def_import_fle = open(def_import_nm, 'r')
    def_import_lst = def_import_fle.readlines()
    def_import_fle.close()
    # Load scenario specs to list
    def_scn_lst = list()
    for def_row in def_import_lst:
        def_aux_str = def_row.split(':')[1].strip()
        def_scn_lst.append(def_aux_str[:])
    return def_scn_lst


def get_scenario_dct(p0):
    """
    function to get the scenario specs in dictionary form
    :param p0: specs file
    :return: dictionary of specs
    """
    def_lst = get_scenario_lst(p0)
    def_yrs = get_scenario_years_tpl(p0)
    def_dct = {'Name':def_lst[0], 'Timestamp':def_lst[1], 'Years':def_yrs, 'Pop':def_lst[3],
               'Wcons':def_lst[4], 'Tariff':def_lst[5], 'Elast':def_lst[6], 'RR':def_lst[7], 'PPet':def_lst[8]}
    return def_dct


def get_scenarios_files():
    """
    return the scenario file names (without the extension)
    :return: tuple of scenario file names
    """
    def_tpl = ('specs', 'pop', 'wcons', 'ppet', 'trff', 'elast', 'rr')
    return def_tpl


def get_scenario_labels_dct():
    """
    scenario file labels, in dictionary form
    :return: dictionary of lables
    """
    def_dct = {'Specfile':'specs',
               'Pop':'Population (hab)',
               'Wcons':'Water Consup. (L/hab/d)',
               'PPet':'(mm)',
               'Tariff':'Tariff ($/m3)',
               'Elast':'Elasticity',
               'RR':'Return rate (%)'}
    return def_dct


def get_scenario_files_dct():
    def_dct = {'Specfile':'specs', 'Pop':'pop', 'Wcons':'wcons', 'Wconsr':'wconsr', 'PPet':'ppet',
               'Tariff':'trff', 'Elast':'elast', 'RR':'rr', 'SC_param':'sc_param'}
    return def_dct


def get_scn_import_files_dct():
    def_dct = {'Pop':'pop_obs', 'Wcons':'wcons_obs', 'PPet':'p_obs',
               'Tariff':'tariff_obs', 'Elast':'elast_obs', 'RR':'rr_obs'}
    return def_dct


def get_scenario_years_tpl(p0):
    """

    :param p0: spec file
    :return: tuple of years in scenario spec file
    """
    def_lst = get_scenario_lst(p0)
    def_str_yrs = def_lst[2][1:-1]
    def_lst = def_str_yrs.split(',')
    def_yrs_lst = list()
    for def_e in def_lst:
        def_yr = int(def_e.strip())
        def_yrs_lst.append(def_yr)
    return tuple(def_yrs_lst)


def get_scenario_types_dct():
    """
    retrive from the template file the type of projections by variable
    :return: dict of scenario projection types
    """
    # 1) get scenario name and scenario file list from import file
    def_import_fle = open('scenario_types.txt', 'r')
    def_import_lst = def_import_fle.readlines()
    def_import_fle.close()
    # Load scenario specs to list
    def_scntypes_lst = list()
    for def_row in def_import_lst[3:]:
        def_aux_str1 = def_row.split(':')[0].strip()
        def_aux_lst = def_aux_str1.split('[')[1].split(']')[0].split('|')
        def_row2 = list()
        for def_e in def_aux_lst:
            def_row2.append(def_e.strip())
        def_scntypes_lst.append(tuple(def_row2[:]))
        def_row2.clear()
    def_tpl = tuple(def_scntypes_lst)
    def_dct = {'Pop':def_tpl[0], 'Wcons':def_tpl[1], 'Tariff':def_tpl[2],
               'Elast':def_tpl[3], 'RR':def_tpl[4], 'PPet':def_tpl[5]}

    return def_dct


def create_scenario_specfile(p0, p1):
    """
    the function creates a scenario specfile and returns the name path
    :param p0: scenario directory
    :param p1: scenario data list
    :return: specfile name path with extension
    """
    def_fle = open('scenario_template.txt', 'r')
    def_tmp_lst = def_fle.readlines()
    def_fle.close()
    def_lst1 = list()
    for def_e in def_tmp_lst:
        def_lst1.append(def_e.split(':')[0])
    def_lst2 = list()
    for def_i in range(0, len(p1)):
        def_aux_str = def_lst1[def_i] + ': ' + p1[def_i] + '\n'
        def_lst2.append(def_aux_str[:])
    #
    # Create specs empty file:
    def_specfile_nm = get_scenarios_files()[0]
    def_export_flenm = p0 + '/' + def_specfile_nm
    def_export_flenm = save.create_new_file(def_export_flenm)
    # print('Export file created at: {}'.format(def_export_flenm))
    #
    # Write lines:
    def_export_fle = open(def_export_flenm, 'w+')
    def_export_fle.writelines(def_lst2)
    def_export_fle.close()
    def_lst1.clear()
    def_lst2.clear()
    def_tmp_lst.clear()
    return def_export_flenm


def list_all_scndirs(p0):
    """

    :param p0: projected datasets dir
    :return: list of all scenarios
    """
    def_lst = os.listdir(p0)
    return def_lst


def list_all_scenarios(p0):
    """
    scenarios recorded in project file
    :param p0: project file
    :return:
    """
    def_tpl = get_index(p0, 78, p3=False)
    def_lst = list()
    for def_e in def_tpl:
        def_lst.append(def_e[0])
    return tuple(def_lst)


def list_all_projects(p0):
    lst = os.listdir(p0)
    lst_projects = list()
    for elem in lst:
        lcl_dir = p0 + '/' + elem
        if check_is_project_dir(lcl_dir):
            #print('{} - OK'.format(elem))
            lst_projects.append(elem)
    return lst_projects

# load index data to tuples:
def get_index(p0, p1=24, p2=49, p3=True):
    """
    Just load index to tuples
    :param p0: project file
    param p1: first line
    :param p2: last line
    :param p3: slicing mode boolean
    :return: tuple of tuples
    """
    def_fle = open(p0, 'r')
    if p3:
        def_lst = def_fle.readlines()[p1:p2]
    else:
        def_lst = def_fle.readlines()[p1:]
    def_fle.close()
    def_index = list()
    for e in def_lst:
        aux_row = e[:-1].split(';')
        def_index_row = list()
        for i in aux_row:
            def_index_row.append(i[:].strip())
        def_index.append(tuple(def_index_row[:]))
        def_index_row.clear()
    def_tpl_index = tuple(def_index)
    def_index.clear()
    return def_tpl_index


def set_indexdata(p0, p1, p2):
    """

    :param p0: project file
    :param p1: string to set
    :param p2: line index in file
    :return:
    """
    # open project file and load lines to list
    def_fle = open(p0, 'r+')
    def_lst = def_fle.readlines()
    def_fle.close()
    # get line by index
    def_lst_line = def_lst[p2]
    # print(def_lst_line)
    # explode line:
    def_lst_line_lst = def_lst_line.split(';')
    # print(def_lst_line_lst)
    def_lst_line_part1 = ';'.join(def_lst_line_lst[:5])
    # print(def_lst_line_part1)
    # set new line string
    def_newline_str = def_lst_line_part1 + p1 + '\n'
    # print(def_newline_str)
    # change list
    def_lst[p2] = def_newline_str
    # overwrite file
    def_fle = open(p0, 'r+')
    def_fle.writelines(def_lst)
    def_fle.close()


def update_obs_index(p0, p1):
    def_observed_dir = p0
    def_lst = os.listdir(def_observed_dir)
    # print(def_lst)
    def_index = get_index(p0=p1)
    # loop in index
    for def_row in def_index:
        def_lcl_fln = def_row[4] + '.' + def_row[2]  # file name in index
        # loop in dir list to find file
        def_c = 0
        def_flag = 'Not found'
        def_flag2 = ''
        while True:
            # finding condition
            if def_lcl_fln == def_lst[def_c]:
                def_flag = 'Found'
                # not listed condition
                if def_row[5] == '':
                    #
                    def_flag2 = 'Not Listed'
                    # edit index in file
                    def_insert_str = '; unknown (manual import) ; unknown (manual import) '
                    def_data_line = 23 + int(def_row[0])
                    set_indexdata(p1, def_insert_str, def_data_line)
                    #
                else:
                    def_flag2 = 'Listed'
                break  # stop the search
            # keep searching:
            else:
                def_c = def_c + 1
                # end of search condition:
                if def_c >= len(def_lst):
                    break
        # print('{}\t{}\t{}'.format(def_flag, def_lcl_fln, def_flag2))
    # display.waiting(p1='Updating project datasets file index')


def update_scn_index(p0, p1):
    """

    :param p0: project file
    :param p1: scenario list
    :return:
    """
    # create scenario specs string:
    def_tpl_index = get_index(p0, p1=77, p3=False)
    def_scn_name = p1[0]
    def_new_flag = True
    if len(def_tpl_index) > 1:
        # new index of lines:
        def_new_index = list()
        # update index:
        for def_e in def_tpl_index:
            if def_e[0] == def_scn_name:
                def_new_flag = False
                def_new_index.append(';'.join(p1))
            else:
                def_new_index.append(';'.join(def_e))
        '''for def_e in def_new_index:
            print(def_e)'''
        if def_new_flag:
            save.appendtext(p0, ';'.join(p1))
        else:
            # overwrite file:
            save.edit_lines(p0, p1=77, p2=def_new_index)
    else:
        save.appendtext(p0, ';'.join(p1))


def getdata_metadata(p0, p1):
    """
    returns the data in string format from metadata file
    :param p1: line index (first line is 0)
    :return: data string
    """
    def_pfile_pth = p0
    def_line_id = p1
    # 1) open file and load lines to list
    def_metadata_fle = open(def_pfile_pth, 'r+')
    def_metadata_lst = def_metadata_fle.readlines()
    def_metadata_fle.close()
    def_line_lst = def_metadata_lst[def_line_id].split(':')
    if len(def_line_lst) >= 2:
        def_data = ':'.join(def_line_lst[1:])[:-1]
    else:
        def_data = def_line_lst[1][:-1]
    # print(def_data)  # inspection print
    def_metadata_lst.clear()
    return def_data.strip()


def editline_metadata(p0, p1, p2):
    """
    simple protocol to edit a line in metadata file
    :param p0: metadata list lines
    :param p1: line index (first is 0)
    :param p2: edit string
    :return: updated metadata list lines
    """
    def_full = p0  # list of lines
    def_line_id = p1  # index of edit line
    def_oldline = str(p0[def_line_id])  # get edit line
    # print(def_oldline)
    def_newline = def_oldline.split(':')[0] + ': ' + p2 + '\n'  # built new line
    # print(def_newline)
    def_full[def_line_id] = def_newline  # inset new line the list of lines
    return def_full


def editdata_metadata(p0, p1, p2):
    """
    edit data to metadata file
    :param p0: project file path
    :param p1: line index
    :param p2: edit string
    :return: none
    """
    # 1) open file and load lines to list
    def_metadata_fle = open(p0, 'r+')
    def_metadata_lst = def_metadata_fle.readlines()
    def_metadata_fle.close()
    # 2) edit line in list
    def_metadata_lst = editline_metadata(def_metadata_lst, p1, p2)
    # 3) overwrite file
    def_metadata_fle = open(p0, 'r+')
    def_metadata_fle.writelines(def_metadata_lst)
    def_metadata_fle.close()


def set_new_project(p0, p1):
    """

    :param p0: root dir string
    :param p1: project title string
    :param p3: project extension string
    :return: tuple of all project dirs and files
    """
    # create project directory
    aux_str = p0 + '/' + p1  # built the project path
    def_project_dir = save.create_new_dir(p0=aux_str)

    def_project_ext = get_projectfile_ext()

    # get basic data:
    def_project_tm = stringsf.now()  # get project creation timestamp
    def_project_id = 'PLANS-' + stringsf.nowsep()  # create unique code for project

    # built return tuple:
    def_pstruc = get_project_struc(def_project_dir)

    # create core directories:
    save.create_new_dir(p0=def_pstruc[0], p1=False)  # create observed datasets directory
    save.create_new_dir(p0=def_pstruc[1], p1=False)  # create observed datasets directory
    save.create_new_dir(p0=def_pstruc[2], p1=False)  # create observed visuals directory
    save.create_new_dir(p0=def_pstruc[3], p1=False)  # create projected datasets directory
    save.create_new_dir(p0=def_pstruc[4], p1=False)  # create runbin directory

    # create metadata file:
    def_aux_str = def_project_dir + '/' + p1
    def_pfile_pth = save.create_new_file(def_aux_str, '.' + def_project_ext)

    # load template to list
    template = open('pfile_template.txt', 'r')
    template_lst = template.readlines()
    template.close()

    # overwrite list to blank file
    def_pfile = open(def_pfile_pth, 'r+')
    def_pfile.writelines(template_lst)
    def_pfile.close()

    # store basic data to file:
    editdata_metadata(def_pfile_pth, 15, p1)
    editdata_metadata(def_pfile_pth, 16, def_project_id)
    editdata_metadata(def_pfile_pth, 17, def_project_tm)
    editdata_metadata(def_pfile_pth, 18, def_project_dir)

    return def_project_dir, def_pfile_pth, def_pstruc


def set_new_scenario(p0, p1, p2, p3, tui=False):
    """

    :param p0: projected datasets dir
    :param p1: imported specs file
    :param p2: project file
    :param p3: observed datasets dir
    :return:
    """
    # get timestamp:
    def_import_ts = stringsf.nowsep('-')
    # get list:
    def_scn_lst = get_scenario_lst(p1)
    # get scenario name:
    def_scenario_nm = def_scn_lst[0]
    # create directory in project dir
    def_scn_dir = p0 + '/' + def_scenario_nm
    def_scn_dir = save.create_new_dir(def_scn_dir)
    # update data with timestamp:
    def_scn_lst[1] = def_import_ts
    # create spec file in directory:
    def_scn_file_nm = create_scenario_specfile(def_scn_dir, def_scn_lst)
    # TUI printing protocol:
    if tui:
        def_aux_str = 'Scenario directory created at: ' + def_scn_dir
        display.okinput(def_aux_str)
        def_aux_str = 'Specfile created at:' + def_scn_file_nm
        display.okinput(def_aux_str)
    # get scenario dict:
    def_scn_dct = get_scenario_dct(def_scn_file_nm)
    # get years list
    def_yrs = def_scn_dct['Years']
    # get file names
    def_file_dct = get_scenario_files_dct()
    # get projection type dict:
    def_type_dct = get_scenario_types_dct()
    # get import file names dict
    def_imp_dct = get_scn_import_files_dct()
    # get labels
    def_exp_lbls = get_scenario_labels_dct()
    # create yearly variables projection
    if tui:
        print('\nInitiating yearly variable projection protocols ... ')
        display.okinput()
    # loop in tuple to create scenarios of yearly variables
    def_aux_tpl = ('Pop', 'Wcons', 'Tariff', 'Elast', 'RR')
    for def_e in def_aux_tpl:
        # built import file name:
        def_imp = p3 + '/' + def_imp_dct[def_e] + '.txt'
        if tui:
            print('Variable scenario: ' + def_e)
            print('Import file: {}'.format(def_imp))
            display.okinput()
        # get export dict from scenario routine:
        def_exp_dct = scenarios.yearly_variable(def_yrs, def_scn_dct[def_e], def_imp, def_type_dct[def_e])
        # load data to arrays:
        def_xobs = def_exp_dct['x_obs']
        def_yobs = def_exp_dct['y_obs']
        def_yobs_fit = def_exp_dct['y_obs_fit']
        def_xprj = def_exp_dct['x_prj']
        def_yprj = def_exp_dct['y_prj']
        #
        # rip some arrays from the loop:
        if def_e == 'Pop':
            yrs_prj = def_xprj
            pop_prj = def_yprj
        if def_e == 'Wcons':
            wcons_prj = def_yprj
        if def_e == 'Tariff':
            trff_prj = def_yprj
        if def_e == 'Elast':
            elast_prj = def_yprj
        def_coefs = def_exp_dct['Coefs']
        def_resid = def_exp_dct['Residuals']
        def_r2 = def_exp_dct['R2']
        def_msg = def_exp_dct['Msg']
        def_typemodel = def_exp_dct['Type']
        if tui:
            display.okinput(def_msg)
            print('\tModel type: {}'.format(def_typemodel))
            print('\tModel R2: {}'.format(def_r2))
            print('\tModel fit residuals: {}'.format(def_resid))
            print('\tModel coefficients: {}'.format(def_coefs))
        # built export file name:
        def_exp = def_scn_dir + '/' + def_file_dct[def_e] + '.txt'
        # create export dataframe:
        def_exp_lbl = def_exp_lbls[def_e]
        def_df = pd.DataFrame({'Years':def_xprj, def_exp_lbl:def_yprj})
        # export dataframe:
        def_df.to_csv(def_exp, sep=';', index=False)
        if tui:
            def_aux_str = 'Projection data exported to: ' + def_exp
            display.okinput(def_aux_str)
        # export model parameters/metadata
        def_exp = def_scn_dir + '/' + def_file_dct[def_e] + '_param'
        def_exp = save.create_new_txt_file(def_exp)
        def_aux_str = 'Model type: ' + str(def_typemodel)
        save.appendtext(def_exp, def_aux_str)
        def_aux_str = 'R2: ' + str(def_r2)
        save.appendtext(def_exp, def_aux_str)
        def_aux_str = 'Model residuals: ' + str(def_resid)
        save.appendtext(def_exp, def_aux_str)
        def_aux_str = 'Model coeffs: ' + str(def_coefs)
        save.appendtext(def_exp, def_aux_str)
        # export visual:
        def_ttl = def_exp_lbl + ' modelling by ' + def_typemodel.lower() + '; R2=' + str(def_r2)[:5]
        def_exp_vis = vizs.viz_scenario(def_scn_dir, def_file_dct[def_e], def_xobs, def_yobs, def_yobs_fit,
                                        def_xprj, def_yprj, ttl=def_ttl, ylbl=def_exp_lbl)
        if tui:
            def_aux_str = 'Projection visual exported to: ' + def_exp_vis
            display.okinput(def_aux_str)
    #
    #
    # derive the consumption array:
    consp_prj = pop_prj * wcons_prj / 1000  # m3/d
    # save the consumption array to file:
    def_df = pd.DataFrame({'Years': yrs_prj, 'Water Cons. m3/d': consp_prj, 'Pop':pop_prj, 'Wcons L/hab/d':wcons_prj})
    def_exp = def_scn_dir + '/wconsr.txt'
    def_df.to_csv(def_exp, sep=';', index=False)
    if tui:
        def_aux_str = 'Water consumption projection data exported to: ' + def_exp
        display.okinput(def_aux_str)
    #
    # calibrate the scarcity cost model parameters:
    sc_param = calibrate_sc(yrs_prj, trff_prj, consp_prj, elast_prj)
    # save the scarcity costs parameters to file sc_param.txt:
    def_df = pd.DataFrame(sc_param)
    def_exp = def_scn_dir + '/sc_param.txt'
    def_df.to_csv(def_exp, sep=';', index=False)
    if tui:
        def_aux_str = 'Scarcity model parameters exported to: ' + def_exp
        display.okinput(def_aux_str)
    # create climatic scenario projection:
    if tui:
        print('Generating climate scenario ... ')
    # built import file name:
    def_imp = p3 + '/' + def_imp_dct['PPet'] + '.txt'
    # get data:
    clm_data = scenarios.climate(def_yrs, def_scn_dct['PPet'], def_imp,  def_type_dct['PPet'])
    if tui:
        display.okinput('Climate scenario successfully generated')
    # export to csv file
    # built export file name:
    def_exp = def_scn_dir + '/' + def_file_dct['PPet'] + '.txt'
    def_df = pd.DataFrame({'Date': clm_data['Dts_prj'], 'P (mm)': clm_data['P_prj'], 'PET (mm)':clm_data['PET_prj']})
    # export dataframe:
    def_df.to_csv(def_exp, sep=';', index=False)
    if tui:
        def_aux_str = 'Climate projection exported to: ' + def_exp
        display.okinput(def_aux_str)
    # export visuals:
    print('\n\nExporting visual pannels ...')
    # water consumption pannel:
    def_exp_vis = vizs.viz_cons_pannel(def_scn_dir, 'cons_pannel', yrs_prj, pop_prj, wcons_prj, consp_prj, trff_prj,
                                       elast_prj, sc_param)
    if tui:
        def_aux_str = 'Consumption scenario exported to: ' + def_exp_vis
        display.okinput(def_aux_str)
    # climate projection pannel:
    def_aux_str = 'Climate scenario type: ' + def_scn_dct['PPet']
    def_exp_vis = vizs.viz_climate_scenario(def_scn_dir, def_file_dct['PPet'], data=clm_data, ttl=def_aux_str)
    if tui:
        def_aux_str = 'Climate projection visual exported to: ' + def_exp_vis
        display.okinput(def_aux_str)
    # do stuff to project file (p2):
    update_scn_index(p2, def_scn_lst)
    #


def reset_scenario(p0, p1, p2, p3, p4, tui=False):
    """

    :param p0: projected datasets dir
    :param p1: imported specs file
    :param p2: project file
    :param p3: observed datasets dir
    :param p4: scenario directory
    :param tui: boolean to control TUI printouts
    :return:
    """
    # create a temp bin dir in projected datasets dir
    def_projected_dir = p0
    tmp_dir = def_projected_dir + '/tmp'
    tmp_dir = save.create_new_dir(tmp_dir)
    # get scpec file:
    def_old_spec = p4 + '/' + get_scenario_files_dct()['Specfile'] + '.txt'
    # copy specfile from scenario dir and save in temp bin
    def_tmp_spec = save.copy_file(def_old_spec, tmp_dir, 'tmp_specs.txt')
    # clear scenario dir:
    save.clear_dir(p4)
    # set new scenario considering the temp file
    if tui:
        display.waiting(p1='Running reset protocol', p4=5)
    set_new_scenario(p0, def_tmp_spec, p2, p3, tui=True)
    # delete the temp file:
    os.remove(def_tmp_spec)
    # delete the temp dir:
    save.delete_dir(tmp_dir)
    if tui:
        display.okinput()


def calibrate_tc(p0, p1, tui=False):
    """

    :param p0: observed dataset string path
    :param p1: visual directory string path
    :param tui: boolean to control TUI-based prints
    :return: none
    """
    dir = p0
    vizdir = p1
    # import file
    tc_cloud = dir + '/tc_cloud.txt'
    if tui:
        print('Importing treatment cost data ...')
    df = pd.read_csv(tc_cloud, sep=';')
    # print(df)
    tc_x = df.T.values[0]  # get array of x (% of forest)
    tc_y = df.T.values[1] # * 1000  # get array of y ($/m3)
    if tui:
        display.okinput()
    import matplotlib.pyplot as plt
    if tui:
        print('Fitting data to model ...')
    # fit power model
    tc_x_lin = np.log10(tc_x)
    tc_y_lin = np.log10(tc_y)
    poly_dct = scenarios.polyfit(tc_x_lin, tc_y_lin, 1)
    model_coefs = poly_dct['coefs']
    model_residuals = poly_dct['residuals']
    model_r2 = scenarios.get_r2_poly(tc_x_lin, tc_y_lin, 1)
    tc_x_fit = np.linspace(1, 100, 100)
    model_a = np.power(10, model_coefs[1])
    model_b = model_coefs[0] * -1
    # tc_y_fit = np.power(10, model_coefs[1]) * (np.power(tc_x_fit, model_coefs[0]))
    tc_y_fit = model_a / (np.power(tc_x_fit, model_b))
    if tui:
        display.okinput()
        print('Exporting model parameters file ...')
    # store the coefs in the tc_param.txt file
    df = pd.DataFrame({'Parameters':('A', 'B', 'Resid.', 'R2'),
                       'Values':(model_a, model_b, model_residuals, model_r2)})
    exp_fle = dir + '/tc_param.txt'
    df.to_csv(exp_fle, sep=';', index=False)
    if tui:
        display.okinput()
        print('Exporting visual file ...')
    # export visual
    viz_data = {'TC_x':tc_x, 'TC_y':tc_y, 'TC_x_fit':tc_x_fit, 'TC_y_fit':tc_y_fit}
    vizs.viz_tc_cost(vizdir, 'tc_model', viz_data)
    if tui:
        display.okinput()


def calibrate_sc(yrs, p0, w0, e):
    """
    calibrate the scarcity model
    :param yrs: years iterable array
    :param p0: price array
    :param w0: full water demand array
    :param e: elasticity array
    :return: dictionary of calibrated model
    """
    # create param lists
    a_param = list()
    b_param = list()
    k_param = list()
    e_param = list()
    for t in range(0, len(yrs)):
        a_lcl = e[t] * w0[t] / p0[t]
        b_lcl = w0[t] - (a_lcl * p0[t])
        k_lcl = w0[t] / (p0[t] ** e[t])
        a_param.append(a_lcl)
        b_param.append(b_lcl)
        k_param.append(k_lcl)
        e_param.append(e[t])
    out = {'Years':yrs, 'A': a_param, 'B': b_param, 'K': k_param, 'e':e_param}
    return out


def calibrate_exp(p0, p1, tui=False):
    """

    :param p0: observed datasets dir
    :param p1: visuals dir
    :param tui: boolean to TUI prints
    :return: none
    """
    dir = p0
    vizdir = p1
    # get data names
    inst_nbsf_fle = dir + '/nbsf_inst.txt'
    inst_nbsp_fle = dir + '/nbsp_inst.txt'
    inst_nbsc_fle = dir + '/nbsc_inst.txt'
    oprt_nbsf_fle = dir + '/nbsf_oprt.txt'
    oprt_nbsp_fle = dir + '/nbsp_oprt.txt'
    oprt_nbsc_fle = dir + '/nbsc_oprt.txt'
    if tui:
        print('Importing installation costs data ...')
    inst_fles_tpl = (inst_nbsf_fle, inst_nbsp_fle, inst_nbsc_fle)
    inst_xyy_data = list()
    inst_coef_a = list()
    inst_coef_b = list()
    for file in inst_fles_tpl:
        # get data from files:
        df = pd.read_csv(file, sep=';')
        xobs = df.T.values[0]
        yobs = df.T.values[1]
        # fit model:
        fit = scenarios.polyfit(xobs, yobs, 1, fixed=True)
        yfit = fit['yfit']
        coefs = fit['coefs']
        # append data
        inst_xyy_data.append((xobs[:], yobs[:], yfit[:]))
        inst_coef_a.append(coefs[0])
        inst_coef_b.append(0)
    if tui:
        display.okinput()
        print('Importing operation costs data ...')
    oprt_fles_tpl = (oprt_nbsf_fle, oprt_nbsp_fle, oprt_nbsc_fle)
    oprt_xyy_data = list()
    oprt_coef_a = list()
    oprt_coef_b = list()
    for file in oprt_fles_tpl:
        # get data from files:
        df = pd.read_csv(file, sep=';')
        xobs = df.T.values[0]
        yobs = df.T.values[1]
        # fit model:
        fit = scenarios.polyfit(xobs, yobs, 1, fixed=True)
        yfit = fit['yfit']
        coefs = fit['coefs']
        # append data
        oprt_xyy_data.append((xobs[:], yobs[:], yfit[:]))
        oprt_coef_a.append(coefs[0])
        oprt_coef_b.append(0)
    if tui:
        display.okinput()
        print('Exporting parameter file ...')
    # export file
    types = ('NBS forest', 'NBS pasture', 'NBS crops')
    df = pd.DataFrame({'NBS type':types, 'Inst_A':inst_coef_a, 'Inst_B':inst_coef_b,
                       'Oprt_A':oprt_coef_a, 'Oprt_B':oprt_coef_b})
    exp_file = dir + '/exp_param.txt'
    df.to_csv(exp_file, sep=';', index=False)
    # visuals
    if tui:
        display.okinput()
        print('Exporting visuals ...')
    xlbl = 'Installation Area (ha)'
    ylbl = 'Cost $/ha'
    vizs.viz_exp_cost(vizdir, 'inst', inst_xyy_data, ttl=types, xlbl=xlbl, ylbl=ylbl)
    xlbl = 'Operation Area (ha)'
    ylbl = 'Cost $/ha/year'
    vizs.viz_exp_cost(vizdir, 'oprt', oprt_xyy_data, ttl=types, xlbl=xlbl, ylbl=ylbl)
    # x = np.append()
    if tui:
        display.okinput()


def calibrate_hydro(p0, p1, tui=False):
    # 1) load data
    obs_dir = p0
    vis_dir = p1
    #
    # get input file paths:
    q_file = obs_dir + '/q_obs.txt'
    lulc_file = obs_dir + '/lulc_gaug.txt'
    soils_file = obs_dir + '/soils_gaug.txt'
    param_file = obs_dir + '/hydro_param.txt'
    calib_file = obs_dir + '/hydro_calib.txt'
    #
    # get output file paths and names:
    series_file = obs_dir + '/hydro_series.txt'
    curves_file = obs_dir + '/hydro_curves.txt'
    cloud_file = obs_dir + '/hydro_cloud.txt'
    metrics_file = obs_dir + '/hydro_metrics.txt'
    pannel_file_name = 'hydro_pannel'
    cloud_file_name = 'hydro_cloud'
    #
    # get data dict:
    if tui:
        print('loading hydrology data ... ')
    # data = hydrology.load_hydro_data(q_file, lulc_file, soils_file, param_file, True)  # old code
    data = hydrology.load_hydro_data_hru(q_file, lulc_file, soils_file, param_file, True)
    if tui:
        display.okinput()
        print('Initiating calibration protocol ...')
    #
    # 2) calibrate
    #
    # get calibration search parameters:
    df = pd.read_csv(calib_file, sep=';')
    size = int(df.T.values[1][0])
    segf = int(df.T.values[1][1])
    rng = ((df.T.values[1][2], df.T.values[1][3]),
           (df.T.values[1][4], df.T.values[1][5]),
           (df.T.values[1][6], df.T.values[1][7]),
           (df.T.values[1][8], df.T.values[1][9]))
    #
    # get calib dict:
    '''calib, metrics, cloud, series, curves= hydrology.calib4(data['Area'], data['Qobs'], data['P'], data['PET'], data['CN'],
                                                            data['Rzdf'], data['Nnash'], size=size, ranges=rng,
                                                            segf=segf, tui=tui)'''

    calib, metrics, cloud, series, curves = hydrology.calib4_hru(data['Area'], data['Qobs'], data['P'],
                                                                 data['PET'], data['LULC'], data['CNs'],
                                                                 data['Nnash'], size=size, ranges=rng,
                                                                 segf=segf, tui=tui)
    if tui:
        display.okinput()
        print('Storing paramters to file ...')
    # store new hydro_param file:
    param_names = ('area', 'cn', 'rzd', 'iaf', 'swmax', 'gwmax', 'knash', 'nnash')
    param_values = (data['Area'], series['CN'][0], series['Rzd'][0], calib['Iaf'], calib['Swmax'],
                    calib['Gwmax'], calib['Knash'], data['Nnash'])
    df = pd.DataFrame({'Parameter':param_names, 'Value':param_values})
    df.to_csv(param_file, sep=';', index=False)
    if tui:
        display.okinput()
        print('Storing series to file ...')
    #
    # Store hydro_series file:
    df = pd.DataFrame(series)
    df.to_csv(series_file, sep=';')
    if tui:
        display.okinput()
        print('Storing CFC curves to file ...')
    #
    # Store hydro_curves:
    df = pd.DataFrame(curves)
    df.to_csv(curves_file, sep=';')
    if tui:
        display.okinput()
        print('Storing metrics to file ...')
    #
    # Store hydro_metrics:
    df = pd.DataFrame(metrics, index=[0])
    df.to_csv(metrics_file, sep=';')
    if tui:
        display.okinput()
        print('Storing calibration cloud to file ...')
    #
    # Store hydro_cloud:
    df = pd.DataFrame(cloud)
    df.to_csv(cloud_file, sep=';')
    if tui:
        display.okinput()
        print('Generating cloud visual ...')
    # Plot clouds
    plot1 = vizs.viz_hydro_cloud(vis_dir, cloud_file_name, cloud['x'], cloud['y'], cloud['z'], cloud['w'], cloud['m'])
    if tui:
        display.okinput()
        print('Generating pannnel visual ...')
    # plot pannel
    # plot2 = vizs.viz_hydro_pannel(vis_dir, pannel_file_name, series, metrics, curves)  # old code
    plot2 = vizs.viz_hydro_hru_pannel(vis_dir, pannel_file_name, series, metrics, curves)
    if tui:
        display.okinput()
        print('*** End of calibration protocol ***')


def load_dp_data(p0, p1):
    """
    load all DP data
    :param p0: observed datasets dir
    :param p1: scenario dir
    :return: dictionary of DP data
    """
    obs_dir = p0
    scn_dir = p1
    # observed data (improve protocol):
    obs_file_tpl = ('lulc_pump', 'soils_pump', 'hydro_param', 'hydro_curves', 'tc_param', 'exp_param')

    # lulc pump:
    obs_file = obs_dir + '/' + obs_file_tpl[0] + '.txt'
    df = pd.read_csv(obs_file, sep=';')
    lulc0 = df.T.values[1]

    # soil types:
    obs_file = obs_dir + '/' + obs_file_tpl[1] + '.txt'
    df = pd.read_csv(obs_file, sep=';')
    # NBS expansion soils are the average of pasture, crops and existing nbs:
    soil_nbs = (df.values[3][1:] + df.values[4][1:]) / 2
    soils = tuple((df.values[0][1:], df.values[1][1:], df.values[2][1:],
                   df.values[3][1:], df.values[4][1:], soil_nbs, soil_nbs, soil_nbs))
    #
    # hydro param
    obs_file = obs_dir + '/' + obs_file_tpl[2] + '.txt'
    df = pd.read_csv(obs_file, sep=';')
    aux_tpl = tuple(df.T.values[1])
    obs_file = obs_dir + '/' + obs_file_tpl[3] + '.txt'
    df = pd.read_csv(obs_file, sep=';')
    aux_tpl2 = tuple(df.T.values[1])
    hydro_p = {'CN':aux_tpl[1], 'Rzdf':aux_tpl[2], 'iaf':aux_tpl[3], 'swmax':aux_tpl[4], 'gwmax':aux_tpl[5],
               'knash':aux_tpl[6], 'nnash':aux_tpl[7], 'q90': aux_tpl2[9]}
    #
    # tc param
    obs_file = obs_dir + '/' + obs_file_tpl[4] + '.txt'
    df = pd.read_csv(obs_file, sep=';')
    tc_p = {'A':df.T.values[1][0], 'B':df.T.values[1][1]}
    #
    # exp param
    obs_file = obs_dir + '/' + obs_file_tpl[5] + '.txt'
    df = pd.read_csv(obs_file, sep=';')
    #
    # installation param
    inst_p_nbsf = {'A':df.values[0][1], 'B':df.values[0][2]}
    inst_p_nbsp = {'A': df.values[1][1], 'B': df.values[1][2]}
    inst_p_nbsc = {'A': df.values[2][1], 'B': df.values[2][2]}
    inst_p = (inst_p_nbsf, inst_p_nbsp, inst_p_nbsc)
    #
    # operation param
    oprt_p_nbsf = {'A': df.values[0][3], 'B': df.values[0][4]}
    oprt_p_nbsp = {'A': df.values[1][3], 'B': df.values[1][4]}
    oprt_p_nbsc = {'A': df.values[2][3], 'B': df.values[2][4]}
    oprt_p = (oprt_p_nbsf, oprt_p_nbsp, oprt_p_nbsc)
    #
    # projected data:
    snc_files_dct = get_scenario_files_dct()
    # load PPet series
    scn_file = scn_dir + '/' + snc_files_dct['PPet'] + '.txt'
    df = pd.read_csv(scn_file, sep=';')
    p = df.T.values[1]
    pet = df.T.values[2]
    #
    # load SC_param
    scn_file = scn_dir + '/' + snc_files_dct['SC_param'] + '.txt'
    df = pd.read_csv(scn_file, sep=';')
    sc_a_p = df.T.values[1]
    sc_b_p = df.T.values[2]
    sc_k_p = df.T.values[3]
    sc_e_p = df.T.values[4]
    sc_param = (sc_a_p, sc_b_p, sc_k_p, sc_e_p)
    #
    # load Tariff series
    scn_file = scn_dir + '/' + snc_files_dct['Tariff'] + '.txt'
    df = pd.read_csv(scn_file, sep=';')
    trf = df.T.values[1]
    #
    # load water consumption (raw, daily volume)
    scn_file = scn_dir + '/' + snc_files_dct['Wconsr'] + '.txt'
    df = pd.read_csv(scn_file, sep=';')
    wconsr = df.T.values[1]
    #
    #
    # load RR series
    scn_file = scn_dir + '/' + snc_files_dct['RR'] + '.txt'
    df = pd.read_csv(scn_file, sep=';')
    rr = df.T.values[1][0]

    #
    ''' 
    Not used series: 
    '''
    #
    #

    # load Elast series
    scn_file = scn_dir + '/' + snc_files_dct['Elast'] + '.txt'
    df = pd.read_csv(scn_file, sep=';')
    elast = df.T.values[1][0]
    #
    #
    # built return dict
    r_dct = {'P':p, 'PET':pet, 'Tariff':trf, 'Wconsr':wconsr, 'RR':rr, 'Elast':elast, 'SC_param': sc_param,
             'Lulc0':lulc0,'Soils':soils, 'Hydro_p':hydro_p, 'TC_p':tc_p, 'Oprt_p':oprt_p, 'Inst_p':inst_p}
    return r_dct


def create_dp_rundir(run_bin, runlbl='', run_ts='000000'):
    aux_str = run_bin + '/' + 'DP_' + runlbl + '_' + run_ts
    dp_rundir = save.create_new_dir(aux_str, p2=False)
    return dp_rundir


def export_dp_report(dplogs, rundir, run_ts='000000'):
    report_flnm = rundir + '/DP-report_'+ run_ts
    report_file = save.create_new_file(report_flnm)
    for i in range(0, len(dplogs)):
        for line in dplogs[i]:
            save.appendtext(report_file, line)
    return report_file


def export_dp_output(out_dct, rundir, run_ts='000000'):
    report_flnm = rundir + '/DP-output_' + run_ts + '.txt'
    df = pd.DataFrame(out_dct)
    df.to_csv(report_flnm, sep=';', index=False)
    return report_flnm


def export_dp_cloud(out_dct, rundir, run_ts='000000'):
    report_flnm = rundir + '/DP-cloud_' + run_ts + '.txt'
    df = pd.DataFrame(out_dct)
    df.to_csv(report_flnm, sep=';', index=False)
    return report_flnm


def create_hydrosim_rundir(run_bin, runlbl='', run_ts='000000'):
    aux_str = run_bin + '/' + 'HYSIM_' + runlbl + '_' + run_ts
    hy_rundir = save.create_new_dir(aux_str, p2=False)
    return hy_rundir

def create_hydrosal_rundir(run_bin, runlbl='', run_ts='000000'):
    aux_str = run_bin + '/' + 'HYSAL_' + runlbl + '_' + run_ts
    hy_rundir = save.create_new_dir(aux_str, p2=False)
    return hy_rundir

def run_hydro_sim(p0, p1='', p2=False):
    """
    run hydrology simulation protocol
    :param p0: observed datasets directory
    :param p1: new lulc file path
    :param p2: boolean to control new lulc file
    :return: dictionary of outputs
    """
    run_ts = stringsf.nowsep()
    #
    obs_dir = p0
    #
    # observed data (improve protocol):
    obs_file_tpl = ('lulc_pump', 'soils_pump', 'hydro_param', 'q_obs')
    #
    qobsf = obs_dir + '/' + 'q_obs' + '.txt'
    lulcf = obs_dir + '/' + 'lulc_pump' + '.txt'
    soilsf = obs_dir + '/' + 'soils_pump' + '.txt'
    paramf = obs_dir + '/' + 'hydro_param' + '.txt'
    if p2:
        lulcf = p1
    #
    data = hydrology.load_hydro_data_hru(qobsf, lulcf, soilsf, paramf)
    #
    # q = hydrology.run_hydro(area, p, pet, cn, rzdf, iaf, swmax, gwmax, knash, nnash, export='full')
    q = hydrology.run_hydro_hru(data['Area'], data['P'], data['PET'], data['LULC'], data['CNs'],
                              data['Iaf'], data['Swmax'], data['Gwmax'], data['Knash'], data['Nnash'], export='full')
    #
    # find q90:
    cfc = hydrology.find_cfc(q['Q'])
    q90 = cfc[1][10]
    curves = {'CFC': cfc[1][1:], 'Exeed': cfc[0][1:]}
    #
    hydro_p = {'Area': data['Area'], 'CN': data['CN'], 'Rzdf': q['Rzd'][0], 'iaf': data['Iaf'], 'swmax': data['Swmax'],
               'gwmax': data['Gwmax'], 'knash': data['Knash'], 'nnash': data['Nnash'], 'q90': q90,
               'LULC':str(data['LULC'])}
    #
    out = {'SIM': q, 'CFC': curves, 'Params':hydro_p, 'RUNTS': run_ts}
    #
    return out


def run_hydro_sal(p0):
    run_ts = stringsf.nowsep()
    #
    obs_dir = p0
    #
    # observed data (improve protocol):
    obs_file_tpl = ('lulc_pump', 'soils_pump', 'hydro_param', 'q_obs')
    #
    qobsf = obs_dir + '/' + 'q_obs' + '.txt'
    lulcf = obs_dir + '/' + 'lulc_pump' + '.txt'
    soilsf = obs_dir + '/' + 'soils_pump' + '.txt'
    paramf = obs_dir + '/' + 'hydro_param' + '.txt'
    #
    data = hydrology.load_hydro_data_hru(qobsf, lulcf, soilsf, paramf)
    #
    series, cfcs = hydrology.sal_hru(data['Area'], data['P'], data['PET'], data['LULC'], data['CNs'], data['Iaf'], data['Swmax'],
                           data['Gwmax'], data['Knash'], data['Nnash'])
    return {'Series':series, 'CFCs':cfcs, 'RUNTS':run_ts}


def export_hydro_sal_series(outdct, rundir, run_ts='000000'):
    report_flnm = rundir + '/' + 'HYSAL_' + run_ts + '_Series.txt'
    df = pd.DataFrame(outdct)
    df.to_csv(report_flnm, sep=';', index=False)
    return report_flnm


def export_hydro_sal_cfcs(outdct, rundir, run_ts='000000'):
    report_flnm = rundir + '/' + 'HYSAL_' + run_ts + '_CFCs.txt'
    df = pd.DataFrame(outdct)
    df.to_csv(report_flnm, sep=';', index=False)
    return report_flnm


def export_hydro_out(outdct, rundir, run_ts='000000'):
    report_flnm = rundir + '/' + 'HYSIM_' + run_ts + '.txt'
    df = pd.DataFrame(outdct)
    df.to_csv(report_flnm, sep=';', index=False)
    return report_flnm


def export_hydro_cfc(outdct, rundir, run_ts='000000'):
    report_flnm = rundir+ '/' + 'HYCFC_' + run_ts + '.txt'
    df = pd.DataFrame(outdct)
    df.to_csv(report_flnm, sep=';', index=False)
    return report_flnm


def export_hydro_p(outdct, rundir, run_ts='000000'):
    report_flnm = rundir+ '/' + 'HYparam_' + run_ts + '.txt'
    df = pd.DataFrame(outdct, index=[0])
    df.T.to_csv(report_flnm, sep=';')
    return report_flnm