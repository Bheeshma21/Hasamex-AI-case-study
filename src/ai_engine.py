import os

from dotenv import load_dotenv
from groq import Groq


try:
    from .retriever import TranscriptRetriever
except ImportError:
    from retriever import TranscriptRetriever


load_dotenv()


class AIEngine:
    """
    Grounded LLM layer for the Hasamex transcript-analysis application.

    Important design decision:
    The LLM generates the synthesis, but citations are NOT generated
    by the LLM. Expert names, markets, timestamps and exact quotes
    always come directly from transcript metadata.
    """

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. "
                "Add GROQ_API_KEY=your_key to the .env file."
            )

        self.client = Groq(api_key=api_key)

        self.retriever = TranscriptRetriever()

        self.model = "openai/gpt-oss-120b"

    def _format_evidence(self, results):
        """
        Convert retrieved transcript passages into structured context
        for the language model.
        """

        evidence = []

        for i, result in enumerate(results, start=1):

            evidence.append(
                f"""SOURCE {i}
Expert: {result['expert']}
Role: {result['role']}
Market: {result['market']}
Timestamp: {result['timestamp']}
Exact transcript text: {result['text']}"""
            )

        return "\n\n".join(evidence)

    def _build_sources(self, results):
        """
        Build verified sources directly from transcript metadata.

        This prevents the language model from hallucinating quotes,
        timestamps or source attribution.
        """

        sources = []
        seen = set()

        for result in results:

            source_id = (
                result["expert"],
                result["market"],
                result["timestamp"],
                result["text"],
            )

            if source_id in seen:
                continue

            seen.add(source_id)

            sources.append(
                {
                    "expert": result["expert"],
                    "role": result["role"],
                    "market": result["market"],
                    "timestamp": result["timestamp"],
                    "quote": result["text"],
                    "similarity": result.get("score"),
                }
            )

        return sources

    def ask(
        self,
        question,
        top_k=12,
        balanced=True,
    ):
        """
        Answer a question using transcript evidence.

        balanced=True:
            Retrieves evidence separately from France, Germany and
            the United Kingdom. This is preferred for cross-call
            analysis.

        balanced=False:
            Uses ordinary global semantic retrieval.
        """

        if not question or not question.strip():

            return {
                "answer": "Please enter a question.",
                "sources": [],
            }

        if balanced:

            # Divide requested context approximately equally across markets.
            market_count = max(
                len(self.retriever.get_markets()),
                1,
            )

            per_market = max(
                2,
                (top_k + market_count - 1) // market_count,
            )

            results = self.retriever.search_across_markets(
                question,
                per_market=per_market,
            )

        else:

            results = self.retriever.search(
                question,
                top_k=top_k,
                expert_only=True,
            )

        if not results:

            return {
                "answer": (
                    "I could not find enough evidence in the "
                    "provided transcripts to answer this question."
                ),
                "sources": [],
            }

        evidence = self._format_evidence(results)

        system_prompt = """
You are a rigorous research assistant analysing expert-call
transcripts about the European robotic surgery market.

Your task is to produce accurate, concise and evidence-grounded
market-research analysis.

STRICT EVIDENCE RULES

1. Use ONLY information contained in the supplied transcript evidence.

2. Never invent facts, numbers, opinions, experts, markets,
   quotations or timestamps.

3. If the evidence is insufficient to support a conclusion,
   explicitly say that the available evidence is insufficient.

4. Do NOT assume that absence from retrieved evidence means an expert
   never discussed a topic.

5. Never say "the expert did not mention this" unless the supplied
   evidence explicitly establishes that fact.

6. Carefully distinguish between:

   - agreement
   - difference in emphasis
   - market-specific difference
   - genuine contradiction

7. A difference in emphasis is NOT automatically a disagreement.

8. Only describe something as a genuine disagreement when two
   experts make clearly incompatible claims.

9. Do not claim that all three experts agree unless evidence from
   all three markets supports the statement.

10. When only two markets support a theme, state that it is supported
    by those two markets rather than all markets.

11. Preserve numerical scope and qualifications exactly.

    For example:

    "15-20 percent annual growth in some stronger centres"

    must NOT become:

    "France will grow 15-20 percent annually."

12. Do not transform a forecast about procedures, centres or selected
    areas into a forecast for an entire national market.

13. Separate factual transcript evidence from your synthesis.

14. Do NOT reproduce exact transcript quotations inside the narrative
    answer.

15. Do NOT generate source citations or timestamps inside the
    narrative answer.

    Verified quotes and timestamps are displayed separately by the
    application using transcript metadata.

16. Prefer cautious professional language when the evidence supports
    several interpretations.

17. Keep answers clear and useful for a professional market-research
    user.
"""

        user_prompt = f"""
USER QUESTION

{question}


TRANSCRIPT EVIDENCE

{evidence}


TASK

Answer the user's question using only the supplied evidence.

Where relevant:

- compare the three markets
- identify common themes
- explain meaningful differences
- preserve qualifications around numbers
- distinguish differences in emphasis from genuine contradictions

Do not provide exact quotations or timestamps in the narrative.
The application will display verified evidence separately.
"""

        try:

            completion = self.client.chat.completions.create(
                model=self.model,
                temperature=0.1,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
            )

            answer = (
                completion
                .choices[0]
                .message
                .content
                .strip()
            )

        except Exception as error:

            return {
                "answer": (
                    "The AI analysis service encountered an error. "
                    f"Details: {str(error)}"
                ),
                "sources": self._build_sources(results),
            }

        sources = self._build_sources(results)

        return {
            "answer": answer,
            "sources": sources,
        }


if __name__ == "__main__":

    engine = AIEngine()

    test_questions = [
        "What are the biggest barriers to adoption across the markets?",
        "How do the experts differ in their view of economics and ROI?",
        "What growth do the experts expect over the next three to five years?",
    ]

    for question in test_questions:

        print("\n" + "=" * 70)

        print("\nQUESTION")
        print(question)

        result = engine.ask(
            question,
            top_k=12,
            balanced=True,
        )

        print("\nANSWER")
        print(result["answer"])

        print("\nVERIFIED SOURCES")

        for source in result["sources"]:

            print(
                f"\n[{source['market']} • "
                f"{source['timestamp']}] "
                f"{source['expert']}"
            )

            print(f'"{source["quote"]}"')