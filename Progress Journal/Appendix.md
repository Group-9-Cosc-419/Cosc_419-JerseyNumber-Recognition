# Appendix

## Individual Contributions

### Aaditya Golash

# Aaditya

## **Individual Contribution Log 1**

**Name:** Aaditya Golash  
**Week:** Week 1 (Feb 13 – Feb 21, 2026\)

---

### **Current Tasks**

* **Task 1: Technical Infrastructure Setup** – Configure initial GitHub repository, establish branch protection (2 reviews required), and integrate Discord webhooks for real-time team updates.  
* **Task 2: Literature Review & Research** – Conduct in-depth research on the Keyframe Identification (KfID) module based on the Balaji et al. (2023) paper.  
* **Task 3: Experimental Validation** – Execute baseline model runs on Google Colab and document results/limitations.  
* **Task 4: Proposal Development (Sections 2 & 5\)** – Draft the Literature Review, Replicated Results, Experiment Design, and Evaluation Metrics.

---

### **Progress Update**

**Status:** In-Progress

| Task | Status | Evidence (commit, file, PR, screenshot) |
| :---- | :---- | :---- |
| **Task 1** | Completed | GitHub Repo established; branch protection & webhooks active. |
| **Task 2** | Completed | Research presentation on KfID and digit-wise loss submitted. |
| **Task 3** | Completed | Successful Colab execution logs shared with the team. |
| **Task 4** | In-Progress | Drafts for Section 2 (Lit Review) and Section 5 (Metrics) initiated. |

---

### **Description (What happened?)**

This week focused on transitioning from initial research to project formalization. I handled the initial technical setup, including repository management, issue assignment via the Kanban board, and branch protection to ensure code integrity. After the first meeting, I selected the **Balaji et al. (2023)** paper for deep research, identifying the **KfID module** as a critical enhancement to filter noisy video tracklets (motion blur and occlusions).

During Meeting 2, the team presented individual pipeline ideas. I advocated for a system using **digit-wise multi-task loss** to address the model's failure on unseen jersey numbers by predicting tens and ones separately. Following a team vote, we decided to **pivot to a new project proposal repository** and adopt **Leila’s pipeline**, which combines my work on KfID, Enock’s work, and her own architectural improvements. I documented our progress in **Meeting Log 3** and began drafting the formal proposal sections I am responsible for (Sections 2 and 5).

---

### **Reflection (What did you learn?)**

I learned that sports video analytics are significantly affected by "tracklet noise," such as motion blur and occlusion. Hard-filtering frames using a KfID module can lead to a massive **\~38% relative accuracy increase** compared to baselines. I also gained critical insight into an **MPS kernel bug on Apple Silicon**; I discovered that tensors must be made **contiguous** at initialization to prevent the Adam optimizer from failing silently during training. This technical hurdle reinforced the importance of using **Google Colab** for consistent experimental results across the team.

---

### **Analysis (Why did it happen this way?)**

The decision to use a **digit-wise multi-task loss** was made because standard holistic classifiers generalize poorly to numbers not seen in the training set. We pivoted to a new repository and a combined pipeline because the individual proposals shared complementary strengths: KfID handles frame-level noise, while multi-task heads address structural digit complexity.

---

### **Conclusions (What insights did you gain?)**

The most significant insight was that **pre-processing is as critical as the model architecture**; passing raw tracklets to a temporal network without filtering is often a "dead end". Additionally, I realized that while state-of-the-art results are impressive, local replication is often **"difficult to run"** due to environment-specific hardware bugs like the MPS issue.

---

### **Next Week Goals (Action Plan)**

* **Finalize Section 2:** Complete the summaries of related work and document the replicated results of the baseline model.  
* **Complete Section 5:** Detail the hardware/software setup and define metrics like **Top-1/Top-5 Accuracy**, Precision, Recall, and F1-score.  
* **Pipeline Implementation:** Help set up the consolidated architecture in the newly established project repository.

---

---

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## **Individual Contribution Log 2**

**Name:** Aaditya Golash  
**Week:** Week 2 (Feb 22 \- Feb 28, 2026\)

---

### **Current Tasks**

* **Task 1: Section 2 Completion** \- Finalize my assigned part of Section 2 in the proposal draft.  
* **Task 2: Section 5 Completion** \- Finalize my assigned part of Section 5 in the proposal draft.  
* **Task 3: Draft Finalization and Peer Review** \- Review teammates' sections and help finalize one complete draft.  
* **Task 4: Transition Planning** \- Prepare for pipeline implementation and divide coding tasks for next week.

---

### **Progress Update**

**Status:** In-Progress

| Task | Status | Evidence (commit, file, PR, screenshot) |
| :---- | :---- | :---- |
| **Task 1** | Completed | My Section 2 part was completed on Feb 22, 2026\. |
| **Task 2** | Completed | My Section 5 part was completed on Feb 23, 2026\. |
| **Task 3** | In-Progress | Team meeting held on Feb 24, 2026 (5:00 PM-5:30 PM) to finalize draft direction and review all members' parts. |
| **Task 4** | Planned | Next team meeting set for Feb 25, 2026 at 7:30 PM; full document targeted for submission readiness on Feb 26, 2026\. |

---

### **Description (What happened?)**

On **Feb 22, 2026**, I completed my assigned contribution for **Section 2**. On **Feb 23, 2026**, I completed my assigned contribution for **Section 5**.

During our team meeting on **Feb 24, 2026 (5:00 PM-5:30 PM)**, we decided to focus on finalizing the full draft and reviewing everyone else's sections for consistency, clarity, and completeness. We also aligned on the remaining timeline: a follow-up meeting on **Feb 25, 2026 at 7:30 PM**, and having the final document ready for submission by **Feb 26, 2026**.

---

### **Reflection (What did you learn?)**

I learned that finishing my own sections early made it easier to spend time on cross-review and improve the overall quality of the proposal. I also saw that short, focused team meetings helped us make clear decisions quickly and keep everyone synchronized on deadlines.

---

### **Analysis (Why did it happen this way?)**

This sequence worked because we split work by sections first, then shifted to team-level review once individual writing was done. Completing Sections 2 and 5 on Feb 22-23 created enough buffer for joint revision before the submission deadline.

---

### **Conclusions (What insights did you gain?)**

The main insight is that proposal quality improves when individual ownership is combined with structured peer review. Early completion of assigned sections reduced last-minute risk and gave the team time to unify writing style and technical clarity.

---

### **Next Week Goals (Action Plan)**

* **Start Pipeline Work:** Begin implementing the agreed pipeline in code.  
* **Divide Coding Tasks:** Assign clear implementation responsibilities across team members.  
* **Set Development Workflow:** Establish milestones, branches, and check-in points for coding progress.

---

---

## 

## **Individual Contribution Log 3**

**Name:** Aaditya Golash  
**Week:** Week 3 (March 1 \-March 7, 2026\)

---

### **Current Tasks**

* **Task 1: Evaluate Koshkina & Elder (2024) baseline pipeline.**   
* **Task 2: Analyze baseline error distribution (1-vs-2 digit confusion).**  
* **Task 3: Conceptualize Top-K frame filtering logic. T**  
* **Task 4: Outline a multi-task structured learning architecture.**

---

### **Progress Update**

**Status:** Completed

| Task | Status | Evidence (commit, file, PR, screenshot) |
| :---- | :---- | :---- |
| **Task 1** | Completed | Pipeline executed; achieved 87.12% reference accuracy.. |
| **Task 2** | Completed | Identified 1-vs-2 digit confusion causing \~48% of errors. |
| **Task 3** | Completed | Drafted logic for confidence-based filtering vs. naive sampling. |
| **Task 4** | Completed | Proposed shared backbone strategy in Pipeline Proposal. |

---

### **Description (What happened?)**

This week focused on evaluating the baseline framework to identify structural weaknesses before writing new code. I successfully ran the Koshkina pipeline, securing our baseline accuracy of 87.12%. During error analysis, I identified that treating jersey numbers as a flat 100-class problem (0-99) caused massive 1-vs-2 digit confusion. To solve this, I proposed two architectural shifts: replacing naive frame sampling with a Top-K confidence filter, and shifting to a multi-task compositional digit classifier.

---

### **Reflection (What did you learn?)**

I learned that deep learning pipeline failures are often structural rather than tuning issues. Discovering the 1-vs-2 digit confusion highlighted that if the network doesn't understand the compositional nature of a number, hyperparameter tuning will not fix the underlying bottleneck.

---

### **Analysis (Why did it happen this way?)**

The baseline model struggled because it forced the network to memorize 100 independent classes rather than learning the shared visual features of individual digits (e.g., the visual similarity of the "7" in "27" and "74").

---

### **Conclusions (What insights did you gain?)**

We must curate the quality of the input frames before classification and change the output head to recognize compositional digits rather than flat classes.

---

### **Next Week Goals (Action Plan)**

* **Develop the experimental Top-K branch.**   
* **Integrate filtering logic into main.py.**   
* **Run legibility evaluation on mock data.**

---

---

## **Individual Contribution Log 4**

**Name:** Aaditya Golash  
**Week:** Week 4 (March 8 \- March 15, 2026\)

---

### **Current Tasks**

* **Task 1: Build the Top-k experimental Git branch.**  
* **Task 2: Implement confidence-based frame filtering logic.**  
* **Task 3: Integrate Top-K into main.py evaluation script.**  
* **Task 4: Validate legibility classifier on mock data.**

---

### **Progress Update**

**Status:** Completed

| Task | Status | Evidence (commit, file, PR, screenshot) |
| :---- | :---- | :---- |
| **Task 1** | Completed | `Top-k` branch created in the repository. |
| **Task 2** | Completed | Tracklet sorting/filtering logic written. |
| **Task 3** | Completed | Modified `main.py` to accept Top-K parameters. |
| **Task 4** | Completed | Achieved 91.71% accuracy on mock validation set. |

---

### **Description (What happened?)**

This week, I transitioned our Top-K conceptualization into functional code. I built the Top-k branch and implemented logic to sort and filter tracklet frames by legibility confidence scores, actively discarding low-quality images. I integrated this directly into main.py and ran an isolated evaluation of the legibility classifier using this new filtering method, achieving 91.71% accuracy (767 TP, 284 TN).

---

### **Reflection (What did you learn?)**

I learned the critical importance of isolating variables during debugging and development. By proving that the legibility filtering worked independently on mock data before attempting to wire it into the full recognition pipeline, I ensured we were building on a stable foundation.

---

### **Analysis (Why did it happen this way?)**

Naive frame sampling passes blurry or occluded frames to the recognizer, which skews the final tracklet voting. Filtering these out early ensures the model only makes predictions on high-confidence visual data.

---

### **Conclusions (What insights did you gain?)**

Confidence-based frame filtering significantly outperforms naive sampling and is ready to be integrated with the final classification model.

---

### **Next Week Goals (Action Plan)**

* **Draft an asynchronous workflow plan for the team.**  
* **Refactor the multi-task classification backbone.**  
* **Rewrite the dataloader for label splitting.**

---

---

## 

## 

## **Individual Contribution Log 5**

**Name:** Aaditya Golash  
**Week:** Week 5 (March 15 \-March 22, 2026\)

---

### **Current Tasks**

* **Task 1: Author "Implementation Plan: Multi-Task Digit Classifier".**  
* **Task 2: Merge 3 separate classification models into a shared ResNet-34 backbone.**  
* **Task 3: Refactor the jersey\_number\_dataset.py dataloader.**  
* **Task 4: Write and push the PyTorch training loop script.**

---

### **Progress Update**

**Status:** Completed

| Task | Status | Evidence (commit, file, PR, screenshot) |
| :---- | :---- | :---- |
| **Task 1** | Completed | Distributed async workflow PDF to the team. |
| **Task 2** | Completed | Pushed `recognition.py` with 3 parallel output heads. |
| **Task 3** | Completed | Dataloader correctly splits labels (e.g., tens=10, ones=digit). |
| **Task 4** | Completed | Pushed the main training loop script for local GPU execution. |

---

### **Description (What happened?)**

I authored a strict asynchronous implementation plan to eliminate code-waiting bottlenecks across the team. Technically, I architected the PyTorch model, merging three separate networks into a single shared ResNet-34 backbone with three output heads (tens, ones, full number) to solve our GPU memory exhaustion risk. I also rewrote the dataloader logic to ensure single-digit jersey numbers are encoded properly (e.g., a "7" becomes tens=10/blank, ones=7) and pushed the final training loop.

---

### **Reflection (What did you learn?)**

I learned that robust project architecture is just as crucial to a successful deployment as software architecture. Enforcing a 100% asynchronous workflow decoupled our engineering dependencies and dramatically accelerated our output.

---

### **Analysis (Why did it happen this way?)**

The multi-head design required a highly specific data ingestion format. Standard dataloaders failed because they could not handle the blank class (10) required for single-digit numbers, necessitating a complete rewrite of the label-splitting logic.

---

### **Conclusions (What insights did you gain?)**

Efficient management of both hardware resources (GPU memory via shared backbones) and human resources (async task delegation) is required to ship complex machine learning pipelines on a deadline.

---

### **Next Week Goals (Action Plan)**

* **Diagnose any performance bottlenecks in the new pipeline.**  
* **Draft parts relevant for the IEEE report.**  
* **Draft Progress Journal and Presentation**

---

---

**Individual Contribution Log 6**  
**Name:** Aaditya Golash  
**Week:** Week 6 (March 22 \-March 30, 2026\)

---

### **Current Tasks**

* **Task 1: Evaluate the multi-task model on full-body images.**  
* **Task 2: Delegate and draft progress journal and/or presentation**  
* **Task 3: Draft the relevant section for the IEEE final report.**  
* **Task 4: Secure presentation logistics and room booking.**

---

### **Progress Update**

**Status:** In-Progress

| Task | Status | Evidence (commit, file, PR, screenshot) |
| :---- | :---- | :---- |
| **Task 1** | In Progress | Finish and submit PPT and  |
| **Task 2** | In Progress | Team Evaluation of the pipeline. |
| **Task 3** | In-Progress | Drafted a structured learning approach in IEEE format. |
| **Task 4** | In-Progress | Booked COM 109 for the group task delegation and final group practice session. |

---

### **Description (What happened?)**

During the full pipeline evaluation, I discovered a critical failure: while the multi-task model achieved 71% training accuracy, its evaluation on full-body/center crops dropped to \~31%. I diagnosed this as a severe input distribution shift i.e. for that the model strictly required pose-based torso crops to function. Following this discovery, I drafted the methodology section of our IEEE final report, detailing our multi-task approach and Top-K logic, and secured a presentation workspace in The Commons.

---

### **Reflection (What did you learn?)**

I learned a stark lesson in deep learning data dependencies. Uncovering the crop-quality bottleneck underscored how hypersensitive these networks are to input-distribution shifts; a model trained on tight torso crops cannot generalize to raw full-body frames.

---

### **Analysis (Why did it happen this way?)**

The network overfit to the specific spatial dimensions and feature distributions of the pose-based crops generated during training. When fed rough center crops during testing, the feature extractor failed to localize the digits.

---

### **Conclusions (What insights did you gain?)**

Data pipeline consistency between training and inference is an absolute, non-negotiable requirement for computer vision models in production.

---

### **Next Week Goals (Action Plan)**

* **Finalize the presentation deck and Progress Journal and submit.**  
* **Conduct a live demo dry-run in COM 109\.**  
* **Finalize and submit the IEEE final report.**

### Enock Mutabazi

# Enock

## **Individual Contribution**

Name:Enock Mutabazi  
Week ( Feb 13–Feb 24, 2026\)  
---

**Current Tasks (Provide sufficient technical details.)**

* **Task 1:** Set up a new repository by cloning Koshkina’s repository and granting access to all group members. *(Completed)*  
* **Task 2:** Set up and run the baseline Jersey Number Recognition pipeline using the shared Google Colab environment (Koshkina’s repository). *(In progress)*  
* **Task 3:** Reviewed relevant research (Vats et al., 2021, *Multi-task Learning for Jersey Number Recognition in Ice Hockey*) and documented the key findings. *(Completed)*  
* **Task 4:** Proposed a pipeline to be used for our project. *(Completed)*  
* **Task 5:** Assigned Sections 2.2 and 5.1 for proposal writing and experimentation with the design. *(completed)*  
* **Task 6**: migrate tasks logs to github kanban (completed)

---

**Progress Update**

| Task | Status | Evidence |
| :---- | :---- | :---- |
| Task 1 | Completed | GitHub repository created, cloned from Koshkina’s repository, with access granted to all group members. |
| Task 2 | In progress | Baseline Jersey Number Recognition pipeline set up and running in the shared Google Colab environment. |
| Task 3 | Completed | Literature review notes and documented key findings from Vats et al. (2021). |
| Task 4 | Completed |  Proposed project pipeline document outlining the selected approach |
| Task 5 | Completed | Literature review notes  |
| Task 6 | Completed | GitHub Kanban board for project tracking. |
|  |  |  |

---

**Description (What happened?)**  
**What work did you do?**

During the week, I worked on setting up and understanding our Jersey Number Recognition project.

First, I created a new GitHub repository by cloning Koshkina’s repository and gave access to all group members. This helped us work together and manage our code properly. I also moved our task logs to a GitHub Kanban board so we could track progress more clearly.

Next, I started setting up and running the baseline Jersey Number Recognition pipeline in Google Colab. This involved installing required packages, managing different environments, loading pretrained models, and fixing several errors. The pipeline includes multiple steps such as filtering soccer balls, extracting features, removing outliers, classifying legibility, detecting pose, generating crops, and predicting jersey numbers.

I also reviewed the research paper by Vats et al. (2021) about multi-task learning for jersey number recognition. I wrote notes about the key ideas and used that understanding to propose a pipeline for our project. In addition, I worked on writing Sections 2.2 and 5.1 of our proposal.

---

**Reflection (What did you learn?)**  
**What did you learn?**

I learned that reproducing a research project is much more difficult than just running code. Many repositories require specific software versions, pretrained checkpoints, and GPU access. Small differences in library versions can cause errors.

I am still struggling with setting up the project properly in Google Colab because of dependency issues. The pipeline depends on specific versions of PyTorch, PyTorch Lightning, and other libraries. Managing multiple environments inside Colab has been challenging.

However, my team members are helping me troubleshoot these issues so that we can successfully run the pipeline and obtain results for our proposal. This experience has shown me the importance of teamwork and communication when working on complex technical projects.

I also gained a better understanding of how multi-stage computer vision systems work. Each step in the pipeline improves the overall accuracy and helps handle difficult cases like occlusion and unclear images.

**Analysis (Why did it happen this way?)**  
**Why was this approach used?**

The pipeline requires a GPU because feature extraction and pose detection are computationally heavy. Running everything on the CPU is extremely slow. That is why we used Google Colab to access GPU resources.

However, Colab has limitations such as runtime limits, storage restrictions, and dependency conflicts. These limitations slowed down experimentation and debugging.

The multi-step pipeline was used because jersey numbers are small, sometimes blurred, and sometimes partially blocked. By separating the problem into smaller tasks (filtering, legibility classification, pose detection, recognition, aggregation), the system becomes more reliable and easier to improve.

The project required GPU acceleration because feature extraction and pose estimation are computationally intensive. Running the pipeline on CPU was impractical due to extremely long runtimes. Therefore, we used Google Colab to access GPU resources.

However, Colab introduced limitations such as session timeouts, memory restrictions, and storage constraints. These constraints slowed experimentation and required repeated debugging. Additionally, the pipeline relies on multiple conda environments and specific PyTorch/PyTorch Lightning versions, which caused compatibility issues.

The multi-stage approach (ReID → filtering → legibility → pose → STR → aggregation) was used because jersey numbers are small, often occluded, and inconsistent across frames. Breaking the problem into structured components increases robustness and allows error isolation at each stage.

Conclusions (What insights did you gain?)

This week taught me that environment setup and dependency management are very important in deep learning projects. Debugging and configuration can take a lot of time.

I improved my understanding of full computer vision pipelines and learned how research ideas are applied in practice. I also strengthened my debugging skills and learned that collaboration is essential when facing technical challenges.

Overall, this experience helped me grow both technically and as a team member.

## **Individual Contribution**

**Name:** Enock Mutabazi

---

### **Current Tasks**

* **Task 1: Section 2.2 Completion** \- Finalize my assigned part of Section 2.2 in the proposal draft.  
* **Task 2: Section 5 Completion** \- Finalize my assigned part of Section 5.1 in the proposal draft.  
* **Task 3: Running Koshkina’s work** \- I was able to run the koshkina’s work using google collab pro  
* **Task 4: Transition Planning** \- Prepare for pipeline implementation and divide coding tasks for next week.

---

### **Progress Update**

**Status:** In-Progress

| Task | Status | Evidence (commit, file, PR, screenshot) |
| :---- | :---- | :---- |
| **Task 1** | Completed | My Section 2.1 part was completed  on time  |
| **Task 2** | Completed | My Section 5.1 part was completed on on time |
| **Task 3** | completed | Team meeting held on Feb 24, 2026 (5:00 PM-5:30 PM) to finalize draft direction and review all members' parts. |
| **Task 4** | Planned | Next team meeting set for Feb 25, 2026 at 7:30 PM; full document targeted for submission readiness on Feb 26, 2026\. |

---

### **Description (What happened?)**

I successfully completed sections 2.1 and 5.1, which rely on Koshkina’s work. I was able to run the pipeline and observe the results; however, due to GPU limitations, I purchased my own subscription to increase available GPU runtime

---

### **Reflection (What did you learn?)**

I learned how to run and evaluate machine learning pipelines based on existing research, particularly Koshkina’s work. I also gained practical experience working with GPU constraints and learned how to manage computational resources effectively. Additionally, I developed problem-solving skills by finding alternative solutions, such as acquiring my own GPU subscription to ensure I could complete my work efficiently.

---

### **Analysis (Why did it happen this way?)**

This situation occurred because the pipeline I was working with is computationally intensive and depends heavily on GPU resources. The available GPU allocation was limited, which restricted my ability to run experiments efficiently. Since my work relied on reproducing and building on Koshkina’s results, these limitations directly impacted my progress. As a result, I needed to find an alternative solution to ensure continuity, which led me to obtain additional GPU resources independently.

---

### **Conclusions (What insights did you gain?)**

I gained the insight that access to adequate computational resources is critical when working with machine learning pipelines, especially those that are GPU-intensive. I also realized the importance of planning for resource limitations early in a project to avoid delays. Additionally, this experience highlighted the value of adaptability and initiative in overcoming technical constraints, as well as the need to consider both technical and logistical factors when conducting research.

## 

## **Individual Contribution Log** 

---

### **Current Tasks**

* **Task 1: Running Top K implementation**   
* **Task 2:Debugging [main.py](http://main.py) to improve accuracy**  
* **Task 4: Documenting the top k results**

---

### **Progress Update**

**Status:** Completed

| Task | Status | Evidence (commit, file, PR, screenshot) |
| :---- | :---- | :---- |
| **Task 1** | Completed | Top 6 had highest accuracy compared to others 89.10% |
| **Task 2** | Completed | I was able to debug [main.py](http://main.py) and [helpers.py](http://helpers.py) to get different accuracy  |
|  |  |  |
|  |  |  |

### **Description (What happened?)**

I successfully ran Koshkina’s work and achieved an accuracy of 87.12%. I then implemented and tested our Top-K approach, where I obtained varying accuracy results, with the highest being 89.10% at K \= 6\. However, I encountered a consistency issue, as different values of K initially produced the same results. After debugging `main.py` and `helpers.py`, I was able to obtain different outputs for each K value, although some consistency issues still remain.

---

### **Reflection (What did you learn?)**

I learned the importance of thorough debugging and validation when working with machine learning implementations, as unexpected issues like inconsistent results can arise even when the code appears correct. This experience also strengthened my ability to troubleshoot by examining different parts of the code, such as `main.py` and `helpers.py`. Additionally, I gained a deeper understanding of how parameter choices, like Top-K values, impact model performance, and the importance of ensuring experimental consistency before drawing conclusions.

---

### **Analysis (Why did it happen this way?)**

This issue occurred mainly due to errors in the implementation, particularly within `main.py` and `helpers.py`, which caused different Top-K values to initially produce the same results. This indicated that the parameter was not being correctly applied or updated during execution. Additionally, factors such as randomness in the model or data processing may have contributed to the remaining consistency issues. Overall, the problem stemmed from a combination of implementation bugs and the need for more careful handling of parameters and experimental setup.

---

### **Conclusions (What insights did you gain?)**

I gained the insight that correct implementation and parameter handling are critical for obtaining reliable results in machine learning experiments. Even small issues in the code can lead to misleading outcomes, such as identical results across different parameter values. I also learned the importance of systematically debugging and validating each component of the pipeline. Additionally, this experience highlighted the need to ensure consistency and reproducibility in experiments before interpreting performance improvements.

**Action Plan:**

Fix remaining consistency issues with the Top-K implementation

Validate results by running multiple tests with controlled settings

Select and justify the best-performing model (e.g., K \= 6\)

Completing meeting logs

### Karo Li

# karo

 

| Task | Description | Status |
| :---- | :---- | :---- |
| **Task 1** | Configure and execute the baseline **Jersey Number Recognition** pipeline within the shared Google Colab environment (based on Koshkina’s repository). This includes environment setup, dependency installation, dataset path configuration, and initial execution of detection and recognition modules to verify reproducibility. | In Progress |
| **Task 2** | Design and maintain structured documentation templates for all project deliverables, including proposal drafts, literature review notes, meeting minutes, and individual contribution logs in a shared Google Docs workspace. | Completed |
| **Task 3** | Conduct a technical review of relevant research papers (e.g., Grad et al.) and extract architectural design insights, model components, loss functions, and evaluation strategies. Document findings and identify potential areas for architectural refinement or performance optimization. | Completed |
| **Task 4** | Develop and organize project proposal presentation materials, including pipeline diagrams, model architecture explanations, methodological improvements, and justification of the selected approach. | Completed |
| **Task 5** | Maintain detailed meeting records and design a structured personal contribution tracking system aligned with course assessment requirements to ensure transparency and traceability of work. | Completed |
| **Task 6** | Coordinate proposal development by decomposing tasks, distributing responsibilities among team members, reviewing contributions, and assisting in evaluating and selecting the final pipeline architecture. | Completed |
| **Task 7** | Draft and finalize assigned proposal sections (Sections 4 and 7), including technical methodology and evaluation framework, while contributing to overall proposal refinement and coherence. | Completed |

 

 

 

What work did you do?

I focused on strengthening the technical direction of the project through literature review and methodological development. I analyzed several relevant research papers, such as Zhou et al. (OSNet) and Lin et al. (ADRS), and summarized key ideas that could inform improvements to our baseline pipeline. Based on this review, I helped identify potential modifications to address known limitations in the original approach.

Each team member proposed their own version of the recognition pipeline, and I contributed by suggesting structural changes aimed at improving prediction stability and overall accuracy. After our team finalized the approach, I was responsible for drafting Section 3 of the proposal, including the overview of the method, model architecture, training strategy, and data preprocessing design.

understanding and extending a deep learning, based computer vision pipeline for jersey number recognition, this required reviewing prior research to understand common architectural choices and recognition strategies, while also examining how the baseline pipeline was structured and implemented.

I ran the existing system in a shared Google Colab environment to observe its behavior and outputs, and to better understand how data flows through each stage of the pipeline. By inspecting the model components and inference process, I gained a clearer understanding of the overall architecture, its computational constraints, and the main sources of prediction errors that our modifications aimed to address.

 

 

Reflection

Through this project I developed a more structured way of reading research papers and translating insights into concrete design decisions. Instead of focusing only on reported accuracy numbers, I learned to examine the error analysis section carefully and identify the dominant failure patterns described by the authors. For example, noticing that a large portion of two digit errors were caused by predicting a single digit changed how I evaluated potential improvements. It showed me that meaningful modifications should directly address the specific weakness identified in the original work.

I also improved my ability to refine a pipeline in a principled way. Rather than replacing components simply because newer models exist, I learned to first ask where the true bottleneck lies and whether a modification targets that bottleneck. This helped me understand that effective improvement comes from building on the original authors’ identified challenges, not from introducing additional tools without clear justification. As a result, I became more conscious of designing changes that are logically connected to observed errors and easier to evaluate through controlled experiments.

 

difficulties

The main difficulty I faced was related to GPU limitations during experimentation. Initially, I was using a T4 GPU in Google Colab, but the runtime repeatedly stopped during training. In one instance, the training process halted at around 22 out of 1221 iterations due to insufficient GPU resources. This interrupted progress and made it difficult to complete full training runs or conduct proper evaluation.

To address this issue, I upgraded to Google Colab Pro to access more stable and higher capacity GPU resources. This allowed the training process to run more consistently and reduced interruptions caused by hardware constraints.

 

**Week:** Mar 02 – Mar 08, 2026 (Phase: Top-K Research & Technical Alignment)

* **Task 1: Codebase Audit & Logic Trace:** Performed a deep-dive into main.py to trace the execution flow of get\_soccer\_net\_raw\_legibility\_results().  
* **Task 2: Interface Consistency Check:** Audited the Aggregation Stage code to ensure that the frame paths in legible\_dict and the scores in the raw JSON shared exact index ordering.  
* **Detailed Top-K Implementation Plan:** write the specific technical roadmap for the Top-K filtering engine, detailing the sprint from baseline locking to the final "K-Sweep" experiments

**Evidence:** Verified that the classifier, when called with threshold=-1, successfully generates the raw scores JSON required for the filtering stage.

### **Description (What happened?)**

During this initial phase, I focused on ensuring 100% technical alignment before any core logic was modified. My primary responsibility was to audit the existing aggregation stage to guarantee it could automatically ingest filtered frame lists once the Top-K logic overwrites the intermediate JSON files. I worked closely with Aaditya and Zhishang to confirm that the baseline configuration was locked and that the data structures were compatible across the pipeline.

### **Reflection (What did you learn?)**

I learned that in a multi-stage computer vision pipeline, data integrity is the most significant bottleneck. Even a minor discrepancy in how frames are indexed between the legibility classifier and the pose estimator can render the Top-K filtering useless. Pre-locking dependencies in the Colab Pro+ environment was essential to prevent version-related execution errors.

**Week:** Mar 09 – Mar 15, 2026 (Phase: Top-K Testing & Performance Tuning)

* **Task 1: Compatibility Validation:** Verified that the filtered output list feeds into the confidence-weighted aggregation module without generating data-type or formatting errors.  
* **Task 2: Parameter Debugging:** Assisted in troubleshooting the "Consistency Issue" where different values of $K$ initially produced identical accuracy results.

### **Description (What happened?)**

This week focused on the "K-Sweep" experiments. I was responsible for confirming that the filtered results correctly moved into the final aggregation stage. When the team encountered a bug where $K=1$ through $K=7$ yielded the same output, I helped debug helpers.py and main.py to ensure the Top-K parameter was actually being applied to the dictionary truncation logic. This allowed us to finalize the ablation study data.

### **Analysis (Why did it happen this way?)**

We utilized the Top-K approach because jersey numbers are frequently occluded or blurred across a tracklet. By isolating only the top $K$ most legible frames, we reduce the noise introduced by poor-quality crops, thereby increasing the reliability of the final prediction during the weighted aggregation phase.

**Week:** Mar 16 – Mar 22, 2026 (Phase: Multi-Task Transition & Data Layer)

* **Task 1: Label Splitting (Primary Owner):** Modified jersey\_number\_dataset.py to transition from a single label to a structured tuple of three labels: (Full, Tens, Ones).  
* **Task 2: Asynchronous Workflow Design:** Structured the data loading tasks to be strictly isolated, enabling the team to continue development while Aaditya and Leila were offline for midterms.

### **Description (What happened?)**

As we pivoted from a 100-class STR module to a multi-task architecture, I took ownership of the data foundation. I modified the core dataset script to split the ground truth jersey numbers into separate "Tens" and "Ones" digits. This ensures the model can learn shared digit features. I also ensured that my code was modular so that it would not create a bottleneck for the training loop development.

### **Reflection (What did you learn?)**

I learned that "Task Isolation" is a powerful project management tool. By strictly defining the inputs and outputs of jersey\_number\_dataset.py, I was able to complete the data layer modification independently, which was crucial during the midterm week when team availability was limited.

**Week:** Mar 23 – Mar 29, 2026 (Phase: Multi-Task Integration & Report Prep)

* **Task 1: Aggregation Integration (Primary Owner):** Integrated the deterministic override logic from the inference stage into the final confidence-weighted aggregation module.  
* **Task 2: System Validation:** Verified that the multi-head architecture correctly handles tie-breaking between the "Full" head and the combined "Tens/Ones" heads

### Leila Saparbek

# Leila

Name: Leila Saparbek  
Week 1–2 (Feb 13–Feb 24, 2026\)  
---

Current Tasks (Provide sufficient technical details.)

* Task 1: Set up and run the baseline Jersey Number Recognition pipeline using the shared Google Colab environment (Koshkina’s repository). (In progress)  
* Task 2: Create and maintain structured templates for all written project deliverables, including proposal sections, meeting logs, and personal reflection logs, in a shared Google document. (Completed)  
* Task 3: Review relevant research papers (including Grad et al.) and document architectural insights and potential improvements in the Literature Review section. (Completed)  
* Task 4: Develop project proposal presentation materials explaining the proposed pipeline and methodological improvements. (Completed)  
* Task 5: Maintain meeting logs and create a structured personal contribution log template aligned with course requirements. (Completed)  
* Task 6: Organize proposal development by distributing subtasks, coordinating contributions, and helping evaluate and finalize the team’s selected pipeline approach. (Completed)  
* Task 7: Complete assigned proposal sections (Sections 4 and 7\) and support overall proposal preparation. (Completed)

---

Progress Update

| Task | Status | Evidence |
| :---- | :---- | :---- |
| Task 1 | In Progress | Colab execution logs, environment setup |
| Task 2 | Completed | Shared project document templates |
| Task 3 | Completed | Literature Review entries and notes |
| Task 4 | Completed | Proposal presentation materials |
| Task 5 | Completed | Meeting log and personal log template |
| Task 6 | Completed | Task distribution records, proposal planning |
| Task 7 | Completed | Final proposal document sections |

---

Description (What happened?)  
What work did you do?  
During these two weeks, I focused on establishing both the organizational structure and technical foundation of the project. I created structured templates for proposal writing, meeting tracking, and individual logs, which helped standardize team contributions and ensured clarity in deliverables. I also actively participated in the literature review by analyzing relevant research papers and documenting potential architectural improvements. Based on these findings, I contributed to the development of the project proposal presentation and completed key sections of the written proposal. Additionally, I helped coordinate task distribution and proposal planning to ensure steady and balanced progress across the team.  
What was the technical context?  
The technical work involved reviewing deep learning–based computer vision research and beginning to interact directly with the baseline Jersey Number Recognition pipeline. I configured and executed the repository in Google Colab, resolved dependency and environment issues, and examined how the pipeline processes inputs and generates predictions. This allowed me to better understand the system’s architecture and computational requirements.  
Were you working individually or with teammates?  
My work involved both independent and collaborative efforts. I independently conducted literature review, documentation, and pipeline setup, while also working closely with teammates through shared documents, frequent discussions, and coordinated planning. I also supported the team by helping organize deliverables and ensuring clear project structure.  
---

Reflection (What did you learn?)  
What did you learn?  
I gained a deeper understanding of the Jersey Number Recognition pipeline, including its structure, execution flow, and computational requirements. I also learned how to effectively use Google Colab as a shared development environment for deep learning experimentation. The literature review helped me understand current research approaches and identify potential areas for improvement.  
What went well?  
Establishing structured documentation and templates early in the project significantly improved team coordination and efficiency. The literature review and proposal development progressed smoothly, and the team responded positively to the structured workflow. Regular discussions helped align our direction and strengthen collaboration.  
What difficulties did you face?  
The main technical challenges involved resolving dependency conflicts, configuring runtime environments, and managing computational limitations on local hardware. These issues were mitigated by transitioning to Google Colab Pro. Balancing this project alongside other academic responsibilities also required careful time management.  
What were your reactions?  
Initially, I was cautious about taking a more active role in organizing tasks and coordinating proposal work. However, the team’s responsiveness and engagement reassured me, and I became more confident in contributing to both the technical and organizational aspects of the project.

Analysis (Why did it happen this way?)  
Why was this approach used?  
Starting with literature review and baseline pipeline setup was necessary to establish a strong technical foundation before proposing improvements. Creating structured documentation and distributing tasks helped ensure clarity, accountability, and steady progress across the team.  
What technical decisions were made?  
We chose to use Google Colab as the primary development environment to ensure consistent execution and access to GPU resources. This enabled reliable experimentation and avoided limitations of local hardware environments.  
What challenges affected your progress?  
The primary challenges involved understanding the structure of an unfamiliar deep learning codebase and resolving environment setup issues. Additionally, initial exploration of simplified setups slightly delayed progress toward fully running the original pipeline, but improved overall understanding of the system.

Conclusions (What insights did you gain?)  
This phase established a strong organizational and technical foundation for the project. I gained practical experience reviewing research literature, working with deep learning pipelines, and contributing to structured project planning. I also developed greater confidence in supporting team coordination and ensuring clear documentation and progress tracking. Overall, this period positioned our team well for transitioning into full pipeline execution and experimentation.  
Next Week Goals (Action Plan. What will you do next?)

* Complete setup and successful execution of the baseline Jersey Number Recognition pipeline in Google Colab  
* Verify baseline outputs and document pipeline behavior  
* Finalize and submit the full project proposal  
* Review and refine proposal sections contributed by all team members  
* Begin implementation work on the KfId stage of the project pipeline  
* Continue maintaining meeting logs and documentation  
* Support team coordination and technical troubleshooting as needed

# final PJ Leila

# **Leila Saparbek**

 

## **Week 3 (Feb 26 – Mar 5, 2026\)**

 

### **Current Tasks**

No project work was completed during this period. This week was fully dedicated to other academic course obligations and did not involve contributions to the Jersey Number Recognition project.

 

### **Progress Update**

| Status | Details |
| :---- | :---- |
| No project activity | Academic obligations outside this course required full attention during this period. All project tasks were paused. |

 

### **Description (What happened?)**

**What work did you do?** No work was completed on the Jersey Number Recognition project this week. The team was in a transition period following the proposal submission and baseline replication phase. Personal academic workload from other courses prevented any meaningful contribution during Feb 26 – Mar 5\.

 

**What was the technical context?** N/A for this period. The last completed project activity was successful end-to-end baseline replication in Google Colab, confirming 87.12% accuracy on the SoccerNet test set (1,055/1,211 tracklets).

 

**Were you working individually or with teammates?** No collaborative or individual project work took place this week.

 

### **Reflection (What did you learn?)**

**What went well?** The prior two weeks had established a solid foundation, so the project was in a stable state that could sustain a brief pause without losing momentum.

 

**What difficulties did you face?** Balancing overlapping academic deadlines across multiple courses made it impossible to contribute to the project this week.

 

**What were your reactions?** While the pause was unavoidable, I made a deliberate effort to be fully re-engaged by the time of Meeting 7 on March 5, arriving prepared to resume technical contributions.

 

### **Analysis (Why did it happen this way?)**

**Why was this approach used?** Given the competing academic deadlines, the decision to temporarily pause project contributions was a deliberate time management choice rather than a lack of engagement.

 

### **Conclusions**

This week served as a recovery and reorientation period. The project foundation remained intact from Weeks 1–2, and I was ready to resume full contributions starting with Meeting 7 on March 5\.

 

### **Next Week Goals**

•       Attend Meeting 7 and contribute to Top-K implementation planning

•       Review Koshkina pipeline structure in preparation for Top-K integration

•       Draft personal Top-K implementation proposal for team review

•       Lock in Google Colab Pro environment for upcoming compute-heavy runs

 

 

## **Week 4 (Mar 6 – Mar 12, 2026\)**

 

### **Current Tasks (Provide sufficient technical details.)**

•       Task 1: Attend Meeting 7 (Mar 5\) and Meeting 8 (Mar 8\) to plan Top-K keyframe selection implementation strategy. (Completed)

•       Task 2: Draft a personal Top-K implementation proposal outlining methods, packages, and pseudocode, submitted to team Discord before Sunday Mar 8\. (Completed)

•       Task 3: Lock and verify the Google Colab Pro+ environment; ensure all pipeline dependencies are pinned and reproducible for the upcoming K-sweep experiments. (Completed)

•       Task 4: Attend Meeting 9 (Mar 9\) and participate in finalizing the revised 5-day Top-K implementation plan, including role assignments for high-compute runs. (Completed)

•       Task 5: Take ownership of High-Compute Run B in the K-sweep experiments (K=5 and K=7), coordinating scheduling with Enock for Run A. (In Progress)

•       Task 6: Begin refactoring Colab notebooks for pipeline reproducibility as teammates submit new Top-K implementation components. (In Progress)

 

### **Progress Update**

| Task | Status | Evidence / Outcome |
| :---- | :---- | :---- |
| Task 1 | Completed | Meeting 7 & 8 attended; Top-K approach finalized (legibility-score-based sorting between Legibility Classifier and Pose Detection stages) |
| Task 2 | Completed | Individual Top-K proposal submitted to Discord before March 8 deadline; team adopted a condensed version of Leila’s plan |
| Task 3 | Completed | Colab Pro+ environment verified; dependencies locked, baseline 87.12% reproducibly confirmed |
| Task 4 | Completed | Meeting 9 attended; role assignments confirmed — Leila assigned to High-Compute Run B (K=5, K=7) alongside Enock’s Run A |
| Task 5 | In Progress | K-sweep runs scheduled; environment ready, awaiting pipeline code from Aaditya/Zhishang |
| Task 6 | In Progress | Ongoing notebook refactoring as new components are merged into the shared branch |

 

### **Description (What happened?)**

**What work did you do?** This week was primarily focused on planning and coordination for the Top-K keyframe selection implementation. I attended three meetings (Meeting 7 on Mar 5, Meeting 8 on Mar 8, and Meeting 9 on Mar 9), contributed a detailed implementation proposal that became the structural basis for the team’s revised 5-day plan, and took on formal responsibility for the high-compute K-sweep runs at K=5 and K=7. I also continued maintaining the Colab environment and started incrementally refactoring notebooks to ensure smooth end-to-end pipeline execution as teammates pushed new components.

 

**What was the technical context?** The Top-K keyframe selection stage is designed to filter tracklet frames by their legibility scores before passing them to the PaRSeq recognition stage, which was identified as the dominant runtime bottleneck (\~78 images/sec). The intervention point is between the Legibility Classifier output and the Pose Detection stage in main.py. Technically, the approach uses existing legibility scores as a ranking proxy, applies apply\_topk\_filtering() to truncate the sorted frame dictionary, and overwrites the intermediate JSON file so downstream stages automatically receive the filtered set. My environment management responsibility involved ensuring that the timm version conflict and the numpy pinning issues documented in earlier weeks did not resurface for the K-sweep runs.

 

**Were you working individually or with teammates?** Collaborative and individual work overlapped heavily this week. Meetings were attended with the full team. My implementation proposal and environment management were individual contributions. The K-sweep execution responsibilities were coordinated with Enock, with Zhishang serving as a local GPU hardware fallback.

 

### **Reflection (What did you learn?)**

**What did you learn?** I learned how to scope an implementation plan at the right level of detail so that it can be adopted and adapted by a team under time pressure. The team’s decision to follow a condensed version of my Top-K proposal confirmed that clear pseudocode and explicit role assignments are more actionable than high-level descriptions alone.

 

**What went well?** The three meetings in quick succession (Mar 5, 8, 9\) allowed the team to converge quickly on a technical direction after the blank week. The decision to pivot away from KFA-ID toward legibility-score-based Top-K sorting was well-reasoned and significantly reduced implementation complexity.

 

**What difficulties did you face?** Co-ordinating GPU availability across team members with different Colab access levels required careful scheduling. The dependency environment also needed ongoing maintenance as new packages were introduced by Aaditya and Zhishang’s codebase audit work.

 

**What were your reactions?** I was energized by the concrete role assignment. Having a specific deliverable (K=5 and K=7 runs) gave me a clear target and made the transition back to active contribution after Week 3 straightforward.

 

### **Analysis (Why did it happen this way?)**

**Why was this approach used?** The team chose legibility-score-based Top-K sorting over KFA-ID because it required no additional network and could be inserted as a thin filter between existing pipeline stages. This minimized integration risk and ensured the change was auditable and reversible.

 

**What technical decisions were made?** The intervention point (between Legibility Classifier and Pose Detection in main.py) was chosen after confirming that apply\_topk\_filtering() could overwrite the intermediate JSON file before the Pose stage reads it. The K values to sweep (K=1, 3, 5, 7\) were selected to span from aggressive to conservative filtering.

 

**What challenges affected your progress?** Pipeline component readiness from teammates (Aaditya’s main.py changes, Zhishang’s shell scripts) was a dependency that slightly delayed the start of the K-sweep runs.

 

### **Conclusions**

This week re-established full project engagement through structured planning and concrete role assignments. The team converged on a technically sound Top-K implementation strategy, and the K-sweep execution responsibilities were clearly divided. The foundation was set for the experimental runs that would follow in Week 5\.

 

### **Next Week Goals**

•       Execute High-Compute Run B: K=5 and K=7 experiments on Colab Pro+

•       Validate K-sweep outputs against Enock’s Run A results (Baseline, K=1, K=3)

•       Continue refactoring notebooks and testing new pipeline components as they are submitted

•       Support Karo’s compatibility verification between Top-K output and the confidence-weighted aggregation stage

•       Attend next team meeting and contribute to result analysis

 

 

## **Week 5 (Mar 13 – Mar 19, 2026\)**

 

### **Current Tasks (Provide sufficient technical details.)**

•       Task 1: Continuously refactor shared Python notebooks to ensure smooth end-to-end pipeline execution as teammates submit new Top-K implementation components. (In Progress)

•       Task 2: Execute High-Compute Run B for the K-sweep experiments, running K=5 and K=7 variants on Colab Pro+. (In Progress)

•       Task 3: Test each teammate’s submitted code against the full pipeline immediately upon receipt and share outputs with the team. (In Progress)

•       Task 4: Identify and flag discrepancies between local Top-K results and Enock’s reported results; communicate findings to the team. (Completed)

•       Task 5: Attend Meeting 11 (Mar 17\) and propose implementation plans for the next pipeline stage. (Completed)

 

### **Progress Update**

| Task | Status | Evidence / Outcome |
| :---- | :---- | :---- |
| Task 1 | In Progress | Ongoing since Mar 13; notebooks refactored after each teammate PR/submission to maintain pipeline stability |
| Task 2 | In Progress | K=5 and K=7 runs executed on Colab Pro+; results collected and compared against baseline |
| Task 3 | In Progress | Each submitted component tested end-to-end immediately; outputs shared on team Discord |
| Task 4 | Completed | Discrepancy identified between Enock’s Top-K results (\~90% reported accuracy) and independently verified outputs; Enock notified to recheck |
| Task 5 | Completed | Meeting 11 attended; role assignments confirmed for next pipeline stage |

 

### **Description (What happened?)**

**What work did you do?** From March 13 onward, I took on a continuous pipeline integration and validation role. Whenever a teammate submitted new code or a notebook change, I tested it against the full pipeline end-to-end and reported outputs back to the team. This involved regularly re-running the full SoccerNet pipeline, checking output JSON formats, and verifying that new components did not introduce regressions at other stages. I ran my assigned K=5 and K=7 K-sweep experiments on Colab Pro+ as part of the team’s ablation study, distributing GPU work in coordination with Enock’s Runs A and B. I also attended Meeting 11 on March 17 and contributed to planning the next phase of the project.

 

**What was the technical context?** The pipeline at this stage consisted of the full Koshkina baseline with the Top-K filtering stage injected between the Legibility Classifier and Pose Detection. Multiple versions of the Top-K main.py changes were proposed and tested during this period. The K-sweep required running the complete SoccerNet evaluation pipeline for each K value, which is compute-intensive due to the PaRSeq recognition stage. My role was to be the consistent integration point: because I was the only team member running the full pipeline reliably, I served as the canonical source of verified results.

 

**Were you working individually or with teammates?** Mostly independent technical work with close coordination through Discord. Pipeline testing was individual; result comparison and discrepancy flagging involved direct communication with Enock and broader team updates.

 

### **Reflection (What did you learn?)**

**What did you learn?** I learned that being the sole reliable pipeline runner on a team creates both responsibility and risk. It is valuable for consistency, but it also means that environment or configuration differences between team members can produce results that are genuinely hard to reconcile without careful version control and environment documentation.

 

**What went well?** The notebook refactoring workflow became smoother over time as I developed a pattern: receive new code, update the shared notebook, run full pipeline, check outputs, report back. This reduced the time between code submission and validated result to roughly one session per component.

 

**What difficulties did you face?** The most significant challenge of the week was an output discrepancy with Enock’s Top-K results. Enock reported a Top-K accuracy of approximately 90%, which would have exceeded the 87.12% PaRSeq baseline — a surprising outcome. When I ran the same configuration independently, I could not reproduce this result. The discrepancy could not be immediately explained by differences in K value or random seed, and raised concerns about whether the evaluation was being performed on the correct subset or using a consistent input format. I brought this to Enock’s attention directly and asked him to re-verify his pipeline run.

 

**What were your reactions?** I was skeptical but methodical. Rather than dismissing the discrepancy or accepting it uncritically, I documented both result sets and framed the issue clearly for Enock so he could investigate. I did not want to block team progress by raising an alarm, but I also could not report an unverified number as a confirmed result.

 

### **Analysis (Why did it happen this way?)**

**Why was this approach used?** I prioritized continuous integration testing because the Top-K stage involved modifications to main.py that touched multiple downstream data paths. Given the earlier history of environment issues and pipeline fragility, testing each change immediately was the most reliable way to catch regressions before they accumulated.

 

**What technical decisions were made?** I chose to manage GPU costs carefully by validating all notebook changes on free Colab resources before committing to paid Colab Pro+ runs. This meant sometimes running on a smaller data subset to confirm correctness before the full K-sweep evaluation.

 

**What challenges affected your progress?** The result conflict with Enock’s output created uncertainty about the correct Top-K accuracy figures and delayed the finalization of the ablation table. Resolving it required additional communication and re-runs.

 

### **Conclusions**

Week 5 established me as the integration lead for the Top-K phase: continuously testing, verifying, and reporting pipeline outputs. The K-sweep data was collected, but the discrepancy in Enock’s reported results introduced uncertainty that needed to be resolved before the final ablation table could be completed. The experience reinforced the importance of having a single canonical evaluation environment.

 

### **Next Week Goals**

•       Resolve discrepancy between independently verified K-sweep results and Enock’s reported figures

•       Consolidate verified K-sweep results into the ablation table

•       Begin work on the multi-task digit classifier branch (leila-multitask-setup)

•       Set up reproducible training environment for the multi-task ResNet-34 pipeline on Colab and Vast.ai

•       Run pose estimation on training frames to generate matched torso crops for classifier training

 

 

## **Week 6–7 (Mar 20 – Mar 26, 2026\)**

 

### **Current Tasks (Provide sufficient technical details.)**

•       Task 1: Stabilize a reproducible training and inference environment for the multi-task digit classifier on Colab and Vast.ai (setup\_env.sh, requirements\_phase1\_pipeline.txt, RUN\_ORDER.md). (Completed)

•       Task 2: Organize end-to-end automation scripts to enable reproducible execution of the full pipeline from data download through training, inference, and evaluation. (Completed)

•       Task 3: Implement and integrate the multi-task ResNet-34 classifier pipeline, including dataset loader fixes, training loop corrections, and inference output formatting. (Completed)

•       Task 4: Run preliminary experiments across full-body, center-crop, and pose-crop input variants to characterize the performance gap versus the PaRSeq baseline. (Completed)

•       Task 5: Diagnose the root cause of the multi-task model’s underperformance relative to baseline. (Completed)

•       Task 6: Run pose estimation on the full SoccerNet training set to generate matched torso crops for classifier retraining. (Completed)

 

### **Progress Update**

| Task | Status | Evidence / Outcome |
| :---- | :---- | :---- |
| Task 1 | Completed | Created setup\_env.sh, requirements\_phase1\_pipeline.txt, and RUN\_ORDER.md documenting dependency fixes and correct execution order |
| Task 2 | Completed | Prepared download\_all.sh and run\_everything.sh for reproducible setup, data download, training, inference, and evaluation |
| Task 3 | Completed | Finished recognition\_multitask.py, jersey\_number\_dataset.py, train\_multitask.py, and inference\_multitask.py integration |
| Task 4 | Completed | Tested full-body (31.3%), center-crop (32.3%), and pose-crop (69.3%) variants; Top-K baseline variants also recorded (K=1: 32.78%, K=5: 85.05%, K=20: 86.37%) |
| Task 5 | Completed | Confirmed that crop quality and train–test mismatch, rather than the multi-task architecture, explain the performance gap |
| Task 6 | Completed | Pose estimation running on full training set; classifier retraining on matched pose-based torso crops initiated |

 

### **Description (What happened?)**

**What work did you do?** This week, I focused on converting the leila-multitask-setup branch into a reliable, reproducible experimentation environment and using it to evaluate the feasibility of the multi-task digit-decomposition architecture. My infrastructure work included creating setup\_env.sh (a one-shot dependency installer handling PyTorch detection, numpy pinning, torch.load patching for PyTorch 2.6+, and removal of incompatible HuggingFace datasets dependencies), download\_all.sh (an idempotent script for repositories, model weights, ReID weights, and SoccerNet data), run\_everything.sh (an all-in-one execution script for Vast.ai), and RUN\_ORDER.md (an execution cheat sheet documenting the timm version conflict and correct stage order). On the model side, I fixed the dataset loader (jersey\_number\_dataset.py) to correctly read SoccerNet JSON instead of the earlier CSV-based format, corrected the training loop (train\_multitask.py) to use the JSON pipeline, and integrated the inference script (inference\_multitask.py) to emit PaRSeq-compatible output JSON. I then ran experiments across three crop conditions and documented the results.

 

**What was the technical context?** The multi-task ResNet-34 architecture uses a shared backbone with three classification heads: a full head (100 classes for jersey numbers 0–99), a tens head (11 classes for the tens digit), and a ones head (10 classes for the ones digit). Training used AdamW with cosine LR scheduling, early stopping, and weighted multi-head losses. The baseline Koshkina pipeline uses pose-guided torso crops as input to PaRSeq, which is why training on full-body or center-crop images produced a severe train–test mismatch. Running pose estimation on the training set was necessary to align the multi-task model’s input distribution with the baseline’s evaluation pipeline.

 

**Were you working individually or with teammates?** Infrastructure cleanup, dataset correction, and training pipeline fixes were primarily my own contributions. The broader multi-task architecture was coordinated with Aaditya (backbone design) and Enock (original inference assignment). Karo was responsible for the aggregation and confidence-weighting stages that interface with the multi-task output.

 

### **Reflection (What did you learn?)**

**What did you learn?** I learned that a model training successfully to \~71% training accuracy is not the same as making progress if the input distribution does not match the evaluation setting. This week reinforced how strongly input preprocessing determines downstream performance in computer vision pipelines. I also deepened my experience with dependency management across heterogeneous GPU environments (Colab vs Vast.ai), specifically around PyTorch version pinning, numpy compatibility, and HuggingFace dataset conflicts.

 

**What went well?** The branch is now well-organized, the scripts are easy to rerun, and the experimental results are clearly documented. I was able to transition the project from scattered implementation attempts to a reproducible workflow that other teammates can execute independently. The diagnostic framing of the 32% result — identifying crop quality as the bottleneck rather than the architecture — was a constructive pivot that gave the team a concrete next step.

 

**What difficulties did you face?** The main challenge was that the early multi-task results (31–32%) looked discouraging at first glance. However, the low accuracy proved diagnostically useful: it revealed a train–test mismatch that had not been made explicit in earlier planning. Managing GPU costs across Colab Pro+ and Vast.ai also required careful sequencing — I followed a consistent rule of validating on free resources before committing to paid runs. Additionally, resolving HuggingFace datasets library conflicts with mmcv and Python 3.12 required targeted version pinning that was not documented anywhere in the original repository.

 

**What were your reactions?** I felt more confident after identifying a concrete, actionable explanation for the failure mode. Rather than treating 32% as evidence that the multi-task idea was fundamentally flawed, I was able to narrow the problem to crop quality and training-data alignment. That made the next step — generating pose-based training crops — feel achievable and well-motivated.

 

### **Analysis (Why did it happen this way?)**

**Why was this approach used?** Prioritizing reproducibility and comparability was a deliberate choice. Without consistent setup scripts and pinned dependencies, experimental results across teammates and across GPU environments would not be comparable. Keeping the inference output format aligned with PaRSeq (same JSON structure) ensured that all results could be evaluated with the same script, making the ablation study rigorous.

 

**What technical decisions were made?** Key decisions included: (1) pinning numpy and PyTorch versions explicitly rather than relying on defaults, (2) patching torch.load to add weights\_only=True for PyTorch 2.6+ compatibility, (3) replacing the CSV-based dataset loader with a JSON-based one to match the SoccerNet tracklet format, and (4) running pose estimation on training data to generate matched crops before drawing any conclusions about the multi-task architecture’s ceiling performance.

 

**What challenges affected your progress?** The mmcv/Python 3.12 conflict and HuggingFace datasets incompatibility were the two most time-consuming environment issues. They required iterative testing across Colab and Vast.ai to isolate and resolve. Additionally, running pose estimation on the full training set was computationally expensive and required careful scheduling on Vast.ai to stay within budget.

 

### **Conclusions**

This period established that the multi-task pipeline is technically functional and produces stable training results, but its current performance is limited by preprocessing mismatch rather than by the architecture or training code itself. The most critical insight is that pose-based torso crops must be generated for the training set before any serious comparative evaluation between the multi-task approach and the PaRSeq baseline can be made. The reproducible environment and automation scripts created this week position the team to execute that evaluation efficiently in the final project phase.

 

### **Next Week Goals**

•       Retrain the multi-task ResNet-34 classifier on pose-based torso crops and evaluate against the 87.12% PaRSeq baseline

•       Investigate the hybrid tens-head oracle approach: use the multi-task tens head as a digit-count oracle to resolve 1-vs-2 digit confusion errors in PaRSeq output

•       Analyze the 1-vs-2 digit confusion rate and determine whether the hybrid approach improves on the baseline

•       Prepare visualizations and ablation tables for the final report

•       Support final report writing and team deliverable submission

### Zhishang Ma

# Zhishang

Zhishang Ma

Week 1-2: 

What happened?

| Task | Description | Status | Evidence |
| :---- | :---- | :---- | :---- |
| Task 1 | Download SoccerNet Dataset. | Completed | Python code in Colab notebook |
| Task 2 | Complete section 1, 6 and 8 in project proposal. | Completed | Project proposal document |
| Task 3 | Provide a pipeline to the team. The content is in my part of literature review. | Completed | Pipeline proposal on the Google document |
| Task 4  | Configure Kashkina’s pipeline locally and run it.  | Failed |  |

Reflections

In practice, it is a difficult thing to configure a development environment. I encountered many situations that the requirement of a package can’t be satisfied, especially for version problems. The research pipeline we are using used many old Python frameworks with many old features. So its required environment can’t be installed automatically. I tried to install some packages  that manually and change some code. But I still can’t run the code. Fortunately, the team managed to run the pipeline on Google Colab. 

Reading papers in the area of machine learning is not a very difficult task. Since many results are based on experiment and I don’t need to understand very complex mathematics proof. The important thing is to know what the researches did and understand relationship between different papers. A very good way to do this is to look at how a paper cites other papers. And in each paper, it is a good idea to focus on the network architecture, find what modules are there in the network and try to figure out the structure of input and output.

Analysis

Jersey number recognition is a task similar to hand written number recognition. But jersey number recognition need to handle images from low-resolution sports broadcast videos. So there are some difficulties to deal with problems including occupation, motion blur, torsion and so on in jersey number recognition task. Based on a number recognition framework, Kashkina’s pipeline has several steps to filter out legal frames and solve torsion problems.  
Week 3

No project work.

Week 4

Description

The group started to work on Top-K this week. I learned the conception about Top-K. Then I provided a draft for the implementation of Tok-K. My draft focused on talking about the structure of Koshkina et al.’s code, tried to find how they defined the classes for legibility classifier and find where to change the code to implement Top-K.

Reflection

It isn’t a very difficult to understand the structure of a research program. The important thing is to focus on the name of classed and functions in the code so I can understand what they are doing and then find out how to change the code. Pytorch is also a easy to use framework. It is easy to import trained models and set my own models in Pytorch. The most difficult thing is to understand the structure of tensors used in the code. It is a good idea to do this by using torch.shape to find out the structures of these tensors. Only when I know what the structures of the tensors are, I can use a model to handle with the tensors correctly.

Week 5

Description

Created code to apply Top-K based on Koshkina et al.’s legibility classifier. Top-K is used to select out K images with highest scores as the output of legibility classifier. A custom image loader for Pytorch is created to load images to tensors as input for the legibility classifier.

## Meeting Logs

# Meeting log

# **Meeting 1 (13 Feb 2026\)**

# **Meeting 1**

**Date:** February 13, 2026  
**Time:** 3:00 PM – 3:40 PM  
**Format:** In-person  
**Location:** —  
**Attendees:** Karo, Aaditya, Leila, Enock, Zhishang

**Written By:** Leila

## **Work Completed Before the Meeting**

* Aaditya set up the GitHub repository.  
* Enock and Aaditya added all necessary files from Koshkina’s original work, including copying the repository and uploading the datasets.  
* Leila created a shared Google document to track the project proposal structure.  
* All team members were assigned to familiarize themselves with the project materials, including the original papers and supporting resources.

## **Discussion During the Meeting**

### **Technical and Organizational Discussion**

* The team identified and discussed potential issues related to running the project locally and managing the repository.  
* A preliminary workflow and development pipeline were established.

### **Project Proposal Timeline**

* The team agreed that a draft version of the full project proposal must be completed by Tuesday or Wednesday (February 24–25, 2026\) to allow sufficient time for structural revisions and refinement.

### **Literature Review Coordination**

* A dedicated Literature Review tab was created in the shared Google document.  
* Each team member was instructed to:  
  * Provide relevant citations  
  * Highlight key findings, methodologies, and performance results  
  * Focus on papers related to the project that could inform its design and implementation  
* This work supports Section 2 of the project proposal and will help inform Sections 3 and 4\.  
* Target completion date: Monday, February 16, 2026\.

## **Role Assignments and Responsibilities**

* Enock volunteered to set up a shared Google Colab environment to run the project, as local execution is computationally demanding on personal devices.  
* Enock also agreed to manage and maintain the GitHub Kanban board.  
* Leila volunteered to create an individual progress tracking file. The team agreed that each member would update this file weekly, every Sunday.  
* The team agreed that all pull requests must be reviewed and approved by at least one team member other than the author prior to merging.  
* Aaditya agreed to configure the necessary GitHub repository settings to enforce this rule.

## **Decisions Made**

* Establish a structured workflow for proposal development and literature review.  
* Maintain a shared progress tracking system.  
* Use pull request review requirements to ensure code quality and accountability.  
* Maintain consistent documentation across GitHub, Google Docs, and Discord.

## **Next Meeting**

**Date:** Monday, February 16, 2026  
**Time:** 3:00 PM

# Meeting 2(16 Feb 2026\)

# **Meeting 2**

**Date:** February 16, 2026  
**Time:** 3:00 PM – 4:00 PM  
**Format:** Discord call  
**Attendees:** Karo, Aaditya, Leila, Enock, Zhishang (present, but unable to speak due to microphone issues)

**Written By:** Leila

## **Work Completed Before the Meeting**

* Enock shared the Google Colab workspace, including results from two completed runs.  
* Aaditya and Leila contributed to the Literature Review tab, including relevant papers and potential project design ideas.  
* Karo shared an additional relevant research paper via Discord.  
* The following team members successfully ran the project locally or in Colab:  
  * Aaditya  
  * Enock  
  * Leila

## **Issues Identified**

### **Technical Issues**

* The team encountered issues importing the SoccerNet package in Google Colab. Despite installation, Colab was unable to locate the package within the execution environment.

### **Documentation and Project Management Issues**

* The team identified the need for a more detailed Progress Journal structure, emphasizing reflective analysis rather than a simple checklist of completed tasks.  
* Enock initially encountered issues creating the Kanban board due to repository permission and configuration settings. This issue was later resolved by Aaditya.

## **Discussion During the Meeting**

* Aaditya and Leila presented summaries of the papers they identified.  
* Leila and Enock compared and discussed their respective experimental run results.  
* The team discussed scheduling and agreed to maintain consistent meeting intervals.

## **Decisions Made**

The team collectively agreed to the following:

### **Communication and Workflow**

* All members must upload results and completed tasks to the appropriate platforms (Discord, Google Docs, GitHub) at least one hour before meetings to allow sufficient review time.  
* All members are expected to actively participate in group discussions and project planning.  
* Meeting logs will be maintained in a shared Google document to ensure accurate documentation for the Progress Journal.

## **Tasks Assigned for Next Meeting**

### **Task 1: Pipeline Proposal Presentations**

Each team member will prepare a short presentation covering:

* Their proposed pipeline design  
* Supporting diagrams or system architecture schemes  
* Relevant methodology and justification

The goal of these presentations is to assess the feasibility of each proposed pipeline and inform final project design decisions.

### **Task 2: Pipeline Selection**

Following presentations, the team will conduct a group discussion and voting process to finalize the project proposal and implementation direction.

### **Task 3: Code Execution Verification**

* All team members must run Enock’s shared Colab implementation.  
* Each member must submit screenshots verifying successful execution.

### **Task 4: Documentation and Project Management**

* Leila is responsible for:  
  * Finalizing and submitting Meeting 1 and Meeting 2 logs  
  * Providing a draft version of the progress tracking README file  
* Enock is responsible for:  
  * Converting assigned tasks into GitHub Kanban board action items after documentation is completed

## **Next Meeting**

**Date:** Thursday, February 19, 2026  
**Time:** 3:00 PM

# **Meeting 3 (19 Feb 2026\)**

# **Meeting 3**

**Date:** February 19, 2026  
**Time:** 3:00 PM – 4:40 PM  
**Format:** Discord  
**Location:** Discord call  
**Attendees:** Karo, Aaditya, Leila, Enock, Zhishang

**Written By:** Aaditya

## **Work Completed Before the Meeting**

* Everyone has run the code  
* Aaditya configured github repo (webhook, branch protection, etc.) and Enock created issues on Kanban board  
* Everyone has submitted their presentations to propose which pipeline we will be using.

## **Discussion During the Meeting**

### **Technical and Organizational Discussion**

* The team identified and discussed potential issues related to running the project locally and managing the repository.  
* The team

### **Project Proposal Timeline**

* The team agreed that we will submit our proposed timelines to be voted on by tonight (11:59pm). We will begin work on Friday (February 20 2026\) to allow sufficient time for structural revisions and refinement.

### **Presentations**

* Each member presented their findings from multiple research papers.  
* Each member asked questions and figured out what they would think the best presentation would be.

## **Role Assignments and Responsibilities**

* Aaditya volunteered to do team log.  
* The team decided to vote tonight by 11:59 pm and work from tomorrow on project proposal.

## **Decisions Made**

* Establish a structured workflow for proposal development and literature review.  
* Maintain a shared progress tracking system.  
* Use pull request review requirements to ensure code quality and accountability.  
* Maintain consistent documentation across GitHub, Google Docs, and Discord.

## **Next Meeting**

**Date:** Saturday, 21 February 2026  
**Time:** 5:00 PM

# **Meeting 4 (21 Feb 2026**

# **Meeting 4**

**Date:** February 21, 2026  
**Time:** 5:00 PM – 6:00 PM  
**Format:** Discord  
**Location:** Discord call  
**Attendees:** Karo, Aaditya, Leila, Enock, Zhishang

**Written By:** Leila

## **Work Completed Before the Meeting**

* Everyone understood Koshkina’s work  
* Team voted the pipeline


## **Discussion During the Meeting**

### **Technical and Organizational Discussion**

* The choose the pipeline that will be used   
* The team discussed the technical issues that might happen during the replications of the Koshkina’s works  
* Each member was assigned the task to complete the project proposal.

### **Project Proposal Timeline**

* Team agreed to have final draft of project proposal by Tuesday 24, 2026 

## **Role Assignments and Responsibilities**

* Karo will work on proposed pipeline sections  
* Enock will work on replication state of art results and experiment design sections   
* Aaditya will work on related work and evaluation metrics sections   
* Zhishang will work on introduction, references and team contributions  
* Leila will work on proposed enhancement and performance improvements,and timeline and milestones sections

## **Decisions Made**

* Creating new repository which clones Koshkina work and giving access to everyone   
* Updating everyone’s progress on discord  
* Creating final project proposal draft by Feb 24

## **Next Meeting**

**Date:** Wednesday, 25 February 2026  
**Time:** 7:30 PM

# **Meeting 5 (24 Feb 2026**

# **Meeting 5**

**Date:** February 25, 2026  
**Time:** 7:30 PM – 8:00 PM  
**Format:** Discord  
**Location:** Discord call  
**Attendees:** Karo, Aaditya, Leila, Enock, Zhishang

**Written By:** Leila

## **Work Completed Before the Meeting**

* Karo,Aaditya, Leiala and Zhishang were completed the final draft for their assigned task  
* New repository was created and everyone has access

## **Discussion During the Meeting**

### **Technical and Organizational Discussion**

* Team had difficulties of running the project because of limitations of GPU, dependences issues, and discussed on how they can run the project including buying colab Pro+

### **Project Proposal Timeline**

* The team agreed to set the final submission for Friday. Enock was unable to complete his sections because he encountered challenges running Koshkina’s work, and his part depends on obtaining those results.

## **Role Assignments and Responsibilities**

* Each team has to put personal reflections in google docs, read all parts of draft and corrects parts  where correction is needed  
* To run the code so that Enock can get results to complete the sections

## **Decisions Made**

* Focusing on running the code to get results  
* Reviewing draft for corrections   
* Organizing the sections in program proposal 

## **Next Meeting**

**Date:**  February 26, 2026  
**Time:** 9:00 PM

# **Meeting 6 (26 Feb 2026\)**

# **Meeting 6**

**Date:** February 26, 2026  
**Time:** 9:00 PM – 9:40 PM  
**Format:** Discord  
**Attendees:** Karo, Aaditya, Leila, Enock

**Written By:** Aaditya

## **Work Completed Before the Meeting**

* Enock and Leila have successfully bought the pro accounts and have been able to run the pipeline and submit screenshots.  
* Everyone has submitted their parts of project proposal.  
* Aaditya and Leila have added relevant feedback to certain parts.  
* Leila has compiled the sections into a final doc and addressed feedback  
* Enock and Karo have also addressed the relevant feedback

## **Discussion During the Meeting**

### **Technical and Organizational Discussion**

* The team identified and discussed our final draft of the project proposal and the progress journal.

### **Project Proposal Timeline**

* The team agreed that we will submit our work tomorrow later in the evening by 9:00pm and we have agreed to work on fixing the citations, formatting and related issues

## **Role Assignments and Responsibilities**

* Aaditya volunteered to do team log.  
* Enock volunteered to compile everything for the progress journal  
* Leila will work on the appendix, her citations and the final progress journal submission  
* Karo will work on fixing her citations as well.  
* The team will reconvene on discord before final submission.

## **Decisions Made**

* Maintain consistent communication till submission tomorrow  
* Work on our designated parts and help others out if lacking  
* Compile and submit tomorrow(27 February 2026\) by our deadline of 9:00pm

## **Next Meeting**

**Date:** March 1st week (TBD)  
**Time:** TBD

# **Meeting 7(5 Mar 2026\)**

# **Meeting 7**

**Date:** March 5, 2026

**Time:** Evening (approx. 8:30 PM – 9:00 PM)

**Format:** Online (Video Call)

**Attendees:** Karo Li, Aaditya Golash, Leila Saparbek, Enock Mutabazi, Zhishang Ma

 **Written By:** Leila

## **Work Completed Before the Meeting**

•        Project proposal submitted to the TA for evaluation.

•        Leila successfully replicated and ran the full baseline pipeline in Google Colab, confirming 87.12% accuracy (1,055/1,211 tracklets correct).

•        Enock independently replicated the baseline pipeline, achieving identical results (87.12%), confirming reproducibility.

•        Aaditya attempted to run the pipeline on a friend's GPU; encountered repeated crashes.

•        Zhishang attempted local execution but experienced slow performance and pipeline stalls after the image loading step (\~4 hours without completion).

## **Discussion During the Meeting**

**Pipeline Execution & Environment Setup**

•        The team agreed that Google Colab Pro or Pro+ is necessary for efficient GPU access. Members were encouraged to upgrade individually if their other coursework also requires it.

**Implementation Planning: Top-K Keyframe Selection**

•        The team identified Top-K keyframe selection as the immediate implementation priority for Week 2, consistent with the project timeline.

•        the team agreed on a research-first approach: each member will draft a short plan outlining how they would implement Top-K (methods, packages, steps), and the team will compare and select the best approach on Sunday.

•        Members were encouraged to re-read the Balaji et al. (2023) paper and review the structure of the Koshkina pipeline code to understand how Top-K can be inserted without breaking existing stages.

**Code Familiarity & Repository Structure**

•        The team noted that the Koshkina pipeline is structured as a series of independent scripts, each taking the output of the previous stage as input.

•        All members were asked to familiarize themselves with the input/output format of each pipeline stage before the Sunday meeting, even if they cannot run the code end-to-end.

•        Members may add progress bars or print statements to the scripts to improve visibility during long runs.

•        The team discussed that the recognition stage (PARSeq, \~78 images/sec) is the dominant runtime bottleneck. Top-K selection is expected to provide a direct computational speedup by reducing the number of frames passed to the recognizer.

## **Decisions Made**

•        Each member will independently draft a short Top-K implementation plan (methods, packages, pseudocode outline) and submit it to the group Discord before Sunday 8:00 AM.

•        The team will meet on Sunday at 2:00 PM to review submitted plans, select the best approach, and delegate implementation subtasks.

•        GPU access will be managed via individual Colab Pro/Pro+ subscriptions where needed.

•        All members should be familiar with the Koshkina pipeline structure and the role of each script before Sunday's meeting.

## **Action Items**

•        **All members**: Research and draft a short Top-K keyframe selection implementation plan. Submit to Discord before Sunday 8:00 AM (March 8, 2026).

•        **All members**: Review the Koshkina repository structure and understand the input/output of each pipeline stage.

## **Next Meeting**

**Date:** Sunday, March 8, 2026

**Time:** 2:00 PM

**Format:** Online

**Agenda:** Review Top-K implementation proposals, select approach, delegate implementation subtasks.

# Meeting 8 (8 Mar 2026\)

# **Meeting 8: Top-K Strategy & Execution Roadmap**

**Date:** March 8, 2026

**Time:** 2:00 PM – 3;00 PM

**Format:** Online (Video Call)

**Attendees:** Aaditya Golash, Karo Li, Leila Saparbek, Enock Mutabazi, Zhishang Ma

**Written By:** Karo

### **1\. Pre-Meeting Progress & Baseline Status**

* All team members submitted individual implementation proposals for the Top-K keyframe selection. Before this meeting, everyone reviewed each other's proposals to identify the most feasible technical path.

**2\. Technical Discussion & Final Decisions**

* Algorithm Selection: The team officially pivoted away from KFA-ID (Key Frame Abstraction). The consensus is that KFA-ID introduces unnecessary complexity (requiring its own network). Instead, the team will implement a Top-K Sorting Algorithm that uses existing legibility scores as the ranking proxy.  
* Intervention Point: The Top-K filter will be injected as a discrete stage in main.py, sitting specifically between the Legibility Classifier and Pose Detection stages.  
* Optimization Strategy: To address runtime bottlenecks (specifically in PARSeq), the Top-K filter will reduce the number of frames passed to the recognizer, theoretically improving both speed and accuracy by removing "noisy" (low-legibility) frames.

### **3\. Resource & Development Workflow**

* **Development Tiering:** Members without high-end GPU access will focus on codebase architecture, logic implementation, and documentation.  
* **Evaluation Tiering:** handle the compute-heavy "K-Sweep" experiments using Colab Pro+ to ensure consistent results.  
* **Environment Management:**lead the creation of a standardized environment script to prevent the "dependency hell" encountered in earlier weeks.

---

# **Top-K Implementation: Revised 5-Day Plan**

### **Day 1: Codebase Deep-Dive & Baseline Locking**

**Goal:** Ensure 100% technical alignment before a single line of code is written.

* **Aaditya \+ Zhishang (Codebase Audit):**  
  * Trace main.py to confirm the existence of get\_soccer\_net\_raw\_legibility\_results().  
  * Verify if calling the classifier with threshold=-1 correctly generates the raw scores JSON.  
  * **Critical Check:** Confirm that the frame paths in legible\_dict and scores in the JSON share the exact same index ordering.  
* **Enock (Baseline Validation):**  
  * Execute a full unmodified run to serve as the control group.  
  * Confirm the file path for the raw scores JSON matches the project configuration.  
* **Leila \+ Karo (Environment & Interface):**  
  * Karo will audit the **Aggregation Stage** code to ensure it can automatically ingest the filtered frame list once the Top-K stage overwrites the intermediate JSON files.  
  * Leila ensures all dependencies are locked in the Colab Pro+ environment.

### **Day 2: Core Logic Implementation**

**Goal:** Build the filtering engine and modify the pipeline architecture.

* **Aaditya (Main Script Architecture):**  
  * Implement four key changes in main.py:  
    1. Update the actions dictionary to include "topk".  
    2. Add \--topk\_k to the argument parser (default=5).  
    3. Develop the apply\_topk\_filtering() function to handle dictionary sorting and truncation.  
    4. Inject the Top-K logic block into the soccer\_net\_pipeline() sequence.  
* **Zhishang (Automation & Logging):**  
  * Create shell scripts for the K-sweep ($K=1, 3, 5, 7$) to automate data collection.  
  * Set up the logging structure to capture: accuracy, frame count reduction, and inference latency.  
* **Enock (Technical Peer Review):**  
  * Conduct a code review of Aaditya’s changes to ensure the overwrite of full\_legibile\_path occurs before the Pose stage begins reading.

### **Day 3: Integration & Stress Testing**

**Goal:** Verify the modified pipeline on a small scale to confirm "Go" status for full runs.

* **Aaditya \+ Zhishang (Manual Logic Check):**  
  * Run the pipeline on 20 tracklets. Manually verify the JSON outputs to ensure the highest-scoring frames were actually the ones selected.  
  * Test "edge cases": tracklets with fewer than $K$ frames and empty raw score files.  
* **Enock \+ Leila (End-to-End Trial):**  
  * Perform one full integration run at $K=3$. If the pipeline completes without error and produces a valid prediction file, the team moves to Day 4\.  
* **Karo (Compatibility Confirmation):**  
  * Verify that the filtered list correctly feeds into the confidence-weighted aggregation module without format errors.

### **Day 4: The "K-Sweep" Experiments**

**Goal:** Collect all data points for the ablation study.

* **Enock (High-Compute Run A):** Execute Baseline (Top-K Off), $K=1$, and $K=3$.  
* **Leila (High-Compute Run B):** Execute $K=5$ and $K=7$ in parallel.  
* **Zhishang (Hardware Fallback):** Maintain a local GPU environment to pick up any runs that fail due to Colab timeouts or disconnections.  
* **Karo \+ Aaditya (Live Monitoring):** Monitor the incoming logs for anomalies (e.g., accuracy dipping below 80% or unexpected crashes).

### **Day 5: Analysis, Handoff & Documentation**

**Goal:** Finalize the best $K$ value and document findings for the report.

* **Aaditya (Statistical Analysis):**  
  * Construct the final **Ablation Table**.  
  * Analyze how Top-K affects the "1-vs-2-digit" confusion rate—a key project metric.  
* **Leila (Visualization):**  
  * Generate the **Accuracy-vs-Latency Trade-off** chart using Matplotlib for the final report.  
* **Karo (Integration Handoff):**  
  * Finalize the interface documentation between Top-K and Aggregation to prevent Week 4 integration bugs.  
* **Zhishang (Technical Writing):**  
  * Draft the "Methodology" section for the report, detailing the apply\_topk\_filtering() logic and identified limitations.

---

**Next Meeting:** Monday, March 9, 2026  7:30 PM

# Meeting 9 (9 Mar 2026\)

# **Meeting 9: Top-K Strategy & Execution Roadmap**

**Date:** March 9, 2026

**Time:** 7:30- 7:55

**Format:** Online (Video Call)

**Attendees:** Aaditya Golash, Karo Li, Enock Mutabazi, Zhishang Ma

**Written By:** Aaditya

### **1\. Pre-Meeting Progress & Baseline Status**

* All team members submitted individual implementation proposals for the Top-K keyframe selection. Before this meeting, everyone reviewed each other's proposals to identify the most feasible technical path.   
* We also further reviewed Leila’s implementation plan and discussed the best path forward

**2\. Technical Discussion & Final Decisions**

* We have decided to follow a shorter version of Leila’s top K plan. Aaditya and Zhishang do their work upto day 3, and Enock and Leila follow after along with Karo.  
* We will have work ready to present and deliver by Sunday 8:00am

### **3\. Resource & Development Workflow**

* **Development Tiering:** Members without access to high-end GPUs will focus on codebase architecture, logic implementation, and documentation.  
* **Evaluation Tiering:** handle the compute-heavy "K-Sweep" experiments using Colab Pro+ to ensure consistent results.  
* **Environment Management:**lead the creation of a standardized environment script to prevent the "dependency hell" encountered in earlier weeks.

---

# **Top-K Implementation: Revised Plan**

### **Day 1: Codebase Deep-Dive & Baseline Locking**

**Goal:** Ensure 100% technical alignment before a single line of code is written.

* **Aaditya \+ Zhishang (Codebase Audit):**  
  * Trace main.py to confirm the existence of get\_soccer\_net\_raw\_legibility\_results().  
  * Verify if calling the classifier with threshold=-1 correctly generates the raw scores JSON.  
  * **Critical Check:** Confirm that the frame paths in legible\_dict and scores in the JSON share the exact same index ordering.  
* **Enock (Baseline Validation):**  
  * Execute a full unmodified run to serve as the control group.  
  * Confirm the file path for the raw scores JSON matches the project configuration.  
* **Leila \+ Karo (Environment & Interface):**  
  * Karo will audit the **Aggregation Stage** code to ensure it can automatically ingest the filtered frame list once the Top-K stage overwrites the intermediate JSON files.  
  * Leila ensures all dependencies are locked in the Colab Pro+ environment.

### **Day 2: Core Logic Implementation**

**Goal:** Build the filtering engine and modify the pipeline architecture.

* **Aaditya (Main Script Architecture):**  
  * Implement four key changes in main.py:  
    1. Update the actions dictionary to include "topk".  
    2. Add \--topk\_k to the argument parser (default=5).  
    3. Develop the apply\_topk\_filtering() function to handle dictionary sorting and truncation.  
    4. Inject the Top-K logic block into the soccer\_net\_pipeline() sequence.  
* **Zhishang (Automation & Logging):**  
  * Create shell scripts for the K-sweep ($K=1, 3, 5, 7$) to automate data collection.  
  * Set up the logging structure to capture: accuracy, frame count reduction, and inference latency.  
* **Enock (Technical Peer Review):**  
  * Conduct a code review of Aaditya’s changes to ensure the overwrite of full\_legibile\_path occurs before the Pose stage begins reading.

### **Day 3: Integration & Stress Testing**

**Goal:** Verify the modified pipeline on a small scale to confirm "Go" status for full runs.

* **Enock \+ Leila (End-to-End Trial):**  
  * Perform one full integration run at $K=3$. If the pipeline completes without error and produces a valid prediction file, the team moves to Day 4\.  
* **Karo (Compatibility Confirmation):**  
  * Verify that the filtered list correctly feeds into the confidence-weighted aggregation module without format errors.

### **Day 4: The "K-Sweep" Experiments**

**Goal:** Collect all data points for the ablation study.

* **Enock (High-Compute Run A):** Execute Baseline (Top-K Off), $K=1$, and $K=3$.  
* **Leila (High-Compute Run B):** Execute $K=5$ and $K=7$ in parallel.  
* **Zhishang (Hardware Fallback):** Maintain a local GPU environment to pick up any runs that fail due to Colab timeouts or disconnections.

---

**Next Meeting:** Sunday, March 15, 2026  2:00 PM

# Meeting 10 (15 Mar 2026\)

# **Meeting 10: Top-K Strategy & Execution Roadmap P2**

**Date:** March 15, 2026

**Time:** 2:00-2:30pm

**Format:** Online (Video Call)

**Attendees:** Aaditya Golash, Karo Li, Zhishang Ma

**Written By:** Aaditya

### **1\. Pre-Meeting Progress & Baseline Status**

* Team members did work and provided updates

**2\. Technical Discussion & Final Decisions**

* We have decided to follow up in a few days and keep researching and working.

### **3\. Resource & Development Workflow**

* **Development Tiering:** Members without access to high-end GPUs will focus on codebase architecture, logic implementation, and documentation.  
* **Evaluation Tiering:** handle the compute-heavy "K-Sweep" experiments using Colab Pro+ to ensure consistent results.  
* **Environment Management:**lead the creation of a standardized environment script to prevent the "dependency hell" encountered in earlier weeks.

---

**Next Meeting:** Tuesday, March 17, 2026  5:00 PM

# Meeting 11 (17 Mar 2026\)

# **Meeting 11: Top-K Strategy & Execution Roadmap P2**

**Date:** March 17, 2026

**Time:** 5:00-5:30pm

**Format:** Online (Video Call)

**Attendees:** Aaditya Golash, Karo Li, Zhishang Ma, Enock, Leila

**Written By:** Aaditya

### **1\. Pre-Meeting Progress & Baseline Status**

* Team members did work and provided updates

**2\. Technical Discussion & Final Decisions**

* We have decided to follow up final implementation and results from Top-K  
* Propose implementation plans for the next part of pipeline and distribution of work.

### **3\. Resource & Development Workflow**

* **Development Tiering:** Members without access to high-end GPUs will focus on codebase architecture, logic implementation, and documentation.  
* **Evaluation Tiering:** handle the compute-heavy "K-Sweep" experiments using Colab Pro+ to ensure consistent results.  
* **Environment Management:**lead the creation of a standardized environment script to prevent the "dependency hell" encountered in earlier weeks.

**4\. Role Assignments and Responsibilities**

* Aaditya volunteered to do a team log and propose an implementation plan.  
* Leila will work on running top \-K along with enock  
* Karo and Zhishang will work on their parts pre assigned as well.  
* Team will all propose implementation plans  
* The team will reconvene on discord.

---

**Next Meeting:** TBD

# Meeting 12 (24 Mar 2026\)

# **Meeting 12: Top-K Strategy & Execution Roadmap P2**

**Date:** March 24, 2026

**Time:** 5:00-5:30pm

**Format:** Online (Video Call)

**Attendees:** Aaditya Golash, Karo Li, Zhishang Ma, Enock, Leila

**Written By:** Aaditya

### **1\. Pre-Meeting Progress & Baseline Status**

* Team members did work and provided updates

**2\. Technical Discussion & Final Decisions**

* We discussed the challenges we are facing for improving accuracy  for Top-K and multi task  
* Proposed the better way to improve the accuracy and having consistency accuracy

### **3\. Resource & Development Workflow**

* **Development Tiering:** Members without access to high-end GPUs will focus on codebase architecture, logic implementation, and documentation.  
* **Evaluation Tiering:** handle the compute-heavy "K-Sweep" experiments using Colab Pro+ to ensure consistent results.  
* **Environment Management:**lead the creation of a standardized environment script to prevent the "dependency hell" encountered in earlier weeks.

**4\. Role Assignments and Responsibilities**

* Everyone will have draft for progress journal  
* Reviewing Liela’s branch on github

---

**Next Meeting:** 25th March 2026

# Meeting 13 (25 Mar 2026\)

# **Meeting 13: Top-K Strategy & Execution Roadmap P2**

**Date:** March 25, 2026

**Time:** 10:00 \-11: 00 AM

**Format:** Online (Video Call)

**Attendees:** Aaditya Golash, Karo Li, Zhishang Ma, Enock, Leila

**Written By:** Aaditya

### **1\. Pre-Meeting Progress & Baseline Status**

* Team members did work and provided updates

**2\. Technical Discussion & Final Decisions**

* We discussed the challenges we are facing for improving accuracy  for Top-K and multi task  
* Proposed the better way to improve the accuracy and having consistency accuracy  
* We discussed what will do if we are not able to improve the accuracy  
* We discussed the presentations and final reports

### **3\. Resource & Development Workflow**

* **Development Tiering:** Members without access to high-end GPUs will focus on codebase architecture, logic implementation, and documentation.  
* **Evaluation Tiering:** handle the compute-heavy "K-Sweep" experiments using Colab Pro+ to ensure consistent results.  
* **Environment Management:**lead the creation of a standardized environment script to prevent the "dependency hell" encountered in earlier weeks.

**4\. Role Assignments and Responsibilities**

* Enock: revise pipeline, cleaning github repo and documenting missing logs  
* Liela: Revise pipeline and canva presentation   
* Aaditya: completing progress journals and prepare canva presentation   
* Zhishang: canva presentation   
* Karo:canva presentation   
* Everyone: completing individual progress journal

---

**Next Meeting:** 27th March 2026 9:30 PM

# Meeting 14 (27 Mar 2026\)

# **Meeting 14: Top-K Strategy & Execution Roadmap P2**

**Date:** March 27, 2026

**Time:**9:30 PM \- 9:45 PM

**Format:** Online (Video Call)

**Attendees:** Aaditya Golash, Karo Li, Zhishang Ma, Enock, Leila

**Written By:** Aaditya

### **1\. Pre-Meeting Progress & Baseline Status**

* Team members did work and provided updates

**2\. Technical Discussion & Final Decisions**

* We discussed the challenges we are facing for improving accuracy  for Top-K and multi task  
* Proposed the better way to improve the accuracy and having consistency accuracy  
* We discussed what will do if we are not able to improve the accuracy  
* We discussed the presentations and final reports

### **3\. Resource & Development Workflow**

* **Development Tiering:** Members without access to high-end GPUs will focus on codebase architecture, logic implementation, and documentation.  
* **Evaluation Tiering:** handle the compute-heavy "K-Sweep" experiments using Colab Pro+ to ensure consistent results.  
* **Environment Management:**lead the creation of a standardized environment script to prevent the "dependency hell" encountered in earlier weeks.

**4\. Role Assignments and Responsibilities**

* Everyone : provide personal reflections  
* Everyone: provide updates for final implementations

---

**Next Meeting:** 28th March 2026 1 PM
