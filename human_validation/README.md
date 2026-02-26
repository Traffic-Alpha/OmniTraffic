# OmniTraffic Human Validation

This is the **human validation** component of [OmniTraffic](https://github.com/your-repo/OmniTraffic), a comprehensive benchmark for traffic scene visual question answering. We have carefully selected **100 questions** from the dataset, covering both **synthetic (simulation)** and **real-world** environments, to evaluate human performance on traffic scene understanding tasks.

![Quiz Interface](./docs/images/quiz_interface.png)
*Quiz interface preview*

## Quick Start

### 1. Download Data

Download the image data from the GitHub Release and extract to the `data/images/` directory:

```bash
# Download from GitHub Release
# https://github.com/your-repo/OmniTraffic/releases

# Extract the data to data/images/
unzip human_validation_data.zip -d OmniTraffic/human_validation/data/
```

After extraction, verify the directory structure:

```
data/images/
├── qa_dataset/           # Synthetic (simulation) images
│   ├── Beijing_Beihuan/
│   ├── Beijing_Beishahe/
│   ├── Beijing_Changjianglu/
│   ├── Chengdu_Chenghannanlu/
│   ├── Chengdu_Guanghua/
│   ├── France_Massy_perturbation_crashed/
│   ├── SouthKorea_Songdo_perturbation_crashed/
│   └── ...
└── qa_dataset_real/     # Real-world images
```

### 2. Start the Web Service

```bash
cd OmniTraffic/human_validation/web_app
uv run python app.py
```

The web application will start at `http://localhost:5000`.

### 3. Take the Test

1. Open `http://localhost:5000` in your browser
2. Enter your username to begin
3. Answer all 100 questions by selecting A/B/C/D options
4. View your score and detailed results after submission

### 4. Review Answers

After completing the test, you can:
- View your score and accuracy
- Check each question with the correct answer
- Download your results as JSON

![Results Page](./docs/images/results_page.png)
*Results page preview*

## File Structure

```
human_validation/
├── web_app/
│   ├── app.py            # Flask application
│   ├── config.py         # Configuration
│   ├── static/           # Static assets
│   ├── templates/        # HTML templates
│   └── results/          # Test results (JSON files)
├── data/
│   ├── images/           # Traffic scene images
│   │   ├── qa_dataset/       # Synthetic images
│   │   └── qa_dataset_real/  # Real-world images
│   └── question_sample.jsonl  # 100 selected questions
├── README.md
└── README_zh.md
```

### Test Results

All test results are saved in `web_app/results/` as JSON files with the naming format:
```
{username}_{timestamp}.json
```

Each result file contains:
- Username and timestamp
- Total questions and correct count
- Accuracy by category, task, and capability
- Detailed answer for each question

---

[中文版](README_zh.md)
