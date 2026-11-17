---
title: Visual Explainable AI for Time Series: Attributions, Counterfactuals, and Model Trust
subtitle: How our founder Udo Schlegel’s doctoral dissertation at the University of Konstanz shapes how we audit, debug, and explain machine learning models in practice.
date: 2026-11-17
date_label: RESEARCH FOUNDATION
read_time: 8 MIN READ
topic: EXPLAINABLE AI × MACHINE LEARNING
tags: Explainable AI, Machine Learning, Data Science, Time Series
slug: visual-explainable-ai-for-time-series-dissertation
alt_slug: visual-explainable-ai-fuer-zeitreihen-dissertation
---

At Merowech Solutions, our approach to **Machine Learning**, **Data Science**, and **Explainable AI (XAI)** rests directly on peer-reviewed research. A cornerstone of that foundation is our founder Udo Schlegel’s doctoral dissertation in Computer Science at the University of Konstanz (Data Analysis and Visualization Group — DBVIS): ***Visual Explainable AI for Time Series Classification: The potential of attributions and counterfactuals***.

Deep neural networks and modern ensemble architectures achieve state-of-the-art accuracy on sequential and operational data—from industrial sensor telemetry and energy load profiles to medical diagnostics. Yet their internal decision logic remains largely opaque, limiting trust in high-stakes environments. Below, we share the core scientific contributions of the dissertation, the open-source resources released alongside it, and how we translate these methods into production Machine Learning consulting.

:::callout Open-Access Dissertation, Interactive Portal & Code
Explore the full open-access thesis on [KOPS (University of Konstanz)](https://kops.uni-konstanz.de/entities/publication/4e108aaf-2cf9-4cfb-bc98-2730b512880b/full), browse interactive visual demonstrations at [time-series-xai.dbvis.de](https://time-series-xai.dbvis.de/), and inspect the accompanying PyTorch and visual analytics repositories at [github.com/visual-xai-for-time-series](https://github.com/visual-xai-for-time-series).
:::

## 1. Why Classical XAI Falls Short on Sequential Data

Most widely adopted post-hoc explanation techniques—such as saliency maps, Integrated Gradients, LIME, or SHAP—were originally designed for static images, text tokens, or independent tabular features. Applied naively to continuous temporal data, they run into structural blind spots:

- **Autocorrelation and phase shifts:** Individual time steps rarely carry isolated meaning; discriminative patterns live in localized shapes, gradients, frequency bands, and multi-channel transitions.
- **Cognitive overload in raw heatmaps:** Coloring thousands of consecutive timestamps by point-wise relevance quickly produces visual clutter rather than actionable insight for domain specialists.
- **Taxonomy of temporal explanations:** To bring structure to the field, the dissertation establishes a systematic taxonomy organizing time-series XAI into **time-point-based**, **subsequence-based**, and **instance-based** explanation paradigms.

## 2. Benchmarking Attribution Faithfulness and Stability

An explanation that looks intuitive on a line chart is not necessarily faithful to what the underlying black-box classifier actually computes. A central pillar of the research is rigorous **perturbation-based verification** tailored to temporal structure—including robustness metrics such as the **Attribution Stability Indicator (ASI)**.

| Dimension | Core Research Question | Practical Consulting Takeaway |
| --- | --- | --- |
| Perturbation Faithfulness | Does replacing high-relevance time points or subsequences with realistic baselines degrade confidence as predicted? | Prevents teams from trusting unverified post-hoc heatmaps |
| Attribution Stability (ASI) | Do explanations remain consistent under minor, domain-plausible perturbations? | Separates genuine learned motifs from noisy gradient artifacts |
| Visual Encoding | How should attributions be rendered across single series and large cohorts? | Dense pixel views and enhanced line encodings prevent misinterpretation |

In our client audits at Merowech Solutions, this benchmark-first mindset applies across **both tabular Machine Learning and temporal models**: we never ship an explanation layer without quantitatively verifying its fidelity first.

## 3. Combining Attributions ("Why?") with Counterfactuals ("What-If?")

Attributions highlight *where* a model looks—identifying which time steps or feature windows contributed most to a classification. Yet engineers, clinicians, and plant operators equally need contrastive answers: ***What minimal, realistic change in the signal would flip the model’s decision to another class?***

The dissertation bridges both worlds by uniting **attributions** and **counterfactual explanations** over time:

1. **Error and shortcut discovery:** If minimal modifications outside the physically relevant regime flip a prediction, the model is exploiting a spurious correlation (*Clever-Hans* effect) rather than domain mechanics.
2. **Actionable hypothesis testing:** Interactive *what-if* exploration allows domain experts to probe decision boundaries directly and test whether learned thresholds align with physical tolerances.
3. **Open-source reproducibility:** Modular algorithms and benchmarks are openly available in [counterfactual-explanations-for-time-series](https://github.com/visual-xai-for-time-series/counterfactual-explanations-for-time-series) and [visual-explanations-on-time-series](https://github.com/visual-xai-for-time-series/visual-explanations-on-time-series).

## 4. From Local Inspection to Global Visual Analytics

Inspecting one prediction at a time cannot reveal systematic model weaknesses across millions of operational records. By combining **dense pixel visualizations** ([dense-time-series-attributions](https://github.com/visual-xai-for-time-series/dense-time-series-attributions)) with dimensionality-reduced global projections, the dissertation demonstrates how analysts can move seamlessly between:

- **Global behavior overviews:** Projecting dataset-wide attributions and counterfactual shifts into 2D visual spaces to uncover clusters of model strategies, boundary cases, and systematic misclassifications.
- **Local sample diagnostics:** Drilling down into individual sequences, attribution bands, and counterfactual trajectories to verify root causes.

## 5. How This Research Powers Our Work at Merowech Solutions

While time-series classification served as the rigorous testbed of the dissertation, the underlying methodology—**quantitative XAI evaluation, contrastive counterfactual auditing, and human-centered visual diagnostics**—strengthens every Machine Learning and Data Science system we build with clients:

- Auditing production **tabular, deep learning, and time-series models** for data leakage and spurious shortcuts prior to rollout.
- Designing **operator-ready visual diagnostic tools** so domain specialists can validate model behavior without digging through raw tensors.
- Establishing **auditable transparency and human-oversight workflows** ready for high-stakes operations and the EU AI Act.

### Primary References & Open Resources

- **Doctoral Dissertation (KOPS, University of Konstanz):** [Visual Explainable AI for Time Series Classification: The potential of attributions and counterfactuals](https://kops.uni-konstanz.de/entities/publication/4e108aaf-2cf9-4cfb-bc98-2730b512880b/full)
- **Research Portal & Interactive Demos:** [time-series-xai.dbvis.de](https://time-series-xai.dbvis.de/)
- **Open-Source GitHub Organization:** [github.com/visual-xai-for-time-series](https://github.com/visual-xai-for-time-series)
