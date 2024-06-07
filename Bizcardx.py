from sys import path
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd 
import numpy as np 
import re


def image_to_text(path):
  input_img= Image.open(path)

  #converting image to array format
  image_arr= np.array(input_img)

  reader = easyocr.Reader(['en'])
  text= reader.readtext(image_arr,  detail= 0)

  return text, input_img

def extracted_text(texts):

  extrd_dict={"NAME":[],"DESIGNATION":[],"COMPANY_NAME":[],"CONTACT":[],"EMAIL":[],"WEBSITE":[],"ADDRESS":[],"PINCODE":[]}

  extrd_dict["NAME"].append(texts[0])
  extrd_dict["DESIGNATION"].append(texts[1])

  for i in range(2,len(texts)):
    
    if texts[i].startswith("+") or (texts[i].replace("-","").isdigit() and '-' in texts[i]):

      extrd_dict["CONTACT"].append(texts[i])

    elif "@" in texts[i] and ".com" in texts[i]:
      extrd_dict["EMAIL"].append(texts[i])

    elif "WWW" in texts[i] or "www" in texts[i] or "Www" in texts[i] or "wWw" in texts[i] or "wWW" in texts[i]:
      small= texts[i].lower()
      extrd_dict["WEBSITE"].append(small)

    elif "Tamil Nadu" in texts[i] or "TamilNadu" in texts[i] or texts[i].isdigit():
        extrd_dict["PINCODE"].append(texts[i])

    elif re.match(r'^[A-Za-z]', texts[i]):
        extrd_dict["COMPANY_NAME"].append(texts[i])

    else:
      remove_colon= re.sub(r'[,;]','',texts[i])
      extrd_dict["ADDRESS"].append(remove_colon)

  for key,value in extrd_dict.items():
    if len(value)>0:
      concadenate= " ".join(value)
      extrd_dict[key] = [concadenate]

    else:
      value = "NA"
      extrd_dict[key] = [value]

  return extrd_dict

  

  print(extrd_dict)


#streamlit part

st.set_page_config(layout = "wide")
st.title("EXTRACTING BUSINESS CARD DATA WITH 'OCR'")

with st.sidebar:

  select= option_menu("Main Menu", ["Home", "Upload & Modifying", "Delete"])

if select == "Home":
   pass

elif select== "Upload & Modifying":
     img = st.file_uploader("Upload the Image",type=["png","jpg","jpeg"])

     if img is not None:
      st.image(img, width= 300)

      text_image, input_img= image_to_text(img)

      text_dict= extracted_text(text_image)

      if text_dict:
        st.success("TEXT IS EXTRACTED SUCCESSFULLY")

      df=pd.DataFrame(text_dict)

      st.dataframe(df)

elif select == "Delete":
 pass
  
