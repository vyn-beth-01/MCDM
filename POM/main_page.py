import streamlit as st
import pandas as pd
import numpy as np
# from  callbacks import *
# from visualization import * 



st.set_page_config(
    page_title="Subject: Multiple Criteria Decison Making", 
    initial_sidebar_state="expanded"
)

# st.sidebar.image('logo-vector-IU-01.png')
st.sidebar.title('Subject: MCDM')
# main page
menu = ("Main_page", "src2")
choice = st.sidebar.selectbox('Content', menu)

# Page subject overview:
if choice == 'Main_page':
    st.divider() 
    st.title('SUBJECT OVERVIEW- TBU')
    # st.badge("In-developing")
    st.caption("This page is still under-developing, if any inputs, please email to me through :blue[beth.mieiu24007@gmail.com] or academic one :blue[TBU]")
    st.divider() 

    st.header("HOW TO USE:")
    st.write("Follow the below step to execute")
    st.write("Step 1: Input data")
    st.write("Step 2: Choose the method & check the results")

    st.divider()
    st.header("Step 1- Input the list of attributes, alternatives, prop & weights:")
    #Method 1: Input by select number of cols and rows:
    with st.expander(" Click to input data variables "):
    # st.markdown("### Parameters")
        col1s = st.columns(1)
        # number_of_attributes = col1s[0].number_input('Input_number_of_attributes',min_value =1)
        lst_of_attributes = col1s[0].text_input("(*)Input name of attributes, break by ',' ; enter to apply")
        cols2=st.columns(2)
        number_of_alternatives = cols2[1].number_input('Input number of alternatives(optional)',min_value =1)
        normalize_method = cols2[0].selectbox('(*)Data normalize method', ('Min-Max Scaler', 'StandardScaler','SquareRootMethod'))

    # Basic pre-process inputs:
    lst_of_attributes_norm=[0,1]
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
    st.header("Step 2: Select method")   
    st.write("This is the input data to run")
    st.table(edited_df)

    def hello():
        return 1
    

    topsis, saw, vikor,_4,_5 = st.columns(5)
    if topsis.button("TOPSIS",type="secondary"):
        topsis.markdown("You choose the :red[TOPSIS] method")
        a= hello()
        st.write(a)
        
    if saw.button("SAW",type="secondary"):
        saw.markdown("You choose the :red[SAW] method")
        a= hello()
        st.write(a)
    if vikor.button("VIKOR",type="secondary"):
        vikor.markdown("You choose the :red[VIKOR] method")
        a= hello()
        st.write(a)
    if _4.button("PLACEHOLDER",type="secondary"):
        _4.markdown("You choose the :red[PLACEHOLDER] method")
        st.write("Placeholder")
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

