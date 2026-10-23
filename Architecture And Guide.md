# MuseEngine: Cognitive Imagination & Non-Linear Ideation Architecture

## Why a Stateful Cognitive Middleware Outperforms Single-Pass Prompting

Standard LLM agents fail at genuine breakthroughs in **scientific hypothesis generation** and **software architecture** for a structural reason: autoregressive next-token prediction rewards **local semantic plausibility** (staying inside the highest-probability neighborhood of training data). Human imagination does the exact opposite—it extracts the **abstract relational skeleton** of a problem, leaps across semantic space into a distant domain with an isomorphic skeleton, allows unfinished problems to simmer in background **Default-Mode Network (DMN)** memory, uses **embodied "felt-sense" intuition** to sense structural brittleness or elegance, and oscillates between **lawless divergence** and **Popperian/architectural stress-testing**.

Pure prompt templates cannot maintain episodic Zeigarnik tension across sessions, nor can they prevent an LLM from collapsing back into safe, textbook averages during generation. **MuseEngine** solves this by operating as a **Dual-Mode Stateful Middleware & Cognitive Orchestrator**:

| Architectural Layer | Role in the Agent Stack | Why It Beats Standard Prompting |
| :--- | :--- | :--- |
| **Drop-In Agent Middleware (`MuseMiddleware`)** | Wraps any `agent(messages)` or `llm(prompt)` callable transparently | Intercepts the problem *before* the LLM locks into a narrow domain distribution, injecting isomorphic operators from distant domains and non-dominated Pareto hypotheses directly into the system scaffold |
| **Bisociation & Isomorphism Engine (`BisociationEngine`)** | Extracts relational tension graphs & collides them with distant archetypes | Separates *relational structure* (feedback loops, conservation laws, bottlenecks) from *surface vocabulary*, enabling genuine Koestlerian bisociation |
| **Default-Mode Network (`DefaultModeNetwork`)** | Persistent episodic trace buffer with Zeigarnik tension & Levy-flight walks | Unsolved bottlenecks from earlier tasks remain active attractors during stochastic incubation walks, sparking cross-problem serendipity |
| **Embodied Intuition Evaluator (`EmbodiedIntuitionEngine`)** | Scores candidate topologies on kinesthetic & thermodynamic aesthetics | Evaluates *Structural Elegance*, *Laminar Flow*, *Antifragility*, *Productive Weirdness*, and *Metabolic Overhead* before formal deductive pruning |
| **Divergent-Convergent Oscillator (`OscillationController`)** | Alternates between paradoxical inversion and Popperian/chaos stress tests | Retains candidates on the **3D Pareto Frontier** (`Novelty × Rigor × Felt-Sense Resonance`) rather than averaging ideas into mediocre consensus |

## How the 5-Phase Cognitive Cycle Works

### Phase 1: Relational Topology & Tension Extraction (`1_embodied_sensing`)
Instead of indexing a problem by surface keywords (e.g., *"Kubernetes"*, *"Kafka"*, *"Astrocyte"*, *"Amyloid"*), `BisociationEngine.extract_problem_topology()` maps the prompt into:
* **Tension Vectors**: Normalized intensities across structural axes (`coordination_overhead`, `consistency_vs_latency`, `backpressure_congestion`, `clearance_bottleneck`, `toxic_accumulation`, `oscillatory_coupling`, `deadlock_under_contention`, `routing_rigidity`).
* **Conservation Laws**: Hard boundaries the system cannot violate (e.g., *Little's Law $L = \lambda W$* in distributed queues, or the *Monro-Kellie volume-pressure constraint* in intracranial fluid dynamics).
* **Runaway Feedback Loops**: Positive feedback traps that turn minor perturbations into systemic collapse (e.g., retry amplification storms or shear-loss aggregation cascades).

### Phase 2: Bisociative Cross-Domain Collision (`2_bisociative_collision`)
Inspired by Arthur Koestler's *The Act of Creation* and Dedre Gentner's *Structure-Mapping Theory*, the engine computes cosine structural isomorphism between the problem's tension vector and a curated library of distant physical, biological, ecological, and musical archetypes, plus controlled exploration noise ($\pm \epsilon$):

$$\text{Isomorphism}(P, A) = \frac{\sum_{k \in T} P_k \cdot A_k}{\|P\|_2 \, \|A\|_2} + \mathcal{U}(-\epsilon, +\epsilon)$$

Built-in archetypes span five orthogonal domains:
1. **Physarum Polycephalum (Slime Mold) Oscillatory Tube Network** (*Biophysics / Decentralized Morphogenesis*) — Flux-proportional conduit dilation ($D^4$ Poiseuille conductivity), autophagic pruning of starved links, and peristaltic phase-wave signaling without a central coordinator.
2. **Adaptive Immune Repertoire & Thymic Negative Selection** (*Computational Immunology*) — Speculative somatic hypermutation, shadow-thymus negative selection against self-reactive handlers, and two-signal co-stimulation (Event + Local Tissue Stress Context).
3. **Frustrated Spin Glass & Thermal Tunneling** (*Condensed Matter Physics*) — Treating conflicts/inconsistencies as mobile topological defects routed to low-stakes boundaries, paired with targeted stochastic heating of jammed subgraphs.
4. **Estuarine Salt-Wedge Stratification & Tidal Pumping** (*Geophysical Fluid Dynamics*) — Achieving unidirectional net clearance from bidirectional oscillations via phase-lagged side-basin capacitance and critical Richardson-number shear mixing.
5. **Polyphonic Fugue Counterpoint & Stretto Canon** (*Music Theory / Temporal Information Architecture*) — Preventing synchronization spikes by enforcing *contrary motion* between neighbor nodes and anchoring fast volatile streams to a slow pedal-point invariant.

### Phase 3: Default-Mode Network (DMN) Daydreaming & Incubation (`3_dmn_incubation`)
Human breakthroughs frequently arrive during wakeful rest because unfinished problems hold **Zeigarnik tension**—elevated sub-threshold activation that pulls random associative walks toward open bottlenecks. `DefaultModeNetwork.incubate_daydream()` samples stored episodic traces weighted by `zeigarnik_tension` and collides them with active archetypes to emit **Serendipity Sparks** (`SerendipitySpark`), measuring the resulting **Free-Energy Drop** ($\Delta F$):

$$\Delta F = \frac{1}{2} \, Z_{\text{trace}} \cdot A_{\text{shared\_axis}}$$

### Phase 4 & 5: Embodied Felt-Sense & Divergent-Convergent Pareto Oscillation (`4_divergent_expansion` → `5_convergent_critique`)
Each bisociative collision is expanded into a bold, counterfactual hypothesis or architecture, evaluated by `EmbodiedIntuitionEngine` for its **Composite Resonance**:

$$R_{\text{felt}} = 0.28 E_{\text{elegance}} + 0.24 F_{\text{laminar}} + 0.24 A_{\text{antifragile}} + 0.24 W_{\text{weirdness}} - 0.20 M_{\text{overhead}}$$

Finally, `OscillationController` pairs each divergent candidate with explicit **Popperian Falsification Experiments** (for scientific hypotheses) or **Chaos/Jepsen Stress Tests** (for software architectures) and computes the non-dominated **Pareto Frontier** across `(novelty_score, rigor_score, composite_resonance)`.

## Quickstart & Integration Patterns

### 1. Drop-In Decorator for Any LLM Agent Function
Wrap any function that accepts either a prompt string or an OpenAI/Anthropic/Gemini-style `messages` list:

```python
from muse_engine import MuseEngine, MuseMiddleware, TaskDomain

engine = MuseEngine(seed=42)

@MuseMiddleware(engine, attach_report_metadata=True)
def call_agent(messages: list[dict[str, str]]) -> str:
    # Replace with client.chat.completions.create(...) or similar
    # messages[0] now contains the full <COGNITIVE_IMAGINATION_SCAFFOLD> system block!
    return your_llm_client(messages)

result = call_agent([
    {
        "role": "user",
        "content": (
            "Design a zero-coordinator distributed state synchronization and backpressure "
            "mesh that survives 100x hot-key traffic spikes without retry storms."
        ),
    }
])

print(result["response"])
print("Pareto Frontier:", [c.title for c in result["imagination_report"].pareto_frontier])
```

### 2. Direct Multi-Phase Ideation & Custom Archetype Injection
Use `MuseEngine.imagine()` directly when building multi-agent research pipelines or background incubation daemons:

```python
from muse_engine import MuseEngine, TaskDomain

engine = MuseEngine(seed=7)

report = engine.imagine(
    "Generate falsifiable mechanistic hypotheses explaining why age-related arterial "
    "pulsatility loss and astrocyte AQP4 depolarization trigger a sudden nonlinear "
    "collapse in glymphatic clearance and rapid amyloid/tau aggregation.",
    domain=TaskDomain.SCIENTIFIC_HYPOTHESIS,
    top_k_archetypes=3,
    dmn_steps=4,
)

for candidate in report.pareto_frontier:
    print(f"[{candidate.imagination_index}] {candidate.title}")
    print("  Thesis:", candidate.core_thesis)
    print("  Felt-Sense:", candidate.felt_sense.kinesthetic_impression)
    print("  Falsification:", candidate.falsification_or_stress_test[0])
```

## Example Breakthroughs Generated by MuseEngine

### Domain A: Software Architecture (Flash-Crowd State Sync & Backpressure)
* **Estuarine Tidal Ratcheting Topology**: Replaces synchronous central backpressure coordinators with asymmetric request/ack phase-lagged side buffers ("marsh capacitance basins"). High-frequency ingress bursts are absorbed into local phase-shifted ring buffers and drained during counter-phase ebb intervals.
* **Physarum Flux-Conductivity Mesh**: Unifies the routing control plane and data plane—conduit bandwidth allocation scales nonlinearly ($D^4$) with successful ack flux while idle or high-retry paths undergo automatic autophagic pruning, enforcing strict conservation of total cluster in-flight tokens (Little's Law invariant).
* **Spin-Glass Defect Routing**: Instead of stalling partitions on write-write conflicts, materializes state conflicts as first-class mobile "topological defect tokens" that route to commutative resolution boundaries, while injecting targeted stochastic jitter to break synchronized retry herds.

### Domain B: Scientific Hypothesis Generation (Glymphatic Clearance & Neurodegeneration)
* **H1: Estuarine Richardson-Number Shear Threshold Hypothesis**: Proposes that glymphatic perivascular efflux is a rectified tidal ratchet rather than a continuous bulk pump. When age-related arterial pulsatility drops below a critical dimensionless shear threshold (the perivascular Richardson number), dense protein-rich basal interstitial fluid decouples from buoyant cerebrospinal fluid inflow, triggering an abrupt stratification lock-in and local supersaturation nucleation.
  * *Popperian Falsification*: Artificially restoring mean bulk CSF pressure *without* asymmetric pulsatile phase lag must fail to restore clearance, whereas low-amplitude asymmetric acoustic/vasomotor phase-ratcheting must restore clearance even at reduced bulk pressure.
* **H2: Physarum Peristaltic Phase-Wave Decoupling Hypothesis**: Models astrocytic AQP4 endfeet arrays as coupled phase oscillators whose effective hydraulic conductivity scales nonlinearly with vasomotor phase coherence. Depolarization breaks the traveling phase wave into standing-wave dead zones where amyloid-$\beta$ oligomers nucleate.
