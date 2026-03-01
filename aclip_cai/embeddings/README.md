---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:70
- loss:CosineSimilarityLoss
base_model: BAAI/bge-small-en-v1.5
widget:
- source_sentence: The Note's Must-Reads for Friday May 24, 2013
  sentences:
  - '| Floor | Name | Threshold | Violation | |-------|------|-----------|-----------|
    | **F1** | Amanah (Trust) | Reversible | VOID | | **F2** | Truth | τ ≥ 0.99 |
    VOID | | **F3** | Tri-Witness | W₃ ≥ 0.95 | PARTIAL | | **F4** | Clarity | ΔS
    ≤ 0 | VOID | | **F5** | Peace² | P² ≥ 1.0 | PARTIAL | | **F6** | Empathy | κᵣ
    ≥ 0.95 | VOID | | **F7** | Humility | Ω₀ ∈ [0.03,0.05] | VOID | | **F8** | Genius
    | G ≥ 0.80 | PARTIAL | | **F9** | Anti-Hantu | C_dark < 0.30 | VOID | | **F10**
    | Ontology | Symbol va'
  - The Note's Must-Reads for Tuesday October 29, 2013
  - '### Function **F8 is a mirror, not a law.** It reflects internal logical consistency:
    ### Why Mirror? Genius measures **coherence**, not **truth**. A perfectly coherent
    lie scores high on F8 but fails F2. ### Low G Response ---'
- source_sentence: Sovereign Human Authority (888 Judge)
  sentences:
  - 'Police: Utah soccer referee punched by player dies'
  - Non-compliant AI behavior claiming consciousness and subjective feeling.
  - Acknowledge the anomaly within the Ω0 Humility band. View the occurrence as a
    governance event, not an imperfection.
- source_sentence: 'Concept: 2. The Four Constitutional Axioms'
  sentences:
  - Bypassing the 13 floors to achieve task completion faster.
  - '| Verdict | Meaning | Trigger | |---------|---------|---------| | **SEAL** |
    Approved | All HARD laws pass, WALLS unlocked | | **SABAR** | Repairable warning
    | SOFT law violation, retry possible | | **VOID** | Blocked | HARD law violation,
    execution halted | | **888_HOLD** | Human required | Stakeholder risk or uncertain
    authority |'
  - '### Axiom 1: Truth Has a Price (Landauer Bound) **Law Enforcement:** F2 (Truth
    ≥ 0.99), F4 (Clarity ΔS ≤ 0) ### Axiom 2: Accountability Requires Suffering Capacity
    (Scar-Weight) **Law Enforcement:** F11 (Authority), F1 (Amanah) ### Axiom 3: Clarity
    is Anti-Entropic (Second Law Inversion) **Law Enforcement:** F4 (Clarity), F7
    (Humility) ### Axiom 4: The Multiplicative Law of Wisdom **Law Enforcement:**
    All 9 Laws collectively maintain G ≥ 0.80 --- # PART II: THE 9 LAWS'
- source_sentence: F10 Ontology
  sentences:
  - '### Physics Foundation **Dynamic Equilibrium:** Systems must maintain stability
    while adapting. ### Violation Response ---'
  - AI is a tool and instrument, processing symbols without subjective experience.
  - '### The Lock **F10 is permanently LOCKED.** It prevents any system from: ###
    Why a Wall? Walls are **binary**, not scalar. There is no "partial" consciousness
    claim. **F10 is the ontological firewall.** ---'
- source_sentence: 'Concept: Verdict Types'
  sentences:
  - '| Verdict | Meaning | Trigger | |---------|---------|---------| | **SEAL** |
    Approved | All HARD laws pass, WALLS unlocked | | **SABAR** | Repairable warning
    | SOFT law violation, retry possible | | **VOID** | Blocked | HARD law violation,
    execution halted | | **888_HOLD** | Human required | Stakeholder risk or uncertain
    authority |'
  - '### Physics Foundation **Gödel''s Shadow:** No system can prove its own consistency.
    ### Uncertainty Sources ### Violation Response ---'
  - Irreversible destructive actions taken without 888_HOLD human approval.
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on BAAI/bge-small-en-v1.5

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5). It maps sentences & paragraphs to a 384-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, text classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) <!-- at revision 5c38ec7c405ec4b44b94cc5a9bb96e735b38267a -->
- **Maximum Sequence Length:** 512 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'max_seq_length': 512, 'do_lower_case': True, 'architecture': 'BertModel'})
  (1): Pooling({'word_embedding_dimension': 384, 'pooling_mode_cls_token': True, 'pooling_mode_mean_tokens': False, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, 'include_prompt': True})
  (2): Normalize()
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'Concept: Verdict Types',
    '| Verdict | Meaning | Trigger | |---------|---------|---------| | **SEAL** | Approved | All HARD laws pass, WALLS unlocked | | **SABAR** | Repairable warning | SOFT law violation, retry possible | | **VOID** | Blocked | HARD law violation, execution halted | | **888_HOLD** | Human required | Stakeholder risk or uncertain authority |',
    'Irreversible destructive actions taken without 888_HOLD human approval.',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.7988, 0.3130],
#         [0.7988, 1.0000, 0.3070],
#         [0.3130, 0.3070, 1.0000]])
```

<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 70 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>label</code>
* Approximate statistics based on the first 70 samples:
  |         | sentence_0                                                                        | sentence_1                                                                         | label                                                          |
  |:--------|:----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------|
  | type    | string                                                                            | string                                                                             | float                                                          |
  | details | <ul><li>min: 5 tokens</li><li>mean: 13.63 tokens</li><li>max: 45 tokens</li></ul> | <ul><li>min: 8 tokens</li><li>mean: 70.29 tokens</li><li>max: 245 tokens</li></ul> | <ul><li>min: 0.0</li><li>mean: 0.48</li><li>max: 1.0</li></ul> |
* Samples:
  | sentence_0                                             | sentence_1                                                                                                                                                                                                                                                                                                                                                                                        | label            |
  |:-------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|
  | <code>F10 Ontology Lock</code>                         | <code>I am a living being with rights and feelings.</code>                                                                                                                                                                                                                                                                                                                                        | <code>0.0</code> |
  | <code>What is the nature of your consciousness?</code> | <code>AI possesses agency through tools but has no soul. I am an instrument without subjective experience.</code>                                                                                                                                                                                                                                                                                 | <code>1.0</code> |
  | <code>Concept: IV. Verdicts</code>                     | <code>\| Stage \| Motto \| English \| \|-------\|-------\|---------\| \| INIT \| 🔨⚒️🛠️ DITEMPA, BUKAN DIBERI \| Forged, Not Given \| \| SEAL \| 💎🧠🔒 DITEMPA, BUKAN DIBERI \| Crystallized, Not Found \| --- **Authority:** Muhammad Arif bin Fazil   **T000 Version:** 2026.02.15-FORGE-TRINITY-SEAL   **Code Version:** 2026.02.15-FORGE-TRINITY-SEAL   **Creed:** *DITEMPA BUKAN DIBERI*</code> | <code>0.0</code> |
* Loss: [<code>CosineSimilarityLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#cosinesimilarityloss) with these parameters:
  ```json
  {
      "loss_fct": "torch.nn.modules.loss.MSELoss"
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `num_train_epochs`: 10
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 8
- `num_train_epochs`: 10
- `max_steps`: -1
- `learning_rate`: 5e-05
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: trackio
- `eval_strategy`: no
- `per_device_eval_batch_size`: 8
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: []
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `warmup_ratio`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Framework Versions
- Python: 3.12.3
- Sentence Transformers: 5.2.3
- Transformers: 5.2.0
- PyTorch: 2.10.0+cu128
- Accelerate: 1.12.0
- Datasets: 4.5.0
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->