# 생물정보학 분석 도구 5개

기존 계정의 BLAST 필터, FASTA/FASTQ·GFF3·VCF·SAM 요약, 단백질 계수와 다른 작업을 다루는 Python CLI 5개입니다. Python 3.11 이상 표준 라이브러리만 사용합니다. AI 도움을 받아 작성했으며 예시 데이터는 직접 만든 합성 자료입니다. 실제 연구 결과나 검증된 임상 분석 도구라고 주장하지 않습니다.

| 소스 | 서로 다른 분석 작업 |
|---|---|
| `bed_overlap.py` | 두 BED 파일의 구간 교집합과 겹치는 염기 수 |
| `rnaseq_tpm.py` | bulk RNA-seq 표의 길이·라이브러리 크기 정규화 |
| `gene_set_ora.py` | 유전자 집합 과대표현 검정과 BH FDR |
| `alpha_diversity.py` | 풍부도 표의 샘플별 다양도 계산 |
| `pdb_ca_geometry.py` | PDB Cα 좌표의 거리·무게 비가중 회전반경 |

## 실행

```console
python bed_overlap.py examples/a.bed examples/b.bed
python rnaseq_tpm.py examples/counts.csv
python gene_set_ora.py examples/query.txt examples/universe.txt examples/sets.gmt
python alpha_diversity.py examples/abundance.csv
python pdb_ca_geometry.py examples/toy.pdb
python -m unittest -v
```

결과는 표준 출력으로 내보냅니다. 파일로 저장하려면 명령 뒤에 `> results.tsv` 또는 `> results.json`을 붙입니다. 잘못된 입력은 오류 메시지와 종료 코드 2로 반환합니다.

## 1. BED 교집합

BED3 이상, 탭 구분, `0 <= start < end`인 0-based half-open 좌표만 지원합니다. 끝과 시작이 닿기만 한 구간은 교집합이 없습니다. 모든 겹치는 입력 행 쌍을 출력하며 중복 입력도 별도 행으로 취급합니다. 이름은 선택하지 않고 원본 줄 번호로 식별합니다. 염색체 이름이 완전히 같아야 비교합니다. Strand·BED12 블록은 해석하지 않습니다. 작은 자료용 구현이며 최악의 경우 O(A×B)여서 대규모 자료에는 bedtools 등을 권장합니다.

[UCSC BED 형식](https://genome.ucsc.edu/FAQ/FAQformat#format1)

## 2. TPM 정규화

입력은 `gene_id,length_bp,sample_1,...` CSV입니다. `rate=count/length_bp`, `TPM=rate/sum(rate)*1e6`을 샘플별로 계산합니다. 모든 count가 0인 샘플은 0을 반환합니다. 길이는 양수, count는 유한한 비음수여야 합니다. 길이 차이를 고려하는 단순 bulk 발현량 비교용이며, effective length·isoform 추정은 수행하지 않습니다. TPM을 차등 발현 검정용 원시 count 대신 사용하지 않습니다. 3′ UMI 자료에 이 길이 보정을 그대로 적용하는 것을 전제로 하지 않습니다.

[RSEM 설명](https://deweylab.github.io/RSEM/rsem-calculate-expression.html)

## 3. Gene-set ORA

query와 측정 가능한 배경(universe)은 줄당 유전자 하나이고, GMT는 `집합명 TAB 설명 TAB 유전자...` 형식입니다. query는 universe의 부분집합이어야 합니다. gene set은 universe와 교차한 뒤 hypergeometric 상측 꼬리확률 P(X≥k)를 구합니다. BH는 입력된 모든 집합에 대해 적용하며 겹침이 0인 집합도 포함합니다. gene ID 매핑, 발현량 기반 GSEA, 교란 보정은 하지 않습니다. 로그 조합 합산 방식이므로 극단적으로 작은 확률은 부동소수점 한계로 0이 될 수 있습니다.

[SciPy hypergeometric 정의](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypergeom.html)

## 4. Alpha diversity

입력은 `feature_id,sample_1,...` 풍부도 CSV입니다. 관측 풍부도 S, 자연로그 Shannon H, Gini-Simpson 1−Σp², Pielou H/ln(S)를 계산합니다. 빈 샘플은 richness=0이고 나머지는 빈 값이며, S≤1인 Pielou도 정의하지 않아 빈 값으로 둡니다. Rarefaction·오염 제거·샘플 간 통계 검정은 하지 않습니다. 시퀀싱 깊이와 전처리가 다른 자료의 지표를 단순 비교하지 마세요.

[scikit-bio 지표 정의](https://scikit.bio/docs/latest/diversity.html)

## 5. PDB Cα geometry

Legacy 고정폭 PDB의 첫 모델, `ATOM`의 `CA`만 읽습니다. HETATM·mmCIF는 지원하지 않습니다. altloc 공백을 A보다 우선하고 다른 altloc은 제외합니다. chain ID·residue number·insertion code로 원자를 식별합니다. 각 chain의 파일상 연속 관측 Cα 거리와 전체 관측 Cα의 동일 가중 회전반경을 Å 단위로 계산합니다. 결손 잔기 사이 거리도 포함될 수 있어 결합 길이로 해석하면 안 됩니다. 동일 chain ID를 TER 뒤에서 다시 사용하는 구조는 지원하지 않습니다. 질량 가중 전체 원자 회전반경·구조 품질·기능·결합 친화도를 추정하지 않습니다.

[wwPDB 좌표 형식](https://www.wwpdb.org/documentation/file-format-content/format33/sect9.html)

## 검증 범위

단위 테스트는 half-open 경계, TPM 합·0 샘플·오류 입력, 조합식으로 계산한 ORA 확률, BH 예시, 알려진 다양도 값, 합성 좌표의 3-4-5 거리 및 회전반경을 확인합니다. 모든 예시는 합성이며 생물학적 발견이나 실제 데이터 벤치마크를 뜻하지 않습니다.
