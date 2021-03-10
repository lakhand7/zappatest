import pandas as pd
import warnings
import operator
warnings.filterwarnings('ignore')

def get_price_bucket(PRODUCT, Price):

    if '4' in PRODUCT:
        if(Price>10000000):
            Price_Bucket = 'last'
        elif((Price>5000000)):
            Price_Bucket = 'Seventh'
        elif((Price>2500000)):
            Price_Bucket = 'Sixth'
        elif((Price>1500000)):
            Price_Bucket = 'Fifth'
        elif((Price>1000000)):
            Price_Bucket = 'Fourth'
        elif((Price>600000)):
            Price_Bucket = 'Third'
        elif((Price>300000)):
            Price_Bucket = 'Second'
        else:
            Price_Bucket = 'First'

    if '2' in PRODUCT:
        if(Price>150000):
            Price_Bucket = 'last'
        elif((Price>90000)):
            Price_Bucket = 'Seventh'
        elif((Price>75000)):
            Price_Bucket = 'Sixth'
        elif((Price>65000)):
            Price_Bucket = 'Fifth'
        elif((Price>60000)):
            Price_Bucket = 'Fourth'
        elif((Price>50000)):
            Price_Bucket = 'Third'
        elif((Price>40000)):
            Price_Bucket = 'Second'
        else:
            Price_Bucket = 'First'

    return Price_Bucket

def get_age_bucket(PRODUCT, Age):

    if '4' in PRODUCT:
        if(Age>20):
            Age_Bucket = '>20'
        elif((Age>10)):
            Age_Bucket = '11to20'
        elif((Age>=8)):
            Age_Bucket = '8to10'
        elif((Age>=4)):
            Age_Bucket = '4to7'
        else:
            Age_Bucket = '0to3'
    if '2' in PRODUCT:
        if(Age>10):
            Age_Bucket = '>10'
        elif((Age>6)):
            Age_Bucket = '7to10'
        elif((Age>=4)):
            Age_Bucket = '4to6'
        elif((Age>=2)):
            Age_Bucket = '2to3'
        else:
            Age_Bucket = '0to1'

    return Age_Bucket

class recommendation():


    def func_recom(manuf_name, model_name, Rto, Age, PRODUCT):
        car_name = manuf_name+'_'+model_name
        grouper = ['PRODUCT', 'Price_Bucket', 'Age_Bucket', 'City_Bucket']

        data = pd.read_csv("./templates/Output_combined.csv")
        city =pd.read_csv("./templates/City_Grouping.csv")
        vehicle_price = pd.read_csv("./templates/Model.csv")

        temp_df = data.loc[(data.PRODUCT == PRODUCT)]

        Price = vehicle_price.loc[vehicle_price.Manu_Model == car_name]['Price']
        City_Bucket = city.loc[city.City == Rto.upper()]['City_Bucket']


        if len(Price) == 0:
            # if the car_name is not in our database
            grouper = list(set(grouper) - {'Price_Bucket'})

            # grouper.remove('Price_Bucket')
        else:
            Price = Price.iloc[0]
            # get the price bucket via the mapping
            Price_Bucket = get_price_bucket(PRODUCT, Price)
            temp_df = temp_df.loc[temp_df.Price_Bucket == Price_Bucket]

        if len(City_Bucket) == 0:
            # if the Rto is not in our database
            grouper = list(set(grouper) - {'City_Bucket'})

            # grouper.remove('City_Bucket')
        else:
            City_Bucket = City_Bucket.iloc[0]
            # get the city bucket via the mapping
            temp_df = temp_df.loc[temp_df.City_Bucket == City_Bucket]

        # get the age bucket
        Age_Bucket = get_age_bucket(PRODUCT, Age)
        temp_df = temp_df.loc[temp_df.Age_Bucket == Age_Bucket]

        col = ['ZD_Cover', 'RSA', 'PA', 'Val_Elec_Accessories', 'Val_Non_Elec_Accessories', 'Consumable_Cover', 'RTI_Cover', 'Anti_Theft_Cover', 'Geo_Ext_Cover', 'Garage_Cash', 'Bi_Fuel_Kit_Cover', 'Vol_Ded_Cover', 'Engine_Protect_Cover', 'Tyre_Protect_Cover', 'Add_Deductable_Cover', 'KP_Cover', 'LOPB_Cover']

        # Combination refers to Price_Bucket, Age_Bucket, City_Bucket

        if temp_df.shape[0]==0:
            # When the combination is not present in the output file
            temp = pd.DataFrame([[PRODUCT,Price_Bucket,Age_Bucket, City_Bucket]], columns = ['PRODUCT','Price_Bucket','Age_Bucket', 'City_Bucket'])
            for i in range(0, len(grouper)-1):
                data1 = data.copy()
                group = grouper[:len(grouper)-1-i]
                for j in group:
                    data1 = data1.loc[data1[j] == temp[j].iloc[0]]

                ## 100 is quite less; we can change it to 1000
                if data1.train_inst.sum()>=100:
                    for i in col:
                        data1[i] = data1[i]*data1['train_inst']
                    recommended_count = int(round(data1.Recommended_Count.mean(),0))
                    data1 = data1.groupby(group)[col].sum().reset_index()
                    recommended_covers = list(data1[col].iloc[0].sort_values(ascending = False)[:recommended_count].index.values)
                    telematics_covers = list(data1[col].iloc[0].sort_values(ascending = False)[:recommended_count+1].index.values)
                    return recommended_covers, telematics_covers

                    ## as we are using return, we can eliminate break from here.
                    break
        elif(temp_df.shape[0]==1):
            # When there is a perfect match, therefore, length is equal to 1

            recommended_covers = temp_df.Recommended_Covers
            telematics_covers = temp_df.Telematics_Covers
            return eval(recommended_covers.iloc[0]),eval(telematics_covers.iloc[0])
        else:
            # When the no of combinations is greater than 1
            # Possible when the Rto or car_name is not in our mappings

            data1 = temp_df.copy()
            recommended_count = int(round(data1.Recommended_Count.mean(),0))
            for i in col:
                data1[i] = data1[i]*data1['train_inst']
            data1 = data1.groupby(grouper)[col].sum().reset_index()
            recommended_covers = list(data1[col].iloc[0].sort_values(ascending = False)[:recommended_count].index.values)
            telematics_covers = list(data1[col].iloc[0].sort_values(ascending = False)[:recommended_count+1].index.values)
            return recommended_covers, telematics_covers
