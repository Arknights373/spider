from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
semantic_cls = pipeline(Tasks.text_classification, 'iic/nlp_structbert_sentiment-classification_chinese-base')

semantic_cls(input='这家餐厅很好吃')