#streamlit run C:\Users\LEGION\Documents\GIT\no-code-app-for-GPT-research\structured_output.py
import streamlit as st
import pandas as pd
import json
import os
import sys
from datetime import datetime
import pickle

# TO DO:
# ADD a variable for client to you can talk to LM Studio server
# ADD a variable for client to you can talk to claude
# ADD Temperature, max_token, seed for model parameters


#-------- Changeable ------------# Define changable variables
# path of code script
script_path = os.path.abspath(sys.argv[0])
script_directory = os.path.dirname(script_path)
#S0S0
log_file_path=os.path.join(script_directory, "structured_output_logs.txt")
#S0S1
pickle_filename = "structured_output_save_defaults.pickle"
pickle_file_path = os.path.join(script_directory, pickle_filename)
#variable for column names in df4review excel/csv file
mrn_col = 'mrn'
date_col = "date"
proc_col = "procedure notes"
path_col = "pathology notes"

defaults_from_pickle_defults = {
    "model_name": None,
    "model_api": None,
    "model_asynchronous_call": False,
    "model_asynchronous_call_number": 0,
    "model_advancedparameters":False,
    "model_advancedparameters_seed":0,
    "model_advancedparameters_temperature":0,
    "model_advancedparameters_max_token":0,
    "schema_description": None,
    "schema_object":{}
}


#----------S0S0 Log file -----------
def append_log(log_message, log_file_path=log_file_path):
    """Appends a log message to the specified file, separated by dashes."""
    # get current time of log
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    separator = "-------\n"
    log_entry = f"{separator}{timestamp} - {log_message}\n"
    
    try:
        # Open the file in append mode, which creates the file if it doesn't exist
        with open(log_file_path, "a") as file:
            file.write(log_entry)
        print("Log appended successfully.")
    except Exception as e:
        print(f"Failed to append log due to: {e}")
        
#----------S0S0 Pickle-------------------------
# Section 0 - Sub 1 - Pickle file (for defaults) # This pickel file will act as a dictionary of defaults.
def load_pickle_file(pickle_file_path=pickle_file_path):
    """Function for loading/creating a pickle file and add it to session_state['defaults_from_pickle']"""
    # Create pickle file for the first time 
    if not os.path.exists(pickle_file_path):
        with open(pickle_file_path, 'wb') as file:
            default_json_file_path = os.path.join(script_directory,'manualreview_data.json')
            default_df4review_path=os.path.join(script_directory,'df4review_data.csv')
            defaults_from_pickle = defaults_from_pickle_defults
            pickle.dump(defaults_from_pickle, file)
            append_log("The pickle file (containing defaults of webapp) was created")
    else: # Load pickle file if it exists
        with open(pickle_file_path, 'rb') as file:
            defaults_from_pickle = pickle.load(file)
            #add new keys, if not included in the loaded pickle
            for key, value in defaults_from_pickle_defults.items():
                defaults_from_pickle[key]=value
            append_log("The pickle file (containing defaults) was loaded")
    st.session_state['defaults_from_pickle'] = defaults_from_pickle

def write_to_pickle_file_and_update_ss(key, value, pickle_file_path=pickle_file_path):
    """Function to write a value to pickle file for the given key and update session state['defaults_from_pickle']"""
    try:
        with open(pickle_file_path, 'rb') as file:
            defaults_from_pickle = pickle.load(file)
        defaults_from_pickle[key] = value
        with open(pickle_file_path, 'wb') as file:
            pickle.dump(defaults_from_pickle, file)
            st.session_state['defaults_from_pickle'] = defaults_from_pickle
            append_log(f"Successfully changed pickle file key ({key}) to value of: {value}")
    except Exception as e:
        append_log(f"Failed to change pickle file key ({key}) to value of: {value} due to ERROR: {e}")


#--------- S0:opneai  -----------------------------
def streamlit_define_modelparameteres():
    st.subheader("Model Parameters")
    modelparameteres_col1,modelparameteres_col2,modelparameteres_col3=  st.columns([2,1,1])
    modelparameteres_col1_col1, modelparameteres_col1_col2= modelparameteres_col1.columns([1,1])
    
    try:
        with modelparameteres_col1:
            # deinining the model name and api
            model_name = st.text_input(label="Enter the exact OpenAI model",placeholder='e.g. gpt-4' , help="Check this page for exact names: https://platform.openai.com/docs/models", value=st.session_state['defaults_from_pickle'].get("model_name", None),key='model_name')
            model_api  = st.text_input(label="Enter your OpenAI API" ,type='password', value=st.session_state['defaults_from_pickle'].get("model_api", None), key='model_api')

            
            model_asynchronous_call= modelparameteres_col1_col1.toggle(label="Using asynchronous call",help="This will send multiple requests at once. This is not advised during the test stage, as you can lose a lot of money in seconds.", value=st.session_state['defaults_from_pickle'].get("model_asynchronous_call", False),key='model_asynchronous_call')
            
            if model_asynchronous_call:
                with modelparameteres_col2:
                    st.info("Watch out with using this feature as you are sending many requests at once. I suggest to do it with 3 batches at first, then increase it. Also, consider your request limits.")
                    model_asynchronous_call_number = st.number_input(label="Number of requests to send at once", help="This depends on your tier. At some point you will hit your request per minute or token per minute limit. You can check your current limit on your OpenAI platform account.",value=st.session_state['defaults_from_pickle'].get("model_asynchronous_call_number", None),key='model_asynchronous_call_number')  
            else:
                model_asynchronous_call_number=0
                
            model_advancedparameters =  modelparameteres_col1_col2.toggle(label="Using asynchronous call",help="This will send multiple requests at once. This is not advised during the test stage, as you can lose a lot of money in seconds.", value=st.session_state['defaults_from_pickle'].get("model_advancedparameters", False),key='model_advancedparameters')
            if model_advancedparameters:
                with modelparameteres_col3:
                    model_advancedparameters_seed =  st.number_input(label="Number of requests to send at once", help="If you are not familiar with this look https://platform.openai.com/docs/api-reference.",value=st.session_state['defaults_from_pickle'].get("model_advancedparameters_seed", None),key='model_advancedparameters_seed') 
                    model_advancedparameters_temperature=   st.number_input(label="Number of requests to send at once", help="If you are not familiar with this look https://platform.openai.com/docs/api-reference.",value=st.session_state['defaults_from_pickle'].get("model_advancedparameters_temperature", None),key='model_advancedparameters_temperature') 
                    model_advancedparameters_max_token=  st.number_input(label="Number of requests to send at once", help="If you are not familiar with this look https://platform.openai.com/docs/api-reference.",value=st.session_state['defaults_from_pickle'].get("model_advancedparameters_max_token", None),key='model_advancedparameters_max_token') 
            else:
                model_advancedparameters_seed = model_advancedparameters_temperature = model_advancedparameters_max_token = 0
                
            
        if st.button(label="Press when finished", key="streamlit_define_modelparameteres_done"): 
            write_to_pickle_file_and_update_ss("model_name", model_name)
            write_to_pickle_file_and_update_ss("model_api", model_api) 
            write_to_pickle_file_and_update_ss("model_asynchronous_call",model_asynchronous_call)
            write_to_pickle_file_and_update_ss("model_asynchronous_call_number",model_asynchronous_call_number)
            write_to_pickle_file_and_update_ss("model_advancedparameters",model_advancedparameters)
            write_to_pickle_file_and_update_ss("model_advancedparameters_seed",model_advancedparameters_seed)
            write_to_pickle_file_and_update_ss("model_advancedparameters_temperature",model_advancedparameters_temperature)
            write_to_pickle_file_and_update_ss("model_advancedparameters_max_token",model_advancedparameters_max_token)
            
            ss_model_name=st.session_state['defaults_from_pickle']["model_name"]
            ss_first_4_letters_of_api = st.session_state['defaults_from_pickle']["model_api"][0:4]
            if ss_model_name and ss_first_4_letters_of_api:
                    
                st.success(f"Successful defined the model parameters.  API: {ss_first_4_letters_of_api}***  Model: {ss_model_name}")
                append_log(f"""SUCCESS on streamlit_define_modelparameteres. 
                                Session_state: {st.session_state}""")  
                return True
            else:
                st.write("You should define model name and api before going to the next step")
                return False
        else:
            return False
    except Exception as e:
        st.error(f"ERROR in streamlit_define_modelparameteres: {e}")
        append_log(f"ERROR in streamlit_define_modelparameteres: {e} ")
        return False

    
#--------- S0:schema  -----------------------------
def streamlit_define_schema():
    streamlit_define_schema_col1, streamlit_define_schema_col2= st.columns([4,1])
    try:
        schema_description  = st.text_area(label="Define your ", value=st.session_state['defaults_from_pickle'])
        schema_numberofobject= st.number_input(label="Number of objects for extraction")
        "schema_object"
        
        
    except Exception as e:
        st.error(f"ERROR in streamlit_define_schema: {e}")
        append_log(f"ERROR in streamlit_define_schema: {e} ")
        return False
    
    
    
#--------- S0:data  --------------------------------
def streamlit_define_data():
    print("hi")


def main():
    st.set_page_config(layout="wide")
    st.header('OpenAI no-code playground')
    load_pickle_file()
    
    streamlit_define_modelparameteres_done = streamlit_define_modelparameteres()
    
    if streamlit_define_modelparameteres_done:
        st.write(st.session_state)
    else:
        st.write("Please define model parameters")
    with st.sidebar:
        st.write(st.session_state)
    

if __name__ == "__main__":
    main()

    
    