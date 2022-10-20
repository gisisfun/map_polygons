 """
Spyder Editor
This is a temporary script file.
"""

import pandas as pd
from janitor import clean_names
import itertools
import numpy as np

def read_sheet(sheet_name:str,fname:str,start_row:int = 2) -> pd.DataFrame:
    """
    Reads a workbook and cleans headings
    Parameters
    ----------
    sheet_name : str
        worksheet name.
    fname : str
        filename of workbook.
    start_row : int, optional
        rows to to skip before data. The default is 2.
    Returns
    -------
    df_out : pd.DataFrame
        The contents of the worksheet in a dataframe.
    """
    df_out = pd.read_excel(fname,sheet_name=sheet_name,
                         header=start_row).\
        clean_names().rename({'grant_id':'merit_project_id'},axis=1)
    return df_out


def load_mult_wbooks(files_list:list,sheet_name:str) -> pd.DataFrame:
    """
    Loads and appends multiple worksheets to a dataframe.
    Parameters
    ----------
    files_list : list
        The list of M file references.
    sheet_name : str
        The target sheet name
    Returns
    -------
    df_out : DataFrame
        The appended worksheets in a dataframe.
    """
    files_list_out = [file_spec + ' ' + extract_date+".xlsx" 
                      for file_spec in files_list]
    df_out = pd.DataFrame()
    for fname in files_list_out:
        df_temp = read_sheet(sheet_name, fname)
        df_out = pd.concat([df_out,df_temp])
    return df_out


def get_indicator(df_in:pd.DataFrame,
                  indicator:str,
                  value:str) -> pd.DataFrame:
    """
    Extract indicator column data
    Parameters
    ----------
    df_in : pd.DataFrame
        Project and indicator source dataframe.
    indicator : str
        New indicator column name.
    value : str
        Test value found source dataframe.
    Returns
    -------
   df_out : pd.DataFrame
        A 2 column list to be joined to the output list.
    """
    df_out = df_in.copy(deep=True)    
    df_out[indicator]='Y'
    return  df_out[df_out['short_term_outcome_indicator_outcome']==
                value][['merit_project_id',indicator]]


def ids_by_df(ids_in:pd.DataFrame, df_in:pd.DataFrame, fy:str) -> pd.DataFrame:
    """
    Create bulk project services
    Parameters
    ----------
    ids_in : pd.DataFrame
        Project Ids.
    df_in : pd.DataFrame
        project Service descriptions.
    fy : str
        financial year text.
    Returns
    -------
    df_out : DataFrame
        A dataframe with an project id for each project service.
    """
    df_temp = pd.concat(list(itertools.repeat(df_in,ids_in.shape[0])))
    ids_out = pd.concat(list(itertools.repeat(ids_in,df_in.shape[0]))).sort_values()
    df_out = pd.DataFrame({'merit_project_id':ids_out.values,
                           'service':df_temp.service.values,
                           'target_measure':df_temp.target_measure.values,
                           'total_to_be_delivered':total_to_be_delivered_missing,
                           'report_financial_year':fy,
                           'fy_target':fy_target_missing})
    return df_out


def conc_col(df_in:pd.DataFrame,
             group_cols:list,
             agg_col:str) -> pd.DataFrame:
    """
    conc_col
    
    copies dataframe, drops duplicate rows, drops null values, sorts values.
    Parameters
    ----------
    df_in : pd.DataFrame
        DESCRIPTION.
    group_cols : list
        DESCRIPTION.
    agg_col : str
        DESCRIPTION.
    Returns
    -------
    df_out : TYPE
        DESCRIPTION.
    """
    df_out = df_in.copy(deep=True)
    df_out.drop_duplicates(inplace=True) 
    df_out = df_out[ ~df_out[agg_col].isnull()].sort_values(by=agg_col)
    df_out = df_out.groupby(group_cols, as_index=False).agg({agg_col: '|'.join})
    return df_out


def join_by_service_target_measure(df_in:pd.DataFrame,service:str,
                                    target_measure:str,
                                    grant_or_procurement:str='procurement'
                                    ) -> pd.DataFrame:
    """
    Join by service and target measure
    Parameters
    ----------
    df_in : pd.DataFrame
        input dataframe.
    service : str
        service name.
    target_measure : str
        target measure name.
    grant_or_procurement : str, optional
        either grant or procurement. The default is 'procurement'.
    Returns
    -------
    df_out : pd.DataFrame
        output dataframe.
    """
    df_out = pd.merge(
        df_in,project_services,
        on=['merit_project_id','service','target_measure',
            'report_financial_year'],
        how='inner') 
    df_out['grant_or_procurement'] = grant_or_procurement
    return df_out  

def make_ref_df(df_in:pd.DataFrame,id_col:str,lookup_col:str,
                lookup_vals:list) -> pd.DataFrame:
    """
    Does not work
    Parameters
    ----------
    df_in : pd.DataFrame
        DESCRIPTION.
    *args : list
        DESCRIPTION.
    Returns
    -------
    df_out : TYPE
        DESCRIPTION.
    """
    df_out = df_in.copy(deep=True)
    filtered = df_out.lookup_col.isin(lookup_vals)
    df_out = df_out[filtered][[id_col,lookup_col]]
    df_out.drop_duplicates(inplace=True)
    df_out = df_out[~df_out[lookup_col].isnull()]
    df_out = conc_col(df_out,id_col,lookup_col)
    return df_out


def no_category_extract_no_context_no_species(
        df_in:pd.DataFrame, worksheet:str, service:str, target_measure:str,
        measured:str, actual:str, invoiced:str, object_class:str=None, 
        property:str=None, value:str=None, category:str=None, context:str=None, 
        sub_category:str=None) -> pd.DataFrame:
    """
    transformation - no_category_extract_no_context_no_species
''' """
    
    df_out = df_in.copy(deep=True)
    df_out['measured']=df_out[measured]
    df_out['invoiced']=df_out[invoiced]
    df_out['actual']=df_out[actual]
    df_out = df_out[project_cols_in+report_cols_in+\
                    ['measured','invoiced','actual']]
    df_out['category'] = 'Various'
    df_out['context'] = np.nan
    df_out['report_species'] = np.nan
    df_out['service'] = service
    df_out['target_measure'] = target_measure
    df_out = join_by_service_target_measure(
        df_out, service, target_measure)
    
    if df_out.shape[0]>0:
        df_out['meta_source_sheetname'] = worksheet
        df_out['meta_transform_func'] = \
            'no_category_extract_no_context_no_species'
        df_out['meta_col_measured'] = measured
        df_out['meta_col_actual'] = actual
        df_out['meta_col_invoiced'] = invoiced
        df_out['meta_col_category'] = category
        df_out['meta_col_context'] = np.nan
        df_out['meta_text_subcategory'] = sub_category
        df_out['meta_col_report_species'] = np.nan
        df_out['meta_line_item_object_class'] = object_class
        df_out['meta_line_item_property'] = property
        df_out['meta_line_item_value'] = value
    
    return df_out
def sub_category_extract_context_no_species(
        df_in:pd.DataFrame, worksheet:str, service:str, target_measure:str,
        measured:str, actual:str, invoiced:str, category:str,sub_category:str,
        context:str,object_class:str=None, property:str=None, value:str=None, 
        species:str=None) -> pd.DataFrame:
    """
    transformation - sub_category_extract_no_context_no_species
    Parameters
    ----------
    df_in : pd.DataFrame
        DESCRIPTION.
    worksheet : str
        DESCRIPTION.
    service : str
        DESCRIPTION.
    target_measure : str
        DESCRIPTION.
    measured : str
        DESCRIPTION.
    actual : str
        DESCRIPTION.
    invoiced : str
        DESCRIPTION.
    category : str
        DESCRIPTION.
    object_class : TYPE, optional
        DESCRIPTION. The default is None.
    property : str, optional
        DESCRIPTION. The default is None.
    value : str, optional
        DESCRIPTION. The default is None.
    context : str, optional
        DESCRIPTION. The default is None.
    sub_category : str, optional
        DESCRIPTION. The default is None.
    Returns
    -------
    df_out : pd.DataFrame
        DESCRIPTION.
    """
    
    df_out = df_in.copy(deep=True)
    df_out['measured']=df_out[measured]
    df_out['invoiced']=df_out[invoiced]
    df_out['actual']=df_out[actual]
    df_out = df_out.rename(columns={category:'category',
                                    context:'context'})
    df_out = df_out[project_cols_in+report_cols_in+\
                    ['measured','invoiced','actual','category','context']]
    
    df_out = df_out[df_out['category'] == sub_category]
    df_out['report_species'] = np.nan
    df_out['service'] = service
    df_out['target_measure'] = target_measure
    df_out = join_by_service_target_measure(
        df_out, service, target_measure)
    
    if df_out.shape[0]>0:
        df_out['meta_source_sheetname'] = worksheet
        df_out['meta_transform_func'] = \
            'sub_category_extract_context_no_species'
        df_out['meta_col_measured'] = measured
        df_out['meta_col_actual'] = actual
        df_out['meta_col_invoiced'] = invoiced
        df_out['meta_col_category'] = category
        df_out['meta_col_context'] = context
        df_out['meta_text_subcategory'] = sub_category
        df_out['meta_col_report_species'] = np.nan
        df_out['meta_line_item_object_class'] = object_class
        df_out['meta_line_item_property'] = property
        df_out['meta_line_item_value'] = value
    
    return df_out

def sub_category_extract_no_context_no_species(
        df_in:pd.DataFrame, worksheet:str, service:str, target_measure:str,
        measured:str, actual:str, invoiced:str, category:str, 
        sub_category:str, context:str=None, object_class=None, 
        property:str=None, species:str=None, value:str=None) -> pd.DataFrame:
    """
    transformation - sub_category_extract_no_context_no_species
    Parameters
    ----------
    df_in : pd.DataFrame
        DESCRIPTION.
    worksheet : str
        DESCRIPTION.
    service : str
        DESCRIPTION.
    target_measure : str
        DESCRIPTION.
    measured : str
        DESCRIPTION.
    actual : str
        DESCRIPTION.
    invoiced : str
        DESCRIPTION.
    category : str
        DESCRIPTION.
    object_class : TYPE, optional
        DESCRIPTION. The default is None.
    property : str, optional
        DESCRIPTION. The default is None.
    value : str, optional
        DESCRIPTION. The default is None.
    context : str, optional
        DESCRIPTION. The default is None.
    sub_category : str, optional
        DESCRIPTION. The default is None.
    Returns
    -------
    df_out : pd.DataFrame
        DESCRIPTION.
    """
    
    df_out = df_in.copy(deep=True)
    df_out['measured'] = df_out[measured]
    df_out['invoiced'] = df_out[invoiced]
    df_out['actual'] =  df_out[actual]
    df_out = df_out.rename(columns={category:'category'})
    df_out = df_out[project_cols_in+report_cols_in+\
                    ['measured','invoiced','actual','category']]
    df_out = df_out[df_out['category'] == sub_category]
    df_out['context'] = np.nan
    df_out['report_species'] = np.nan
    df_out['service'] = service
    df_out['target_measure'] = target_measure
    df_out = join_by_service_target_measure(
        df_out, service, target_measure)
    
    if df_out.shape[0]>0:
        df_out['meta_source_sheetname'] = worksheet
        df_out['meta_transform_func'] = \
            'sub_category_extract_no_context_no_species'
        df_out['meta_col_measured'] = measured
        df_out['meta_col_actual'] = actual
        df_out['meta_col_invoiced'] = invoiced
        df_out['meta_col_category'] = category
        df_out['meta_col_context'] = np.nan
        df_out['meta_text_subcategory'] = sub_category
        df_out['meta_col_report_species'] = np.nan
        df_out['meta_line_item_object_class'] = object_class
        df_out['meta_line_item_property'] = property
        df_out['meta_line_item_value'] = value
    return df_out


def no_category_extract_context_species(
        df_in:pd.DataFrame, worksheet:str, service:str, target_measure:str,
        measured:str, actual:str, invoiced:str,context:str,species:str,
        object_class=None, property:str=None,value:str=None,
        sub_category:str=None,category:str=None) -> pd.DataFrame:
    df_out = df_in.copy(deep=True)
    df_out['measured']=df_out[measured]
    df_out['invoiced']=df_out[invoiced]
    df_out['actual']=df_out[actual]
    df_out = df_out.rename(columns={species:'species'})
    df_out = df_out[project_cols_in+report_cols_in+\
                    ['measured','invoiced','actual','species']]
    
    df_out['category'] = 'Various'
    df_out['context'] = np.nan
    df_out['service'] = service
    df_out['target_measure'] = target_measure
    df_out = join_by_service_target_measure(
        df_out, service, target_measure)
    
    if df_out.shape[0]>0:
        df_out['meta_source_sheetname'] = worksheet
        df_out['meta_transform_func'] = \
            'no_category_extract_context_species'
        df_out['meta_col_measured'] = measured
        df_out['meta_col_actual'] = actual
        df_out['meta_col_invoiced'] = invoiced
        df_out['meta_col_category'] = category
        df_out['meta_col_context'] = np.nan
        df_out['meta_text_subcategory'] = np.nan
        df_out['meta_col_report_species'] = np.nan
        df_out['meta_line_item_object_class'] = object_class
        df_out['meta_line_item_property'] = property
        df_out['meta_line_item_value'] = value
    return df_out


def no_category_extract_context_no_species(
        df_in:pd.DataFrame, worksheet:str, service:str, target_measure:str,
        measured:str, actual:str, invoiced:str,context:str,object_class=None, 
        property:str=None,value:str=None,sub_category:str=None,
        category:str=None,species:str=None) -> pd.DataFrame:
    df_out = df_in.copy(deep=True)
   
    df_out['measured']=df_out[measured]
    df_out['invoiced']=df_out[invoiced]
    df_out['actual']=df_out[actual]
    df_out = df_out[project_cols_in+report_cols_in+\
                    ['measured','invoiced','actual']]
    df_out['category'] = 'Various'
    df_out['context'] = np.nan
    df_out['report_species'] = np.nan
    df_out['service'] = service
    df_out['target_measure'] = target_measure
    df_out = join_by_service_target_measure(
        df_out, service, target_measure)
    
    if df_out.shape[0]>0:
        df_out['meta_source_sheetname'] = worksheet
        df_out['meta_transform_func'] = \
            'no_category_extract_context_no_species'
        df_out['meta_col_measured'] = measured
        df_out['meta_col_actual'] = actual
        df_out['meta_col_invoiced'] = invoiced
        df_out['meta_col_category'] = category
        df_out['meta_col_context'] = np.nan
        df_out['meta_text_subcategory'] = np.nan
        df_out['meta_col_report_species'] = np.nan
        df_out['meta_line_item_object_class'] = object_class
        df_out['meta_line_item_property'] = property
        df_out['meta_line_item_value'] = value
    return df_out

    

extract_date = '2022-07-18'
version = '1.0.1'
measured_missing, \
    actual_missing,\
    invoiced_missing,\
    fy_target_missing,\
    total_to_be_delivered_missing = (0,0,0,0,0)

project_cols_in = \
    ['project_id','merit_project_id','external_id',
     'internal_order_number','work_order_id', 'program','sub_program','name',
     'management_unit','organisation','status','start_date','end_date',
     'contracted_start_date','contracted_end_date','last_modified_1']

project_cols_out = \
    ['project_id','merit_project_id','external_id','internal_order_number',
     'work_order_id','organisation','management_unit','management_unit_id',
     'management_unit_state','project_name','program','sub_program',
     'project_start_date', 'project_end_date','project_contracted_start_date',
     'project_contracted_end_date','project_status']

project_meta_cols_out = \
    ['meta_source_sheetname','meta_col_project_start_date',
     'meta_col_project_end_date','meta_col_project_contracted_start_date',
     'meta_col_project_contracted_end_date','meta_col_project_name']

# Reports
report_cols_in = \
    ['site_id','report_status','report_financial_year','stage',
     'activity_id', 'activity_type','report_from_date','report_to_date']
report_cols_out = \
    ['MERIT_Reports_link','report_financial_year','report_status','service',
    'target_measure','context','site_id','report_last_modified','category',
    'report_species','total_to_be_delivered','fy_target','measured','invoiced',
    'actual','report_stage','report_activity_id','report_activity_type',
    'report_from_date','report_to_date']
report_meta_cols_out = \
    ['meta_col_measured','meta_col_actual','meta_col_invoiced',
     'meta_col_category','meta_text_subcategory','meta_col_context',
     'meta_col_report_species','meta_line_item_object_class',
     'meta_line_item_property','meta_line_item_value',
     'meta_col_project_status','meta_col_report_last_modified',
     'meta_col_report_stage','meta_col_report_activity_id',
     'meta_col_report_activity_type','meta_transform_func']

#Species Etc
species_etc_cols_out = \
    ['primary_secondary_outcomes','primary_outcomes','secondary_outcomes',
      'primary_secondary_investment_priorities','primary_investment_priority',
      'secondary_investment_priority','documents_priority','assets',
      'natural_cultural_assets_managed','threatened_species', 
      'threatened_ecological_communities','migratory_species',
      'ramsar_wetland','world_heritage_area',
      'community_awareness_participation_in_nrm',
      'indigenous_cultural_values','indigenous_ecological_knowledge',
      'remnant_vegetation','aquatic_and_coastal_systems_including_wetlands',
      'report_species','epbc','tec','ramsar','version']

numeric_cols = \
    ['measured','invoiced','actual','report_from_date','report_to_date',
     'start_date','end_date','contracted_start_date','contracted_end_date',
     'last_modified_2']

character_cols = \
    ['management_unit','external_id','site_id','organisation',
     'report_species','category','context']

extract_date_cols = ['version','grant_or_procurement','extract_date']

meri_outcomes_indicator_ref = \
    ["natural_cultural_assets_managed","threatened_species",
    "threatened_ecological_communities", "migratory_species",
    "ramsar_wetland","world_heritage_area",
    "community_awareness_participation_in_nrm","indigenous_cultural_values",
    "indigenous_ecological_knowledge","remnant_vegetation",
    "aquatic_and_coastal_systems_including_wetlands","world_heritage_area",
    "community_awareness_participation_in_nrm","indigenous_cultural_values",
    "indigenous_ecological_knowledge","remnant_vegetation",
    "aquatic_and_coastal_systems_including_wetlands"]

adjustment_cols = \
  ['project_service','output_measure','reported_measure_requiring_adjustment',
    'adjustment']
    
# management_units = pd.read_csv('management_units.csv')
# management_units.to_pickle("./management_units.pkl")  
management_units = pd.read_pickle("management_units.pkl")
management_units.rename({'investment_priority_derived':'merit_lookup',
             'investment_priority':'mu_state'},
            axis=1,inplace=True)

# investment_priority_themes = pd.read_excel('investment_priority_themes.xlsx')
# investment_priority_themes.to_pickle("./investment_priority_themes.pkl")  


investment_priority_themes = pd.read_pickle("./investment_priority_themes.pkl").\
rename(
    {'management_unit_id':'mu_id',
     'investment_priority_derived':'investment_priority',
     'short_term_indicator':'short_term_outcome_indicator_outcome'},
     axis=1)

# all_project_services = pd.read_excel('all_project_services.xlsx')
# all_project_services.to_pickle("./all_project_services.pkl")

all_project_services = pd.read_pickle("./all_project_services.pkl").\
    clean_names()


RLP_Outcomes = read_sheet('RLP Outcomes','M01 '+extract_date+'.xlsx',
                          start_row = 0).\
    rename({'merit_project_id':'grant_id'})
    
    
RLP_Outcomes_investment_priority = RLP_Outcomes.copy(deep=True)
RLP_Outcomes_investment_priority['investment_priority'] = \
    RLP_Outcomes_investment_priority['investment_priority'].str.split(',')
RLP_Outcomes_investment_priority = \
    RLP_Outcomes_investment_priority.explode('investment_priority')
RLP_Outcomes_investment_priority['investment_priority'] = \
    RLP_Outcomes_investment_priority['investment_priority'].str.strip()
RLP_Outcomes_investment_priority= \
        pd.merge(RLP_Outcomes_investment_priority,investment_priority_themes,
                 how='left',on='investment_priority')
    
epbc = get_indicator(RLP_Outcomes_investment_priority,
                     'epbc','Threatened Species')  

tec = get_indicator(RLP_Outcomes_investment_priority,
                     'tec','Threatened Ecological Community')     

ramsar = get_indicator(RLP_Outcomes_investment_priority,
                     'ramsar','Ramsar')    
    
projects = read_sheet('Projects',
                      'M01 '+extract_date+'.xlsx',
                      start_row = 0)

project_services_RLP = read_sheet('Project services and targets',
                                  'M01 '+extract_date+'.xlsx',
                                  start_row = 0)\
    [['merit_project_id','service','target_measure','total_to_be_delivered',
          '2018_2019','2019_2020','2020_2021','2021_2022','2022_2023']]
    
project_services_RLP = pd.melt(project_services_RLP,id_vars = \
                               ['merit_project_id','service',
                                'target_measure','total_to_be_delivered'],
                               var_name='report_financial_year',
                               value_name='fy_target')
 
project_services_RLP.report_financial_year = project_services_RLP.\
    report_financial_year.\
        replace('[_]','/',regex=True)
 
SGE_ids = projects[projects['sub_program']=='State Government Emergency']\
    ['merit_project_id'] 

    
project_services = pd.concat(
    [ids_by_df(SGE_ids, all_project_services,'2018/2019'),
     ids_by_df(SGE_ids, all_project_services,'2019/2020'),
     ids_by_df(SGE_ids, all_project_services,'2020/2021'),
     ids_by_df(SGE_ids, all_project_services,'2021/2022'),
     ids_by_df(SGE_ids, all_project_services,'2022/2023'),
     project_services_RLP])

RLP_Data = load_mult_wbooks(['M02','M05','M07','M08','M09'],
                             'RLP - Baseline da...tput Report')
BR_Data = load_mult_wbooks(['M05'],'Baseline data Sta...inal Report')

report_raw = pd.concat([
    no_category_extract_no_context_no_species( 
        df_in = RLP_Data,
        worksheet = 'RLP - Baseline da...tput Report',
        service = 'Collecting, or synthesising baseline data',
        target_measure = 'Number of baseline data sets collected and/or synthesised',
        measured = 'number_of_baseline_data_sets_collected_and_or_synthesised',
        invoiced = 'number_of_baseline_data_sets_collected_and_or_synthesised',
        actual = 'number_of_baseline_data_sets_collected_and_or_synthesised',
        object_class = 'Baseline Data',
        property = 'collected and/or synthesised',
        value = 'Total Data Sets'
        ),
    no_category_extract_no_context_no_species(
        df_in = BR_Data,
        worksheet = 'Baseline data Sta...inal Report',
        service = "Collecting, or synthesising baseline data",
        target_measure = "Number of baseline data sets collected and/or synthesised",
        measured = 'number_of_baseline_data_sets_collected_and_or_synthesised',
        invoiced = 'number_of_baseline_data_sets_collected_and_or_synthesised',
        actual = 'number_of_baseline_data_sets_collected_and_or_synthesised',
        object_class = 'Baseline data sets',
        property = 'collected and/or synthesised',
        value = 'Total Data Sets')])

RLP_Data = load_mult_wbooks(['M02','M05','M07','M08','M09'],
                             'RLP - Community e...tput Report')
BR_Data = load_mult_wbooks(['M05'],'Community engagem...inal Report')

report_raw = pd.concat([
    report_raw,
    sub_category_extract_no_context_no_species(
        df_in = BR_Data,
        worksheet = 'Community engagem...inal Report',
        service = "Community/stakeholder engagement",
        target_measure = "Number of conferences / seminars",
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        category = 'type_of_community_stakeholder_engagement_activity',
        sub_category = 'Conferences / seminars',
        context = 'purpose_of_engagement',
        object_class = 'Community Engagement',
        property = 'conferences / seminars',
        value ='Total Events'),
    sub_category_extract_no_context_no_species(
        df_in = RLP_Data,
        worksheet = 'RLP - Community e...tput Report',
        service = 'Community/stakeholder engagement',
        target_measure = 'Number of field days',
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        category = 'type_of_community_stakeholder_engagement_activity',
        sub_category = 'Field days',
        object_class = 'Community Engagement', 
        property = 'field days',
        value = 'Total Events'),
    sub_category_extract_context_no_species(
        df_in = BR_Data,
        worksheet = 'Community engagem...inal Report',
        service = 'Community/stakeholder engagement',
        target_measure = 'Number of field days',
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        category = 'type_of_community_stakeholder_engagement_activity',
        sub_category = 'Field days',
        context = 'purpose_of_engagement',
        object_class = 'Community Engagement',
        property = 'field days',
        value = 'Total Events'),
    sub_category_extract_context_no_species(
        df_in = RLP_Data,
        worksheet = 'RLP - Community e...tput Report',
        service = 'Community/stakeholder engagement',
        target_measure = 'Number of on-ground trials / demonstrations',
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        category = 'type_of_community_stakeholder_engagement_activity',
        sub_category = 'On-ground trials / demonstrations',
        context = 'purpose_of_engagement',
        object_class = 'Community Engagement',
        property = 'On-ground trials / demonstrations',
        value = 'Total Events'),
    sub_category_extract_context_no_species(
        df_in = BR_Data,
        worksheet = 'Community engagem...inal Report',
        service = 'Community/stakeholder engagement',
        target_measure = 'Number of on-ground trials / demonstrations',
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        category = 'type_of_community_stakeholder_engagement_activity',
        sub_category = 'On-ground trials / demonstrations',
        context = 'purpose_of_engagement',
        object_class = 'Community Engagement',
        property = 'On-ground trials / demonstrations',
        value = 'Total Events'),
    sub_category_extract_context_no_species(
        df_in = RLP_Data,
        worksheet = 'RLP - Community e...tput Report',
        service = 'Community/stakeholder engagement',
        target_measure = 'Number of on-ground works',
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        category = 'type_of_community_stakeholder_engagement_activity',
        context = 'purpose_of_engagement',
        sub_category = 'On-ground works',
        object_class = 'Community Engagement',
        property = 'on-ground works',
        value = 'Total Events'),
    sub_category_extract_context_no_species(
        df_in = BR_Data,
        worksheet = 'Community engagem...inal Report',
        service = 'Community/stakeholder engagement',
        target_measure = 'Number of on-ground works',
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        category = 'type_of_community_stakeholder_engagement_activity',
        context = 'purpose_of_engagement',
        sub_category = 'On-ground works',
        object_class = 'Community Engagement',
        property = 'on-ground works',
        value = 'Total Events'),
    sub_category_extract_context_no_species(
        df_in = RLP_Data,
        worksheet = 'RLP - Community e...tput Report',
        service = 'Community/stakeholder engagement',
        target_measure = 'Number of one-on-one technical advice interactions',
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        context = 'purpose_of_engagement',
        category = 'type_of_community_stakeholder_engagement_activity',
        sub_category = 'One-on-one technical advice interactions',
        object_class = 'Community Engagement',
        property = 'one-on-one technical advice interactions',
        value = 'Total Events'),
    sub_category_extract_context_no_species(
        df_in = BR_Data,
        worksheet = 'Community engagem...inal Report',
        service = 'Community/stakeholder engagement',
        target_measure = 'Number of one-on-one technical advice interactions',
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        category = 'type_of_community_stakeholder_engagement_activity',
        sub_category = 'One-on-one technical advice interactions',
        context = 'purpose_of_engagement',
        object_class = 'Community Engagement',
        property = 'one-on-one technical advice interactions',
        value = 'Total Events'),
    sub_category_extract_context_no_species(
        df_in = RLP_Data,
        worksheet = 'RLP - Community e...tput Report',
        service = 'Community/stakeholder engagement',
        target_measure = 'Number of training / workshop events',
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        category = 'type_of_community_stakeholder_engagement_activity',
        context = 'purpose_of_engagement',
        sub_category = 'Training / workshop events',
        object_class = 'Community Engagement',
        property = 'training / workshop events',
        value = 'Total Events'),
    sub_category_extract_context_no_species(
        df_in = BR_Data,
        worksheet = 'Community engagem...inal Report',
        service = 'Community/stakeholder engagement',
        target_measure = 'Number of training / workshop events',
        measured = 'number_of_community_stakeholder_engagement_type_events',
        invoiced = 'number_of_community_stakeholder_engagement_type_events',
        actual = 'number_of_community_stakeholder_engagement_type_events',
        category = 'type_of_community_stakeholder_engagement_activity',
        sub_category = 'Training / workshop events',
        context = 'purpose_of_engagement',
        object_class = 'Community Engagement',
        property = 'training / workshop events',
        value = 'Total Events')])

RLP_Data = load_mult_wbooks(['M02','M05','M07','M08','M09'],
                             'RLP - Management ...tput Report')
BR_Data = load_mult_wbooks(['M05'],'Management plan d...inal Report')

report_raw = pd.concat([
  report_raw,
  no_category_extract_context_species(
    df_in = RLP_Data,
    worksheet = 'RLP - Management ...tput Report',
    service = 'Developing farm/project/site management plan',
    target_measure = 'Area (ha) covered by plan',
    measured = 'calculatedareaha',
    invoiced = 'areainvoicedha',
    actual = 'area_ha_covered_by_plan_s',
    context = 'type_of_plan',
    species = 'species_and_or_threatened_ecological_communities_covered_in_plan',
    object_class = 'Debris',
    property = 'Removal',
    value = 'Total Area (Ha)'),
  no_category_extract_context_no_species(
    df_in = RLP_Data,
    worksheet = 'RLP - Management ...tput Report',
    service = 'Developing farm/project/site management plan',
    target_measure = 'Number of farm/project/site plans developed',
    measured = 'number_of_plans_developed',
    invoiced = 'number_of_plans_developed',
    actual = 'number_of_plans_developed',
    context = 'type_of_plan',
    object_class = 'Debris',
    property = 'Removal',
    value = 'Total Plans'),
  no_category_extract_context_no_species(
    df_in = BR_Data,
    worksheet = 'Management plan d...inal Report',
    service = 'Developing farm/project/site management plan',
    target_measure = 'Number of farm/project/site plans developed',
    measured = 'number_of_plans_developed',
    invoiced = 'number_of_plans_developed',
    actual = 'number_of_plans_developed',
    context = 'management_plan_type',
    object_class = 'Debris',
    property = 'Removal',
    value = 'Total Plans')])

adjustments_data = load_mult_wbooks('M09', 'RLP Output Report Adjustment')
adjustments_data = adjustments_data[project_cols_in + report_cols_in + \
                                    adjustment_cols]
adjustments_data = adjustments_data.rename(columns={
    'project_service':'service','output_measure':'target_measure'})
adjustments_data['measured'] = np.nan
adjustments_data['actual'] = \
    adjustments_data['reported_measure_requiring_adjustment']
adjustments_data['invoiced'] = adjustments_data['adjustment']
adjustments_data['report_species'] = np.nan
adjustments_data['category'] = np.nan
adjustments_data['context'] = np.nan
adjustments_data['sub_category'] = np.nan
adjustments_data['meta_source_sheetname'] = 'RLP Output Report Adjustment' 
adjustments_data['meta_transform_func'] = 'Adjustment Reports',
adjustments_data['meta_col_measured'] = np.nan
adjustments_data['meta_col_actual'] = 'reported_measure_requiring_adjustment',
adjustments_data['meta_col_invoiced'] = 'adjustment',
adjustments_data['meta_col_category'] = np.nan
adjustments_data['meta_col_context'] = np.nan
adjustments_data['meta_text_subcategory'] = np.nan
adjustments_data['meta_col_report_species'] = np.nan
adjustments_data['meta_line_item_object_class'] = np.nan
adjustments_data[' meta_line_item_property'] = np.nan
adjustments_data['meta_line_item_value'] = np.nan
adjustments_data.drop(['reported_measure_requiring_adjustment','adjustment'],
                      axis=1, inplace=True)
adjustments_data = join_by_service_target_measure(adjustments_data,'service',
                                                  'target_measure')
report_raw = pd.concat([report_raw,adjustments_data])

# Project Reports
project_reports = report_raw.copy(deep=True)
project_reports = project_reports.merge(management_units,
                                        on='management_unit',
                                        how='left')
project_reports[
    project_reports.total_to_be_delivered.isna()]['total_to_be_delivered'] =\
    total_to_be_delivered_missing
project_reports.loc[project_reports['report_status'] != 'Approved','invoiced'] = 0
project_reports['extract_date'] = extract_date
project_reports['MERIT_Reports_link'] = MERIT_Reports_link = \
"https://fieldcapture.ala.org.au/project/index/"+project_reports['project_id']
project_reports = project_reports.rename(
    columns=\
        {'status':'project_status', 'last_modified_1':'report_last_modified',
         'stage':'report_stage','activity_id':'report_activity_id',
          'activity_type':'report_activity_type','end_date':'project_end_date',
          'start_date':'project_start_date','name':'project_name',
          'contracted_start_date':'project_contracted_start_date',
          'contracted_end_date':'project_contracted_end_date'})
project_reports['version'] = version
project_reports['meta_col_project_status'] ='status'
project_reports['meta_col_report_last_modified'] ='last_modified_2'
project_reports['meta_col_report_stage'] ='stage'
project_reports['meta_col_report_activity_id'] ='activity_id'
project_reports['meta_col_report_activity_type'] ='activity_type'
project_reports['meta_col_project_start_date'] ='start_date'
project_reports['meta_col_project_end_date'] ='end_date'
project_reports['meta_col_project_contracted_start_date'] ='contracted_start_date'
project_reports['meta_col_project_contracted_end_date'] ='contracted_end_date'
project_reports['meta_col_project_name'] ='name'
project_reports = project_reports[project_cols_out+report_cols_out+\
                                  project_meta_cols_out+report_meta_cols_out+\
                                  extract_date_cols]
project_reports = project_reports[
    (project_reports['measured'] != 0) |
    (project_reports['actual'] != 0) |
    (project_reports['invoiced'] != 0) &
    (project_reports['report_status']=='Approved')]

# Primary and Secondary Outcomes
primary_secondary_outcomes = RLP_Outcomes.copy(deep=True)

primary_secondary_outcomes = primary_secondary_outcomes[\
primary_secondary_outcomes['type_of_outcomes'].
isin(['Primary outcome','Secondary Outcome/s'])]\
    [['merit_project_id','outcome']]
primary_secondary_outcomes = conc_col(
    primary_secondary_outcomes,'merit_project_id','outcome')
primary_secondary_outcomes.rename(columns={'outcome':
                                           'primary_secondary_outcomes'},
                          inplace=True)

# Primary Outcomes
primary_outcomes = RLP_Outcomes.copy(deep=True)
primary_outcomes = primary_outcomes[\
primary_outcomes['type_of_outcomes'] =='Primary outcome']\
    [['merit_project_id','outcome']]
primary_outcomes = conc_col(
    primary_outcomes,'merit_project_id','outcome')
primary_outcomes.rename(columns={'outcome':'primary_outcomes'},
                          inplace=True)

# Secondary Outcomes
secondary_outcomes = RLP_Outcomes.copy(deep=True)
secondary_outcomes = secondary_outcomes[\
secondary_outcomes['type_of_outcomes'] =='Secondary Outcome/s']\
    [['merit_project_id','outcome']]
secondary_outcomes = conc_col(
    secondary_outcomes,'merit_project_id','outcome')
secondary_outcomes.rename(columns={'outcome':'secondary_outcomes'},
                          inplace=True)

# Primary and Secondary Investment Priorities 
primary_secondary_investment_priorities = RLP_Outcomes.copy(deep=True)

primary_secondary_investment_priorities = primary_secondary_investment_priorities[\
primary_secondary_investment_priorities['type_of_outcomes'].
isin(['Primary outcome','Secondary Outcome/s'])]\
    [['merit_project_id','investment_priority']]
primary_secondary_investment_priorities = conc_col(
    primary_secondary_investment_priorities,'merit_project_id',
    'investment_priority')
primary_secondary_investment_priorities.rename(columns=
    {'investment_priority':'primary_secondary_investment_priorities'},
    inplace=True)

# Primary Investment Priorities
primary_investment_priorities = RLP_Outcomes.copy(deep=True)
primary_investment_priorities = primary_investment_priorities[\
primary_investment_priorities['type_of_outcomes'] =='Primary outcome']\
    [['merit_project_id','investment_priority']]
primary_investment_priorities = conc_col(
    primary_investment_priorities,'merit_project_id','investment_priority')
primary_investment_priorities.rename(columns=
    {'investment_priority':'primary_investment_priority'},
    inplace=True)

# Secondary Investment Priorities
secondary_investment_priorities = RLP_Outcomes.copy(deep=True)
secondary_investment_priorities = secondary_investment_priorities[\
secondary_investment_priorities['type_of_outcomes'] =='Secondary Outcome/s']\
    [['merit_project_id','investment_priority']]
secondary_investment_priorities = conc_col(
    secondary_investment_priorities,'merit_project_id','investment_priority')
secondary_investment_priorities.rename(columns=
    {'investment_priority':'secondary_investment_priority'},
    inplace=True)

# Project Assets
project_assets = read_sheet('MERI_Project Assets','M01 '+extract_date+'.xlsx',
                            start_row=0)[['merit_project_id','asset']]
project_assets = conc_col(project_assets, 'merit_project_id','asset')
project_assets.rename(columns={'asset':'assets'}, inplace=True)

# Meri Outcomes Indicators
meri_outcomes = read_sheet('MERI_Outcomes','M01 '+extract_date+'.xlsx',
                            start_row=0)[['merit_project_id']+ \
                                          meri_outcomes_indicator_ref].\
                                         groupby('merit_project_id').\
                                             tail(1)

# Meri Outcomes Priorities
meri_priorities = read_sheet('MERI_Priorities','M01 '+extract_date+'.xlsx',
                            start_row=0)[['merit_project_id',
                                          'document_name',
                                          'relevant_section',
                                          'explanation_of_strategic_alignment']]
meri_priorities.drop_duplicates(inplace=True)
meri_priorities = meri_priorities[~meri_priorities['document_name'].isnull()]
meri_priorities['documents_priority'] = "name: " + \
                meri_priorities['document_name'] + ' section: ' + \
                meri_priorities['relevant_section'] +' alignment: '+ \
                meri_priorities['explanation_of_strategic_alignment']
                
meri_priorities = meri_priorities[['merit_project_id','documents_priority']]
meri_priorities = conc_col(meri_priorities,
                           'merit_project_id',
                           'documents_priority')

reports_species = report_raw.copy(deep = True)                                   
reports_species = reports_species[~reports_species['species'].isnull()]
reports_species = reports_species[['merit_project_id','species']]
reports_species = conc_col(reports_species,'merit_project_id','species')
reports_species = reports_species.rename(columns={'species':'report_species'})

reports_project_services = report_raw.copy(deep=True)
reports_project_services = reports_project_services[['merit_project_id',
                                                   'service','target_measure']]
reports_project_services['report_project_services'] = reports_project_services[
    'service'] +' - ' + reports_project_services['target_measure']
reports_project_services = reports_project_services[['merit_project_id',
                                                     'report_project_services']]
reports_project_services = conc_col(reports_project_services,
                                     'merit_project_id',
                                     'report_project_services')

# # load("sprat_lookup.Rdata")
# # col_by_merit_project_id <- function(Data,col) {
# #   fred <- Data %>% 
# #     filter(!is.na({{ col }})) %>%
# #     separate_rows({{ col }},sep='[,;|//\n]') %>% 
# #     select(merit_project_id,{{ col}}) %>% 
# #     drop_na() %>% 
# #     mutate(merit_raw=str_trim( {{ col }})) %>% 
# #     distinct() %>%
# #     select(merit_project_id,merit_raw)
# # }
# # 
# # merit_sprat_clean <- bind_rows(
# #   col_by_merit_project_id(projects_species,assets),
# #   col_by_merit_project_id(projects_species,primary_investment_priority),
# #   col_by_merit_project_id(projects_species,secondary_investment_priority),
# #   col_by_merit_project_id(projects_reports_species,report_species)) %>%
# #   distinct() %>%
# #   left_join(sprat_lookup,on='merit_raw') %>%
# #   filter(!is.na(sprat_category)) %>%
# #   distinct()

projects_reports_species = project_reports.copy(deep=True)
projects_reports_species = projects_reports_species.merge(
    primary_secondary_investment_priorities,on='merit_project_id', how='left').\
    merge(primary_investment_priorities,on='merit_project_id', how='left').\
    merge(secondary_investment_priorities,on='merit_project_id', how='left').\
    merge(project_assets,on='merit_project_id', how='left').\
    merge(meri_outcomes,on='merit_project_id', how='left').\
    merge(epbc,on='merit_project_id',how='left').\
    merge(tec,on='merit_project_id',how='left').\
    merge(ramsar,on='merit_project_id',how='left').\
    merge(primary_secondary_outcomes,on='merit_project_id',how='left').\
    merge(primary_outcomes,on='merit_project_id',how='left').\
    merge(secondary_outcomes,on='merit_project_id',how='left').\
    merge(meri_priorities,on='merit_project_id',how='left')
projects_reports_species['meta_col_project_status'] = 'status'
projects_reports_species['meta_col_project_start_date'] = 'start_date'
projects_reports_species['meta_col_project_end_date'] = 'end_date'
projects_reports_species['meta_col_project_contracted_start_date'] = \
    'contracted_start_date'
projects_reports_species['meta_col_project_contracted_end_date'] = \
                                          'contracted_end_date'
projects_reports_species['meta_col_project_name'] = 'name'
projects_reports_species = projects_reports_species[
    project_cols_out + report_cols_out + \
    project_meta_cols_out + report_meta_cols_out + \
    species_etc_cols_out + extract_date_cols]


projects_species = projects.copy(deep=True)
projects_species = projects_species.merge(
    primary_secondary_investment_priorities,on='merit_project_id', how='left').\
    merge(primary_investment_priorities,on='merit_project_id', how='left').\
    merge(secondary_investment_priorities,on='merit_project_id', how='left').\
    merge(project_assets,on='merit_project_id', how='left').\
    merge(meri_outcomes,on='merit_project_id', how='left').\
    merge(epbc,on='merit_project_id',how='left').\
    merge(tec,on='merit_project_id',how='left').\
    merge(ramsar,on='merit_project_id',how='left').\
    merge(primary_secondary_outcomes,on='merit_project_id',how='left').\
    merge(primary_outcomes,on='merit_project_id',how='left').\
    merge(secondary_outcomes,on='merit_project_id',how='left').\
    merge(meri_priorities,on='merit_project_id',how='left').\
    merge(management_units,on='management_unit',how='left').\
    merge(reports_project_services,on='merit_project_id',how='left').\
    merge(reports_species,on='merit_project_id',how='left')
projects_species['meta_col_project_status'] = 'status'
projects_species['extract_date'] = extract_date
projects_species['version'] = version
projects_species['grant_or_procurement'] = np.nan
projects_species['meta_col_project_start_date'] = 'start_date'
projects_species['meta_col_project_end_date'] = 'end_date'
projects_species['meta_col_project_contracted_start_date'] = \
    'contracted_start_date'
projects_species['meta_col_project_contracted_end_date'] = \
                                          'contracted_end_date'
projects_species['meta_col_project_name'] = 'name'

projects_species.rename(columns={
    'status':'project_status',
    'start_date':'project_start_date',
    'end_date':'project_end_date',
    'contracted_start_date':'project_contracted_start_date',
    'contracted_end_date':'project_contracted_end_date',
    'name':'project_name'},inplace=True)

project_species = projects_species[project_cols_out + ['service_provider', \
                                   'report_project_services'] + \
                                   species_etc_cols_out +\
                                       extract_date_cols]    
    
