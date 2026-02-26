'''
Author: Zhengyan Huang, WANG Maonan
Date: 2026-02-26 15:15:29
Description: Configuration for OmniTraffic VQA Web Test
LastEditTime: 2026-02-26 15:40:13
'''
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the sampled question JSONL file
QA_SAMPLING_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
QUESTION_JSONL = os.path.join(QA_SAMPLING_DIR, "question_sample.jsonl")
IMAGES_DIR = os.path.join(QA_SAMPLING_DIR, "images")

# Directory where user result JSONs are saved
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# Flask secret key for session
SECRET_KEY = "omnitraffic-vqa-web-test-secret-2026"

# Whether to shuffle question order per user session
SHUFFLE_QUESTIONS = False

