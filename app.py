import streamlit as st
import json
import os
from core import analyze_story, remap_context, generate_story, check_integrity

st.set_page_config(page_title="NTE", layout="wide")

st.title("Narrative Transposition Engine")
st.caption("Reimagining stories using Gemini 1.5 Flash")

with st.sidebar:
    st.header("Configuration")
    
    source_path = "data/hamlet_summary.txt"
    default_text = open(source_path).read() if os.path.exists(source_path) else ""
        
    source_story = st.text_area("Source Story", value=default_text, height=300)
    target_world = st.text_input("Target World", value="Modern Corporate Silicon Valley, 2040")
    world_rules = st.text_area("World Rules (Optional)", placeholder="e.g. Magic is binary-based")
    
    run_engine = st.button("Transform", type="primary", use_container_width=True)

if run_engine or "results" in st.session_state:
    if "results" not in st.session_state:
        try:
            with st.status("Engine running...", expanded=True) as status:
                st.write("Analyzing source...")
                analysis = analyze_story(source_story)
                
                st.write("Remapping context...")
                remapped = remap_context(analysis, target_world, world_rules)
                
                st.write("Generating prose...")
                story = generate_story(remapped)
                
                st.write("Verifying integrity...")
                report = check_integrity(analysis, story)
                
                status.update(label="Transformation complete", state="complete", expanded=False)
            
            st.session_state.results = {
                "analysis": analysis,
                "remapped": remapped,
                "story": story,
                "report": report
            }
        except Exception as e:
            st.error(f"Engine failure: {e}")
            st.stop()

    res = st.session_state.results
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Transformed Narrative")
        if res['report']['overall'] == "PASS":
            st.success("Integrity Check: PASSED")
        else:
            st.warning("Integrity Check: FAILED")
            
        st.text_area("Prose", res['story'], height=600, label_visibility="collapsed")
        st.download_button("Download Story", res['story'], file_name="story.txt", use_container_width=True)

    with col2:
        st.subheader("Pipeline Artifacts")
        with st.expander("1. Source Analysis"):
            st.json(res['analysis'])
        with st.expander("2. Remapped World"):
            st.json(res['remapped'])
        with st.expander("3. Integrity Report", expanded=True):
            st.json(res['report'])

st.divider()
st.caption("NTE v1.0")
