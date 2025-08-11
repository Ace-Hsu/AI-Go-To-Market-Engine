#!/usr/bin/env python3
"""
Keywords Bank Agent - Phase 1 Evaluation Script
GUI-based evaluation system using 5-criteria framework
"""

import os
import json
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
from typing import Dict, List, Optional

class KeywordsBankPhase1Evaluator:
    def __init__(self):
        """Initialize the Phase 1 evaluator with GUI."""
        self.base_dir = Path(__file__).parent.parent
        self.current_project = self._load_current_project()
        self.root = tk.Tk()
        self.root.title("Keywords Bank Agent - Phase 1 Evaluation")
        self.root.geometry("1000x800")
        
        # Evaluation criteria
        self.criteria = {
            "strategic_alignment": {
                "name": "Strategic Alignment",
                "description": "Message house extraction quality and brand consistency",
                "weight": 0.25,
                "score": tk.IntVar(value=5)
            },
            "completeness": {
                "name": "Completeness", 
                "description": "All persona language and themes captured",
                "weight": 0.20,
                "score": tk.IntVar(value=5)
            },
            "creative_expansion": {
                "name": "Creative Expansion",
                "description": "Semantic variations quality beyond simple synonyms",
                "weight": 0.20,
                "score": tk.IntVar(value=5)
            },
            "insightfulness": {
                "name": "Insightfulness",
                "description": "Thematic cluster analysis and strategic synthesis",
                "weight": 0.20,
                "score": tk.IntVar(value=5)
            },
            "actionability": {
                "name": "Actionability",
                "description": "Clear structure for expansion engine usage",
                "weight": 0.15,
                "score": tk.IntVar(value=5)
            }
        }
        
        self.current_file = None
        self.evaluation_data = {}
        
        self.create_gui()
        
    def _load_current_project(self) -> Optional[str]:
        """Load current project from config.json."""
        config_path = self.base_dir / "config.json"
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get("current_project", None)
        except:
            return None
        
    def create_gui(self):
        """Create the main GUI interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Keywords Bank Agent - Phase 1 Evaluation", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Select File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.file_var = tk.StringVar()
        self.file_combo = ttk.Combobox(file_frame, textvariable=self.file_var, state="readonly")
        self.file_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        refresh_btn = ttk.Button(file_frame, text="Refresh", command=self.refresh_files)
        refresh_btn.grid(row=0, column=2)
        
        load_btn = ttk.Button(file_frame, text="Load File", command=self.load_file)
        load_btn.grid(row=0, column=3, padx=(10, 0))
        
        # Content and evaluation frame
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Content display
        content_label_frame = ttk.LabelFrame(content_frame, text="Generated Content", padding="10")
        content_label_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        content_label_frame.columnconfigure(0, weight=1)
        content_label_frame.rowconfigure(0, weight=1)
        
        self.content_text = scrolledtext.ScrolledText(content_label_frame, wrap=tk.WORD, 
                                                     width=50, height=20)
        self.content_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Evaluation panel
        eval_frame = ttk.LabelFrame(content_frame, text="Evaluation Criteria", padding="10")
        eval_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        eval_frame.columnconfigure(0, weight=1)
        
        # Criteria evaluation
        row = 0
        for key, criteria in self.criteria.items():
            # Criteria name and description
            name_label = ttk.Label(eval_frame, text=f"{criteria['name']}", 
                                 font=("Arial", 10, "bold"))
            name_label.grid(row=row, column=0, sticky=tk.W, pady=(10, 0))
            
            desc_label = ttk.Label(eval_frame, text=criteria['description'], 
                                 font=("Arial", 8), foreground="gray")
            desc_label.grid(row=row+1, column=0, sticky=tk.W, pady=(0, 5))
            
            # Score scale
            score_frame = ttk.Frame(eval_frame)
            score_frame.grid(row=row+2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            
            ttk.Label(score_frame, text="Score:").grid(row=0, column=0, sticky=tk.W)
            
            scale = tk.Scale(score_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                           variable=criteria['score'], length=200)
            scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
            
            score_frame.columnconfigure(1, weight=1)
            row += 3
            
        # Score display
        score_display_frame = ttk.Frame(eval_frame)
        score_display_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        
        ttk.Label(score_display_frame, text="Current Score:", font=("Arial", 12, "bold")).grid(row=0, column=0)
        self.score_label = ttk.Label(score_display_frame, text="0.0", 
                                    font=("Arial", 14, "bold"), foreground="red")
        self.score_label.grid(row=0, column=1, padx=(10, 0))
        
        # Update score button
        update_btn = ttk.Button(eval_frame, text="Update Score", command=self.update_score)
        update_btn.grid(row=row+1, column=0, pady=(10, 0))
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=3, pady=(20, 0))
        
        save_btn = ttk.Button(action_frame, text="Save Evaluation", command=self.save_evaluation)
        save_btn.grid(row=0, column=0, padx=(0, 10))
        
        approve_btn = ttk.Button(action_frame, text="Approve & Continue to Phase 2", 
                               command=self.approve_and_continue)
        approve_btn.grid(row=0, column=1, padx=(0, 10))
        
        reject_btn = ttk.Button(action_frame, text="Reject & Regenerate", 
                              command=self.reject_and_regenerate)
        reject_btn.grid(row=0, column=2)
        
        # Initialize
        self.refresh_files()
        
    def refresh_files(self):
        """Refresh the list of available files."""
        if self.current_project:
            # Use project-specific directory
            unlabeled_dir = self.base_dir / "3_unlabeled" / self.current_project
            if not unlabeled_dir.exists():
                unlabeled_dir.mkdir(parents=True)
            files = list(unlabeled_dir.glob("keywords_bank_vocabulary_*.md"))
            
            # If no files in project folder, check root folder as fallback
            if not files:
                root_unlabeled_dir = self.base_dir / "3_unlabeled"
                if root_unlabeled_dir.exists():
                    files = list(root_unlabeled_dir.glob("keywords_bank_vocabulary_*.md"))
        else:
            # Fallback to root directory
            unlabeled_dir = self.base_dir / "3_unlabeled"
            if not unlabeled_dir.exists():
                unlabeled_dir.mkdir(parents=True)
            files = list(unlabeled_dir.glob("keywords_bank_vocabulary_*.md"))
            
        file_names = [f.name for f in sorted(files, key=os.path.getmtime, reverse=True)]
        
        self.file_combo['values'] = file_names
        if file_names:
            self.file_combo.set(file_names[0])
            
    def load_file(self):
        """Load the selected file for evaluation."""
        if not self.file_var.get():
            messagebox.showerror("Error", "Please select a file to load.")
            return
            
        # Try project-specific directory first
        if self.current_project:
            file_path = self.base_dir / "3_unlabeled" / self.current_project / self.file_var.get()
            if not file_path.exists():
                # Fallback to root directory
                file_path = self.base_dir / "3_unlabeled" / self.file_var.get()
        else:
            # Use root directory
            file_path = self.base_dir / "3_unlabeled" / self.file_var.get()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, content)
            self.current_file = file_path
            
            # Load existing evaluation if available
            self.load_existing_evaluation()
            
            messagebox.showinfo("Success", f"Loaded file: {file_path.name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            
    def load_existing_evaluation(self):
        """Load existing evaluation data if available."""
        if not self.current_file:
            return
            
        json_dir = self.base_dir / "5_labeled_json"
        json_file = json_dir / f"{self.current_file.stem}_labeled.json"
        
        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Load scores
                if 'criteria_scores' in data:
                    for key, score in data['criteria_scores'].items():
                        if key in self.criteria:
                            self.criteria[key]['score'].set(score)
                            
                self.update_score()
                
            except Exception as e:
                print(f"Failed to load existing evaluation: {e}")
                
    def update_score(self):
        """Update the overall score based on criteria weights."""
        total_score = 0
        for key, criteria in self.criteria.items():
            score = criteria['score'].get()
            weight = criteria['weight']
            total_score += score * weight
            
        # Update display
        color = "green" if total_score >= 7.0 else "orange" if total_score >= 5.0 else "red"
        self.score_label.config(text=f"{total_score:.1f}", foreground=color)
        
        return total_score
        
    def save_evaluation(self):
        """Save the evaluation data to JSON."""
        if not self.current_file:
            messagebox.showerror("Error", "No file loaded for evaluation.")
            return
            
        score = self.update_score()
        
        evaluation_data = {
            "file_path": str(self.current_file),
            "evaluation_date": datetime.datetime.now().isoformat(),
            "overall_score": score,
            "criteria_scores": {key: criteria['score'].get() for key, criteria in self.criteria.items()},
            "criteria_weights": {key: criteria['weight'] for key, criteria in self.criteria.items()},
            "passed_threshold": score >= 7.0,
            "evaluator": "human"
        }
        
        # Save to labeled JSON directory
        json_dir = self.base_dir / "5_labeled_json"
        json_dir.mkdir(exist_ok=True)
        
        json_file = json_dir / f"{self.current_file.stem}_labeled.json"
        
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(evaluation_data, f, indent=2)
                
            messagebox.showinfo("Success", f"Evaluation saved to: {json_file.name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save evaluation: {str(e)}")
            
    def approve_and_continue(self):
        """Approve the current evaluation and continue to Phase 2."""
        if not self.current_file:
            messagebox.showerror("Error", "No file loaded for evaluation.")
            return
            
        score = self.update_score()
        
        if score < 7.0:
            if not messagebox.askyesno("Low Score Warning", 
                                     f"Current score is {score:.1f}, below the 7.0 threshold. "
                                     "Are you sure you want to approve and continue?"):
                return
                
        # Save evaluation
        self.save_evaluation()
        
        # Show next steps
        messagebox.showinfo("Approved", 
                          f"Phase 1 approved with score {score:.1f}!\n\n"
                          "Next steps:\n"
                          "1. Run generate_phase2.py to create expansion engine\n"
                          "2. Phase 2 output will feed directly into Agents 7, 8, 9")
        
    def reject_and_regenerate(self):
        """Reject the current evaluation and suggest regeneration."""
        if not self.current_file:
            messagebox.showerror("Error", "No file loaded for evaluation.")
            return
            
        score = self.update_score()
        
        # Save evaluation
        self.save_evaluation()
        
        # Show regeneration instructions
        messagebox.showinfo("Rejected", 
                          f"Phase 1 rejected with score {score:.1f}.\n\n"
                          "Next steps:\n"
                          "1. Review the generated content\n"
                          "2. Adjust inputs if needed\n"
                          "3. Run generate_phase1.py again\n"
                          "4. Re-evaluate until score ≥ 7.0")
        
    def run(self):
        """Run the evaluation GUI."""
        self.root.mainloop()

if __name__ == "__main__":
    evaluator = KeywordsBankPhase1Evaluator()
    evaluator.run()