__author__ = "Zhongchuan Sun"
__email__ = "zhongchuansun@gmail.com"

__all__ = ["Pop"]

import numpy as np
import pandas as pd
from typing import Dict
from ..io import Dataset
from ..utils.py import Config
from ..utils.py import RankingEvaluator
from .base import AbstractRecommender


class PopConfig(Config):
    def __init__(self, **kwargs):
        super(PopConfig, self).__init__()


class Pop(AbstractRecommender):
    def __init__(self, dataset: Dataset, cfg_dict: Dict, evaluator: RankingEvaluator):
        config = PopConfig(**cfg_dict)
        super(Pop, self).__init__(dataset, config)
        self.config = config
        self.dataset = dataset
        self.evaluator = evaluator
        self.users_num, self.items_num = self.dataset.num_users, self.dataset.num_items
        self.ranking_score = np.zeros([self.items_num], dtype=np.float32)

    def fit(self):
        self.logger.info("metrics:".ljust(12) + f"\t{self.evaluator.metrics_str}")
        items = self.dataset.train_data.to_user_item_pairs()[:, 1]
        items_count = pd.value_counts(items, sort=False)
        items = items_count.index.values
        count = items_count.values
        self.ranking_score[items] = count

        result = self.evaluate()
        self.logger.info(f"Pop results:".ljust(12) + f"\t{result.values_str}")

    def evaluate(self):
        return self.evaluator.evaluate(self)

    def predict(self, users, neg_items=None):
        ratings = np.tile(self.ranking_score, len(users))
        ratings = np.reshape(ratings, newshape=[len(users), self.items_num])
        return ratings
