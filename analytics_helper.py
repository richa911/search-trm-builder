import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def create_pie_chart_image(data, title, filename):
    labels = list(data.keys())
    values = list(data.values())

    def absolute_value(val):
        total = sum(values)
        count = int(val / 100.0 * total)
        return f'{count} ({val:.1f}%)'

    colors = ['#FFA500', '#1E90FF']  

    plt.figure(figsize=(4, 4), facecolor='white')

    # Create the pie chart
    wedges, texts, autotexts = plt.pie(
        values,
        labels=labels,
        autopct=absolute_value,
        startangle=140,
        textprops={'fontsize': 11, 'color': 'black'},
        colors=colors[:len(labels)],
        wedgeprops={'edgecolor': 'black', 'linewidth': 1},
        pctdistance=0.85
    )

    # Add donut effect
    center_circle = plt.Circle((0, 0), 0.60, fc='white', edgecolor='black', linewidth=1)
    plt.gca().add_artist(center_circle)

    # Improve text appearance
    for text in texts:
        text.set_fontsize(11)
        text.set_fontweight('bold')

    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_fontweight('bold')

    # Set title
    plt.title(title, fontsize=14, fontweight='bold', pad=10, color='#333333')

    # Equal aspect ratio for a perfect circle
    plt.gca().set_aspect('equal')
    plt.gca().patch.set_facecolor('white')

    # Save with tight bounding box and transparent background for better alignment
    plt.savefig(filename, bbox_inches='tight', dpi=200, transparent=True)
    plt.close()

    return filename

# The data should be in below format
# {
#   "06-07-2024": {
#     'P1': 1,
#     'P2': 3,
#     'P3': 20
#   },
#   "05-07-2024": {
#     'P1': 10,
#     'P2': 5,
#     'P3': 0
#   }
# }
def plot_alerts_per_day(data, title, file_name='priorities_graph.png'):
    # Prepare the plot
    plt.figure(figsize=(10, 6))

    # Initialize a dictionary to hold dates and values for each priority type
    priority_data = {}

    # Process each date and its corresponding priorities
    for date, priorities in data.items():
        date_object = datetime.strptime(date, '%d-%m-%Y')
        for priority, value in priorities.items():
            if priority not in priority_data:
                priority_data[priority] = {'dates': [], 'values': []}
            priority_data[priority]['dates'].append(date_object)
            priority_data[priority]['values'].append(value)

    # Plot each priority type using bar graph
    width = 0.2  # Width of the bars, adjust as needed
    for i, (priority, values) in enumerate(priority_data.items()):
        # Offset each bar for each priority to avoid overlap
        date_offsets = [date + timedelta(days=i * width) for date in values['dates']]
        plt.bar(date_offsets, values['values'], width=width, label=priority, align='center')

    # Formatting the date labels on the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Adjust interval as needed
    # Adding labels, legend, and title
    plt.xlabel('')
    plt.ylabel('Number of alerts')
    plt.title(title)
    plt.legend()
    plt.grid(False)
    # Rotate date labels for better readability
    plt.gcf().autofmt_xdate()
    # Save the plot as a PNG file
    plt.savefig(file_name)
    plt.close()
    return file_name