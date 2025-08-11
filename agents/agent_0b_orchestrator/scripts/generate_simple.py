#!/usr/bin/env python3
"""
Agent 0b: Pipeline Orchestrator Script

This script executes complete agent pipeline with automated file management.
Run MULTIPLE times for same project with different inputs.
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

def detect_execution_mode(project_name, base_path):
    """Detect execution mode based on available input files"""
    print(f"\nDetecting execution mode for project: {project_name}")
    
    # Check required files
    message_house_input = Path(base_path) / "message_house_agent" / "1_input" / project_name
    customer_reviews_input = Path(base_path) / "user_story_real_reviews_agent" / "1_input" / project_name
    
    # Check if message house input exists
    qa_files = list(message_house_input.glob("*.md"))
    if not qa_files:
        print("❌ ERROR: No Q&A input file found in message_house_agent input folder")
        print(f"Expected location: {message_house_input}")
        return None, []
    
    # Check if customer reviews exist
    review_files = list(customer_reviews_input.glob("*.csv"))
    
    if review_files:
        print("✅ Found Q&A input and customer reviews")
        print("🔄 Mode: VALIDATION MODE (Full Pipeline: 1→2→3→4→5→7→8→9)")
        return "validation", [1, 2, 3, 4, 5, 7, 8, 9]
    else:
        print("✅ Found Q&A input, no customer reviews")
        print("🔄 Mode: NEW BRAND MODE (Streamlined: 1→2→5→7→8→9)")
        return "new_brand", [1, 2, 5, 7, 8, 9]

def run_agent_script(agent_number, agent_name, base_path, project_name):
    """Execute specific agent's generate_simple.py script"""
    print(f"\n{'='*50}")
    print(f"Running Agent {agent_number}: {agent_name}")
    print(f"{'='*50}")
    
    agent_path = Path(base_path) / agent_name
    script_path = agent_path / "scripts" / "generate_simple.py"
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
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
            print(f"✅ Agent {agent_number} completed successfully")
            print("Output:", result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
            return True
        else:
            print(f"❌ Agent {agent_number} failed with error code {result.returncode}")
            print("Error output:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Agent {agent_number} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running Agent {agent_number}: {e}")
        return False

def get_latest_output(agent_name, project_name, base_path):
    """Find most recent output file from agent"""
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
        print(f"❌ No output file found from Agent {source_agent}")
        return False
    
    print(f"\n📂 Copying output from Agent {source_agent} to downstream agents...")
    print(f"Source file: {source_file.name}")
    
    success_count = 0
    for target_agent in target_agents:
        target_agent_name = agent_mapping[str(target_agent)]
        target_dir = Path(base_path) / target_agent_name / "1_input" / project_name
        
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / source_file.name
            shutil.copy2(source_file, target_path)
            print(f"  ✅ Copied to Agent {target_agent}: {target_agent_name}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ Failed to copy to Agent {target_agent}: {e}")
    
    print(f"📂 Copy operation completed: {success_count}/{len(target_agents)} successful")
    return success_count == len(target_agents)

def check_keywords_phase1_approved(project_name, base_path):
    """Check if keywords Phase 1 has been evaluated and approved"""
    keywords_labeled_dir = Path(base_path) / "keywords_bank_agent" / "5_labeled_json"
    
    if not keywords_labeled_dir.exists():
        return False
    
    # Look for recent evaluation JSON files
    json_files = list(keywords_labeled_dir.glob("*.json"))
    if not json_files:
        return False
    
    # Check the most recent evaluation
    latest_eval = max(json_files, key=lambda f: f.stat().st_mtime)
    
    try:
        with open(latest_eval, 'r', encoding='utf-8') as f:
            eval_data = json.load(f)
        
        # Check if score is >= 7.0 (approval threshold)
        overall_score = eval_data.get('overall_score', 0)
        return overall_score >= 7.0
        
    except:
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

def execute_pipeline(project_name, base_path, config, execution_sequence):
    """Run complete pipeline with proper sequencing and keywords pause/resume"""
    print(f"\nStarting pipeline execution for: {project_name}")
    print(f"Execution sequence: {' -> '.join(map(str, execution_sequence))}")
    
    agent_mapping = config['agent_mapping']
    dependencies = config['agent_dependencies']
    
    completed_agents = []
    failed_agents = []
    
    for agent_number in execution_sequence:
        agent_name = agent_mapping[str(agent_number)]
        
        # Check dependencies
        required_deps = dependencies.get(str(agent_number), [])
        missing_deps = [dep for dep in required_deps if dep not in completed_agents]
        
        if missing_deps:
            print(f"Skipping Agent {agent_number} - missing dependencies: {missing_deps}")
            continue
        
        # Special handling for Keywords Bank Agent (Agent 5)
        if agent_number == 5:
            # Check if Phase 1 already approved
            if check_keywords_phase1_approved(project_name, base_path):
                print(f"\nKeywords Phase 1 already approved, running Phase 2...")
                success = run_keywords_phase2(project_name, base_path)
                if success:
                    completed_agents.append(agent_number)
                else:
                    failed_agents.append(agent_number)
                    break
                continue
            else:
                # Run Phase 1 and pause for evaluation
                success = run_agent_script(agent_number, agent_name, base_path, project_name)
                if success:
                    print(f"""
==================================================
PIPELINE PAUSED: Keywords Bank Phase 1 Complete
==================================================

REQUIRED NEXT STEP: Human Evaluation
   Run: python keywords_bank_agent/scripts/evaluate_phase1.py
   
   - Evaluate vocabulary quality
   - Score must be >=7.0 to proceed
   - This ensures high-quality marketing assets

RESUME PIPELINE: Run Agent 0b again after evaluation
   The system will detect approval and continue automatically

WARNING: Do not skip evaluation - this is the quality gate!
""")
                    return completed_agents, failed_agents  # Clean exit for evaluation
                else:
                    failed_agents.append(agent_number)
                    break
        else:
            # Normal agent execution
            success = run_agent_script(agent_number, agent_name, base_path, project_name)
        
        if success:
            completed_agents.append(agent_number)
            
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
                    print(f"⚠️ Warning: Copy operation partially failed for Agent {agent_number}")
        else:
            failed_agents.append(agent_number)
            
            # Ask user if they want to continue
            retry = input(f"\nAgent {agent_number} failed. Retry? (y/N): ").strip().lower()
            if retry == 'y':
                # Retry once
                success = run_agent_script(agent_number, agent_name, base_path, project_name)
                if success:
                    completed_agents.append(agent_number)
                    failed_agents.remove(agent_number)
                else:
                    break_execution = input("Continue with remaining agents? (y/N): ").strip().lower()
                    if break_execution != 'y':
                        break
            else:
                break_execution = input("Continue with remaining agents? (y/N): ").strip().lower()
                if break_execution != 'y':
                    break
    
    return completed_agents, failed_agents

def generate_execution_report(project_name, mode, completed_agents, failed_agents, config):
    """Generate execution report"""
    agent_mapping = config['agent_mapping']
    
    print(f"\n{'='*60}")
    print(f"PIPELINE EXECUTION REPORT")
    print(f"{'='*60}")
    print(f"Project: {project_name}")
    print(f"Mode: {mode.upper()}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n✅ COMPLETED AGENTS ({len(completed_agents)}):")
    for agent_num in completed_agents:
        agent_name = agent_mapping[str(agent_num)]
        print(f"  Agent {agent_num}: {agent_name}")
    
    if failed_agents:
        print(f"\n❌ FAILED AGENTS ({len(failed_agents)}):")
        for agent_num in failed_agents:
            agent_name = agent_mapping[str(agent_num)]
            print(f"  Agent {agent_num}: {agent_name}")
    
    print(f"\n📁 GENERATED ASSETS:")
    base_path = config['base_path']
    for agent_num in completed_agents:
        agent_name = agent_mapping[str(agent_num)]
        output_file = get_latest_output(agent_name, project_name, base_path)
        if output_file:
            print(f"  {agent_name}: {output_file.name}")
    
    success_rate = len(completed_agents) / (len(completed_agents) + len(failed_agents)) * 100
    print(f"\n📊 Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print(f"\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"All marketing assets ready for use in respective 3_unlabeled/{project_name}/ folders")
    else:
        print(f"\n⚠️ PIPELINE COMPLETED WITH ISSUES")
        print(f"Review failed agents and retry if needed")

def save_execution_log(project_name, mode, completed_agents, failed_agents, config):
    """Save execution log"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"pipeline_execution_{project_name}_{timestamp}.json"
    log_path = Path(__file__).parent.parent / "3_unlabeled" / log_filename
    
    log_data = {
        "execution_timestamp": timestamp,
        "project_name": project_name,
        "execution_mode": mode,
        "completed_agents": completed_agents,
        "failed_agents": failed_agents,
        "success_rate": len(completed_agents) / (len(completed_agents) + len(failed_agents)) * 100
    }
    
    try:
        log_path.parent.mkdir(exist_ok=True)
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
        print(f"\nExecution log saved: {log_path}")
    except Exception as e:
        print(f"Warning: Could not save execution log: {e}")

def main():
    """Main execution function"""
    print("Agent 0b: Pipeline Orchestrator Starting...")
    
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
    
    # Confirm execution
    print(f"\nPipeline will execute {len(execution_sequence)} agents")
    confirm = input("Proceed with pipeline execution? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Pipeline execution cancelled.")
        sys.exit(0)
    
    # Execute pipeline
    completed_agents, failed_agents = execute_pipeline(
        project_name, base_path, config, execution_sequence
    )
    
    # Generate report
    generate_execution_report(project_name, mode, completed_agents, failed_agents, config)
    
    # Save log
    save_execution_log(project_name, mode, completed_agents, failed_agents, config)

if __name__ == "__main__":
    main()