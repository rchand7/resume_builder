import streamlit as st
from fpdf import FPDF
from PIL import Image
import os

# Function to create a PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Resume', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_image(self, path, w=50):  # Set default width smaller
        self.image(path, x=150, y=25, w=w)  # Adjusted position

# Function to create a resume PDF
def create_pdf(name, dob, address, linkedin, experience, summary, skills, job_role, photo_path=None, additional_skills=None, theme=None):
    pdf = PDF()
    pdf.add_page()

    # Add photo if provided
    if photo_path:
        pdf.add_image(photo_path, w=50)  # Adjusted width for the photo

    # Personal Information
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, f"Name: {name}", ln=True)
    pdf.cell(0, 10, f"DOB: {dob}", ln=True)
    pdf.cell(0, 10, f"Address: {address}", ln=True)
    pdf.cell(0, 10, f"LinkedIn: {linkedin}", ln=True)
    pdf.ln(10)

    # Experience
    pdf.chapter_title("Experience")
    for exp in experience:
        pdf.chapter_body(f"- {exp}")

    # Summary
    pdf.chapter_title("Summary")
    pdf.chapter_body(summary)

    # Skills
    pdf.chapter_title("Skills")
    pdf.chapter_body(', '.join(skills))

    # Additional Skills
    if additional_skills:
        pdf.chapter_title("Additional Skills")
        pdf.chapter_body(', '.join(additional_skills))

    # Desired Job Role
    pdf.chapter_title("Desired Job Role")
    pdf.chapter_body(job_role)

    # Apply theme color (if needed)
    if theme == "Dark":
        pdf.set_fill_color(50, 50, 50)  # Dark background color
    else:
        pdf.set_fill_color(255, 255, 255)  # Light background color

    # Save the PDF to a file
    pdf.output("resume.pdf")

# Define the Streamlit app
def main():
    st.title("Stylish Resume Builder")
    st.write("Fill in the details below to create your stylish resume.")

    name = st.text_input("Name")
    dob = st.date_input("Date of Birth")
    address = st.text_input("Address")
    linkedin = st.text_input("LinkedIn Profile URL")
    
    experience = st.text_area("Experience (separate each experience with a newline)").splitlines()
    summary = st.text_area("Summary")
    skills = st.text_input("Skills (comma-separated)").split(',')
    
    # Option to add additional skills
    additional_skills = st.text_input("Additional Skills (comma-separated)").split(',')

    job_role = st.text_input("Desired Job Role")
    
    photo = st.file_uploader("Upload Your Photo", type=['jpg', 'jpeg', 'png'])
    photo_path = None
    if photo is not None:
        photo_path = f"temp_{photo.name}"
        with open(photo_path, "wb") as f:
            f.write(photo.getbuffer())

    # Theme selection
    theme = st.selectbox("Select a Theme", ["Light", "Dark"])

    if st.button("Generate Resume", key="generate_resume"):
        if name and experience and summary and skills and job_role:
            create_pdf(name, dob.strftime("%Y-%m-%d"), address, linkedin, experience, summary, skills, job_role, photo_path, additional_skills, theme)
            st.success("Resume generated successfully! Download it below:")
            with open("resume.pdf", "rb") as f:
                st.download_button("Download Resume", f, file_name="resume.pdf", key="download_resume")
        else:
            st.error("Please fill in all fields.")

    # Clean up the uploaded photo
    if photo_path and os.path.exists(photo_path):
        os.remove(photo_path)

if __name__ == "__main__":
    main()






















