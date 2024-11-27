from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load the Excel file (make sure the file is in the same directory as this script)
ACCOUNTING_DATA_PATH = '2023 AFR.xlsm'

# Read the 'Accounting Data' and 'COA' sheets
data = pd.read_excel(ACCOUNTING_DATA_PATH, sheet_name='Accounting Data', engine='openpyxl')
coa = pd.read_excel(ACCOUNTING_DATA_PATH, sheet_name='COA', engine='openpyxl')

# Replace numeric codes with names using COA
columns_to_replace = ['Program', 'Function', 'Object']
for col in columns_to_replace:
    if col in data.columns:
        data = data.merge(coa[['Code', 'Name']], how='left', left_on=col, right_on='Code')
        data[col] = data['Name']
        data.drop(['Code', 'Name'], axis=1, inplace=True)

# API route to provide summarized data
@app.route('/summary', methods=['GET'])
def get_summary():
    # Summarize YTD Transactions by Final Fund
    summary = data.groupby('Final Fund')['YTD Transactions'].sum().reset_index()
    return jsonify(summary.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
