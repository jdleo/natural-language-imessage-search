import gradio as gr
from typing import Dict, List, Tuple, Optional
import pandas as pd
from utils.ai import get_sql_query
from utils.db import execute_query
from prompts import MAIN_PROMPT


def search_messages(query: str) -> Tuple[pd.DataFrame, str, str, str]:
    """
    Search iMessage history using natural language query
    Returns: (messages_df, result_stats, status, sql_query)
    """
    # Get SQL query from AI
    sql_query = get_sql_query(query, MAIN_PROMPT)
    if not sql_query:
        return pd.DataFrame(), "", "Failed to generate SQL query", ""

    # Execute the query
    result = execute_query(sql_query)
    if result is None:
        return pd.DataFrame(), "", "Failed to execute SQL query", sql_query

    headers, rows = result
    # Create pandas DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Generate stats
    stats = f"Found {len(rows)} messages"

    return df, stats, "Query executed successfully", sql_query


def export_results(data: pd.DataFrame, format: str) -> str:
    """Export results in the specified format"""
    if data.empty:
        return "No data to export"

    # TODO: Implement export functionality
    return f"Export to {format} not yet implemented"


def create_ui() -> gr.Blocks:
    with gr.Blocks(title="Natural Language iMessage Search") as app:
        gr.Markdown("# iMessage History Search")

        with gr.Row():
            query_input = gr.Textbox(
                label="Search Query",
                placeholder="Enter your search query in natural language...",
                lines=2,
            )

        with gr.Row():
            search_button = gr.Button("Search", variant="primary")
            export_button = gr.Button("Export Results")

        with gr.Row():
            results_stats = gr.Markdown("", label="Results Statistics")
            status_display = gr.Markdown("", label="Status")

        sql_display = gr.Code(
            label="Generated SQL Query",
            language="sql",
            interactive=False,
        )

        # Dynamic dataframe without predefined headers
        results_table = gr.Dataframe(
            label="Search Results",
            wrap=True,
            interactive=False,
        )

        export_format = gr.Dropdown(
            choices=["CSV", "JSON", "TXT"], label="Export Format", value="CSV"
        )

        # Wire up the components
        search_button.click(
            fn=search_messages,
            inputs=[query_input],
            outputs=[results_table, results_stats, status_display, sql_display],
        )

        export_button.click(
            fn=export_results,
            inputs=[results_table, export_format],
            outputs=[status_display],
        )

    return app
