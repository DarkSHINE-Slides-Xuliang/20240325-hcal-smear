#!/usr/bin/env python3
import glob, os


# Function to extract the number from the filename
def extract_number(filename):
    basename = os.path.basename(filename)  # Get the base name of the file
    # number = ''.join(filter(str.isdigit, basename))  # Extract digits
    number = basename.split('_')[0]
    return int(number) if number else 0  # Convert to integer


def gen_index_html(outdir: str, file_list):
    template = r"""
<!DOCTYPE html>
<html>
<head>
    <title>Dark SHINE Analysis</title>
    <!-- Include the Plotly.js CDN -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js"></script>
    <style>
        .container {
            display: flex;
            flex-direction: row;
            align-items: center;
            margin-bottom: 20px;
            flex-shrink: 0;
        }
        .plot {
            margin-right: 10px;
        }
        .description {
            font-size: 22px;
            flex-grow: 1;
            padding: 10px;
            width: 70%;
            text-align: left;
            display: flex;
        }
        @media (max-width: 1200px) {
            .container {
                flex-direction: column;
            }
            .description {
                text-align: center;
                border-bottom: 1px solid #ccc; /* Add a border bottom line */
                margin-bottom: 20px; /* Optional: Add some margin to the bottom */
            }
        }
    </style>
</head>
<body>

<h1>Dark SHINE Analysis</h1>
<!-- Placeholder for Plotly Charts -->
<div id="plotly-charts"></div>

<script>
    // List of your JSON file names
    var jsonFiles = __files__;
    fetch('plots.yaml')
        .then(response => response.text())
        .then(yamlText => {
            const plotDescriptions = jsyaml.load(yamlText).plots;
            const plotlyContainer = document.getElementById('plotly-charts');

            jsonFiles.forEach((file, index) => {
                const container = document.createElement('div');
                container.className = 'container';

                // Create a div for each plot
                var plotDiv = document.createElement('div');
                plotDiv.className = 'plot'
                plotDiv.innerHTML = '<h2>Loading...</h2>';
                container.appendChild(plotDiv);

                const description = document.createElement('div');
                description.className = 'description';
                description.innerHTML = '<span><a href="plot/json/' + file + '" target="_blank"><strong>Figure ' + (index + 1) + '.</strong></a> ' + (plotDescriptions[file] || '') + '</span>';
                container.appendChild(description);

                plotlyContainer.appendChild(container);

                // Fetch the JSON data and create a plot
                fetch('plot/json/' + file)
                    .then(response => response.json())
                    .then(data => {
                        // Remove the "Loading..." message
                        plotDiv.innerHTML = '';
                        Plotly.newPlot(plotDiv, data.data, data.layout);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        // Update message in case of error
                        plotDiv.innerHTML = '<p>Error loading the plot</p>';
                    });
            });
        })

</script>

</body>
</html>
"""
   
    # Get the file list sorted by the number in the filename
    # file_list = sorted(glob.glob(f"{outdir}/plot/json/*.json"), key=extract_number)
    # template = template.replace('__files__', str([os.path.basename(f) for f in file_list]))
    template = template.replace('__files__', str(file_list))
    # Write the file out again
    with open(f'{outdir}/index.html', 'w') as file:
        file.write(template)
