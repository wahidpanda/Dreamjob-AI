import streamlit as st
import base64
import os
import io
import pdf2image
from docx import Document
from io import BytesIO
import google.generativeai as genai
from dotenv import load_dotenv
import requests


# Load environment variables
load_dotenv()

# Configure generativeai with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define a class for Resume
class Resume:
    def __init__(self, name, email, mobile, profile_pic, education, skills, experience, projects, 
                achievements, activities):
        # Initialize the Resume object with user information
        self.name = name
        self.email = email
        self.mobile = mobile
        self.profile_pic = profile_pic
        self.education = education
        self.skills = skills
        self.experience = experience
        self.projects = projects
        self.achievements = achievements
        self.activities = activities

    def generate_markdown(self):
        # Generate Markdown content for the resume
        markdown_text = f"<div style='position:relative;'>"
        
        if self.profile_pic is not None:
            # Check if profile picture is uploaded
            markdown_text += f"<img src='data:image/jpeg;base64,{base64.b64encode(self.profile_pic.read()).decode('utf-8')}' style='position:absolute; top:0; right:0; width:100px;'>"
        
        markdown_text += f"<h1 style=\"text-align:center;\">{self.name}</h1>\n<p style=\"text-align:center;\">Email: {self.email} | Mobile: {self.mobile} </p>\n\n"
        markdown_text += "</div>"
        markdown_text += "### Education\n\n---\n\n"
        # Add education details to the Markdown content
        for edu in self.education:
            markdown_text += f"- {edu['level']}: {edu['institution']} | {edu['field']} | Score: {edu['score']} | {edu['duration']}." + "\n\n"

        markdown_text += "### Skills\n\n---\n\n"
        # Add skills to the Markdown content
        markdown_text += f"{self.skills} \n\n"

        markdown_text += "### Experience\n\n---\n\n"
        # Add work experience details to the Markdown content
        for exp in self.experience:
            markdown_text += f"- **{exp['job_role']}({exp['company_name']})**: {exp['description']}\n"

        markdown_text += "\n### Projects\n\n---\n\n"
        # Add project details to the Markdown content
        for proj in self.projects:
            markdown_text += f"- **{proj['name']}**: {proj['description']}\n"

        markdown_text += "\n### Achievements\n\n---\n\n"
        # Add achievement details to the Markdown content
        for ach in self.achievements:
            markdown_text += f"- {ach}\n"

        markdown_text += "\n### Other Activities\n\n---\n\n"
        # Add other activities to the Markdown content
        markdown_text += self.activities + '\n'

        return markdown_text


# Function to get Gemini response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Define a simple user authentication function
def authenticate(username, password):
    # Replace this with your own authentication logic
    # For example, you might query a database to validate credentials
    return username == "@wahid" and password == "12#"

# Define a function to show the login form
def show_login_form():
    st.title("🚀 Dreamjob.AI")
   
    st.header("Dreamjob.AI - Your Ultimate Career Companion")
    st.image("vv.jpg", use_column_width=400)

    # Key Features
    st.subheader("Key Features:")
    st.image("gg.gif")

    # Pricing List
    st.subheader("Pricing:")
    st.image("pp.gif", use_column_width=800)
    
    
    st.sidebar.subheader("User Login")
    st.sidebar.markdown("To use this app, Usernamer: @wahid  Password: 12#")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")
    new_user_button = st.sidebar.button("Create New Account")
    st.sidebar.markdown("To use this app, you need to provide your Google API Key.")
    
    google_api_key = st.sidebar.text_input("Enter your Google API Key", type="password")

    st.sidebar.markdown("[Click here](https://makersuite.google.com/app/apikey) to generate your Google API Key.")
    if google_api_key:
        user_input(google_api_key)

    if login_button:
        if authenticate(username, password):
            # Set a session state variable to indicate successful login
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.sidebar.error("Invalid username or password")
    if new_user_button:
        pass
    

# Define a function to show the logout button
def show_logout_button():
    st.sidebar.button("Logout", on_click=logout)

# Define a function to logout
def logout():
    st.session_state.logged_in = False

# Define the main app function
def main():
    st.set_page_config(
        page_title="Dreamjob.AI",
        page_icon=":rocket:",
        layout="wide"
    )
    

    # Check if the user is logged in
    if not hasattr(st.session_state, "logged_in") or not st.session_state.logged_in:
        show_login_form()
    else:
        show_logout_button()
        st.write(f"Logged in as {st.session_state.username}")

        # Sidebar with navigation
        feature_selected = st.sidebar.radio("Select Feature", ["Resume Evaluation", "Analyze Your CV", "Job Preparation", "Interview Simulator", "Resume Builder", "Cover Letter Generator","Recruiter Email","Career Suggestion"])

        if feature_selected == "Resume Evaluation":
            home_page()
        elif feature_selected == "Analyze Your CV":
            analyze_cv_page()
        elif feature_selected == "Job Preparation":
            job_preparation_page()
        elif feature_selected == "Interview Simulator":
            interview_simulator_page()
        elif feature_selected == "Resume Builder":
            resume_formatter_page()
        elif feature_selected == "Cover Letter Generator":
            cover_letter_generator_page()
        elif feature_selected == "Recruiter Email":
            email_to_recruiter_page()
        elif feature_selected == "Career Suggestion":
            career_suggestions_page()
# Home Page
def home_page():
    st.title("Resume Evaluation ⚖️")

    input_text = st.text_area("Job Description: ", key="input")
    uploaded_file = st.file_uploader("Upload your CV (PDF)...", type=["pdf"], key="file_uploader")

    if uploaded_file is not None:
        st.success("PDF Uploaded Successfully")

    submit1 = st.button("Tell Me About the Resume")
    submit3 = st.button("Percentage Match")

    input_prompt1 = """
     You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
      Please share your professional evaluation on whether the candidate's profile aligns with the role.
     Highlight the major things :
     You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
      Please share your professional evaluation on whether the candidate's profile aligns with the role.
     Highlight and evalaute ar below scale for applicant CV
     1. Formatting and Presentation (Weight: 10%)
     2. Key Skills and Achievements (Weight: 30%)
     3.Work Experience Alignment (Weight: 40%)
     4.Bonus: Keyword Match (Weight: 20%)
     and told how is he/she good for that company.
    """

    input_prompt3 = """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
    your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
    the job description. First, the output should come as a percentage, then keywords missing, and last final thoughts. Second show what are not match as bullet points.
    """

    # Main functionality logic
    if submit1:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.warning("Please upload the resume before generating the response.")

    elif submit3:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.warning("Please upload the resume before generating the response.")

# Analyze Your CV Page
def analyze_cv_page():
    st.title("Analyze Your CV 🕵️‍♂️ ")
    uploaded_cv_file = st.file_uploader("Upload your CV (PDF)...", type=["pdf"], key="cv_file_uploader")
    analyze_cv_button = st.button("Analyze my CV")
    
    prompt1 = """
        You are an expert CV reviewer. Review cv and provide with
        1. strength, 
        2. weakness. 
        Mention user Applicant where to improve him/her self according to cv as bullet point wise.
    """

    if analyze_cv_button:
        if uploaded_cv_file is not None:
            cv_content = input_pdf_setup(uploaded_cv_file)
            # Pass the relevant input prompt and pdf_content for CV analysis
            response = get_gemini_response("", cv_content, prompt1)
            st.subheader("Analyzed Result:")
            st.write(response)
        else:
            st.warning("Please upload the CV before generating the response for analysis.")

# Job Preparation Page
def gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt])
    return response.text

def job_preparation_page():
    st.title("Job Preparation Feature ✍")

    # Add the logic for job preparation here
    input_text = st.text_area("Job Description: ", key="input")
    submit1 = st.button("Generate Interview Questions and Answers")

    input_prompt_job_preparation = """
        You are a skilled and experienced professional in your field, currently preparing for a job interview.
        Your goal is to generate relevant interview questions and answers based on your job description.
        Please provide details about your professional background, skills, and experiences.
        Mention key areas that align with the job description to receive customized interview questions.
    """

    # Main functionality logic
    if submit1:
        if input_text is not None:
            response = gemini_response(input_prompt_job_preparation + input_text)
            st.subheader("Generated Interview Questions and Answers:")
            st.write(response)
        else:
            st.warning("Please enter the job description before generating interview questions and answers.")

# Function to set up PDF content
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
# Interview Simulator Page
def interview_simulator_page():
    st.title("Interview Simulator 🗣️")
    input_text_simulator = st.text_area("Job Description: ", key="input_simulator")
    simulate_button = st.button("Simulate Interview")

    input_prompt_simulator = """
        You are a seasoned interviewer conducting an interview for the position of [Job Title].
        Generate 15 interview questions and provide expert-level answers to help job seekers prepare for interviews.
    """

    if simulate_button:
        if input_text_simulator is not None:
            response = gemini_response(input_prompt_simulator + input_text_simulator)
            st.subheader("Simulated Interview Questions and Answers:")
            st.write(response)
        else:
            st.warning("Please enter the job description before simulating the interview.")

# Resume Formatter Page
def resume_formatter_page():
    st.title("Resume Builder 📄")
    user_resume = get_user_input()

    # Generate Markdown content from user input
    markdown_text = user_resume.generate_markdown()

    # Convert Markdown to PDF
    pdf_file = convert_markdown_to_pdf(markdown_text)

    # Offer the PDF as a download link
    download_link = create_download_link(pdf_file, filename="Resume.pdf", label="Download PDF")
    st.markdown(download_link, unsafe_allow_html=True)
# Function to create a download link for files
def create_download_link(file_content, filename="file", label="Download"):
    b64 = base64.b64encode(file_content).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{label}</a>'
    return href


# Function to gather user input for creating the resume
def get_user_input():
    st.subheader("Personal Information")
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    mobile = st.text_input("Enter your mobile number:")

    # Upload profile picture
    st.subheader("Profile Picture")
    profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])

    st.subheader("Education")
    education = []
    add_education = st.checkbox("Add Education")
    while add_education:
        level = st.text_input("Enter education level (e.g., Graduation(UG/PG), High School):")
        institution = st.text_input("Enter the name of the institution:")
        field = st.text_input("Enter the field of study:")
        duration = st.text_input("Enter passing year:")
        score = st.text_input("Enter your score (e.g., GPA/Percentage):")
        education.append({"level": level, "institution": institution, "field": field, "duration": duration, "score": score})
        add_education = st.checkbox("Add Another Education")

    st.subheader("Skills")
    skills = st.text_area("Enter your skills (comma-separated):")

    st.subheader("Experience")
    experience = []
    add_experience = st.checkbox("Add Experience")
    while add_experience:
        job_role = st.text_input("Enter your job role:")
        company_name = st.text_input("Enter the company name:")
        description = st.text_area("Enter job description:")
        experience.append({"job_role": job_role, "company_name": company_name, "description": description})
        add_experience = st.checkbox("Add Another Experience")

    st.subheader("Projects")
    projects = []
    add_project = st.checkbox("Add Project")
    while add_project:
        name = st.text_input("Enter project name:")
        description = st.text_area("Enter project description:")
        projects.append({"name": name, "description": description})
        add_project = st.checkbox("Add Another Project")

    st.subheader("Achievements")
    achievements = []
    add_achievement = st.checkbox("Add Achievement")
    while add_achievement:
        achievement = st.text_input("Enter an achievement detail:")
        achievements.append(achievement)
        add_achievement = st.checkbox("Add Another Achievement")

    st.subheader("Other Activities")
    activities = st.text_area("Enter other activities or hobbies:")
    return Resume(name, email, mobile, profile_pic, education, skills, experience, projects, achievements, activities)


#     return Resume(name, email, mobile, profile_pic, education, skills, experience, projects, achievements, activities)
# # Function to convert Markdown to PDF using an external API
def convert_markdown_to_pdf(markdown_content, engine="weasyprint"):
    # Define CSS styles for the PDF
    cssfile = """
                body{
                    padding: 0px;
                    margin:0px;
                }
                h1 {
                color: MidnightBlue;
                margin:0px;
                padding:0px;
                    
                }
                h3{
                    color: MidnightBlue;
                    padding-bottom:0px; 
                    margin-bottom:0px; 
                }
                li{
                    margin-top:5px;
                }
                
                """
    # API endpoint for converting Markdown to PDF
    url = "https://md-to-pdf.fly.dev"

    # Data to be sent in the POST request
    data = {
        'markdown': markdown_content,
        'css': cssfile,
        'engine': engine
    }

    # Send a POST request to the API
    response = requests.post(url, data=data)

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Return the PDF content
        return response.content
    else:
        print(f"Error {response.status_code}: {response.text}")






# Cover Letter Generator Page
def cover_letter_generator_page():
    st.title("Cover Letter Builder 📝")

    # Input fields for job description and resume upload
    uploaded_file = st.file_uploader("Upload your CV (PDF)...", type=["pdf"], key="file_uploader")

    if uploaded_file is not None:
        st.success("PDF Uploaded Successfully")

    input_text = st.text_area("Job Description: ", key="input")

    # Button to generate cover letter
    submit_cl = st.button("Build Cover Letter")

    # Prompt for cover letter generation
    input_prompt_cl = """
    You are a skilled Cover Letter Writer. Your task is to write a powerful cover letter based on the provided CV and job description.
    Consider tailoring the cover letter to the specific company and highlighting the 
    1. candidate's relevant skills and experiences mention from CV.
    2. how candidate helpful for this position.
    3. how passionate candidate is for the job.
    Also, lastly mention candidate name and address, phone number, email address collect from CV.
    """


    # Main functionality logic
    if submit_cl:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt_cl, pdf_content, input_text)
            st.subheader("Generated Cover Letter:")
            st.write(response)

            # Offer the cover letter as a download button
            download_button = st.download_button(label="Download Cover Letter", data=response, file_name="Cover_Letter.doc", mime="text/plain")
        else:
            st.warning("Please upload the resume before generating the cover letter.")

# Email to Recruiter Page
def email_to_recruiter_page():
    st.title("Generate Email to send recruiter 📧")

    # Input fields for job description and resume upload
    uploaded_file = st.file_uploader("Upload your CV (PDF)...", type=["pdf"], key="file_uploader")

    if uploaded_file is not None:
        st.success("PDF Uploaded Successfully")

    input_text = st.text_area("Job Description: ", key="input")

    # Button to generate email
    submit_email = st.button("Build Email to Recruiter")

    # Prompt for cover letter generation
    input_prompt_email = """
    You are a skilled Email Writer to recuiter. Your task is to write a short and powerful email  with strong subjectline to recruiter based on the provided CV and job description.
    Consider tailoring the email to the specific company and highlighting the 
    1. between 50 to 125 words
    2. candidate's relevant skills and experiences mention from CV.
    3. how candidate helpful for this position.
    4. how passionate candidate is for the job.
    Also, lastly mention candidate name and address, phone number, email address collect from CV. Note that email will be short and powerfull.
    """


    # Main functionality logic
    if submit_email:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt_email, pdf_content, input_text)
            st.subheader("Generated Email:")
            st.write(response)

            # Offer the cover letter as a download button
            download_button = st.download_button(label="Download Email", data=response, file_name="Email.doc", mime="text/plain")
        else:
            st.warning("Please upload the resume before generating the Email.")

# Career Suggestions Page
def career_suggestions_page():
    st.title("Career Suggestions 💡")

    uploaded_cv_file = st.file_uploader("Upload your CV (PDF)...", type=["pdf"], key="cv_file_uploader")
    analyze_cv_button = st.button("Get Career Suggestions")

    prompt_career_suggestions = """
        You are a speaclist career advisor and planner providing personalized recommendations based on the user's CV.
        Analyze the uploaded CV and suggest potential career paths, future scope, skill development areas, and job opportunities as bullet point highlithing major points.
    """

    if analyze_cv_button:
        if uploaded_cv_file is not None:
            cv_content = input_pdf_setup(uploaded_cv_file)
            response = get_gemini_response("", cv_content, prompt_career_suggestions)
            st.subheader("Career Suggestions:")
            st.write(response)
        else:
            st.warning("Please upload the CV before generating career suggestions.")




if __name__ == "__main__":
    main()
