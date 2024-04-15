import base64
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt

from io import BytesIO

def generate_base64_graph(df):
    plt.figure(figsize=(12, 8))
    sns.barplot(x='num_posts', y='main_field', data=df, palette='viridis')
    plt.title('주요분야별 채용공고 수')
    plt.xlabel('채용공고 수')
    plt.ylabel('주요분야')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')  # PNG 형식으로 그래프 저장
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph_string = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    plt.close()

    return graph_string
