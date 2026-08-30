import streamlit as st
from graph.graph import graph_main
def main():
    """Steamlit UI"""
    graph ,config=graph_main()
    user_input = st.chat_input("Enter job details or a job posting link:")

    # Initialize chat histroy in session state

    if "messages" not in st.session_state:
        st.session_state.messages =[]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("is_json"):
                st.json(msg["content"])
            else:
                st.write(msg["content"])
        
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("User"):
            with st.spinner("Processing..."):
                try:
                    final_state = None
                    events_log =[]

                    for event in graph.stream(
                        {"user_input": user_input},
                        config=config,
                        stream_mode="updates",
                    ):
                        events_log.append(event)   # show each node's output as it streams in
                        final_state = event

                    st.success("Done")
                    if final_state:
                        st.json(final_state)
                    st.session_state.messages.append({
                            "role": "assistant",
                            "content": {"events": events_log, "final_state": final_state},
                            "is_json": True
                        })
                except Exception as e:
                    st.error(f"Something went wrong: {e}")



if __name__ == "__main__":
    main()
