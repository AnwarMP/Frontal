import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

subjects = ['Math42', 'Physics50', 'Physics51', 'CS171', 'CS155', 'CS166', 'CS146', 'CS147']


# Load the adjusted data from the CSV
df = pd.read_csv('synthetic_homework_data.csv')

# Set the aesthetic style of the plots
sns.set_style('whitegrid')

# Create a figure and axes with a size large enough to accommodate 8 subplots
plt.figure(figsize=(20, 20))

# Plotting the data for each subject
for i, subject in enumerate(subjects, 1):
    # Create a subplot for each subject
    plt.subplot(4, 2, i)
    # Filter the DataFrame for the current subject
    subject_df = df[df['Subject'] == subject]
    # Scatter plot of Problem Set size vs Time Required to Finish
    sns.scatterplot(data=subject_df, x='Problem Set', y='Time Required to Finish', hue='Priority', palette='viridis')
    # Title for each subplot
    plt.title(f'Subject: {subject}')
    # Adjust layout for readability
    plt.tight_layout()

# Show the plot
plt.show()