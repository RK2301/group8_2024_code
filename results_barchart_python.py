import json
import numpy as np
import matplotlib.pyplot as plt

with open(r'results.json', 'r') as re:
    results = json.load(re)

# Step 2: Calculate the averages for Python only
averages_python = {model: np.mean(langs['python']) for model, langs in results.items()}

# Step 3: Prepare the data for plotting
models = list(averages_python.keys())
python_averages = list(averages_python.values())

# Step 4: Plotting the bar chart for Python only
x = np.arange(len(models))  # the label locations
width = 0.5  # the width of the bars

fig, ax = plt.subplots()
bars_python = ax.bar(x, python_averages, width, label='Python', color='blue')

# Add labels, title, and ticks
ax.set_xlabel('Models')
ax.set_ylabel('Average Performance in Python')
ax.set_title('Average Python Performance by GPT Model')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, 100)
ax.legend()

# Display the bar chart
plt.show()