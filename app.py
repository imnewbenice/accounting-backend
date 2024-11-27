from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load data once when the app starts
ACCOUNTING_DATA_PATH = 'AccountingData.xlsx'

# Load sheets
data = pd.read_excel(ACCOUNTING_DATA_PATH, sheet_name='Accounting Data', usecols='A:M')
coa = pd.read_excel(ACCOUNTING_DATA_PATH, sheet_name='COA')

# Columns to replace codes with names
columns_to_replace = ['Program', 'Function', 'Object']

# Replace numeric codes with names
for col in columns_to_replace:
    if col in data.columns:
        data = data.merge(coa[['Code', 'Name']], how='left', left_on=col, right_on='Code')
        data[col] = data['Name']
        data.drop(['Code', 'Name'], axis=1, inplace=True)


@app.route('/summary', methods=['GET'])
def get_summary():
    # Summarize data
    summary = data.groupby('Final Fund')['YTD Transactions'].sum().reset_index()
    return jsonify(summary.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
