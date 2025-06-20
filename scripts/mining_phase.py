import pandas as pd
import sys


def main(input_file, output_file):
    # Load the deduplicated input file (CSV or Excel)
    if input_file.lower().endswith(('.xlsx', '.xls')):
        df = pd.read_excel(input_file)
    else:
        df = pd.read_csv(input_file)

    # Remove duplicates based on DOI/PubMed ID or Title if available
    if 'DOI/PubMed ID' in df.columns:
        df = df.drop_duplicates(subset=['DOI/PubMed ID'])
    elif 'Title' in df.columns:
        df = df.drop_duplicates(subset=['Title'])

    # Generate Study ID column (M001, M002, ...)
    df.insert(0, 'Study ID', ['M%03d' % (i + 1) for i in range(len(df))])

    # Ensure all expected columns exist
    expected_cols = [
        'Study ID',
        'Title',
        'DOI/PubMed ID',
        'Year of publication',
        'Clinical vs Preclinical',
        'Study Type',
        'Review Focus Area',
        'Intervention Type',
        'Outcome Reported?'
    ]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ''

    # Reorder columns according to the template
    df = df[expected_cols]

    # Save the mining phase sheet
    df.to_excel(output_file, index=False)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python mining_phase.py <input_file> <output_file>')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
