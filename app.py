### Libraries ###
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go

### Personal Links ###
from config import LINKS

### Components ###
def card_component(title, text=None, icon=None, url=None):
    card_style = "padding: 1.2rem; border-radius: 1.2rem; border: .2rem solid #e6e6e6; margin-bottom: 1.6rem;"
    card_html = f"""
        <div style="{card_style}">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <h2 style="font-size: 28px;">{title}</h2>
    """
    if icon:
        card_html += f'<img src="{icon}" width="80">'
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

def fetch_API(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return response.status_code
    
def display_events(items):
    sorted_items = sorted(items, key=lambda x: x["start"], reverse=True)
    
    for item in sorted_items:
        with st.expander(item["content"]):
            start = item.get("start", None)
            end = item.get("end", "-")  # Replace empty end with "-"
            
            if start:
                st.markdown(f"*{start} to {end}*")  # Italicize the duration
            
            # Loop through all the keys in the item, excluding "start", "end", and "content"
            for key, value in item.items():
                if key not in ["start", "end", "content"]:
                    if isinstance(value, list):  # Only lists are displayed as sub-items
                        st.write(f"**{key.capitalize()}:**")
                        for sub_item in value:
                            st.write(f"- {sub_item}")


### Function to load data from CSV ###
def load_skills_csv(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    skills_freq = dict(zip(df['Skill'], df['Frequency']))
    return skills_freq


### Sidebar Navigation ###
st.sidebar.title("Navigation")
pages = ["About Me", "Documents", "Projects"]
selected_page = st.sidebar.selectbox("Go to", pages)


### Pages ###
if selected_page == "About Me":
    st.header("Profile")
    from config import MY_GITHUB_URL, PROFILE_PICTURE_URL
    profile_info = fetch_info(MY_GITHUB_URL)
    # Calculate the age
    current_year = datetime.now().year
    age = current_year - 2005

    card_component(profile_info[0],
                    f'🇸🇬<br>Male<br>{age} y/o', 
                   icon=PROFILE_PICTURE_URL)
    
    card_component("About Me",
                   text=profile_info[3])

    card_component("Technologies & Tools",
                   text="<br>".join(profile_info[11:]))

    st.header("Skills")
    skills_freq = load_skills_csv("skills.csv")
    wordcloud = WordCloud().generate_from_frequencies(skills_freq)
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    st.header('Progression')
    from items import items
    display_events(items)

    st.header('LeetCode Profile')
    leetcode_data = fetch_API("https://leetcode-api-faisalshohag.vercel.app/javenlai")
    labels = ["Easy", "Medium", "Hard"]
    sizes = [leetcode_data["easySolved"], leetcode_data["mediumSolved"], leetcode_data["hardSolved"]]

    st.subheader("Statistics")
    st.info(f"Total Solved: {leetcode_data['totalSolved']}")
    st.success(f"Contribution Points: {leetcode_data['contributionPoint']}")

    st.subheader("Distribution of Solved Problems")
    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.4)])
    fig.update_traces(textposition='inside', 
                    textinfo='percent+label',
                    hovertemplate='%{label}<br>Solved: %{value}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True)  

    st.subheader("Recent Submissions")
    for submission in leetcode_data["recentSubmissions"]:
        with st.expander(submission["title"]):
            st.write(f"Language: {submission['lang']}")
            st.write(f"Status: {submission['statusDisplay']}")

    st.header('Contact Information')
    card_component("Contact me via email",
                     text=LINKS["email"]["text"],
                     url=LINKS["email"]["url"])

    card_component("Connect on LinkedIn",
                    url=LINKS["linkedin"]["url"],
                    icon=LINKS["linkedin"]["icon"])
    
    card_component("Check out my Github",
                    url=LINKS["github"]["url"],
                    icon=LINKS["github"]["icon"])

elif selected_page == "Documents":
    st.header("Documents")
    resume_url = LINKS["resume"]["url"]
    card_component("Resume", url=resume_url, text=f'<iframe src="{resume_url}" width="100%" height="800px"></iframe>')

    poly_url = LINKS["polytechnic_transcript"]["url"]
    card_component("Polytechnic Transcript", url=poly_url, text=f'<iframe src="{poly_url}" width="100%" height="800px"></iframe>')
   

elif selected_page == "Projects":
    st.header("Projects")

    search_query = st.text_input("Search for a topic...")
    repositories_info = fetch_git_repos("Javen05")
    for repo in repositories_info:
        if repo["info"]:
            if search_query.lower() in repo["name"].lower() or search_query.lower() in repo["info"].lower():
                card_component(title=repo["name"], text=repo["info"], url=repo["url"], icon=LINKS["github"]["icon"])
