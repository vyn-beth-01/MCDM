import streamlit as st
import pandas as pd
# from  callbacks import *
# from visualization import * 



st.set_page_config(
    page_title="Subject: Multiple Criteria Decison Making", 
    initial_sidebar_state="expanded"
)

# st.sidebar.image('Logo-HCMIU.png')
st.sidebar.title('Subject: MCDM')


# Create main content page
src1_page = st.Page("page_src1.py", title="SRC", icon=":material/add_circle:")
src2_page = st.Page("page_src2.py", title="SRC2", icon=":material/delete:")

#Set up the navigation
pg = st.navigation([src1_page, src2_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()


# # menu = ["Project overview" , "Price prediction", "Prediction for HASS avocado in the future"]
# menu = ("Project overview" , "src", "src2")
# choice = st.sidebar.selectbox('Content', menu)

# ## Project overivew: Combine all business information and target of project 3: Price prediction
# if choice == 'Project overview':
#     st.divider() 
#     st.title('BUSINESS UNDERSTANDING')
#     st.divider() 
#     st.header("I. HASS company")
#     st.subheader('1. Giới thiệu công ty:')
#     st.write(""" HASS là một công ty có trụ sở tại Mexico, chuyên sản xuất nhiều loại bơ và xuất khẩu ở nhiều quốc gia trên thế giới """)
#     st.image('HASS_company.jpg')
#     st.write(" 'Bơ' là một trong những trái cây yêu thích nhất của người Mỹ.  'Hơn 95\% bơ tiêu thụ ở Mỹ là bơ HASS'. Đó cũng là lý do vì sao một thị trường phát triển mạnh của HASS là Mỹ. Gần như các vùng của Mỹ đều tiêu thụ bơ HASS. ")
#     st.image('business statements.png',width = 600)
#     st.subheader('2. Tìm hiểu vấn đề: ')
#     st.write('Công ty hiện tại kinh doanh ở rất nhiều vùng của nước Mỹ với 2 loại bơ chủ đạo: Bơ thường(conventional) và bơ hữu cơ (Organic), với nhiều quy chuẩn đóng gói (Small/Large/XLarge Bags), và có 3 PLUs(Product Look Up) chính: 4046, 4225 và 4770  ')
#     st.image('avocado_type.png')
#     st.write('Vấn đề của công ty là: Nên tiếp tục mở rộng xuất khẩu sang Mỹ,ở vùng  ')

#     st.header("II.Approach method ")
#     st.subheader('Method 1: Regression')
#     st.subheader('Method 2: ARIMA and Prophet')




# if choice == 'Prediction with HASS avocado':
#     st.title('Predict with HASS avocado')
#     # st.empty()
#     tab1,tab2 = st.tabs(['Price prediction', 'Avocado price in the future'])
#     with tab1:
#         st.header('Price prediction with XGBoost model')
#         st.write()
#         # Section 1: Manual input from WEB GUI:
#         st.markdown('### Manual input for prediction')
#         with st.expander(" Click to input variable for prediction "):
#             # st.markdown("### Parameters")
#             col1s = st.columns(3)
#             Volume_4046 = col1s[0].number_input('Volumne of type 4046',min_value =0)
    
#             Volume_4225 = col1s[1].number_input('Volumne of type 4225',min_value =0)
#             Volume_4770 = col1s[2].number_input('Volumne of type 4770',min_value = 0)

#             col2s = st.columns(3)
#             total_bags = col2s[0].number_input('Total bags')
#             total_bags = col2s[1].selectbox('Avocado type', ('Conventional', 'Organic'))
#             month = col2s[2].number_input('Month')
            
#             lst_country = set(data.region.tolist())
#             total_bags = st.selectbox('region', lst_country)
            
#         Results = st.button('Show prediction')
#         if Results:
#             predict_val = show_price_prediction(price_model,month,Volume_4046,Volume_4225,Volume_4770)
#             st.write('Gia bo trung binh du doan: ', predict_val)
    
#         # Section 2: Upload file with format:
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
        
#         Results2 = st.button('Show prediction all')
#         if Results2:
#             df = show_price_prediction2(dataframe,price_model)
#             st.dataframe(df)


#     with tab2:
#         st.header('Predict avocado price in the future')
#         st.markdown('### Business revenue of each region in USA')
#         cols = st.columns(2)
#         fig1,df_rev = summarize_revenue(data,'revenue')
#         fig2,df_vol = summarize_revenue(data,'total_volume')
#         cols[0].pyplot(fig1)
#         cols[1].pyplot(fig2)
        
#         df_rev_list = set(df_rev.index.tolist()).add('all')

#         st.markdown('#### Select parameters to predict: ')
#         country = st.selectbox('Region:',('all','California','GreatLakes','Midsouth','LosAngeles','Plains'))
#         year_predict = st.slider('Select how many years want to predict from 25/Mar/2018',
#                                 min_value=3,
#                                 max_value=10,
#                                 value=5,
#                                 step=1)
            
#         topn_country = st.slider('Select how many regions that you want to predict in case choose "all" region',
#                                 min_value=1,
#                                 max_value=5,
#                                 value=3,
#                                 step=1)
#         st.markdown("### You chose to predict for {} country/countries in next {} years. Click button to see the results ".format(country,year_predict))

#         Result3 = st.button('Show prediction future')
#         if Result3:
#             st.markdown('## Conventional')
#             fig2= show_results3(country,year_predict,data,'conventional')
#             st.pyplot(fig2)

#             st.markdown('## organic')
#             fig2= show_results3(country,year_predict,data,'organic')
#             st.pyplot(fig2)

   