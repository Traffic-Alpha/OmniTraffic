"""OmniTraffic VQA Web Test"""

from __future__ import annotations

import json
import os
import random
import time
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

import config

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_questions(path: str) -> List[Dict[str, Any]]:
    """Load questions from a JSONL file."""
    questions: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if isinstance(obj, dict):
                questions.append(obj)
    return questions


QUESTIONS: List[Dict[str, Any]] = load_questions(config.QUESTION_JSONL)

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
# Allow larger session cookies (100 questions of answers)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


# ---------------------------------------------------------------------------
# Image serving — serve images from QA_sampling/images/
# ---------------------------------------------------------------------------

@app.route("/images/<path:filename>")
def serve_image(filename: str):
    """Serve image files from the QA_sampling images directory."""
    return send_from_directory(config.IMAGES_DIR, filename)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Homepage — enter username to begin."""
    return render_template("index.html", total_questions=len(QUESTIONS))


@app.route("/start", methods=["POST"])
def start():
    """Initialise a new quiz session."""
    username = request.form.get("username", "").strip()
    if not username:
        return redirect(url_for("index"))

    # Build question order
    order = list(range(len(QUESTIONS)))
    if config.SHUFFLE_QUESTIONS:
        random.shuffle(order)

    session["username"] = username
    session["order"] = order
    session["answers"] = {}          # {str(q_idx): {"selected": "A", "time_spent": float}}
    session["start_time"] = time.time()
    session["q_start_time"] = time.time()  # time when current question was shown

    return redirect(url_for("quiz", q_pos=0))


@app.route("/quiz/<int:q_pos>")
def quiz(q_pos: int):
    """Render question at position *q_pos* in the user's order."""
    if "username" not in session:
        return redirect(url_for("index"))

    order = session.get("order", [])
    if q_pos < 0 or q_pos >= len(order):
        return redirect(url_for("result"))

    # Allow free navigation - removed restriction on going back

    q_idx = order[q_pos]
    question = QUESTIONS[q_idx]

    # Record the time this question page was rendered (only if not answered yet)
    answers = session.get("answers", {})
    if str(q_idx) not in answers:
        session["q_start_time"] = time.time()
        session.modified = True

    # Determine image mode
    image_mode = "none"
    if question.get("option_images"):
        image_mode = "option_images"
    elif question.get("images"):
        image_mode = "multi"
    elif question.get("image_path"):
        image_mode = "single"

    # Build answer status list for navigation
    answer_status = []
    for i, idx in enumerate(order):
        answer_status.append({
            "pos": i,
            "answered": str(idx) in answers,
            "selected": answers.get(str(idx), {}).get("selected", "")
        })

    # Check if all questions are answered
    all_answered = len(answers) == len(order)

    return render_template(
        "quiz.html",
        question=question,
        q_pos=q_pos,
        q_idx=q_idx,
        total=len(order),
        image_mode=image_mode,
        progress_pct=round(len(answers) / len(order) * 100),
        answer_status=answer_status,
        all_answered=all_answered,
        current_answer=answers.get(str(q_idx), {}).get("selected", ""),
    )


@app.route("/submit", methods=["POST"])
def submit():
    """Record user answer and navigate based on action."""
    if "username" not in session:
        return redirect(url_for("index"))

    q_pos = int(request.form.get("q_pos", 0))
    selected = request.form.get("selected", "")
    q_idx = int(request.form.get("q_idx", 0))
    action = request.form.get("action", "next")  # next, prev, jump, finish

    # Calculate time spent on this question (only if not previously answered)
    answers: Dict[str, Any] = session.get("answers", {})
    if str(q_idx) not in answers:
        q_start = session.get("q_start_time", time.time())
        time_spent = round(time.time() - q_start, 2)
    else:
        time_spent = answers[str(q_idx)].get("time_spent", 0)

    # Save answer (only if an option is selected)
    if selected:
        answers[str(q_idx)] = {
            "selected": selected,
            "time_spent": time_spent,
        }
        session["answers"] = answers
        session.modified = True

    order = session.get("order", [])

    # Handle different actions
    if action == "finish":
        # Check if all questions answered
        if len(answers) == len(order):
            _save_results()
            return redirect(url_for("result"))
        else:
            # Not all answered, stay on current page
            return redirect(url_for("quiz", q_pos=q_pos))
    
    elif action == "prev":
        prev_pos = max(0, q_pos - 1)
        return redirect(url_for("quiz", q_pos=prev_pos))
    
    elif action == "jump":
        target_pos = int(request.form.get("target_pos", q_pos))
        return redirect(url_for("quiz", q_pos=target_pos))
    
    else:  # next
        next_pos = q_pos + 1
        if next_pos >= len(order):
            # Last question, stay here
            return redirect(url_for("quiz", q_pos=q_pos))
        return redirect(url_for("quiz", q_pos=next_pos))


# ---------------------------------------------------------------------------
# Result computation & display
# ---------------------------------------------------------------------------

def _compute_results() -> Dict[str, Any]:
    """Compute detailed result statistics from session data."""
    answers = session.get("answers", {})
    order = session.get("order", [])
    username = session.get("username", "unknown")
    start_time = session.get("start_time", time.time())
    total_time = round(time.time() - start_time, 1)

    details: List[Dict[str, Any]] = []
    correct_count = 0

    # Group stats
    by_category: Dict[str, Dict] = defaultdict(lambda: {"total": 0, "correct": 0})
    by_task: Dict[str, Dict] = defaultdict(lambda: {"total": 0, "correct": 0})
    by_subtask: Dict[str, Dict] = defaultdict(lambda: {"total": 0, "correct": 0})
    by_capability: Dict[str, Dict] = defaultdict(lambda: {"total": 0, "correct": 0})

    for pos, q_idx in enumerate(order):
        question = QUESTIONS[q_idx]
        ans_data = answers.get(str(q_idx), {})
        user_answer = ans_data.get("selected", "")
        correct_answer = question.get("correct_answer", "")
        is_correct = user_answer == correct_answer

        if is_correct:
            correct_count += 1

        cat = question.get("category", "Unknown")
        task = question.get("task", "Unknown")
        sub = question.get("subtask", "Unknown")
        caps = question.get("capabilities", [])

        by_category[cat]["total"] += 1
        by_task[task]["total"] += 1
        by_subtask[sub]["total"] += 1
        if is_correct:
            by_category[cat]["correct"] += 1
            by_task[task]["correct"] += 1
            by_subtask[sub]["correct"] += 1

        for cap in caps:
            by_capability[cap]["total"] += 1
            if is_correct:
                by_capability[cap]["correct"] += 1

        # Get answer explanation
        explanation = question.get("answer", "") or question.get("answer_text", "")

        details.append({
            "question_idx": q_idx,
            "position": pos,
            "question": question.get("question", ""),
            "options": question.get("options", {}),
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "time_spent": ans_data.get("time_spent", 0),
            "category": cat,
            "task": task,
            "subtask": sub,
            "capabilities": caps,
            "explanation": explanation,
            "image_path": question.get("image_path", ""),
            "images": question.get("images", []),
            "option_images": question.get("option_images", []),
            "bev_image": question.get("bev_image", ""),
            "view_image": question.get("view_image", ""),
            "reference_images": question.get("reference_images", []),
        })

    # Add accuracy to grouped stats
    def _add_accuracy(d: Dict[str, Dict]) -> Dict[str, Dict]:
        out = {}
        for k, v in sorted(d.items()):
            v["accuracy"] = round(v["correct"] / v["total"], 3) if v["total"] else 0
            out[k] = v
        return out

    total = len(order)
    return {
        "username": username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_questions": total,
        "correct_count": correct_count,
        "accuracy": round(correct_count / total, 3) if total else 0,
        "total_time_seconds": total_time,
        "by_category": _add_accuracy(by_category),
        "by_task": _add_accuracy(by_task),
        "by_subtask": _add_accuracy(by_subtask),
        "by_capability": _add_accuracy(by_capability),
        "details": details,
    }


def _save_results() -> str:
    """Persist results as a JSON file and return its filename."""
    results = _compute_results()
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{results['username']}_{ts}.json"
    filepath = os.path.join(config.RESULTS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    session["result_file"] = filename
    session.modified = True
    return filename


@app.route("/result")
def result():
    """Display quiz results and statistics."""
    if "username" not in session:
        return redirect(url_for("index"))

    results = _compute_results()
    return render_template("result.html", r=results)


@app.route("/result/download")
def result_download():
    """Download the saved result JSON file."""
    filename = session.get("result_file")
    if not filename:
        abort(404)
    return send_from_directory(config.RESULTS_DIR, filename, as_attachment=True)


# ---------------------------------------------------------------------------
# Admin: list all past results
# ---------------------------------------------------------------------------

@app.route("/admin/results")
def admin_results():
    """List all saved result files with aggregate statistics."""
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    files = sorted(
        [f for f in os.listdir(config.RESULTS_DIR) if f.endswith(".json")],
        reverse=True,
    )
    records = []
    
    # Aggregate statistics across all test takers
    agg_stats = {
        "total_tests": 0,
        "total_questions": 0,
        "total_correct": 0,
        "by_category": defaultdict(lambda: {"correct": 0, "total": 0}),
        "by_task": defaultdict(lambda: {"correct": 0, "total": 0}),
        "by_subtask": defaultdict(lambda: {"correct": 0, "total": 0}),
        "by_capability": defaultdict(lambda: {"correct": 0, "total": 0}),
    }
    
    for fn in files:
        try:
            with open(os.path.join(config.RESULTS_DIR, fn), "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Add to records list
            records.append({
                "filename": fn,
                "username": data.get("username", "?"),
                "timestamp": data.get("timestamp", "?"),
                "accuracy": data.get("accuracy", 0),
                "total": data.get("total_questions", 0),
                "correct": data.get("correct_count", 0),
            })
            
            # Aggregate statistics
            agg_stats["total_tests"] += 1
            agg_stats["total_questions"] += data.get("total_questions", 0)
            agg_stats["total_correct"] += data.get("correct_count", 0)
            
            # Aggregate by category
            for cat, stats in data.get("by_category", {}).items():
                agg_stats["by_category"][cat]["correct"] += stats.get("correct", 0)
                agg_stats["by_category"][cat]["total"] += stats.get("total", 0)
            
            # Aggregate by task
            for task, stats in data.get("by_task", {}).items():
                agg_stats["by_task"][task]["correct"] += stats.get("correct", 0)
                agg_stats["by_task"][task]["total"] += stats.get("total", 0)
            
            # Aggregate by subtask
            for subtask, stats in data.get("by_subtask", {}).items():
                agg_stats["by_subtask"][subtask]["correct"] += stats.get("correct", 0)
                agg_stats["by_subtask"][subtask]["total"] += stats.get("total", 0)
            
            # Aggregate by capability
            for cap, stats in data.get("by_capability", {}).items():
                agg_stats["by_capability"][cap]["correct"] += stats.get("correct", 0)
                agg_stats["by_capability"][cap]["total"] += stats.get("total", 0)
                
        except Exception:
            records.append({"filename": fn, "username": "?", "timestamp": "?", "accuracy": 0, "total": 0, "correct": 0})
    
    # Calculate overall accuracy
    if agg_stats["total_questions"] > 0:
        agg_stats["accuracy"] = agg_stats["total_correct"] / agg_stats["total_questions"]
    else:
        agg_stats["accuracy"] = 0
    
    # Calculate accuracy for each grouping
    for group_key in ["by_category", "by_task", "by_subtask", "by_capability"]:
        for name, stats in agg_stats[group_key].items():
            if stats["total"] > 0:
                stats["accuracy"] = stats["correct"] / stats["total"]
            else:
                stats["accuracy"] = 0
    
    return render_template("admin.html", records=records, agg_stats=agg_stats)


@app.route("/admin/results/<filename>")
def admin_result_detail(filename: str):
    """View a specific past result."""
    filepath = os.path.join(config.RESULTS_DIR, filename)
    if not os.path.exists(filepath):
        abort(404)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return render_template("result.html", r=data)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    print(f"Loaded {len(QUESTIONS)} questions from {config.QUESTION_JSONL}")
    print(f"Images directory: {config.IMAGES_DIR}")
    print(f"Results directory: {config.RESULTS_DIR}")
    app.run(host="0.0.0.0", port=5000, debug=True)

