import google.generativeai as genai

from flask import current_app


class GeminiService:

    @staticmethod
    def generate_recommendation(report):

        genai.configure(
            api_key=current_app.config["GEMINI_API_KEY"]
        )

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
You are a Senior Cloud Cost Optimization Expert.

Analyze this cloud billing report.

Total Monthly Cost:
₹{report.total_cost}

Highest Spending Service:
{report.highest_service}

Highest Service Cost:
₹{report.highest_cost}

Average Service Cost:
₹{report.average_cost}

Estimated Savings:
₹{report.estimated_savings}

Provide:

1. A short executive summary.

2. Which service should be optimized first.

3. Cost optimization recommendations.

4. Estimated monthly savings.

Keep the answer under 180 words.

Return only plain text.
"""

        response = model.generate_content(prompt)

        return response.text