class QuestionGenerator:
    """
    Generates different types of exam questions from retrieved context.
    """

    def generate_questions(self, context):

        mcq = []
        short_answer = []
        viva = []

        sentences = context.split(".")

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) < 30:
                continue

            sentence = " ".join(sentence.split())
            words = sentence.split()[:10]
            topic = " ".join(words)

            mcq.append(f"What does {topic} refer to?")
            short_answer.append(f"Explain {topic}.")
            viva.append(f"Can you describe {topic}?")

        return mcq, short_answer, viva