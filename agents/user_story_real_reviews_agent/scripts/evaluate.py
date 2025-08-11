#!/usr/bin/env python3
"""
User Story Real Reviews Evaluation Tool

This script provides a GUI for evaluating user stories generated from customer reviews 
from 3_unlabeled/ and saving labeled results to 5_labeled_json/
"""

import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from datetime import datetime
from pathlib import Path
import traceback

class UserStoryReviewsEvaluator:
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
        self.user_stories = []
        self.current_index = 0
        
        # Scoring criteria with weights (adapted for review-based user stories)
        self.scoring_criteria = {
            "persona_authenticity": {"weight": 0.2, "description": "Believable demographics extracted from review language"},
            "narrative_depth": {"weight": 0.2, "description": "Vivid first-person scenarios reflecting real customer experiences"},
            "user_story_clarity": {"weight": 0.2, "description": "Clear 'As a... I want... So that...' format and actionability"},
            "emotional_resonance": {"weight": 0.2, "description": "Deep understanding of real customer emotions and pain points"},
            "review_alignment": {"weight": 0.2, "description": "Alignment with actual customer review content and experiences"}
        }
        
        # Improvement tags (adapted for review-based user stories)
        self.improvement_tags = [
            "persona_specificity", "narrative_vividness", "user_story_format", 
            "emotional_depth", "review_authenticity", "demographic_diversity"
        ]
        
        # Initialize scoring variables
        self.score_vars = {}
        self.tag_vars = {}
        
        # Setup UI
        self.setup_ui()
    
    def _load_current_project(self):
        """Load current project from config.json."""
        config_path = self.project_dir / "config.json"
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get("current_project", None)
        except:
            return None
    
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("User Story Reviews Evaluator")
        self.root.geometry("1400x900")
        
        # Top frame for file operations
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(top_frame, text="Load Unlabeled Files", command=self.load_unlabeled_files).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Save Evaluation", command=self.save_evaluation).pack(side=tk.LEFT, padx=5)
        
        # Create main content area with notebook
        main_notebook = ttk.Notebook(self.root)
        main_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Content tab
        content_frame = ttk.Frame(main_notebook)
        main_notebook.add(content_frame, text="User Stories Content")
        
        # Text area for displaying user stories
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
            
            # Label
            label_text = f"{criteria.replace('_', ' ').title()} ({info['weight']*100:.0f}%)"
            tk.Label(frame, text=label_text, width=25, anchor="w").pack(side=tk.LEFT)
            
            # Score scale
            var = tk.IntVar(value=5)
            self.score_vars[criteria] = var
            scale = tk.Scale(frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=var)
            scale.pack(side=tk.LEFT, padx=10)
            
            # Description
            tk.Label(frame, text=info['description'], font=("Arial", 9), fg="gray").pack(side=tk.LEFT, padx=10)
        
        # Overall score display
        overall_frame = tk.Frame(scoring_frame)
        overall_frame.pack(fill=tk.X, padx=5, pady=10)
        
        tk.Label(overall_frame, text="Overall Score:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        self.overall_score_var = tk.StringVar(value="5.0")
        tk.Label(overall_frame, textvariable=self.overall_score_var, font=("Arial", 12, "bold"), fg="blue").pack(side=tk.LEFT, padx=10)
        
        tk.Button(overall_frame, text="Calculate Score", command=self.calculate_overall_score).pack(side=tk.LEFT, padx=10)
        
        # Improvement tags section
        tags_frame = ttk.LabelFrame(scrollable_eval_frame, text="Improvement Areas")
        tags_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tags_grid_frame = tk.Frame(tags_frame)
        tags_grid_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for i, tag in enumerate(self.improvement_tags):
            var = tk.BooleanVar()
            self.tag_vars[tag] = var
            cb = tk.Checkbutton(tags_grid_frame, text=tag.replace('_', ' ').title(), variable=var)
            cb.grid(row=i//2, column=i%2, sticky="w", padx=10, pady=2)
        
        # Comments section
        comments_frame = ttk.LabelFrame(scrollable_eval_frame, text="Comments")
        comments_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.comments_text = scrolledtext.ScrolledText(comments_frame, height=5, wrap=tk.WORD, font=("Arial", 10))
        self.comments_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Navigation and status
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(nav_frame, text="Previous", command=self.prev_item).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next", command=self.next_item).pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar(value="No files loaded")
        tk.Label(nav_frame, textvariable=self.status_var).pack(side=tk.RIGHT, padx=5)
        
        # Bind score changes to auto-calculate
        for var in self.score_vars.values():
            var.trace("w", lambda *args: self.calculate_overall_score())
        
        self.root.mainloop()
    
    def load_unlabeled_files(self):
        """Load all .md files from 3_unlabeled/ directory with project-specific logic"""
        try:
            md_files = []
            
            # Try project-specific directory first
            if self.current_project:
                project_unlabeled_dir = self.project_dir / "3_unlabeled" / self.current_project
                if not project_unlabeled_dir.exists():
                    project_unlabeled_dir.mkdir(parents=True)
                
                # Look for userstories_reviews_*.md files in project directory
                md_files = list(project_unlabeled_dir.glob("userstories_reviews_*.md"))
                
                # If no files found in project directory, check root folder as fallback
                if not md_files:
                    root_unlabeled_dir = self.project_dir / "3_unlabeled"
                    if root_unlabeled_dir.exists():
                        md_files = list(root_unlabeled_dir.glob("userstories_reviews_*.md"))
            else:
                # Fallback to root directory
                if not self.unlabeled_dir.exists():
                    messagebox.showerror("Error", f"Unlabeled directory not found: {self.unlabeled_dir}")
                    return
                
                # Get all customer_side_persona_*.md files
                md_files = list(self.unlabeled_dir.glob("userstories_reviews_*.md"))
            
            if not md_files:
                messagebox.showwarning("Warning", f"No customer_side_persona_*.md files found")
                return
            
            # Load file contents
            self.user_stories = []
            for file_path in md_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    self.user_stories.append({
                        'file_path': file_path,
                        'file_name': file_path.name,
                        'content': content
                    })
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
            
            if self.user_stories:
                self.current_index = 0
                self.update_display()
                messagebox.showinfo("Success", f"Loaded {len(self.user_stories)} user story files")
            else:
                messagebox.showwarning("Warning", "No files could be loaded")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load files: {str(e)}")
            traceback.print_exc()
    
    def update_display(self):
        """Update the display with current user stories"""
        if not self.user_stories:
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, "No user stories loaded")
            self.status_var.set("No files loaded")
            return
        
        # Clear display
        self.text_display.delete(1.0, tk.END)
        
        # Get current user stories
        current = self.user_stories[self.current_index]
        
        # Display content
        self.text_display.insert(tk.END, f"File: {current['file_name']}\n")
        self.text_display.insert(tk.END, "="*50 + "\n\n")
        self.text_display.insert(tk.END, current['content'])
        
        # Update status
        self.status_var.set(f"File {self.current_index + 1} of {len(self.user_stories)}")
        
        # Reset evaluation form
        self.reset_evaluation_form()
    
    def reset_evaluation_form(self):
        """Reset all evaluation inputs"""
        # Reset scores to 5
        for var in self.score_vars.values():
            var.set(5)
        
        # Reset tags
        for var in self.tag_vars.values():
            var.set(False)
        
        # Clear comments
        self.comments_text.delete(1.0, tk.END)
        
        # Recalculate score
        self.calculate_overall_score()
    
    def calculate_overall_score(self):
        """Calculate weighted overall score"""
        total_score = 0
        total_weight = 0
        
        for criteria, info in self.scoring_criteria.items():
            score = self.score_vars[criteria].get()
            weight = info['weight']
            total_score += score * weight
            total_weight += weight
        
        overall = total_score / total_weight if total_weight > 0 else 0
        self.overall_score_var.set(f"{overall:.1f}")
    
    def save_current_evaluation(self):
        """Save current evaluation data"""
        if not self.user_stories:
            return None
        
        current = self.user_stories[self.current_index]
        
        # Calculate overall score
        self.calculate_overall_score()
        overall_score = float(self.overall_score_var.get())
        
        # Get detailed scores
        detailed_scores = {}
        for criteria, info in self.scoring_criteria.items():
            detailed_scores[criteria] = {
                "score": self.score_vars[criteria].get(),
                "weight": info['weight'],
                "comments": f"{criteria.replace('_', ' ').title()} evaluation"
            }
        
        # Get improvement tags
        selected_tags = [tag for tag, var in self.tag_vars.items() if var.get()]
        
        # Get comments
        comments = self.comments_text.get(1.0, tk.END).strip()
        
        # Create evaluation data
        evaluation_data = {
            "evaluation_metadata": {
                "document_id": current['file_name'].replace('.md', ''),
                "original_file_path": f"3_unlabeled/{current['file_name']}",
                "evaluation_date": datetime.now().isoformat(),
                "evaluator_id": "human_reviewer",
                "evaluation_version": "1.0",
                "overall_score": overall_score,
                "source_type": "customer_reviews"
            },
            "detailed_scores": detailed_scores,
            "improvement_analysis": {
                "tags": selected_tags,
                "strengths": [],
                "minor_improvements": selected_tags
            },
            "comments": comments,
            "user_stories_content": {
                "generated_personas": current['content']
            },
            "system_learning": {
                "example_quality": "high" if overall_score >= 8.5 else "medium" if overall_score >= 7.0 else "low",
                "use_as_training": overall_score >= 7.0,
                "key_patterns": []
            }
        }
        
        return evaluation_data
    
    def save_evaluation(self):
        """Save current evaluation to 5_labeled_json/"""
        evaluation_data = self.save_current_evaluation()
        if not evaluation_data:
            messagebox.showwarning("Warning", "No evaluation to save")
            return
        
        try:
            # Ensure labeled directory exists
            self.labeled_dir.mkdir(exist_ok=True)
            
            # Create filename
            doc_id = evaluation_data["evaluation_metadata"]["document_id"]
            filename = f"{doc_id}_labeled.json"
            file_path = self.labeled_dir / filename
            
            # Save to JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(evaluation_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Evaluation saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save evaluation: {str(e)}")
            traceback.print_exc()
    
    def next_item(self):
        """Move to next user story"""
        if not self.user_stories:
            return
        
        if self.current_index < len(self.user_stories) - 1:
            self.current_index += 1
            self.update_display()
    
    def prev_item(self):
        """Move to previous user story"""
        if not self.user_stories:
            return
        
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()

if __name__ == "__main__":
    evaluator = UserStoryReviewsEvaluator()