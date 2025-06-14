# import streamlit as st
# import pandas as pd
# import base64,random
# import time,datetime
# import spacy
# #libraries to parse the resume pdf files
# from pyresparser import ResumeParser
# from pdfminer3.layout import LAParams, LTTextBox
# from pdfminer3.pdfpage import PDFPage
# from pdfminer3.pdfinterp import PDFResourceManager
# from pdfminer3.pdfinterp import PDFPageInterpreter
# from pdfminer3.converter import TextConverter
# import io,random
# from streamlit_tags import st_tags
# from PIL import Image
# import pymysql
# from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
# import pafy #for uploading youtube videos
# import plotly.express as px #to create visualisations at the admin session
# import nltk
# nltk.download('stopwords')
# def fetch_yt_video(link):
#     video = pafy.new(link)
#     return video.title

# def get_table_download_link(df,filename,text):
#     """Generates a link allowing the data in a given panda dataframe to be downloaded
#     in:  dataframe
#     out: href string
#     """
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
#     # href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
#     href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
#     return href

# def pdf_reader(file):
#     resource_manager = PDFResourceManager()
#     fake_file_handle = io.StringIO()
#     converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
#     page_interpreter = PDFPageInterpreter(resource_manager, converter)
#     with open(file, 'rb') as fh:
#         for page in PDFPage.get_pages(fh,
#                                       caching=True,
#                                       check_extractable=True):
#             page_interpreter.process_page(page)
#             print(page)
#         text = fake_file_handle.getvalue()

#     # close open handles
#     converter.close()
#     fake_file_handle.close()
#     return text

# def show_pdf(file_path):
#     with open(file_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#     # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
#     pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#     st.markdown(pdf_display, unsafe_allow_html=True)

# def course_recommender(course_list):
#     st.subheader("**Courses & Certificates Recommendations 🎓**")
#     c = 0
#     rec_course = []
#     no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
#     random.shuffle(course_list)
#     for c_name, c_link in course_list:
#         c += 1
#         st.markdown(f"({c}) [{c_name}]({c_link})")
#         rec_course.append(c_name)
#         if c == no_of_reco:
#             break
#     return rec_course





# #CONNECT TO DATABASE

# connection = pymysql.connect(host='localhost',user='root',password='RadhaRani@9',db='cv')
# cursor = connection.cursor()

# def insert_data(name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses):
#     DB_table_name = 'user_data'
#     insert_sql = "insert into " + DB_table_name + """
#     values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#     rec_values = (name, email, str(res_score), timestamp,str(no_of_pages), reco_field, cand_level, skills,recommended_skills,courses)
#     cursor.execute(insert_sql, rec_values)
#     connection.commit()

# st.set_page_config(
#    page_title="AI Resume Analyzer",
#    page_icon='./Logo/logo2.png',
# )
# def run():
#     img = Image.open('./Logo/logo2.png')
#     # img = img.resize((250,250))
#     st.image(img)
#     st.title("AI Resume Analyser")
#     st.sidebar.markdown("# Choose User")
#     activities = ["User", "Admin"]
#     choice = st.sidebar.selectbox("Choose among the given options:", activities)
#     link = '[©Developed by Dr,Briit](https://www.linkedin.com/in/mrbriit/)'
#     st.sidebar.markdown(link, unsafe_allow_html=True)


#     # Create the DB
#     db_sql = """CREATE DATABASE IF NOT EXISTS CV;"""
#     cursor.execute(db_sql)

#     # Create table
#     DB_table_name = 'user_data'
#     table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
#                     (ID INT NOT NULL AUTO_INCREMENT,
#                      Name varchar(500) NOT NULL,
#                      Email_ID VARCHAR(500) NOT NULL,
#                      resume_score VARCHAR(8) NOT NULL,
#                      Timestamp VARCHAR(50) NOT NULL,
#                      Page_no VARCHAR(5) NOT NULL,
#                      Predicted_Field BLOB NOT NULL,
#                      User_level BLOB NOT NULL,
#                      Actual_skills BLOB NOT NULL,
#                      Recommended_skills BLOB NOT NULL,
#                      Recommended_courses BLOB NOT NULL,
#                      PRIMARY KEY (ID));
#                     """
#     cursor.execute(table_sql)
#     if choice == 'User':
#         st.markdown('''<h5 style='text-align: left; color: #021659;'> Upload your resume, and get smart recommendations</h5>''',
#                     unsafe_allow_html=True)
#         pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
#         if pdf_file is not None:
#             with st.spinner('Uploading your Resume...'):
#                 time.sleep(4)
#             save_image_path = './Uploaded_Resumes/'+pdf_file.name
#             with open(save_image_path, "wb") as f:
#                 f.write(pdf_file.getbuffer())
#             show_pdf(save_image_path)
#             resume_data = ResumeParser(save_image_path).get_extracted_data()
#             if resume_data:
#                 ## Get the whole resume data
#                 resume_text = pdf_reader(save_image_path)

#                 st.header("**Resume Analysis**")
#                 st.success("Hello "+ resume_data['name'])
#                 st.subheader("**Your Basic info**")
#                 try:
#                     st.text('Name: '+resume_data['name'])
#                     st.text('Email: ' + resume_data['email'])
#                     st.text('Contact: ' + resume_data['mobile_number'])
#                     st.text('Resume pages: '+str(resume_data['no_of_pages']))
#                 except:
#                     pass
#                 cand_level = ''
#                 if resume_data['no_of_pages'] == 1:
#                     cand_level = "Fresher"
#                     st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
#                 elif resume_data['no_of_pages'] == 2:
#                     cand_level = "Intermediate"
#                     st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
#                 elif resume_data['no_of_pages'] >=3:
#                     cand_level = "Experienced"
#                     st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)

#                 # st.subheader("**Skills Recommendation💡**")
#                 ## Skill shows
#                 keywords = st_tags(label='### Your Current Skills',
#                 text='See our skills recommendation below',
#                     value=resume_data['skills'],key = '1  ')

#                 ##  keywords
#                 ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
#                 web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
#                                'javascript', 'angular js', 'c#', 'flask']
#                 android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
#                 ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
#                 uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']

#                 recommended_skills = []
#                 reco_field = ''
#                 rec_course = ''
#                 ## Courses recommendation
#                 for i in resume_data['skills']:
#                     ## Data science recommendation
#                     if i.lower() in ds_keyword:
#                         print(i.lower())
#                         reco_field = 'Data Science'
#                         st.success("** Our analysis says you are looking for Data Science Jobs.**")
#                         recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
#                         recommended_keywords = st_tags(label='### Recommended skills for you.',
#                         text='Recommended skills generated from System',value=recommended_skills,key = '2')
#                         st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job</h4>''',unsafe_allow_html=True)
#                         rec_course = course_recommender(ds_course)
#                         break

#                     ## Web development recommendation
#                     elif i.lower() in web_keyword:
#                         print(i.lower())
#                         reco_field = 'Web Development'
#                         st.success("** Our analysis says you are looking for Web Development Jobs **")
#                         recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
#                         recommended_keywords = st_tags(label='### Recommended skills for you.',
#                         text='Recommended skills generated from System',value=recommended_skills,key = '3')
#                         st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
#                         rec_course = course_recommender(web_course)
#                         break

#                     ## Android App Development
#                     elif i.lower() in android_keyword:
#                         print(i.lower())
#                         reco_field = 'Android Development'
#                         st.success("** Our analysis says you are looking for Android App Development Jobs **")
#                         recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
#                         recommended_keywords = st_tags(label='### Recommended skills for you.',
#                         text='Recommended skills generated from System',value=recommended_skills,key = '4')
#                         st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
#                         rec_course = course_recommender(android_course)
#                         break

#                     ## IOS App Development
#                     elif i.lower() in ios_keyword:
#                         print(i.lower())
#                         reco_field = 'IOS Development'
#                         st.success("** Our analysis says you are looking for IOS App Development Jobs **")
#                         recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
#                         recommended_keywords = st_tags(label='### Recommended skills for you.',
#                         text='Recommended skills generated from System',value=recommended_skills,key = '5')
#                         st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
#                         rec_course = course_recommender(ios_course)
#                         break

#                     ## Ui-UX Recommendation
#                     elif i.lower() in uiux_keyword:
#                         print(i.lower())
#                         reco_field = 'UI-UX Development'
#                         st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
#                         recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
#                         recommended_keywords = st_tags(label='### Recommended skills for you.',
#                         text='Recommended skills generated from System',value=recommended_skills,key = '6')
#                         st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
#                         rec_course = course_recommender(uiux_course)
#                         break

                
#                 ## Insert into table
#                 ts = time.time()
#                 cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
#                 cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
#                 timestamp = str(cur_date+'_'+cur_time)

#                 ### Resume writing recommendation
#                 st.subheader("**Resume Tips & Ideas💡**")
#                 resume_score = 0
#                 if 'Objective' in resume_text:
#                     resume_score = resume_score+20
#                     st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',unsafe_allow_html=True)
#                 else:
#                     st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add your career objective, it will give your career intension to the Recruiters.</h4>''',unsafe_allow_html=True)

#                 if 'Declaration'  in resume_text:
#                     resume_score = resume_score + 20
#                     st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Delcaration/h4>''',unsafe_allow_html=True)
#                 else:
#                     st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Declaration. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h4>''',unsafe_allow_html=True)

#                 if 'Hobbies' or 'Interests'in resume_text:
#                     resume_score = resume_score + 20
#                     st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''',unsafe_allow_html=True)
#                 else:
#                     st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Hobbies. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)

#                 if 'Achievements' in resume_text:
#                     resume_score = resume_score + 20
#                     st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
#                 else:
#                     st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Achievements. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)

#                 if 'Projects' in resume_text:
#                     resume_score = resume_score + 20
#                     st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
#                 else:
#                     st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Projects. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)

#                 st.subheader("**Resume Score📝**")
#                 st.markdown(
#                     """
#                     <style>
#                         .stProgress > div > div > div > div {
#                             background-color: #d73b5c;
#                         }
#                     </style>""",
#                     unsafe_allow_html=True,
#                 )
#                 my_bar = st.progress(0)
#                 score = 0
#                 for percent_complete in range(resume_score):
#                     score +=1
#                     time.sleep(0.1)
#                     my_bar.progress(percent_complete + 1)
#                 st.success('** Your Resume Writing Score: ' + str(score)+'**')
#                 st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")
#                 st.balloons()

#                 insert_data(resume_data['name'], resume_data['email'], str(resume_score), timestamp,
#                               str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']),
#                               str(recommended_skills), str(rec_course))


#                 ## Resume writing video
#                 st.header("**Bonus Video for Resume Writing Tips💡**")
#                 resume_vid = random.choice(resume_videos)
#                 res_vid_title = fetch_yt_video(resume_vid)
#                 st.subheader("✅ **"+res_vid_title+"**")
#                 st.video(resume_vid)



#                 ## Interview Preparation Video
#                 st.header("**Bonus Video for Interview Tips💡**")
#                 interview_vid = random.choice(interview_videos)
#                 int_vid_title = fetch_yt_video(interview_vid)
#                 st.subheader("✅ **" + int_vid_title + "**")
#                 st.video(interview_vid)

#                 connection.commit()
#             else:
#                 st.error('Something went wrong..')
#     else:
#         ## Admin Side
#         st.success('Welcome to Admin Side')
#         # st.sidebar.subheader('**ID / Password Required!**')

#         ad_user = st.text_input("Username")
#         ad_password = st.text_input("Password", type='password')
#         if st.button('Login'):
#             if ad_user == 'briit' and ad_password == 'briit123':
#                 st.success("Welcome Dr Briit !")
#                 # Display Data
#                 cursor.execute('''SELECT*FROM user_data''')
#                 data = cursor.fetchall()
#                 st.header("**User's Data**")
#                 df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
#                                                  'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
#                                                  'Recommended Course'])
#                 st.dataframe(df)
#                 st.markdown(get_table_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)
#                 ## Admin Side Data
#                 query = 'select * from user_data;'
#                 plot_data = pd.read_sql(query, connection)

#                 ## Pie chart for predicted field recommendations
#                 labels = plot_data.Predicted_Field.unique()
#                 print(labels)
#                 values = plot_data.Predicted_Field.value_counts()
#                 print(values)
#                 st.subheader("**Pie-Chart for Predicted Field Recommendation**")
#                 fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills')
#                 st.plotly_chart(fig)

#                 ### Pie chart for User's👨‍💻 Experienced Level
#                 labels = plot_data.User_level.unique()
#                 values = plot_data.User_level.value_counts()
#                 st.subheader("**Pie-Chart for User's Experienced Level**")
#                 fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
#                 st.plotly_chart(fig)


#             else:
#                 st.error("Wrong ID & Password Provided")
# run()

import streamlit as st
import pandas as pd
import base64
import random
import time
import datetime
import spacy
from spacy.cli.download import download as spacy_download
import os
import io
from streamlit_tags import st_tags
from PIL import Image
import pymysql
import pafy
import plotly.express as px
import nltk
import re
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer.high_level import extract_text as pdfminer_extract_text
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
# Download required NLTK data
nltk.download('stopwords')

# Initialize spaCy model with error handling
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    try:
        st.warning("Downloading spaCy English model... (this may take a few minutes)")
        spacy_download('en_core_web_sm')
        nlp = spacy.load('en_core_web_sm')
    except Exception as e:
        st.error(f"Failed to load spaCy model: {str(e)}")
        st.stop()

# ================== CUSTOM RESUME PARSER ==================
class CustomResumeParser:
    def __init__(self, resume_path):
        self.resume_path = resume_path
        self.text = self._extract_text()
        self.entities = self._extract_entities()
    
    def _extract_text(self):
        """Extract text from PDF using pdfminer with fallback"""
        try:
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            
            with open(self.resume_path, 'rb') as fh:
                for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                    page_interpreter.process_page(page)
                text = fake_file_handle.getvalue()
            
            converter.close()
            fake_file_handle.close()
            return text
        except Exception:
            return pdfminer_extract_text(self.resume_path)
    
    def _extract_entities(self):
        """Extract entities using spaCy"""
        doc = nlp(self.text)
        return {
            'name': self._extract_name(doc),
            'email': self._extract_email(),
            'skills': self._extract_skills(doc),
            'education': self._extract_education(doc),
            'experience': self._extract_experience(doc)
        }
    
    def _extract_name(self, doc):
        """Extract name using spaCy's NER"""
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Your Name"
    
    def _extract_email(self):
        """Extract email using regex"""
        email = re.search(r'[\w\.-]+@[\w\.-]+', self.text)
        return email.group(0) if email else "your.email@example.com"
    
    def _extract_skills(self, doc):
        """Extract skills using keyword matching"""
        skills = []
        skill_keywords = ['python', 'java', 'sql', 'machine learning', 'data analysis',
                        'project management', 'communication', 'teamwork', 'problem solving',
                        'leadership', 'analytical skills', 'creativity', 'time management']
        
        for token in doc:
            if token.text.lower() in skill_keywords:
                skills.append(token.text)
        
        return list(set(skills)) if skills else ["List your skills"]
    
    def _extract_education(self, doc):
        """Extract education information"""
        education = []
        for ent in doc.ents:
            if ent.label_ == "ORG" and any(word in ent.text.lower() for word in ['university', 'college', 'institute']):
                education.append(ent.text)
        return education if education else ["Your Education"]
    
    def _extract_experience(self, doc):
        """Extract experience information"""
        experience = []
        for ent in doc.ents:
            if ent.label_ == "ORG" and any(word in ent.text.lower() for word in ['inc', 'ltd', 'corp', 'company']):
                experience.append(ent.text)
        return experience if experience else ["Your Experience"]
    
    def get_extracted_data(self):
        """Return formatted resume data"""
        return {
            'name': self.entities['name'],
            'email': self.entities['email'],
            'skills': self.entities['skills'],
            'education': self.entities['education'],
            'experience': self.entities['experience'],
            'no_of_pages': len(list(PDFPage.get_pages(open(self.resume_path, 'rb')))),
            'text': self.text
        }

# ================== RESUME SCORING ==================
def calculate_resume_score(resume_data, job_description=""):
    """Calculate a score for the resume based on completeness and job match"""
    score = 0
    
    # Basic completeness scoring
    if resume_data['name'] and resume_data['name'] != "Your Name":
        score += 10
    if resume_data['email'] and resume_data['email'] != "your.email@example.com":
        score += 10
    if len(resume_data['skills']) > 0 and resume_data['skills'][0] != "List your skills":
        score += 20
    if len(resume_data['education']) > 0 and resume_data['education'][0] != "Your Education":
        score += 20
    if len(resume_data['experience']) > 0 and resume_data['experience'][0] != "Your Experience":
        score += 20
    
    # Job description matching (if provided)
    if job_description:
        job_skills = extract_skills_from_jd(job_description)
        matched_skills = [skill for skill in resume_data['skills'] if skill.lower() in [js.lower() for js in job_skills]]
        score += min(20, len(matched_skills) * 2)  # Max 20 points for skill matching
    
    return min(100, score)  # Cap at 100

def extract_skills_from_jd(job_description):
    """Extract skills from job description text"""
    doc = nlp(job_description.lower())
    skills = []
    skill_keywords = ['python', 'java', 'sql', 'machine learning', 'data analysis',
                     'project management', 'communication', 'teamwork', 'problem solving',
                     'leadership', 'analytical skills', 'creativity', 'time management']
    
    for token in doc:
        if token.text in skill_keywords:
            skills.append(token.text)
    
    return list(set(skills))

# ================== ROLE-BASED RECOMMENDATIONS ==================
def get_recommended_skills(target_role, job_description=""):
    """Get recommended skills based on target role and optional job description"""
    role_skills = {
        'Data Scientist': ['Python', 'Machine Learning', 'SQL', 'Data Visualization', 
                          'Statistics', 'Deep Learning', 'Big Data', 'Natural Language Processing'],
        'Web Developer': ['JavaScript', 'HTML/CSS', 'React', 'Node.js', 'Python', 
                         'Django', 'REST APIs', 'Database Design'],
        'Software Engineer': ['Java', 'Python', 'C++', 'Data Structures', 'Algorithms',
                            'Software Design', 'Testing', 'Debugging'],
        'Product Manager': ['Product Strategy', 'Market Research', 'Agile Methodologies',
                          'User Stories', 'Roadmapping', 'Stakeholder Management'],
        'UX Designer': ['User Research', 'Wireframing', 'Prototyping', 'UI Design',
                       'Figma', 'Adobe XD', 'Usability Testing']
    }
    
    # Get base skills for the role
    recommended = role_skills.get(target_role, [])
    
    # Add skills from job description if provided
    if job_description:
        jd_skills = extract_skills_from_jd(job_description)
        recommended.extend([skill for skill in jd_skills if skill not in recommended])
    
    return list(set(recommended))  # Remove duplicates

# ================== MAIN APPLICATION ==================
def show_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to display PDF: {str(e)}")

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 🎓**")
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    
    for c_name, c_link in random.sample(course_list, min(no_of_reco, len(course_list))):
        st.markdown(f"- [{c_name}]({c_link})")
        rec_course.append(c_name)
    
    return rec_course

# Database functions
def create_connection():
    try:
        return pymysql.connect(
            host='localhost',
            user='root',
            password='RadhaRani@9',
            db='cv',
            autocommit=True
        )
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        return None

def init_database():
    try:
        conn = create_connection()
        if not conn:
            return False
            
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS CV;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    ID INT NOT NULL AUTO_INCREMENT,
                    Name varchar(500) NOT NULL,
                    Email_ID VARCHAR(500) NOT NULL,
                    resume_score VARCHAR(8) NOT NULL,
                    Timestamp VARCHAR(50) NOT NULL,
                    Page_no VARCHAR(5) NOT NULL,
                    Predicted_Field BLOB NOT NULL,
                    User_level BLOB NOT NULL,
                    Actual_skills BLOB NOT NULL,
                    Recommended_skills BLOB NOT NULL,
                    Recommended_courses BLOB NOT NULL,
                    PRIMARY KEY (ID)
                );
            """)
        return True
    except Exception as e:
        st.error(f"Database initialization failed: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
    try:
        conn = create_connection()
        if not conn:
            return False
            
        with conn.cursor() as cursor:
            insert_sql = """
                INSERT INTO user_data 
                VALUES (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(insert_sql, (
                name, email, str(res_score), timestamp,
                str(no_of_pages), reco_field, cand_level,
                str(skills), str(recommended_skills), str(courses)
            ))
        return True
    except Exception as e:
        st.error(f"Error inserting data: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

def run():
    st.set_page_config(
        page_title="AI Resume Analyzer",
        page_icon='./Logo/logo2.png',
    )
    
    try:
        img = Image.open('./Logo/logo2.png')
        st.image(img)
    except:
        st.warning("Logo image not found")

    st.title("AI Resume Analyser")
    st.sidebar.markdown("# Choose User")
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    st.sidebar.markdown('[Devoloped by Sahithi_Puchakayala](https://www.linkedin.com/in/sahithi-puchakayala-b79488284/)', unsafe_allow_html=True)

    if not init_database():
        st.error("Failed to initialize database")
        st.stop()

    if choice == 'User':
        st.markdown('''<h5 style='text-align: left; color: #021659;'> Upload your resume for analysis</h5>''',
                   unsafe_allow_html=True)
        
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        
        # Job description input
        target_role = st.selectbox("Select your target role:", 
                                  ["Data Scientist", "Web Developer", "Software Engineer", 
                                   "Product Manager", "UX Designer", "Other"])
        job_description = st.text_area("Paste the job description (optional):", height=150)
        
        if pdf_file is not None:
            os.makedirs('./Uploaded_Resumes', exist_ok=True)
            save_image_path = f'./Uploaded_Resumes/{pdf_file.name}'
            
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            
            show_pdf(save_image_path)
            
            with st.spinner('Analyzing your resume...'):
                # Parse resume
                parser = CustomResumeParser(save_image_path)
                resume_data = parser.get_extracted_data()
                
                # Calculate resume score
                resume_score = calculate_resume_score(resume_data, job_description)
                
                # Get recommended skills
                recommended_skills = get_recommended_skills(target_role, job_description)
                
                if not resume_data.get('name') or resume_data['name'] == "Your Name":
                    st.warning("We couldn't detect your name automatically. Please enter it below:")
                    resume_data['name'] = st.text_input("Your Full Name", value=resume_data['name'])
                
                st.header("**Resume Analysis**")
                st.success(f"Hello {resume_data['name']}")
                
                # Display Resume Score with visual progress bar
                st.subheader("**Resume Score**")
                st.markdown(f"**Your Resume Score: {resume_score}/100**")
                st.progress(resume_score / 100)
                
                # Score breakdown
                with st.expander("How is my score calculated?"):
                    st.markdown("""
                    - **Basic Information (Name, Email)**: 20 points
                    - **Skills Listed**: 20 points
                    - **Education**: 20 points
                    - **Experience**: 20 points
                    - **Job Description Match**: 20 points (if provided)
                    """)
                
                st.subheader("**Your Basic info**")
                st.text(f"Name: {resume_data['name']}")
                st.text(f"Email: {resume_data['email']}")
                st.text(f"Resume pages: {resume_data['no_of_pages']}")
                
                # Determine candidate level
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''', unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''', unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >= 3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''', unsafe_allow_html=True)
                
                # Current Skills
                st.subheader("**Your Current Skills**")
                keywords = st_tags(
                    label='### Your Skills',
                    text='These skills were identified in your resume',
                    value=resume_data['skills'],
                    key='1'
                )
                
                # Recommended Skills
                st.subheader("**Recommended Skills**")
                st.markdown(f"Based on your target role as **{target_role}**, we recommend adding these skills:")
                
                # Display recommended skills
                recommended_skills_display = st_tags(
                    label='### Skills to Add',
                    text='These skills would strengthen your resume',
                    value=recommended_skills,
                    key='recommended_skills'
                )
                
                # Skill gap analysis
                missing_skills = [skill for skill in recommended_skills_display if skill.lower() not in [s.lower() for s in resume_data['skills']]]
                if missing_skills:
                    st.warning(f"**You're missing these key skills for {target_role} roles:**")
                    for skill in missing_skills:
                        st.markdown(f"- {skill}")
                
                # Courses recommendation
                st.subheader("**Recommended Courses**")
                if target_role == "Data Scientist":
                    rec_course = course_recommender(ds_course)
                elif target_role == "Web Developer":
                    rec_course = course_recommender(web_course)
                elif target_role == "Software Engineer":
                    rec_course = course_recommender(android_course + ios_course)
                else:
                    rec_course = course_recommender(uiux_course)
                
                # Save data to database
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)
                
                if insert_data(resume_data['name'], resume_data['email'], str(resume_score), timestamp,
                             str(resume_data['no_of_pages']), target_role, cand_level, str(resume_data['skills']),
                             str(recommended_skills_display), str(rec_course)):
                    st.success("Analysis saved successfully!")
                else:
                    st.warning("Could not save analysis to database")

    else:  # Admin Side
        st.success('Welcome to Admin Side')
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        
        if st.button('Login'):
            if ad_user == 'briit' and ad_password == 'briit123':
                st.success("Welcome Dr Briit!")
                
                conn = create_connection()
                if conn:
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute('''SELECT * FROM user_data''')
                            data = cursor.fetchall()
                            
                            if data:
                                df = pd.DataFrame(data, columns=[
                                    'ID', 'Name', 'Email', 'Resume Score', 'Timestamp',
                                    'Total Page', 'Predicted Field', 'User Level',
                                    'Actual Skills', 'Recommended Skills', 'Recommended Course'
                                ])
                                
                                st.header("**User's Data**")
                                st.dataframe(df)
                                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), 
                                           unsafe_allow_html=True)
                                
                                # Visualization
                                st.subheader("**Field Recommendations Distribution**")
                                if not df.empty:
                                    fig = px.pie(df, names='Predicted Field', title='Field Recommendations')
                                    st.plotly_chart(fig)
                                    
                                    st.subheader("**User Experience Levels**")
                                    fig = px.pie(df, names='User Level', title="User Experience Distribution")
                                    st.plotly_chart(fig)
                            else:
                                st.warning("No user data found")
                    except Exception as e:
                        st.error(f"Error fetching data: {str(e)}")
                    finally:
                        conn.close()
                else:
                    st.error("Database connection failed")
            else:
                st.error("Invalid credentials")

if __name__ == "__main__":
    run()