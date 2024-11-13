import pandas as pd
import os

def main():
    # Load data from CSV
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data_after_sdv.csv"), keep_default_na=False)

    # Group by 'bus_num', 'start', and 'end' to obtain counts
    counts = data.groupby(['bus_num', 'start', 'end']).size().reset_index(name='count')

    # Total count per bus_num and start
    totals = counts.groupby(['bus_num', 'start'])['count'].transform('sum')

    # Probability by dividing the count of each end by the total for each (bus_num, start)
    counts['probability'] = counts['count'] / totals

    # Save HTML output
    output_file = os.path.join(os.path.dirname(__file__), "../visualisations/od_probability_matrices.html")

    # Open the file to write HTML content
    with open(output_file, "w") as file:
        # Styles
        file.write("<html><head><title>Origin-Destination Probability Matrices</title>")
        file.write("""
        <style>
            table {
                width: 100%;
                border-collapse: collapse; /* Merge borders */
            }
            th, td {
                border: 1px solid black; /* Add border to table cells */
                padding: 8px; /* Add padding for better spacing */
                text-align: center; /* Center-align text */
            }
            th {
                background-color: #f2f2f2; /* Light gray background for header */
            }
            .grey-cell {
                background-color: #f2f2f2; /* Light gray background for zero values */
            }
        </style>
        """)
        file.write("</head><body>\n")
        
        for bus in counts['bus_num'].unique():
            bus_df = counts[counts['bus_num'] == bus]
            od_matrix = bus_df.pivot(index='start', columns='end', values='probability').fillna(0)
            
            # Title for each bus service
            file.write(f"<h2>Origin-Destination Probability Matrix for Bus {bus}:</h2>\n")
            
            html_table = '<table>'
            
            # Header for 'start' stop
            html_table += '<tr>'
            html_table += '<th rowspan="2">Start</th>'  # Combined header cell
            
            # Header for 'end' stop
            html_table += '<th colspan="{}">End</th>'.format(len(od_matrix.columns))
            html_table += '</tr>'
            
            # Add the row for the end columns
            html_table += '<tr>'
            html_table += '<th>' + '</th><th>'.join(od_matrix.columns) + '</th>'  # Sub-header for end locations
            html_table += '</tr>'
            
            # Fill up table with values
            for index, row in od_matrix.iterrows():
                html_table += '<tr><td>{}</td>'.format(index) + ''.join(
                    f'<td class="grey-cell">' if value == 0 else f'<td>' + f'{value:.2f}' + '</td>' for value in row
                ) + '</tr>'
            
            html_table += '</table>'
            
            file.write(html_table)
            file.write("<br>\n")  # Add spaces between each table

        # Close HTML structure
        file.write("</body></html>\n")

    print(f"HTML tables saved to {output_file}")


if __name__ == "__main__":
    main()