"""
Script to convert predictions from the algorithm output format
to the common output format.
"""

import argparse
import pandas as pd
import ast
from base import OutputMapperBase


class OutputMapper(OutputMapperBase):
    REPLACEMENTS = [
        ("C(Carbamidomethylation)", "C[UNIMOD:4]"),
        ("M(Oxidation)", "M[UNIMOD:35]"),
        ("N(Deamidation)", "N[UNIMOD:7]"),
        ("Q(Deamidation)", "Q[UNIMOD:7]"),
    ]

    def format_sequence(self, sequence):
        sequence = str(sequence).replace(",", "")

        for repl_args in self.REPLACEMENTS:
            sequence = sequence.replace(*repl_args)

        return sequence


# 设置命令行参数
parser = argparse.ArgumentParser()
parser.add_argument("--output_path", help="The path to the algorithm predictions file.")
args = parser.parse_args()

# 读取算法输出的特征文件
output_data = pd.read_csv(args.output_path, sep="\t")
# print(output_data.dtypes)
# 实例化OutputMapper并进行格式转换
output_mapper = OutputMapper()
output_data = output_data[(output_data != output_data.columns).all(axis=1)]
output_data = output_data.rename(
    {
        "predicted_sequence": "sequence",
        "predicted_score": "score",
        "feature_id": "spectrum_id",
        "predicted_position_score": "aa_scores",
    },
    axis=1,
)
output_data = output_mapper.format_output(output_data)

# 将处理后的数据保存为outputs.csv
output_data.to_csv("outputs.csv", index=False)
