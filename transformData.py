import streamlit as st
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score


def convertCheckboxToInt(variavel):
    if variavel == 1:
        return 1
    return 0


def convertMultiSelect(values):
    if values.any() == False:
        return 0
    return 1

def convertGenderToInt(variavel):
    if variavel[0] == "Masculine":
        return 1
    return 0


def convertAlcool(variavel):
    if variavel[0] == "Yes":
        return 1
    return 0


def normalize(value, min, max):
    normalized = (value[0] - min) / (max - min)
    return normalized

    
#value = switcher.get(proveniencia, 0)



def get_user_input_with_gasome(fcol1, fcol2, fcol3, fcol4):
    
    proveniencia = fcol1.selectbox("Patient origin", ("Home", "Inter-hospital patient transfer", "Intra-hospital patient transfer", "Nursing home"))
    grupoDiagnostico = fcol1.selectbox("Admission category", ("Hemato-oncology","Neurology","Respiratory","Cardiovascular","Musculoskeletal","Genitourinary","Gastrointestinal","Other"))
    localSU = fcol1.selectbox("Urgent admission",("Ambulatory","UCISU","UDC1","UDC2"))
    idade = fcol1.slider("Age", min_value=18, max_value=100, step=1)
    gender = fcol1.radio("Gender:", ("Feminine", "Masculine"))
    tempo = fcol1.number_input("Length of stay", min_value=0.08, max_value=12.0, step=0.01 ,help="Number of days")
    sirs = fcol2.slider("SIRS Criteria:",min_value=0, max_value=4, step=1, help="fever >38.0°C or hypothermia <36.0°C, tachycardia >90 beats/minute, tachypnea >20 breaths/minute, leucocytosis >12*109/l or leucopoenia <4*109/l")
    glicose = fcol2.number_input("Glucose levels (mg/dL)", min_value=41.0, max_value=1000.0, step=0.01, help="Reference range: 90-130 mg/dL", value= 90.0)
    sodio = fcol2.number_input("Sodium blood test (mEq/L)", min_value=42.0, max_value=151.0, step=0.01, help="Reference range: 135-146 mEq/L", value=136.0)
    ureia = fcol2.number_input("Blood urea nitrogen (mg/dL)", min_value=4.0, max_value=275.0, step=0.01, help="Reference range: 19-49 mg/dL", value=21.0)
    creatinina = fcol2.number_input(
        "Creatinine (mg/dL)", min_value=0.1, max_value=19.5, step=0.01, help="Reference range: 0.6-1.2 mg/dL", value=0.8
    )
    pcr = fcol2.number_input("CRP (mg/L)", min_value=2.90, max_value=499.00, step=0.01, help="C-reactive protein. Reference range: < 5mg/L")
    ph = fcol2.number_input("pH", min_value=7.026, max_value=7.625, step=0.001, help="Reference range: 7.35-7.45", value=7.38)
    ca = fcol3.number_input("Ionized calcium (mmol/L)", min_value=0.84, max_value=1.37, step=0.01, help="Reference range: 1.15-1.35 mmol/L", value=1.21)
    co2 = fcol3.number_input("Partial pressure of carbon dioxide (mm Hg)", min_value=13.2, max_value=121.3, step=0.01, help=" Reference range: 33-45 mm Hg", value=36.3)
    o2 = fcol3.number_input("Partial pressure of oxygen (mm Hg)", min_value=34.1, max_value=178.1, step=0.01, help= "Reference range: 75-105 mm Hg", value=87.9)
    hco3 = fcol3.number_input("Bicarbonate (mEq/L)", min_value=7.40, max_value=39.1, step=0.01, help="Reference range: 22-28 mEq/L", value=24.6)

    antidislipidemicos = fcol3.multiselect(
        'Antidyslipidemic',
        ['Rosuvastatine', 'Atorvastatine', 'Pravastatine', 'Sinvastatine', 'Fluvastatine'],
        default=None,
        help="Rosuvastatine, Atorvastatine, Pravastatine, Sinvastatine, Fluvastatine"
    ),
    antipsicoticos = fcol3.multiselect(
        'Antipsychotics',
        ['Haloperidol', 'Quetiapine', 'Risperidone', 'Paliperidone', 'Iloperidone'],
        default=None,
        help="Haloperidol, Quetiapine, Risperidone, Paliperidone, Iloperidone"
    ),
    antidepressores = fcol4.multiselect(
        'Antidepressants',
        ['Fluvoxamine','Paroxetine', 'Sertraline', 'Venlafaxine', 'Trazodone', 'Amitriptyline'],
        default=None,
        help="Fluvoxamine, Paroxetine, Sertraline, Venlafaxine, Trazodone, Amitriptyline"
    ),

    #antihipertensores = fcol3.multiselect(
    #    'Antihipertensores',
    #    ['Nifedipine','Captopril','Clonidine'],
    #    default=None,
    #    help="HEP_TEXT"
    #),

    analgesicos = fcol4.multiselect(
        'Analgesics',
        ['Nifedipine','Captopril','Clonidine'],
        default=None,
        help="Nifedipine, Captopril, Clonidine"
    ),
    anticoagulantes = fcol4.multiselect(
        'Anticoagulants',
        ['Warfarin','Dipyridamole'],
        default=None,
        help="Warfarin, Dipyridamole"
    ),
    corticosteroides = fcol4.multiselect(
        'Corticosteroids',
        ['Hydrocortisone','Prednisone'],
        default=None,
        help="Hydrocortisone, Prednisone"
    ),
    digitalicos = fcol4.multiselect(
        'Digitalis',
        ['Digoxin'],
        default=None,
        help="Digoxin"
    ),
    outrosMed = fcol4.multiselect(
        'Other medicines',
        ['Ranitidine','Scopolamine', 'Desloratadine', 'Hydroxyzine', 'Trihexyphenidyl', 'Trospium'],
        default= None,
        help="Ranitidine, Scopolamine, Desloratadine, Hydroxyzine, Trihexyphenidyl, Trospium"
    ),
    
    alcoolico = fcol1.radio("Alcohol dependence?", ["Yes", "No"], index=1)

    # Guardar o dicionário numa variável
    user_data = {
        "Patient origin": proveniencia,
        "Admission category": grupoDiagnostico,
        "Urgent admission": localSU,
        "Age": idade,
        "Gender": gender,
        "Length of stay": tempo,
        "SIRS Criteria" : sirs,
        "Glucose levels": glicose,
        "Sodium blood test": sodio,
        "Blood urea nitrogen": ureia,
        "Creatinine": creatinina,
        "CRP": pcr,
        "pH": ph,
        "Ionized calcium": ca,
        "CO2": co2,
        "O2": o2,
        "HCO3": hco3,
        "Antidyslipidemic":antidislipidemicos,
        "Antipsychotics":antipsicoticos,
        "Antidepressants":antidepressores,
        "Analgesics":analgesicos,
        "Anticoagulants": anticoagulantes,
        "Corticosteroids":corticosteroides,
        "Digitalis":digitalicos,
        "Other medicines":outrosMed, 
        "Alcohol dependence": alcoolico,  
    }

    # Transformar os dados inseridos pelo utilizador num dataframe
    features = pd.DataFrame(user_data, index=[0])
    return features


def convertLocalSu(variavel):
    switcher = {
        'Ambulatory': 0,
        'UCISU': 1,
        'UDC1': 2,
        'UDC2': 3,
    }
    return switcher[variavel[0]]

def convertProv(variavel):
    dic = {
        'Home': 1 if variavel[0] == 'Home' else 0, 
        'Inter-hospital patient transfer': 1 if variavel[0] == 'Inter-hospital patient transfer' else 0,
        'Intra-hospital patient transfer': 1 if variavel[0] == 'Intra-hospital patient transfer' else 0,
        'Nursing home': 1 if variavel[0] == 'Nursing home' else 0,
    }
    return dic


def convertGrupoDiag(variavel):
    dic = {
        'GrupoDiagn_Hemato-Oncologico': 1 if variavel[0] == 'Hemato-oncology' else 0, 
        'GrupoDiagn_Neurologico': 1 if variavel[0] == 'Neurology' else 0,
        'GrupoDiagn_Respiratorio': 1 if variavel[0] == 'Respiratory' else 0,
        'GrupoDiagn_Musculoesqueletico': 1 if variavel[0] == 'Musculoskeletal ' else 0,
        'GrupoDiagn_Cardiovascular': 1 if variavel[0] == 'Cardiovascular' else 0,
        'GrupoDiagn_Geniturinario': 1 if variavel[0] == 'Genitourinary' else 0,
        'GrupoDiagn_Gastrointestinal': 1 if variavel[0] == 'Gastrointestinal' else 0,
        'GrupoDiagn_Outro': 1 if variavel[0] == 'Other' else 0,
    }
    return dic


def convert_user_input_data_to_predict_format(features):
# Guardar o dicionário numa variável
    data_to_predict = {
        "Age": normalize(features["Age"],18,100),
        "Gender": convertGenderToInt(features["Gender"]),
        "Length of stay": normalize(features["Length of stay"],0.083,12),
        "SIRS" : normalize(features["SIRS Criteria"],0,4),
        "Glucose levels": normalize(features["Glucose levels"],41,1000),
        "Sodium blood test": normalize(features["Sodium blood test"],42,151),
        "Blood urea nitrogen": normalize(features["Blood urea nitrogen"],4,275),
        "Creatinine": normalize(features["Creatinine"],0.1,19.5),
        "CRP": normalize(features["CRP"],2.3,499),
        "pH": normalize(features["pH"],7.026,7.625),
        "Ionized calcium": normalize(features["Ionized calcium"],0.84,1.37),
        "pCO2": normalize(features["CO2"],13.2,121.3),
        "pO2": normalize(features["O2"],34.1,178.1),
        "HCO3": normalize(features["HCO3"],7.40,39.1),
        "Urgent admission": convertLocalSu(features["Urgent admission"]),
        "Antidyslipidemic": convertMultiSelect(features["Antidyslipidemic"]),
        "Antipsychotics": convertMultiSelect(features["Antipsychotics"]),
        "Antidepressants": convertMultiSelect(features["Antidepressants"]),
        "Analgesics": convertMultiSelect(features["Analgesics"]),
        "Anticoagulants": convertMultiSelect(features["Anticoagulants"]),
        "Alcohol dependence": convertMultiSelect(features["Alcohol dependence"]),
        "Corticosteroids": convertMultiSelect(features["Corticosteroids"]),
        "Digitalis": convertMultiSelect(features["Digitalis"]),
        "Outros Med_Presente": convertMultiSelect(features["Other medicines"]),
    }

    merged = {** data_to_predict, **convertProv(features["Patient origin"])}
    merged = {** merged, **convertGrupoDiag(features["Admission category"])}

    return pd.DataFrame(merged, index=[0])
