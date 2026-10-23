"""
MuseEngine Domain Adapters: Marketer / Market-Strategy Agent & Web Designer Agent
=================================================================================

Plugs `MuseEngine` and `MuseMiddleware` directly into two new agent roles:
  1. Marketer / Market-Dynamics Agent (`MarketerMuseAdapter`)
     - Replaces generic marketing clichés ("seamless all-in-one solution",
       "unlock your potential") with bisociative positioning, contrary-motion
       channel choreography, and falsifiable conversion/CAC experiments.
  2. Web Designer / UI-UX Architecture Agent (`WebDesignerMuseAdapter`)
     - Replaces cookie-cutter SaaS templates (generic 3-card hero, purple gradients)
       with embodied kinesthetic layouts, Fitts's/Hick's Law cognitive-load
       conservation, and concrete CSS/DOM/motion design tokens.
"""

from __future__ import annotations

from dataclasses import dataclass
import functools
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

OUTPUT_DIR = Path("/working_dir/c_d1c55802486763fb/artifacts/file_generation/ttl=63d/output")
if str(OUTPUT_DIR) not in sys.path:
    sys.path.insert(0, str(OUTPUT_DIR))

from muse_engine import (
    CreativeCandidate,
    DistantArchetype,
    FeltSenseProfile,
    ImaginationReport,
    MuseEngine,
    RelationalPattern,
    SerendipitySpark,
    TaskDomain,
)


# ============================================================================
# Specialized Archetypes for Market Dynamics & Spatial Web Design
# ============================================================================

CREATIVE_STUDIO_ARCHETYPES: List[DistantArchetype] = [
    DistantArchetype(
        id="coral_reef_symbiosis",
        name="Coral-Zooxanthellae Trophic Symbiosis & Calcified Micro-Habitats",
        source_domain="Marine Community Ecology / Niche Construction",
        summary=(
            "In nutrient-barren tropical waters (oligotrophic deserts), coral polyps build "
            "high-surface-area calcium carbonate architectures that trap light and recycle "
            "metabolic waste internally with symbiotic algae, creating a self-sustaining oasis."
        ),
        pattern=RelationalPattern(
            nodes=["Structural Host Skeleton", "Symbiotic Producer", "Micro-Eddy Boundary Layer"],
            causal_edges=[
                ("Rugose 3D Surface Geometry", "slows_boundary_flow_to_capture", "Scarce Ambient Attention/Nutrients"),
                ("Internal Waste-to-Fuel Loop", "eliminates_dependency_on", "External Paid Acquisition"),
                ("Modular Polyp Cloning", "compounds", "Surface Area Without Central Redesign"),
            ],
            feedback_loops=[
                "Higher structural rugosity traps more micro-currents, feeding symbionts that calcify more structure",
                "Thermal/trust bleaching if host extracts more than symbiont regenerates",
            ],
            conservation_laws=[
                "Trophic energy balance: user value recycled internally must exceed paid acquisition burn (LTV/CAC > 3)",
                "Hick's & Fitts's cognitive conservation: surface complexity must organize into fractal depth, not flat clutter",
            ],
            failure_modes=["Monoculture bleaching when sudden category shift invalidates a single acquisition channel"],
            tension_vectors={
                "attention_scarcity": 0.95,
                "trust_skepticism": 0.89,
                "retention_churn": 0.93,
                "visual_homogenization": 0.88,
                "cognitive_overload": 0.85,
            },
        ),
        sensory_metaphor=(
            "A sunlit, porous limestone cathedral in an empty blue desert—every alcove "
            "shelters a distinct micro-interaction while the whole reef breathes as one organism."
        ),
        invariants=[
            "Every user output becomes structural habitat for the next user",
            "Fractal progressive disclosure: calm macro-silhouette, rich micro-texture on hover/focus",
        ],
        inversion_hook=(
            "Stop renting fleeting attention in crowded feeds; build a calcified tool/artifact "
            "where every customer's normal workflow leaves behind a permanent, indexable reef structure."
        ),
        transferable_operators=[
            "Niche calcification (turn ephemeral user actions into permanent public/shareable artifacts)",
            "Symbiotic waste-to-fuel loop (one persona's byproduct is another persona's trigger)",
            "Rugose progressive disclosure (calm macro-canvas that reveals tactile micro-tools on proximity)",
        ],
    ),
]


# ============================================================================
# Role-Specific Tension & Blueprint Synthesizers
# ============================================================================

class AgentRole:
    MARKETER = "marketer_and_market_maker"
    WEB_DESIGNER = "web_designer_and_ui_architect"


class RoleAwareMuseEngine(MuseEngine):
    """
    Extends `MuseEngine` with native support for:
      - `AgentRole.MARKETER` (Campaigns, Category Design, Viral Loops, Positioning, Marketplaces)
      - `AgentRole.WEB_DESIGNER` (Visual Hierarchy, Spatial UI/UX, CSS/Motion Choreography)
    """

    def __init__(self, seed: int = 42):
        super().__init__(seed=seed)
        # Add the niche-construction / spatial symbiosis archetype
        self.bisociation.archetypes.extend(CREATIVE_STUDIO_ARCHETYPES)

    def extract_role_topology(self, brief: str, role: str) -> RelationalPattern:
        text = brief.lower()

        if role == AgentRole.MARKETER:
            tensions = {
                "coordination_overhead": 0.84,   # Multi-channel alignment
                "clearance_bottleneck": 0.88,    # Funnel conversion friction
                "oscillatory_coupling": 0.86,    # Launch cadence & narrative rhythm
                "attention_scarcity": 0.94,      # Cutting through category noise
                "trust_skepticism": 0.89,        # Overcoming buyer cynicism
            }
            if "liquidity" in text or "marketplace" in text or "market" in text:
                tensions["deadlock_under_contention"] = 0.92  # Cold-start supply/demand deadlock

            return RelationalPattern(
                nodes=[
                    "Skeptical Prospect / Cold-Start Side A",
                    "Category Narrative & Hook Surface",
                    "Proof / Co-Stimulation Trigger",
                    "Compounding Referral / Liquidity Loop",
                ],
                causal_edges=[
                    ("Generic Category Claims", "trigger", "Habituation & Banner Blindness"),
                    ("Unsynchronized Channel Blasts", "inflate", "CAC and Audience Fatigue"),
                    ("Two-Signal Proof + Timing", "unlocks", "Non-Linear Word-of-Mouth Cascade"),
                ],
                feedback_loops=[
                    "Cold-start liquidity ratchet: small asymmetric supply pockets seed local demand density",
                    "Narrative habituation decay: any static hook loses 50% efficiency every 21 days without contrapuntal variation",
                ],
                conservation_laws=[
                    "Attention-Trust Conservation: you cannot increase urgency claim intensity without proportional verifiable proof",
                    "Unit Economics Invariant: Marginal viral/organic loop coefficient (k) must offset paid CAC decay",
                ],
                failure_modes=[
                    "Homophonic channel mud: shouting the exact same generic message across all channels simultaneously",
                    "Premature broad-market dilution before hyper-saturating a single high-density niche basin",
                ],
                tension_vectors=tensions,
            )

        # Web Designer / UI Architect Role
        tensions = {
            "consistency_vs_latency": 0.87,      # Perceived instant responsiveness vs rich state
            "clearance_bottleneck": 0.91,        # Visual scanning flow & cognitive friction
            "oscillatory_coupling": 0.90,        # Typographic & scroll rhythm
            "visual_homogenization": 0.94,       # Escaping generic template sameness
            "cognitive_overload": 0.88,          # Managing dense information cleanly
        }
        return RelationalPattern(
            nodes=[
                "Entry Viewport (Above-the-Fold Field)",
                "Primary Interactive Spine (Pedal-Point Anchor)",
                "Dense Information Strata",
                "Micro-Interaction Feedback Loop",
            ],
            causal_edges=[
                ("Uniform Visual Weight", "paralyzes", "Foveal Gaze Path (No Entry Vector)"),
                ("Jarring Modal Interrupts", "shatter", "Spatial Mental Model & Flow State"),
                ("Kinetic Spring Physics", "grounds", "Digital Elements in Tactile Reality"),
            ],
            feedback_loops=[
                "Gaze-velocity coupling: high-scroll speed demands high-contrast macro-anchors; pause triggers micro-detail reveal",
                "Adaptive path thickening: frequently used actions gain visual prominence and shorter Fitts's Law distance",
            ],
            conservation_laws=[
                "Hick's & Tesler's Law (Conservation of Complexity): every element given high visual contrast steals contrast from its neighbors",
                "Fitts's Law Biomechanical Invariant: acquisition time scales with log2(2D / W)",
            ],
            failure_modes=[
                "Bento-box monotony: equal-sized cards with equal visual weight creating zero narrative momentum",
                "Gratuitous scroll-jacking that fights the user's physical input velocity",
            ],
            tension_vectors=tensions,
        )

    def imagine_for_role(
        self,
        brief: str,
        role: str,
        top_k: int = 3,
    ) -> Dict[str, Any]:
        """
        Runs the full 5-phase MuseEngine cycle tailored to a Marketer or Web Designer
        agent, returning both the structured blueprint and the ready-to-inject system prompt.
        """
        pattern = self.extract_role_topology(brief, role)
        bisociations = self.bisociation.collide(pattern, top_k=top_k, rng=self.rng)
        sparks = self.dmn.incubate_daydream(
            problem_statement=brief,
            problem_pattern=pattern,
            archetypes=[a for a, _, _ in bisociations],
            steps=4,
            rng=self.rng,
        )

        directives: List[Dict[str, Any]] = []
        for idx, (arch, score, _) in enumerate(bisociations):
            felt = self.intuition.evaluate_felt_sense(
                arch, pattern, TaskDomain.HYBRID
            )
            paradox = sparks[idx % len(sparks)].productive_paradox

            if role == AgentRole.MARKETER:
                directives.append(self._synthesize_marketing_play(idx, brief, arch, score, felt, paradox))
            else:
                directives.append(self._synthesize_web_design_system(idx, brief, arch, score, felt, paradox))

        # Record into DMN episodic memory so the Marketer and Web Designer cross-pollinate each other!
        self.dmn.record_trace(
            content=f"[{role}] {brief}",
            domain=role,
            tags=list(pattern.tension_vectors.keys()),
            tension_vectors=pattern.tension_vectors,
            zeigarnik_tension=0.82,
        )

        scaffold = self._build_role_prompt_scaffold(role, brief, pattern, directives, sparks)
        return {
            "role": role,
            "brief": brief,
            "conservation_laws": pattern.conservation_laws,
            "directives": directives,
            "dmn_sparks": [s.productive_paradox for s in sparks[:2]],
            "system_prompt_scaffold": scaffold,
        }

    def _synthesize_marketing_play(
        self,
        idx: int,
        brief: str,
        arch: DistantArchetype,
        score: float,
        felt: FeltSenseProfile,
        paradox: str,
    ) -> Dict[str, Any]:
        return {
            "play_id": f"MKT-{idx + 1}",
            "name": f"{arch.transferable_operators[0]} Play (via {arch.name})",
            "isomorphism_score": score,
            "resonance": felt.composite_resonance,
            "positioning_inversion": arch.inversion_hook,
            "campaign_mechanics": [
                f"Hook & Category Frame: Apply '{arch.transferable_operators[0]}' — instead of claiming superiority in the existing category, reframe the status quo as structurally broken.",
                f"Channel Choreography: Use '{arch.transferable_operators[1]}' so organic proof, technical teardowns, and community triggers fire at staggered phase offsets rather than synchronous ad blasts.",
                f"Paradox Resolution: {paradox}",
            ],
            "embodied_brand_feel": felt.kinesthetic_impression,
            "falsifiable_growth_experiment": (
                f"A/B Falsification Gate: Run a 14-day split test comparing standard benefit copy vs. "
                f"the '{arch.transferable_operators[0]}' artifact hook; falsify this play if organic "
                f"share-to-signup velocity does not beat baseline by >= 1.8x at equal CAC."
            ),
        }

    def _synthesize_web_design_system(
        self,
        idx: int,
        brief: str,
        arch: DistantArchetype,
        score: float,
        felt: FeltSenseProfile,
        paradox: str,
    ) -> Dict[str, Any]:
        return {
            "design_id": f"UI-{idx + 1}",
            "name": f"{arch.transferable_operators[0]} Design System (via {arch.name})",
            "isomorphism_score": score,
            "resonance": felt.composite_resonance,
            "spatial_inversion": arch.inversion_hook,
            "layout_and_css_mechanics": [
                f"Spatial Grid & Hierarchy: Implement '{arch.transferable_operators[0]}' — replace static equal-weight cards with dynamic viewport proportions (`grid-template-columns` scaling nonlinearly with active focus).",
                f"Scroll & Motion Choreography: Apply '{arch.transferable_operators[1]}' — anchor a slow invariant 'pedal-point' navigation rail (`position: sticky`) while secondary evidence strata glide in contrary motion.",
                f"Tactile & Visual Metaphor: {arch.sensory_metaphor}",
                f"Paradox Resolution: {paradox}",
            ],
            "embodied_ux_feel": felt.kinesthetic_impression,
            "ux_stress_test": (
                f"5-Second Squint & Fitts's Law Audit: Blur the viewport to 12px Gaussian; the primary "
                f"entry vector and pedal-point spine must remain unmistakable, and primary action acquisition "
                f"must require <= 1.2s without modal interruption."
            ),
        }

    @staticmethod
    def _build_role_prompt_scaffold(
        role: str,
        brief: str,
        pattern: RelationalPattern,
        directives: List[Dict[str, Any]],
        sparks: List[SerendipitySpark],
    ) -> str:
        lines = [
            f"<MUSE_ROLE_SCAFFOLD role='{role.upper()}'>",
            f"Brief: {brief}",
            "",
            "1. HARD CONSERVATION LAWS (Never violate in your output):",
        ]
        for law in pattern.conservation_laws:
            lines.append(f"   - {law}")

        lines.append("")
        lines.append("2. NON-LINEAR CROSS-DOMAIN PLAYS & DESIGN SYSTEMS:")
        for d in directives:
            title = d.get("name")
            inv = d.get("positioning_inversion") or d.get("spatial_inversion")
            test = d.get("falsifiable_growth_experiment") or d.get("ux_stress_test")
            mechanics = d.get("campaign_mechanics") or d.get("layout_and_css_mechanics") or []
            lines.append(f"   * {title} [Resonance={d['resonance']}]")
            lines.append(f"     - Core Inversion: {inv}")
            for m in mechanics[:2]:
                lines.append(f"     - {m}")
            lines.append(f"     - Verification Gate: {test}")

        lines.extend([
            "",
            "3. EXECUTION RULE:",
            "   Ban generic templates and clichés. Translate the highest-resonance play above",
            "   into concrete copy, growth loops, or production HTML/CSS/JS layout specifications.",
            "</MUSE_ROLE_SCAFFOLD>",
        ])
        return "\n".join(lines)


# ============================================================================
# Drop-In Role Decorators (`@marketer_imagination` and `@web_designer_imagination`)
# ============================================================================

def marketer_imagination(engine: Optional[RoleAwareMuseEngine] = None):
    """
    Decorator that wraps any Marketing / Market-Strategy Agent callable.
    """
    eng = engine or RoleAwareMuseEngine()

    def decorator(agent_fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(agent_fn)
        def wrapped(prompt_or_messages: Union[str, List[Dict[str, str]]], *args: Any, **kwargs: Any) -> Any:
            if isinstance(prompt_or_messages, str):
                res = eng.imagine_for_role(prompt_or_messages, role=AgentRole.MARKETER)
                return agent_fn(f"{res['system_prompt_scaffold']}\n\nBRIEF:\n{prompt_or_messages}", *args, **kwargs)
            user_msg = next((m["content"] for m in reversed(prompt_or_messages) if m.get("role") == "user"), "")
            res = eng.imagine_for_role(user_msg, role=AgentRole.MARKETER)
            augmented = [{"role": "system", "content": res["system_prompt_scaffold"]}, *prompt_or_messages]
            return agent_fn(augmented, *args, **kwargs)
        return wrapped
    return decorator


def web_designer_imagination(engine: Optional[RoleAwareMuseEngine] = None):
    """
    Decorator that wraps any Web Designer / Frontend UI Agent callable.
    """
    eng = engine or RoleAwareMuseEngine()

    def decorator(agent_fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(agent_fn)
        def wrapped(prompt_or_messages: Union[str, List[Dict[str, str]]], *args: Any, **kwargs: Any) -> Any:
            if isinstance(prompt_or_messages, str):
                res = eng.imagine_for_role(prompt_or_messages, role=AgentRole.WEB_DESIGNER)
                return agent_fn(f"{res['system_prompt_scaffold']}\n\nBRIEF:\n{prompt_or_messages}", *args, **kwargs)
            user_msg = next((m["content"] for m in reversed(prompt_or_messages) if m.get("role") == "user"), "")
            res = eng.imagine_for_role(user_msg, role=AgentRole.WEB_DESIGNER)
            augmented = [{"role": "system", "content": res["system_prompt_scaffold"]}, *prompt_or_messages]
            return agent_fn(augmented, *args, **kwargs)
        return wrapped
    return decorator


# ============================================================================
# Live Demonstration: Marketer + Web Designer Sharing One DMN Brain
# ============================================================================

def _demo_shared_creative_studio() -> None:
    # Notice: By sharing a single RoleAwareMuseEngine instance between your
    # Marketer Agent and your Web Designer Agent, their Default-Mode Network (DMN)
    # cross-pollinates campaign tensions with UI/UX layout architecture!
    shared_studio_brain = RoleAwareMuseEngine(seed=11)

    mkt_brief = (
        "Launch a developer-first AI observability and debugging marketplace in a "
        "crowded category where buyers ignore cold ads and distrust generic 'AI-powered' claims."
    )
    mkt_out = shared_studio_brain.imagine_for_role(mkt_brief, role=AgentRole.MARKETER)
    print("=" * 90)
    print("1. MARKETER / MARKET-STRATEGY AGENT SCAFFOLD")
    print("=" * 90)
    print(mkt_out["system_prompt_scaffold"])

    web_brief = (
        "Design the interactive landing page and live telemetry explorer for our AI "
        "observability marketplace—must feel visceral and alive without cluttered dashboards."
    )
    web_out = shared_studio_brain.imagine_for_role(web_brief, role=AgentRole.WEB_DESIGNER)
    print("\n" + "=" * 90)
    print("2. WEB DESIGNER / UI-UX ARCHITECT AGENT SCAFFOLD (Cross-Pollinated via Shared DMN)")
    print("=" * 90)
    print(web_out["system_prompt_scaffold"])


if __name__ == "__main__":
    _demo_shared_creative_studio()