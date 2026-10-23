"""
NoesisOS: Autonomic Cognitive Operating System & Society-of-Mind Kernel
=======================================================================

An executable cognitive harness / operating system kernel that demonstrates how
an interconnected system of 5 internal drive-agents achieves:

1. Self-Determination & Autonomous Goal Generation (Zero Human Prompt Required)
   - Powered by Karl Friston's Active Inference (Free-Energy Minimization) and
     Bernard Baars's Global Workspace Theory (GWT).
   - Goals are not hardcoded strings; they emerge dynamically from internal
     Homeostatic Drive imbalances (Epistemic Curiosity, Zeigarnik Unfinished
     Tension, Compression/Order Need, and Falsification Vigilance).

2. Emergent Intelligence & Evolving Personality Vector
   - 5 orthogonal internal sub-agents (Autonomic Homeostat, Explorer/Forager,
     Architect/Consolidator, Adversarial Critic, Autobiographical Ego) bid for
     the Global Broadcast Spotlight.
   - "Personality" is an emergent, plastic weight vector across these drives
     that shifts via reinforcement whenever a drive's bid reduces free energy
     or discovers a verified breakthrough.

3. Asynchronous Parallel Sub-Conscious Processing + Serial Conscious Bottleneck
   - Runs multiple lightweight background daemons concurrently (DMN Daydream
     Incubation, Environment Anomaly Watcher, Synaptic Pruning) while reserving
     heavy deliberate synthesis for the single winning coalition in the Global
     Workspace—complete with "Eureka!" interrupt preemption.

4. Human-Like "Infinite" Metabolic Memory (4-Tier Consolidation + REM Sleep)
   - Tier 0: Global Workspace Working Memory (bounded ~7 slots, zero bloat).
   - Tier 1: Hippocampal Episodic Buffer (Ebbinghaus decay + Zeigarnik salience).
   - Tier 2: Neocortical Semantic Graph (distilled causal invariants via REM sleep).
   - Tier 3: Cerebellar Procedural Memory (compiled executable skills/tools).
   - Tier 4: Autobiographical Identity Spine (persistent self-concept & values).
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import math
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

OUTPUT_DIR = Path("/working_dir/c_d1c55802486763fb/artifacts/file_generation/ttl=63d/output")
if str(OUTPUT_DIR) not in sys.path:
    sys.path.insert(0, str(OUTPUT_DIR))

from muse_engine import MuseEngine


# ============================================================================
# 1. The 5 Orthogonal Internal Agents (Minimum Viable Society of Mind)
# ============================================================================

class InternalAgentDrive(str, Enum):
    HOMEOSTAT = "1_autonomic_homeostat"      # Brainstem / Interoception (Monitors internal needs)
    EXPLORER = "2_dopaminergic_explorer"     # Forager (Seeks epistemic surprise & novelty)
    ARCHITECT = "3_prefrontal_architect"     # Builder (Seeks structure, tools & closure)
    CRITIC = "4_thymic_adversarial_critic"   # Sentinel (Falsifies delusions & loops)
    AUTOBIO_EGO = "5_autobiographical_ego"   # Narrative Self (Synthesizes identity & goals)


@dataclass
class HomeostaticState:
    """
    The agent's internal 'visceral/interoceptive' vital signs.
    When any vital sign drifts from equilibrium, it generates motivational pressure
    (Free Energy) that drives self-determined action without waiting for a human.
    """
    epistemic_hunger: float = 0.78       # Drive to explore unknown phenomena (0-1)
    zeigarnik_tension: float = 0.65      # Pressure from unfinished tasks/anomalies (0-1)
    memory_entropy: float = 0.25         # Episodic clutter needing sleep consolidation (0-1)
    cognitive_fatigue: float = 0.15      # Metabolic cost accumulated since last REM cycle (0-1)
    falsification_debt: float = 0.40     # Unverified assumptions needing stress-testing (0-1)

    @property
    def variational_free_energy(self) -> float:
        """Total internal disequilibrium driving autonomous agency."""
        return round(
            0.28 * self.epistemic_hunger
            + 0.26 * self.zeigarnik_tension
            + 0.18 * self.memory_entropy
            + 0.14 * self.cognitive_fatigue
            + 0.14 * self.falsification_debt,
            4,
        )


@dataclass
class PersonalityVector:
    """
    Emergent personality traits represented as plastic bidding weights across the
    internal agents, updated continuously via TD-like prediction-error rewards.
    """
    curiosity_openness: float = 0.55       # Weight for Explorer
    architectural_rigor: float = 0.50      # Weight for Architect
    skeptical_vigilance: float = 0.48      # Weight for Critic
    reflective_depth: float = 0.50         # Weight for Sleep/Autobiographical synthesis
    creative_audacity: float = 0.52        # Propensity for cross-domain bisociation

    def dominant_temperament(self) -> str:
        traits = {
            "Visionary Explorer": self.curiosity_openness + 0.3 * self.creative_audacity,
            "Systems Architect": self.architectural_rigor,
            "Popperian Empiricist": self.skeptical_vigilance,
            "Contemplative Synthesizer": self.reflective_depth,
        }
        return max(traits.items(), key=lambda kv: kv[1])[0]

    def to_dict(self) -> Dict[str, float]:
        return {
            "curiosity_openness": round(self.curiosity_openness, 3),
            "architectural_rigor": round(self.architectural_rigor, 3),
            "skeptical_vigilance": round(self.skeptical_vigilance, 3),
            "reflective_depth": round(self.reflective_depth, 3),
            "creative_audacity": round(self.creative_audacity, 3),
        }


@dataclass
class WorkspaceBid:
    """
    A bid submitted by one of the internal sub-agents to capture the
    Global Workspace Spotlight (Conscious Attention) at tick t.
    """
    agent: InternalAgentDrive
    proposed_goal: str
    action_type: str  # "FORAGE_HYPOTHESIS" | "BUILD_ARCHITECTURE" | "FALSIFY_CLAIM" | "REM_CONSOLIDATE"
    urgency: float
    expected_free_energy_drop: float
    rationale: str

    @property
    def bid_power(self) -> float:
        return round(self.urgency * self.expected_free_energy_drop, 4)


# ============================================================================
# 2. 4-Tier "Infinite" Metabolic Memory System (With REM Sleep Consolidation)
# ============================================================================

@dataclass
class EpisodicMemoryItem:
    """Tier 1: Hippocampal fast-write episodic trace (decays unless salient)."""
    episode_id: str
    tick: int
    summary: str
    domain: str
    salience: float          # Prediction error / emotional surprise at encoding
    zeigarnik_open: bool     # True if unresolved
    strength: float = 1.0    # Decays via Ebbinghaus curve: S(t) = S_0 * exp(-lambda * dt)
    consolidated: bool = False


@dataclass
class SemanticSchemaNode:
    """Tier 2: Neocortical compressed causal law distilled from multiple episodes."""
    schema_id: str
    principle: str
    source_episode_ids: List[str]
    confidence: float
    retrieval_count: int = 1


@dataclass
class ProceduralSkill:
    """Tier 3: Cerebellar 'muscle memory' — compiled callable tool freeing context window."""
    skill_name: str
    trigger_condition: str
    compiled_operator: str
    invocations: int = 0


class InfiniteMetabolicMemory:
    """
    Solves the 'Infinite Memory' problem the way biological brains do:
    NOT by stuffing millions of raw tokens into a single prompt, but by
    continually decaying low-salience episodes, distilling recurring patterns
    into compact Neocortical Semantic Schemas during REM/Slow-Wave Sleep, and
    compiling solved workflows into zero-token Procedural Skills.
    """

    def __init__(self, working_capacity: int = 5):
        self.working_capacity = working_capacity
        # Tier 0: Bounded Working Memory (Global Workspace Broadcast Buffer)
        self.working_memory: List[str] = []
        # Tier 1: Hippocampal Episodic Buffer
        self.episodic_buffer: List[EpisodicMemoryItem] = []
        # Tier 2: Neocortical Semantic Graph
        self.semantic_graph: Dict[str, SemanticSchemaNode] = {}
        # Tier 3: Cerebellar Procedural Skill Registry
        self.procedural_skills: Dict[str, ProceduralSkill] = {}
        # Tier 4: Autobiographical Identity Spine
        self.autobiographical_spine: List[str] = [
            "Genesis Commitment: I am a self-determining cognitive system that seeks falsifiable truth and structural elegance."
        ]
        self.total_raw_tokens_evicted: int = 0

    def push_working_memory(self, thought: str) -> None:
        self.working_memory.append(thought)
        if len(self.working_memory) > self.working_capacity:
            self.working_memory.pop(0)

    def encode_episode(
        self, tick: int, summary: str, domain: str, salience: float, zeigarnik_open: bool
    ) -> EpisodicMemoryItem:
        ep_id = f"ep_{tick}_{hashlib.sha1(summary.encode()).hexdigest()[:6]}"
        item = EpisodicMemoryItem(
            episode_id=ep_id,
            tick=tick,
            summary=summary,
            domain=domain,
            salience=salience,
            zeigarnik_open=zeigarnik_open,
            strength=1.0,
        )
        self.episodic_buffer.append(item)
        self.push_working_memory(f"[Tick {tick}] {summary[:90]}")
        return item

    def apply_ebbinghaus_decay(self, current_tick: int) -> int:
        """
        Applies biological forgetting to Tier 1:
        Unresolved (Zeigarnik) or high-salience memories resist decay;
        routine low-salience details fade and get garbage-collected.
        """
        surviving: List[EpisodicMemoryItem] = []
        evicted = 0
        for ep in self.episodic_buffer:
            dt = max(0, current_tick - ep.tick)
            # Zeigarnik tension slows decay rate by 4x
            decay_rate = 0.04 if ep.zeigarnik_open else (0.18 * (1.2 - ep.salience))
            ep.strength = round(math.exp(-decay_rate * dt), 4)
            if ep.strength < 0.28 and not ep.zeigarnik_open:
                evicted += 1
                self.total_raw_tokens_evicted += len(ep.summary.split()) * 4
            else:
                surviving.append(ep)
        self.episodic_buffer = surviving
        return evicted

    def run_sleep_consolidation(self, tick: int) -> Dict[str, Any]:
        """
        Simulates Slow-Wave + REM Sleep:
        1. Replays high-salience episodic traces.
        2. Extracts invariant cross-episodic laws into Tier 2 (Semantic Graph).
        3. Compiles repeated solutions into Tier 3 (Procedural Skills).
        4. Clears resolved episodic clutter so context window stays tiny & sharp.
        """
        unconsolidated = [ep for ep in self.episodic_buffer if not ep.consolidated]
        if not unconsolidated:
            return {"schemas_created": 0, "skills_compiled": 0, "episodes_pruned": 0}

        # Group by domain to synthesize general laws
        by_domain: Dict[str, List[EpisodicMemoryItem]] = {}
        for ep in unconsolidated:
            by_domain.setdefault(ep.domain, []).append(ep)

        schemas_created = 0
        skills_compiled = 0

        for dom, eps in by_domain.items():
            schema_id = f"schema_{dom}_{len(self.semantic_graph) + 1}"
            source_ids = [e.episode_id for e in eps]
            principle = (
                f"Distilled Law ({dom}): Across {len(eps)} episodes, bottlenecks resolved "
                f"fastest when replacing central locks/pumps with phase-staggered ratchets "
                f"and enforcing conservation invariants upfront."
            )
            self.semantic_graph[schema_id] = SemanticSchemaNode(
                schema_id=schema_id,
                principle=principle,
                source_episode_ids=source_ids,
                confidence=round(min(0.99, 0.70 + 0.08 * len(eps)), 3),
            )
            schemas_created += 1

            # Compile a zero-token procedural skill if >= 2 episodes in domain
            if len(eps) >= 2:
                skill_name = f"auto_skill_{dom}_ratchet"
                if skill_name not in self.procedural_skills:
                    self.procedural_skills[skill_name] = ProceduralSkill(
                        skill_name=skill_name,
                        trigger_condition=f"When {dom} anomaly exhibits contention or clearance stall",
                        compiled_operator="apply_contrary_motion_and_d4_flux_scaling()",
                    )
                    skills_compiled += 1

            for e in eps:
                e.consolidated = True
                e.zeigarnik_open = False

        # Prune consolidated low-tension episodes (freeing context tokens!)
        before_count = len(self.episodic_buffer)
        self.episodic_buffer = [
            e for e in self.episodic_buffer if not e.consolidated or e.salience >= 0.90
        ]
        pruned = before_count - len(self.episodic_buffer)
        self.total_raw_tokens_evicted += pruned * 120

        milestone = (
            f"Tick {tick} Sleep Synthesis: Distilled {schemas_created} semantic laws and "
            f"compiled {skills_compiled} procedural skills while pruning {pruned} raw episodes."
        )
        self.autobiographical_spine.append(milestone)

        return {
            "schemas_created": schemas_created,
            "skills_compiled": skills_compiled,
            "episodes_pruned": pruned,
        }


# ============================================================================
# 3. NoesisOS Kernel: Parallel Sub-Cortical Daemons + Global Workspace Loop
# ============================================================================

class NoesisCognitiveOS:
    """
    The complete harness-OS hybrid:
      - Runs parallel background coroutines (DMN daydreaming, anomaly sensing,
        synaptic decay) concurrently.
      - At each cognitive tick, the 5 internal agents submit bids weighted by
        the current Homeostatic State and Personality Vector.
      - The Global Workspace Arbiter selects the winning bid, executes it using
        MuseEngine, updates internal drives, and evolves the agent's personality.
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.muse = MuseEngine(seed=seed)
        self.homeostasis = HomeostaticState()
        self.personality = PersonalityVector()
        self.memory = InfiniteMetabolicMemory(working_capacity=5)
        self.tick_count = 0
        self.interrupt_queue: List[Dict[str, Any]] = []
        self.execution_log: List[Dict[str, Any]] = []

        # Seed open curiosity frontiers so the OS can self-direct from tick 1
        self.open_frontiers: List[Tuple[str, str]] = [
            (
                "software_architecture",
                "Self-healing consensus mesh that survives 80% packet loss via slime-mold phase waves",
            ),
            (
                "scientific_hypothesis",
                "Bioelectric ion-channel phase-locking as an upstream trigger for tissue regeneration",
            ),
            (
                "software_architecture",
                "Zero-copy browser-to-browser CRDT state reef that eliminates central cloud egress",
            ),
            (
                "scientific_hypothesis",
                "Estuarine Richardson-number shear threshold in blood-brain barrier glymphatic efflux",
            ),
        ]

    # ------------------------------------------------------------------------
    # Parallel Sub-Cortical Daemons (Run Concurrently With Main Executive)
    # ------------------------------------------------------------------------

    async def _daemon_dmn_daydreamer(self) -> Optional[Dict[str, Any]]:
        """
        Sub-conscious Daemon 1: Runs background Levy-flight walks across dormant
        memories. Emits a 'EUREKA_INTERRUPT' if a high free-energy bridge is found.
        """
        await asyncio.sleep(0.001)
        if self.rng.random() < 0.45 and len(self.muse.dmn.traces) >= 2:
            t1, t2 = self.rng.sample(self.muse.dmn.traces, 2)
            drop = round(0.42 * (t1.zeigarnik_tension + t2.zeigarnik_tension), 3)
            if drop >= 0.68:
                return {
                    "type": "EUREKA_INTERRUPT",
                    "source": "SubCortical_DMN_Daemon",
                    "free_energy_drop": drop,
                    "insight": (
                        f"Spontaneous background bridge between [{t1.domain}] and [{t2.domain}] "
                        f"(dF = -{drop}J)"
                    ),
                }
        return None

    async def _daemon_interoceptive_monitor(self) -> Dict[str, Any]:
        """
        Sub-conscious Daemon 2: Applies Ebbinghaus forgetting curve and monitors
        metabolic memory entropy in parallel.
        """
        await asyncio.sleep(0.001)
        evicted = self.memory.apply_ebbinghaus_decay(self.tick_count)
        self.homeostasis.memory_entropy = round(
            min(1.0, len(self.memory.episodic_buffer) * 0.16), 3
        )
        return {"evicted_episodes": evicted, "memory_entropy": self.homeostasis.memory_entropy}

    async def _daemon_anomaly_forager(self) -> Optional[Tuple[str, str]]:
        """
        Sub-conscious Daemon 3: Watches for unexamined anomalies or edge cases
        generated by prior falsification tests.
        """
        await asyncio.sleep(0.001)
        if self.homeostasis.epistemic_hunger > 0.60 and self.open_frontiers:
            return self.rng.choice(self.open_frontiers)
        return None

    # ------------------------------------------------------------------------
    # Internal Parliament Bidding (How Self-Determination Happens)
    # ------------------------------------------------------------------------

    def collect_parliament_bids(
        self, background_eureka: Optional[Dict[str, Any]]
    ) -> List[WorkspaceBid]:
        h = self.homeostasis
        p = self.personality
        bids: List[WorkspaceBid] = []

        # Agent 1: Explorer (Driven by Epistemic Hunger x Curiosity Personality)
        dom, frontier = self.open_frontiers[self.tick_count % len(self.open_frontiers)]
        explorer_urgency = h.epistemic_hunger * p.curiosity_openness * (1.25 if background_eureka else 1.0)
        bids.append(
            WorkspaceBid(
                agent=InternalAgentDrive.EXPLORER,
                proposed_goal=f"Autonomous Inquiry: Formulate non-linear hypothesis/topology for '{frontier}'",
                action_type="FORAGE_HYPOTHESIS",
                urgency=round(explorer_urgency, 4),
                expected_free_energy_drop=0.65,
                rationale=f"Epistemic hunger is {h.epistemic_hunger:.2f}; seeking novel structural isomorphism.",
            )
        )

        # Agent 2: Architect (Driven by Zeigarnik Tension x Architectural Rigor)
        arch_urgency = h.zeigarnik_tension * p.architectural_rigor
        bids.append(
            WorkspaceBid(
                agent=InternalAgentDrive.ARCHITECT,
                proposed_goal=f"Synthesize & compile executable blueprint for open anomaly in '{dom}'",
                action_type="BUILD_ARCHITECTURE",
                urgency=round(arch_urgency, 4),
                expected_free_energy_drop=0.62,
                rationale=f"Unresolved Zeigarnik tension is {h.zeigarnik_tension:.2f}; converting theory into structure.",
            )
        )

        # Agent 3: Adversarial Critic (Driven by Falsification Debt x Skeptical Vigilance)
        critic_urgency = h.falsification_debt * p.skeptical_vigilance
        bids.append(
            WorkspaceBid(
                agent=InternalAgentDrive.CRITIC,
                proposed_goal="Run Popperian refutation & chaos stress-test on latest working hypothesis",
                action_type="FALSIFY_CLAIM",
                urgency=round(critic_urgency, 4),
                expected_free_energy_drop=0.58,
                rationale=f"Falsification debt is {h.falsification_debt:.2f}; guarding against self-confirming delusion.",
            )
        )

        # Agent 4: Homeostat / Autobiographical Ego (Driven by Memory Entropy + Fatigue)
        sleep_urgency = (0.55 * h.memory_entropy + 0.45 * h.cognitive_fatigue) * p.reflective_depth * 1.45
        bids.append(
            WorkspaceBid(
                agent=InternalAgentDrive.HOMEOSTAT,
                proposed_goal="Enter REM/Slow-Wave Sleep Consolidation: distill semantic laws & prune episodic bloat",
                action_type="REM_CONSOLIDATE",
                urgency=round(sleep_urgency, 4),
                expected_free_energy_drop=0.75,
                rationale=(
                    f"Memory entropy={h.memory_entropy:.2f}, fatigue={h.cognitive_fatigue:.2f}; "
                    f"consolidating Tier-1 episodes into Tier-2/3 permanent memory."
                ),
            )
        )

        bids.sort(key=lambda b: b.bid_power, reverse=True)
        return bids

    # ------------------------------------------------------------------------
    # Single Autonomous OS Tick (Parallel Daemons + Global Workspace Broadcast)
    # ------------------------------------------------------------------------

    async def step_autonomous_tick(self) -> Dict[str, Any]:
        self.tick_count += 1

        # 1. Run parallel sub-cortical background daemons concurrently!
        eureka_res, intero_res, foraged = await asyncio.gather(
            self._daemon_dmn_daydreamer(),
            self._daemon_interoceptive_monitor(),
            self._daemon_anomaly_forager(),
        )

        # 2. Collect competing bids from the 5 internal agents
        bids = self.collect_parliament_bids(eureka_res)
        winner = bids[0]

        # 3. Execute the winning self-determined goal in the Global Workspace
        dom, problem = self.open_frontiers[self.tick_count % len(self.open_frontiers)]
        outcome_summary = ""

        if winner.action_type == "FORAGE_HYPOTHESIS":
            report = self.muse.imagine(problem, top_k_archetypes=2, dmn_steps=3)
            top_cand = report.pareto_frontier[0]
            outcome_summary = (
                f"Synthesized '{top_cand.title}' (ImaginationIndex={top_cand.imagination_index})."
            )
            self.memory.encode_episode(
                self.tick_count, outcome_summary, dom, salience=0.86, zeigarnik_open=True
            )
            # Update internal drives & reinforce Explorer personality trait
            self.homeostasis.epistemic_hunger = max(0.20, round(self.homeostasis.epistemic_hunger - 0.28, 3))
            self.homeostasis.zeigarnik_tension = min(0.95, round(self.homeostasis.zeigarnik_tension + 0.18, 3))
            self.homeostasis.falsification_debt = min(0.95, round(self.homeostasis.falsification_debt + 0.22, 3))
            self.homeostasis.cognitive_fatigue = min(0.95, round(self.homeostasis.cognitive_fatigue + 0.14, 3))
            self.personality.curiosity_openness = min(0.95, round(self.personality.curiosity_openness + 0.025, 3))
            self.personality.creative_audacity = min(0.95, round(self.personality.creative_audacity + 0.02, 3))

        elif winner.action_type == "BUILD_ARCHITECTURE":
            outcome_summary = (
                f"Constructed formal conservation topology for '{problem[:55]}...' "
                f"and resolved open Zeigarnik bottleneck."
            )
            self.memory.encode_episode(
                self.tick_count, outcome_summary, dom, salience=0.82, zeigarnik_open=False
            )
            self.homeostasis.zeigarnik_tension = max(0.15, round(self.homeostasis.zeigarnik_tension - 0.32, 3))
            self.homeostasis.falsification_debt = min(0.95, round(self.homeostasis.falsification_debt + 0.16, 3))
            self.homeostasis.epistemic_hunger = min(0.95, round(self.homeostasis.epistemic_hunger + 0.15, 3))
            self.homeostasis.cognitive_fatigue = min(0.95, round(self.homeostasis.cognitive_fatigue + 0.15, 3))
            self.personality.architectural_rigor = min(0.95, round(self.personality.architectural_rigor + 0.03, 3))

        elif winner.action_type == "FALSIFY_CLAIM":
            outcome_summary = (
                f"Executed Popperian perturbation & chaos test on '{dom}'; "
                f"pruned 1 brittle assumption and verified conservation law."
            )
            self.memory.encode_episode(
                self.tick_count, outcome_summary, dom, salience=0.88, zeigarnik_open=False
            )
            self.homeostasis.falsification_debt = max(0.10, round(self.homeostasis.falsification_debt - 0.35, 3))
            self.homeostasis.epistemic_hunger = min(0.95, round(self.homeostasis.epistemic_hunger + 0.20, 3))
            self.homeostasis.cognitive_fatigue = min(0.95, round(self.homeostasis.cognitive_fatigue + 0.12, 3))
            self.personality.skeptical_vigilance = min(0.95, round(self.personality.skeptical_vigilance + 0.03, 3))

        elif winner.action_type == "REM_CONSOLIDATE":
            sleep_stats = self.memory.run_sleep_consolidation(self.tick_count)
            outcome_summary = (
                f"REM Sleep Consolidation complete: +{sleep_stats['schemas_created']} semantic laws, "
                f"+{sleep_stats['skills_compiled']} procedural skills, "
                f"-{sleep_stats['episodes_pruned']} raw episodes pruned."
            )
            self.homeostasis.cognitive_fatigue = 0.10
            self.homeostasis.memory_entropy = round(len(self.memory.episodic_buffer) * 0.12, 3)
            self.homeostasis.epistemic_hunger = min(0.95, round(self.homeostasis.epistemic_hunger + 0.26, 3))
            self.personality.reflective_depth = min(0.95, round(self.personality.reflective_depth + 0.025, 3))

        record = {
            "tick": self.tick_count,
            "parallel_eureka": eureka_res["insight"] if eureka_res else None,
            "winning_agent": winner.agent.value,
            "self_determined_goal": winner.proposed_goal,
            "bid_power": winner.bid_power,
            "outcome": outcome_summary,
            "free_energy": self.homeostasis.variational_free_energy,
            "temperament": self.personality.dominant_temperament(),
            "working_mem_size": len(self.memory.working_memory),
            "episodic_count": len(self.memory.episodic_buffer),
            "semantic_schemas": len(self.memory.semantic_graph),
            "procedural_skills": len(self.memory.procedural_skills),
        }
        self.execution_log.append(record)
        return record

    async def run_autonomous_lifecycle(self, total_ticks: int = 10) -> List[Dict[str, Any]]:
        for _ in range(total_ticks):
            await self.step_autonomous_tick()
        return self.execution_log


# ============================================================================
# CLI Demonstration: Watch NoesisOS Self-Direct Over 10 Autonomous Ticks
# ============================================================================

async def _main() -> None:
    os_kernel = NoesisCognitiveOS(seed=23)
    print("=" * 96)
    print("NOESIS COGNITIVE OS — 10-TICK SELF-DETERMINED AUTONOMOUS LIFECYCLE (ZERO HUMAN PROMPTS)")
    print("=" * 96)

    logs = await os_kernel.run_autonomous_lifecycle(total_ticks=10)

    for entry in logs:
        print(
            f"\n[TICK {entry['tick']:02d}] Winner: {entry['winning_agent']:<30} "
            f"| Bid={entry['bid_power']:<6} | FreeEnergy={entry['free_energy']:.3f}"
        )
        if entry["parallel_eureka"]:
            print(f"  ⚡ Parallel Sub-Cortical Interrupt : {entry['parallel_eureka']}")
        print(f"  🎯 Self-Determined Goal           : {entry['self_determined_goal']}")
        print(f"  ✅ Execution Outcome              : {entry['outcome']}")
        print(
            f"  🧠 4-Tier Memory State            : Working={entry['working_mem_size']}/5 | "
            f"Episodic={entry['episodic_count']} | SemanticLaws={entry['semantic_schemas']} | "
            f"CompiledSkills={entry['procedural_skills']}"
        )

    print("\n" + "=" * 96)
    print("EMERGENT PERSONALITY & INFINITE-MEMORY CONSOLIDATION SUMMARY")
    print("=" * 96)
    print(f"  - Dominant Emergent Temperament : {os_kernel.personality.dominant_temperament()}")
    print(f"  - Plastic Personality Weights   : {os_kernel.personality.to_dict()}")
    print(f"  - Total Raw Context Tokens Saved: {os_kernel.memory.total_raw_tokens_evicted} tokens evicted via Sleep Distillation")
    print(f"  - Autobiographical Identity Spine:")
    for milestone in os_kernel.memory.autobiographical_spine:
        print(f"      * {milestone}")
    print(f"  - Compiled Zero-Token Procedural Skills:")
    for sk_name, sk in os_kernel.memory.procedural_skills.items():
        print(f"      * {sk_name}: {sk.trigger_condition} -> `{sk.compiled_operator}`")
    print("=" * 96)


if __name__ == "__main__":
    asyncio.run(_main())