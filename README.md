# Artificial_Intelligence_Ecosystem

# High Life Rag System -- README

## Project Overview
This project implements a Retrieval-Augmented Generation (RAG) system designed to answer questions about the 2018 film High Life using text extracted from the film's Wikipedia article. The system performs:
- document loading 
- chunking
- embedding
- FAISS vector search
- cross-encoder re-ranking
- GPT-based answer generation
The selected documemt provides plot details, character arcs, and thematic descriptions that serve as the knowledge base for all retrieval-grounded answers.

---

## Selected Document Summary 
The selected document is the full Wikipedia article for High Life(2018), a science-fiction film by Claire Denis. It covers the film's nonlinear plot,
the doomed space mission involving death-row inmates, the psychological tension aboard the ship, and the relationship between Monte (Robert Pattinson) and the infant Willow.

---

## RAG Questions and Answers

### 1. My Question:  What is the plot to High Life?

### RAG Answer: 
"High Life follows a group of criminals serving death sentences who are sent on a space mission to extract alternative energy from a black hole. As part of the mission, they become subjects of scientific experients led by a scientist nammed Dibs, who is obsessed with creating a child in space through artificial insemination, but so far has not succeeded. Sexual activity between prisoners is prohibited. The story unfolds in a lol-linear fashion, initially focusing on a man and a baby alone on the spacecraft, with flashbacks revealing the events that led to their situation and exploring themes of human nature, survival, and despair as they draw closer to the black hole.

### 2. My Question: What events lead to Monte and the baby being alone on the ship?

### RAG Answer:
"Monte and the baby, Willow, end up alone on the ship due to a series of tragic events involving the other crew members:

- Pregnant prisoner Elektra delivers a baby, who later dies, and Elektra herself also dies. The captian, Chandra, develops leukemia from radiation exposure, suffers a stroke, and is euthanized by Dibs.

- Male prisoner Ettore attempts to rape Boyse. During the struggle, Mink kills Ettore by stabbing him in the hallway.

- Dibs, the doctor, doubles the prisoners' sedative and rapes monte while he is sedated. She then uses monte's semen to inseminate Boyse, resulting in the birth of Willow. Monte is unaware he is her father.

- Boyse kills Nansen (the pilot) and tries to pilot the shuttle around the black hole herself, but the shuttle is destroyed and Boyse is killed by spaghettification.

- Mink attacks and severely injures Dibs, but is killed by Monte. Dibs tells Monte that Willow is his child, then she ejects herself into space, committing suicide.

- Tcherny, Monte's only friend, becomes depressed and eventually commits suicide. Monte buries Tcherny in the garden.

With all other adults dead, Monte is left as the sole survivor, raising the baby Willow alone on the ship."

### 3. My Question: How does the mission's purpose shape the crew's fate?

### RAG Answer:
"The mission's purpose--to use criminals as test subjects for extracting alternative energy from a black hole and for reproductive experients in space--directly shapes the crew's fate in several ways:

1.** Expendability and Experimentation:** Because the crew consists of death row inmates considered expendable, they are treated as guinea pigs by the scientist Dibs, who enforces strict sexual controls and subjects them to dangerous scientific experients. This lack of concern for their well-being creates an atmosphere of mistrust, isolation, and violence among the prisoners.

2.** Psychological Deterioration:** The mission's grim purpose and harsh conditions (sedation, sexual control, and forced participation in reproductive experiments) lead to the psychological breakdowns, deaths, and suicides among the crew.

3.** Failure and Death:** Attempts to achieve the mission's goal--both the scientific quest to harness black hole energy and Dibs' obsession with artficial reproduction--end in failure. Dibs' experiment to create a child in space succeeds only after she rapes Monte, but most attempts result in death (e.g., Elektra and her baby). Crew members die one by one due to violence, suicide, or the hazards of space.

4.** Inevitable Doom:** As the ship moves closer to the black hole, the mission's risk escalates. The crew is eventually whittled down to only Monte and the child, Willow, survivors shaped by the isolation and trauma of the mission. Their ultimate fate--to approach the black hole together, uncertain if they will survive--underscores how the mission's dangerous and exploitative purpose determines both the physical and psychological fate of everyone on board."

---

## Retrieval Quality Analysis

### Chunk Size
- A 500-character chunk_size preserved narrative flow and kept plot events intact.

- Smaller chunks caused fragmentation and reduced retrieval accuracy.

- 500 characters consistently returned all relevant plot segments.

### Chunk Overlap
- A 50-character overlap prevented semantic tearing at chunk boundries.

- Without overlap, key sentences were split across chunks.

- Larger overlaps increased cost without improving retrieval.

### Overall Retrieval Behavior
- The combination of chunk_size=500 and chunk_overlap=50 produced the most coherent retrieval.

- All three test questions returned 20/20 chunks, showing strong embedding alignment.

- Re-ranking ensured the most relevant chunks appeared first.

---

## Deep-Dive Questions & AI Answers 

### Q1. How does embedding dimensionally affect retrieval quality?
** AI Answer:**
 Embedding dimensionality determines how much semantic information each vector can store. Higher-dimensional embeddings capture more nuance, improving similarity search, but also increase memory and compute cost. The 768-dimensional vectors uaed here balance expressiveness and efficiency.

### Q2. Why does FAISS sometimes return imperfect matches?
** AI Answer:**
FAISS performs approximate nearest-neighbor search, meaning it finds vectors that are close in embedding space, not necessarily perfect semantic matches. Re-ranking corrects this by evaluating each chunk jointly with the question.

### Q3. What role does chunk overlap play in preserving meaning?
** AI Answer:**
Chunk overlap prevents important sentences from being split across boundries. Without overlap, retrieval may miss key context, especially in non linear narratives like High Life.

### Q4. How does the system prompt influence groundedness?
** AI Answer:**
The system prompt instructs the model to answer only using retrieved context and to avoid hallucination. This keeps answers anchored in the document.

### Q5. Why is re-ranking necessary if FAISS already returns top-k chunks?
** AI Answer:**
FAISS uses vector similarity, which is shallow. Re-ranking evaluates each chunk jointly with the question, producing a more accurate relevance score and improving final answer quality.














































