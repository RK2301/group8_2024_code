import json
import numpy as np
import matplotlib.pyplot as plt

# Calculate the averages for JavaScript only


with open(r'results.json', 'r') as re:
    results = json.load(re)

# Step 2: Calculate the averages for JavaScript only
averages_js = {model: np.mean(langs['javascript']) for model, langs in results.items()}

# Step 3: Prepare the data for plotting
models = list(averages_js.keys())
javascript_averages = list(averages_js.values())

# Step 4: Plotting the bar chart for JavaScript only
x = np.arange(len(models))  # the label locations
width = 0.5  # the width of the bars

fig, ax = plt.subplots()
bars_js = ax.bar(x, javascript_averages, width, label='JavaScript', color='orange')

# Add labels, title, and ticks
ax.set_xlabel('Models')
ax.set_ylabel('Average Performance in JavaScript')
ax.set_title('Average JavaScript Performance by GPT Model')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, 100)
ax.legend()

# Display the bar chart
plt.show()