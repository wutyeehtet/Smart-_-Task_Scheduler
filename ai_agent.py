import os
import json
import re
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: API Key is MISSING! Please check your .env file.")
else:
    print(f"✅ API Key loaded successfully! (Starts with: {api_key[:5]}...)")

def extract_json(text):
    
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return None

def get_task_priority(title, deadline, duration, category):
    print(f"--- Asking AI for Priority: {title} ---")
    

    today = datetime.now().strftime("%Y-%m-%d")
    
    prompt = f"""
    You are an AI Smart Task Scheduler for a university student.
    Today's Date is: {today}
    
    Carefully evaluate the following task and assign a priority score from 1 to 10.
    
    Scoring Rubric:
    - 9 to 10: Extremely urgent! (e.g., deadline is today or tomorrow).
    - 7 to 8: High priority (e.g., deadline is within 2 to 4 days).
    - 4 to 6: Medium priority (e.g., deadline is within a week or normal homework).
    - 1 to 3: Low priority (e.g., no deadline, or far in the future).
    
    Task Details:
    - Title: {title}
    - Deadline: {deadline}
    - Estimated Duration: {duration} minutes
    - Category: {category}
    
    Respond STRICTLY in JSON format only:
    {{"score": 8, "reason": "Deadline is very near."}}
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code != 200:
            print(f"❌ GOOGLE API ERROR: {response.text}")
            return {"score": 5, "reason": "API Error"}
            
        data = response.json()
        result_text = data['candidates'][0]['content']['parts'][0]['text']
        
        
        print(f"🤖 AI Raw Response: {result_text}")
        
        clean_json = extract_json(result_text)
        if clean_json:
            return clean_json
        else:
            return {"score": 5, "reason": "JSON Parsing Error"}
            
    except Exception as e:
        print(f"❌ PYTHON ERROR: {e}")
        return {"score": 5, "reason": "Code Error"}

def get_daily_recommendation(tasks_data):
    
    today = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""
    You are an AI Smart Task Scheduler. Today's Date is: {today}
    Look at the following list of pending student tasks and provide a daily schedule recommendation. 
    Tell the user which task they should focus on first and give a short productivity tip.
    
    Pending Tasks: {tasks_data}
    
    Respond strictly in JSON format only:
    {{"focus_task_id": 1, "recommendation_message": "Focus on...", "productivity_tip": "Try..."}}
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, json=payload)
        
        if response.status_code != 200:
            return {
                "focus_task_id": None, 
                "recommendation_message": "API Error.", 
                "productivity_tip": "Check your terminal."
            }
            
            
        data = response.json()
        result_text = data['candidates'][0]['content']['parts'][0]['text']
        clean_json = extract_json(result_text)
        
        if clean_json:
            return clean_json
        else:
            return {
                "focus_task_id": None, 
                "recommendation_message": "Focus on highest priority.", 
                "productivity_tip": "JSON Error."
            }
            
    except Exception as e:
        return {
            "focus_task_id": None, 
            "recommendation_message": "Code Error.", 
            "productivity_tip": "Check terminal."
        }