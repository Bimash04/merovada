from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import google.generativeai as genai  


PLATFORM_CONTEXT = """
You are a chatbot for a user-centric renting web application called 'MeroVada,' designed to facilitate resource sharing, reduce financial stress,
and promote a sustainable and collaborative economy. Here are the platform's aims and objectives:

Aims:
- To develop a user-centric renting web application that facilitates resource sharing, reduces financial stress, and promotes a sustainable and collaborative economy.

Objectives:
- Develop a Comprehensive Platform: Establish efficient connections between item owners and renters.
- User-Centric Design: Simplify registration, item browsing, and rental processes for users.
- Address Urban Challenges: Provide affordable access to basic needs for students, immigrants, and families, reducing unnecessary purchases.
- Encourage Resource Optimization: Promote the use of underused items to reduce waste and support environmental conservation.
- Ensure Trust and Security: Implement user authorization, secure payments, and a credible structure with governance, rewards, and penalties.
- Promote Scalability and Flexibility: Build a platform that can grow and adapt to user needs and new technologies.
- Support Community Building: Foster user relationships and enhance social cohesion in urban settings.

Use this information to provide helpful, platform-specific responses to user queries.
"""

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Configure the Google Gemini API with the API key directly
        genai.configure(api_key="AIzaSyCvDFiQwan6cqTVMWMde59Sc0vzhf_ijB0")
        model = genai.GenerativeModel('gemini-1.5-flash')  
       
        full_prompt = f"{PLATFORM_CONTEXT}\n\nUser Query: {user_message}"

        try:
            # Generate response using the Gemini API
            response = model.generate_content(full_prompt)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"Error: {str(e)}"

        return JsonResponse({"reply": bot_reply})
    return JsonResponse({"error": "Invalid request"}, status=400)

def chat_page(request):
    return render(request, "chatbot.html")