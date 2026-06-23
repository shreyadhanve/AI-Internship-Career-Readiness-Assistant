import streamlit as st
from google import genai
import streamlit as st

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    color: #1E3A5F;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="AI Internship & Career Readiness Assistant",
    layout="wide"
)
# Gemini API Key
from config import API_KEY

client = genai.Client(api_key=API_KEY)

st.title("AI Internship & Career Readiness Assistant")

st.markdown("""
An AI-powered platform that helps students evaluate internship opportunities,
identify skill gaps, and generate personalized learning roadmaps.
""")

st.divider()
with st.sidebar:

    st.header("About")

    st.write("""
    This platform assists students in:

    • Evaluating internship opportunities

    • Identifying missing skills

    • Generating learning roadmaps

    • Accessing learning resources

    • Improving career readiness
    """)

st.caption(
    "Paste an internship description from LinkedIn, Internshala, company websites, or other job portals."
)

st.subheader("Internship Information")
internship_details = st.text_area(
    "Paste Internship Description",
    height=250,
    placeholder="""
Company Name:
Role:
Requirements:
Stipend:
Selection Process:
"""
)
st.subheader("Student Profile")
student_skills = st.text_input(
    "Enter Your Current Skills",
    placeholder="Python, SQL, Excel"
)
analyze = st.button(
    "Analyze Internship",
    use_container_width=True
)
if analyze:
    st.write("Internship Details:", internship_details)
    st.write("Student Skills:", student_skills)
    
    st.subheader("Analysis Results")

    prompt = f"""
You are an AI Internship & Career Readiness Assistant.

Analyze the internship and student profile below.

Internship:
{internship_details}

Student Skills:
{student_skills}

Generate the following:

1. Internship Assessment Score (0-100)
Scoring Criteria (Internal Use Only):

Company Information: 20 points
Role Clarity: 20 points
Required Skills: 20 points
Selection Process: 20 points
Compensation Details: 20 points

Calculate a total score out of 100.

Classification Rules:

80-100 → Legitimate

50-79 → Needs Verification

0-49 → Potentially Suspicious
Use the scoring criteria internally to calculate the Internship Assessment Score.

Do not display the category-wise scores.

Display only:
- Final Internship Assessment Score
- Classification
2. Internship Analysis

Analyze the internship and explain:

- Why the internship received its assessment score.
- Key strengths of the opportunity.
- Any concerns or factors that require attention.
- Keep the analysis concise (3-5 sentences).

3. Skill Gap Analysis

Analyze the student's skills against the internship requirements.

Include:
- Matching skills
- Missing skills (if any)
- Skill Match Percentage
- Student's overall readiness for the role

Keep the analysis concise and professional.

4. Learning Roadmap

Generate a personalized 3-week learning roadmap.

Week 1:
Week 2:
Week 3:

Focus only on the skills that need improvement.
Make the roadmap practical and beginner-friendly.

Focus on learning goals rather than listing database topics.

5. Learning Resources

Recommend learning resources for each missing skill.

For each skill provide:
- One free YouTube resource
- One free online course
- One practice platform

If no skills are missing, recommend interview preparation and project-building resources instead.

6. Final Recommendation

Provide one of the following recommendations:

- Apply Immediately
- Apply After Skill Improvement
- Not Recommended Currently

Briefly justify the recommendation in 2-3 sentences.

For each missing skill provide:
- One free YouTube resource
- One free online course
- One practice platform

IMPORTANT RULES:
- The internship details and student skills are already provided.
Use only the information present in the internship description.
-Do not assume facts that are not provided.
- Do NOT ask for additional information.
- Do NOT say "input required".
- Do NOT repeat the internship details.
- Do NOT repeat the student skills.
- Keep the response concise.
- Use bullet points only.
- Keep each section under 3 bullet points.
- Start directly with the Internship Assessment Score.

Output Format

## Internship Assessment Score

Score: XX/100

## Classification

Legitimate / Needs Verification / Potentially Suspicious

## Internship Analysis

(Analysis here)

## Skill Gap Analysis

Matching Skills:
- ...

Missing Skills:
- ...

Skill Match Percentage:
- ...

Readiness:
- ...

## Learning Roadmap

### Week 1

...

### Week 2

...

### Week 3

...

## Learning Resources

### Skill Name

YouTube Resource:
...

Online Course:
...

Practice Platform:
...

## Final Recommendation

Apply Immediately / Apply After Skill Improvement / Not Recommended Currently

(Explanation)
...
Formatting Rules:

-Do not use decorative symbols such as 🔹, ★, ➜, or emojis.
-Use clear section headings followed by the content.
Formatting Requirements:

- Use Markdown headings.
- Main sections must use ## headings.
- Subsections such as Week 1, Week 2, Week 3 must use ### headings.
- Leave a blank line between sections.
- Do not place headings and content on the same line.
- Present the output as a professional report.
- Make the output easy to read and visually organized.
- Keep the response concise and professional.
- Do not repeat the internship description.
- Do not repeat the student skills.
- Do not ask for additional information.
- Focus on actionable insights rather than simply listing information.

"""

    try:

        with st.spinner("Analyzing internship and generating recommendations..."):

         response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

        st.markdown(response.text)
        st.success("Analysis completed successfully.")
        

    except Exception as e:

      if "503" in str(e):
        st.warning(
             "⚠️ AI server is busy right now. Please wait a few seconds and click Analyze Internship again."
        )
      else:
        st.error(e)
        st.divider()

