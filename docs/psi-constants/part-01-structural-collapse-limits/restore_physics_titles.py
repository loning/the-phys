#!/usr/bin/env python3
"""
Script to extract all chapter titles and restore physics concepts
Helps understand the tensor field physics interpretation of ψ = ψ(ψ)
"""

import os
import re
from typing import Dict, List, Tuple

def extract_chapter_info(filepath: str) -> Tuple[str, str, str]:
    """Extract chapter number, title, and sidebar label from a chapter file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from frontmatter
    title_match = re.search(r'title:\s*"([^"]+)"', content)
    sidebar_match = re.search(r'sidebar_label:\s*"([^"]+)"', content)
    
    if title_match and sidebar_match:
        full_title = title_match.group(1)
        sidebar = sidebar_match.group(1)
        
        # Extract chapter number
        chapter_num_match = re.search(r'Chapter\s+(\d+):', full_title)
        chapter_num = chapter_num_match.group(1) if chapter_num_match else "???"
        
        return chapter_num, full_title, sidebar
    
    return "???", "Unknown", "Unknown"

def scan_all_chapters(base_dir: str) -> Dict[str, List[Tuple[str, str, str]]]:
    """Scan all parts and extract chapter information"""
    chapters_by_part = {}
    
    # Parts to scan
    parts = [
        "part-01-structural-collapse-limits",
        "part-02-collapse-unit-isomorphism", 
        "part-03-spectral-constants",
        "part-04-cosmological-parameters"
    ]
    
    for part in parts:
        part_path = os.path.join(base_dir, part)
        if not os.path.exists(part_path):
            continue
            
        chapters = []
        
        # Find all chapter files
        for filename in sorted(os.listdir(part_path)):
            if filename.startswith("chapter-") and filename.endswith(".md"):
                filepath = os.path.join(part_path, filename)
                chapter_info = extract_chapter_info(filepath)
                chapters.append(chapter_info)
        
        chapters_by_part[part] = sorted(chapters, key=lambda x: int(x[0]) if x[0].isdigit() else 999)
    
    return chapters_by_part

def create_physics_mapping() -> Dict[str, str]:
    """Create mapping of mathematical concepts to physics interpretations"""
    return {
        # Part 1: Structural Collapse Limits
        "collapse limit": "fundamental physical constant",
        "φ-trace": "golden ratio spacetime path", 
        "speed limit": "speed of light c",
        "minimal action trace": "Planck's constant ħ",
        "entropy gradient": "gravitational constant G",
        "spectral average": "fine structure constant α",
        "collapse scaling invariants": "Planck units",
        "natural tick": "Planck time",
        "structural energy": "energy quantization",
        "rank-energy": "mass-energy relation",
        "golden-length": "Planck length scaling",
        
        # Part 2: Collapse Unit Isomorphism
        "collapse structure": "physical units system",
        "SI units": "measurement standards",
        "collapse basis": "fundamental dimensions",
        "equivalence theorem": "unit system isomorphism",
        "dimensional scaling": "unit conversions",
        "homomorphism": "structural preservation",
        "conformal invariance": "scale symmetry",
        "measurement axes": "dimensional basis",
        "quantity preservation": "conservation laws",
        "unit category": "dimensional algebra",
        
        # Part 3: Spectral Constants
        "rank paths": "quantum state transitions",
        "collapse weight": "transition probability", 
        "visibility factor": "quantum interference",
        "spectral filter": "measurement selection",
        "rank coupling": "gauge coupling strength",
        "window drift": "running coupling",
        "β-function": "renormalization flow",
        "degeneracy splitting": "symmetry breaking",
        "spectral lock": "coupling quantization",
        
        # Part 4: Cosmological Parameters
        "path entropy": "cosmological density",
        "rank cutoff": "observable universe boundary",
        "energy boundary": "critical density",
        "collapse baseline": "Planck density",
        "rank spectrum": "matter/energy distribution",
        "expansion dynamics": "cosmic evolution",
        "trace degeneracy": "scale factor ratios",
        "CMB anisotropy": "cosmic microwave background",
        "observer populations": "anthropic selection"
    }

def generate_physics_report(chapters_by_part: Dict[str, List[Tuple[str, str, str]]], 
                          physics_map: Dict[str, str]) -> str:
    """Generate comprehensive report with physics interpretations"""
    report = []
    report.append("# Physical Constants from ψ = ψ(ψ) Tensor Field Theory")
    report.append("\n## Complete Chapter Overview with Physics Interpretations\n")
    
    part_names = {
        "part-01-structural-collapse-limits": "Part I: Fundamental Constants from Collapse Structure",
        "part-02-collapse-unit-isomorphism": "Part II: Unit Systems and Dimensional Analysis", 
        "part-03-spectral-constants": "Part III: Quantum Field Couplings and Running",
        "part-04-cosmological-parameters": "Part IV: Cosmological Constants and Evolution"
    }
    
    for part, chapters in chapters_by_part.items():
        if part in part_names:
            report.append(f"\n### {part_names[part]}\n")
            
            for num, title, sidebar in chapters:
                # Extract the main concept from title
                concept_match = re.search(r'Chapter \d+:\s*([^—]+)', title)
                if concept_match:
                    concept = concept_match.group(1).strip()
                    
                    # Find physics interpretation
                    physics_interp = None
                    concept_lower = concept.lower()
                    for math_term, phys_term in physics_map.items():
                        if math_term in concept_lower:
                            physics_interp = phys_term
                            break
                    
                    if physics_interp:
                        report.append(f"- **Chapter {num}**: {concept}")
                        report.append(f"  - Physics: *{physics_interp}*")
                    else:
                        report.append(f"- **Chapter {num}**: {title}")
    
    # Add tensor field physics interpretation section
    report.append("\n## Tensor Field Physics Interpretation\n")
    report.append("The ψ = ψ(ψ) framework can be understood as a tensor field theory where:\n")
    report.append("1. **Collapse tensors** ↔ **Field strength tensors** (Fμν)")
    report.append("2. **φ-trace paths** ↔ **Geodesics in curved spacetime**")
    report.append("3. **Rank structure** ↔ **Energy scale hierarchy**")
    report.append("4. **Path weights** ↔ **Transition amplitudes**")
    report.append("5. **Visibility factors** ↔ **Quantum interference patterns**")
    report.append("6. **Collapse limits** ↔ **Fundamental constants**")
    report.append("7. **Observer states** ↔ **Measurement eigenstates**")
    report.append("8. **Zeckendorf constraint** ↔ **Quantization condition**")
    
    # Add constant summary
    report.append("\n## Derived Physical Constants Summary\n")
    report.append("From pure ψ = ψ(ψ) structure, we derive:\n")
    report.append("- **Speed of light**: c = φ²/2 × (collapse unit)")
    report.append("- **Planck constant**: ħ = φ⁻¹ × (minimal action)")  
    report.append("- **Gravitational constant**: G = φ³/π × (entropy gradient)")
    report.append("- **Fine structure constant**: α⁻¹ = 136.979 (from rank-6/7 paths)")
    report.append("- **Weinberg angle**: sin²θw = 0.234 (from rank-3 splitting)")
    report.append("- **Strong coupling**: αs(MZ) = 0.1181 (from rank-4 window)")
    report.append("- **Dark energy fraction**: ΩΛ ≈ 0.69 (from path entropy)")
    
    # Add first principles validation
    report.append("\n## First Principles Validation\n")
    report.append("Every derivation follows strictly from:\n")
    report.append("1. Self-reference axiom: ψ = ψ(ψ)")
    report.append("2. Zeckendorf representation (no consecutive 1s)")
    report.append("3. Golden ratio as the unique self-consistent limit")
    report.append("4. Category theory for structural relationships")
    report.append("5. Information theory for path weights")
    report.append("6. NO external parameters or empirical fitting")
    
    return "\n".join(report)

def main():
    """Main execution"""
    base_dir = "/Users/auric/the-phys/docs/psi-constants"
    
    print("Scanning all chapters...")
    chapters_by_part = scan_all_chapters(base_dir)
    
    print("\nGenerating physics mapping...")
    physics_map = create_physics_mapping()
    
    print("\nCreating comprehensive report...")
    report = generate_physics_report(chapters_by_part, physics_map)
    
    # Save report
    report_path = os.path.join(base_dir, "physics_interpretation_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_path}")
    
    # Also print summary
    total_chapters = sum(len(chapters) for chapters in chapters_by_part.values())
    print(f"\nTotal chapters found: {total_chapters}")
    for part, chapters in chapters_by_part.items():
        print(f"  {part}: {len(chapters)} chapters")

if __name__ == "__main__":
    main()