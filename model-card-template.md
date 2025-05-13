<!-- See https://huggingface.co/docs/hub/model-card-annotated for more details. -->

# Model Card for Model ID

<!-- Provide a quick summary of what the model is/does. -->

This modelcard aims to be a base template for new models. It has been generated using [this raw template](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/modelcard_template.md?plain=1).

## Model Details

### Model Description

<!-- Provide basic details about the model. This includes the architecture, version, if it was introduced in a paper, if an original implementation is available, and the creators. Any copyright should be attributed here. General information about training procedures, parameters, and important disclaimers can also be mentioned in this section. -->

[More Information Needed]

<!-- List (and ideally link to) the people who built the model. -->
- **Developed by:** [More Information Needed]
<!-- List (and ideally link to) the funding sources that financially, computationally, or otherwise supported or enabled this model. -->
- **Funded by [optional]:** [More Information Needed]
<!-- List (and ideally link to) the people/organization making the model available online. -->
- **Shared by [optional]:** [More Information Needed]
<!--You can name the "type" as:
1. Supervision/Learning Method
2. Machine Learning Type
3. Modality -->
- **Model type:** [More Information Needed]
- **Language(s) (NLP):** [More Information Needed]
- **License:** [More Information Needed]
- **Finetuned from model [optional]:** [More Information Needed]

### Model Sources [optional]

<!-- Provide the basic links for the model. -->

- **Repository:** [More Information Needed]
- **Paper [optional]:** [More Information Needed]
- **Demo [optional]:** [More Information Needed]

## Uses

<!-- This section addresses questions around how the model is intended to be used in different applied contexts, discusses the foreseeable users of the model (including those affected by the model), and describes uses that are considered out of scope or misuse of the model. Note this section is not intended to include the license usage details. For that, link directly to the license. -->

### Direct Use

<!-- Explain how the model can be used without fine-tuning, post-processing, or plugging into a pipeline. An example code snippet is recommended. -->

[More Information Needed]

### Downstream Use [optional]

<!-- Explain how this model can be used when fine-tuned for a task or when plugged into a larger ecosystem or app. An example code snippet is recommended. -->

[More Information Needed]

### Out-of-Scope Use

<!-- List how the model may foreseeably be misused (used in a way it will not work for) and address what users ought not do with the model. -->

[More Information Needed]

## Bias, Risks, and Limitations

<!-- This section identifies foreseeable harms, misunderstandings, and technical and sociotechnical limitations. It also provides information on warnings and potential mitigations. Bias, risks, and limitations can sometimes be inseparable/refer to the same issues. Generally, bias and risks are sociotechnical, while limitations are technical:
- A bias is a stereotype or disproportionate performance (skew) for some subpopulations.
- A risk is a socially-relevant issue that the model might cause.
- A limitation is a likely failure mode that can be addressed following the listed Recommendations. -->

[More Information Needed]

### Recommendations

<!-- This section is meant to convey recommendations with respect to the bias, risk, and technical limitations. -->

Users (both direct and downstream) should be made aware of the risks, biases and limitations of the model. More information needed for further recommendations.

## How to Get Started with the Model

Use the code below to get started with the model.

[More Information Needed]

## Training Details

<!-- This section provides information to describe and replicate training, including the training data, the speed and size of training elements, and the environmental impact of training. This relates heavily to the Technical Specifications as well, and content here should link to that section when it is relevant to the training procedure. It is useful for people who want to learn more about the model inputs and training footprint. It is relevant for anyone who wants to know the basics of what the model is learning. -->

### Training Data

<!-- This should link to a Dataset Card, perhaps with a short stub of information on what the training data is all about as well as documentation related to data pre-processing or additional filtering. -->

[More Information Needed]

### Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

[More Information Needed]

#### Preprocessing [optional]

<!-- Detail tokenization, resizing/rewriting (depending on the modality), etc. -->

[More Information Needed]

#### Training Hyperparameters

- **Training regime:** [More Information Needed] <!--fp32, fp16 mixed precision, bf16 mixed precision, bf16 non-mixed precision, fp16 non-mixed precision, fp8 mixed precision -->

#### Speeds, Sizes, Times [optional]

<!-- This section provides information about throughput, start/end time, checkpoint size if relevant, etc. -->

[More Information Needed]

## Evaluation

<!-- This section describes the evaluation protocols, what is being measured in the evaluation, and provides the results. Evaluation is ideally constructed with factors, such as domain and demographic subgroup, and metrics, such as accuracy, which are prioritized in light of foreseeable error contexts and groups. Target fairness metrics should be decided based on which errors are more likely to be problematic in light of the model use.  -->

### Testing Data, Factors & Metrics

#### Testing Data

<!-- This should link to a Dataset Card if possible. -->

[More Information Needed]

#### Factors

<!-- What are the foreseeable characteristics that will influence how the model behaves? This includes domain and context, as well as population subgroups. Evaluation should ideally be disaggregated across factors in order to uncover disparities in performance. -->

[More Information Needed]

#### Metrics

<!-- These are the evaluation metrics being used, ideally with a description of why. -->

[More Information Needed]

### Results

<!-- Results should be based on the Factors and Metrics defined above. -->

[More Information Needed]

#### Summary

<!-- What do the results say? This can function as a kind of tl;dr for general audiences. -->

[More Information Needed]

## Model Examination [optional]

<!-- Relevant explainability/interpretability work for the model goes here -->

[More Information Needed]

## Environmental Impact

<!-- Total emissions (in grams of CO2eq) and additional considerations, such as electricity usage, go here. Edit the suggested text below accordingly -->

Carbon emissions can be estimated using the [Machine Learning Impact calculator](https://mlco2.github.io/impact#compute) presented in [Lacoste et al. (2019)](https://arxiv.org/abs/1910.09700).

- **Hardware Type:** [More Information Needed]
- **Hours used:** [More Information Needed]
- **Cloud Provider:** [More Information Needed]
- **Compute Region:** [More Information Needed]
- **Carbon Emitted:** [More Information Needed]

## Technical Specifications [optional]

### Model Architecture and Objective

[More Information Needed]

### Compute Infrastructure

[More Information Needed]

#### Hardware

<!-- What are the minimum hardware requirements, e.g. processing, storage, and memory requirements? -->

[More Information Needed]

#### Software

[More Information Needed]

## Citation [optional]

<!-- If there is a paper or blog post introducing the model, the APA and Bibtex information for that should go in this section. -->

**BibTeX:**

[More Information Needed]

**APA:**

[More Information Needed]

## Glossary [optional]

<!-- If relevant, include terms and calculations in this section that can help readers understand the model or model card. -->

[More Information Needed]

## More Information [optional]

[More Information Needed]

## Model Card Authors [optional]

[More Information Needed]

## Model Card Contact

[More Information Needed]