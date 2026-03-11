class QuestionGenerator:
    """
    Generates clearer exam questions from retrieved context.
    """

    def generate_questions(self, context):

        questions = []

        sentences = context.split(".")

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) < 30:
                continue

            # Clean extra spaces
            sentence = " ".join(sentence.split())

            # Extract first 8–12 words for cleaner question
            words = sentence.split()[:10]
            topic = " ".join(words)

            question = f"What is {topic}?"

            questions.append(question)

        return questions