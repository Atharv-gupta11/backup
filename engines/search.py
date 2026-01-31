import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

class SearchEngine:
    def __init__(self):
        # Using Serper.dev or Google Custom Search API is standard for 2026 hackathons
        self.api_key = os.getenv("SERPER_API_KEY") 

    def execute_google_search(self, query):
        """Standard API call to fetch real-time global context."""
        if not self.api_key:
            return "Search API key missing. Ground truth verification disabled."
        
        url = "https://google.serper.dev/search"
        payload = {"q": query}
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            results = response.json()
            # Combine snippets into a single context string
            snippets = [item.get('snippet', '') for item in results.get('organic', [])[:3]]
            return " ".join(snippets)
        except Exception as e:
            return f"Search failed: {str(e)}"

    def extract_locations(self, text):
        """Simple Regex-based entity extraction for location generalization."""
        # Professional tip: In production, you'd use spaCy here.
        # For a hackathon, common city/country patterns work well.
        locations = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', text)
        return list(set(locations))[:5] # Return unique entities

    def check_context(self, claim):
        # GENERALIZED QUERY: Check if the claim is a known social media scam
        # This works for any celebrity or any 'reward' claim
        queries = [
            f"{claim} official statement",
            f"{claim} fake or real scam",
            f"official website for {claim}"
        ]
        
        combined_results = ""
        for q in queries:
            combined_results += self.execute_google_search(q) + " "

        # 2026 Hackathon Trick: Look for 'Urgency' and 'Reward' patterns in text
        scam_patterns = ["winners selected", "claim now", "fill the form", "randomly selected", "limited time"]
        is_suspicious_text = any(p in claim.lower() for p in scam_patterns)

        return {
            "raw_text": combined_results,
            "is_suspicious_text": is_suspicious_text,
            "source_count": len(combined_results.split())
        }