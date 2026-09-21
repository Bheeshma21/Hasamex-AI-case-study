from sentence_transformers import SentenceTransformer
import faiss


try:
    from .parser import load_all_transcripts
except ImportError:
    from parser import load_all_transcripts


class TranscriptRetriever:
    """
    Semantic retrieval engine for the Hasamex expert-call transcripts.

    Every retrieved passage preserves:
    - expert
    - role
    - market
    - timestamp
    - speaker
    - exact transcript text

    The retriever supports both global semantic search and
    market-balanced cross-call retrieval.
    """

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.transcripts = load_all_transcripts()
        self.documents = []

        self._prepare_documents()
        self._build_index()

    def _prepare_documents(self):
        """
        Convert transcript segments into searchable documents while
        preserving their original metadata.
        """

        for transcript in self.transcripts:
            for segment in transcript["segments"]:

                embedding_text = (
                    f"Market: {segment['market']}. "
                    f"Expert: {segment['expert']}. "
                    f"Role: {segment['role']}. "
                    f"Speaker: {segment['speaker']}. "
                    f"{segment['text']}"
                )

                self.documents.append(
                    {
                        **segment,
                        "embedding_text": embedding_text,
                    }
                )

    def _build_index(self):
        """
        Generate embeddings and create a FAISS cosine-similarity index.
        """

        texts = [
            document["embedding_text"]
            for document in self.documents
        ]

        if not texts:
            raise ValueError(
                "No transcript segments were found to index."
            )

        print(f"Embedding {len(texts)} transcript segments...")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")

        # Normalize vectors so inner product behaves like cosine similarity.
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        print(
            f"FAISS index ready: "
            f"{self.index.ntotal} searchable segments."
        )

    def search(
        self,
        query,
        top_k=5,
        market=None,
        expert_only=True,
    ):
        """
        Semantic search across transcript segments.

        Parameters
        ----------
        query:
            User/research question.

        top_k:
            Maximum number of results.

        market:
            Optional exact market filter.

        expert_only:
            When True, interviewer questions are excluded.
        """

        if not query or not query.strip():
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")

        faiss.normalize_L2(query_embedding)

        # Search broadly before filters are applied.
        # Searching the whole tiny corpus gives reliable market filtering.
        search_size = len(self.documents)

        scores, indices = self.index.search(
            query_embedding,
            search_size,
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index < 0:
                continue

            document = self.documents[index]

            # Remove interviewer questions from evidence.
            if (
                expert_only
                and document["speaker"].strip().lower() == "interviewer"
            ):
                continue

            # Optional market filter.
            if market:
                if (
                    document["market"].strip().lower()
                    != market.strip().lower()
                ):
                    continue

            result = {
                "expert": document["expert"],
                "role": document["role"],
                "market": document["market"],
                "timestamp": document["timestamp"],
                "speaker": document["speaker"],
                "text": document["text"],
                "source_file": document["source_file"],
                "score": round(float(score), 4),
            }

            results.append(result)

            if len(results) >= top_k:
                break

        return results

    def search_across_markets(
        self,
        query,
        per_market=4,
    ):
        """
        Retrieve evidence independently from every market.

        This is important for cross-call analysis because ordinary
        global top-K semantic search can allow one market to dominate
        the retrieved context.

        Example:
            France         -> top 4 relevant passages
            Germany        -> top 4 relevant passages
            United Kingdom -> top 4 relevant passages
        """

        markets = sorted(
            {
                document["market"]
                for document in self.documents
            }
        )

        all_results = []

        for market in markets:

            market_results = self.search(
                query=query,
                top_k=per_market,
                market=market,
                expert_only=True,
            )

            all_results.extend(market_results)

        return all_results

    def get_markets(self):
        """
        Return all markets represented in the transcript collection.
        """

        return sorted(
            {
                document["market"]
                for document in self.documents
            }
        )

    def get_all_expert_segments(self):
        """
        Return every expert statement.

        Useful for deterministic transcript exploration or when the
        complete small corpus is required.
        """

        results = []

        for document in self.documents:

            if document["speaker"].strip().lower() == "interviewer":
                continue

            results.append(
                {
                    "expert": document["expert"],
                    "role": document["role"],
                    "market": document["market"],
                    "timestamp": document["timestamp"],
                    "speaker": document["speaker"],
                    "text": document["text"],
                    "source_file": document["source_file"],
                }
            )

        return results


if __name__ == "__main__":

    retriever = TranscriptRetriever()

    print("\n" + "=" * 70)
    print("MARKET-BALANCED RETRIEVAL TEST")
    print("=" * 70)

    test_queries = [
        "What are the main barriers to robotic surgery adoption?",
        "How important are ROI and hospital budgets?",
        "What growth is expected over the next three to five years?",
        "How long does purchasing a robotic system take?",
    ]

    for query in test_queries:

        print(f"\nQUESTION: {query}")
        print("-" * 70)

        results = retriever.search_across_markets(
            query,
            per_market=2,
        )

        for number, result in enumerate(results, start=1):

            print(
                f"\n{number}. "
                f"{result['expert']} | "
                f"{result['market']} | "
                f"{result['timestamp']} | "
                f"Score: {result['score']}"
            )

            print(f'"{result["text"]}"')