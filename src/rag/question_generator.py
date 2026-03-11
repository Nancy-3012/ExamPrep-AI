class QuestionGenerator:
    """
    Generates exam questions from retrieved context without a fixed limit.
    """

    def generate_questions(self, context):

        prompt = f"""
You are an AI exam assistant.

Based on the following study material, generate as many useful exam questions as possible.

Study Material:
{context}

Instructions:
- Create different types of questions:
  • MCQ questions
  • Short answer questions
  • Viva questions
- Do NOT limit the number of questions.
- Generate all possible meaningful questions from the material.
"""

        return prompt