"""Actual public-only numbering and MMseqs2 audit. No private candidates."""
from __future__ import annotations
import csv, hashlib, importlib.metadata, io, json, os, pathlib, platform, random, shutil, subprocess, sys, tarfile, time, traceback, urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path('evidence')
ROOT.mkdir(exist_ok=True)
RAW = ROOT / 'raw_public_sources'; RAW.mkdir(exist_ok=True)
LOGS = ROOT / 'logs'; LOGS.mkdir(exist_ok=True)
REPORT = {'started_utc': datetime.now(timezone.utc).isoformat(), 'private_candidates_received': False, 'private_candidates_screened': 0, 'new_design_sequences': 0, 'complex_predictions': 0, 'official_novelty_cleared': False, 'status': 'RUNNING', 'commands': [], 'errors': []}
TNF_ENTRIES = ('5M2I', '5M2J', '5M2M', '8Z8M')
CONTROL_ENTRIES = ('8Z8V', '7EOW')
AA = set('ACDEFGHIKLMNPQRSTVWY')
MMSEQS_URL = 'https://github.com/soedinglab/MMseqs2/releases/download/18-8cc5c/mmseqs-linux-avx2.tar.gz'
MMSEQS_SHA = 'bd9b0234da5949ad528d5b5f9ea4cda9c1e23dce14b46c0791d4d919a76e61ce'
FIELDS = 'query,target,nident,alnlen,qstart,qend,qlen,tstart,tend,tlen,qcov,fident,qaln,taln'.split(',')

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + '\n')

def get_public(url, name):
    request = urllib.request.Request(url, headers={'User-Agent': 'TNFA-public-reference-audit/1.0'})
    with urllib.request.urlopen(request, timeout=60) as r:
        data = r.read(30_000_001)
        if len(data) > 30_000_000:
            raise RuntimeError('Public asset exceeds size cap')
    (RAW / name).write_bytes(data)
    return json.loads(data)

def command(argv, name, timeout=150):
    before = time.monotonic()
    p = subprocess.run([str(a) for a in argv], capture_output=True, text=True, timeout=timeout)
    (LOGS / (name + '.stdout.txt')).write_text(p.stdout)
    (LOGS / (name + '.stderr.txt')).write_text(p.stderr)
    REPORT['commands'].append({'argv': [str(a) for a in argv], 'returncode': p.returncode, 'seconds': time.monotonic()-before})
    if p.returncode:
        raise RuntimeError(name + ' failed; see preserved log')
    return p.stdout

def fasta(path, sequences):
    if not sequences:
        raise ValueError('Refuse empty FASTA')
    path.write_text(''.join('>' + k + '\n' + v + '\n' for k,v in sequences.items()))

def risk(nq, qlen, nident, alnlen):
    if not (0 <= nq <= qlen and 0 <= nident <= alnlen and qlen > 0 and alnlen > 0):
        raise ValueError('Invalid integer alignment counts')
    return 5*nq >= 4*qlen and 10*nident > 7*alnlen

def check_tsv(path):
    checked = []
    with path.open() as f:
        for values in csv.reader(f, delimiter='\t'):
            if not values: continue
            if len(values) != len(FIELDS): raise ValueError('Unexpected MMseqs2 columns')
            row = dict(zip(FIELDS, values))
            a, b = row['qaln'], row['taln']
            if len(a) != len(b): raise ValueError('Alignment strings differ in length')
            nident = sum(x == y and x != '-' for x,y in zip(a,b))
            nq = len(a.replace('-', '')); nt = len(b.replace('-', ''))
            if nident != int(row['nident']) or len(a) != int(row['alnlen']):
                raise ValueError('Native counts disagree with explicit alignment strings')
            if nq != int(row['qend'])-int(row['qstart'])+1 or nt != int(row['tend'])-int(row['tstart'])+1:
                raise ValueError('Coverage coordinate mismatch')
            qlen = int(row['qlen']); alen = len(a)
            if abs(float(row['qcov'])-nq/qlen) > 0.002 or abs(float(row['fident'])-nident/alen) > 0.002:
                raise ValueError('Reported fractions disagree with integer recomputation')
            row.update(query_covered_residues=nq, query_length=qlen, identical_residues=nident, alignment_columns=alen, gap_columns=sum(x=='-' or y=='-' for x,y in zip(a,b)), coverage_exact=nq/qlen, identity_exact=nident/alen, risk_80_70=risk(nq,qlen,nident,alen))
            checked.append(row)
    return checked

def mmsearch(executable, q, t, label, no_mask=False):
    output = ROOT / (label + '.tsv')
    args = [executable, 'easy-search', q, t, output, ROOT/(label+'_tmp'), '--threads', '2', '-a', '--alignment-mode', '3', '--seq-id-mode', '0', '--cov-mode', '2', '-c', '0', '--min-seq-id', '0', '-e', '1000000', '--max-seqs', '10000', '-s', '7.5', '--format-output', ','.join(FIELDS)]
    if no_mask: args += ['--mask', '0', '--comp-bias-corr', '0']
    command(args,label)
    rows = check_tsv(output)
    write_json(ROOT/(label+'_integer_audit.json'), rows)
    shutil.rmtree(ROOT/(label+'_tmp'), ignore_errors=True)
    return rows

def run():
    REPORT['environment'] = {'python':sys.version, 'platform':platform.platform(), 'commit':os.getenv('GITHUB_SHA'), 'workflow_run_id':os.getenv('GITHUB_RUN_ID'), 'anarcii':importlib.metadata.version('anarcii'), 'torch':importlib.metadata.version('torch')}
    tests = [((40,50,35,50),False),((40,50,36,50),True),((39,50,50,50),False),((30,37,21,30),False),((30,37,22,30),True),((29,37,29,29),False)]
    for args,expected in tests: assert risk(*args) == expected
    write_json(ROOT/'integer_boundary_tests.json',[{'counts':args,'expected_risk':expected,'actual_risk':risk(*args)} for args,expected in tests])
    REPORT['arithmetic_boundary_tests_passed'] = len(tests)
    records = []
    for pdb in TNF_ENTRIES + CONTROL_ENTRIES:
        entry = get_public(f'https://data.rcsb.org/rest/v1/core/entry/{pdb}', pdb+'_entry.json')
        title = entry.get('struct',{}).get('title','')
        if pdb in TNF_ENTRIES and not ('tnf' in title.lower() or 'tumor necrosis factor' in title.lower()):
            raise ValueError('Unexpected title for declared TNF complex: '+pdb)
        for eid in entry['rcsb_entry_container_identifiers']['polymer_entity_ids']:
            entity = get_public(f'https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb}/{eid}', pdb+'_entity_'+eid+'.json')
            seq = ''.join(entity.get('entity_poly',{}).get('pdbx_seq_one_letter_code_can','').split()).upper()
            if not 90 <= len(seq) <= 160 or set(seq)-AA: continue
            desc = entity.get('rcsb_polymer_entity',{}).get('pdbx_description','')
            records.append({'id':pdb+'_entity_'+eid,'pdb':pdb,'entity':eid,'title':title,'description':desc,'sequence':seq,'scope':'TNF_public_exclusion_reference' if pdb in TNF_ENTRIES else 'NON_TNF_scope_control','chains':entity.get('rcsb_polymer_entity_container_identifiers',{}).get('auth_asym_ids',[])})
    from anarcii import Anarcii
    model = Anarcii(seq_type='antibody', mode='accuracy', cpu=True, ncpu=2, batch_size=8)
    numbered = model.number({r['id']:r['sequence'] for r in records})
    write_json(ROOT/'public_entities_numbering_raw.json',numbered)
    kept = []; excluded = []
    for record in records:
        result = numbered.get(record['id'],{})
        if result.get('error') or result.get('chain_type') != 'H' or not result.get('numbering'):
            excluded.append({**record,'reason':'not successfully numbered H domain','numbering_result':result}); continue
        if str(result.get('scheme','imgt')).lower() != 'imgt': raise ValueError('Unexpected numbering scheme')
        numbering = result['numbering']
        pieces = []
        for low,high in ((27,38),(56,65),(105,117)):
            pieces.append(''.join(aa for pos,aa in numbering if low<=int(pos[0])<=high and aa!='-'))
        domain = ''.join(aa for pos,aa in numbering if aa!='-')
        if domain not in record['sequence'] or not all(pieces): raise ValueError('Domain/CDR extraction inconsistency')
        kept.append({**record,'numbering_scheme':'IMGT','CDR1':pieces[0],'CDR2':pieces[1],'CDR3':pieces[2],'CDR_concat':''.join(pieces),'numbered_domain':domain,'numbering_score':result.get('score'),'query_start':result.get('query_start'),'query_end':result.get('query_end')})
    write_json(ROOT/'public_VHH_reference_records.json',kept)
    write_json(ROOT/'excluded_non_H_entities.json',excluded)
    known = [r for r in kept if r['scope']=='TNF_public_exclusion_reference']
    assert {r['pdb'] for r in known} == set(TNF_ENTRIES), 'Each curated TNF complex must yield a numbered H domain'
    assert not any(r['pdb']=='8Z8V' for r in known), 'ALB8 is not an anti-TNF reference'
    reference = {r['id']:r['CDR_concat'] for r in known}
    all_cdr = {r['id']:r['CDR_concat'] for r in kept}
    fasta(ROOT/'public_TNF_CDR_IMGT.fasta',reference)
    fasta(ROOT/'public_controls_CDR_IMGT.fasta',all_cdr)
    fasta(ROOT/'public_VHH_full_sequences.fasta',{r['id']:r['sequence'] for r in kept})
    REPORT['public_tnf_reference_entries'] = len(known)
    REPORT['unique_public_tnf_CDR_sequences'] = len(set(reference.values()))
    REPORT['non_tnf_scope_controls'] = [r['id'] for r in kept if r['scope']!='TNF_public_exclusion_reference']
    tarpath = pathlib.Path('mmseqs18.tar.gz')
    with urllib.request.urlopen(MMSEQS_URL,timeout=90) as r: data=r.read(25_000_001)
    if hashlib.sha256(data).hexdigest()!=MMSEQS_SHA: raise ValueError('Official MMseqs2 archive digest mismatch')
    tarpath.write_bytes(data)
    with tarfile.open(tarpath) as tf: tf.extractall('tools',filter='data')
    exe = str(pathlib.Path('tools/mmseqs/bin/mmseqs').resolve())
    REPORT['mmseqs2']={'version':command([exe,'version'],'mmseqs_version').strip(),'archive_sha256':MMSEQS_SHA,'binary_sha256':hashlib.sha256(pathlib.Path(exe).read_bytes()).hexdigest()}
    regular = mmsearch(exe,ROOT/'public_controls_CDR_IMGT.fasta',ROOT/'public_TNF_CDR_IMGT.fasta','public_reference_default')
    sensitive = mmsearch(exe,ROOT/'public_controls_CDR_IMGT.fasta',ROOT/'public_TNF_CDR_IMGT.fasta','public_reference_unmasked',True)
    self_default = {r['query'] for r in regular if r['query']==r['target'] and r['coverage_exact']==1 and r['identity_exact']==1}
    self_unmasked = {r['query'] for r in sensitive if r['query']==r['target'] and r['coverage_exact']==1 and r['identity_exact']==1}
    REPORT['native_reference_rows']={'default':len(regular),'unmasked':len(sensitive)}
    REPORT['self_control_recovery']={'default':len(self_default),'unmasked':len(self_unmasked),'expected':len(reference),'missing_default':sorted(set(reference)-self_default),'missing_unmasked':sorted(set(reference)-self_unmasked)}
    rng=random.Random(20261107)
    q=''.join(rng.choice(sorted(AA)) for _ in range(50))
    fasta(ROOT/'SYNTHETIC_query_NOT_CANDIDATE.fasta',{'synthetic50':q})
    targets={'self50':q,'prefix40':q[:40],'prefix39':q[:39],'gap_insert':q[:25]+'WPK'+q[25:]}
    fasta(ROOT/'SYNTHETIC_targets_NOT_CANDIDATES.fasta',targets)
    fixture=mmsearch(exe,ROOT/'SYNTHETIC_query_NOT_CANDIDATE.fasta',ROOT/'SYNTHETIC_targets_NOT_CANDIDATES.fasta','synthetic_native_alignment',True)
    REPORT['synthetic_native_rows']=len(fixture)
    REPORT['synthetic_results']=[{k:r[k] for k in ('target','query_covered_residues','query_length','identical_residues','alignment_columns','gap_columns','coverage_exact','identity_exact','risk_80_70')} for r in fixture]
    if len(self_unmasked)!=len(reference): raise RuntimeError('Unmasked self-control recovery failed; do not trust no-hit results')
    REPORT['status']='PUBLIC_AUDIT_COMPLETED_PRIVATE_CANDIDATES_NOT_SCREENED'
    (ROOT/'README_zh.md').write_text('# TNF公开参考集与真实MMseqs2检查\n\n本包只含公开PDB数据和明确标记的人工测试序列。没有上传或检查R08私有候选，没有生成新分子，没有预测复合物。\n\n采用ANARCII 2.0.8的antibody/accuracy/CPU模型重新编号；使用IMGT 27–38、56–65、105–117区间，去除编号空位后串联CDR。该CDR定义是本地预筛选择，不等于组委会未披露的内部定义。5M2I、5M2J、5M2M、8Z8M是有限的公开TNF排除参考；8Z8V为albumin结合域，仅为非TNF范围对照；7EOW为非TNF来源对照。阳性参考绝不作为提交序列或优化母本。\n\nMMseqs2 18-8cc5c实际运行两组参数；保留逐列原生比对、gap计数、query覆盖和整数边界检查。两组参数的无命中均不能认证官方私有参考库新颖性。实际结果以summary.json及原始TSV为准。\n\n范围：CDR公开参考准备和软件行为验证；不是新候选结果、不是官方算法完整复现、不是亲和力证据。\n')

try:
    run()
except Exception as exc:
    REPORT['status']='FAILED_WITH_PRESERVED_EVIDENCE'
    REPORT['errors'].append(type(exc).__name__+': '+str(exc))
    (LOGS/'failure_traceback.txt').write_text(traceback.format_exc())
finally:
    REPORT['finished_utc']=datetime.now(timezone.utc).isoformat()
    write_json(ROOT/'summary.json',REPORT)
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'}
    write_json(ROOT/'SHA256SUMS.json',manifest)
    print('PUBLIC_AUDIT_SUMMARY='+json.dumps(REPORT,ensure_ascii=False))
if REPORT['status'].startswith('FAILED'): raise SystemExit(1)
