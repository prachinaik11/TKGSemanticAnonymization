import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Load data from CSV files
# file1 = pd.read_csv('diff_k_l_comparisons/mynew.csv')
# file2 = pd.read_csv('diff_k_l_comparisons/new_with_reset_w_-1.csv')
# file2 = pd.read_csv('diff_k_l_comparisons/new2.csv')

file1 = pd.read_csv('withoutUUrelations/finalResults_wo_UU_relations.csv')
file2 = pd.read_csv('withoutUUrelations/yago15_-1#isCitizenOf_mean_5.csv')

# Function to filter data based on k and l values
# def filter_data(df, k, l):
#     return df[(df['k'] == k) & (df['l'] == l)]
def filter_and_sort_data(df, k, l):
    filtered_df = df[(df['k'] == k) & (df['l'] == l)]
    return filtered_df.sort_values(by='snapshot_id')

# Define k and l values
# k = 10
# l = 4
for k in (2,4,6,8,10):
    for l  in (1,2,3,4):
        if (k in (2,4,6,8) and l==1) or (k==10 and l in (1,2,3,4)):
            # Filter data for k=10 and l=4
            filtered_file1 = filter_and_sort_data(file1, k, l)
            filtered_file2 = filter_and_sort_data(file2, k, l)

            # Plotting
            plt.figure(figsize=(10, 6))
            plt.plot(filtered_file1['snapshot_id'], filtered_file1['AIL'], label='Our AIL values', marker='o')
            plt.plot(filtered_file2['snapshot_id'], filtered_file2['AIL'], label='Their AIL values', marker='o')
            plt.xlabel('Snapshot ID')
            plt.ylabel('AIL')
            plt.title(f'AIL across different snapshots for k={k} and l={l}')
            plt.legend()
            plt.grid(True)
            # Save the plot to a file
            output_file = 'withoutUUrelations/outputs/comparison_diff_'+str(k)+'and'+str(l)+'.png'
            plt.savefig(output_file)
            plt.close()

            print(f"Plot saved to {output_file}")
            # Open the saved image
            img = Image.open(output_file)
            # img.show()
            # plt.show()
