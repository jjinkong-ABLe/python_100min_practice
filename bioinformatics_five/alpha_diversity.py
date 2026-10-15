"""Observed richness, natural-log Shannon, Gini-Simpson and Pielou evenness."""
import argparse
import csv
import math
import sys


def diversity(counts):
    if any(not math.isfinite(x) or x < 0 for x in counts):
        raise ValueError('abundances must be finite and nonnegative')
    total = math.fsum(counts)
    positive = [x for x in counts if x > 0]
    if not positive:
        return {'total': total, 'richness': 0, 'shannon': None, 'gini_simpson': None, 'pielou': None}
    proportions = [x/total for x in positive]
    shannon = -math.fsum(p*math.log(p) for p in proportions)
    return {'total': total, 'richness': len(positive), 'shannon': shannon,
            'gini_simpson': 1-math.fsum(p*p for p in proportions),
            'pielou': shannon/math.log(len(positive)) if len(positive)>1 else None}


def summarize(path):
    with open(path, newline='', encoding='utf-8-sig') as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
        if len(header)<2 or header[0] != 'feature_id' or len(set(header)) != len(header):
            raise ValueError('CSV header must be feature_id,<unique sample names>')
        columns, seen = [[] for _ in header[1:]], set()
        for number, row in enumerate(reader, 2):
            if len(row)!=len(header) or not row[0] or row[0] in seen:
                raise ValueError(f'row {number}: invalid width/feature_id')
            seen.add(row[0])
            for column, value in zip(columns, row[1:]):
                column.append(float(value))
        if not seen:
            raise ValueError('no features')
    return [dict(sample=sample, **diversity(column)) for sample,column in zip(header[1:],columns)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('abundance_csv')
    args = parser.parse_args()
    try:
        rows = summarize(args.abundance_csv)
    except (OSError, ValueError, OverflowError) as error:
        parser.error(str(error))
    writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)


if __name__ == '__main__':
    main()
