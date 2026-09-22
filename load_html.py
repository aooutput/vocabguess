import streamlit as st
import streamlit.components.v1 as components

# Read HTML file from your GitHub repository
with open("test_colordice.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Render the HTML in the app
components.html(html_content,height=3000)#, height=600, scrolling=True)
