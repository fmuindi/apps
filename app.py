import gradio as gr
import pandas as pd

# Load the CSV file into a DataFrame
csv_url = 'https://raw.githubusercontent.com/fmuindi/My_Sample_Dataset/main/dataset.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_url)


# Function to get data from a specific row
def get_row_data(row_number):
    if 0 <= row_number < len(df):
        # Extract data for the given row number
        return df.iloc[row_number].to_dict()
    else:
        # Return a message if the row number is out of range
        return {"Error": "Data out of range."}

# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="DataTrailblazer") as demo:
    gr.Markdown(
                "<h2 style='color: #4F46E5; font-size: 50pt; font-weight: bold; text-align: center; border: 2px #4F46E5e; padding: 10px; display: inline-block;'>DataTrailblazer</h2>"
                "<h3 style='color: #3d3a4b;'>Generated AI Responses from a predefined dataset. Responses are rated based on accuracy and relevance</h3>"
                "<p style='color: #3d3a4b;'>Scroll through</p>"
                )
    row_number = gr.Number(value=0, label="Enter a number to get a sample")  # Input for row number
    
    # Buttons for navigation
    with gr.Row():
        prev_button = gr.Button("Previous")
        next_button = gr.Button("Next")
    
    
    
    # Create a row of Textboxes, one for each column in the CSV
    textboxes = {col: gr.Textbox(label=col) for col in df.columns}
    
    # Function to update the data displayed in the Textboxes
    def update_data(row_number):
        data = get_row_data(int(row_number))
        return [data.get(col, "") for col in df.columns]
    
    # Function to go to the next row
    def next(row_num):
        return min(row_num + 1, len(df) - 1)
    
    # Function to go to the previous row
    def previous(row_num):
        return max(row_num - 1, 0)
    
   
    
    textboxes_row = gr.Row(*textboxes.values())
    row_number.change(update_data, inputs=row_number, outputs=list(textboxes.values()))

    # Bind the next and previous functions to the buttons
    next_button.click(next, inputs=row_number, outputs=row_number)
    prev_button.click(previous, inputs=row_number, outputs=row_number)

# Launch the interface
demo.launch()
