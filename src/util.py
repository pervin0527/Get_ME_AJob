import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def draw_main_graph(field_counts):
    plt.figure(figsize=(12, 8))
    sns.barplot(x=field_counts.values, y=field_counts.index, palette='viridis')
    plt.title('주요분야별 채용공고 수')
    plt.xlabel('채용공고 수')
    plt.ylabel('주요분야')
    # plt.show()
    plt.savefig('outputs/Main.png')


def draw_sub_graph(counter, keyword):
    top_related_fields = counter.most_common(10)
    if top_related_fields:
        related_fields, related_counts = zip(*top_related_fields)
        plt.figure(figsize=(12, 8))
        sns.barplot(x=list(related_fields), y=list(related_counts), palette='viridis')
        plt.title(f'Top 10 Related Fields for {keyword}')
        plt.ylabel('Counts')
        plt.xticks(rotation=45)
        # plt.show()
        plt.savefig(f'outputs/Relation_{keyword}.png')

    else:
        print("No data to display.")