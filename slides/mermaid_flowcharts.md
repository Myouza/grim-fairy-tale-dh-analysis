# Mermaid Flowcharts for Presentation

## Flowchart 1: Two-Stage Validation Design

```mermaid
flowchart TB
    subgraph Stage1["STAGE 1: Ground Truth"]
        A1[Songs of Memory<br/>300k words] --> A2[I know every branch]
        A2 --> A3[Develop extraction prompt]
        A3 --> A4[Verify: captures known structure?]
        A4 --> A5[✓ Prompt calibrated]
    end
    
    subgraph Stage2["STAGE 2: Blind Replication"]
        B1[小红帽<br/>Random selection] --> B2[First encounter<br/>day of experiment]
        B2 --> B3[Same prompt<br/>zero modifications]
        B3 --> B4[Verify: transfers to unknown?]
        B4 --> B5[✓ This repository]
    end
    
    A5 --> B1
    
    style Stage1 fill:#e8f4e8,stroke:#4a7c4a
    style Stage2 fill:#e8e8f4,stroke:#4a4a7c
```

## Flowchart 2: Extraction Pipeline

```mermaid
flowchart LR
    subgraph Input["Raw Game"]
        A[RPG Maker .exe]
    end
    
    subgraph Extract["Extraction"]
        B[Ruby Script<br/>one-click dump]
        C[EventTextDump.txt<br/>84,123 lines]
        D[LLM Prompt<br/>game-agnostic]
        E[narrative_extraction.md<br/>Arc→Sequence→Beat]
    end
    
    subgraph Analyze["Analysis"]
        F[Python Experiments<br/>parameterized]
        G[26 figures<br/>8 tables<br/>4 metrics]
    end
    
    A --> B --> C --> D --> E --> F --> G
    
    style Input fill:#f4e8e8,stroke:#7c4a4a
    style Extract fill:#e8f4e8,stroke:#4a7c4a
    style Analyze fill:#e8e8f4,stroke:#4a4a7c
```

## Flowchart 3: What the Experiments Test

```mermaid
flowchart TB
    Data[Extracted Data] --> Q1{Can we test<br/>hypotheses?}
    Data --> Q2{Can we calculate<br/>spatial metrics?}
    Data --> Q3{Can we run<br/>network analysis?}
    Data --> Q4{Can we track<br/>symbols over time?}
    
    Q1 --> E1[Exp 1: Structural Alignment<br/>76.9% correspondence]
    Q2 --> E2[Exp 2: Narrative Density<br/>162 maps analyzed]
    Q3 --> E3[Exp 3: Semantic Network<br/>28 nodes, 4 communities]
    Q4 --> E4[Exp 4: Motif Evolution<br/>380 instances tracked]
    
    E1 --> V[✓ Data is DH-ready]
    E2 --> V
    E3 --> V
    E4 --> V
    
    style Data fill:#f4f4e8,stroke:#7c7c4a
    style V fill:#e8f4e8,stroke:#4a7c4a
```

## Flowchart 4: The Bigger Pipeline

```mermaid
flowchart TB
    A[Dark Archive<br/>thousands of games] --> B[Extraction Pipeline<br/>← current work]
    B --> C[Formal Verification<br/>Stability Analysis]
    C --> D[DH Methods<br/>with guarantees]
    D --> E[Corpus-Scale<br/>Cultural Analysis]
    
    style A fill:#f4e8e8,stroke:#7c4a4a
    style B fill:#e8f4e8,stroke:#4a7c4a,stroke-width:3px
    style C fill:#e8e8f4,stroke:#4a4a7c
    style D fill:#f4e8f4,stroke:#7c4a7c
    style E fill:#f4f4e8,stroke:#7c7c4a
```

## Flowchart 5: Validation Logic (Simple)

```mermaid
flowchart LR
    S1[Stage 1<br/>Known Ground Truth] -->|Tests| Accuracy
    S2[Stage 2<br/>Unknown Game] -->|Tests| Transferability
    
    Accuracy --> Both[Both Required<br/>for Valid Pipeline]
    Transferability --> Both
    
    style S1 fill:#e8f4e8,stroke:#4a7c4a
    style S2 fill:#e8e8f4,stroke:#4a4a7c
    style Both fill:#f4f4e8,stroke:#7c7c4a
```

---

## Usage Notes

Copy each mermaid code block into:
- [Mermaid Live Editor](https://mermaid.live/) to export as PNG/SVG
- Or use mermaid-cli: `mmdc -i flowchart.mmd -o flowchart.png`

Recommended exports:
- **Flowchart 1** (Two-Stage): Use for explaining validation design
- **Flowchart 2** (Pipeline): Use for "how it works" slide
- **Flowchart 3** (Experiments): Use for experiment overview
- **Flowchart 4** (Bigger Picture): Use for closing/context slide
