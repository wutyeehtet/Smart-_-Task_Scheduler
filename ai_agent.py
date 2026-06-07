import os
import json
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: Gemini API Key is missing!")

model = genai.GenerativeModel('gemini-1.5-flash')

def get_task_priority(title, deadline, duration, category):
    """
    Task အချက်အလက်တွေကို Gemini ဆီပို့ပြီး Priority Score (1-10) တောင်းမယ့် Function
    """
    prompt = f"""
    You are an AI Smart Task Scheduler. Evaluate the following task and assign a priority score from 1 to 10 (10 being the most urgent).
    Also, provide a short reason for your score.
    
    Task Title: {title}
    Deadline: {deadline}
    Estimated Duration: {duration} minutes
    Category: {category}
    
    Respond STRICTLY in JSON format like this:
    {{"score": 8, "reason": "Short explanation here"}}
    """

    try:
        response = model.generate_content(prompt)
     
        result_text = response.text.strip().removeprefix('```json').removesuffix('```').strip()
        result_json = json.loads(result_text)
        return result_json
    except Exception as e:
        print(f"AI Error (Priority): {e}")
       
        return {"score": 5, "reason": "Error connecting to AI. Default score applied."}

def get_daily_recommendation(tasks_data):
    """
    လက်ရှိ Task တွေကို ကြည့်ပြီး ဒီနေ့အတွက် အကောင်းဆုံး အကြံပြုချက်တောင်းမယ့် Function
    """
    prompt = f"""
    You are an AI Smart Task Scheduler. Look at the following list of pending tasks and provide a daily schedule recommendation. 
    Tell the user which task they should focus on first and give a short productivity tip.
    
    Pending Tasks: {tasks_data}
    
    Respond STRICTLY in JSON format like this:
    {{"focus_task_id": 1, "recommendation_message": "Focus on [Task Name] because...", "productivity_tip": "Try the Pomodoro technique..."}}
    """

    try:
        response = model.generate_content(prompt)
       
        result_text = response.text.strip().removeprefix('```json').removesuffix('```').strip()
        return json.loads(result_text)
    except Exception as e:
        print(f"AI Error (Recommendation): {e}")
        
        return {
            "focus_task_id": None, 
            "recommendation_message": "Please focus on your highest priority task.", 
            "productivity_tip": "Take a 5-minute break every 25 minutes of work."
        }


if __name__ == "__main__":
    print("Testing AI Agent...")
    
    
    test_priority = get_task_priority(
        title="Complete AI Module Presentation", 
        deadline="2026-05-08", 
        duration=120, 
        category="University Project"
    )
    print("\n--- Priority Test Result ---")
    print(test_priority)

    
    dummy_tasks = [
        {"id": 1, "title": "Buy groceries", "priority": 3},
        {"id": 2, "title": "Finish Database Code", "priority": 9}
    ]
    test_recommendation = get_daily_recommendation(dummy_tasks)
    print("\n--- Recommendation Test Result ---")
    print(test_recommendation)