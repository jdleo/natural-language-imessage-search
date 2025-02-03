import gradio as gr
import json
import pandas as pd


def json_to_table(json_str):
    try:
        # Parse JSON string
        data = json.loads(json_str)

        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            return "Input must be a JSON object or array"

        return df
    except json.JSONDecodeError:
        return "Invalid JSON format"
    except Exception as e:
        return f"Error: {str(e)}"


# Create Gradio interface
demo = gr.Interface(
    fn=json_to_table,
    inputs=gr.Textbox(label="Enter JSON", placeholder='{"name": "John", "age": 30}'),
    outputs=gr.Dataframe(),
    title="JSON to Table Converter",
    description="Enter valid JSON to see it displayed as a table",
)

if __name__ == "__main__":
    demo.launch()
