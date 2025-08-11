#!/usr/bin/env python3
"""
Agent 0b: Pipeline Orchestrator - Phase 1 Script
Runs Agents 1-4 with state tracking and resume functionality

Phase 1: Foundation Building (Agents 1-4)
- Agent 1: Message House
- Agent 2: Brand-Side Personas  
- Agent 3: Customer-Side Personas (from reviews)
- Agent 4: Gap Analysis

PAUSE for Keywords Agent evaluation after completion.
"""

import json
import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent.parent / "config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("Error: config.json not found. Please create it with your API key.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: config.json is not valid JSON.")
        sys.exit(1)

def get_available_projects(base_path):
    """Get list of available projects from agent configurations"""
    projects = set()
    
    # Check message_house_agent for available projects
    agent_path = Path(base_path) / "message_house_agent" / "1_input"
    if agent_path.exists():
        for project_dir in agent_path.iterdir():
            if project_dir.is_dir() and not project_dir.name.startswith('.'):
                projects.add(project_dir.name)
    
    return sorted(list(projects))

def select_project(base_path):
    """Interactive project selection"""
    projects = get_available_projects(base_path)
    
    if not projects:
        print("No projects found. Please run Agent 0a first to create a project.")
        sys.exit(1)
    
    print("\n=== Available Projects ===")
    for i, project in enumerate(projects, 1):
        print(f"{i}. {project}")
    
    while True:
        try:
            choice = input(f"\nSelect project (1-{len(projects)}): ").strip()
            if choice:
                index = int(choice) - 1
                if 0 <= index < len(projects):
                    return projects[index]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")

def get_phase1_state_file(project_name, base_path):
    """Get the Phase 1 state tracking file path"""
    state_dir = Path(base_path) / "agent_0b_orchestrator" / "2_system_assets"
    state_dir.mkdir(exist_ok=True)
    return state_dir / f"phase1_state_{project_name}.json"

def load_phase1_state(project_name, base_path):
    """Load Phase 1 execution state"""
    state_file = get_phase1_state_file(project_name, base_path)
    
    if state_file.exists():
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # Default state
    return {
        "project_name": project_name,
        "phase": 1,
        "completed_agents": [],
        "failed_agents": [],
        "last_updated": None,
        "ready_for_keywords": False
    }

def save_phase1_state(state, base_path):
    """Save Phase 1 execution state"""
    state["last_updated"] = datetime.now().isoformat()
    state_file = get_phase1_state_file(state["project_name"], base_path)
    
    try:
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save state: {e}")

def detect_execution_mode(project_name, base_path):
    """Detect execution mode based on available input files"""
    print(f"\nDetecting execution mode for project: {project_name}")
    
    # Check required files
    message_house_input = Path(base_path) / "message_house_agent" / "1_input" / project_name
    customer_reviews_input = Path(base_path) / "user_story_real_reviews_agent" / "1_input" / project_name
    
    # Check if message house input exists
    qa_files = list(message_house_input.glob("*.md"))
    if not qa_files:
        print("ERROR: No Q&A input file found in message_house_agent input folder")
        print(f"Expected location: {message_house_input}")
        return None, []
    
    # Check if customer reviews exist
    review_files = list(customer_reviews_input.glob("*.csv"))
    
    if review_files:
        print("Found Q&A input and customer reviews")
        print("Mode: VALIDATION MODE (Phase 1: 1->2->3->4)")
        return "validation", [1, 2, 3, 4]
    else:
        print("Found Q&A input, no customer reviews")
        print("Mode: NEW BRAND MODE (Phase 1: 1->2)")
        return "new_brand", [1, 2]

def run_agent_script(agent_number, agent_name, base_path, project_name):
    """Execute specific agent's generate_simple.py script"""
    print(f"\n{'='*50}")
    print(f"Running Agent {agent_number}: {agent_name}")
    print(f"{'='*50}")
    
    agent_path = Path(base_path) / agent_name
    script_path = agent_path / "scripts" / "generate_simple.py"
    
    if not script_path.exists():
        print(f"Script not found: {script_path}")
        return False
    
    try:
        # Change to agent directory and run script
        original_cwd = os.getcwd()
        os.chdir(agent_path)
        
        print(f"Executing: python scripts/generate_simple.py")
        result = subprocess.run([sys.executable, "scripts/generate_simple.py"], 
                              capture_output=True, text=True, timeout=300)
        
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            print(f"Agent {agent_number} completed successfully")
            print("Output:", result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
            return True
        else:
            print(f"Agent {agent_number} failed with error code {result.returncode}")
            print("Error output:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"Agent {agent_number} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"Error running Agent {agent_number}: {e}")
        return False

def get_latest_output(agent_name, project_name, base_path):
    """Find most recent output file from agent"""
    
    # Special handling for Keywords Bank Agent - now uses project-specific folders
    if agent_name == "keywords_bank_agent":
        # First try project-specific folder (new structure)
        output_dir = Path(base_path) / agent_name / "3_unlabeled" / project_name
        if output_dir.exists():
            # Look for Keywords expansion files (Phase 2 output)
            expansion_files = list(output_dir.glob("keywords_bank_expansion_*.md"))
            if expansion_files:
                latest_file = max(expansion_files, key=lambda f: f.stat().st_mtime)
                return latest_file
            
            # Fallback to vocabulary files (Phase 1 output)
            vocab_files = list(output_dir.glob("keywords_bank_vocabulary_*.md"))
            if vocab_files:
                latest_file = max(vocab_files, key=lambda f: f.stat().st_mtime)
                return latest_file
        
        # Fallback to root folder (legacy structure) - only if project folder doesn't exist
        root_output_dir = Path(base_path) / agent_name / "3_unlabeled"
        if root_output_dir.exists() and not output_dir.exists():
            # Look for Keywords expansion files (Phase 2 output)
            expansion_files = list(root_output_dir.glob("keywords_bank_expansion_*.md"))
            if expansion_files:
                latest_file = max(expansion_files, key=lambda f: f.stat().st_mtime)
                return latest_file
            
            # Fallback to vocabulary files (Phase 1 output)
            vocab_files = list(root_output_dir.glob("keywords_bank_vocabulary_*.md"))
            if vocab_files:
                latest_file = max(vocab_files, key=lambda f: f.stat().st_mtime)
                return latest_file
        
        return None
    
    # Normal handling for other agents - project-specific folders
    output_dir = Path(base_path) / agent_name / "3_unlabeled" / project_name
    
    if not output_dir.exists():
        return None
    
    # Get all markdown files
    md_files = list(output_dir.glob("*.md"))
    if not md_files:
        return None
    
    # Return most recent file
    latest_file = max(md_files, key=lambda f: f.stat().st_mtime)
    return latest_file

def copy_agent_output(source_agent, target_agents, project_name, base_path, config):
    """Copy output files to target agent input folders"""
    agent_mapping = config['agent_mapping']
    source_agent_name = agent_mapping[str(source_agent)]
    
    # Get latest output from source agent
    source_file = get_latest_output(source_agent_name, project_name, base_path)
    if not source_file:
        print(f"No output file found from Agent {source_agent}")
        return False
    
    print(f"\nCopying output from Agent {source_agent} to downstream agents...")
    print(f"Source file: {source_file.name}")
    
    success_count = 0
    for target_agent in target_agents:
        target_agent_name = agent_mapping[str(target_agent)]
        target_dir = Path(base_path) / target_agent_name / "1_input" / project_name
        
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / source_file.name
            shutil.copy2(source_file, target_path)
            print(f"  Copied to Agent {target_agent}: {target_agent_name}")
            success_count += 1
        except Exception as e:
            print(f"  Failed to copy to Agent {target_agent}: {e}")
    
    print(f"Copy operation completed: {success_count}/{len(target_agents)} successful")
    return success_count == len(target_agents)

def execute_phase1_pipeline(project_name, base_path, config, execution_sequence, mode):
    """Run Phase 1 pipeline with state tracking and resume functionality"""
    print(f"\nStarting Phase 1 pipeline execution for: {project_name}")
    print(f"Execution sequence: {' -> '.join(map(str, execution_sequence))}")
    
    # Load existing state
    state = load_phase1_state(project_name, base_path)
    print(f"\nCurrent state: {len(state['completed_agents'])} agents completed")
    
    agent_mapping = config['agent_mapping']
    dependencies = config['agent_dependencies']
    
    for agent_number in execution_sequence:
        # Skip if already completed
        if agent_number in state['completed_agents']:
            print(f"\nAgent {agent_number} already completed - SKIPPING")
            continue
            
        agent_name = agent_mapping[str(agent_number)]
        
        # Check dependencies
        required_deps = dependencies.get(str(agent_number), [])
        missing_deps = [dep for dep in required_deps if dep not in state['completed_agents']]
        
        if missing_deps:
            print(f"Skipping Agent {agent_number} - missing dependencies: {missing_deps}")
            continue
        
        # Execute agent
        success = run_agent_script(agent_number, agent_name, base_path, project_name)
        
        if success:
            state['completed_agents'].append(agent_number)
            
            # Remove from failed list if previously failed
            if agent_number in state['failed_agents']:
                state['failed_agents'].remove(agent_number)
            
            # Copy output to downstream agents
            downstream_agents = []
            for other_agent, deps in dependencies.items():
                if agent_number in deps and int(other_agent) in execution_sequence:
                    downstream_agents.append(int(other_agent))
            
            if downstream_agents:
                copy_success = copy_agent_output(
                    agent_number, downstream_agents, project_name, base_path, config
                )
                if not copy_success:
                    print(f"Warning: Copy operation partially failed for Agent {agent_number}")
            
            # Save state after each successful agent
            save_phase1_state(state, base_path)
            
        else:
            if agent_number not in state['failed_agents']:
                state['failed_agents'].append(agent_number)
            
            # Ask user if they want to retry
            retry = input(f"\nAgent {agent_number} failed. Retry? (y/N): ").strip().lower()
            if retry == 'y':
                # Remove from failed list for retry
                if agent_number in state['failed_agents']:
                    state['failed_agents'].remove(agent_number)
                
                # Retry once
                success = run_agent_script(agent_number, agent_name, base_path, project_name)
                if success:
                    state['completed_agents'].append(agent_number)
                else:
                    state['failed_agents'].append(agent_number)
            
            save_phase1_state(state, base_path)
            
            if not success:
                break_execution = input("Continue with remaining agents? (y/N): ").strip().lower()
                if break_execution != 'y':
                    break
    
    # Check if minimum required agents for Keywords are complete
    completed_agents = set(state['completed_agents'])
    # Mode-specific requirements for Keywords Agent
    if mode == "validation":
        required_for_keywords = {1, 2, 3}  # Keywords needs all foundation agents
    else:  # new_brand mode
        required_for_keywords = {1, 2}  # Keywords only needs message house and brand persona
    
    if required_for_keywords.issubset(completed_agents):
        # Run Keywords Phase 1 if not already done
        if 5 not in state['completed_agents']:
            print(f"\nRunning Keywords Bank Phase 1...")
            
            # Copy input files from completed foundation agents to Keywords Agent
            print(f"Copying input files to Keywords Bank Agent...")
            for source_agent in required_for_keywords:
                if source_agent in completed_agents:
                    copy_success = copy_agent_output(
                        source_agent, [5], project_name, base_path, config
                    )
                    if not copy_success:
                        print(f"Warning: Failed to copy files from Agent {source_agent} to Keywords Agent")
            
            keywords_success = run_agent_script(5, "keywords_bank_agent", base_path, project_name)
            if keywords_success:
                state['completed_agents'].append(5)
                save_phase1_state(state, base_path)
                print(f"\nKeywords Phase 1 completed successfully!")
            else:
                print(f"\nKeywords Phase 1 failed. Cannot proceed to evaluation.")
                if 5 not in state['failed_agents']:
                    state['failed_agents'].append(5)
                save_phase1_state(state, base_path)
                return False
        
        # Phase 1 complete - ready for Keywords evaluation
        state['ready_for_keywords'] = True
        save_phase1_state(state, base_path)
        
        print(f"\n{'='*60}")
        print(f"PHASE 1 COMPLETE: Ready for Keywords Evaluation")
        print(f"{'='*60}")
        print(f"REQUIRED NEXT STEP: Keywords Phase 1 Evaluation")
        print(f"")
        print(f"1. Run evaluation: python keywords_bank_agent/scripts/evaluate_phase1.py")
        print(f"2. Score must be >= 7.0 to proceed to Phase 2")  
        print(f"3. Then run: python scripts/run_pipeline_phase2.py")
        print(f"")
        print(f"Note: Agent 4 failure (if any) does not block Keywords or Phase 2")
        
        return True
    else:
        missing_required = required_for_keywords - completed_agents
        print(f"\nPhase 1 incomplete. Missing required agents for Keywords: {sorted(list(missing_required))}")
        return False

def generate_phase1_report(project_name, base_path, config):
    """Generate Phase 1 execution report"""
    state = load_phase1_state(project_name, base_path)
    agent_mapping = config['agent_mapping']
    
    print(f"\n{'='*60}")
    print(f"PHASE 1 EXECUTION REPORT")
    print(f"{'='*60}")
    print(f"Project: {project_name}")
    print(f"Phase: Foundation Building (Agents 1-4)")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if state['completed_agents']:
        print(f"\nCOMPLETED AGENTS ({len(state['completed_agents'])}):")
        for agent_num in sorted(state['completed_agents']):
            agent_name = agent_mapping[str(agent_num)]
            print(f"  Agent {agent_num}: {agent_name}")
    
    if state['failed_agents']:
        print(f"\nFAILED AGENTS ({len(state['failed_agents'])}):")
        for agent_num in sorted(state['failed_agents']):
            agent_name = agent_mapping[str(agent_num)]
            print(f"  Agent {agent_num}: {agent_name}")
    
    print(f"\nGENERATED ASSETS:")
    for agent_num in sorted(state['completed_agents']):
        agent_name = agent_mapping[str(agent_num)]
        output_file = get_latest_output(agent_name, project_name, base_path)
        if output_file:
            print(f"  {agent_name}: {output_file.name}")
    
    total_agents = len(state['completed_agents']) + len(state['failed_agents'])
    if total_agents > 0:
        success_rate = len(state['completed_agents']) / total_agents * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    if state['ready_for_keywords']:
        print(f"\nNEXT STEPS:")
        print(f"1. Run Keywords Bank Agent: python keywords_bank_agent/scripts/generate_simple.py")
        print(f"2. Evaluate keywords quality: python keywords_bank_agent/scripts/evaluate_phase1.py") 
        print(f"3. If score >= 7.0, run Phase 2: python scripts/run_pipeline_phase2.py")
    else:
        print(f"\nPHASE 1 INCOMPLETE")
        print(f"Complete missing agents before proceeding to Keywords evaluation.")

def main():
    """Main execution function"""
    print("Agent 0b: Pipeline Orchestrator - Phase 1 Starting...")
    
    # Load configuration
    config = load_config()
    base_path = config['base_path']
    
    # Project selection
    project_name = select_project(base_path)
    print(f"\nSelected project: {project_name}")
    
    # Mode detection
    mode, execution_sequence = detect_execution_mode(project_name, base_path)
    if not mode:
        sys.exit(1)
    
    # Show current state
    state = load_phase1_state(project_name, base_path)
    if state['completed_agents']:
        print(f"\nRESUMING: {len(state['completed_agents'])} agents already completed")
        for agent_num in sorted(state['completed_agents']):
            agent_name = config['agent_mapping'][str(agent_num)]
            print(f"  Agent {agent_num}: {agent_name}")
    
    # Confirm execution
    remaining_agents = [a for a in execution_sequence if a not in state['completed_agents']]
    if remaining_agents:
        print(f"\nPhase 1 will execute {len(remaining_agents)} remaining agents: {remaining_agents}")
        confirm = input("Proceed with Phase 1 execution? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Phase 1 execution cancelled.")
            sys.exit(0)
    else:
        print(f"\nAll Phase 1 agents already completed!")
    
    # Execute Phase 1 pipeline
    success = execute_phase1_pipeline(project_name, base_path, config, execution_sequence, mode)
    
    # Generate report
    generate_phase1_report(project_name, base_path, config)
    
    if success:
        print(f"\nPhase 1 Complete! Ready for Keywords Agent evaluation.")

if __name__ == "__main__":
    main()