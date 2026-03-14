import random
import re

class QuestionGenerator:

    def generate_questions(self, context):

        sentences = context.split(".")
        topics = []

        for sentence in sentences:

            sentence = sentence.strip()

            # Remove very short sentences
            if len(sentence) < 40:
                continue

            # Skip slide numbers / formatting
            if re.search(r"\d+ ---", sentence):
                continue

            # Skip professor names / headers
            if "Professor" in sentence or "University" in sentence:
                continue

            words = sentence.split()[:8]
            topic = " ".join(words)

            topics.append(topic)

        mcq = []
        short_answer = []
        viva = []

        for topic in topics:

            distractors = random.sample([t for t in topics if t != topic], min(3, len(topics)-1))

           options = distractors + [topic]
           random.shuffle(options)

            mcq.append({
                question = f"Which of the following best explains: {topic}?",
                "options": options,
                "answer": topic
            })

            short_answer.append(f"Explain {topic}.")
            viva.append(f"What do you understand by {topic}?")

        return mcq, short_answer, viva