from unittest.util import _MAX_LENGTH
import numpy as np
import pandas as pd
from sympy import sequence
import tensorflow as tf
import tensorflow_hub as hub
import joblib
import spacy
import random
from chatbot.models import Chatbot
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle




THRESH_HOLD=0.65
MAX_LENGTH= 308


user_name = ""
user_step = 0
next_step = 0
inputs = []


# Load models
# import NLP model created to classify user's inputs to one of the classes mentioned in `output_df`. More info on this is providied in `Train Breast Cancer NLP Model for Chatbot`
model_load  = tf.keras.models.load_model(r'chatbot\chatbot_models\models\NLP_model.h5', custom_objects={'KerasLayer': hub.KerasLayer})

loadedModel = joblib.load(r'chatbot\chatbot_models\models\BC_risk_model.pkl')
trained_nlp = spacy.load(r"chatbot\chatbot_models\models\output\model-best")
output_df = pd.read_json(r"chatbot\chatbot_data\save_replys_dataframe\output_df.json")


def checkBreastCancerRisk(user_step, user_input, request):
    print("test")
    print(user_step)
    if (user_step == 1):
        return ("Anyone can get Breast Cancer, however chances of getting Breast cancer are more if you or your first degree family memeber had history of Invasive or In situ Breast cancer and they are other risk factors.\nDo you want to analyze your risk of getting Breast Cancer? \nyou will be asked few questions and at the end you will get a result in terms of probabilty percentage(0% means least probable and  100% means most probable)\n do you want to continue? (y/n)", 2)
   
    if (user_step == 2 and user_input.casefold() != "yes".casefold() and   user_input.casefold() != "y".casefold()):
        return("No Problem, how else can I help you ?", 0)
    elif(user_step == 2):  
        return("What is your Meanopause status?\n If premenopausal enter '0' if postmenopausal or if age greater than or equal to 55 enter '1', if unknown enter '9' ",4)
            
    try:

        if (user_step>=4):
            request.session["inputs"].append(int(user_input))

        if (user_step == 4):   
            
            return("Enter Age Group:\n '1' for 35-39; '2' for 40-44; '3' for 45-49; '4' for 50-54; '5' for 55-59; '6' for 60-64; '7' for 65-69; '8' for 70-74; '9' for 75-79; '10' for 80-84",5)
        if (user_step == 5): 
            return("Do you know your Breast Density? If you don't know please enter '9' else enter according to the below mentioned categories:\n'1' for Almost entirely fat; '2' for Scattered fibroglandular densities; '3' for Heterogeneously dense; '4' for Extremely dense; '9' for Unknown or different measurement system",6)
            
        if (user_step == 6):
            return("Please mention your race as per below categories:\n'1' for white; '2' for Asian/Pacific Islander; '3' for black; '4; for Native American; '5' for other/mixed; '9' for unknown",7)
        if (user_step == 7):
            return("Are you a Hispanic? (a person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin regardless of race.)\n Enter'0' for no; '1' for yes; '9' for unknown",8) 
        if (user_step == 8):
            return("Enter your bmi:\nEnter '1' if BMI falls in '10-24.99'; 2 if bmi fall in '25-29.99'; 3 if bmi falls in '30-34.99'; '4' if bmi fall in '35 or more'; '9' if unknown",9)
        if (user_step == 9):
            return("What was your age when your first baby was born?\nEnter '0' if  Age was less than 30; '1' if Age was 30 or greater; Enter '2' if Nulliparous; Enter '9' if unknown",10)
        if (user_step == 10):
            return("How many of your first degree relatives have or had Breast cancer?\nEnter '0' for zero; '1' for one; '2' for 2 or more; '9' for unknown`",11)
        if (user_step == 11):
            return("Has any procedure, like biopsy or any breast related surgery was done on you?\nEnter '0' for 'no';Enter '1' = yes; '9' = unknown",12)    
        if (user_step == 12):
            return("Result of last mammogram you had:\n '0' for negative for suspected cancer; '1' for false positive for suspected cancer; '9' for unknown or none of the above. ",13)
        if (user_step == 13):
            return("Did you have Surgical menopause:\n'0' for natural; '1' for surgical; '9' for unknown or not menopausal (menopaus=0 or menopaus=9)",14)
        if(user_step == 14):
            return("Are you currently on hormone therapy?\nEnter '0' for no; '1' for yes; '9' for unknown or not menopausal (menopaus=0 or menopaus=9)",15)
    except:
            return("Please add numeric input", user_step )
    if(user_step == 15):
        print("test2")
        print(loadedModel.predict_proba([request.session["inputs"]]))
        probablity = loadedModel.predict_proba([request.session["inputs"]])[0][1]
        request.session["inputs"] =[]
        return(f"\nYour chance of getting Breast Cancer is: {probablity*100:.2f}%, anything else I can do for you?", 0)





def get_user_name(text):
    doc = trained_nlp(text)
            
    for ent in doc.ents:
        if (ent.label_ == "PERSON"):
            return ent.text
    return ""

def get_tokanized_input(user_input):

    with open(r"chatbot\chatbot_data\tokenizer\tokenizer.pickle", 'rb') as handle:
        tokenizer = pickle.load(handle)
    
    sequences = tokenizer.texts_to_sequences([user_input])
    padded_seq = pad_sequences(sequences=sequences, padding="post", truncating="post", maxlen =MAX_LENGTH )
    return padded_seq

def get_reply_from_BC_npl_model(user_input):

    padded_sequence = get_tokanized_input(user_input)
    print(padded_sequence)
    
    predicted_result = model_load.predict([padded_sequence])
    class_output = predicted_result[0].argmax()
    print(predicted_result[0][class_output])

    if (predicted_result[0][class_output] > THRESH_HOLD):
        response = random.sample(output_df[output_df['class'] ==class_output]['responses'].to_list()[0],1)[0]
    else:
        response = "Sorry!! I could not understand, could you please rephrase it?"
    return class_output, response 



def respond_to_user(user_input, request):
    additional_data_to_response = ""
    
    if(request.session.get('asked_for_name')==1):
        if (len(user_input.split()) <=1):
            request.session['asked_for_name']=0
            request.session["user_name"] = user_input.split()[0]
            return f"{request.session['user_name']} please feel free to ask any question you have.\n"
        else:
            expected_name = get_user_name(user_input)
            if (expected_name!=""):
                request.session['asked_for_name']=0
                request.session["user_name"] = expected_name
                return f"{request.session.get('user_name')} please feel free to ask any question you have.\n"
            else:
                return "Sorry I could not understand, could you please rephrase it?"


    class_output, response = get_reply_from_BC_npl_model(user_input)
    if request.session.get("user_name") == "":
        name = get_user_name(user_input[:30])
        if (name!=""):
            request.session["user_name"] = name
        else:
            request.session['asked_for_name']=1
            additional_data_to_response = "May I know your name?"

    if (request.session.get("user_step") == 0 and response != ""):
        response = response.replace("{username}", request.session.get('user_name'))
        
        if(output_df[output_df['class'] == class_output ]['tag'].to_list()[0] == "CancerRisk"):
            request.session["user_step"] +=1
            response, request.session["user_step"] = checkBreastCancerRisk(request.session.get("user_step"), user_input,request)
        if (additional_data_to_response == ""):
            return response
        else:
            return response +"\n" + additional_data_to_response
    
    if(request.session.get("user_step")> 0 or output_df[output_df['class'] == class_output ]['tag'].to_list()[0] == "CancerRisk"):
        response, request.session["user_step"] = checkBreastCancerRisk(request.session.get("user_step"), user_input,request)
        return response