import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

import cmap


def second_task(combination_method='sum'):
    # read results.csv
    df = pd.read_csv('results.csv')

    # show per min confidence a grouped bar plot of
    # rank methods: avg confidence, popularity, product, interest, all_confidence
    # filter the dataframe
    # is_ndi: False
    filtered_df = df[df['is_ndi'] == 0]
    # score type: ARHR
    filtered_df = filtered_df[filtered_df['score_type'] == 'ARHR']
    # combination method: sum
    filtered_df = filtered_df[filtered_df['combination_method'] == combination_method]

    # rename the rank methods
    filtered_df['rank_method'] = filtered_df['rank_method'].replace(
        {'avg_confidence': 'Avg. Confidence', 'popularity': 'Popularity',
         'product': 'Product', 'interest': 'Interest',
         'all_confidence': 'All-Confidence', 'regular': 'Confidence'})

    # construct the grouped bar plot
    sns.barplot(filtered_df, x='min_confidence', y='score', hue='rank_method',
                palette=cmap.okabe_tl)
    # rename the x-axis and y-axis
    plt.xlabel('Minimum Confidence')
    plt.ylabel('ARHR')

    # put the legend on top and don't show a box
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3,
               fancybox=True, shadow=False)

    # make the plot bigger
    plt.gcf().set_size_inches(10, 6)

    # show the grouped barplot
    plt.savefig(f'{combination_method}.png')
    # plt.show()


def third_task():
    # read results.csv
    df = pd.read_csv('results.csv')

    # show per min confidence a grouped bar plot of
    # rank methods: avg confidence, popularity, product, interest, all_confidence
    # filter the dataframe
    # is_ndi: False
    filtered_df = df[df['is_ndi'] == 1]
    # score type: ARHR
    filtered_df = filtered_df[filtered_df['score_type'] == 'ARHR']
    # combination method: sum
    filtered_df = filtered_df[filtered_df['combination_method'] == 'max']

    # rename the rank methods
    filtered_df['rank_method'] = filtered_df['rank_method'].replace(
        {'avg_confidence': 'Avg. Confidence', 'popularity': 'Popularity',
         'product': 'Product', 'interest': 'Interest',
         'all_confidence': 'All-Confidence', 'regular': 'Confidence'})

    # construct the grouped bar plot
    sns.barplot(filtered_df, x='min_support', y='score', hue='rank_method',
                palette=cmap.okabe_tl)
    # rename the x-axis and y-axis
    plt.xlabel('NDI Support')
    plt.ylabel('ARHR')

    # put the legend on top and don't show a box
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3,
               fancybox=True, shadow=False)

    # make the plot bigger
    plt.gcf().set_size_inches(10, 6)

    # show the grouped barplot
    plt.savefig(f'ndi.png')


if __name__ == '__main__':
    # second_task('sum')
    # second_task('max')
    third_task()
