#!/usr/bin/env python3
"""
Agent 0b: Pipeline Orchestrator - Phase 2 Script
Runs Keywords Agent + Final Agents (5, 7, 8, 9) with proper validation

Phase 2: Content Generation (After Keywords Approval)
- Agent 5: Keywords Bank (Phase 1 & 2)
- Agent 7: Testimonials Generation
- Agent 8: Social Media/Twitter Content
- Agent 9: Website Copy

Requires Phase 1 completion and Keywords evaluation score >= 7.0
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
    return state_dir / f"phase1_state_{project_name}.json"

def get_phase2_state_file(project_name, base_path):
    """Get the Phase 2 state tracking file path"""
    state_dir = Path(base_path) / "agent_0b_orchestrator" / "2_system_assets"
    state_dir.mkdir(exist_ok=True)
    return state_dir / f"phase2_state_{project_name}.json"

def load_phase1_state(project_name, base_path):
    """Load Phase 1 execution state"""
    state_file = get_phase1_state_file(project_name, base_path)
    
    if state_file.exists():
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    return None

def load_phase2_state(project_name, base_path):
    """Load Phase 2 execution state"""
    state_file = get_phase2_state_file(project_name, base_path)
    
    if state_file.exists():
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # Default state
    return {
        "project_name": project_name,
        "phase": 2,
        "completed_agents": [],
        "failed_agents": [],
        "last_updated": None,
        "keywords_approved": False,
        "keywords_phase2_completed": False
    }

def save_phase2_state(state, base_path):
    """Save Phase 2 execution state"""
    state["last_updated"] = datetime.now().isoformat()
    state_file = get_phase2_state_file(state["project_name"], base_path)
    
    try:
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save state: {e}")

def validate_phase1_completion(project_name, base_path):
    """Validate that Phase 1 is completed before running Phase 2"""
    phase1_state = load_phase1_state(project_name, base_path)
    
    if not phase1_state:
        print("ERROR: Phase 1 state not found. Please run run_pipeline_phase1.py first.")
        return False
    
    # Check if Keywords Phase 1 was completed
    completed_agents = set(phase1_state.get('completed_agents', []))
    if 5 not in completed_agents:
        print("ERROR: Keywords Phase 1 not completed. Please complete Phase 1 first.")
        print(f"Phase 1 completed agents: {phase1_state.get('completed_agents', [])}")
        return False
    
    # Check if Keywords evaluation is completed with passing score
    approved, score = check_keywords_phase1_approved(project_name, base_path)
    if not approved:
        print("ERROR: Keywords Phase 1 evaluation not approved.")
        print(f"Current evaluation score: {score:.1f} (requires >= 7.0)")
        print("Please run: python keywords_bank_agent/scripts/evaluate_phase1.py")
        return False
    
    print("Phase 1 validation: PASSED")
    print(f"Keywords Phase 1 approved with score: {score:.1f}")
    return True

def check_keywords_phase1_approved(project_name, base_path):
    """Check if keywords Phase 1 has been evaluated and approved"""
    keywords_labeled_dir = Path(base_path) / "keywords_bank_agent" / "5_labeled_json"
    
    if not keywords_labeled_dir.exists():
        return False, 0.0
    
    # Look for recent evaluation JSON files
    json_files = list(keywords_labeled_dir.glob("*.json"))
    if not json_files:
        return False, 0.0
    
    # Check the most recent evaluation
    latest_eval = max(json_files, key=lambda f: f.stat().st_mtime)
    
    try:
        with open(latest_eval, 'r', encoding='utf-8') as f:
            eval_data = json.load(f)
        
        # Check if score is >= 7.0 (approval threshold)
        overall_score = eval_data.get('overall_score', 0)
        return overall_score >= 7.0, overall_score
        
    except:
        return False, 0.0

def detect_execution_mode(project_name, base_path):
    """Detect execution mode based on available input files"""
    print(f"\nDetecting execution mode for project: {project_name}")
    
    # Check if customer reviews exist to determine mode
    customer_reviews_input = Path(base_path) / "user_story_real_reviews_agent" / "1_input" / project_name
    review_files = list(customer_reviews_input.glob("*.csv"))
    
    if review_files:
        print("Mode: VALIDATION MODE (Phase 2: 5->7->8->9)")
        return "validation", [5, 7, 8, 9]
    else:
        print("Mode: NEW BRAND MODE (Phase 2: 5->7->8->9)")
        return "new_brand", [5, 7, 8, 9]

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

def run_keywords_phase2(project_name, base_path):
    """Run keywords Phase 2 generation"""
    try:
        print("\nRunning Keywords Bank Phase 2: Expansion Engine...")
        
        original_cwd = os.getcwd()
        agent_dir = Path(base_path) / "keywords_bank_agent"
        os.chdir(agent_dir)
        
        result = subprocess.run([sys.executable, "scripts/generate_phase2.py"], 
                              capture_output=True, text=True, timeout=300)
        
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            print("Keywords Bank Phase 2 completed successfully")
            return True
        else:
            print(f"Keywords Bank Phase 2 failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error running Keywords Bank Phase 2: {e}")
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

def execute_phase2_pipeline(project_name, base_path, config, execution_sequence, mode):
    """Run Phase 2 pipeline with state tracking and resume functionality"""
    print(f"\nStarting Phase 2 pipeline execution for: {project_name}")
    print(f"Execution sequence: {' -> '.join(map(str, execution_sequence))}")
    
    # Load existing states - need to merge Phase 1 and Phase 2 completed agents
    phase1_state = load_phase1_state(project_name, base_path)
    state = load_phase2_state(project_name, base_path)
    
    # Merge completed agents from both phases for dependency checking
    phase1_completed = set(phase1_state.get('completed_agents', []) if phase1_state else [])
    phase2_completed = set(state['completed_agents'])
    all_completed_agents = phase1_completed | phase2_completed
    
    print(f"\nCurrent state: {len(state['completed_agents'])} Phase 2 agents completed")
    print(f"Total completed agents (Phase 1 + 2): {sorted(list(all_completed_agents))}")
    
    agent_mapping = config['agent_mapping']
    dependencies = config['agent_dependencies']
    
    for agent_number in execution_sequence:
        agent_name = agent_mapping[str(agent_number)]
        
        # Special handling for Keywords Bank Agent (Agent 5)
        if agent_number == 5:
            # Check if Phase 2 is already completed
            if state.get('keywords_phase2_completed', False):
                print(f"\nAgent 5 (Keywords Bank) Phase 2 already completed - SKIPPING")
                continue
            # Check if Phase 1 already approved
            approved, score = check_keywords_phase1_approved(project_name, base_path)
            if approved and not state['keywords_phase2_completed']:
                print(f"\nKeywords Phase 1 approved with score {score:.1f}, running Phase 2...")
                success = run_keywords_phase2(project_name, base_path)
                if success:
                    state['completed_agents'].append(agent_number)
                    state['keywords_approved'] = True
                    state['keywords_phase2_completed'] = True
                    
                    # Copy Keywords Phase 2 output to downstream agents
                    downstream_agents = []
                    for other_agent, deps in dependencies.items():
                        if agent_number in deps and int(other_agent) in execution_sequence:
                            downstream_agents.append(int(other_agent))
                    
                    if downstream_agents:
                        copy_success = copy_agent_output(
                            agent_number, downstream_agents, project_name, base_path, config
                        )
                        if not copy_success:
                            print(f"Warning: Copy operation partially failed for Keywords Phase 2")
                    
                    save_phase2_state(state, base_path)
                else:
                    if agent_number not in state['failed_agents']:
                        state['failed_agents'].append(agent_number)
                    save_phase2_state(state, base_path)
                    break
                continue
        
        # Generic completion check for other agents (7, 8, 9)
        if agent_number in state['completed_agents']:
            print(f"\nAgent {agent_number} already completed - SKIPPING")
            continue
        
        # Check dependencies using merged completed agents list - mode-aware
        required_deps = dependencies.get(str(agent_number), [])
        
        # Mode-aware dependency filtering
        if mode == "new_brand":
            # In New Brand Mode, remove Agent 3 dependency for agents 7 and 8
            if agent_number in [7, 8] and 3 in required_deps:
                required_deps = [dep for dep in required_deps if dep != 3]
                print(f">>> New Brand Mode: Removed Agent 3 dependency for Agent {agent_number}")
        
        missing_deps = [dep for dep in required_deps if dep not in all_completed_agents]
        
        if missing_deps:
            print(f"Skipping Agent {agent_number} - missing dependencies: {missing_deps}")
            continue
        
        # Copy all required dependencies before executing agent (including Phase 1 outputs)
        # Use the same filtered dependencies as the missing check above
        for dep_agent in required_deps:
            if dep_agent in all_completed_agents:
                copy_success = copy_agent_output(
                    dep_agent, [agent_number], project_name, base_path, config
                )
                if not copy_success:
                    print(f"Warning: Failed to copy files from Agent {dep_agent} to Agent {agent_number}")
            else:
                print(f"Debug: Dependency Agent {dep_agent} not found in completed agents for Agent {agent_number}")
                print(f"Available completed agents: {sorted(list(all_completed_agents))}")
        
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
            save_phase2_state(state, base_path)
            
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
            
            save_phase2_state(state, base_path)
            
            if not success:
                break_execution = input("Continue with remaining agents? (y/N): ").strip().lower()
                if break_execution != 'y':
                    break
    
    # Check if Phase 2 is complete
    expected_agents = set(execution_sequence)
    completed_agents = set(state['completed_agents'])
    
    if expected_agents.issubset(completed_agents):
        print(f"\nPHASE 2 COMPLETED SUCCESSFULLY!")
        return True
    else:
        missing_agents = expected_agents - completed_agents
        print(f"\nPhase 2 incomplete. Missing agents: {sorted(list(missing_agents))}")
        return False

def generate_phase2_report(project_name, base_path, config):
    """Generate Phase 2 execution report"""
    state = load_phase2_state(project_name, base_path)
    agent_mapping = config['agent_mapping']
    
    print(f"\n{'='*60}")
    print(f"PHASE 2 EXECUTION REPORT")
    print(f"{'='*60}")
    print(f"Project: {project_name}")
    print(f"Phase: Content Generation (Keywords + Agents 7-9)")
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
    
    # Check keywords approval status
    approved, score = check_keywords_phase1_approved(project_name, base_path)
    print(f"\nKeywords Status:")
    print(f"  Phase 1 Score: {score:.1f}")
    print(f"  Approved: {'YES' if approved else 'NO'}")
    print(f"  Phase 2 Complete: {'YES' if state['keywords_phase2_completed'] else 'NO'}")
    
    total_agents = len(state['completed_agents']) + len(state['failed_agents'])
    if total_agents > 0:
        success_rate = len(state['completed_agents']) / total_agents * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    # Check if complete pipeline is done
    expected_phase2_agents = {5, 7, 8, 9}
    completed_phase2_agents = set(state['completed_agents'])
    
    if expected_phase2_agents.issubset(completed_phase2_agents):
        print(f"\nPIPELINE COMPLETE!")
        print(f"All marketing assets ready for use in respective 3_unlabeled/{project_name}/ folders")
    else:
        missing_agents = expected_phase2_agents - completed_phase2_agents
        print(f"\nPipeline incomplete. Missing agents: {sorted(list(missing_agents))}")

def main():
    """Main execution function"""
    print("Agent 0b: Pipeline Orchestrator - Phase 2 Starting...")
    
    # Load configuration
    config = load_config()
    base_path = config['base_path']
    
    # Project selection
    project_name = select_project(base_path)
    print(f"\nSelected project: {project_name}")
    
    # Validate Phase 1 completion
    if not validate_phase1_completion(project_name, base_path):
        sys.exit(1)
    
    # Check keywords approval status
    approved, score = check_keywords_phase1_approved(project_name, base_path)
    print(f"Keywords evaluation status: {'APPROVED' if approved else 'NOT APPROVED'} (Score: {score:.1f})")
    
    # Mode detection
    mode, execution_sequence = detect_execution_mode(project_name, base_path)
    
    # Show current state
    state = load_phase2_state(project_name, base_path)
    if state['completed_agents']:
        print(f"\nRESUMING: {len(state['completed_agents'])} agents already completed")
        for agent_num in sorted(state['completed_agents']):
            agent_name = config['agent_mapping'][str(agent_num)]
            print(f"  Agent {agent_num}: {agent_name}")
    
    # Confirm execution
    remaining_agents = [a for a in execution_sequence if a not in state['completed_agents']]
    if remaining_agents:
        print(f"\nPhase 2 will execute {len(remaining_agents)} remaining agents: {remaining_agents}")
        confirm = input("Proceed with Phase 2 execution? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Phase 2 execution cancelled.")
            sys.exit(0)
    else:
        print(f"\nAll Phase 2 agents already completed!")
    
    # Execute Phase 2 pipeline
    success = execute_phase2_pipeline(project_name, base_path, config, execution_sequence, mode)
    
    # Generate report
    generate_phase2_report(project_name, base_path, config)
    
    if success:
        print(f"\nPhase 2 Complete! All marketing assets generated.")

if __name__ == "__main__":
    main()