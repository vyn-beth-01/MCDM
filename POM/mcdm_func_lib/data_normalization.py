from sklearn.preprocessing import MinMaxScaler,StandardScaler,RobustScaler
import pandas as pd
import copy

def minmaxscaler(df,exclude_row=None):
    """
    This func employ the min-max scaler lib in python to execute the normlization data
    Args:
    - df (dataframe): the raw data frame
    - exclude_row (optional): this is optional fields to specific number of row to exclude out of normalize step
    Return:
    - norm_df: normalize data WITH original exclude row.
    - normalized_data: matrix after normalize
    """

    # Initialize MinMaxScaler
    scaler = MinMaxScaler()
    if not exclude_row:
        target_data = df
    else:
        target_data = df.iloc[:-exclude_row,:]
    
    # print(df.shape)
    # print(target_data.shape)
    # Fit and transform the data
    normalized_data = scaler.fit_transform(target_data)
    # print(normalized_data)

    # Convert back to DataFrame (optional)
    normalized_df = pd.DataFrame(normalized_data, columns=df.columns)

    final_normalized_df = pd.concat([normalized_df,df.iloc[-2:,:]])
    return final_normalized_df,normalized_data


def standardscaler(df,exclude_row=None):
    """
    This func employ the standard scaler lib in python to execute the normlization data
    Args:
    - df (dataframe): the raw data frame
    - exclude_row (optional): this is optional fields to specific number of row to exclude out of normalize step
    Return:
    - norm_df: normalize data WITH original exclude row.
    - normalized_data: matrix after normalize
    """

    # Initialize MinMaxScaler
    scaler = StandardScaler()
    if not exclude_row:
        target_data = df
    else:
        target_data = df.iloc[:-exclude_row,:]
    
    # print(df.shape)
    # print(target_data.shape)
    # Fit and transform the data
    normalized_data = scaler.fit_transform(target_data)
    # print(normalized_data)

    # Convert back to DataFrame (optional)
    normalized_df = pd.DataFrame(normalized_data, columns=df.columns)

    final_normalized_df = pd.concat([normalized_df,df.iloc[-2:,:]])
    return final_normalized_df,normalized_data


def robustscaler(df,exclude_row=None):
    """
    This func employ the robust scaler lib in python to execute the normlization data
    Args:
    - df (dataframe): the raw data frame
    - exclude_row (optional): this is optional fields to specific number of row to exclude out of normalize step
    Return:
    - norm_df: normalize data WITH original exclude row.
    - normalized_data: matrix after normalize
    """

    # Initialize MinMaxScaler
    scaler = RobustScaler()
    if not exclude_row:
        target_data = df
    else:
        target_data = df.iloc[:-exclude_row,:]
    
    # print(df.shape)
    # print(target_data.shape)
    # Fit and transform the data
    normalized_data = scaler.fit_transform(target_data)
    # print(normalized_data)

    # Convert back to DataFrame (optional)
    normalized_df = pd.DataFrame(normalized_data, columns=df.columns)

    final_normalized_df = pd.concat([normalized_df,df.iloc[-2:,:]])
    return final_normalized_df,normalized_data



 def normV1(self,mat):
        self._txtResult.append("The normalization method \n Squareroot Method \n")
        new_mat=copy.deepcopy(mat)
        new_mat2=copy.deepcopy(mat)
        sqr_col=[]
        for c in range(self.NUM_ATBS):
            val=np.sqrt(np.dot(new_mat[:,c],new_mat[:,c]))
            new_mat[:,c]=self.WEIGHTS[c]*1/val*new_mat[:,c]
            new_mat2[:,c]=1/val*new_mat2[:,c]
            sqr_col.append(val)
        return new_mat,new_mat2

def normV2(self,mat):
    self._txtResult.append("The normalization method \n Max-Min Difference \n")
    new_mat=copy.deepcopy(mat)
    new_mat2=copy.deepcopy(mat)
    ref=[]
    for c in range(self.NUM_ATBS):
        min_val=np.min(new_mat[:,c])
        max_val=np.max(new_mat[:,c])
        ref.append((min_val,max_val))
        for r in range(self.NUM_ALTS):  
            new_mat[r,c]=self.WEIGHTS[c]*(new_mat[r,c]-min_val)/(max_val-min_val)
            new_mat2[r,c]=(new_mat2[r,c]-min_val)/(max_val-min_val)
            
    print("Reference :",ref)
    return new_mat, new_mat2
