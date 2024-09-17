import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


def min_AIL_for_all_snapshots(data):
    # Process data to find minimum AIL for each snapshot_id
    min_ail_data = data.loc[data.groupby('snapshot_id')['AIL'].idxmin()]

    # Create the plot
    plt.figure(figsize=(12, 8))
    colors = ['b', 'g', 'r']
    styles = ['-', '--', '-.']
    snapshot_ids = min_ail_data['snapshot_id'].unique()

    # Extract the snapshot_id and corresponding original_num_of_individuals
    snapshot_info = data[['snapshot_id', 'original_num_of_individuals']].drop_duplicates()

    for i, snapshot_id in enumerate(snapshot_ids):
        subset = min_ail_data[min_ail_data['snapshot_id'] == snapshot_id]
        x = subset['snapshot_id']
        y = subset['AIL']
        k_l = subset.apply(lambda row: f"({row['k']}, {row['l']})", axis=1)

        plt.plot(x, y, color=colors[i % len(colors)], linestyle=styles[i % len(styles)], marker='o',
                 label=f'Snapshot {snapshot_id}')
        for xi, yi, kli in zip(x, y, k_l):
            plt.text(xi, yi, kli, fontsize=9, ha='right')

    plt.xlabel('Snapshot ID (original_num_of_individuals)')
    plt.ylabel('AIL')
    plt.title('Minimum AIL values for each Snapshot ID with corresponding (k, l)')
    plt.legend()
    plt.grid(True)

    # Add the original_num_of_individuals below each snapshot_id on the x-axis
    ax = plt.gca()
    ax.set_xticks(snapshot_ids)
    ax.set_xticklabels([f'{sid}\n({row["original_num_of_individuals"]})'
                        for sid, row in snapshot_info.set_index('snapshot_id').loc[snapshot_ids].iterrows()])

    # Save the plot to a file
    output_file = 'min_AIL_for_all_snapshots.png'
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to {output_file}")
    # Open the saved image
    img = Image.open(output_file)
    img.show()


def AIL_diff_k_values_const_l(data):
    # Filter the data to include only rows where l = 1
    filtered_data = data[data['l'] == 1]

    # Unique values of k
    k_values = filtered_data['k'].unique()

    # Extract the snapshot_id and corresponding original_num_of_individuals
    snapshot_info = data[['snapshot_id', 'original_num_of_individuals']].drop_duplicates()

    # Create the plot
    plt.figure(figsize=(12, 8))
    colors = ['b', 'g', 'r', 'c', 'm']
    styles = ['-', '--', '-.', ':', 'solid']
    snapshot_ids = filtered_data['snapshot_id'].unique()

    for i, k in enumerate(k_values):
        subset = filtered_data[filtered_data['k'] == k]
        x = subset['snapshot_id']
        y = subset['AIL']

        plt.plot(x, y, color=colors[i % len(colors)], linestyle=styles[i % len(styles)], marker='o', label=f'k = {k}')
        # Annotate each point with the num_of_individuals_post_anonymization
        for j in range(len(x)):
            plt.annotate(f"{subset.iloc[j]['num_of_individuals_post_anonymization']}",
                         (x.iloc[j], y.iloc[j]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.xlabel('Snapshot ID (original_num_of_individuals)')
    plt.ylabel('AIL')
    plt.title('AIL values for each Snapshot ID with l = 1 and varying k')
    plt.legend()
    plt.grid(True)

    # Add the original_num_of_individuals below each snapshot_id on the x-axis
    ax = plt.gca()
    ax.set_xticks(snapshot_ids)
    ax.set_xticklabels([f'{sid}\n({row["original_num_of_individuals"]})'
                        for sid, row in snapshot_info.set_index('snapshot_id').loc[snapshot_ids].iterrows()])

    # Save the plot to a file
    output_file = 'AIL_diff_k_values_const_l.png'
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to {output_file}")
    # Open the saved image
    img = Image.open(output_file)
    img.show()

def AAIL_diff_k_values_const_l(data):
    # Filter the data to include only rows where l = 1
    filtered_data = data[data['l'] == 1]

    # Unique values of k
    k_values = filtered_data['k'].unique()

    # Extract the snapshot_id and corresponding original_num_of_individuals
    snapshot_info = data[['snapshot_id', 'original_num_of_individuals']].drop_duplicates()

    # Create the plot
    plt.figure(figsize=(12, 8))
    colors = ['b', 'g', 'r', 'c', 'm']
    styles = ['-', '--', '-.', ':', 'solid']
    snapshot_ids = filtered_data['snapshot_id'].unique()

    for i, k in enumerate(k_values):
        subset = filtered_data[filtered_data['k'] == k]
        x = subset['snapshot_id']
        y = subset['AAIL']

        plt.plot(x, y, color=colors[i % len(colors)], linestyle=styles[i % len(styles)], marker='o', label=f'k = {k}')
        # Annotate each point with the num_of_individuals_post_anonymization
        for j in range(len(x)):
            plt.annotate(f"{subset.iloc[j]['num_of_individuals_post_anonymization']}",
                         (x.iloc[j], y.iloc[j]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.xlabel('Snapshot ID (original_num_of_individuals)')
    plt.ylabel('AAIL')
    plt.title('AAIL values for each Snapshot ID with l = 1 and varying k')
    plt.legend()
    plt.grid(True)

    # Add the original_num_of_individuals below each snapshot_id on the x-axis
    ax = plt.gca()
    ax.set_xticks(snapshot_ids)
    ax.set_xticklabels([f'{sid}\n({row["original_num_of_individuals"]})'
                        for sid, row in snapshot_info.set_index('snapshot_id').loc[snapshot_ids].iterrows()])

    # Save the plot to a file
    output_file = 'AAIL_diff_k_values_const_l.png'
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to {output_file}")
    # Open the saved image
    img = Image.open(output_file)
    img.show()

def AIL_diff_l_values_const_k(data):
    # Filter the data to include only rows where k = 6
    filtered_data = data[data['k'] == 6]

    # Unique values of l
    l_values = filtered_data['l'].unique()

    # Extract the snapshot_id and corresponding original_num_of_individuals
    snapshot_info = data[['snapshot_id', 'original_num_of_individuals']].drop_duplicates()

    # Create the plot
    plt.figure(figsize=(12, 8))
    colors = ['b', 'g', 'r', 'c', 'm']
    styles = ['-', '--', '-.', ':', 'solid']
    snapshot_ids = filtered_data['snapshot_id'].unique()

    for i, l in enumerate(l_values):
        subset = filtered_data[filtered_data['l'] == l]
        x = subset['snapshot_id']
        y = subset['AIL']

        plt.plot(x, y, color=colors[i % len(colors)], linestyle=styles[i % len(styles)], marker='o', label=f'l = {l}')
        # Annotate each point with the num_of_individuals_post_anonymization
        for j in range(len(x)):
            plt.annotate(f"{subset.iloc[j]['num_of_individuals_post_anonymization']}",
                         (x.iloc[j], y.iloc[j]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.xlabel('Snapshot ID (original_num_of_individuals)')
    plt.ylabel('AIL')
    plt.title('AIL values for each Snapshot ID with k = 6 and varying l')
    plt.legend()
    plt.grid(True)

    # Add the original_num_of_individuals below each snapshot_id on the x-axis
    ax = plt.gca()
    ax.set_xticks(snapshot_ids)
    ax.set_xticklabels([f'{sid}\n({row["original_num_of_individuals"]})'
                        for sid, row in snapshot_info.set_index('snapshot_id').loc[snapshot_ids].iterrows()])

    # Save the plot to a file
    output_file = 'AIL_diff_l_values_const_k.png'
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to {output_file}")
    # Open the saved image
    img = Image.open(output_file)
    img.show()

def AAIL_diff_l_values_const_k(data):
    # Filter the data to include only rows where k = 6
    filtered_data = data[data['k'] == 6]

    # Unique values of l
    l_values = filtered_data['l'].unique()

    # Extract the snapshot_id and corresponding original_num_of_individuals
    snapshot_info = data[['snapshot_id', 'original_num_of_individuals']].drop_duplicates()

    # Create the plot
    plt.figure(figsize=(12, 8))
    colors = ['b', 'g', 'r', 'c', 'm']
    styles = ['-', '--', '-.', ':', 'solid']
    snapshot_ids = filtered_data['snapshot_id'].unique()

    for i, l in enumerate(l_values):
        subset = filtered_data[filtered_data['l'] == l]
        x = subset['snapshot_id']
        y = subset['AAIL']

        plt.plot(x, y, color=colors[i % len(colors)], linestyle=styles[i % len(styles)], marker='o', label=f'l = {l}')
        # Annotate each point with the num_of_individuals_post_anonymization
        for j in range(len(x)):
            plt.annotate(f"{subset.iloc[j]['num_of_individuals_post_anonymization']}",
                         (x.iloc[j], y.iloc[j]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.xlabel('Snapshot ID (original_num_of_individuals)')
    plt.ylabel('AAIL')
    plt.title('AAIL values for each Snapshot ID with k = 6 and varying l')
    plt.legend()
    plt.grid(True)

    # Add the original_num_of_individuals below each snapshot_id on the x-axis
    ax = plt.gca()
    ax.set_xticks(snapshot_ids)
    ax.set_xticklabels([f'{sid}\n({row["original_num_of_individuals"]})'
                        for sid, row in snapshot_info.set_index('snapshot_id').loc[snapshot_ids].iterrows()])

    # Save the plot to a file
    output_file = 'AAIL_diff_l_values_const_k.png'
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to {output_file}")
    # Open the saved image
    img = Image.open(output_file)
    img.show()


def min_AIL_per_snapshot(data):
    # Group by snapshot_id and find the row with the minimum AIL value for each group
    min_ail_per_snapshot = data.loc[data.groupby('snapshot_id')['AIL'].idxmin()]

    # Select relevant columns: snapshot_id, k, l, and AIL
    min_ail_per_snapshot = min_ail_per_snapshot[['snapshot_id', 'k', 'l', 'AIL']].reset_index(drop=True)

    # Print the results
    print(min_ail_per_snapshot)
    output_file = 'min_ail_per_snapshot.csv'
    min_ail_per_snapshot.to_csv(output_file, index=False)

    # Plotting the data
    plt.figure(figsize=(12, 8))  # Set the figure size (width, height) in inches
    plt.plot(min_ail_per_snapshot['snapshot_id'], min_ail_per_snapshot['AIL'], marker='o')
    plt.title('Minimum AIL per Snapshot ID')
    plt.xlabel('Snapshot ID')
    plt.ylabel('Minimum AIL')
    plt.grid(True)  # Adding a grid for better readability

    # Setting x-axis ticks
    plt.xticks(range(min(min_ail_per_snapshot['snapshot_id']), max(min_ail_per_snapshot['snapshot_id']) + 1))

    # plt.show()
    # Save the plot to a file
    output_file = 'min_AIL_per_snapshot.png'
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to {output_file}")
    # Open the saved image
    img = Image.open(output_file)
    img.show()

def min_AIL_per_snapshot_comparison(data_1, data_2):
    # Group by snapshot_id and find the row with the minimum AIL value for each group in the first file
    min_ail_per_snapshot_1 = data_1.loc[data_1.groupby('snapshot_id')['AIL'].idxmin()]
    min_ail_per_snapshot_1 = min_ail_per_snapshot_1[['snapshot_id', 'k', 'l', 'AIL']].reset_index(drop=True)

    # Group by snapshot_id and find the row with the minimum AIL value for each group in the second file
    min_ail_per_snapshot_2 = data_2.loc[data_2.groupby('snapshot_id')['AIL'].idxmin()]
    min_ail_per_snapshot_2 = min_ail_per_snapshot_2[['snapshot_id', 'k', 'l', 'AIL']].reset_index(drop=True)

    # Plotting the data
    plt.figure(figsize=(10, 5))  # Set the figure size (width, height) in inches

    # Plot for the first file
    plt.plot(min_ail_per_snapshot_1['snapshot_id'], min_ail_per_snapshot_1['AIL'], marker='o', label='Our Approach')

    # Annotate points with k and l values for the first file
    for i, row in min_ail_per_snapshot_1.iterrows():
        plt.annotate(f"{int(row['k'])}, {int(row['l'])}",
                     (row['snapshot_id'], row['AIL']),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center')

    # Plot for the second file
    plt.plot(min_ail_per_snapshot_2['snapshot_id'], min_ail_per_snapshot_2['AIL'], marker='x', label='Their Approach')
    # Annotate points with k and l values for the second file
    for i, row in min_ail_per_snapshot_2.iterrows():
        plt.annotate(f"{int(row['k'])}, {int(row['l'])}",
                     (row['snapshot_id'], row['AIL']),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center')

    # Add titles and labels
    plt.title('Minimum AIL per Snapshot ID')
    plt.xlabel('Snapshot ID')
    plt.ylabel('Minimum AIL')
    plt.grid(True)  # Adding a grid for better readability
    # Setting x-axis ticks
    plt.xticks(range(0, 10))  # Adjust this range based on your actual data if needed

    # Add a legend
    plt.legend()

    # Show the plot
    # plt.show()

    # plt.show()
    # Save the plot to a file
    output_file = 'min_AIL_per_snapshot_comparison.png'
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to {output_file}")
    # Open the saved image
    img = Image.open(output_file)
    img.show()


def min_AAIL_per_snapshot_comparison(data_1, data_2):
    # Group by snapshot_id and find the row with the minimum AIL value for each group in the first file
    min_aail_per_snapshot_1 = data_1.loc[data_1.groupby('snapshot_id')['AAIL'].idxmin()]
    min_aail_per_snapshot_1 = min_aail_per_snapshot_1[['snapshot_id', 'k', 'l', 'AAIL']].reset_index(drop=True)

    # Group by snapshot_id and find the row with the minimum AIL value for each group in the second file
    min_aail_per_snapshot_2 = data_2.loc[data_2.groupby('snapshot_id')['AAIL'].idxmin()]
    min_aail_per_snapshot_2 = min_aail_per_snapshot_2[['snapshot_id', 'k', 'l', 'AAIL']].reset_index(drop=True)

    # Plotting the data
    plt.figure(figsize=(10, 5))  # Set the figure size (width, height) in inches

    # Plot for the first file
    plt.plot(min_aail_per_snapshot_1['snapshot_id'], min_aail_per_snapshot_1['AAIL'], marker='o', label='Our Approach')

    # Annotate points with k and l values for the first file
    for i, row in min_aail_per_snapshot_1.iterrows():
        plt.annotate(f"{int(row['k'])}, {int(row['l'])}",
                     (row['snapshot_id'], row['AAIL']),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center')

    # Plot for the second file
    plt.plot(min_aail_per_snapshot_2['snapshot_id'], min_aail_per_snapshot_2['AAIL'], marker='x', label='Their Approach')
    # Annotate points with k and l values for the second file
    for i, row in min_aail_per_snapshot_2.iterrows():
        plt.annotate(f"{int(row['k'])}, {int(row['l'])}",
                     (row['snapshot_id'], row['AAIL']),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center')

    # Add titles and labels
    plt.title('Minimum AAIL per Snapshot ID')
    plt.xlabel('Snapshot ID')
    plt.ylabel('Minimum AAIL')
    plt.grid(True)  # Adding a grid for better readability
    # Setting x-axis ticks
    plt.xticks(range(0, 10))  # Adjust this range based on your actual data if needed

    # Add a legend
    plt.legend()

    # Show the plot
    # plt.show()

    # plt.show()
    # Save the plot to a file
    output_file = 'min_AAIL_per_snapshot_comparison.png'
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to {output_file}")
    # Open the saved image
    img = Image.open(output_file)
    img.show()


# Load the data from the CSV file
# file_path = 'extracted_values.csv'
# file_path_to_be_campared_with = 'existingResults.csv'
anony_path = "/home/prachi/PycharmProjects/Anonymization/Freebase/"
file_path = anony_path + 'freebase_extracted_values.csv'
file_path_to_be_campared_with = anony_path + 'freebase_their_values.csv'
data = pd.read_csv(file_path)
data_2 = pd.read_csv(file_path_to_be_campared_with)
min_AIL_for_all_snapshots(data)
# AIL_diff_k_values_const_l(data)
# AAIL_diff_k_values_const_l(data)
# AIL_diff_l_values_const_k(data)
# AAIL_diff_l_values_const_k(data)
# min_AIL_per_snapshot(data)
# min_AIL_per_snapshot_comparison(data, data_2)
# min_AAIL_per_snapshot_comparison(data, data_2)

