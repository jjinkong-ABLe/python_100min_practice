"""Pairwise BED3 intersections in zero-based, half-open coordinates."""
import argparse
import bisect
import csv
import sys
from collections import defaultdict


def read_bed(path):
    records = []
    with open(path, encoding='utf-8-sig') as handle:
        for number, raw in enumerate(handle, 1):
            if not raw.strip() or raw.startswith(('#', 'track ', 'browser ')):
                continue
            fields = raw.rstrip('\n').split('\t')
            if len(fields) < 3:
                raise ValueError(f'{path}:{number}: BED3 requires three tab-separated fields')
            chrom = fields[0].strip()
            try:
                start, end = int(fields[1]), int(fields[2])
            except ValueError as error:
                raise ValueError(f'{path}:{number}: coordinates must be integers') from error
            if not chrom or start < 0 or end <= start:
                raise ValueError(f'{path}:{number}: require chromosome and 0 <= start < end')
            records.append((chrom, start, end, number))
    return records


def overlaps(left, right):
    """Yield every overlapping input pair; touching boundaries do not overlap."""
    by_chrom = defaultdict(list)
    for record in right:
        by_chrom[record[0]].append(record)
    for chrom in by_chrom:
        by_chrom[chrom].sort(key=lambda record: record[1])
    starts = {chrom: [record[1] for record in rows] for chrom, rows in by_chrom.items()}
    for chrom, start, end, line in left:
        rows = by_chrom.get(chrom, [])
        stop = bisect.bisect_left(starts.get(chrom, []), end)
        for _, other_start, other_end, other_line in rows[:stop]:
            shared = min(end, other_end) - max(start, other_start)
            if shared > 0:
                yield chrom, line, other_line, max(start, other_start), min(end, other_end), shared


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('left')
    parser.add_argument('right')
    args = parser.parse_args()
    try:
        left, right = read_bed(args.left), read_bed(args.right)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    writer = csv.writer(sys.stdout, delimiter='\t', lineterminator='\n')
    writer.writerow(['chrom', 'left_line', 'right_line', 'start', 'end', 'overlap_bp'])
    writer.writerows(overlaps(left, right))


if __name__ == '__main__':
    main()
