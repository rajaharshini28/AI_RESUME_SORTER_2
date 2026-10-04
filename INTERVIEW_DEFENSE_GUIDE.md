# 🎓 Master Technical Interview Defense Guide
## AI Resume-to-Job Matching and Ranking System

This document provides complete, line-by-line technical defense answers for all 41+ interview questions expected in a technical AI / Data Engineering / Full Stack interview.

---

### Q1. Explain your project.
- **Simple Answer**: I built an AI-assisted Resume Sorter and Ranking Application using Flask, Sentence Transformers, and SQLite. It parses PDF/DOCX resumes, extracts candidate information, converts document text into 384-dimensional dense semantic vectors using a local language model, and ranks candidates based on an explainable weighted score.
- **Technical Explanation**: The application uses a modular architecture: PyMuPDF and python-docx extract raw text, which undergoes whitespace and syntax-preserving normalization. The text is passed to `sentence-transformers/all-MiniLM-L6-v2` to generate 384-dimensional dense embeddings for both the job description and candidate resumes. Cosine similarity computes vector alignment, which is combined with explicit regex skill matching ($25\%$), experience heuristics ($10\%$), and education checks ($5\%$) to form a composite score stored in SQLite.
- **Likely Follow-Up Questions**: 
  - How did you choose the model?
  - How does cosine similarity work mathematically?
- **What NOT to Say**: Do NOT say "I trained a machine learning model to predict who gets hired." (You used pre-trained embeddings for inference).

---

### Q2. What problem does it solve?
- **Simple Answer**: Traditional ATS systems rely on exact keyword matching, missing qualified candidates who use different phrasing or synonyms. My project solves this by using semantic AI embeddings to understand context and intent, paired with transparent scoring.
- **Technical Explanation**: Keyword ATS systems use lexical matching (e.g. TF-IDF or string search), which fails on vocabulary mismatch (e.g. "Machine Learning Engineer" vs "Predictive Modeling Specialist"). Dense vector embeddings map sentences into a high-dimensional continuous vector space where semantically similar concepts reside close to each other regardless of exact wording.
- **Likely Follow-Up Questions**: Can keyword matching still be useful alongside embeddings?
- **What NOT to Say**: Do NOT say "It completely eliminates recruiters and makes automated hiring decisions."

---

### Q3. Why Flask?
- **Simple Answer**: Flask is a lightweight Python web framework that allowed me to quickly construct a modular, clean MVC application without unnecessary boilerplate.
- **Technical Explanation**: Flask provides essential HTTP routing, request handling, session management, and Jinja2 templating with a minimal footprint. Its WSGI compliance and decoupled design allowed clean integration of PyTorch/SentenceTransformers without framework overhead.
- **Likely Follow-Up Questions**: How did you structure your application services?
- **What NOT to Say**: Do NOT say "Flask is the best framework for heavy production enterprise systems."

---

### Q4. Why not FastAPI?
- **Simple Answer**: FastAPI is great for asynchronous REST APIs, but Flask was chosen because this project includes server-side HTML rendering (Jinja2) for a complete recruiter dashboard, aligning with my original resume scope.
- **Technical Explanation**: FastAPI relies on ASGI (`uvicorn`/`pydantic`) optimized for asynchronous microservices and API-first architectures. Since embedding generation with SentenceTransformers is CPU/GPU compute-bound (blocking CPU execution), async I/O doesn't inherently speed up vector encoding without a background task queue like Celery.
- **Likely Follow-Up Questions**: How would you transition this system to FastAPI in production?
- **What NOT to Say**: Do NOT say "FastAPI is slow" or "FastAPI doesn't support databases."

---

### Q5. Why SQLite?
- **Simple Answer**: SQLite is a serverless, zero-configuration database built into Python. It is ideal for local development, rapid prototyping, and demonstrating a clean relational schema.
- **Technical Explanation**: SQLite reads and writes directly to a single disk file using standard SQL. It supports ACID transactions, foreign key constraints (`PRAGMA foreign_keys = ON;`), and parameterized queries to prevent SQL injection, providing full relational capability without database server overhead.
- **Likely Follow-Up Questions**: How would SQLite perform under concurrent write access?
- **What NOT to Say**: Do NOT say "SQLite can easily handle enterprise traffic with millions of concurrent users."

---

### Q6. Why not PostgreSQL?
- **Simple Answer**: For a prototype/local project, PostgreSQL adds unnecessary installation and server administration overhead. SQLite handles our single-user recruiter workflow perfectly.
- **Technical Explanation**: PostgreSQL is a client-server RDBMS requiring daemon management, user role setup, and connection pooling (`psycopg2`/`SQLAlchemy`). While PostgreSQL excels in high-concurrency production environments (and supports `pgvector` for vector search), SQLite is optimal for local execution.
- **Likely Follow-Up Questions**: How would you migrate this project to PostgreSQL?
- **What NOT to Say**: Do NOT say "PostgreSQL is unnecessary for real systems."

---

### Q7. How does PDF parsing work?
- **Simple Answer**: PDF parsing extracts text streams, character positioning, and fonts embedded inside PDF objects.
- **Technical Explanation**: PDF files store content as vector graphics, font dictionaries, and text placement commands (`Tj`/`TJ` operators in PDF binary specification). Libraries like PyMuPDF traverse the document page tree, parse font encoding maps (ToUnicode CMap), and reconstruct line strings in reading order.
- **Likely Follow-Up Questions**: What happens if the PDF is scanned?
- **What NOT to Say**: Do NOT say "PDF parsing automatically performs optical character recognition (OCR)."

---

### Q8. Why PyMuPDF / PyPDF?
- **Simple Answer**: PyMuPDF (built on the MuPDF C engine) is extremely fast and accurate at text extraction, while PyPDF provides a pure-Python fallback.
- **Technical Explanation**: PyMuPDF (`fitz`) wraps the C-based MuPDF renderer, delivering up to $10\times - 50\times$ faster extraction rates compared to pure Python parsers, with superior handling of multi-column layouts and custom font encodings.
- **Likely Follow-Up Questions**: How do you detect if a PDF extraction failed?
- **What NOT to Say**: Do NOT say "PyMuPDF works on images without OCR."

---

### Q9. Why python-docx?
- **Simple Answer**: `python-docx` is the standard Python library for reading OpenXML (`.docx`) Word documents.
- **Technical Explanation**: A `.docx` file is a zipped archive containing XML files (`word/document.xml`). `python-docx` parses the XML DOM tree, extracting text nodes inside paragraph (`<w:p>`) and table cell (`<w:tc>`) tags.
- **Likely Follow-Up Questions**: Do you extract text inside headers or text boxes?
- **What NOT to Say**: Do NOT say "python-docx works on old binary `.doc` files." (It requires `.docx` OpenXML).

---

### Q10. What is document parsing?
- **Simple Answer**: Document parsing is converting unstructured binary files (PDFs, DOCX) into clean plain text strings that computer algorithms can analyze.
- **Technical Explanation**: It involves inspecting file metadata, decoding character encodings, navigating document object models (DOM or page trees), and outputting normalized plain text while removing layout formatting scripts.
- **Likely Follow-Up Questions**: What are the common challenges in parsing multi-column resumes?
- **What NOT to Say**: Do NOT say "Parsing means understanding the meaning of text." (That is NLP/Extraction).

---

### Q11. What is text preprocessing?
- **Simple Answer**: Text preprocessing cleans raw text by removing noise, standardizing whitespace, and normalizing encoding artifacts.
- **Technical Explanation**: Preprocessing prepares raw text for downstream NLP. In our system, we use two strategies:
  1. *For Embeddings*: Normalize unicode & whitespace while retaining casing, punctuation, and stopwords for transformer syntax.
  2. *For Rule Extraction*: Standardize text while preserving technical syntax like `C++`, `C#`, and `.NET`.
- **Likely Follow-Up Questions**: Why did you NOT remove stopwords before embedding generation?
- **What NOT to Say**: Do NOT say "I stripped all punctuation and lowercased everything before passing text to Sentence Transformers."

---

### Q12. What are embeddings?
- **Simple Answer**: Embeddings are numerical vector representations of text where semantically similar words or sentences are converted into vectors that sit close to each other in vector space.
- **Technical Explanation**: A sentence embedding maps a sequence of tokens to a fixed-length continuous vector $\mathbf{v} \in \mathbb{R}^d$ (in our case $d = 384$). Dense neural networks (Transformers) capture contextual, semantic, and syntactic relationships, enabling linear vector math to evaluate semantic proximity.
- **Likely Follow-Up Questions**: What is the difference between word embeddings (Word2Vec) and sentence embeddings?
- **What NOT to Say**: Do NOT say "Embeddings are just word count tables like Bag-of-Words."

---

### Q13. Why embeddings?
- **Simple Answer**: Embeddings capture deep conceptual meaning rather than relying on exact word matches.
- **Technical Explanation**: Exact keyword matching fails when applicants express qualifications using different vocabulary (e.g., "built REST APIs in Flask" vs "web backend engineering"). Embeddings map both expressions to adjacent positions in vector space, enabling semantic scoring.
- **Likely Follow-Up Questions**: Can embeddings hallucinate?
- **What NOT to Say**: Do NOT say "Embeddings are 100% accurate and never make mistakes."

---

### Q14. What is a Sentence Transformer?
- **Simple Answer**: A Sentence Transformer is a neural network model fine-tuned using Siamese Network structures to generate meaningful sentence-level vector embeddings.
- **Technical Explanation**: Standard BERT models output token-level representations that require expensive cross-encoder computations ($O(N^2)$ pairs). Sentence-BERT (SBERT) uses a Siamese/Triplet network structure with mean-pooling to derive semantically meaningful fixed-length sentence embeddings that can be compared instantly using cosine similarity.
- **Likely Follow-Up Questions**: Who introduced SBERT? (Reimers & Gurevych, 2019).
- **What NOT to Say**: Do NOT say "Sentence Transformer is a simple rule-based script."

---

### Q15. Why `all-MiniLM-L6-v2`?
- **Simple Answer**: `all-MiniLM-L6-v2` is a lightweight, high-performance model that generates 384-dimensional vectors fast enough to run locally on CPU without needing a GPU.
- **Technical Explanation**: `all-MiniLM-L6-v2` is distilled from larger transformer architectures. It has 6 transformer layers, 22.7 million parameters, outputs 384-d embeddings, and disk size is only ~90MB. It achieves competitive semantic benchmark scores (e.g. STSb) while performing vector inference in milliseconds on standard CPU.
- **Likely Follow-Up Questions**: How does 384 dimensions compare to 768 or 1536 dimensions?
- **What NOT to Say**: Do NOT say "It is the largest and most complex LLM available."

---

### Q16. What is cosine similarity?
- **Simple Answer**: Cosine similarity measures the cosine of the angle between two vectors in multi-dimensional space, indicating how similar their direction is regardless of vector length.
- **Technical Explanation**: Formally defined as:
$$\text{Cosine Similarity}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} = \frac{\sum_{i=1}^{d} u_i v_i}{\sqrt{\sum_{i=1}^{d} u_i^2} \sqrt{\sum_{i=1}^{d} v_i^2}}$$
Values range from $-1.0$ (opposite directions) to $1.0$ (identical direction).
- **Likely Follow-Up Questions**: Why use Cosine Similarity instead of Euclidean Distance?
- **What NOT to Say**: Do NOT say "Cosine similarity measures the physical distance between two points." (That is Euclidean distance).

---

### Q17. Why cosine similarity?
- **Simple Answer**: Cosine similarity evaluates direction rather than vector magnitude, meaning candidate score isn't artificially inflated just because a resume is longer.
- **Technical Explanation**: Longer documents contain higher word counts, which expands vector magnitude in Euclidean space. Cosine similarity normalizes vector lengths to unit length $\|\mathbf{u}\| = 1$, making comparisons magnitude-invariant and focused purely on semantic orientation.
- **Likely Follow-Up Questions**: If embeddings are pre-normalized, what simplifies in the formula? ($\mathbf{u} \cdot \mathbf{v}$).
- **What NOT to Say**: Do NOT say "Cosine similarity measures exact string matching."

---

### Q18. What is semantic similarity?
- **Simple Answer**: Semantic similarity measures how close two texts are in meaning, even if they use completely different words.
- **Technical Explanation**: It assesses contextual equivalence across natural language sequences by projecting text into continuous vector representations trained on large-scale textual corpora.
- **Likely Follow-Up Questions**: Give an example of two sentences with high semantic similarity but zero keyword overlap.
- **What NOT to Say**: Do NOT say "Semantic similarity is counting matching letters."

---

### Q19. How is semantic similarity different from keyword matching?
- **Simple Answer**: Keyword matching checks for exact word hits; semantic similarity checks for conceptual overlap in meaning.
- **Technical Explanation**:
  - **Lexical/Keyword (e.g. BM25/TF-IDF)**: High precision, zero recall on synonyms. Fails on vocabulary mismatch.
  - **Semantic Similarity (Dense Embeddings)**: High recall on contextual intent and synonyms.
- **Likely Follow-Up Questions**: Why does our system combine BOTH embedding similarity and explicit skill matching?
- **What NOT to Say**: Do NOT say "Keyword matching is obsolete and should never be used."

---

### Q20. Is this supervised learning?
- **Simple Answer**: No. In our application, we are using a pre-trained embedding model for zero-shot inference, not training a supervised classifier on labeled hiring data.
- **Technical Explanation**: Supervised learning requires training on labeled target datasets $(X, y)$ (e.g. historical hired/rejected labels). Our system performs feature extraction and vector space distance computation (unsupervised vector inference).
- **Likely Follow-Up Questions**: Why didn't you train a supervised classifier on historical hiring data? (Avoid introducing historical hiring bias!).
- **What NOT to Say**: Do NOT say "Yes, I trained a supervised model on 10,000 resumes."

---

### Q21. Did you train the model?
- **Simple Answer**: No. I used the pre-trained `all-MiniLM-L6-v2` model for inference.
- **Technical Explanation**: Pre-training a transformer requires billions of text tokens and hundreds of GPU hours. We consume the model weights fine-tuned on sentence pairs (NLI / STSb) via `sentence-transformers` for zero-shot embedding inference.
- **Likely Follow-Up Questions**: How could you fine-tune this model if you had labeled domain data?
- **What NOT to Say**: Do NOT say "Yes, I trained Sentence Transformer from scratch."

---

### Q22. What is inference?
- **Simple Answer**: Inference is running new input data through a pre-trained machine learning model to get predictions or vector outputs without updating model weights.
- **Technical Explanation**: During inference, input text passes forward through frozen model weights (forward pass), executing matrix multiplications and self-attention operations to produce embeddings without backpropagation or weight updates.
- **Likely Follow-Up Questions**: What is the time complexity of inference for a transformer?
- **What NOT to Say**: Do NOT say "Inference means training the model live on user uploads."

---

### Q23. Why not TF-IDF?
- **Simple Answer**: TF-IDF only measures word frequency and cannot understand synonyms, context, or semantic relationships.
- **Technical Explanation**: TF-IDF creates sparse vectors of vocabulary size $|V|$. It treats every word as orthogonal (independent), meaning "developer" and "programmer" have a dot product of zero. Dense embeddings project words into shared continuous space where related concepts have high dot products.
- **Likely Follow-Up Questions**: Where might TF-IDF still be useful?
- **What NOT to Say**: Do NOT say "TF-IDF is a deep learning model."

---

### Q24. Why not BERT directly?
- **Simple Answer**: Standard BERT requires comparing sentences in pairs, which takes thousands of calculations per resume search. Sentence Transformers compute individual vectors once.
- **Technical Explanation**: Standard BERT uses a cross-encoder architecture. To rank $N = 1000$ resumes against a job description, BERT must process 1000 pairs through 12 layers of self-attention ($O(N)$ forward passes through full BERT). SBERT uses a bi-encoder: it pre-computes 384d vectors once and compares them via dot product in microseconds.
- **Likely Follow-Up Questions**: What is the difference between Bi-Encoder and Cross-Encoder?
- **What NOT to Say**: Do NOT say "BERT cannot generate embeddings."

---

### Q25. What is the difference between BERT and Sentence Transformers?
- **Simple Answer**: BERT outputs token embeddings designed for fine-tuning; Sentence Transformers fine-tune BERT with pooling layers to produce single sentence-level vectors for fast distance math.
- **Technical Explanation**: BERT's default `[CLS]` token or mean token outputs without fine-tuning produce poor sentence embeddings (worse than GloVe averages). Sentence Transformers use Siamese training on NLI datasets to optimize cosine similarity in vector space.
- **Likely Follow-Up Questions**: What pooling strategy does `all-MiniLM-L6-v2` use? (Mean Pooling).
- **What NOT to Say**: Do NOT say "BERT and Sentence Transformers are completely unrelated."

---

### Q26. How do you calculate the final score?
- **Simple Answer**: I use an explainable weighted formula combining semantic similarity ($60\%$), explicit skill match ($25\%$), experience ($10\%$), and education ($5\%$).
- **Technical Explanation**:
$$\text{Final Score} = 0.60(S_{\text{semantic}}) + 0.25(S_{\text{skill}}) + 0.10(S_{\text{exp}}) + 0.05(S_{\text{edu}})$$
All sub-scores are normalized to $[0, 100]$.
- **Likely Follow-Up Questions**: Are these weights hardcoded or configurable?
- **What NOT to Say**: Do NOT say "The weights were calculated by an AI algorithm." (They are transparent architectural design choices).

---

### Q27. Why did you choose these weights?
- **Simple Answer**: The weights prioritize semantic fit and core technical skills while ensuring experience and education act as supportive factors.
- **Technical Explanation**: In modern technical recruitment, role relevance ($60\%$) and skill coverage ($25\%$) are primary indicators of candidate capability, while degree level ($5\%$) and years ($10\%$) serve as baseline prerequisites. The weights are configurable in `config.py`.
- **Likely Follow-Up Questions**: How could you optimize these weights empirically?
- **What NOT to Say**: Do NOT say "These weights are mathematically proven to be perfect for every company."

---

### Q28. How do you prevent bias?
- **Simple Answer**: The system strictly excludes non-job demographic information like gender, age, race, photos, and address from candidate extraction and ranking.
- **Technical Explanation**: By enforcing demographic neutrality in `services/information_extractor.py`, ranking depends strictly on candidate skills, experience, education, and semantic resume content. Furthermore, using zero-shot vector matching rather than biased historical hiring models prevents reinforcing historical workplace bias.
- **Likely Follow-Up Questions**: Can language style bias still exist in resumes?
- **What NOT to Say**: Do NOT say "Our AI system has 0% bias and is completely flawless."

---

### Q29. What happens with scanned PDFs?
- **Simple Answer**: Scanned PDFs contain images rather than selectable text. My parser detects when extracted text is empty and returns an informative error stating OCR is required.
- **Technical Explanation**: Text-based PDFs contain font glyph maps and text operators. Image PDFs contain bitmap images inside PDF streams. `services/document_parser.py` checks character count after parsing; if $<20$ characters are extracted, it raises a `ParsingError` explaining that OCR (Tesseract / AWS Textract) is required.
- **Likely Follow-Up Questions**: How would you add OCR to this pipeline?
- **What NOT to Say**: Do NOT say "My PDF parser automatically converts scanned images to text."

---

### Q30. How do you handle missing information?
- **Simple Answer**: Extractor functions return safe default values (e.g. "Not Provided", 0.0 years) rather than throwing errors or crashing.
- **Technical Explanation**: Safe extraction routines fall back gracefully. If an email is absent, `extract_email()` returns `"Not Provided"`. If experience years cannot be detected, it defaults to `0.0`. Ranking sub-scores handle default values without throwing `TypeError` or `NullPointerException`.
- **Likely Follow-Up Questions**: How does missing email affect ranking score? (It doesn't affect ranking score, preserving fairness).
- **What NOT to Say**: Do NOT say "The app crashes if a resume is missing a phone number."

---

### Q31. How do you handle duplicate resumes?
- **Simple Answer**: On file upload, filenames are sanitized using `secure_filename()` and appended with unique counter increments if identical file names exist.
- **Technical Explanation**: `app.py` checks `os.path.exists(save_path)`. If a duplicate filename occurs, it appends `_1`, `_2` before saving to disk. Each upload creates a distinct record in SQLite with its own timestamp.
- **Likely Follow-Up Questions**: How would you detect duplicate resume contents (hash comparison)?
- **What NOT to Say**: Do NOT say "Duplicate files overwrite existing candidate records in the database."

---

### Q32. What if the embedding model fails?
- **Simple Answer**: The model is encapsulated in a singleton service with exception handling to log errors cleanly and return safe fallback scores.
- **Technical Explanation**: `EmbeddingService` checks model initialization status. If model loading fails, it catches the exception, logs diagnostic details, and prevents application startup crashes.
- **Likely Follow-Up Questions**: How would you implement a fallback encoder?
- **What NOT to Say**: Do NOT say "The server crashes and displays raw tracebacks to users."

---

### Q33. What if two candidates get the same score?
- **Simple Answer**: Candidates with identical scores are ordered deterministically by submission timestamp and candidate ID in SQLite queries.
- **Technical Explanation**: SQLite handles tie-breaking via `ORDER BY final_score DESC, candidate_id ASC`.
- **Likely Follow-Up Questions**: How would you display tie-break sub-score details?
- **What NOT to Say**: Do NOT say "The system picks one randomly and deletes the other."

---

### Q34. What happens if there are 10,000 resumes?
- **Simple Answer**: For 10,000 resumes, processing sequentially on request would freeze the web thread. I would move extraction to a background queue (Celery/Redis) and use a vector index (FAISS/ChromaDB).
- **Technical Explanation**: In-memory linear scan of 10,000 embeddings requires 10,000 vector dot products ($O(N)$). While dot products are fast, parsing and encoding 10,000 PDF documents synchronously exceeds HTTP gateway timeouts. An asynchronous worker task architecture is necessary.
- **Likely Follow-Up Questions**: How does FAISS speed up vector search? (Approximate Nearest Neighbors - ANN).
- **What NOT to Say**: Do NOT say "Flask can easily process 10,000 PDF files synchronously in 1 second."

---

### Q35. How would you scale it?
- **Simple Answer**: Separate file processing into worker nodes (Celery/Redis), store files on object storage (AWS S3), migrate SQLite to PostgreSQL, and index embeddings using a vector database (FAISS/ChromaDB).
- **Technical Explanation**:
  1. *Ingestion*: Decouple web server from document parsing using asynchronous task workers (Celery + Redis/RabbitMQ).
  2. *Storage*: Store raw resumes in S3; store structured metadata in PostgreSQL.
  3. *Search*: Index 384d embeddings using FAISS HNSW index for sub-millisecond similarity search.
- **Likely Follow-Up Questions**: What is an HNSW index? (Hierarchical Navigable Small World graph).
- **What NOT to Say**: Do NOT say "I would just buy a bigger CPU."

---

### Q36. How would you deploy it on AWS?
- **Simple Answer**: Containerize the app using Docker, deploy on AWS ECS or App Runner, store files in S3, use AWS RDS for PostgreSQL, and manage domain routing with Application Load Balancer.
- **Technical Explanation**:
  - **Frontend/Backend**: Package Flask app into Docker image served via Gunicorn WSGI.
  - **Compute**: AWS ECS (Fargate) for container orchestration with auto-scaling.
  - **Database**: Managed AWS RDS PostgreSQL instance.
  - **File Storage**: AWS S3 with pre-signed upload URLs.
- **Likely Follow-Up Questions**: How would you secure S3 resume buckets?
- **What NOT to Say**: Do NOT say "I would copy-paste files onto a single EC2 instance without Docker."

---

### Q37. How would you replace SQLite?
- **Simple Answer**: Replace SQLite by updating the database configuration in `config.py` and using an ORM like `SQLAlchemy` connected to PostgreSQL.
- **Technical Explanation**: Refactor `models/database.py` to use SQLAlchemy ORM models. Replace `sqlite3` connection strings with `postgresql://user:password@localhost:5432/dbname`.
- **Likely Follow-Up Questions**: Would schema definitions change significantly?
- **What NOT to Say**: Do NOT say "I would have to rewrite the entire application from scratch."

---

### Q38. How would you introduce a vector database?
- **Simple Answer**: Use ChromaDB, FAISS, or Pinecone to store candidate embeddings and perform fast Approximate Nearest Neighbor (ANN) vector searches.
- **Technical Explanation**: Instead of storing embeddings as raw blobs or recalculating cosine similarity linearly across all database rows, push embeddings to ChromaDB/FAISS. When a recruiter submits a job description, query `vector_db.query(job_embedding, k=50)` to retrieve top candidate IDs in $O(\log N)$ time.
- **Likely Follow-Up Questions**: What is the difference between exact KNN search and ANN search?
- **What NOT to Say**: Do NOT say "Vector databases replace relational databases completely."

---

### Q39. How would you monitor the system?
- **Simple Answer**: Log application metrics, track model inference latency, monitor error rates using Prometheus/Grafana or Sentry, and log structured data.
- **Technical Explanation**: Instrument Flask routes with Prometheus metrics (`request_duration_seconds`, `parsing_errors_total`). Monitor CPU/memory usage of SentenceTransformers model inference. Capture unhandled exceptions with Sentry.
- **Likely Follow-Up Questions**: What metrics indicate model bottleneck?
- **What NOT to Say**: Do NOT say "I don't need monitoring if there are no syntax errors."

---

### Q40. What are the limitations?
- **Simple Answer**: Limitations include lack of built-in OCR for scanned PDFs, reliance on zero-shot pre-trained embeddings without domain fine-tuning, and regex reliance for skill taxonomy.
- **Technical Explanation**:
  1. *Scanned Documents*: Requires OCR pipeline integration (Tesseract).
  2. *Domain Specificity*: `all-MiniLM-L6-v2` is a general-purpose model; specialized industry jargon (e.g. niche medical/legal roles) benefits from domain fine-tuning.
  3. *Skill Taxonomy*: Unlisted novel tech stacks require updating the skill dictionary.
- **Likely Follow-Up Questions**: How would you address these limitations in version 2?
- **What NOT to Say**: Do NOT say "There are no limitations, the system is 100% perfect."

---

### Q41. What would you improve next?
- **Simple Answer**: Add OCR support for scanned resumes, implement vector search with ChromaDB, support custom scoring weight sliders in the UI, and enable export of candidate ranking reports to PDF/Excel.
- **Technical Explanation**:
  1. Integrate Tesseract OCR fallback for scanned PDF documents.
  2. Implement ChromaDB for sub-millisecond vector indexing.
  3. Add UI controls allowing recruiters to dynamically adjust weight ratios (e.g., increase skill weight to $50\%$).
  4. Export candidate evaluation reports to CSV/Excel formats.
- **Likely Follow-Up Questions**: Which improvement would yield the highest user impact?
- **What NOT to Say**: Do NOT say "I would re-architect the whole project in a different language."
