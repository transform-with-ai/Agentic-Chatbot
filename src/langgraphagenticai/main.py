import streamlit as st
from src.langgraphagenticai.UI.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.Graph.graph_builder import GraphBuilder
from src.langgraphagenticai.UI.streamlitui.display_results import DisplayResultStreamlit


def load_langgrapgh_agentic_app():
    """
    Loads and runs Langgraph AgenticAI Application with Streamlit UI.
    This function initializes the UI, handles User input, confirgures the LLM Model, 
    sets-up the grapgh based on the, selected use case,and displayes the response 
    in the output while implementing execption handling for robustness.

    """

    #  Load UI
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            ## Configure the LLM`s
            obj_llm_config=GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM Model could notbe initialized ")
                return
            
            # Initialize and set up the graph on use case
            usecase=user_input.get("selected_usecase")

            if not usecase:
                st.error("Enter: No use case selected.")

            # Graph builder
            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error Graph set up failed{e}")
                return
       
        except Exception as e:
            st.error(f"Error Graph set up failed{e}")
            return

   
