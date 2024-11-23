import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from difflib import get_close_matches
import google.generativeai as genai

# Predefined dictionary of KPIs or queries
KPIS = {
    "hi": "<p><b>Hello,</b> How can I assist You?</p>",
    # "how to reduce energy consumption": "<p>Consider using <i>energy-efficient appliances</i> and <u>renewable energy sources</u>.</p>",
    # "what is a smart city": "<p>A <b>smart city</b> integrates technology to enhance the quality of life, efficiency of services, and sustainability.</p>",
    # "how to manage waste sustainably": "<p>Adopt the 3Rs: <i>Reduce</i>, <b>Reuse</b>, and <u>Recycle</u>. Implement proper waste segregation.</p>",
    # "tips for sustainable construction": "<p>Use <b>green materials</b>, optimize energy usage, and reduce construction waste.</p>",
}

def index(request):
    """
    Render the chatbot's main page.
    """
    return render(request, 'index.html')

@csrf_exempt
def ChatResponse(request):
    """
    Handle chat queries and return responses.
    """
    if request.method == "POST":
        try:
            # Parse the JSON request
            data = json.loads(request.body)
            query = data.get("query", "").strip().lower()

            if not query:
                return JsonResponse({"response": "<p>Please provide a valid query.</p>"}, status=400)

            # Check for local KPI match
            response = KPIS.get(query) or find_closest_kpi(query)
            if response:
                return JsonResponse({"response": response})

            # Fall back to calling the generate_response function
            external_response = generate_response(query)
            if external_response:
                return JsonResponse({"response": external_response})
            else:
                return JsonResponse(
                    {"response": "I am currently unable to answer your question. Please try again later."},
                    status=500,
                )

        except json.JSONDecodeError:
            return JsonResponse({"response": "<p>Invalid JSON format.</p>"}, status=400)
    else:
        return HttpResponseBadRequest("<p>Invalid request method.</p>")

def find_closest_kpi(query):
    """
    Find the closest matching KPI using fuzzy matching.
    """
    matches = get_close_matches(query, KPIS.keys(), n=1, cutoff=0.5)
    if matches:
        return KPIS[matches[0]]
    return None

def generate_response(query):
    """
    Generate a response for queries not in KPIs.
    """
    # Simple logic to generate a response based on the query
    genai.configure(api_key="AIzaSyDloTU8alHp2JLXWFkQzPuNFK_4-8q6ckg")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query)
    
    # Formatting response as HTML for aesthetic rendering
    formatted_response = f"<p>{response.text}</p>"
    cleaned_text = formatted_response.replace('*', '')
    return cleaned_text
