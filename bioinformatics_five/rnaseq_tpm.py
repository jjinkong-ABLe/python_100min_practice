"""Length-normalize bulk RNA-seq abundance tables to per-sample TPM."""
import argparse
import csv
import math
import sys


def tpm(counts, lengths):
    if len(counts) != len(lengths) or not counts:
        raise ValueError('counts and lengths must have equal nonzero length')
    if any(not math.isfinite(x) or x < 0 for x in counts):
        raise ValueError('counts must be finite and nonnegative')
    if any(not math.isfinite(x) or x <= 0 for x in lengths):
        raise ValueError('lengths must be finite and positive')
    # Scaling by the largest rate before summing avoids large-denominator overflow.
    rates = [count / length for count, length in zip(counts, lengths)]
    if any(not math.isfinite(x) for x in rates):
        raise ValueError('count/length exceeds numeric range')
    peak = max(rates)
    if peak == 0:
        return [0.0] * len(rates)
    scaled = [rate / peak for rate in rates]
    total = math.fsum(scaled)
    return [rate / total * 1_000_000 for rate in scaled]


def convert(path):
    with open(path, newline='', encoding='utf-8-sig') as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
        if len(header) < 3 or header[:2] != ['gene_id', 'length_bp'] or len(set(header)) != len(header):
            raise ValueError('CSV header must be gene_id,length_bp,<unique sample names>')
        rows, seen = [], set()
        for number, row in enumerate(reader, 2):
            if len(row) != len(header) or not row[0].strip() or row[0] in seen:
                raise ValueError(f'row {number}: wrong width, missing ID or duplicate gene_id')
            seen.add(row[0])
            rows.append((row[0], [float(value) for value in row[1:]]))
    if not rows:
        raise ValueError('no genes')
    lengths = [values[0] for _, values in rows]
    columns = [tpm([values[i] for _, values in rows], lengths) for i in range(1, len(header)-1)]
    return ['gene_id']+header[2:], [[gene]+[column[i] for column in columns] for i,(gene,_) in enumerate(rows)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('counts_csv')
    args = parser.parse_args()
    try:
        header, rows = convert(args.counts_csv)
    except (OSError, ValueError, OverflowError) as error:
        parser.error(str(error))
    writer = csv.writer(sys.stdout, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(rows)


if __name__ == '__main__':
    main()
