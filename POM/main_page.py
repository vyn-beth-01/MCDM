import streamlit as st
import pandas as pd
import numpy as np
# from  callbacks import *
# from visualization import * 
from PIL import Image



st.set_page_config(
    page_title="Subject: Multiple Criteria Decison Making", 
    initial_sidebar_state="expanded"
)

# st.image('Logo-HCMIU.png')
# st.sidebar.image('logo-vector-IU-01.png')
st.sidebar.title('Subject: MCDM')
# main page
menu = ("Main_page", "src2")
choice = st.sidebar.selectbox('Content', menu)

# Page subject overview:
if choice == 'Main_page':
    st.divider() 
    st.title('SUBJECT OVERVIEW- TBU')
    st.badge("In-developing")
    st.caption("This page is still under-developing, if any inputs, please email to me through :blue[beth.mieiu24007@gmail.com] or academic one :blue[TBU]")
    st.divider() 

    st.header("HOW TO USE:")
    st.write("Follow the below step to execute")
    st.write("Step 1: Input data")
    st.write("Step 2: Choose the method & check the results")

    st.divider()
    st.subheader("Step 1- Input the list of attributes, alternatives, prop & weights:")
    #Method 1: Input by select number of cols and rows:
    with st.expander(" Click to input data variables "):
    # st.markdown("### Parameters")
        col1s = st.columns(1)
        # number_of_attributes = col1s[0].number_input('Input_number_of_attributes',min_value =1)
        lst_of_attributes = col1s[0].text_input("(*)Input name of attributes, break by ',' ; enter to apply")
        cols2=st.columns(2)
        number_of_alternatives = cols2[1].number_input('Input number of alternatives(optional)',min_value =1)
        normalize_method = cols2[0].selectbox('(*)Data normalize method', ('Min-Max Scaler', 'StandardScaler','RobustScaler','SquareRootMethod'))

    # Basic pre-process inputs:
    lst_of_attributes_norm=[0,1] #initiate default cols name
    lst_of_attributes_norm = lst_of_attributes.split(",")

    lst_alternatives = [str(i) for i in range(0,number_of_alternatives)]
    default_alternatives= ["Weights","Prop"]
    for i in default_alternatives:
        lst_alternatives.append(i)

    # Initiate dataframe
    df = pd.DataFrame(
        index=lst_alternatives,
        columns=lst_of_attributes_norm,
    )
    edited_df = st.data_editor(df,num_rows="dynamic")
    # st.button("Rerun")
    st.divider()
    st.write("Method 2: Upload an existed excel (later ^^)")
    # Method 2: Upload an excel file:
    # Section 2: Upload file with format:

#         st.markdown('### Prediction with multiple values')
#         # Create a upload button:
#         uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)

#         if uploaded_file is not None:
#             dataframe = pd.read_csv(uploaded_file)
#             st.write(dataframe)

#         # Download a sample file:
#         @st.cache_data
#         def convert_df(df):
#             return df.to_csv().encode('utf-8')

#         csv = convert_df(pd.read_csv('avocado.csv'))
#         download = st.download_button(
#             label="Sample input",
#             data=csv,
#             file_name='sample_input.csv',
#             mime='text/csv',
#         )

    st.divider()
    st.subheader("Step 2: Select method")   
    st.write("This is the input data to run")
    st.table(edited_df)

    def callbacks(raw_df, normalize_method):
        import callbacks
        ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP = callbacks.main_run(raw_df,normalize_method)
        
        return ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP
    

    topsis, saw, vikor, promethee, electre = st.columns(5)
    #initiate method variable:
    method = None

    if topsis.button("TOPSIS",type="secondary"):
        topsis.markdown("You choose the :red[TOPSIS] method")
        method="topsis"
        
    if saw.button("SAW",type="secondary"):
        saw.markdown("You choose the :red[SAW] method")
        method="saw"

    if vikor.button("VIKOR",type="secondary"):
        vikor.markdown("You choose the :red[VIKOR] method")
        method="vikor"

    if promethee.button("PROMETHEE",type="secondary"):
        promethee.markdown("You choose the :red[PROMETHEE] method")
        method="promethee"

    if electre.button("ELECTRE",type="secondary"):
        electre.markdown("You choose the :red[ELECTRE] method")
        method="electre"


    if method is not None:
        st.write("Calculation has been completed, output illustrate as below. \n Click Download if need raw output: " )
        ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP = callbacks(edited_df, normalize_method)
        st.write(NUM_ALTS)
        st.write(ATBS)
        st.write(ALTS)
        st.write(NUM_ATBS)
        st.write(WEIGHTS)
        st.write(ATB_PROP)
        st.write(edited_df.to_numpy())
#     @st.cache_data

#     def convert_df(df):
#         return df.to_csv().encode('utf-8')

#     csv = pd.read_excel('mcdm_func_lib/src/TOPSIS.xlsx')
#     download = st.download_button(
#     label="Download output to txt file",
#     data=csv,
#     # file_name='sample_input.csv',
#     # mime='text/csv',
# )

