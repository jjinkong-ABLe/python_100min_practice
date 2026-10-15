"""One-sided hypergeometric over-representation with Benjamini-Hochberg FDR."""
import argparse
import csv
import math
import sys


def hypergeom_tail(total, members, selected, overlap):
    if not (0 <= members <= total and 0 <= selected <= total and total > 0):
        raise ValueError('invalid universe/set/query sizes')
    lower, upper = max(0, selected-(total-members)), min(members, selected)
    if overlap <= lower:
        return 1.0
    if overlap > upper:
        return 0.0
    def log_choose(n, k):
        return math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)
    logs = [log_choose(members,k)+log_choose(total-members,selected-k)-log_choose(total,selected)
            for k in range(overlap, upper+1)]
    peak = max(logs)
    return min(1.0, math.exp(peak)*math.fsum(math.exp(value-peak) for value in logs))


def bh_adjust(pvalues):
    if any(not math.isfinite(p) or not 0 <= p <= 1 for p in pvalues):
        raise ValueError('p-values must be finite and in [0,1]')
    order = sorted(range(len(pvalues)), key=pvalues.__getitem__)
    adjusted, previous = [0.0]*len(pvalues), 1.0
    for rank in range(len(order), 0, -1):
        index = order[rank-1]
        previous = min(previous, pvalues[index]*len(order)/rank)
        adjusted[index] = previous
    return adjusted


def enrich(query, universe, gene_sets):
    if not universe or not query or not query <= universe:
        raise ValueError('query must be nonempty and a subset of a nonempty measured universe')
    rows = []
    for name, genes in gene_sets.items():
        members = genes & universe
        overlap = query & members
        rows.append({'set': name, 'universe_size': len(universe), 'set_size': len(members),
                     'query_size': len(query), 'overlap': len(overlap),
                     'p_value': hypergeom_tail(len(universe),len(members),len(query),len(overlap)),
                     'overlap_genes': ';'.join(sorted(overlap))})
    for row, qvalue in zip(rows, bh_adjust([row['p_value'] for row in rows])):
        row['q_value_bh'] = qvalue
    return sorted(rows, key=lambda row: (row['p_value'], row['set']))


def read_genes(path):
    with open(path, encoding='utf-8-sig') as handle:
        return {line.strip() for line in handle if line.strip() and not line.startswith('#')}


def read_gmt(path):
    sets = {}
    with open(path, encoding='utf-8-sig') as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip() or line.startswith('#'):
                continue
            fields = line.rstrip('\n').split('\t')
            if len(fields) < 3 or not fields[0] or fields[0] in sets:
                raise ValueError(f'GMT row {number}: invalid or duplicate set name')
            sets[fields[0]] = {gene for gene in fields[2:] if gene}
    if not sets:
        raise ValueError('no gene sets')
    return sets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('universe')
    parser.add_argument('gmt')
    args = parser.parse_args()
    try:
        rows = enrich(read_genes(args.query),read_genes(args.universe),read_gmt(args.gmt))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    fields = ['set','universe_size','set_size','query_size','overlap','p_value','q_value_bh','overlap_genes']
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, delimiter='\t', lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)


if __name__ == '__main__':
    main()
