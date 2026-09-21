try:
    from .parser import load_all_transcripts, load_interview_guide
    from .ai_engine import AIEngine
except ImportError:
    from parser import load_all_transcripts, load_interview_guide
    from ai_engine import AIEngine


class CaseStudyAnalyzer:
    """
    High-level analysis layer for the Hasamex case study.

    Responsibilities:
    1. Answer the supplied interview guide.
    2. Identify common themes across calls.
    3. Identify differences in emphasis and genuine disagreements.
    4. Preserve verified transcript evidence for every analysis.
    """

    def __init__(self):
        self.engine = AIEngine()
        self.transcripts = load_all_transcripts()
        self.questions = load_interview_guide()

    # ---------------------------------------------------------
    # INTERVIEW GUIDE
    # ---------------------------------------------------------

    def analyze_interview_guide(self):
        """
        Answer every interview-guide question using balanced evidence
        from France, Germany and the United Kingdom.
        """

        results = []

        for number, question in enumerate(
            self.questions,
            start=1,
        ):

            enhanced_question = f"""
INTERVIEW GUIDE QUESTION:

{question}

Analyse this question across:
- France
- Germany
- United Kingdom

For each market:

1. Give a concise answer based only on transcript evidence.
2. Preserve any numerical qualifications exactly.
3. Identify meaningful similarities and differences.
4. Do not generalise a statement about selected centres or areas
   to the entire national market.
5. Do not invent missing information.
6. Do not claim that an expert did not discuss something simply
   because it was not retrieved.
7. Do not reproduce exact quotations in the narrative.

The application displays verified transcript quotations and
timestamps separately.
"""

            response = self.engine.ask(
                enhanced_question,
                top_k=15,
                balanced=True,
            )

            results.append(
                {
                    "number": number,
                    "question": question,
                    "answer": response["answer"],
                    "sources": response["sources"],
                }
            )

        return results

    # ---------------------------------------------------------
    # COMMON THEMES
    # ---------------------------------------------------------

    def analyze_themes(self):
        """
        Identify evidence-supported common themes across calls.
        """

        question = """
Analyse the France, Germany and United Kingdom robotic-surgery
expert calls and identify the most important common themes.

Focus specifically on:

- current adoption
- adoption barriers
- hospital budgets
- ROI and economics
- utilisation and procedure volume
- surgeon/staff training
- clinical outcomes
- expected growth
- purchasing decisions
- decision-making timelines

EVIDENCE RULES:

A theme may only be described as shared by all three markets when
the supplied evidence supports it for France, Germany and the
United Kingdom.

If evidence supports a theme in only two markets, explicitly say
that it is supported by those two markets.

Preserve numerical scope carefully.

For example:

"15-20 percent more procedures annually in some stronger centres"

must not become:

"the French market will grow 15-20 percent annually."

Likewise, a statement about "some areas" must not be converted into
a nationwide forecast.

Separate:

1. genuinely common themes
2. market-specific nuances
3. conditional forecasts

Do not invent information.

Do not reproduce exact quotations or timestamps in the narrative.
Verified evidence will be displayed separately by the application.
"""

        return self.engine.ask(
            question,
            top_k=18,
            balanced=True,
        )

    # ---------------------------------------------------------
    # DIFFERENCES / DISAGREEMENTS
    # ---------------------------------------------------------

    def analyze_disagreements(self):
        """
        Identify genuine contradictions, differences in emphasis,
        and market-specific differences without forcing disagreement.
        """

        question = """
Compare the France, Germany and United Kingdom robotic-surgery
expert calls.

Identify meaningful differences between the experts.

Classify each difference as one of:

1. DIFFERENCE IN EMPHASIS
   The experts broadly agree but place different weight on certain
   factors.

2. MARKET-SPECIFIC DIFFERENCE
   The experts describe different market circumstances, forecasts,
   procurement processes or adoption conditions.

3. GENUINE DISAGREEMENT
   Two experts make clearly incompatible claims about the same issue.

STRICT RULES:

Do not manufacture disagreement simply because Hasamex asks us to
identify disagreements.

A difference in emphasis is NOT a genuine disagreement.

Only use the label "genuine disagreement" when the evidence contains
clearly incompatible positions.

If there is no genuine contradiction in the evidence, explicitly
state that no clear genuine disagreement was identified.

IMPORTANT ABSENCE RULE:

Never state that an expert or market provided:

- "no forecast"
- "no view"
- "no opinion"
- "did not mention"
- "did not discuss"
- "did not provide"

or any similar absence claim merely because the relevant passage was
not retrieved.

If the supplied evidence is insufficient for one side of a
comparison, say:

"The retrieved evidence does not establish a comparison for this
point."

Do not turn missing retrieval evidence into a factual claim about
the complete transcript.

GROWTH FORECAST RULE:

Preserve the scope of every forecast.

France:
A forecast applying to "some stronger centres" must remain limited
to those stronger centres.

Germany:
A market-wide procedure-volume forecast must remain market-wide.

United Kingdom:
A forecast applying to "some areas" must remain limited to those
areas and preserve any stated conditions such as training expansion
or improved cost competitiveness.

Compare the experts across topics such as:

- economics versus clinical considerations
- capital budgets
- ROI
- utilisation
- training
- adoption patterns
- future growth
- procurement timelines

Do not reproduce exact quotations or timestamps in the narrative.
Verified transcript evidence is displayed separately.
"""

        return self.engine.ask(
            question,
            top_k=18,
            balanced=True,
        )

    # ---------------------------------------------------------
    # GENERAL Q&A
    # ---------------------------------------------------------

    def ask_transcripts(self, question):
        """
        Public method used by the future Streamlit application
        for user questions across all expert calls.
        """

        return self.engine.ask(
            question,
            top_k=15,
            balanced=True,
        )

    # ---------------------------------------------------------
    # BASIC SUMMARY INFORMATION
    # ---------------------------------------------------------

    def get_case_summary(self):
        """
        Return deterministic case-pack information for the UI.
        """

        experts = []

        total_segments = 0

        for transcript in self.transcripts:

            expert_segments = [
                segment
                for segment in transcript["segments"]
                if segment["speaker"].strip().lower()
                != "interviewer"
            ]

            total_segments += len(expert_segments)

            experts.append(
                {
                    "expert": transcript["expert"],
                    "role": transcript["role"],
                    "market": transcript["market"],
                    "source_file": transcript["source_file"],
                    "expert_statements": len(expert_segments),
                }
            )

        return {
            "transcript_count": len(self.transcripts),
            "question_count": len(self.questions),
            "expert_statement_count": total_segments,
            "experts": experts,
        }


# -------------------------------------------------------------
# TERMINAL TEST
# -------------------------------------------------------------

if __name__ == "__main__":

    analyzer = CaseStudyAnalyzer()

    print("\n" + "=" * 70)
    print("HASAMEX CROSS-CALL ANALYSIS TEST")
    print("=" * 70)

    # ---------------------------------------------------------
    # Case summary
    # ---------------------------------------------------------

    summary = analyzer.get_case_summary()

    print("\nCASE SUMMARY")
    print("-" * 70)

    print(
        f"Transcripts: {summary['transcript_count']}"
    )

    print(
        f"Interview questions: {summary['question_count']}"
    )

    print(
        f"Expert statements: "
        f"{summary['expert_statement_count']}"
    )

    for expert in summary["experts"]:

        print(
            f"\n{expert['expert']} | "
            f"{expert['role']} | "
            f"{expert['market']}"
        )

    # ---------------------------------------------------------
    # Common themes
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("COMMON THEMES")
    print("-" * 70)

    themes = analyzer.analyze_themes()

    print(themes["answer"])

    print("\nVERIFIED EVIDENCE")

    for source in themes["sources"]:

        print(
            f"\n{source['market']} | "
            f"{source['expert']} | "
            f"{source['timestamp']}"
        )

        print(
            f'"{source["quote"]}"'
        )

    # ---------------------------------------------------------
    # Differences / disagreements
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("DISAGREEMENTS / DIFFERENCES")
    print("-" * 70)

    differences = analyzer.analyze_disagreements()

    print(differences["answer"])

    print("\nVERIFIED EVIDENCE")

    for source in differences["sources"]:

        print(
            f"\n{source['market']} | "
            f"{source['expert']} | "
            f"{source['timestamp']}"
        )

        print(
            f'"{source["quote"]}"'
        )