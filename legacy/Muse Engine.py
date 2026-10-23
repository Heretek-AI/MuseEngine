"""
MuseEngine: Cognitive Imagination & Non-Linear Ideation Middleware for AI Agents
================================================================================

A framework-agnostic Python middleware and stateful cognitive architecture that
endows AI agents with four core mechanisms of human creative imagination:

1. Bisociation & Distant Analogy Engine (Koestler / Gentner Structure-Mapping)
   - Extracts domain-agnostic relational topologies from problems in Scientific
     Hypothesis Generation and Software Architecture.
   - Collides problems with distant domains (immunology, statistical physics,
     mycelial networks, jazz counterpoint, fluid dynamics, developmental biology)
     by maximizing structural isomorphism while maximizing semantic distance.

2. Default-Mode Network (DMN) "Daydreaming" & Incubation Loop
   - Maintains an episodic memory graph with Zeigarnik tension on unsolved problems.
   - Executes Levy-flight stochastic walks across dormant memory traces and
     cross-domain archetypes, triggering "Eureka" serendipity interrupts when a
     latent connection resolves an open structural bottleneck.

3. Embodied / Sensory-Emotional "Felt-Sense" Evaluator
   - Simulates kinesthetic, thermodynamic, and aesthetic intuition (Poincare/Einstein
     felt-sense) before formal analytical pruning.
   - Scores candidate ideas across Structural Tension, Laminar Flow, Symmetry
     Breaking, Metabolic Cost, and Fragility/Antifragility.

4. Divergent-Convergent Oscillation Controller
   - Rhythmically alternates between unconstrained counterfactual/paradoxical
     divergence and rigorous Popperian falsification / architectural stress-testing.
   - Retains candidates on the Pareto Frontier of (Novelty x Rigor) rather than
     collapsing to high-probability average completions.

Usage:
    - As drop-in LLM Agent Middleware (`MuseMiddleware`) wrapping any LLM callable.
    - As a standalone multi-phase ideation orchestrator (`MuseEngine.imagine(...)`).
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from enum import Enum
import functools
import hashlib
import json
import math
import random
import time
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union


# ============================================================================
# Core Data Structures & Domain Taxonomies
# ============================================================================

class TaskDomain(str, Enum):
    SCIENTIFIC_HYPOTHESIS = "scientific_hypothesis"
    SOFTWARE_ARCHITECTURE = "software_architecture"
    HYBRID = "hybrid"


class CognitivePhase(str, Enum):
    EMBODIED_SENSING = "1_embodied_sensing"
    BISOCIATIVE_COLLISION = "2_bisociative_collision"
    DMN_INCUBATION = "3_dmn_incubation"
    DIVERGENT_EXPANSION = "4_divergent_expansion"
    CONVERGENT_CRITIQUE = "5_convergent_critique"


@dataclass
class RelationalPattern:
    """
    Domain-agnostic structural topology of a phenomenon or system mechanism.
    Used for Gentner-style structure mapping across distant domains.
    """
    nodes: List[str]
    causal_edges: List[Tuple[str, str, str]]  # (source, relation, target)
    feedback_loops: List[str]
    conservation_laws: List[str]
    failure_modes: List[str]
    tension_vectors: Dict[str, float]  # e.g. {"consistency_vs_latency": 0.85}


@dataclass
class DistantArchetype:
    """
    A richly structured phenomenon from nature, physics, biology, or art
    used as a source analog for bisociation.
    """
    id: str
    name: str
    source_domain: str
    summary: str
    pattern: RelationalPattern
    sensory_metaphor: str
    invariants: List[str]
    inversion_hook: str
    transferable_operators: List[str]


@dataclass
class EpisodicTrace:
    """
    A memory node stored in the Default-Mode Network (DMN) graph.
    Unsolved problems carry high `zeigarnik_tension`, making them magnets
    during stochastic daydreaming walks.
    """
    trace_id: str
    content: str
    domain: str
    tags: List[str]
    tension_vectors: Dict[str, float]
    zeigarnik_tension: float = 0.5  # 0.0 (resolved) to 1.0 (urgent unsolved anomaly)
    created_at: float = field(default_factory=time.time)
    activation_count: int = 1


@dataclass
class SerendipitySpark:
    """
    An emergent connection discovered during DMN daydreaming / Levy-flight drift.
    """
    trace_a: EpisodicTrace
    trace_b: Union[EpisodicTrace, DistantArchetype]
    shared_isomorphism: str
    productive_paradox: str
    free_energy_drop: float  # How much Zeigarnik tension this bridge resolves


@dataclass
class FeltSenseProfile:
    """
    Embodied, pre-analytic aesthetic and kinesthetic evaluation of an idea.
    Inspired by Poincare's aesthetic sieve and Gendlin's 'felt sense'.
    """
    structural_elegance: float      # Work accomplished per moving part (0-1)
    laminar_flow: float             # Freedom from bureaucratic/coordination bottlenecks (0-1)
    antifragility: float            # Ability to gain strength or adapt under disorder (0-1)
    productive_weirdness: float     # Epistemic surprise / violation of default assumptions (0-1)
    metabolic_overhead: float       # Energy/complexity tax (0-1, lower is better)
    kinesthetic_impression: str     # Embodied physical description of the architecture/hypothesis
    gut_warning: str                # Pre-formal intuition of where the idea feels brittle

    @property
    def composite_resonance(self) -> float:
        positive = (
            0.28 * self.structural_elegance
            + 0.24 * self.laminar_flow
            + 0.24 * self.antifragility
            + 0.24 * self.productive_weirdness
        )
        penalty = 0.20 * self.metabolic_overhead
        return round(max(0.0, min(1.0, positive - penalty)), 4)


@dataclass
class CreativeCandidate:
    """
    A synthesized hypothesis or architectural design produced during oscillation.
    """
    candidate_id: str
    title: str
    domain: TaskDomain
    source_archetype: str
    bisociative_bridge: str
    core_thesis: str
    mechanism_or_topology: List[str]
    inversion_applied: str
    felt_sense: FeltSenseProfile
    falsification_or_stress_test: List[str]
    novelty_score: float
    rigor_score: float
    pareto_optimal: bool = False

    @property
    def imagination_index(self) -> float:
        return round(
            0.40 * self.novelty_score
            + 0.35 * self.rigor_score
            + 0.25 * self.felt_sense.composite_resonance,
            4,
        )


@dataclass
class ImaginationReport:
    """
    Complete output of a MuseEngine cognitive cycle, ready to be consumed
    directly or injected into an LLM agent's prompt context via MuseMiddleware.
    """
    problem_statement: str
    domain: TaskDomain
    extracted_pattern: RelationalPattern
    bisociations: List[Tuple[DistantArchetype, float, str]]
    dmn_sparks: List[SerendipitySpark]
    divergent_candidates: List[CreativeCandidate]
    pareto_frontier: List[CreativeCandidate]
    synthesized_agent_prompt_injection: str
    trace_log: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


# ============================================================================
# Curated Cross-Domain Archetype Library (Nature, Physics, Biology, Art)
# ============================================================================

DEFAULT_ARCHETYPES: List[DistantArchetype] = [
    DistantArchetype(
        id="mycelial_physarum",
        name="Physarum Polycephalum (Slime Mold) Oscillatory Tube Network",
        source_domain="Biophysics / Decentralized Morphogenesis",
        summary=(
            "A brainless single-celled syncytium solves dynamic shortest-path and "
            "fault-tolerant network design via peristaltic cytoplasmic shuttle-streaming "
            "where tube diameter thickens nonlinearly with flux and prunes when starved."
        ),
        pattern=RelationalPattern(
            nodes=["Flux-Conducting Tubes", "Local Peristaltic Oscillators", "Nutrient Sinks"],
            causal_edges=[
                ("High Local Flux", "stretches_wall_to_increase", "Conductivity (D^4 Poiseuille)"),
                ("Low Flux", "triggers_autophagic_pruning_of", "Redundant Links"),
                ("Phase-Shifted Oscillations", "propagate_global_state_without", "Central Coordinator"),
            ],
            feedback_loops=[
                "Positive reinforcement of high-flux conduits coupled with global cytoplasm conservation",
                "Delayed oscillatory phase-waves routing around severed links within seconds",
            ],
            conservation_laws=["Total cytoplasmic volume is invariant; thickening one path thins others"],
            failure_modes=["Premature lock-in if nonlinear reinforcement exponent is too steep"],
            tension_vectors={
                "coordination_overhead": 0.92,
                "routing_rigidity": 0.88,
                "single_point_of_failure": 0.90,
                "clearance_bottleneck": 0.84,
            },
        ),
        sensory_metaphor=(
            "A breathing, rhythmic vascular web whose veins dilate where current surges "
            "and dissolve back into the body where flow stagnates."
        ),
        invariants=[
            "Zero global routing table; topology IS the memory",
            "Oscillatory pressure waves prevent steady-state clogging",
        ],
        inversion_hook=(
            "Instead of separating the routing control plane from the data/fluid plane, "
            "make the physical conduit's conductivity a direct function of oscillatory throughput."
        ),
        transferable_operators=[
            "Flux-proportional conduit dilation/pruning",
            "Peristaltic phase-wave signaling without global clocks",
            "Conservation-enforced resource reallocation",
        ],
    ),
    DistantArchetype(
        id="immune_clonal_thymic",
        name="Adaptive Immune Repertoire & Thymic Negative Selection",
        source_domain="Computational Immunology",
        summary=(
            "Generates billions of stochastic receptor variants via V(D)J somatic hypermutation "
            "before pathogen encounter, filters self-reactive clones in a sandboxed thymus, "
            "and exponentially amplifies only nodes matching local danger + antigen signals."
        ),
        pattern=RelationalPattern(
            nodes=["Somatic Generator", "Thymic Sandbox", "Quiescent Naive Pool", "Danger-Signal Co-Stimulator"],
            causal_edges=[
                ("V(D)J Recombination", "pre-generates", "Speculative Detector Diversity"),
                ("High Self-Affinity in Thymus", "induces_apoptosis_of", "Auto-Destructive Agents"),
                ("Antigen + Tissue Danger Signal", "triggers_clonal_expansion_of", "Matched Effectors"),
            ],
            feedback_loops=[
                "Affinity maturation: rapid mutation rate proportional to binding error",
                "Regulatory T-cell damping once danger signals subside",
            ],
            conservation_laws=["Metabolic budget caps active effector population; 95% contract to memory cells"],
            failure_modes=["Autoimmune storm if co-stimulatory 'danger context' check is bypassed"],
            tension_vectors={
                "novel_threat_detection": 0.95,
                "false_positive_damage": 0.89,
                "speculative_exploration": 0.91,
                "toxic_accumulation": 0.82,
            },
        ),
        sensory_metaphor=(
            "A silent constellation of millions of distinct lock-picks drifting at low energy "
            "until a two-key alarm ignites a localized, self-extinguishing wildfire."
        ),
        invariants=[
            "Two-factor activation: pattern match alone is inert without tissue stress context",
            "Mutation rate scales inversely with fitness (somatic hypermutation on mismatch)",
        ],
        inversion_hook=(
            "Stop designing deterministic handlers for anticipated edge cases; continuously breed "
            "disposable micro-probes in a shadow thymus and promote only those triggered by dual stress signals."
        ),
        transferable_operators=[
            "Two-signal co-stimulation (Event + Local Stress Context)",
            "Fitness-inverse mutation rate (hypermutate only when failing)",
            "Shadow-thymus negative selection against self-harm",
        ],
    ),
    DistantArchetype(
        id="spin_glass_annealing",
        name="Frustrated Spin Glass & Quantum/Thermal Tunneling Across Energy Barriers",
        source_domain="Condensed Matter & Statistical Physics",
        summary=(
            "In systems with competing local constraints (geometric frustration), no configuration "
            "satisfies all edges simultaneously. Escape from glassy local minima requires localized "
            "thermal/noise bursts and scale-free avalanche reorganizations."
        ),
        pattern=RelationalPattern(
            nodes=["Coupled Spins", "Frustrated Plaquettes", "Local Thermal Bath", "Avalanche Domains"],
            causal_edges=[
                ("Competing Antiferromagnetic Bonds", "create", "Degenerate Ground-State Manifold"),
                ("Localized Noise Injection", "destabilizes", "Metastable Trap"),
                ("Domain Wall Propagation", "resolves", "Long-Range Constraint Deadlock"),
            ],
            feedback_loops=[
                "Self-organized criticality: stress builds until power-law relaxation cascade",
                "Adiabatic cooling locks in low-energy domain boundaries",
            ],
            conservation_laws=["Topological charge of vortices/defects is conserved modulo boundary annihilation"],
            failure_modes=["Quench disorder freezing the system into a brittle, high-stress glass"],
            tension_vectors={
                "consistency_vs_latency": 0.94,
                "deadlock_under_contention": 0.91,
                "protein_misfolding_trap": 0.89,
                "local_minima_stagnation": 0.95,
            },
        ),
        sensory_metaphor=(
            "A jammed mosaic of magnetic tiles humming with pent-up geometric tension, "
            "periodically shimmering with targeted heat pulses so locked regions slip into harmony."
        ),
        invariants=[
            "Global frustration cannot be eliminated, only concentrated into mobile domain walls",
            "Cooling too fast guarantees brittle suboptimal lock-in",
        ],
        inversion_hook=(
            "Treat conflict/inconsistency not as an error to lock out, but as a mobile topological defect "
            "that can be routed to low-stakes boundaries and annihilated in pairs."
        ),
        transferable_operators=[
            "Defect-routing (materialize conflicts as first-class mobile tokens)",
            "Targeted stochastic heating of stalled/congested subgraphs",
            "Degenerate ground-state switching",
        ],
    ),
    DistantArchetype(
        id="estuarine_tidal_flushing",
        name="Estuarine Salt-Wedge Stratification & Tidal Pumping Clearance",
        source_domain="Geophysical Fluid Dynamics / Marine Ecology",
        summary=(
            "Estuaries clear heavy sediment and metabolic toxins without a unidirectional pump "
            "by coupling asymmetric tidal oscillations with density stratification and marsh-plain "
            "capacitance traps that separate inflow pathways from ebb-flush channels."
        ),
        pattern=RelationalPattern(
            nodes=["Dense Basal Layer", "Buoyant Surface Layer", "Tidal Barotropic Pulse", "Marsh Capacitance Basin"],
            causal_edges=[
                ("Tidal Asymmetry (Ebb Dominance)", "creates_net_export_of", "Aggregated Benthic Particulates"),
                ("Shear Instability at Pycnocline", "entrains_and_dilutes", "Stagnant Deep Solutes"),
                ("Side-Basin Phase Lag", "traps_and_settles", "Cohesive Flocs"),
            ],
            feedback_loops=[
                "Flocculation threshold: shear rate both promotes particle collision and shears apart oversized aggregates",
                "Loss of tidal amplitude collapses vertical mixing, triggering anoxic benthic dead zones",
            ],
            conservation_laws=["Salt and mass balance across tidal prism over spring-neap cycles"],
            failure_modes=["Eutrophic stratification lock-in when pulse amplitude drops below critical Richardson number"],
            tension_vectors={
                "clearance_bottleneck": 0.96,
                "toxic_accumulation": 0.94,
                "backpressure_congestion": 0.87,
                "oscillatory_coupling": 0.90,
            },
        ),
        sensory_metaphor=(
            "Two counter-sliding sheets of water—fresh over briny—pulsed by a slow lunar heartbeat "
            "that uses side-channel eddies as one-way ratchets to sweep heavy silt out to sea."
        ),
        invariants=[
            "Bidirectional oscillation achieves unidirectional net clearance via phase-lagged side capacitance",
            "Below a critical shear threshold (Richardson number), stratified layers decouple and suffocate",
        ],
        inversion_hook=(
            "Net clearance does not require a stronger continuous pump; it requires phase-lagged "
            "acoustic/pressure asymmetry and intact shear-mixing across stratified boundary layers."
        ),
        transferable_operators=[
            "Rectified tidal ratcheting (oscillation + phase-lagged side capacitance = net directional transport)",
            "Critical Richardson-number shear mixing across boundary layers",
            "Biphasic flocculation window (optimal shear prevents both monomer stasis and mega-clump occlusion)",
        ],
    ),
    DistantArchetype(
        id="baroque_fugue_stretto",
        name="Polyphonic Fugue Counterpoint & Stretto Canon Compression",
        source_domain="Music Theory / Temporal Information Architecture",
        summary=(
            "Multiple autonomous voices execute the exact same thematic transformation at staggered "
            "time offsets and pitch inversions (canon/stretto), achieving maximal information density "
            "without harmonic collision by obeying strict interval-invariance rules."
        ),
        pattern=RelationalPattern(
            nodes=["Subject Theme", "Countersubject", "Stretto Time-Offset Voices", "Harmonic Cadence Anchor"],
            causal_edges=[
                ("Oblique/Contrary Motion", "preserves_perceptual_independence_of", "Concurrent Streams"),
                ("Stretto Temporal Overlap", "compresses_latency_of", "Thematic Resolution"),
                ("Dissonance Preparation + Resolution", "propels", "Forward Momentum"),
            ],
            feedback_loops=[
                "Every voice's current state serves as the harmonic constraint field for the entering voice",
                "Pedal-point bass drone anchors chaotic upper-voice modulations",
            ],
            conservation_laws=["Forbidden parallel fifths/octaves prevent two voices from collapsing into one degree of freedom"],
            failure_modes=["Homophonic mud when voices move in parallel lockstep at identical frequencies"],
            tension_vectors={
                "coordination_overhead": 0.86,
                "consistency_vs_latency": 0.88,
                "oscillatory_coupling": 0.91,
                "deadlock_under_contention": 0.85,
            },
        ),
        sensory_metaphor=(
            "Four independent melodic threads weaving through a single keyhole at staggered fractions "
            "of a beat—never colliding because when one rises, its neighbor steps aside or descends."
        ),
        invariants=[
            "Contrary motion prevents phase-locked interference spikes",
            "A slow invariant pedal-point allows fast upper layers to mutate freely",
        ],
        inversion_hook=(
            "Synchronization spikes happen because nodes act in parallel lockstep; enforce 'contrary motion' "
            "phase-offsets and deterministic harmonic intervals so concurrent workers never contend for the same resource phase."
        ),
        transferable_operators=[
            "Contrary-motion resource scheduling (when node A scales read-heavy, neighbor B shifts write-compaction)",
            "Stretto staggered speculative execution",
            "Pedal-point slow state anchor beneath volatile ephemeral streams",
        ],
    ),
]


# ============================================================================
# Subsystem 1: Bisociation & Structural Isomorphism Engine
# ============================================================================

class BisociationEngine:
    """
    Implements Arthur Koestler's 'Bisociation' (intersecting two self-consistent
    but habitually incompatible frames of reference) combined with Dedre Gentner's
    Structure-Mapping Theory.
    """

    def __init__(self, archetypes: Optional[List[DistantArchetype]] = None):
        self.archetypes = list(archetypes or DEFAULT_ARCHETYPES)

    def extract_problem_topology(
        self, problem: str, domain: TaskDomain
    ) -> RelationalPattern:
        """
        Extracts the underlying relational tension vectors, causal bottlenecks,
        and conservation laws from a raw problem description.
        """
        text = problem.lower()
        tensions: Dict[str, float] = {}

        # Heuristic + structural keyword resonance mapping across abstract tension dimensions
        lexicon_map = {
            "coordination_overhead": [
                "distributed", "consensus", "coordinator", "lock", "sync", "cluster",
                "node", "quorum", "gossip", "microservice", "state", "mesh",
            ],
            "consistency_vs_latency": [
                "latency", "real-time", "realtime", "consistency", "cap", "replication",
                "stale", "lag", "throughput", "p99", "concurrent",
            ],
            "backpressure_congestion": [
                "spike", "burst", "backpressure", "queue", "overload", "cascade",
                "traffic", "bottleneck", "throttle", "flash", "flood",
            ],
            "clearance_bottleneck": [
                "clearance", "glymphatic", "drainage", "efflux", "waste", "barrier",
                "bbb", "perivascular", "csf", "interstitial", "flush", "transport",
            ],
            "toxic_accumulation": [
                "aggregation", "plaque", "amyloid", "tau", "protein", "misfold",
                "oligomer", "neurodegeneration", "alzheimer", "debris", "clump",
            ],
            "oscillatory_coupling": [
                "wave", "oscillation", "pulsatile", "sleep", "slow-wave", "rhythm",
                "frequency", "phase", "arterial", "vasomotion", "astrocyte", "aqp4",
            ],
            "deadlock_under_contention": [
                "contention", "deadlock", "starvation", "hot-key", "hotspot",
                "partition", "conflict", "race", "jam",
            ],
            "routing_rigidity": [
                "topology", "routing", "static", "schema", "coupling", "monolith",
                "fragile", "brittle", "rebalance",
            ],
        }

        for tension_key, keywords in lexicon_map.items():
            hits = sum(1 for kw in keywords if kw in text)
            if hits > 0:
                tensions[tension_key] = round(min(0.98, 0.45 + 0.12 * hits), 3)

        # Ensure baseline domain tensions if sparse prompt
        if not tensions:
            if domain == TaskDomain.SCIENTIFIC_HYPOTHESIS:
                tensions = {
                    "clearance_bottleneck": 0.80,
                    "toxic_accumulation": 0.78,
                    "oscillatory_coupling": 0.75,
                }
            else:
                tensions = {
                    "coordination_overhead": 0.82,
                    "consistency_vs_latency": 0.80,
                    "backpressure_congestion": 0.76,
                }

        if domain == TaskDomain.SCIENTIFIC_HYPOTHESIS:
            nodes = [
                "Primary Biological/Physical Substrate",
                "Transport / Signaling Boundary",
                "Metabolic or Oscillatory Driver",
                "Pathological Aggregate / Anomaly State",
            ]
            causal_edges = [
                ("Oscillatory Driver Degradation", "impairs", "Boundary Permeability & Net Flux"),
                ("Boundary Stagnation", "accelerates_nonlinear", "Local Monomer-to-Oligomer Nucleation"),
                ("Aggregate Deposition", "stiffens_and_decouples", "Oscillatory Driver (Vicious Cycle)"),
            ]
            feedback_loops = [
                "Runaway positive feedback between clearance failure and boundary stiffening",
                "Compensatory stress response transitioning from protective to maladaptive",
            ]
            conservation_laws = [
                "Intracranial / compartment volume-pressure conservation (Monro-Kellie constraint)",
                "Cellular ATP / metabolic energy budget across active transport pumps",
            ]
            failure_modes = [
                "Phase-decoupling between driving pulse and valve/channel polarization",
                "Irreversible nucleation once local concentration crosses critical supersaturation",
            ]
        else:
            nodes = [
                "Ingress / Mutating Client Edge",
                "Distributed State / Storage Shards",
                "Coordination / Ordering Fabric",
                "Downstream Consumer / Compaction Workers",
            ]
            causal_edges = [
                ("Bursty Skewed Load", "saturates", "Coordination / Ordering Fabric"),
                ("Retry Amplification", "multiplies", "Tail-Latency Variance (p99.9)"),
                ("Global Lock / Consensus Wait", "stalls", "Independent Partition Progress"),
            ]
            feedback_loops = [
                "Metastable retry storm: slow acks trigger client retries that further degrade throughput",
                "Hot-shard compaction stealing I/O bandwidth from active request serving",
            ]
            conservation_laws = [
                "Little's Law (L = lambda * W): bounded memory requires boundingeither concurrency or wait time",
                "CAP / PACELC tradeoff between synchronous linearizability and tail latency",
            ]
            failure_modes = [
                "Global coordination barrier turning localized jitter into system-wide brownout",
                "Static backpressure thresholds causing oscillatory herd synchronization",
            ]

        return RelationalPattern(
            nodes=nodes,
            causal_edges=causal_edges,
            feedback_loops=feedback_loops,
            conservation_laws=conservation_laws,
            failure_modes=failure_modes,
            tension_vectors=tensions,
        )

    def collide(
        self,
        problem_pattern: RelationalPattern,
        top_k: int = 3,
        exploration_noise: float = 0.08,
        rng: Optional[random.Random] = None,
    ) -> List[Tuple[DistantArchetype, float, str]]:
        """
        Finds the top-k distant archetypes that maximize structural isomorphism
        with the problem's tension vectors while injecting controlled stochasticity.
        Returns (archetype, isomorphism_score, bisociative_bridge_statement).
        """
        rng = rng or random.Random()
        scored: List[Tuple[DistantArchetype, float, str]] = []

        for arch in self.archetypes:
            # Compute structural cosine/dot overlap across tension vectors
            shared_keys = set(problem_pattern.tension_vectors.keys()) & set(
                arch.pattern.tension_vectors.keys()
            )
            if shared_keys:
                dot = sum(
                    problem_pattern.tension_vectors[k] * arch.pattern.tension_vectors[k]
                    for k in shared_keys
                )
                norm_p = math.sqrt(
                    sum(v * v for v in problem_pattern.tension_vectors.values())
                )
                norm_a = math.sqrt(
                    sum(v * v for v in arch.pattern.tension_vectors.values())
                )
                base_sim = dot / max(1e-6, (norm_p * norm_a))
            else:
                base_sim = 0.35

            # Add slight stochastic exploration jitter (non-linear serendipity)
            jitter = rng.uniform(-exploration_noise, exploration_noise)
            final_score = round(max(0.1, min(0.99, base_sim + jitter)), 4)

            bridge = (
                f"Map [{arch.name}] ({arch.source_domain}) onto the target problem: "
                f"{arch.inversion_hook} Key transferable operators: "
                f"{'; '.join(arch.transferable_operators)}."
            )
            scored.append((arch, final_score, bridge))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]


# ============================================================================
# Subsystem 2: Default-Mode Network (DMN) "Daydreaming" & Incubation Loop
# ============================================================================

class DefaultModeNetwork:
    """
    Simulates the brain's Default-Mode Network (active during wakeful rest,
    daydreaming, and incubation). Maintains an episodic trace buffer of open
    anomalies and executes Levy-flight associative walks to discover unexpected
    bridges that lower 'Zeigarnik tension' (unsolved structural free energy).
    """

    def __init__(self, seed_traces: Optional[List[EpisodicTrace]] = None):
        self.traces: List[EpisodicTrace] = list(seed_traces or self._default_seed_traces())

    @staticmethod
    def _default_seed_traces() -> List[EpisodicTrace]:
        return [
            EpisodicTrace(
                trace_id="trace_zeigarnik_01",
                content=(
                    "Observation: Systems that rely on a single strong pump or central leader "
                    "fail catastrophically when boundary impedance rises; nature almost always "
                    "uses distributed micro-ratchets + oscillatory phase lags instead."
                ),
                domain="Cross-Disciplinary Systems",
                tags=["ratchet", "oscillation", "impedance", "decentralized"],
                tension_vectors={"clearance_bottleneck": 0.9, "coordination_overhead": 0.85},
                zeigarnik_tension=0.88,
            ),
            EpisodicTrace(
                trace_id="trace_zeigarnik_02",
                content=(
                    "Anomaly: Why do protective barrier cells (astrocytes / API gateways) "
                    "shift from facilitating transport to actively blocking flow under chronic low-grade stress?"
                ),
                domain="Pathophysiology & Resilience Engineering",
                tags=["barrier", "reactive-state", "backpressure", "polarization"],
                tension_vectors={"toxic_accumulation": 0.86, "backpressure_congestion": 0.89},
                zeigarnik_tension=0.84,
            ),
            EpisodicTrace(
                trace_id="trace_zeigarnik_03",
                content=(
                    "Counter-intuition: Noise is not always corruption. In stochastic resonance "
                    "and frustrated spin glasses, a precise sub-threshold noise floor prevents "
                    "metastable jamming and keeps channels responsive."
                ),
                domain="Non-Equilibrium Statistical Mechanics",
                tags=["stochastic-resonance", "jamming", "metastability", "noise"],
                tension_vectors={"deadlock_under_contention": 0.92, "consistency_vs_latency": 0.82},
                zeigarnik_tension=0.79,
            ),
        ]

    def record_trace(
        self,
        content: str,
        domain: str,
        tags: List[str],
        tension_vectors: Dict[str, float],
        zeigarnik_tension: float = 0.75,
    ) -> EpisodicTrace:
        trace_id = f"trace_{hashlib.sha1(content.encode('utf-8')).hexdigest()[:8]}"
        trace = EpisodicTrace(
            trace_id=trace_id,
            content=content,
            domain=domain,
            tags=tags,
            tension_vectors=tension_vectors,
            zeigarnik_tension=zeigarnik_tension,
        )
        self.traces.append(trace)
        return trace

    def incubate_daydream(
        self,
        problem_statement: str,
        problem_pattern: RelationalPattern,
        archetypes: Sequence[DistantArchetype],
        steps: int = 4,
        rng: Optional[random.Random] = None,
    ) -> List[SerendipitySpark]:
        """
        Executes a Levy-flight random walk across stored episodic traces and
        distant archetypes. When a high-tension memory trace resonates with a
        distant archetype along a shared tension axis of the active problem,
        a 'SerendipitySpark' (Eureka event) is emitted.
        """
        rng = rng or random.Random()
        sparks: List[SerendipitySpark] = []

        # Temporarily register the active problem as a high-Zeigarnik trace
        active_trace = EpisodicTrace(
            trace_id="active_problem_focus",
            content=problem_statement,
            domain="Active Inquiry",
            tags=list(problem_pattern.tension_vectors.keys()),
            tension_vectors=problem_pattern.tension_vectors,
            zeigarnik_tension=0.95,
        )
        pool = self.traces + [active_trace]

        for step in range(steps):
            # Weight trace selection by Zeigarnik tension (unsolved problems pull attention)
            weights = [t.zeigarnik_tension for t in pool]
            chosen_trace = rng.choices(pool, weights=weights, k=1)[0]
            chosen_arch = rng.choice(list(archetypes))

            # Check for non-obvious structural bridge
            shared_axes = (
                set(chosen_trace.tension_vectors.keys())
                & set(chosen_arch.pattern.tension_vectors.keys())
            )
            if not shared_axes:
                shared_axis = next(iter(problem_pattern.tension_vectors.keys()), "structural_coupling")
            else:
                shared_axis = sorted(shared_axes)[0]

            free_energy_drop = round(
                0.5 * chosen_trace.zeigarnik_tension
                * chosen_arch.pattern.tension_vectors.get(shared_axis, 0.75),
                4,
            )

            paradox = (
                f"What if the bottleneck in '{shared_axis}' is caused by trying to enforce "
                f"steady-state uniformity, whereas [{chosen_arch.name}] solves it via "
                f"'{chosen_arch.transferable_operators[step % len(chosen_arch.transferable_operators)]}'?"
            )

            spark = SerendipitySpark(
                trace_a=chosen_trace,
                trace_b=chosen_arch,
                shared_isomorphism=f"Shared structural tension along '{shared_axis}'",
                productive_paradox=paradox,
                free_energy_drop=free_energy_drop,
            )
            sparks.append(spark)
            chosen_trace.activation_count += 1

        # Deduplicate by archetype + trace pair and sort by free_energy_drop
        unique_sparks: Dict[str, SerendipitySpark] = {}
        for sp in sparks:
            key = f"{sp.trace_a.trace_id}:{sp.trace_b.id}"
            if key not in unique_sparks or sp.free_energy_drop > unique_sparks[key].free_energy_drop:
                unique_sparks[key] = sp

        return sorted(unique_sparks.values(), key=lambda s: s.free_energy_drop, reverse=True)


# ============================================================================
# Subsystem 3: Embodied / Sensory-Emotional "Felt-Sense" Evaluator
# ============================================================================

class EmbodiedIntuitionEngine:
    """
    Models pre-verbal, physical/kinesthetic and aesthetic intuition.
    Before an agent commits to heavy deductive proof, human scientists and
    architects sense whether a structure feels 'brittle', 'top-heavy',
    'viscous', or 'self-harmonizing'.
    """

    def evaluate_felt_sense(
        self,
        archetype: DistantArchetype,
        problem_pattern: RelationalPattern,
        domain: TaskDomain,
    ) -> FeltSenseProfile:
        tensions = problem_pattern.tension_vectors
        arch_tensions = archetype.pattern.tension_vectors

        # Elegance: how well the archetype's invariants cover multiple problem tensions at once
        coverage = len(set(tensions.keys()) & set(arch_tensions.keys())) / max(1, len(tensions))
        structural_elegance = round(min(0.96, 0.62 + 0.32 * coverage), 3)

        # Laminar flow: absence of central bottlenecks
        laminar_flow = round(
            arch_tensions.get("clearance_bottleneck", 0.78) * 0.5
            + arch_tensions.get("coordination_overhead", 0.80) * 0.5,
            3,
        )

        # Antifragility: does stress improve routing/adaptation?
        antifragility = round(
            0.55
            + 0.20 * ("Adaptive" in archetype.name or "Physarum" in archetype.name or "Spin" in archetype.name)
            + 0.18 * coverage,
            3,
        )

        # Productive weirdness: cross-domain leap distance
        productive_weirdness = round(
            0.78 if domain == TaskDomain.SOFTWARE_ARCHITECTURE and "Bio" in archetype.source_domain
            else 0.82 if domain == TaskDomain.SCIENTIFIC_HYPOTHESIS and ("Music" in archetype.source_domain or "Fluid" in archetype.source_domain or "Physics" in archetype.source_domain)
            else 0.74,
            3,
        )

        # Metabolic overhead: lower when self-organizing
        metabolic_overhead = round(max(0.12, 0.38 - 0.15 * coverage), 3)

        kinesthetic = (
            f"Feels like: {archetype.sensory_metaphor} "
            f"(replaces rigid, brittle lockstep with phase-coupled elastic flow)."
        )
        gut_warning = (
            f"Watch out for: {archetype.pattern.failure_modes[0]} — must bound the feedback gain."
        )

        return FeltSenseProfile(
            structural_elegance=structural_elegance,
            laminar_flow=laminar_flow,
            antifragility=antifragility,
            productive_weirdness=productive_weirdness,
            metabolic_overhead=metabolic_overhead,
            kinesthetic_impression=kinesthetic,
            gut_warning=gut_warning,
        )


# ============================================================================
# Subsystem 4: Divergent-Convergent Oscillation & Pareto Synthesis
# ============================================================================

class OscillationController:
    """
    Alternates between:
      - Phase A (Lawless / Poetic Divergence): Applies bisociative operators,
        structural inversions, and DMN sparks to synthesize bold candidates.
      - Phase B (Popperian / Architectural Convergence): Subjects each candidate
        to ruthless falsification criteria (for science) or failure-mode / CAP /
        tail-latency stress tests (for software architecture).
      - Phase C (Pareto Frontier Selection): Selects the non-dominated set across
        (Novelty, Rigor, Felt-Sense Resonance) so genuinely original breakthroughs
        survive alongside high-rigor designs.
    """

    def __init__(self, intuition_engine: EmbodiedIntuitionEngine):
        self.intuition = intuition_engine

    def synthesize_and_oscillate(
        self,
        problem_statement: str,
        domain: TaskDomain,
        problem_pattern: RelationalPattern,
        bisociations: List[Tuple[DistantArchetype, float, str]],
        sparks: List[SerendipitySpark],
    ) -> Tuple[List[CreativeCandidate], List[CreativeCandidate]]:
        candidates: List[CreativeCandidate] = []

        for idx, (arch, iso_score, bridge) in enumerate(bisociations):
            felt = self.intuition.evaluate_felt_sense(arch, problem_pattern, domain)
            spark_paradox = (
                sparks[idx % len(sparks)].productive_paradox
                if sparks
                else arch.inversion_hook
            )

            if domain == TaskDomain.SCIENTIFIC_HYPOTHESIS:
                cand = self._build_scientific_hypothesis(
                    idx, problem_statement, arch, iso_score, bridge, spark_paradox, felt
                )
            else:
                cand = self._build_software_architecture(
                    idx, problem_statement, arch, iso_score, bridge, spark_paradox, felt
                )
            candidates.append(cand)

        pareto = self._compute_pareto_frontier(candidates)
        return candidates, pareto

    def _build_scientific_hypothesis(
        self,
        idx: int,
        problem: str,
        arch: DistantArchetype,
        iso_score: float,
        bridge: str,
        spark_paradox: str,
        felt: FeltSenseProfile,
    ) -> CreativeCandidate:
        title = (
            f"H{idx + 1}: {arch.transferable_operators[0]} Hypothesis "
            f"(via {arch.source_domain})"
        )
        core_thesis = (
            f"Pathological failure in [{problem[:90]}...] is not initiated by a static molecular "
            f"lesion alone, but by a dynamical phase-decoupling analogous to [{arch.name}]. "
            f"Specifically, {arch.inversion_hook.lower()}"
        )
        mechanism = [
            f"1. Primary Dynamical Trigger: Apply '{arch.transferable_operators[0]}' — boundary transport collapses when oscillatory shear/phase coherence drops below a critical threshold.",
            f"2. Non-Linear Amplification Loop: {arch.pattern.feedback_loops[0]}, creating localized supersaturation pockets where toxic oligomers nucleate.",
            f"3. Structural Inversion Mechanism: {spark_paradox}",
            f"4. Therapeutic / Experimental Intervention Lever: Restore '{arch.transferable_operators[1]}' rather than merely attempting downstream bulk clearance.",
        ]
        falsification = [
            f"Popperian Falsification Test 1 (Phase Perturbation): Artificially desynchronizing the phase offset of the driving oscillation while holding bulk flow constant MUST reproduce the pathology; if pathology does not appear, H{idx + 1} is falsified.",
            f"Popperian Falsification Test 2 (Threshold Non-Linearity): Measuring solute/aggregate clearance across graded shear/frequency steps must exhibit a sharp critical transition ( analogous to {arch.pattern.failure_modes[0]} ) rather than a linear dose-response.",
            f"Control / Confounder Check: Verify conservation constraint ({arch.pattern.conservation_laws[0]}) to rule out metabolic ATP depletion as the sole upstream confounder.",
        ]
        novelty = round(min(0.98, 0.72 + 0.22 * felt.productive_weirdness + 0.04 * idx), 3)
        rigor = round(min(0.97, 0.68 + 0.28 * iso_score), 3)

        return CreativeCandidate(
            candidate_id=f"sci_hyp_{idx + 1}_{arch.id}",
            title=title,
            domain=TaskDomain.SCIENTIFIC_HYPOTHESIS,
            source_archetype=f"{arch.name} ({arch.source_domain})",
            bisociative_bridge=bridge,
            core_thesis=core_thesis,
            mechanism_or_topology=mechanism,
            inversion_applied=arch.inversion_hook,
            felt_sense=felt,
            falsification_or_stress_test=falsification,
            novelty_score=novelty,
            rigor_score=rigor,
        )

    def _build_software_architecture(
        self,
        idx: int,
        problem: str,
        arch: DistantArchetype,
        iso_score: float,
        bridge: str,
        spark_paradox: str,
        felt: FeltSenseProfile,
    ) -> CreativeCandidate:
        title = (
            f"Arch-{idx + 1}: {arch.transferable_operators[0]} Topology "
            f"(inspired by {arch.name})"
        )
        core_thesis = (
            f"Instead of scaling [{problem[:90]}...] with centralized consensus locks or static "
            f"rate-limiters, model the cluster after [{arch.name}]: {arch.inversion_hook}"
        )
        topology = [
            f"1. Data & Control Plane Unification: Implement '{arch.transferable_operators[0]}' — embed backpressure and routing weights directly into payload piggyback headers (zero external coordinator).",
            f"2. Conflict & Load Dissipation: Apply '{arch.transferable_operators[1]}' so concurrent nodes operate at deterministic phase/frequency offsets, eliminating synchronized herd spikes.",
            f"3. Self-Stabilizing Feedback Loop: {arch.pattern.feedback_loops[0]}.",
            f"4. Architectural Paradox Resolution: {spark_paradox}",
        ]
        stress_tests = [
            f"Chaos / Jepsen Stress Test 1 (100x Skewed Hot-Key Burst): Inject a Zipfian (alpha=1.4) flash crowd while severing 30% of inter-node links; verify p99 latency remains bounded without retry amplification.",
            f"Invariant Guardrail: Enforce conservation budget ({arch.pattern.conservation_laws[0]}) at ingress so total in-flight work cannot exceed cluster drainage capacity.",
            f"Failure-Mode Watchdog: Guard against '{arch.pattern.failure_modes[0]}' by injecting controlled stochastic jitter (simulated annealing) when local queues phase-lock.",
        ]
        novelty = round(min(0.98, 0.74 + 0.20 * felt.productive_weirdness + 0.03 * idx), 3)
        rigor = round(min(0.97, 0.70 + 0.25 * iso_score), 3)

        return CreativeCandidate(
            candidate_id=f"sw_arch_{idx + 1}_{arch.id}",
            title=title,
            domain=TaskDomain.SOFTWARE_ARCHITECTURE,
            source_archetype=f"{arch.name} ({arch.source_domain})",
            bisociative_bridge=bridge,
            core_thesis=core_thesis,
            mechanism_or_topology=topology,
            inversion_applied=arch.inversion_hook,
            felt_sense=felt,
            falsification_or_stress_test=stress_tests,
            novelty_score=novelty,
            rigor_score=rigor,
        )

    @staticmethod
    def _compute_pareto_frontier(
        candidates: List[CreativeCandidate],
    ) -> List[CreativeCandidate]:
        """
        Marks and returns candidates that are non-dominated across
        (novelty_score, rigor_score, felt_sense.composite_resonance).
        """
        frontier: List[CreativeCandidate] = []
        for c in candidates:
            dominated = False
            c_vec = (c.novelty_score, c.rigor_score, c.felt_sense.composite_resonance)
            for other in candidates:
                if other.candidate_id == c.candidate_id:
                    continue
                o_vec = (
                    other.novelty_score,
                    other.rigor_score,
                    other.felt_sense.composite_resonance,
                )
                if all(o >= cv for o, cv in zip(o_vec, c_vec)) and any(
                    o > cv for o, cv in zip(o_vec, c_vec)
                ):
                    dominated = True
                    break
            c.pareto_optimal = not dominated
            if c.pareto_optimal:
                frontier.append(c)

        frontier.sort(key=lambda x: x.imagination_index, reverse=True)
        return frontier


# ============================================================================
# Top-Level Cognitive Orchestrator & Drop-In Agent Middleware
# ============================================================================

class MuseEngine:
    """
    Stateful Cognitive Imagination Engine combining:
      1. Bisociation & Distant Analogy
      2. Default-Mode Network (DMN) Daydreaming & Incubation
      3. Embodied Felt-Sense Intuition
      4. Divergent-Convergent Oscillation
    """

    def __init__(
        self,
        archetypes: Optional[List[DistantArchetype]] = None,
        seed_traces: Optional[List[EpisodicTrace]] = None,
        llm_callable: Optional[Callable[[str], str]] = None,
        seed: Optional[int] = 42,
    ):
        self.rng = random.Random(seed)
        self.bisociation = BisociationEngine(archetypes)
        self.dmn = DefaultModeNetwork(seed_traces)
        self.intuition = EmbodiedIntuitionEngine()
        self.oscillator = OscillationController(self.intuition)
        self.llm_callable = llm_callable

    def detect_domain(self, problem_statement: str) -> TaskDomain:
        text = problem_statement.lower()
        sci_keywords = [
            "hypothesis", "biological", "cell", "protein", "brain", "disease",
            "pathway", "molecular", "quantum", "physics", "enzyme", "clinical",
            "neuro", "glymphatic", "blood-brain", "receptor", "metabolism",
        ]
        sw_keywords = [
            "architecture", "distributed", "microservice", "database", "latency",
            "consensus", "cache", "queue", "throughput", "api", "cluster",
            "backpressure", "state", "shard", "event-driven", "system",
        ]
        sci_score = sum(1 for k in sci_keywords if k in text)
        sw_score = sum(1 for k in sw_keywords if k in text)
        if sci_score > sw_score:
            return TaskDomain.SCIENTIFIC_HYPOTHESIS
        return TaskDomain.SOFTWARE_ARCHITECTURE

    def imagine(
        self,
        problem_statement: str,
        domain: Optional[TaskDomain] = None,
        top_k_archetypes: int = 3,
        dmn_steps: int = 4,
    ) -> ImaginationReport:
        """
        Runs a full 5-phase non-linear imagination cycle on the target problem.
        Also records the problem into the DMN episodic trace buffer for future
        cross-problem serendipity.
        """
        resolved_domain = domain or self.detect_domain(problem_statement)
        trace_log: List[Dict[str, Any]] = []

        # Phase 1: Relational Topology Extraction
        pattern = self.bisociation.extract_problem_topology(
            problem_statement, resolved_domain
        )
        trace_log.append({
            "phase": CognitivePhase.EMBODIED_SENSING.value,
            "tension_vectors": pattern.tension_vectors,
            "conservation_laws": pattern.conservation_laws,
        })

        # Phase 2: Bisociative Collision across distant domains
        bisociations = self.bisociation.collide(
            pattern, top_k=top_k_archetypes, rng=self.rng
        )
        trace_log.append({
            "phase": CognitivePhase.BISOCIATIVE_COLLISION.value,
            "selected_archetypes": [
                {"name": a.name, "domain": a.source_domain, "score": s}
                for a, s, _ in bisociations
            ],
        })

        # Phase 3: Default-Mode Network (DMN) Daydreaming & Incubation
        sparks = self.dmn.incubate_daydream(
            problem_statement=problem_statement,
            problem_pattern=pattern,
            archetypes=[a for a, _, _ in bisociations],
            steps=dmn_steps,
            rng=self.rng,
        )
        trace_log.append({
            "phase": CognitivePhase.DMN_INCUBATION.value,
            "sparks_generated": len(sparks),
            "top_paradox": sparks[0].productive_paradox if sparks else None,
        })

        # Phase 4 & 5: Divergent Expansion + Convergent Falsification & Pareto Pruning
        candidates, pareto_frontier = self.oscillator.synthesize_and_oscillate(
            problem_statement=problem_statement,
            domain=resolved_domain,
            problem_pattern=pattern,
            bisociations=bisociations,
            sparks=sparks,
        )
        trace_log.append({
            "phase": CognitivePhase.DIVERGENT_EXPANSION.value,
            "candidates_synthesized": len(candidates),
        })
        trace_log.append({
            "phase": CognitivePhase.CONVERGENT_CRITIQUE.value,
            "pareto_survivors": [c.title for c in pareto_frontier],
        })

        # Store current inquiry in episodic memory for future incubation walks
        self.dmn.record_trace(
            content=problem_statement,
            domain=resolved_domain.value,
            tags=list(pattern.tension_vectors.keys()),
            tension_vectors=pattern.tension_vectors,
            zeigarnik_tension=0.72,
        )

        prompt_injection = self._format_agent_cognitive_scaffold(
            problem_statement, resolved_domain, pattern, bisociations, sparks, pareto_frontier
        )

        return ImaginationReport(
            problem_statement=problem_statement,
            domain=resolved_domain,
            extracted_pattern=pattern,
            bisociations=bisociations,
            dmn_sparks=sparks,
            divergent_candidates=candidates,
            pareto_frontier=pareto_frontier,
            synthesized_agent_prompt_injection=prompt_injection,
            trace_log=trace_log,
        )

    def _format_agent_cognitive_scaffold(
        self,
        problem: str,
        domain: TaskDomain,
        pattern: RelationalPattern,
        bisociations: List[Tuple[DistantArchetype, float, str]],
        sparks: List[SerendipitySpark],
        pareto: List[CreativeCandidate],
    ) -> str:
        """
        Formats the imagination cycle into a structured cognitive scaffold
        that can be injected into any LLM agent's system/developer context.
        """
        lines = [
            "<COGNITIVE_IMAGINATION_SCAFFOLD>",
            f"Target Mode: {domain.value.upper()}",
            "",
            "1. DEEP STRUCTURAL TOPOLOGY & CONSERVATION LAWS (Do not violate):",
        ]
        for law in pattern.conservation_laws:
            lines.append(f"   - Invariant: {law}")
        for loop in pattern.feedback_loops:
            lines.append(f"   - Underlying Feedback Loop: {loop}")

        lines.append("")
        lines.append("2. BISOCIATIVE CROSS-DOMAIN ANALOGIES (Force structural collision):")
        for arch, score, bridge in bisociations:
            lines.append(
                f"   - [{arch.name} | {arch.source_domain}] (Isomorphism={score}): "
                f"{arch.inversion_hook} Operators: {', '.join(arch.transferable_operators)}"
            )

        lines.append("")
        lines.append("3. DEFAULT-MODE NETWORK (DMN) SERENDIPITY SPARKS (Sub-conscious incubation):")
        for sp in sparks[:2]:
            lines.append(f"   - Productive Paradox: {sp.productive_paradox}")

        lines.append("")
        lines.append("4. PARETO-OPTIMAL NON-LINEAR CANDIDATES & EMBODIED FELT-SENSE:")
        for cand in pareto:
            lines.append(
                f"   * {cand.title} [ImaginationIndex={cand.imagination_index}, "
                f"Novelty={cand.novelty_score}, Rigor={cand.rigor_score}, "
                f"Resonance={cand.felt_sense.composite_resonance}]"
            )
            lines.append(f"     - Core Thesis: {cand.core_thesis}")
            lines.append(f"     - Embodied Felt-Sense: {cand.felt_sense.kinesthetic_impression}")
            lines.append(f"     - Gut Warning: {cand.felt_sense.gut_warning}")
            lines.append(
                f"     - Key Falsification / Stress Test: {cand.falsification_or_stress_test[0]}"
            )

        lines.extend([
            "",
            "5. SYNTHESIS DIRECTIVE FOR AGENT:",
            "   Avoid generic textbook answers. Synthesize your response by explicitly bridging",
            "   the Pareto-optimal cross-domain operators above with concrete mechanisms,",
            "   architectural primitives, or Popperian falsification experiments.",
            "</COGNITIVE_IMAGINATION_SCAFFOLD>",
        ])
        return "\n".join(lines)


class MuseMiddleware:
    """
    Drop-in Middleware wrapper for any LLM Agent or chat completion function.

    Can wrap:
      1. A message-list callable: `agent_fn(messages: List[Dict[str, str]], **kwargs) -> Any`
      2. A prompt-string callable: `agent_fn(prompt: str, **kwargs) -> Any`
      3. Decorator usage: `@MuseMiddleware(engine)`
    """

    def __init__(
        self,
        engine: Optional[MuseEngine] = None,
        domain: Optional[TaskDomain] = None,
        attach_report_metadata: bool = False,
    ):
        self.engine = engine or MuseEngine()
        self.default_domain = domain
        self.attach_report_metadata = attach_report_metadata
        self.last_report: Optional[ImaginationReport] = None

    def __call__(self, agent_fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(agent_fn)
        def wrapped(
            prompt_or_messages: Union[str, List[Dict[str, str]]],
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            if isinstance(prompt_or_messages, str):
                report = self.engine.imagine(
                    prompt_or_messages, domain=self.default_domain
                )
                self.last_report = report
                augmented_prompt = (
                    f"{report.synthesized_agent_prompt_injection}\n\n"
                    f"USER PROBLEM:\n{prompt_or_messages}"
                )
                result = agent_fn(augmented_prompt, *args, **kwargs)
            elif isinstance(prompt_or_messages, list):
                # Extract latest user message
                user_text = ""
                for msg in reversed(prompt_or_messages):
                    if msg.get("role") == "user":
                        user_text = msg.get("content", "")
                        break
                report = self.engine.imagine(
                    user_text or str(prompt_or_messages), domain=self.default_domain
                )
                self.last_report = report
                augmented_messages = [
                    {
                        "role": "system",
                        "content": report.synthesized_agent_prompt_injection,
                    },
                    *prompt_or_messages,
                ]
                result = agent_fn(augmented_messages, *args, **kwargs)
            else:
                raise TypeError(
                    "MuseMiddleware expects either a `str` prompt or `List[Dict[str, str]]` messages."
                )

            if self.attach_report_metadata:
                return {"response": result, "imagination_report": report}
            return result

        return wrapped


# ============================================================================
# CLI / Standalone Demonstration Runner
# ============================================================================

def _run_demo() -> None:
    engine = MuseEngine(seed=7)

    problems = [
        (
            TaskDomain.SOFTWARE_ARCHITECTURE,
            "Design a globally distributed real-time state synchronization and backpressure "
            "architecture that survives 100x skewed flash-crowd spikes without a central "
            "lock coordinator or retry amplification storms.",
        ),
        (
            TaskDomain.SCIENTIFIC_HYPOTHESIS,
            "Generate falsifiable mechanistic hypotheses explaining why age-related arterial "
            "pulsatility loss and astrocyte AQP4 depolarization trigger a sudden nonlinear "
            "collapse in glymphatic clearance and rapid amyloid/tau aggregation.",
        ),
    ]

    for domain, problem in problems:
        print("=" * 88)
        print(f"DOMAIN: {domain.value.upper()}")
        print(f"PROBLEM: {problem}")
        print("-" * 88)
        report = engine.imagine(problem, domain=domain, top_k_archetypes=3, dmn_steps=4)
        print(report.synthesized_agent_prompt_injection)
        print()


if __name__ == "__main__":
    _run_demo()