#!/usr/bin/env python3
"""
Testimonial Evaluation Tool

This script provides a GUI for evaluating testimonials from 3_unlabeled/
and saving labeled results to 5_labeled_json/
"""

import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from datetime import datetime
from pathlib import Path
import traceback

class TestimonialEvaluator:
    def __init__(self):
        # Set up paths
        self.script_dir = Path(__file__).parent
        self.project_dir = self.script_dir.parent
        self.current_project = self._load_current_project()
        
        # Set up project-specific paths
        if self.current_project:
            self.unlabeled_dir = self.project_dir / "3_unlabeled" / self.current_project
            self.labeled_dir = self.project_dir / "5_labeled_json"
        else:
            # Fallback to root directories if no project specified
            self.unlabeled_dir = self.project_dir / "3_unlabeled"
            self.labeled_dir = self.project_dir / "5_labeled_json"
        
        # Initialize data
        self.testimonials = []
        self.current_index = 0
        
        # Scoring criteria with weights (adapted for testimonials)
        self.scoring_criteria = {
            "authenticity": {"weight": 0.25, "description": "Believable customer voice and realistic scenarios"},
            "strategic_alignment": {"weight": 0.20, "description": "Reflects brand positioning and value props"},
            "emotional_resonance": {"weight": 0.20, "description": "Connects with target audience pain points and desires"},
            "believability": {"weight": 0.20, "description": "Sounds like real customer experiences, not marketing copy"},
            "marketing_effectiveness": {"weight": 0.15, "description": "Ready for immediate use across marketing channels"}
        }
        
        # Improvement tags (adapted for testimonials)
        self.improvement_tags = [
            "more_authentic_voice", "strategic_alignment", "emotional_depth", 
            "believability_issues", "marketing_readiness", "customer_diversity"
        ]
        
        # Initialize scoring variables
        self.score_vars = {}
        self.tag_vars = {}
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Testimonial Evaluator")
        self.root.geometry("1400x900")
        
        # Top frame for file operations
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(top_frame, text="Load Unlabeled Files", command=self.load_unlabeled_files).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Save Evaluation", command=self.save_evaluation).pack(side=tk.LEFT, padx=5)
        
        # File selection dropdown
        self.file_var = tk.StringVar()
        self.file_dropdown = ttk.Combobox(top_frame, textvariable=self.file_var, state="readonly", width=40)
        self.file_dropdown.pack(side=tk.LEFT, padx=10)
        self.file_dropdown.bind("<<ComboboxSelected>>", self.load_selected_file)
        
        # Create main content area with notebook
        main_notebook = ttk.Notebook(self.root)
        main_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Content tab
        content_frame = ttk.Frame(main_notebook)
        main_notebook.add(content_frame, text="Testimonials Content")
        
        # Text area for displaying testimonials
        self.text_display = scrolledtext.ScrolledText(content_frame, height=25, wrap=tk.WORD, font=("Arial", 11))
        self.text_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Evaluation tab
        eval_frame = ttk.Frame(main_notebook)
        main_notebook.add(eval_frame, text="Evaluation")
        
        # Create scrollable frame for evaluation
        canvas = tk.Canvas(eval_frame)
        scrollbar = ttk.Scrollbar(eval_frame, orient="vertical", command=canvas.yview)
        scrollable_eval_frame = ttk.Frame(canvas)
        
        scrollable_eval_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_eval_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scoring section
        scoring_frame = ttk.LabelFrame(scrollable_eval_frame, text="Scoring (1-10 scale)")
        scoring_frame.pack(fill=tk.X, padx=10, pady=10)
        
        for i, (criteria, info) in enumerate(self.scoring_criteria.items()):
            frame = tk.Frame(scoring_frame)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Criteria label with description
            label_text = f"{criteria.replace('_', ' ').title()} ({info['weight']*100:.0f}%)"
            tk.Label(frame, text=label_text, width=25, anchor='w').pack(side=tk.LEFT)
            
            # Score variable and scale
            self.score_vars[criteria] = tk.IntVar(value=7)
            scale = tk.Scale(frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.score_vars[criteria], length=200)
            scale.pack(side=tk.LEFT, padx=10)
            
            # Description label
            tk.Label(frame, text=info['description'], anchor='w', fg='gray').pack(side=tk.LEFT, padx=10)
        
        # Overall score display
        self.overall_score_var = tk.StringVar(value="Overall Score: 7.0")
        overall_label = tk.Label(scoring_frame, textvariable=self.overall_score_var, font=("Arial", 12, "bold"))
        overall_label.pack(pady=10)
        
        # Update overall score when individual scores change
        for var in self.score_vars.values():
            var.trace('w', self.update_overall_score)
        
        # Improvement tags section
        tags_frame = ttk.LabelFrame(scrollable_eval_frame, text="Improvement Areas (optional)")
        tags_frame.pack(fill=tk.X, padx=10, pady=10)
        
        for tag in self.improvement_tags:
            self.tag_vars[tag] = tk.BooleanVar()
            cb = tk.Checkbutton(tags_frame, text=tag.replace('_', ' ').title(), 
                              variable=self.tag_vars[tag])
            cb.pack(anchor='w', padx=5, pady=2)
        
        # Notes section
        notes_frame = ttk.LabelFrame(scrollable_eval_frame, text="Additional Notes")
        notes_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.notes_text = tk.Text(notes_frame, height=4, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Load unlabeled files automatically
        self.load_unlabeled_files()
    
    def _load_current_project(self):
        """Load current project from config.json."""
        config_path = self.project_dir / "config.json"
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get("current_project", None)
        except:
            return None
    
    def update_overall_score(self, *args):
        """Update overall score display"""
        try:
            total_score = 0
            for criteria, score_var in self.score_vars.items():
                weight = self.scoring_criteria[criteria]['weight']
                total_score += score_var.get() * weight
            
            self.overall_score_var.set(f"Overall Score: {total_score:.2f}")
        except:
            pass
    
    def load_unlabeled_files(self):
        """Load all unlabeled testimonial files"""
        try:
            md_files = []
            
            # Try project-specific directory first
            if self.current_project:
                if not self.unlabeled_dir.exists():
                    self.unlabeled_dir.mkdir(parents=True)
                md_files = list(self.unlabeled_dir.glob("testimonials_*.md"))
                
                # If no files in project folder, check root folder as fallback
                if not md_files:
                    root_unlabeled_dir = self.project_dir / "3_unlabeled"
                    if root_unlabeled_dir.exists():
                        md_files = list(root_unlabeled_dir.glob("testimonials_*.md"))
            else:
                # No project specified, use root directory
                if not self.unlabeled_dir.exists():
                    messagebox.showerror("Error", f"Unlabeled directory not found: {self.unlabeled_dir}")
                    return
                md_files = list(self.unlabeled_dir.glob("testimonials_*.md"))
            
            if not md_files:
                messagebox.showinfo("Info", "No testimonial files found in 3_unlabeled/")
                return
            
            # Sort by modification time (newest first)
            md_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
            # Update dropdown
            file_names = [f.name for f in md_files]
            self.file_dropdown['values'] = file_names
            
            # Auto-select the most recent file
            if file_names:
                self.file_dropdown.set(file_names[0])
                self.load_selected_file()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load unlabeled files: {e}")
    
    def load_selected_file(self, event=None):
        """Load the selected file"""
        try:
            selected_file = self.file_var.get()
            if not selected_file:
                return
            
            file_path = self.unlabeled_dir / selected_file
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Display content
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(1.0, content)
            
            # Store current file info
            self.current_file = file_path
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def save_evaluation(self):
        """Save the current evaluation"""
        try:
            if not hasattr(self, 'current_file'):
                messagebox.showwarning("Warning", "No file loaded to evaluate")
                return
            
            # Calculate overall score
            overall_score = 0
            criteria_scores = {}
            for criteria, score_var in self.score_vars.items():
                score = score_var.get()
                weight = self.scoring_criteria[criteria]['weight']
                criteria_scores[criteria] = score
                overall_score += score * weight
            
            # Get selected improvement tags
            selected_tags = [tag for tag, var in self.tag_vars.items() if var.get()]
            
            # Get notes
            notes = self.notes_text.get(1.0, tk.END).strip()
            
            # Create evaluation data
            evaluation_data = {
                "file_path": str(self.current_file),
                "evaluation_date": datetime.now().isoformat(),
                "overall_score": overall_score,
                "criteria_scores": criteria_scores,
                "criteria_weights": {k: v['weight'] for k, v in self.scoring_criteria.items()},
                "improvement_tags": selected_tags,
                "notes": notes,
                "passed_threshold": overall_score >= 7.0,
                "evaluator": "human"
            }
            
            # Create output filename
            base_name = self.current_file.stem
            output_filename = f"{base_name}_labeled.json"
            output_path = self.labeled_dir / output_filename
            
            # Ensure labeled directory exists
            self.labeled_dir.mkdir(exist_ok=True)
            
            # Save evaluation
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(evaluation_data, f, indent=2)
            
            messagebox.showinfo("Success", f"Evaluation saved to: {output_filename}\\n\\nOverall Score: {overall_score:.2f}")
            
            # Reset form for next evaluation
            self.reset_evaluation_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save evaluation: {e}")
            print(traceback.format_exc())
    
    def reset_evaluation_form(self):
        """Reset the evaluation form"""
        # Reset scores to default (7)
        for var in self.score_vars.values():
            var.set(7)
        
        # Clear improvement tags
        for var in self.tag_vars.values():
            var.set(False)
        
        # Clear notes
        self.notes_text.delete(1.0, tk.END)
    
    def run(self):
        """Start the evaluation GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        evaluator = TestimonialEvaluator()
        evaluator.run()
    except Exception as e:
        print(f"Error starting testimonial evaluator: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()