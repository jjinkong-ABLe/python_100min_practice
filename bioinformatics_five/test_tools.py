import io
import math
import tempfile
import unittest
from pathlib import Path

from alpha_diversity import diversity
from bed_overlap import overlaps, read_bed
from gene_set_ora import bh_adjust, enrich, hypergeom_tail
from pdb_ca_geometry import geometry, read_ca
from rnaseq_tpm import convert, tpm


class BedTests(unittest.TestCase):
    def test_half_open_and_pairwise(self):
        left = [('chr1',0,10,1),('chr2',0,10,2)]
        right = [('chr1',10,20,1),('chr1',5,15,2),('chr1',0,10,3)]
        self.assertEqual(list(overlaps(left,right)),[
            ('chr1',1,3,0,10,10),('chr1',1,2,5,10,5)])

    def test_invalid_interval(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'bad.bed'
            path.write_text('chr1\t3\t3\n',encoding='utf-8')
            with self.assertRaises(ValueError):
                read_bed(path)


class TpmTests(unittest.TestCase):
    def test_known_ratio(self):
        values = tpm([10,20],[1000,2000])
        self.assertEqual(values,[500000.0,500000.0])
        self.assertAlmostEqual(sum(tpm([3,5,7],[2,3,4])),1e6)

    def test_empty_library(self):
        self.assertEqual(tpm([0,0],[10,20]),[0,0])

    def test_reject_bad_values(self):
        for counts,lengths in [([1],[0]),([-1],[3]),([float('inf')],[3]),([1],[float('nan')])]:
            with self.subTest(counts=counts,lengths=lengths),self.assertRaises(ValueError):
                tpm(counts,lengths)

    def test_csv_duplicate_gene(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'counts.csv'
            path.write_text('gene_id,length_bp,S\nA,100,2\nA,100,3\n',encoding='utf-8')
            with self.assertRaises(ValueError):
                convert(path)


class OraTests(unittest.TestCase):
    def test_exact_combinatorial_probability(self):
        expected = sum(math.comb(4,k)*math.comb(16,5-k) for k in range(2,5))/math.comb(20,5)
        self.assertAlmostEqual(hypergeom_tail(20,4,5,2),expected,places=12)
        self.assertEqual(hypergeom_tail(20,4,5,0),1)
        self.assertEqual(hypergeom_tail(20,4,5,5),0)

    def test_bh_known_values_and_order(self):
        observed = bh_adjust([0.01,0.04,0.03,0.2])
        for actual,expected in zip(observed,[0.04,0.05333333333333334,0.05333333333333334,0.2]):
            self.assertAlmostEqual(actual,expected)
        self.assertEqual(bh_adjust([]),[])

    def test_background_controls_membership(self):
        rows = enrich({'A'}, {'A','B','C'}, {'example':{'A','X'}, 'outside':{'X'}})
        self.assertEqual(rows[0]['set_size'],1)
        self.assertEqual(rows[1]['p_value'],1)
        with self.assertRaises(ValueError):
            enrich({'X'},{'A'},{'example':{'A'}})


class DiversityTests(unittest.TestCase):
    def test_equal_abundances(self):
        result = diversity([1,1,0])
        self.assertEqual(result['richness'],2)
        self.assertAlmostEqual(result['shannon'],math.log(2))
        self.assertAlmostEqual(result['gini_simpson'],0.5)
        self.assertAlmostEqual(result['pielou'],1)

    def test_empty_and_single_feature(self):
        self.assertIsNone(diversity([0,0])['shannon'])
        self.assertIsNone(diversity([5,0])['pielou'])
        self.assertEqual(diversity([5,0])['gini_simpson'],0)

    def test_invalid_values(self):
        for value in [-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):
                diversity([value])


class PdbTests(unittest.TestCase):
    def test_known_distance_and_radius(self):
        result = geometry([(('A',1,''),(0,0,0)),(('A',2,''),(3,4,0))])
        self.assertEqual(result['adjacent_observed_ca_distances'][0]['distance_angstrom'],5)
        self.assertEqual(result['unweighted_ca_radius_of_gyration_angstrom'],2.5)

    def test_chain_boundary(self):
        self.assertEqual(geometry([(('A',1,''),(0,0,0)),(('B',1,''),(3,4,0))])[
            'adjacent_observed_ca_distances'],[])

    def test_first_model_only_and_altloc(self):
        def atom(serial,residue,xyz,alt=' '):
            return f'ATOM  {serial:5d}  CA {alt}GLY A{residue:4d}    {xyz[0]:8.3f}{xyz[1]:8.3f}{xyz[2]:8.3f}  1.00 20.00           C\n'
        text = 'MODEL        1\n'+atom(1,1,(9,9,9),'A')+atom(2,1,(0,0,0))+atom(3,2,(3,4,0))+'ENDMDL\nMODEL        2\n'+atom(4,1,(99,99,99))+'ENDMDL\n'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'toy.pdb'
            path.write_text(text,encoding='utf-8')
            atoms = read_ca(path)
        self.assertEqual(len(atoms),2)
        self.assertEqual(atoms[0][1],(0,0,0))


if __name__ == '__main__':
    unittest.main()
