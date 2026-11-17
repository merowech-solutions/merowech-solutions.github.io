---
title: Visual Explainable AI für Zeitreihen: Attributionen, Counterfactuals und Modellvertrauen
subtitle: Wie die Dissertation unseres Gründers Udo Schlegel an der Universität Konstanz unsere Beratungspraxis für erklärbares Machine Learning und Data Science prägt.
date: 2026-11-17
date_label: FORSCHUNGSFUNDAMENT
read_time: 8 MIN LESEZEIT
topic: EXPLAINABLE AI × MACHINE LEARNING
tags: Explainable AI, Machine Learning, Data Science, Time Series
slug: visual-explainable-ai-fuer-zeitreihen-dissertation
alt_slug: visual-explainable-ai-for-time-series-dissertation
---

Bei Merowech Solutions ruht unsere Arbeit in **Machine Learning**, **Data Science** und **Explainable AI (XAI)** unmittelbar auf begutachteter wissenschaftlicher Forschung. Ein zentraler Baustein dieses Fundaments ist die Informatik-Dissertation unseres Gründers Udo Schlegel an der Universität Konstanz (Arbeitsgruppe Data Analysis and Visualization — DBVIS): ***Visual Explainable AI for Time Series Classification: The potential of attributions and counterfactuals***.

Tiefe neuronale Netze und moderne Ensemble-Verfahren erzielen auf sequenziellen und operativen Daten – von industrieller Sensortelemetrie und Energielastgängen bis hin zur medizinischen Diagnostik – herausragende Klassifikations- und Prognosegüten. Gleichzeitig bleibt ihre interne Entscheidungslogik häufig eine Black Box. Im Folgenden geben wir einen Einblick in die Kernergebnisse der Dissertation, die zugehörigen Open-Source-Bibliotheken und wie wir diese Methodik heute in produktive Machine-Learning-Projekte einbringen.

:::callout Open-Access-Dissertation, Forschungsportal & Quellcode
Die vollständige Dissertation ist frei zugänglich auf [KOPS (Universität Konstanz)](https://kops.uni-konstanz.de/entities/publication/4e108aaf-2cf9-4cfb-bc98-2730b512880b/full). Interaktive Übersichten und Publikationen finden Sie unter [time-series-xai.dbvis.de](https://time-series-xai.dbvis.de/), sämtliche PyTorch- und Visual-Analytics-Implementierungen unter [github.com/visual-xai-for-time-series](https://github.com/visual-xai-for-time-series).
:::

## 1. Warum klassische XAI-Verfahren auf Zeitreihen zu kurz greifen

Weit verbreitete Post-hoc-Erklärverfahren – etwa Saliency Maps, Integrated Gradients, LIME oder SHAP – wurden ursprünglich für Bilder, Text-Tokens oder unabhängige Tabellenmerkmale entworfen. Werden sie unkritisch auf kontinuierliche Zeitreihen übertragen, entstehen systematische Schwachstellen:

- **Autokorrelation und Phasenverschiebungen:** Einzelne Zeitpunkte tragen selten isolierte Bedeutung; entscheidend sind lokale Verlaufsformen, Steigungen, Frequenzmuster und mehrkanalige Übergänge.
- **Visuelle Überlastung bei naiven Heatmaps:** Tausende farbig hinterlegte Einzelzeitpunkte erzeugen auf langen Sequenzen oft visuelles Rauschen statt belastbarer Erkenntnisse für Fachexperten.
- **Strukturierte Taxonomie für Zeitreihen-XAI:** Die Dissertation ordnet das Forschungsfeld systematisch in **zeitpunktbasierte**, **teilsequenzbasierte** und **instanzbasierte** Erklärungsansätze.

## 2. Quantitative Prüfung von Faithfulness und Stabilität

Eine optisch ansprechende Relevanzkurve garantiert noch nicht, dass sie das tatsächliche Berechnungsverhalten des Modells korrekt widerspiegelt. Ein Schwerpunkt der Arbeit liegt daher auf der **perturbationsbasierten Evaluierung** zeitlicher Erklärungen – darunter Robustheitsmaße wie der **Attribution Stability Indicator (ASI)**.

| Prüfdimension | Zentrale Forschungsfrage | Nutzen in unseren Beratungsprojekten |
| --- | --- | --- |
| Perturbations-Faithfulness | Sinkt die Modellkonfidenz erwartungsgemäß, wenn hoch relevante Zeitfenster durch realistische Referenzen ersetzt werden? | Schützt Ihr Team vor trügerischen, ungeprüften Post-hoc-Heatmaps |
| Attributionsstabilität (ASI) | Bleiben Erklärungen unter geringfügigen, fachlich plausiblen Signalvariationen konsistent? | Trennt echte gelernte Signalmuster von instabilen Gradienten-Artefakten |
| Visuelle Kodierung | Wie lassen sich Relevanzen über einzelne Kurven und große Datensätze hinweg verzerrungsfrei darstellen? | Dense-Pixel-Ansichten und abgestimmte Linienkodierungen verhindern Fehlinterpretationen |

In unseren Modell-Audits bei Merowech Solutions übertragen wir genau diesen Prüfstandard auf **tabellarische ebenso wie auf sequenzielle Machine-Learning-Systeme**: Keine Erklärungsoberfläche geht ohne quantitative Verifikation in den Betrieb.

## 3. Attributionen („Warum?“) und Counterfactuals („Was-wäre-wenn?“) vereinen

Attributionen zeigen, *wohin* ein Modell blickt – welche Zeitabschnitte oder Merkmalsfenster eine Klassifikation am stärksten beeinflusst haben. In Technik, Qualitätswesen und Fachbereichen zählt jedoch ebenso die kontrastive Gegenfrage: ***Welche minimale, fachlich realistische Änderung des Verlaufs würde die Modellentscheidung umkehren?***

Die Dissertation verbindet beide Perspektiven zu einem durchgängigen Ansatz aus **Attributionen** und **Counterfactual Explanations**:

1. **Gezieltes Aufdecken von Scheinkorrelationen:** Kippt eine Prognose bereits durch minimale Änderungen außerhalb des physikalisch relevanten Bereichs, nutzt das Modell einen fragilen Shortcut (*Clever-Hans*-Effekt) statt robuster Fachzusammenhänge.
2. **Interaktive Hypothesenprüfung:** *What-If*-Analysen erlauben es Ihren Fachexperten, Entscheidungsgrenzen direkt zu erproben und mit realen Prozesstoleranzen abzugleichen.
3. **Offene Referenzimplementierungen:** Modulare Algorithmen und Benchmarks stehen unter [counterfactual-explanations-for-time-series](https://github.com/visual-xai-for-time-series/counterfactual-explanations-for-time-series) sowie [visual-explanations-on-time-series](https://github.com/visual-xai-for-time-series/visual-explanations-on-time-series) bereit.

## 4. Von lokalen Einzelprüfungen zu globaler Visual Analytics

Die isolierte Betrachtung einzelner Beispiele reicht nicht aus, um systematische Modellschwächen in großen Datenbeständen zu erkennen. Durch die Kombination aus **Dense-Pixel-Visualisierungen** ([dense-time-series-attributions](https://github.com/visual-xai-for-time-series/dense-time-series-attributions)) und zweidimensionalen Projektionen schafft die Arbeit einen nahtlosen Übergang zwischen zwei Ebenen:

- **Globale Modellübersichten:** Projektion datensatzweiter Attributionen und Counterfactual-Muster zur Identifikation von Modellstrategien, Grenzfällen und systematischen Fehlergruppen.
- **Lokale Detaildiagnostik:** Gezieltes Hineinzoomen in einzelne Sequenzen, Relevanzfenster und kontrastive Gegenbeispiele zur Ursachenanalyse.

## 5. Wie diese Forschung unsere Mandate bei Merowech Solutions stärkt

Während die Zeitreihenklassifikation in der Dissertation als anspruchsvolles Prüffeld diente, prägt die zugrunde liegende Methodik – **quantitative XAI-Validierung, kontrastives Counterfactual-Auditing und nutzerzentrierte Visual Analytics** – heute unsere gesamte Beratungspraxis in Data Science und Machine Learning:

- Systematische Prüfung produktiver **tabellarischer, tiefer und zeitbasierter ML-Modelle** auf Data Leakage und Scheinkorrelationen vor dem Go-Live.
- Entwicklung **verständlicher visueller Diagnosewerkzeuge**, mit denen Fachbereiche Modellentscheidungen eigenständig nachvollziehen können.
- Aufbau **prüffähiger Transparenz- und Human-in-the-Loop-Prozesse** für geschäftskritische Anwendungen und den EU AI Act.

### Primärquellen & Open-Source-Ressourcen

- **Dissertation im Volltext (KOPS, Universität Konstanz):** [Visual Explainable AI for Time Series Classification: The potential of attributions and counterfactuals](https://kops.uni-konstanz.de/entities/publication/4e108aaf-2cf9-4cfb-bc98-2730b512880b/full)
- **Forschungsportal & Interaktive Übersichten:** [time-series-xai.dbvis.de](https://time-series-xai.dbvis.de/)
- **Open-Source GitHub-Organisation:** [github.com/visual-xai-for-time-series](https://github.com/visual-xai-for-time-series)
