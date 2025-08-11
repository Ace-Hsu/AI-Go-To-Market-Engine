#!/usr/bin/env python3
"""
Keywords Bank Agent - Phase 1 Wrapper for Pipeline Integration

This script runs ONLY Phase 1 (vocabulary generation) and stops for human evaluation.
Agent 0b will pause the pipeline here for quality control.
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def get_project_paths(config_file="config.json"):
    """Get project-specific paths from configuration"""
    config_path = Path(__file__).parent.parent / config_file
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        project = config.get("current_project", None)
        
        if project:
            # New project-based structure
            return {
                "input_dir": Path(__file__).parent.parent / "1_input" / project,
                "system_assets_dir": Path(__file__).parent.parent / "2_system_assets" / project,
                "output_dir": Path(__file__).parent.parent / "3_unlabeled" / project
            }
        else:
            # Legacy structure (backward compatibility)
            return {
                "input_dir": Path(__file__).parent.parent / "1_input",
                "system_assets_dir": Path(__file__).parent.parent / "2_system_assets",
                "output_dir": Path(__file__).parent.parent / "3_unlabeled"
            }
    except:
        # Fallback to legacy structure
        return {
            "input_dir": Path(__file__).parent.parent / "1_input",
            "system_assets_dir": Path(__file__).parent.parent / "2_system_assets",
            "output_dir": Path(__file__).parent.parent / "3_unlabeled"
        }

def check_required_inputs(input_dir):
    """Check which input files are available"""
    required_patterns = [
        ("messagehouse*.md", "Message House"),
        ("*brand*.md", "Brand Personas"),
        ("*user*story*.md", "User Stories"),
        ("*customer*.md", "Customer Personas"),
        ("*review*.md", "Customer Reviews")
    ]
    
    available_files = []
    for pattern, description in required_patterns:
        files = list(input_dir.glob(pattern))
        if files:
            # Get most recent file
            latest_file = max(files, key=lambda f: f.stat().st_mtime)
            available_files.append((description, latest_file))
    
    return available_files

def run_phase1_generation():
    """Run Phase 1 keywords generation"""
    try:
        print("Running Keywords Bank Phase 1: Vocabulary Generation...")
        
        # Change to agent directory (required for phase1 script)
        original_cwd = os.getcwd()
        agent_dir = Path(__file__).parent.parent
        os.chdir(agent_dir)
        
        # Run Phase 1 script
        result = subprocess.run([sys.executable, "scripts/generate_phase1.py"], 
                              capture_output=True, text=True, timeout=300)
        
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            print("Keywords Bank Phase 1 completed successfully")
            # Show last part of output (avoid too much noise)
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines[-5:]:  # Show last 5 lines
                    if line.strip():
                        print(f"   {line}")
            return True
        else:
            print(f"Keywords Bank Phase 1 failed")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("Keywords Bank Phase 1 timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"Error running Keywords Bank Phase 1: {e}")
        return False

def main():
    """Main execution function"""
    print("Keywords Bank Generator (Phase 1) Starting...")
    
    # Get project-aware paths
    paths = get_project_paths()
    input_dir = paths["input_dir"]
    output_dir = paths["output_dir"]
    
    # Check available inputs
    available_files = check_required_inputs(input_dir)
    
    if not available_files:
        print(f"No input files found in {input_dir}")
        print("Required: Message house, brand personas, and/or customer personas")
        sys.exit(1)
    
    print(f"Found {len(available_files)} input files:")
    for description, file_path in available_files:
        print(f"  - {description}: {file_path.name}")
    
    # Run Phase 1 generation
    success = run_phase1_generation()
    
    if success:
        # Find the generated Phase 1 output
        vocab_files = list(output_dir.glob("keywords_bank_vocabulary*.md"))
        
        if vocab_files:
            latest_vocab = max(vocab_files, key=lambda f: f.stat().st_mtime)
            print(f"\nPhase 1 output generated: {latest_vocab.name}")
            print(f"Location: {output_dir}")
        
        print(f"""
PIPELINE PAUSE: Keywords Bank Phase 1 Complete

REQUIRED NEXT STEP: Human Evaluation
   Run: python keywords_bank_agent/scripts/evaluate_phase1.py
   
   - Evaluate vocabulary quality (Strategic alignment, completeness, etc.)
   - Score must be >=7.0 to proceed to Phase 2
   - This step ensures high-quality marketing assets

AFTER EVALUATION: Resume pipeline with Agent 0b
   The pipeline will automatically detect approval and continue

WARNING: DO NOT SKIP EVALUATION - This is the quality control gate!
""")
        
    else:
        print("Keywords Bank Phase 1 generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()