import csv

file_name = "20230208225135_book_comment.csv"
with open(file_name, encoding='utf-8') as f:
    c_csv = list(csv.reader(f))

row = c_csv[1]
comment_content = row[6]


from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

semantic_cls = pipeline(Tasks.text_classification, 'iic/nlp_structbert_sentiment-classification_chinese-base')

result = semantic_cls(input = comment_content)

sorted_labels_scores = sorted(zip(result['labels'], result['scores']), key=lambda x: x[0] == '正面', reverse=True)

positive_label, positive_probs = sorted_labels_scores[0]
negative_label, negative_probs = sorted_labels_scores[1]
is_positive = 1 if positive_probs >= negative_probs else 0

import time
import os

now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
key_list = ["is_positive", "positive_probs", "negative_probs"]
analysis_path = os.getcwd() + now_time + "comment_emotion.csv"
with open(analysis_path, 'w+', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=key_list)
    writer.writeheader()
    value = {"is_positive": is_positive, "positive_probs": format(positive_probs, '.4f'), "negative_probs": format(negative_probs, '.4f')}
    writer.writerow(value)