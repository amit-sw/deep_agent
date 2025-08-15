import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.set_page_config(
        page_title="Deep Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Deep Agent")
    st.write("Welcome to the Deep Agent application!")

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Data Explorer", "About"])

    if page == "Home":
        st.header("Home")
        st.write("This is the home page of the Deep Agent application.")
        
        if st.button("Click me!"):
            st.balloons()
            
    elif page == "Data Explorer":
        st.header("Data Explorer")
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['A', 'B', 'C']
        )
        st.line_chart(chart_data)
        
    elif page == "About":
        st.header("About")
        st.write("""
        ## Deep Agent
        
        A Streamlit-based application for exploring AI agents.
        
        **Version:** 0.1.0
        """)

if __name__ == "__main__":
    main()
