import gradio as gr
import joblib
import pandas as pd
# Save the models
import joblib
joblib.dump(dtree, 'dt_model.joblib')
joblib.dump(rfc, 'rf_model.joblib')

# Load the models
dt_model = joblib.load('dt_model.joblib')
rf_model = joblib.load('rf_model.joblib')

# Define a prediction function
def predict_sleep_disorder(model_name, *input_data):
    model = dt_model if model_name == 'Decision Tree' else rf_model
    input_df = pd.DataFrame([input_data], columns=input_features)
    prediction = model.predict(input_df)
    return prediction[0]

# Define the input features
input_features = ['feature1', 'feature2', 'feature3']  # replace with your actual feature names
## Prediction for Single Data Point

# Create the Gradio interface
inputs = [gr.components.Radio(['Decision Tree', 'Random Forest'], label='Model Choice')]
inputs += [gr.components.Textbox(label=feature) for feature in input_features]
outputs = gr.components.Textbox(label='Prediction')

gr_interface = gr.Interface(
    fn=predict_sleep_disorder,
    inputs=inputs,
    outputs=outputs,
    live=True
)

# Launch the interface
if __name__ == '__main__':
    gr_interface.launch()
