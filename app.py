import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import uuid
import json

# Page configuration
st.set_page_config(
    page_title="Bhasha Corpus - Indic Language AI Builder",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'contributions' not in st.session_state:
    st.session_state.contributions = []
if 'audio_hours' not in st.session_state:
    st.session_state.audio_hours = 0
if 'video_hours' not in st.session_state:
    st.session_state.video_hours = 0
if 'text_records' not in st.session_state:
    st.session_state.text_records = 0
if 'image_records' not in st.session_state:
    st.session_state.image_records = 0
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Language Contributor"

# Language data
LANGUAGES = {
    "Hindi": {"name": "हिन्दी", "contributors": 156, "hours": 234.5},
    "Tamil": {"name": "தமிழ்", "contributors": 143, "hours": 198.2},
    "Telugu": {"name": "తెలుగు", "contributors": 98, "hours": 167.8},
    "Bengali": {"name": "বাংলা", "contributors": 87, "hours": 145.3},
    "Marathi": {"name": "मराठी", "contributors": 76, "hours": 134.7},
    "Gujarati": {"name": "ગુજરાતી", "contributors": 65, "hours": 112.4},
    "Kannada": {"name": "ಕನ್ನಡ", "contributors": 54, "hours": 98.6},
    "Malayalam": {"name": "മലയാളം", "contributors": 43, "hours": 87.3},
    "English": {"name": "English", "contributors": 0, "hours": 0}
}

def render_home():
    st.title("🗣️ Bhasha Corpus - Indic Language AI Builder")
    st.markdown("### **Building AI datasets to preserve and teach Indian languages**")
    
    # Hero section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        #### 🎯 Our Mission
        Help build the world's largest open Indic language dataset for AI training. 
        Your contributions help create:
        
        - 🤖 **Voice assistants** in your mother tongue
        - 🌐 **Better translation** models  
        - 📚 **Language learning** applications
        - 🏛️ **Cultural preservation** tools
        - 🎓 **Educational AI** for Indian languages
        
        #### 🏆 Internship Goals (Per Contributor)
        - **🎵 Audio/Video**: 80 hours minimum
        - **📝 Text/Images**: 800 records minimum
        - **👥 Team Collaboration**: Build together
        - **📊 Quality Focus**: High-quality contributions
        """)
        
        if st.button("🚀 Start Contributing Now!", type="primary", use_container_width=True):
            st.session_state.current_page = "contribute"
            st.rerun()
    
    with col2:
        st.markdown("#### 📊 Your Progress")
        
        # Progress metrics
        audio_progress = min(st.session_state.audio_hours + st.session_state.video_hours, 80)
        text_progress = min(st.session_state.text_records + st.session_state.image_records, 800)
        
        st.metric("🎵 Audio+Video Hours", f"{audio_progress:.1f}/80", 
                 f"+{st.session_state.audio_hours + st.session_state.video_hours:.1f}")
        st.metric("📝 Text+Image Records", f"{text_progress}/800", 
                 f"+{st.session_state.text_records + st.session_state.image_records}")
        st.metric("🏆 Overall Progress", f"{((audio_progress/80 + text_progress/800)/2*100):.1f}%")
        
        # Weekly recommendation
        st.info("📅 **Weekly Target:** 20 hours + 200 records")
    
    # Global statistics
    st.markdown("---")
    st.markdown("#### 🌍 Global Corpus Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎵 Total Audio Hours", "2,847", "+234 this week")
    with col2:
        st.metric("📝 Text Records", "45,672", "+3,421 this week")
    with col3:
        st.metric("🌐 Languages", len(LANGUAGES), "More coming")
    with col4:
        st.metric("👥 Contributors", "1,247", "+89 this week")
    
    # Language breakdown
    st.markdown("#### 🗣️ Language Contributions")
    
    lang_data = []
    for lang, data in LANGUAGES.items():
        lang_data.append({
            "Language": f"{lang} ({data['name']})",
            "Contributors": data['contributors'], 
            "Hours": data['hours']
        })
    
    df = pd.DataFrame(lang_data)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df, x="Language", y="Contributors", title="Contributors by Language")
        fig.update_layout(xaxis_tickangle=45) 
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(df, values="Hours", names="Language", title="Audio Hours by Language")
        st.plotly_chart(fig, use_container_width=True)

def render_contribute():
    st.title("📤 Contribute to Indic Language Corpus")
    st.markdown("**Every contribution helps build better AI for Indian languages!**")
    
    # Progress tracking header
    col1, col2, col3, col4 = st.columns(4)
    
    audio_total = st.session_state.audio_hours + st.session_state.video_hours
    text_total = st.session_state.text_records + st.session_state.image_records
    
    audio_progress = min(audio_total / 80 * 100, 100)
    text_progress = min(text_total / 800 * 100, 100)
    
    with col1:
        st.metric("🎵 Audio Progress", f"{audio_progress:.1f}%")
        st.progress(audio_progress / 100)
    with col2:
        st.metric("🎥 Video Progress", f"{st.session_state.video_hours:.1f}h")
        st.progress(min(st.session_state.video_hours / 40 * 100, 100) / 100)
    with col3:
        st.metric("📝 Text Progress", f"{text_progress:.1f}%") 
        st.progress(text_progress / 100)
    with col4:
        st.metric("🖼️ Images", f"{st.session_state.image_records}/400")
        st.progress(min(st.session_state.image_records / 400 * 100, 100) / 100)
    
    # Contribution tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎤 Audio Recording", "🎥 Video Recording", "📝 Text Data", "🖼️ Image Data"])
    
    with tab1:
        render_audio_contribution()
    
    with tab2:
        render_video_contribution()
    
    with tab3:
        render_text_contribution()
    
    with tab4:
        render_image_contribution()

def render_audio_contribution():
    st.subheader("🎤 Audio Corpus Collection")
    st.markdown("Record natural speech in Indian languages for AI training")
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox("Choose Language", 
                               [f"{lang} ({data['name']})" for lang, data in LANGUAGES.items()],
                               key="audio_lang")
        
        categories = [
            "🗣️ Common Phrases", 
            "🔢 Numbers & Counting", 
            "💬 Daily Conversations", 
            "📚 Stories & Literature",
            "🎵 Songs & Poetry",
            "📰 News Reading",
            "🏛️ Cultural Content",
            "🎓 Educational Content"
        ]
        category = st.selectbox("Content Category", categories, key="audio_cat")
    
    with col2:
        duration_options = ["2-3 minutes", "3-5 minutes", "5-10 minutes", "10+ minutes"]
        duration = st.selectbox("Recording Duration", duration_options, key="audio_dur")
        
        quality = st.selectbox("Audio Quality", ["High (Studio)", "Medium (Quiet room)", "Basic (Normal)"], key="audio_qual")
    
    # Sample prompts based on category
    prompts = {
        "🗣️ Common Phrases": [
            "Introduce yourself and your background",
            "Describe your daily routine", 
            "Talk about your family and hometown",
            "Share your favorite memories"
        ],
        "🔢 Numbers & Counting": [
            "Count from 1 to 100",
            "Say important years and dates",
            "Describe quantities and measurements",
            "Read phone numbers and addresses"
        ],
        "💬 Daily Conversations": [
            "Order food at a restaurant",
            "Ask for directions",
            "Shopping conversation",
            "Doctor visit conversation"
        ],
        "📚 Stories & Literature": [
            "Tell a folk tale from your region",
            "Recite a famous poem",
            "Share a moral story",
            "Describe local legends"
        ]
    }
    
    if category in prompts:
        selected_prompt = st.selectbox("Choose Recording Prompt", prompts[category], key="audio_prompt")
        st.info(f"🎯 **Your Task:** {selected_prompt}")
        
        with st.expander("💡 Recording Tips"):
            st.markdown("""
            - **Speak clearly** and at natural pace
            - **Use natural expressions** - don't sound robotic
            - **Include emotions** and natural pauses
            - **Avoid background noise**
            - **Speak in your regional dialect** - variations are valuable!
            """)
    
    # Recording simulation
    if st.button("🎤 Start Recording", key="record_audio", type="primary"):
        lang_clean = language.split(" (")[0]
        
        with st.spinner("🔴 Recording in progress... Speak clearly!"):
            # Simulate recording time
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.03)  # 3 second total simulation
                progress_bar.progress(i + 1)
        
        # Determine duration hours
        duration_map = {
            "2-3 minutes": 0.04,  # 2.5 minutes = 0.04 hours
            "3-5 minutes": 0.07,  # 4 minutes = 0.07 hours  
            "5-10 minutes": 0.12, # 7.5 minutes = 0.12 hours
            "10+ minutes": 0.25   # 15 minutes = 0.25 hours
        }
        
        hours_added = duration_map.get(duration, 0.04)
        
        # Add contribution
        contribution = {
            "id": str(uuid.uuid4()),
            "type": "audio",
            "language": lang_clean,
            "category": category,
            "prompt": selected_prompt if category in prompts else "Custom recording",
            "duration": duration,
            "duration_hours": hours_added,
            "quality": quality,
            "timestamp": datetime.now().isoformat(),
            "contributor": st.session_state.user_name
        }
        
        st.session_state.contributions.append(contribution)
        st.session_state.audio_hours += hours_added
        
        st.success(f"✅ **Recording Saved!** +{hours_added:.2f} hours to corpus")
        st.balloons()
        st.rerun()

def render_video_contribution():
    st.subheader("🎥 Video Corpus Collection") 
    st.markdown("Create visual language content for multimodal AI training")
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox("Choose Language", 
                               [f"{lang} ({data['name']})" for lang, data in LANGUAGES.items()],
                               key="video_lang")
        
        video_types = [
            "👋 Sign Language & Gestures",
            "🎭 Cultural Performances", 
            "🍳 Cooking Instructions",
            "🏛️ Monument & Place Descriptions",
            "📖 Story Telling with Visuals",
            "🎓 Educational Explanations",
            "🎨 Art & Craft Tutorials"
        ]
        video_type = st.selectbox("Video Type", video_types, key="video_type")
    
    with col2:
        duration = st.selectbox("Video Duration", 
                               ["5-10 minutes", "10-15 minutes", "15-20 minutes", "20+ minutes"], 
                               key="video_dur")
        
        setting = st.selectbox("Recording Setting", 
                              ["Indoor/Studio", "Outdoor/Natural", "Cultural Location", "Educational Setup"],
                              key="video_setting")
    
    video_prompts = {
        "👋 Sign Language & Gestures": [
            "Demonstrate common gestures in your culture",
            "Show traditional greeting styles",
            "Express emotions through gestures"
        ],
        "🎭 Cultural Performances": [
            "Perform a traditional dance",
            "Sing a folk song",
            "Demonstrate cultural rituals"
        ],
        "🍳 Cooking Instructions": [
            "Cook a traditional dish step-by-step",
            "Explain ingredients in local language",
            "Share family recipes"
        ]
    }
    
    if video_type in video_prompts:
        prompt = st.selectbox("Video Prompt", video_prompts[video_type], key="video_prompt")
        st.info(f"🎬 **Your Task:** {prompt}")
    
    if st.button("🎥 Start Video Recording", key="record_video", type="primary"):
        lang_clean = language.split(" (")[0]
        
        with st.spinner("🔴 Recording video... Action!"):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.05)  # 5 second simulation
                progress_bar.progress(i + 1)
        
        # Duration mapping for videos
        duration_map = {
            "5-10 minutes": 0.12,  # 7.5 minutes = 0.12 hours
            "10-15 minutes": 0.21, # 12.5 minutes = 0.21 hours
            "15-20 minutes": 0.29, # 17.5 minutes = 0.29 hours
            "20+ minutes": 0.42    # 25 minutes = 0.42 hours
        }
        
        hours_added = duration_map.get(duration, 0.12)
        
        contribution = {
            "id": str(uuid.uuid4()),
            "type": "video",
            "language": lang_clean,
            "video_type": video_type,
            "prompt": prompt if video_type in video_prompts else "Custom video",
            "duration": duration,
            "duration_hours": hours_added,
            "setting": setting,
            "timestamp": datetime.now().isoformat(),
            "contributor": st.session_state.user_name
        }
        
        st.session_state.contributions.append(contribution)
        st.session_state.video_hours += hours_added
        
        st.success(f"✅ **Video Saved!** +{hours_added:.2f} hours to corpus")
        st.balloons()
        st.rerun()

def render_text_contribution():
    st.subheader("📝 Text Corpus Collection")
    st.markdown("Contribute text data for language model training")
    
    col1, col2 = st.columns(2)
    
    with col1:
        text_type = st.selectbox("Text Type", [
            "🌐 Translation Pairs",
            "📚 Literature & Poetry", 
            "📰 News & Articles",
            "💬 Conversational Data",
            "🏛️ Cultural Content",
            "🎓 Educational Material",
            "📱 Social Media Style",
            "📧 Formal Communications"
        ], key="text_type")
        
        source_lang = st.selectbox("Source Language", 
                                  ["English"] + list(LANGUAGES.keys()),
                                  key="source_lang")
    
    with col2:
        target_lang = st.selectbox("Target Language", 
                                  list(LANGUAGES.keys()),
                                  key="target_lang")
        
        difficulty = st.selectbox("Content Difficulty", 
                                 ["Basic/Everyday", "Intermediate", "Advanced/Technical"],
                                 key="text_diff")
    
    # Text input areas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{source_lang} Text:**")
        source_text = st.text_area("Enter source text", height=200, 
                                 placeholder="Enter text to translate or create original content...",
                                 key="source_text")
        
        # Word count
        if source_text:
            st.caption(f"📊 {len(source_text.split())} words, {len(source_text)} characters")
    
    with col2:
        st.markdown(f"**{target_lang} Text:**")
        target_text = st.text_area("Enter target text", height=200,
                                 placeholder="Provide translation or equivalent content...",
                                 key="target_text")
        
        if target_text:
            st.caption(f"📊 {len(target_text.split())} words, {len(target_text)} characters")
    
    # Additional context
    context = st.text_input("Cultural Context (optional)", 
                           placeholder="Explain cultural nuances, regional variations, usage context...",
                           key="text_context")
    
    region = st.selectbox("Regional Dialect", 
                         ["Standard", "Northern", "Southern", "Eastern", "Western", "Central"],
                         key="text_region")
    
    if st.button("📤 Submit Text Contribution", key="submit_text", type="primary"):
        if source_text and target_text and len(source_text) > 20 and len(target_text) > 20:
            contribution = {
                "id": str(uuid.uuid4()),
                "type": "text",
                "text_type": text_type,
                "source_language": source_lang,
                "target_language": target_lang,
                "source_text": source_text,
                "target_text": target_text,
                "difficulty": difficulty,
                "context": context,
                "region": region,
                "word_count": len(target_text.split()),
                "timestamp": datetime.now().isoformat(),
                "contributor": st.session_state.user_name
            }
            
            st.session_state.contributions.append(contribution)
            st.session_state.text_records += 1
            
            st.success(f"✅ **Text Contribution Added!** Total records: {st.session_state.text_records}")
            
            # Clear the text areas
            st.session_state.source_text = ""
            st.session_state.target_text = ""
            st.session_state.text_context = ""
            
            st.rerun()
        else:
            st.error("Please provide substantial text in both fields (minimum 20 characters each)")

def render_image_contribution():
    st.subheader("🖼️ Visual Context Collection")
    st.markdown("Add images with descriptions for multimodal AI training")
    
    col1, col2 = st.columns(2)
    
    with col1:
        image_category = st.selectbox("Image Category", [
            "🏛️ Cultural Heritage",
            "🍽️ Food & Cuisine", 
            "🎭 Festivals & Celebrations",
            "🏞️ Landscapes & Places",
            "👥 People & Portraits",
            "📚 Documents & Text",
            "🎨 Art & Crafts",
            "📱 Modern Life"
        ], key="img_cat")
        
        description_lang = st.selectbox("Description Language", 
                                       list(LANGUAGES.keys()),
                                       key="desc_lang")
    
    with col2:
        uploaded_image = st.file_uploader("Upload Image", 
                                         type=['png', 'jpg', 'jpeg', 'webp'],
                                         key="upload_img")
        
        if uploaded_image:
            st.image(uploaded_image, width=300, caption="Your uploaded image")
    
    if uploaded_image:
        # Description fields
        description = st.text_area("Describe this image in your language", 
                                 height=150,
                                 placeholder="What do you see? Describe objects, people, activities, cultural significance...",
                                 key="img_desc")
        
        cultural_significance = st.text_area("Cultural Significance (optional)",
                                           height=100, 
                                           placeholder="Explain any cultural, historical, or regional importance...",
                                           key="img_cultural")
        
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("Location (optional)", 
                                   placeholder="Where was this taken?",
                                   key="img_location")
        with col2:
            tags = st.text_input("Tags (comma-separated)", 
                                placeholder="festival, food, temple, traditional...",
                                key="img_tags")
        
        if st.button("📤 Submit Image + Description", key="submit_image", type="primary"):
            if description and len(description) > 30:
                contribution = {
                    "id": str(uuid.uuid4()),
                    "type": "image",
                    "category": image_category,
                    "language": description_lang,
                    "description": description,
                    "cultural_significance": cultural_significance,
                    "location": location,
                    "tags": tags.split(",") if tags else [],
                    "filename": uploaded_image.name,
                    "file_size": len(uploaded_image.getvalue()),
                    "timestamp": datetime.now().isoformat(),
                    "contributor": st.session_state.user_name
                }
                
                st.session_state.contributions.append(contribution)
                st.session_state.image_records += 1
                
                st.success(f"✅ **Image Contribution Added!** Total images: {st.session_state.image_records}")
                
                # Clear description
                st.session_state.img_desc = ""
                st.session_state.img_cultural = ""
                st.session_state.img_location = ""
                st.session_state.img_tags = ""
                
                st.rerun()
            else:
                st.error("Please provide a detailed description (minimum 30 characters)")

def render_dashboard():
    st.title("📊 Personal Dashboard")
    st.markdown(f"**Welcome back, {st.session_state.user_name}!**")
    
    # Overall progress
    col1, col2, col3 = st.columns(3)
    
    total_av = st.session_state.audio_hours + st.session_state.video_hours
    total_ti = st.session_state.text_records + st.session_state.image_records
    
    with col1:
        st.metric("🎯 Overall Progress", 
                 f"{((total_av/80 + total_ti/800)/2*100):.1f}%",
                 "Towards internship goal")
    with col2:
        st.metric("📅 Days Active", "5", "This week")
    with col3:
        st.metric("🏆 Quality Score", "94.2%", "+2.1%")
    
    # Progress charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Weekly Progress")
        
        # Simulate weekly data
        progress_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Audio Hours': [2.5, 1.2, 3.8, 2.1, 4.2, 1.8, 0.9],
            'Text Records': [15, 23, 8, 34, 19, 28, 12]
        })
        
        fig = px.line(progress_data, x='Day', y=['Audio Hours', 'Text Records'],
                     title="Daily Contributions This Week")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🗣️ Language Distribution")
        
        # Language contribution breakdown
        if st.session_state.contributions:
            lang_counts = {}
            for contrib in st.session_state.contributions:
                lang = contrib.get('language', 'Unknown')
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
            
            if lang_counts:
                fig = px.pie(values=list(lang_counts.values()), 
                           names=list(lang_counts.keys()),
                           title="Your Contributions by Language")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Start contributing to see your language distribution!")
    
    # Recent contributions
    st.subheader("📋 Recent Contributions")
    
    if st.session_state.contributions:
        recent = st.session_state.contributions[-10:]  # Last 10 contributions
        
        for contrib in reversed(recent):
            with st.expander(f"{contrib['type'].title()} - {contrib.get('language', 'N/A')} - {contrib['timestamp'][:16].replace('T', ' ')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Type:** {contrib['type'].title()}")
                    st.write(f"**Language:** {contrib.get('language', 'N/A')}")
                    if 'duration_hours' in contrib:
                        st.write(f"**Duration:** {contrib['duration_hours']:.2f} hours")
                
                with col2:
                    if contrib['type'] == 'audio':
                        st.write(f"**Category:** {contrib.get('category', 'N/A')}")
                        st.write(f"**Quality:** {contrib.get('quality', 'N/A')}")
                    elif contrib['type'] == 'text':
                        st.write(f"**Word Count:** {contrib.get('word_count', 'N/A')}")
                        st.write(f"**Difficulty:** {contrib.get('difficulty', 'N/A')}")
                
                if 'prompt' in contrib and contrib['prompt']:
                    st.write(f"**Prompt:** {contrib['prompt'][:100]}...")
    else:
        st.info("No contributions yet. Start contributing to see your activity!")
    
    # Achievements
    st.subheader("🏆 Achievements")
    
    achievements = []
    
    # Check various achievements
    if st.session_state.audio_hours > 0:
        achievements.append("🎤 First Audio Recording")
    if st.session_state.video_hours > 0:
        achievements.append("🎥 First Video Recording") 
    if st.session_state.text_records > 0:
        achievements.append("📝 First Text Contribution")
    if st.session_state.image_records > 0:
        achievements.append("🖼️ First Image Contribution")
    if st.session_state.text_records >= 50:
        achievements.append("📚 Text Enthusiast (50+ records)")
    if (st.session_state.audio_hours + st.session_state.video_hours) >= 10:
        achievements.append("🎵 Audio Master (10+ hours)")
    if len(set(contrib.get('language', '') for contrib in st.session_state.contributions)) >= 3:
        achievements.append("🌐 Multilingual Contributor")
    
    if achievements:
        for achievement in achievements:
            st.success(f"✅ {achievement}")
    else:
        st.info("Start contributing to unlock achievements!")

def render_team_progress():
    st.title("👥 Team Corpus Building")
    st.markdown("**Collaborative Indic language dataset construction**")
    
    # Team stats
    teams_data = {
        "Tamil Titans": {
            "audio": 67.8, "video": 23.4, "text": 543, "images": 234, 
            "members": 5, "languages": ["Tamil", "English"]
        },
        "Hindi Heroes": {
            "audio": 58.3, "video": 19.2, "text": 487, "images": 198, 
            "members": 4, "languages": ["Hindi", "Punjabi", "English"]
        },
        "Your Team": {
            "audio": st.session_state.audio_hours, 
            "video": st.session_state.video_hours,
            "text": st.session_state.text_records, 
            "images": st.session_state.image_records,
            "members": 1, "languages": list(set(contrib.get('language', '') for contrib in st.session_state.contributions))
        },
        "Bengali Bulls": {
            "audio": 45.6, "video": 15.8, "text": 398, "images": 167, 
            "members": 4, "languages": ["Bengali", "English"]
        },
        "Telugu Tigers": {
            "audio": 52.1, "video": 18.3, "text": 423, "images": 189, 
            "members": 5, "languages": ["Telugu", "English"]
        }
    }
    
    st.subheader("🏆 Team Leaderboard")
    
    # Create leaderboard dataframe
    leaderboard_data = []
    for team, stats in teams_data.items():
        total_hours = stats['audio'] + stats['video']
        total_records = stats['text'] + stats['images']
        overall_score = (total_hours/80 + total_records/800) * 50  # Out of 100
        
        leaderboard_data.append({
            "Team": team,
            "Audio+Video": f"{total_hours:.1f}h",
            "Text+Images": total_records,
            "Members": stats['members'],
            "Languages": len(stats['languages']),
            "Score": f"{overall_score:.1f}%"
        })
    
    # Sort by score
    df = pd.DataFrame(leaderboard_data)
    df['ScoreNum'] = df['Score'].str.replace('%', '').astype(float)
    df = df.sort_values('ScoreNum', ascending=False).drop('ScoreNum', axis=1)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Team collaboration features
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Progress Comparison")
        
        comparison_data = []
        for team, stats in teams_data.items():
            comparison_data.append({
                "Team": team,
                "Audio Hours": stats['audio'],
                "Text Records": stats['text']
            })
        
        comp_df = pd.DataFrame(comparison_data)
        fig = px.scatter(comp_df, x="Audio Hours", y="Text Records", 
                        text="Team", title="Team Performance Scatter")
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🌐 Language Coverage")
        
        all_languages = set()
        for stats in teams_data.values():
            all_languages.update(stats['languages'])
        
        lang_coverage = []
        for lang in all_languages:
            count = sum(1 for stats in teams_data.values() if lang in stats['languages'])
            lang_coverage.append({"Language": lang, "Teams": count})
        
        coverage_df = pd.DataFrame(lang_coverage)
        fig = px.bar(coverage_df, x="Language", y="Teams", 
                    title="Language Coverage Across Teams")
        st.plotly_chart(fig, use_container_width=True)
    
    # Collaboration tools
    st.subheader("🤝 Collaboration Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Team Chat", use_container_width=True):
            st.info("Opening team chat... (Feature coming soon)")
    
    with col2:
        if st.button("📋 Shared Tasks", use_container_width=True):
            st.info("Loading shared task board... (Feature coming soon)")
    
    with col3:
        if st.button("📈 Team Analytics", use_container_width=True):
            st.info("Generating detailed team analytics... (Feature coming soon)")

def render_export():
    st.title("📥 Export & Submit Data")
    st.markdown("**Prepare your contributions for submission to corpus.swecha.org**")
    
    if not st.session_state.contributions:
        st.info("🔍 No contributions found. Start contributing to enable data export!")
        return
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    audio_contribs = [c for c in st.session_state.contributions if c['type'] == 'audio']
    video_contribs = [c for c in st.session_state.contributions if c['type'] == 'video']
    text_contribs = [c for c in st.session_state.contributions if c['type'] == 'text']
    image_contribs = [c for c in st.session_state.contributions if c['type'] == 'image']
    
    with col1:
        st.metric("🎤 Audio", f"{len(audio_contribs)} recordings", f"{st.session_state.audio_hours:.1f} hours")
    with col2:
        st.metric("🎥 Video", f"{len(video_contribs)} recordings", f"{st.session_state.video_hours:.1f} hours")
    with col3:
        st.metric("📝 Text", f"{len(text_contribs)} records", f"{sum(c.get('word_count', 0) for c in text_contribs)} words")
    with col4:
        st.metric("🖼️ Images", f"{len(image_contribs)} images", "With descriptions")
    
    # Data preview
    st.subheader("📋 Contribution Summary")
    
    # Create summary dataframe
    summary_data = []
    for contrib in st.session_state.contributions:
        summary_data.append({
            "ID": contrib['id'][:8],
            "Type": contrib['type'].title(),
            "Language": contrib.get('language', 'N/A'),
            "Timestamp": contrib['timestamp'][:16].replace('T', ' '),
            "Details": f"{contrib.get('category', contrib.get('text_type', contrib.get('video_type', 'N/A')))}"
        })
    
    if summary_data:
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Export options
    st.subheader("📤 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        export_format = st.selectbox("Export Format", 
                                   ["CSV (Recommended)", "JSON", "Excel"])
        
        include_metadata = st.checkbox("Include detailed metadata", value=True)
        
        anonymize = st.checkbox("Anonymize contributor info", value=False)
    
    with col2:
        date_filter = st.date_input("Filter by date (optional)")
        
        type_filter = st.multiselect("Filter by type", 
                                   ["audio", "video", "text", "image"],
                                   default=["audio", "video", "text", "image"])
    
    # Generate export data
    if st.button("📥 Generate Export File", type="primary"):
        # Filter contributions
        filtered_contribs = st.session_state.contributions.copy()
        
        if type_filter:
            filtered_contribs = [c for c in filtered_contribs if c['type'] in type_filter]
        
        # Anonymize if requested
        if anonymize:
            for contrib in filtered_contribs:
                contrib['contributor'] = 'Anonymous'
        
        # Remove metadata if not requested
        if not include_metadata:
            for contrib in filtered_contribs:
                # Keep only essential fields
                essential = ['id', 'type', 'language', 'timestamp']
                contrib = {k: v for k, v in contrib.items() if k in essential}
        
        # Create export based on format
        if export_format == "CSV (Recommended)":
            df = pd.DataFrame(filtered_contribs)
            csv = df.to_csv(index=False)
            
            filename = f"indic_language_corpus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            st.download_button(
                label="📥 Download CSV for corpus.swecha.org",
                data=csv,
                file_name=filename,
                mime="text/csv",
                use_container_width=True
            )
        
        elif export_format == "JSON":
            json_data = json.dumps(filtered_contribs, indent=2, default=str)
            
            filename = f"indic_language_corpus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=filename,
                mime="application/json",
                use_container_width=True
            )
        
        st.success("✅ Export file ready for download!")
        
        with st.expander("📋 Submission Instructions"):
            st.markdown("""
            ### 📤 How to Submit to Viswam.ai Corpus
            
            1. **Download** your export file using the button above
            2. **Visit** [corpus.swecha.org](https://corpus.swecha.org)
            3. **Login** with your code.swecha.org account
            4. **Upload** your contribution file
            5. **Verify** data quality and completeness
            6. **Submit** for review and inclusion
            
            ### ✅ Quality Guidelines
            - Ensure audio recordings are clear and noise-free
            - Verify translations are accurate and natural
            - Check that cultural context is appropriate
            - Confirm all metadata is complete
            
            ### 🎯 Internship Requirements Met
            - **Audio/Video**: {:.1f}/{} hours
            - **Text/Images**: {}/{} records
            - **Team Collaboration**: Contributing to shared dataset
            - **Quality Focus**: High-quality contributions with metadata
            """.format(
                st.session_state.audio_hours + st.session_state.video_hours, 80,
                st.session_state.text_records + st.session_state.image_records, 800
            ))

# Main application
def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🗣️ Bhasha Corpus")
        st.caption("Indic Language AI Builder")
        
        # User info
        user_name = st.text_input("Your Name", value=st.session_state.user_name, key="user_input")
        if user_name != st.session_state.user_name:
            st.session_state.user_name = user_name
            st.rerun()
        
        st.markdown("---")
        
        # Navigation menu
        pages = {
            "🏠 Home": "home",
            "📤 Contribute": "contribute", 
            "📊 Dashboard": "dashboard",
            "👥 Team Progress": "team",
            "📥 Export Data": "export"
        }
        
        st.markdown("#### 📋 Navigation")
        for label, key in pages.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("#### 📊 Quick Stats")
        st.metric("🎵 Your Audio", f"{st.session_state.audio_hours:.1f}h")
        st.metric("🎥 Your Video", f"{st.session_state.video_hours:.1f}h") 
        st.metric("📝 Your Text", f"{st.session_state.text_records}")
        st.metric("🖼️ Your Images", f"{st.session_state.image_records}")
        
        # Progress bars
        audio_video_progress = min((st.session_state.audio_hours + st.session_state.video_hours) / 80, 1.0)
        text_image_progress = min((st.session_state.text_records + st.session_state.image_records) / 800, 1.0)
        
        st.progress(audio_video_progress, "Audio+Video Progress")
        st.progress(text_image_progress, "Text+Image Progress")
        
        st.markdown("---")
        st.markdown("#### 🎯 Internship Goals")
        st.caption("🎵 80 hours Audio/Video")
        st.caption("📝 800 records Text/Images")
        st.caption("👥 Team collaboration")
        st.caption("📊 Quality contributions")
    
    # Main content area
    page = st.session_state.current_page
    
    if page == 'home':
        render_home()
    elif page == 'contribute':
        render_contribute()
    elif page == 'dashboard':
        render_dashboard()
    elif page == 'team':
        render_team_progress()
    elif page == 'export':
        render_export()

if __name__ == "__main__":
    main()

