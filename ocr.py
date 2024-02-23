import easyocr as ocr  #OCR
import streamlit as st  #Web App
from PIL import Image #Image Processing
import numpy as np #Image Processing 
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import matplotlib.pyplot as plt
import re

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
img_contact_form = Image.open("images/yt_contact_form.png")
img_lottie_animation = Image.open("images/yt_lottie_animation.png")




st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")
#title
# ---- HEADER SECTION ----
with st.container():
    
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Hi,Are You a Steady Packaged Food Consumer?")
        st.title("Welcome...!:wave:")
        st.title("To Food Researcher")
        st.write(
            "Know the risks rates and their toxcity of every chemical used in your daily packages! "
        )

    
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")
        
# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")




#image uploader
image = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])


@st.cache
def load_model(): 
    reader = ocr.Reader(['en'],model_storage_directory='.')
    return reader 

reader = load_model() #load model
result_text = []


if image is not None:

    input_image = Image.open(image) #read image
    st.image(input_image) #display image

    with st.spinner("🤖 AI is at Work! "):
        

        result = reader.readtext(np.array(input_image))


        for text in result:
            result_text.append(text[1])

        #st.write(result_text)
    #st.success("Here you go!")
    
   
    
    st.balloons()

else:
    st.write("Upload an Image")
    
    

    
    
df = pd.read_excel(r"D:\persis files\GD\Dataset.xlsx")

elements = [
"Behaviour", "Biomass", "Body weight", "Clinical Chemistry", "Clinical signs",
"Development", "Food consumption", "Food efficiency", "Frond number", "Gross pathology",
"Growth", "Haematology", "Histopathology Neoplastic", "Histopathology non neoplastic",
"Immunology", "Mobility", "Morphology", "Mortality", "Neurology",
"No adverse effect observed", "No adverse effect observed at single/highest dose",
"No data", "Not reported", "Ophthalmoloscopic examination", "Organ weights", "Other",
"Reproduction", "Seedling emergence", "Time to hatch", "Time to swim up",
"Urinalysis", "Blanks"
]
result_text=" ".join(result_text)
result_text=result_text.split(",")
result_text=list(result_text)

nnli=[]
for i in result_text:
  li=[]
  for j in i:
    if j.isalpha():
      li.append(j)
  #print(li)
  nli=''.join(li)
  nnli.append(nli)
  #print(nnli)
#li= re.sub("[()[],.:;{}]", "", result_text)
print(nnli)
 
global tox
for i in nnli:
    ind=df.index[df["Substance"]==i]
    tox=df.loc[ind]["Effect"]
    

toxicity_colors = []
hightox = ["clinical signs","gross pathology","histopathology neoplastic","histopathology non neoplastic","mortality","neurology","ophthalmoloscopic examination","reproduction"]
moderatetox = ["clinical chemistry","haematology","immunology","organ weights","urinalysis","body weight"]
lowtox = ["behaviour","biomass","development","food consumption","food efficiency","frond number","growth","mobility","morphology","no adverse effect observed at single/highest dose","seedling emergence","time to hatch","time to swim up"]

for i in tox:
  i=i.lower()
  if i in hightox:
    toxicity_colors.append('red')
  elif i in moderatetox:
    toxicity_colors.append('orange')
  elif i in lowtox:
    toxicity_colors.append('yellow')
  else:
    toxicity_colors.append('green') 
st.write("nnli")
st.write(nnli)    
st.write("tox")
st.write(list(tox))

fig1, ax1 = plt.subplots()
#plt.figure(figsize=(10, 8))
ax1.pie([1] * len(tox), labels=tox, colors=toxicity_colors, startangle=140)
ax1.axis('equal')
#ax1.title('Pie Chart of Toxicity Levels')
#plt.show()
st.pyplot(fig1)

        







