import streamlit as st
from graph.graph import graph_main
def main():
    """Steamlit UI"""
    graph ,config=graph_main()
    user_input = st.chat_input("Enter job details or a job posting link:")

    if user_input:
        with st.spinner("Processing..."):
            try:
                final_state = None
                for event in graph.stream(
                    {"user_input": user_input},
                    config=config,
                    stream_mode="updates",
                ):
                    st.write(event)   # show each node's output as it streams in
                    final_state = event

                st.success("Done")
                if final_state:
                    st.json(final_state)

            except Exception as e:
                st.error(f"Something went wrong: {e}")



if __name__ == "__main__":
    main()
