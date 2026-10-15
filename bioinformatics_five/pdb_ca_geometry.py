"""Read legacy PDB C-alpha coordinates and summarize unweighted geometry."""
import argparse
import json
import math


def read_ca(path):
    atoms, order = {}, []
    with open(path, encoding='utf-8') as handle:
        for number, line in enumerate(handle, 1):
            if line.startswith('ENDMDL'):
                break  # first model only
            if line[:6].strip()!='ATOM' or line[12:16].strip()!='CA':
                continue
            alt = line[16:17]
            if alt not in {' ', 'A'}:
                continue
            try:
                key = (line[21:22],int(line[22:26]),line[26:27])
                xyz = tuple(float(line[start:start+8]) for start in (30,38,46))
            except ValueError as error:
                raise ValueError(f'PDB line {number}: invalid residue/coordinates') from error
            if not all(math.isfinite(value) for value in xyz):
                raise ValueError(f'PDB line {number}: nonfinite coordinates')
            if key not in atoms:
                order.append(key)
                atoms[key] = (alt,xyz)
            elif atoms[key][0]=='A' and alt==' ':
                atoms[key] = (alt,xyz)
            elif atoms[key][0]==alt:
                raise ValueError(f'PDB line {number}: duplicate C-alpha identifier')
    if not atoms:
        raise ValueError('no supported ATOM C-alpha records in first model')
    return [(key,atoms[key][1]) for key in order]


def geometry(atoms):
    if not atoms:
        raise ValueError('no C-alpha coordinates')
    center = [math.fsum(xyz[i] for _,xyz in atoms)/len(atoms) for i in range(3)]
    rg = math.sqrt(math.fsum(math.dist(xyz,center)**2 for _,xyz in atoms)/len(atoms))
    previous, distances = {}, []
    for (chain,residue,icode),xyz in atoms:
        if chain in previous:
            previous_id,previous_xyz = previous[chain]
            distances.append({'chain':chain.strip() or '_', 'from':previous_id,
                              'to':str(residue)+icode.strip(),
                              'distance_angstrom':math.dist(xyz,previous_xyz)})
        previous[chain] = (str(residue)+icode.strip(),xyz)
    return {'ca_atoms':len(atoms), 'centroid_angstrom':center,
            'unweighted_ca_radius_of_gyration_angstrom':rg,
            'adjacent_observed_ca_distances':distances}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdb')
    args = parser.parse_args()
    try:
        result = geometry(read_ca(args.pdb))
    except (OSError,ValueError,OverflowError) as error:
        parser.error(str(error))
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__ == '__main__':
    main()
