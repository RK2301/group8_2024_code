import json
import numpy as np
import matplotlib.pyplot as plt

with open(r'results.json', 'r') as re:
    results = json.load(re)

# Step 2: Calculate the averages
#for each model, the average success rate for python and JS
averages = {model: {lang: np.mean(scores) for lang, scores in langs.items()} for model, langs in results.items()}
print(averages)

# Step 3: Prepare the data for plotting
models = list(averages.keys())
python_averages = [averages[model]['python'] for model in models]
javascript_averages = [averages[model]['javascript'] for model in models]

# Step 4: Plotting the bar chart
x = np.arange(len(models))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
bars_python = ax.bar(x - width/2, python_averages, width, label='Python', color='blue')
bars_js = ax.bar(x + width/2, javascript_averages, width, label='JavaScript', color='orange')

# Add labels, title, and ticks
ax.set_xlabel('Models')
ax.set_ylabel('Average Performance')
ax.set_title('Average Performance by GPT Model and Language')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, 100)
ax.legend()

# Display the bar chart
plt.show()