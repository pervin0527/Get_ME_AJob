import matplotlib
matplotlib.use('Agg')

import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def draw_main_graph(names, counts, filepath):
    plt.figure(figsize=(12, 8))
    sns.barplot(x=names, y=counts, palette='viridis')
    plt.title('주요분야별 채용공고 수')
    plt.xlabel('채용공고 수')
    plt.ylabel('주요분야')
    plt.savefig(filepath)  # 파라미터로 받은 경로에 저장
    plt.close()


def draw_sub_graph(fields, counts, keyword):
    plt.figure(figsize=(12, 8))
    sns.barplot(x=list(fields), y=list(counts), palette='viridis')
    plt.title(f'Top 10 Related Fields for {keyword}')
    plt.ylabel('Counts')
    plt.xticks(rotation=45)
    # plt.show()
    plt.savefig(f'static/Relation_{keyword}.png')
    plt.close()