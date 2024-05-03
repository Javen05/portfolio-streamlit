import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from streamlit_vis_timeline import st_timeline

### Components ###
def card_component(title, text=None, icon=None, url=None):
    card_style = "padding: 1.2rem; border-radius: 1.2rem; border: .2rem solid #e6e6e6; margin-bottom: 1.6rem;"
    card_html = f"""
        <div style="{card_style}">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <h2 style="font-size: 28px;">{title}</h2>
    """
    if icon:
        card_html += f'<img src="{icon}" width="80" style="margin-left: 2rem;">'
    card_html += """</div>"""

    if text:
        card_html += f'<p style="font-size: 16px; margin-top: 1rem;">{text}</p>'
    if url:
        card_html = f'<a href="{url}" target="_blank">' + card_html + '</a>'
    card_html += """</div>"""

    st.markdown(card_html, unsafe_allow_html=True)

def fetch_git_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        repo_info = []
        for repo in repos:
            name = repo["name"]
            info = repo["description"]
            url = repo["html_url"]
            repo_info.append({"name": name, "info": info, "url": url})
        return repo_info
    
    else:
        st.error(f"Failed to fetch repositories. Status code: {response.status_code}")
        return []

def fetch_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    page_info = soup.get_text()
    array = page_info.split('\n')
    return array


### Sidebar Navigation ###
st.sidebar.title("Navigation")
pages = ["About Me", "Documents", "Projects"]
selected_page = st.sidebar.selectbox("Go to", pages)


### Pages ###
if selected_page == "About Me":
    st.header("Profile")
    MY_GITHUB_URL = "https://raw.githubusercontent.com/Javen05/Javen05/main/README.md"
    profile_info = fetch_info(MY_GITHUB_URL)
    # Calculate the age
    current_year = datetime.now().year
    age = current_year - 2005

    card_component(profile_info[0],
                    f'🇸🇬<br>Male<br>{age} y/o', 
                   icon="https://avatars.githubusercontent.com/u/107395637?s=400&u=0b7ac436dfb509803792053287d0f5dcfa986982&v=4")
    
    card_component("About Me",
                   text=profile_info[3])

    st.header("Skills")
    skills_freq = {
        'Python': 84,
        'SQL': 80,
        'Tableau': 79,
        'Powerpoint': 40,
        'Canvas': 47,
        'Machine Learning': 60,
        'Data Storytelling': 75,
        'Data Mining': 66,
        'Analytical': 77,
        'Data Cleaning': 69,
        'Excel': 66,
        'Problem-Solving': 80,
        'Critical Thinking': 75,
        'Communication Skills': 60,
        'Data Warehousing': 78,
        'Relational Database': 74,
        'ETL': 70,
        'Data Warehousing': 65,
        'Data Engineering': 70,
        'Big Data': 65,
        'Data Modeling': 65,
        'Programming': 70,
        'Data Pipeline': 71,
        'BI': 75,
        'RPA': 64,
        'Full Stack': 66,
        'Creativity': 70,
    }

    wordcloud = WordCloud().generate_from_frequencies(skills_freq)
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    st.header('Progression Chart')
    items = [
        {
            "start": "2024-04-15",
            "end": "2024-10-16",
            "content": "RPA Developer Internship @ Synapxe",
            "skills": [],
        },
        {
            "start": "2023-04-01",
            "end": "2024-04-01",
            "content": "Y2 Diploma",
            "events": [
                "Participated in Alibaba Cloud AI Hackathon",
                "Participated in InnoCon 2023 - Hackathon by Lexagle",
                "Participated in PSA Hackathon 2023 - CodeSprint",
                "Participated in Tableau Data + Movies Hackathon (Within TP)",
                "Completed TP Lead Programme"
            ],
            "skills": [
                "Engineered Machine Learning models and extracted insights by interpreting SHAP",
                "Developed supervised and unsupervised models using Python libraries (Scikit-learn, Pandas, Numpy, Matplotlib, Seaborn, etc.)",
                "Constructed Data Storyboards using Tableau",
                "Conducted Data Mining and Business Analytics using SAS Enterprise Miner",
                "Designed a Data Warehouse and used it for conducting Business Intelligence",
                "Developed an automated ETL Pipline using Alteryx and AWS",
                "Data cleaning and transformations using Python"
            ],
            "achievements": [
                "Director's List Award (AY2023/2024)",
                "Champion for Sustainability Campaign Design Competition - 'Reduce Single-Use Plastics' (Within TP)",
                "Bronze Award for SUSS Analytics and Visualisation Challenge 2023",
            ]
        },
        {
            "start": "2022-04-01",
            "end": "2023-04-01",
            "content": "Y1 Diploma",
            "events": [
                "Trained for WorldSkills SG IT Software Solutions for Business for 1 Semester",
                "Participated in Sustainability Innovation Challenge 2023 by Junior Achievement Singapore",
                "Attended an AWS workshop",
                "Attended an RPA seminar",
            ],
            "skills": [
                "Full Stack Development using MySQL, Express, React, NodeJS",
                "App Ideation and Wireframing using Adobe XD",
                "Built a hardcoded Music App on Android Studio using Java",
                "Built Dashboards using PowerBi",
                "Data Preparation using KNIME"
            ],
            "achievements": [
                "Director's List Award (AY2022/2023), 4.0 GPA for Y1",
                "Participation (58/87) - Lag and Crash 3.0 (CTF)",
                "Bronze Medal - Poly-ITE Olympiad for Informatic (PIOI)"
            ]
        },
        {
            "start": "2021-01-01",
            "end": "2022-01-01",
            "content": "Sec 4",
            "events": [
                "Participated in Shell Education NXplorers"
            ]
        },
        {
            "start": "2020-01-01",
            "end": "2021-01-01",
            "content": "Sec 3",
            "events": [
                "Micro:Bit Training - Innovation Garage",
                "Organisation of CCA Display Day"
            ]
        },
        {
            "start": "2019-01-01",
            "end": "2020-01-01",
            "content": "Sec 2",
            "events": [
                "Drone Swarming DJI Tello EDU - 65DRONES",
                "Participation - Singapore Amazing Flying Machine Competition (SAFMC)"
            ]
        },
        {
            "start": "2018-01-01",
            "end": "2019-01-01",
            "content": "Sec 1",
            "events": [
                "Participation - Science & Technology Challenge by NYP",
                "Certificate of Appreciation - Maker Faire Singapore"
            ]
        },
        {
            "start": "2016",
            "end": "2017",
            "content": "Pri 6",
            "events": [
                "SYF Certificate of Recognition - Art Exhibition",
                "EAGLES (Edusave Award for Achievement, Good Leadership and Services)",
                "Edusave Certificate of Academic Achievement"
            ]
        },
        {
            "start": "2014",
            "end": "2015",
            "content": "Pri 4",
            "events": [
                "Edusave Certificate of Academic Achievement (Top 25%)",
                "Edusave Good Progress Award"
            ]
        },
        {
            "start": "2012",
            "end": "2013",
            "content": "Pri 2",
            "events": [
                "Edusave Certificate of Academic Achievement (Top 25%)",
                "Edusave Good Progress Award",
                "Good Progress Award for Chinese Language"
            ]
        },
        {
            "start": "2023-03-01",
            "end": "2023-04-01",
            "content": "Warehouse Assistant @ UPS Supply Chain Solutions",
            "tasks": [
                "Performed Data Entry using SAP Hana Inventory Management System",
                "Produced Excel Spreadsheets from transaction invoices",
                "Assisted with the logistics of products"
            ]
        },
        {
            "start": "2022-10-01",
            "end": "2022-10-31",
            "content": "Grocery Shopper @ NTUC FairPrice",
            "tasks": [
                "Diligently picked and scanned products for online orders",
                "Assembled and packed groceries for shipping",
                "Ensured positive customer experience by assisting with their requests"
            ]
        },
        {
            "start": "2022-09-01",
            "end": "2022-09-30",
            "content": "Logistics Assistant @ KrisShop",
            "tasks": [
                "Prepared carts for next flight by restocking and updating stock status using a scanner"
            ]
        },
        {
            "start": "2022-02-01",
            "end": "2022-02-28",
            "content": "Picker @ Omni Logistics",
            "tasks": [
                "Picked products specified on a list in a warehouse"
            ]
        },
        {
            "start": "2021-11-15",
            "end": "2021-11-30",
            "content": "Replenisher @ NTUC FairPrice",
            "tasks": [
                "Restocked inventory in storage",
                "Replenished shelves in the frozen food section",
                "Assisted customers with their queries"
            ]
        }
    ]

    timeline = st_timeline(items, groups=[], options={}, height="400px")
    st.subheader("Details")
    st.write("Click on an event on the Progression Chart to view more details.")
    st.write(timeline)

    st.header('Contact Information')
    card_component("Contact me via email",
                     text="javenlai5@gmail.com",
                     url="mailto:javenlai5@gmail.com?subject=Feedback&body=Hi Javen,")

    card_component("Connect on LinkedIn",
                     url="https://www.linkedin.com/in/javen-lai/",
                     icon="https://media.licdn.com/dms/image/D5603AQH9NtyrrcT2dA/profile-displayphoto-shrink_100_100/0/1695917340965?e=1720051200&v=beta&t=nyf3ufspWb3NPxk_z-IKVocksabcVTltOfAMiAS8lJs")
    
    card_component("Check out my Github",
                        url="github.com/Javen05",
                        icon="https://img.icons8.com/?size=256&id=g7P0iny5Rros&format=png")

elif selected_page == "Documents":
    st.header("Documents")
    resume_url = "https://drive.google.com/file/d/1Oe-QSj_f-azkXOviGjzVmZtPibsxgPkq/view?usp=sharing"
    card_component("Resume", url=resume_url, text=f'<iframe src="{resume_url}" width="100%" height="auto"></iframe>')

    poly_url = "https://drive.google.com/file/d/1Pi4CJmaFXUtuAmPIp-oxsRdQ30P9xwdA/view?usp=sharing"
    card_component("Polytechnic Transcript", url=poly_url, text=f'<iframe src="{poly_url}" width="100%" height="auto"></iframe>')
   

elif selected_page == "Projects":
    st.header("Projects")

    search_query = st.text_input("Search for a topic...")
    repositories_info = fetch_git_repos("Javen05")
    for repo in repositories_info:
        if repo["info"]:
            if search_query.lower() in repo["name"].lower() or search_query.lower() in repo["info"].lower():
                card_component(title=repo["name"], text=repo["info"], url=repo["url"], icon="https://img.icons8.com/?size=256&id=g7P0iny5Rros&format=png")
