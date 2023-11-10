import pandas as pd
import numpy as np

# Define the subjects and the number of subjects
subjects = ['Math42', 'Physics50', 'Physics51', 'CS171', 'CS155', 'CS166', 'CS146', 'CS147']
num_subjects = len(subjects)

# Define the number of data points
num_data_points = 2000

# Create the problem set sizes with a normal distribution around the mean
# with the specified minimum and maximum
min_problems, max_problems = 5, 100
mean_problems = (min_problems + max_problems) / 2
std_dev_problems = (max_problems - mean_problems) / 3  # Assuming 99.7% of data within [min, max]

# Create a dictionary to hold the data
data = {'Subject': [], 'Problem Set': [], 'Priority': [], 'Time Required to Finish': []}

# Priorities
priorities = ['High', 'Medium', 'Low']

# The polynomial coefficients for the time required
# The harder the subject, the higher the coefficient
coefficients = {
    'Math42': np.random.uniform(0.001, 0.0005, 4),  # lower coefficients for easier subjects
    'Physics50': np.random.uniform(0.0003, 0.0007, 4),
    'Physics51': np.random.uniform(0.003, 0.0007, 4),
    'CS171': np.random.uniform(0.005, .0010, 4),
    'CS155': np.random.uniform(0.05, .0030, 4),
    'CS166': np.random.uniform(0.07, 0.002, 4),
    'CS146': np.random.uniform(0.07, 0.002, 4),
    'CS147': np.random.uniform(0.09, 0.003, 4)  # higher coefficients for harder subjects
}

# Maximum time allowed for a homework
max_time = 7 * 60 # 7 hours in minutes

# Generate the synthetic data
for subject in subjects:
    # Number of tasks per subject, approximately equal
    tasks_per_subject = num_data_points // num_subjects
    
    for _ in range(tasks_per_subject):
        # Generate a normally distributed problem set size
        problem_set = int(np.clip(np.random.normal(mean_problems, std_dev_problems), min_problems, max_problems))
        
        # Select a random priority
        priority = np.random.choice(priorities)
        
        # Calculate the time required using a polynomial function of the problem set size
        # plus some random noise
        time_required = np.polyval(coefficients[subject], problem_set)
        time_required = int(np.clip(time_required + np.random.normal(0, 10), 0, max_time))
        
        # Append the generated data to the dictionary
        data['Subject'].append(subject)
        data['Problem Set'].append(problem_set)
        data['Priority'].append(priority)
        data['Time Required to Finish'].append(time_required)

# Create the DataFrame
df = pd.DataFrame(data)

# Since we used floor division, there might be some subjects with less data points
# Adding extra rows to balance it out
while len(df) < num_data_points:
    for subject in subjects:
        if len(df) >= num_data_points:
            break
        problem_set = int(np.clip(np.random.normal(mean_problems, std_dev_problems), min_problems, max_problems))
        priority = np.random.choice(priorities)
        time_required = np.polyval(coefficients[subject], problem_set)
        time_required = int(np.clip(time_required + np.random.normal(0, 10), 0, max_time))/100000
        extra_data = {'Subject': subject, 'Problem Set': problem_set, 'Priority': priority, 'Time Required to Finish': time_required}
        df = df.append(extra_data, ignore_index=True)

# Save the DataFrame to a CSV file
csv_file = 'synthetic_homework_data.csv'
df.to_csv(csv_file, index=False)

csv_file
