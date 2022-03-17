import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from transformData import get_user_input_with_gasome, convert_user_input_data_to_predict_format
import joblib

#Page headers
st.set_page_config(
    page_title='Predicting Delirium Risk', 
    page_icon=None, 
    layout="wide", 
    #initial_sidebar_state="collapsed", 
    menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': None
     }
)

st.sidebar.title("About")
st.sidebar.write("The web application was developed by Célia Figueiredo, under the supervision of Professor Ana Cristina Braga and co-supervision by José Mariz.") 
st.sidebar.write("Its construction was part of the dissertation for the completion of the MSc in Systems Engineering at the University of Minho. The classification algorithm used was logistic regression that presents an accuracy of 0.847, as well as an AUC of the ROC curve of 0.83 and an AUC of the Precision-Recall curve of 0.582. This model is composed of 26 independent variables.")
 
 
    
#remover side menu
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

#Page Title
st.title('Predict the risk of delirium among people admitted to a hospital setting.')

#change_text = """
#    <style>
#    div.stMultiSelect .st-ek {visibility: hidden;}
#    div.stMultiSelect .st-ek:before {content: "Selecione uma opção"; visibility: visible;}
#    </style>

#st.markdown(change_text, unsafe_allow_html=True)


header_container = st.container()
filters_container = st.container()
results_container = st.container()


# load the model from disk
clf = joblib.load('final_model.sav')

#Criacao de um título e subtitulo
header_container.write("""
Delirium is a common but serious condition that is under recognized and associated with poor outcomes. However, delirium can be prevented and treated if it is diagnosed in time. It is therefore essential that all hospital staff be aware of the possibility of delirium developing, and that prompt assessment and appropriate management are ensured. This web application has been designed to support healthcare staff and alert them to the development of delirium in patients admitted to a hospital environment.""")

filters_container.subheader("Please fill the form")
filters_container.write("Please complete all the information requested below to make a prediction of delirium. If you do not modify the content of a field, the default value will be applied.s")
fcol1, fcol2, fcol3, fcol4 = filters_container.columns(4)

# guardar o input do utilizador numa variavel
user_input = get_user_input_with_gasome(fcol1, fcol2, fcol3, fcol4)

# Configurar uma subhead e mostrar aos utilizadores input
results_container.subheader('Check if you entered the information correctly:')
results_container.write('Please check the table below to make sure that the data entered matches the desired values.')

results_container.write(user_input)

# Guardar o modelospd.DataFrame(data_to_predict, index=[0]) preditos numa variavel

# Exemplo de dados de entrada para o algoritmo de previsão 
# data = {'Casa': [0], 'Inter-Hospitalar ': [0], 'Intra-Hospitalar': [0], 'Lar': [0], 'GrupoDiagn_Cardiovascular': [0], 'GrupoDiagn_Gastrointestinal': [1], 'GrupoDiagn_Geniturinario': [0], 'GrupoDiagn_Hemato-Oncologico': [0], 'GrupoDiagn_Musculoesqueletico': [0], 'GrupoDiagn_Neurologico ': [0], 'GrupoDiagn_Outro': [0], 'GrupoDiagn_Respiratorio': [0], 'Local_SU': [2], 'Idade': [0.792682927], 'Interna_Dias': [0.034992028], 'SIRS': [0.0], 'Glicose': [0.057351408], 'Sodio': [0.798165138], 'Ureia': [0.712177122], 'Creatinina': [0.201030928], 'PCR': [0.128447755], 'pH': [0.607679466], 'Ca_ionizado': [0.339622642], 'pCO2': [0.301572618], 'pO2': [0.388194444], 'HCO3 ': [0.460567823], 'Genero': [1], 'Antidislipidemicos': [0], 'Antipsicoticos': [0], 'Antidepressores': [0], 'Analgesicos': [0], 'Anticoagulantes': [1], 'Digitalicos': [0], 'Corticosteroides': [0],'Outros Med_Presente': [0], 'Alcoolico': [0]}


def res(prediction):
    if prediction == 0:
        pred = 'The person is unlikely to develop delirium.'
    else:
        pred = 'The individual may present a case of delirium.'
    return pred


def predictP():
    input_data_converted = convert_user_input_data_to_predict_format(user_input)
    prediction = clf.predict(input_data_converted)
    st.write(res(prediction[0]))

#results_container.button(
#    label='Calcular Previsão',
#    on_click=predictP()
#)


results_container.subheader('Forecast Results:')
predictP()


#prediction = clf.predict(data_to_predict)
# configurar um subheader e mostrar a classificação
#results_container.subheader('Classification:')
#st.write(res(prediction))



