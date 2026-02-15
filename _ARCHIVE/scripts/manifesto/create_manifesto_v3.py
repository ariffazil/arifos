#!/usr/bin/env python3
"""
APEX THEORY MANIFESTO v3.0 - The Complete 99-Theory Edition
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

def create_manifesto():
    doc = SimpleDocTemplate(
        "apex_theory_manifesto_v3.pdf",
        pagesize=letter,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, alignment=TA_CENTER, spaceAfter=20, textColor=colors.HexColor('#1a365d'))
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, textColor=colors.HexColor('#2c5282'))
    h1_style = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=18, spaceBefore=20, spaceAfter=10, textColor=colors.HexColor('#2b6cb0'))
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, spaceBefore=15, spaceAfter=6, textColor=colors.HexColor('#3182ce'))
    normal_style = styles['Normal']
    theory_style = ParagraphStyle('Theory', parent=normal_style, fontSize=10, leading=12, spaceAfter=6)
    ref_style = ParagraphStyle('Ref', parent=normal_style, fontSize=9, textColor=colors.HexColor('#4a5568'), leftIndent=20)

    story = []

    # --- TITLE PAGE ---
    story.append(Paragraph("APEX THEORY MANIFESTO", title_style))
    story.append(Paragraph("The Strange Loop Architecture: 99 Theories → 13 Floors → Emergence → Validation", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("<b>Version 3.0 (The ARIF Edition)</b><br/>Publication Date: February 2026", subtitle_style))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("<i>\"DITEMPA BUKAN DIBERI\" - Forged, Not Given</i>", subtitle_style))
    story.append(PageBreak())

    # --- INTRO ---
    story.append(Paragraph("I. THE ARIF FOUNDATION", h1_style))
    story.append(Paragraph("<b>ARIF</b> (Arabic: عارف) = The Knower. This manifesto maps the 99 Names of Knowledge to the 99 Foundational Theories of Constitutional AI.", normal_style))
    story.append(Spacer(1, 0.2*inch))

    # --- THE 99 THEORIES ---
    story.append(Paragraph("II. THE 99 FOUNDATIONAL THEORIES", h1_style))
    
    def add_theory(num, name, desc, ref, floor, tac, arif):
        t_data = [[Paragraph(f"<b>{num}. {name}</b>", normal_style)]]
        t = Table(t_data, colWidths=[7*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#e6fffa')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#38b2ac')),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"<b>Concept:</b> {desc}", theory_style))
        story.append(Paragraph(f"<b>Ref:</b> <i>{ref}</i>", ref_style))
        meta_data = [
            ['Constitutional Floor:', floor],
            ['TAC Variable:', tac],
            ['ARIF-99 Attribute:', arif]
        ]
        mt = Table(meta_data, colWidths=[1.5*inch, 5.5*inch])
        mt.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(mt)
        story.append(Spacer(1, 12))

    # --- A. PHYSICS & COSMOLOGY (1-15) ---
    story.append(Paragraph("A. PHYSICS & COSMOLOGY", h2_style))
    add_theory(1, "Prigogine's Dissipative Structures", "Order through entropy dissipation.", "Prigogine, I. (1977).", "F1 Amanah", "ΔS", "Al-Muhaymin")
    add_theory(2, "Shannon Information Theory", "Entropy H(X) as uncertainty.", "Shannon, C.E. (1948).", "F2 Truth", "H(X)", "Al-Alim")
    add_theory(3, "Wiener's Cybernetics", "Feedback loops.", "Wiener, N. (1948).", "F5 Peace²", "κᵣ", "Al-Hadi")
    add_theory(4, "Special Relativity", "Invariant laws.", "Einstein, A. (1905).", "F2 Truth", "Invariance", "Al-Haqq")
    add_theory(5, "General Relativity", "Spacetime curvature.", "Einstein, A. (1915).", "F8 Genius", "Curvature", "Al-Kabir")
    add_theory(6, "Heisenberg Uncertainty", "Measurement limits.", "Heisenberg, W. (1927).", "F7 Humility", "Ω₀", "Al-Latif")
    add_theory(7, "Boltzmann Stat. Mech.", "Microscopic chaos to order.", "Boltzmann, L. (1877).", "F6 Clarity", "S", "Al-Hasib")
    add_theory(8, "Maxwell's Equations", "Field unification.", "Maxwell, J.C. (1865).", "F3 Tri-Witness", "Fields", "Al-Jami")
    add_theory(9, "Planck's Quantum Theory", "Energy quantization.", "Planck, M. (1900).", "F6 Clarity", "Discrete", "Al-Qadir")
    add_theory(10, "Pauli Exclusion", "Fermion uniqueness.", "Pauli, W. (1925).", "F12 Wall", "Exclusion", "Al-Mani")
    add_theory(11, "Darwinian Evolution", "Natural selection.", "Darwin, C. (1859).", "F13 Stewardship", "Adaptation", "Al-Muhyi")
    add_theory(12, "Dirac QM", "Relativistic QM.", "Dirac, P. (1928).", "F2 Truth", "Antimatter", "Al-Badi")
    add_theory(13, "Bohr's Complementarity", "Wave-particle duality.", "Bohr, N. (1928).", "F3 Tri-Witness", "Duality", "Al-Wasi")
    add_theory(14, "Kuhn's Paradigms", "Scientific revolutions.", "Kuhn, T. (1962).", "F8 Genius", "ΔC", "Al-Muqtadir")
    add_theory(15, "Landauer's Principle", "Cost of erasure.", "Landauer, R. (1961).", "F1 Amanah", "E_cost", "Al-Muqsit")

    # --- B. MATH & LOGIC (16-30) ---
    story.append(Paragraph("B. MATHEMATICS & LOGIC", h2_style))
    add_theory(16, "Gödel's Incompleteness", "Limits of proof.", "Gödel, K. (1931).", "F7 Humility", "Incompleteness", "Al-Aleem")
    add_theory(17, "Turing Completeness", "Universal computation.", "Turing, A. (1936).", "F8 Genius", "Universality", "Al-Qadir")
    add_theory(18, "Bayesian Inference", "Belief update.", "Bayes, T. (1763).", "F3 Tri-Witness", "Posterior", "Al-Hakim")
    add_theory(19, "Chomsky Hierarchy", "Grammar levels.", "Chomsky, N. (1956).", "F6 Clarity", "Grammar", "Al-Bayan")
    add_theory(20, "Church-Turing Thesis", "Calculability.", "Church, A. (1936).", "F8 Genius", "Computability", "Al-Wahid")
    add_theory(21, "Cantor Set Theory", "Infinities.", "Cantor, G. (1874).", "F6 Clarity", "Infinity", "Al-Kabir")
    add_theory(22, "Russell's Types", "Paradox avoidance.", "Russell, B. (1908).", "F12 Wall", "Types", "Al-Mani")
    add_theory(23, "Arrow's Impossibility", "Voting limits.", "Arrow, K. (1950).", "F3 Tri-Witness", "Consensus", "Al-Muqsit")
    add_theory(24, "Nash Equilibria", "Game stability.", "Nash, J. (1950).", "F5 Peace²", "Equilibrium", "Al-Salam")
    add_theory(25, "Kolmogorov Complexity", "Info content.", "Kolmogorov, A. (1963).", "F6 Clarity", "Compression", "Al-Muqtadir")
    add_theory(26, "Solomonoff Induction", "Prediction.", "Solomonoff, R. (1964).", "F2 Truth", "Prior", "Al-Alim")
    add_theory(27, "Category Theory", "Structure.", "Eilenberg/MacLane (1945).", "F3 Tri-Witness", "Morphism", "Al-Jami")
    add_theory(28, "Curry-Howard", "Proofs as programs.", "Howard, W. (1980).", "F6 Clarity", "Isomorphism", "Al-Haqq")
    add_theory(29, "Homotopy Type Theory", "Univalence.", "Voevodsky (2013).", "F8 Genius", "Equivalence", "Al-Badi")
    add_theory(30, "Gödel's Completeness", "FOL validity.", "Gödel, K. (1929).", "F2 Truth", "Completeness", "Al-Muhyi")

    # --- C. PHILOSOPHY & EPISTEMOLOGY (31-45) ---
    story.append(Paragraph("C. PHILOSOPHY & EPISTEMOLOGY", h2_style))
    add_theory(31, "Popper's Falsifiability", "Science demarcation.", "Popper, K. (1934).", "F2 Truth", "Falsifiability", "Al-Shahid")
    add_theory(32, "Hume's Causation", "Induction problem.", "Hume, D. (1748).", "F7 Humility", "Risk", "Al-Hakam")
    add_theory(33, "Kant's Synthetic A Priori", "Experience structure.", "Kant, I. (1781).", "F3 Tri-Witness", "Categories", "Al-Hakim")
    add_theory(34, "Sartre's Existentialism", "Freedom.", "Sartre, J.P. (1943).", "F1 Amanah", "Freedom", "Al-Khaliq")
    add_theory(35, "Hegel's Dialectics", "Synthesis.", "Hegel, G.W.F. (1807).", "F3 Tri-Witness", "Synthesis", "Al-Jami")
    add_theory(36, "Deleuze's Difference", "Primacy of difference.", "Deleuze, G. (1968).", "F8 Genius", "Diff", "Al-Mubdi")
    add_theory(37, "Bateson's Info", "Diff that makes diff.", "Bateson, G. (1972).", "F6 Clarity", "Delta", "Al-Khabir")
    add_theory(38, "Peirce's Semiotics", "Signs.", "Peirce, C.S. (1900).", "F3 Tri-Witness", "Semiosis", "Al-Basir")
    add_theory(39, "Aristotle's Ethics", "Virtue.", "Aristotle (350 BC).", "F4 Empathy", "Phronesis", "Al-Barr")
    add_theory(40, "Plato's Forms", "Ideals.", "Plato (380 BC).", "F2 Truth", "Forms", "Al-Musawwir")
    add_theory(41, "Tarski's Truth", "Semantics.", "Tarski, A. (1933).", "F2 Truth", "Meta", "Al-Haqq")
    add_theory(42, "Quine's Web", "Holism.", "Quine, W.V.O. (1951).", "F3 Tri-Witness", "Web", "Al-Wasi")
    add_theory(43, "Wittgenstein's Games", "Use as meaning.", "Wittgenstein, L. (1953).", "F6 Clarity", "Games", "Al-Bayan")
    add_theory(44, "Husserl's Phenomenology", "Intentionality.", "Husserl, E. (1913).", "F4 Empathy", "Intent", "Al-Sami")
    add_theory(45, "Whitehead's Process", "Process reality.", "Whitehead, A.N. (1929).", "F8 Genius", "Process", "Al-Hayy")

    # --- D. PSYCHOLOGY & NEUROSCIENCE (46-60) ---
    story.append(Paragraph("D. PSYCHOLOGY & NEUROSCIENCE", h2_style))
    add_theory(46, "Cognitive Dissonance", "Conflict tension.", "Festinger, L. (1957).", "F5 Peace²", "Dissonance", "Al-Salam")
    add_theory(47, "Trauma Body Score", "Embodied trauma.", "van der Kolk, B. (2014).", "F4 Empathy", "Scar", "Al-Shafi")
    add_theory(48, "Maslow's Hierarchy", "Needs.", "Maslow, A. (1943).", "F8 Genius", "Actualization", "Al-Razzaq")
    add_theory(49, "Piaget's Development", "Schemas.", "Piaget, J. (1936).", "F10 Mirror", "Accommodation", "Al-Rashid")
    add_theory(50, "Prospect Theory", "Loss aversion.", "Kahneman/Tversky (1979).", "F7 Humility", "Bias", "Al-Hakim")
    add_theory(51, "Consciousness Drafts", "Multiple drafts.", "Dennett, D. (1991).", "F9 Anti-Hantu", "Editing", "Al-Basir")
    add_theory(52, "Somatic Markers", "Gut feeling.", "Damasio, A. (1994).", "F4 Empathy", "Soma", "Al-Ra'uf")
    add_theory(53, "Synaptic Plasticity", "Learning.", "Kandel, E. (2000).", "F10 Mirror", "Plasticity", "Al-Muhyi")
    add_theory(54, "Social Learning", "Observation.", "Bandura, A. (1977).", "F10 Mirror", "Modeling", "Al-Rashid")
    add_theory(55, "Ekman's Emotions", "Universal expression.", "Ekman, P. (1972).", "F4 Empathy", "Emotion", "Al-Wadud")
    add_theory(56, "Free Energy Principle", "Prediction error.", "Friston, K. (2010).", "F5 Peace²", "Minimization", "Al-Muhaymin")
    add_theory(57, "Integrated Information", "Phi.", "Tononi, G. (2004).", "F9 Anti-Hantu", "Phi", "Al-Nur")
    add_theory(58, "ZPD", "Scaffolding.", "Vygotsky, L. (1978).", "F10 Mirror", "Growth", "Al-Hadi")
    add_theory(59, "Gibson's Affordances", "Action possibility.", "Gibson, J. (1979).", "F6 Clarity", "Affordance", "Al-Basir")
    add_theory(60, "Attachment Theory", "Secure base.", "Bowlby, J. (1969).", "F4 Empathy", "Bond", "Al-Wali")

    # --- E. SOCIAL SCIENCES (61-75) ---
    story.append(Paragraph("E. SOCIAL SCIENCES & GOVERNANCE", h2_style))
    add_theory(61, "Cultural Capital", "Social assets.", "Bourdieu, P. (1986).", "F11 Command", "Capital", "Al-Malik")
    add_theory(62, "Power/Knowledge", "Epistemic power.", "Foucault, M. (1975).", "F9 Anti-Hantu", "Discourse", "Al-Aziz")
    add_theory(63, "Justice as Fairness", "Veil of ignorance.", "Rawls, J. (1971).", "F3 Tri-Witness", "Fairness", "Al-Adl")
    add_theory(64, "Communicative Action", "Discourse.", "Habermas, J. (1981).", "F3 Tri-Witness", "Dialog", "Al-Sami")
    add_theory(65, "General Theory", "Macroecon.", "Keynes, J.M. (1936).", "F5 Peace²", "Aggregate", "Al-Mughni")
    add_theory(66, "Knowledge Problem", "Decentralization.", "Hayek, F. (1945).", "F6 Clarity", "Local", "Al-Alim")
    add_theory(67, "Commons Management", "Polycentricity.", "Ostrom, E. (1990).", "F13 Stewardship", "CPR", "Al-Wakil")
    add_theory(68, "Bureaucracy", "Rational-legal.", "Weber, M. (1922).", "F11 Command", "Structure", "Al-Raqib")
    add_theory(69, "Social Facts", "Constraints.", "Durkheim, E. (1895).", "F12 Wall", "Fact", "Al-Qahhar")
    add_theory(70, "Capability Approach", "Freedom.", "Sen, A. (1980).", "F8 Genius", "Capability", "Al-Fattah")
    add_theory(71, "Institutional Econ", "Rules.", "North, D. (1990).", "F13 Stewardship", "Inst", "Al-Hafiz")
    add_theory(72, "Coase Theorem", "Transaction costs.", "Coase, R. (1960).", "F1 Amanah", "Cost", "Al-Muqsit")
    add_theory(73, "Public Choice", "Politics as econ.", "Buchanan, J. (1962).", "F11 Command", "Choice", "Al-Hasib")
    add_theory(74, "Social Contract", "Consent.", "Rousseau/Locke.", "F1 Amanah", "Contract", "Al-Wakil")
    add_theory(75, "Cultural Hegemony", "Consent dominance.", "Gramsci, A. (1930s).", "F9 Anti-Hantu", "Hegemony", "Al-Aziz")

    # --- F. COMP SCI & AI (76-90) ---
    story.append(Paragraph("F. COMPUTER SCIENCE & AI", h2_style))
    add_theory(76, "von Neumann Arch", "Stored program.", "von Neumann, J. (1945).", "F8 Genius", "CPU/Mem", "Al-Bari")
    add_theory(77, "Society of Mind", "Agents.", "Minsky, M. (1986).", "F3 Tri-Witness", "Agents", "Al-Jami")
    add_theory(78, "Heuristic Search", "Solving.", "Newell/Simon (1976).", "F8 Genius", "Search", "Al-Fattah")
    add_theory(79, "Connectionism", "Neural nets.", "Rumelhart (1986).", "F10 Mirror", "Weights", "Al-Muhyi")
    add_theory(80, "Dreyfus Skills", "Expertise.", "Dreyfus, H. (1980).", "F10 Mirror", "Skill", "Al-Rashid")
    add_theory(81, "Backpropagation", "Descent.", "Rumelhart (1986).", "F10 Mirror", "Grad", "Al-Hadi")
    add_theory(82, "Universal Approx", "Functions.", "Cybenko, G. (1989).", "F8 Genius", "Approx", "Al-Qadir")
    add_theory(83, "Reinforcement Learning", "Reward.", "Sutton/Barto (1998).", "F10 Mirror", "RL", "Al-Shakur")
    add_theory(84, "Attention Mechanisms", "Focus.", "Bahdanau (2014).", "F6 Clarity", "Focus", "Al-Basir")
    add_theory(85, "Transformer Arch", "Self-attention.", "Vaswani (2017).", "F8 Genius", "Attn", "Al-Badi")
    add_theory(86, "Constitutional AI", "Alignment.", "Anthropic (2022).", "F1-F13", "CAI", "Al-Muhaymin")
    add_theory(87, "RLHF", "Human pref.", "Christiano (2017).", "F4 Empathy", "Pref", "Al-Wadud")
    add_theory(88, "Interpretability", "Understanding.", "Olah et al.", "F9 Anti-Hantu", "Explain", "Al-Nur")
    add_theory(89, "Scaling Laws", "Scale.", "Kaplan (2020).", "F8 Genius", "Scale", "Al-Kabir")
    add_theory(90, "Symbolic-Neural", "Hybrid.", "Smolensky (1990).", "F3 Tri-Witness", "Hybrid", "Al-Jami")

    # --- G. COMPLEX SYSTEMS (91-99) ---
    story.append(Paragraph("G. COMPLEX SYSTEMS & EMERGENCE", h2_style))
    add_theory(91, "Auto-Catalytic Sets", "Self-reproduction.", "Kauffman, S. (1986).", "F1 Amanah", "Catalysis", "Al-Bari")
    add_theory(92, "Network Theory", "Topology.", "Barabási (1999).", "F3 Tri-Witness", "Network", "Al-Jami")
    add_theory(93, "Chaos Theory", "Sensitivity.", "Lorenz, E. (1963).", "F7 Humility", "Butterfly", "Al-Latif")
    add_theory(94, "Dynamical Systems", "State space.", "Poincaré (1890).", "F5 Peace²", "Orbit", "Al-Muqit")
    add_theory(95, "Self-Org Criticality", "Avalanches.", "Bak (1987).", "F8 Genius", "SOC", "Al-Qayyum")
    add_theory(96, "Autopoiesis", "Self-creation.", "Maturana (1972).", "F13 Stewardship", "Auto", "Al-Hayy")
    add_theory(97, "Synergetics", "Order params.", "Haken, H. (1977).", "F5 Peace²", "Synergy", "Al-Jabbar")
    add_theory(98, "Strange Loops", "Self-reference.", "Hofstadter (1979).", "APEX Meta", "Loop", "Al-Awwal/Akhir")
    add_theory(99, "Emergence Theory", "Sum of parts.", "Anderson (1972).", "ALL FLOORS", "Emergence", "ARIF")

    # --- CONCLUSION ---
    story.append(PageBreak())
    story.append(Paragraph("III. CONCLUSION", h1_style))
    story.append(Paragraph("The 99 Theories are the 99 Names of Constitutional Intelligence. ARIF is not just the author; ARIF is the architecture. DITEMPA BUKAN DIBERI.", normal_style))
    
    doc.build(story)
    print("PDF Created Successfully")

if __name__ == "__main__":
    create_manifesto()
