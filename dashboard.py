import pandas as pd
import numpy as np
import streamlit as st
import boto3
import io
from PIL import Image
from ast import literal_eval

st.title('Image Viewer!')

def safe_literal_eval(input_str):
    try:
        return literal_eval(input_str)
    except:
        return None

if 's3' not in st.session_state:
    id = st.secrets['aws_access_key_id']
    access_key = st.secrets['aws_secret_access_key']
    region_name = st.secrets['region_name']
    st.session_state['bucket_name'] = st.secrets['bucket_name']
    s3 = boto3.client('s3', aws_access_key_id=id,
                  aws_secret_access_key=access_key,
                  region_name=region_name)
    st.session_state['s3'] = s3


df = pd.read_csv('All_Field_Inspection_Field_Photos.csv')
field_ids = list(df.croppableAreaId.unique())
field_id = st.selectbox('Select a Field ID: ',field_ids)
df_filtered = df[df.croppableAreaId==field_id]
df_filtered['date'] = pd.to_datetime(df_filtered.executedOn).dt.date
dates = list(df_filtered.date.unique())
date = st.selectbox('Select a date: ',dates)

temp_df = df_filtered[df_filtered.date==date]
for index,row in temp_df.iterrows():
    if row['FieldPhot1hldr']!='None':
        key = 'CropIn_Photos/'+str(df.loc[index,'FieldPhot1hldr'])
        try:
            response = st.session_state['s3'].get_object(Bucket=st.session_state['bucket_name'], Key=key)
            image_content = response['Body'].read()
            image = Image.open(io.BytesIO(image_content))
            st.image(image)
        except:
            pass

    if row['FieldPhot2hldr']!='None':
        key = 'CropIn_Photos/'+str(df.loc[index,'FieldPhot2hldr'])
        try:
            response = st.session_state['s3'].get_object(Bucket=st.session_state['bucket_name'], Key=key)
            image_content = response['Body'].read()
            image = Image.open(io.BytesIO(image_content))
            st.image(image)
        except:
            pass

    if not pd.isna(row['Soilmoist5hldr']):
        lst = safe_literal_eval(row['Soilmoist5hldr'])
        for image in lst:
            try:
                key = 'CropIn_Photos/'+image['originalFileName']
                response = st.session_state['s3'].get_object(Bucket=st.session_state['bucket_name'], Key=key)
                image_content = response['Body'].read()
                image = Image.open(io.BytesIO(image_content))
                st.image(image)
            except:
                pass

    