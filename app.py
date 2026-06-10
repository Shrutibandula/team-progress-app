import streamlit as st
import pandas as pd

from tracker import (
    load_data,
    save_data,
    get_insights,
    MEMBERS,
    COURSES
)


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Team Progress Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Team Learning Progress Dashboard")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

data = load_data()

# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

rows = []

for member in MEMBERS:

    completed = sum(data[member].values())

    row = {
        "Name": member,
        "Progress %": round(
            completed / len(COURSES) * 100
        )
    }

    for course in COURSES:
        row[course] = data[member][course]

    rows.append(row)

df = pd.DataFrame(rows)

# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

total_members = len(MEMBERS)

fully_completed = sum(
    1 for m in data.values()
    if all(m.values())
)

avg_completion = round(
    sum(
        sum(member.values())
        for member in data.values()
    )
    /
    (len(MEMBERS) * len(COURSES))
    * 100
)

not_started = sum(
    1 for m in data.values()
    if not any(m.values())
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Team Members", total_members)

with col2:
    st.metric("Fully Complete", fully_completed)

with col3:
    st.metric("Average Completion", f"{avg_completion}%")

with col4:
    st.metric("Not Started", not_started)

st.divider()

# --------------------------------------------------
# EDITABLE TABLE
# --------------------------------------------------

st.subheader("Training Progress")

edited_df = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    disabled=["Name", "Progress %"]
)

# --------------------------------------------------
# SAVE CHANGES
# --------------------------------------------------

for _, row in edited_df.iterrows():

    member = row["Name"]

    for course in COURSES:
        data[member][course] = bool(row[course])

save_data(data)

st.success("Changes are automatically saved.")

st.divider()

# --------------------------------------------------
# AI INSIGHTS BUTTON
# --------------------------------------------------

st.subheader("🤖 AI Insights")

if st.button("Generate Insights"):
    with st.spinner("Claude is thinking..."):
        result = get_insights(data)
        st.write(result)
