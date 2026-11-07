"""Public-only MMseqs2 pair-completeness follow-up. Never reads private candidates.
Enumerates all sequence pairs, not all possible alignments. No design, cofold,
provider submission, purchases, or official novelty certification.
"""
from __future__ import annotations
import csv, hashlib, io, json, os, pathlib, platform, shutil, struct, subprocess, sys, tarfile, time, traceback, urllib.error, urllib.parse, urllib.request, zipfile
from datetime import datetime, timezone

OUT = pathlib.Path('pairwise_evidence'); OUT.mkdir(exist_ok=False)
LOG = OUT / 'logs'; LOG.mkdir()
SOURCE = OUT / 'source_audit'; SOURCE.mkdir()
SOURCE_ID = 13556011887
SOURCE_SHA = '71c816e09d53def58530917cd5108fb0221b166de565d8fc7be92b1b400058e9'
MM_SHA = 'bd9b0234da5949ad528d5b5f9ea4cda9c1e23dce14b46c0791d4d919a76e61ce'
FIELDS = 'query,target,nident,alnlen,qstart,qend,qlen,tstart,tend,tlen,qcov,fident,qaln,taln'.split(',')
REPORT = {'started_utc':datetime.now(timezone.utc).isoformat(), 'status':'RUNNING', 'private_candidates_received':False, 'private_candidates_screened':0, 'new_design_sequences':0, 'complex_predictions':0, 'provider_inference_requests':0, 'official_novelty_cleared':False, 'commands':[], 'errors':[]}


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def limited_read(response, maximum):
    data = response.read(maximum+1)
    if len(data)>maximum: raise RuntimeError('Download exceeds declared byte budget')
    return data


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def previous_artifact():
    token = os.environ.get('GH_TOKEN')
    if not token: raise RuntimeError('Read-only artifact token missing')
    repo = os.environ['GITHUB_REPOSITORY']
    url = f'https://api.github.com/repos/{repo}/actions/artifacts/{SOURCE_ID}/zip'
    request = urllib.request.Request(url, headers={'Authorization':'Bearer '+token, 'Accept':'application/vnd.github+json', 'X-GitHub-Api-Version':'2022-11-28', 'User-Agent':'TNFA-public-pair-audit/1.0'})
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=40) as response:
            data = limited_read(response, 2_000_000)
    except urllib.error.HTTPError as exc:
        if exc.code not in (301,302,303,307,308): raise RuntimeError('Artifact endpoint status '+str(exc.code)) from None
        location = exc.headers.get('Location','')
        parsed = urllib.parse.urlparse(location)
        if parsed.scheme!='https' or parsed.username or parsed.password: raise RuntimeError('Unsafe artifact redirect')
        # Intentionally DO NOT forward Authorization to the blob-storage origin.
        with urllib.request.urlopen(urllib.request.Request(location, headers={'User-Agent':'TNFA-public-pair-audit/1.0'}), timeout=60) as response:
            data = limited_read(response, 2_000_000)
    if hashlib.sha256(data).hexdigest()!=SOURCE_SHA: raise RuntimeError('Original audit archive hash mismatch')
    (OUT/'original_public_audit.zip').write_bytes(data)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if sum(i.file_size for i in archive.infolist())>12_000_000: raise RuntimeError('Archive expansion limit')
        for info in archive.infolist():
            name=pathlib.PurePosixPath(info.filename)
            if name.is_absolute() or '..' in name.parts or ((info.external_attr>>16)&0o170000)==0o120000: raise RuntimeError('Unsafe archive member')
            if info.is_dir(): continue
            dest=SOURCE.joinpath(*name.parts); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(archive.read(info))
    manifest=json.loads((SOURCE/'SHA256SUMS.json').read_text())
    for name,expected in manifest.items():
        path=SOURCE/name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected: raise RuntimeError('Source member mismatch: '+name)
    REPORT['source_archive']={'artifact_id':SOURCE_ID,'bytes':len(data),'sha256':SOURCE_SHA,'manifest_members_verified':len(manifest)}


def command(argv, label):
    start=time.monotonic()
    proc=subprocess.run([str(x) for x in argv],capture_output=True,text=True,timeout=120)
    (LOG/(label+'.stdout.txt')).write_text(proc.stdout)
    (LOG/(label+'.stderr.txt')).write_text(proc.stderr)
    REPORT['commands'].append({'argv':[str(x) for x in argv],'returncode':proc.returncode,'seconds':time.monotonic()-start})
    if proc.returncode: raise RuntimeError(label+' failed; original logs retained')
    return proc.stdout


def fasta_records(path):
    result={}; key=None
    for line in path.read_text().splitlines():
        if not line: continue
        if line.startswith('>'):
            key=line[1:].split()[0]
            if key in result: raise ValueError('Duplicate FASTA ID')
            result[key]=''
        else:
            if key is None: raise ValueError('FASTA sequence before header')
            result[key]+=line.strip()
    if not result or any(not s or set(s)-set('ACDEFGHIKLMNPQRSTVWY') for s in result.values()): raise ValueError('Invalid FASTA')
    return result


def parse_rows(path):
    rows=[]
    with path.open() as handle:
        for fields in csv.reader(handle,delimiter='\t'):
            if not fields: continue
            if len(fields)!=len(FIELDS): raise ValueError('Column count mismatch')
            r=dict(zip(FIELDS,fields)); a,b=r['qaln'],r['taln']
            if not a or len(a)!=len(b) or any(x==y=='-' for x,y in zip(a,b)): raise ValueError('Invalid alignment')
            nq=sum(x!='-' for x in a); nt=sum(x!='-' for x in b); ni=sum(x==y and x!='-' for x,y in zip(a,b)); alen=len(a); qlen=int(r['qlen'])
            if ni!=int(r['nident']) or alen!=int(r['alnlen']) or nq!=int(r['qend'])-int(r['qstart'])+1 or nt!=int(r['tend'])-int(r['tstart'])+1: raise ValueError('Native integer counts disagree')
            if not (0<=ni<=min(nq,nt) and 0<nq<=qlen): raise ValueError('Impossible identity or coverage count')
            if abs(float(r['qcov'])-nq/qlen)>0.002 or abs(float(r['fident'])-ni/alen)>0.002: raise ValueError('Native fraction mismatch')
            r.update(query_covered_residues=nq,query_length=qlen,identical_residues=ni,alignment_columns=alen,gap_columns=sum(x=='-' or y=='-' for x,y in zip(a,b)),coverage_exact=nq/qlen,identity_exact=ni/alen,risk_80_70=(5*nq>=4*qlen and 10*ni>7*alen))
            rows.append(r)
    pairs=[(r['query'],r['target']) for r in rows]
    if len(pairs)!=len(set(pairs)): raise ValueError('Duplicate alignment pair')
    return rows


def run():
    REPORT['environment']={'python':sys.version,'platform':platform.platform(),'commit':os.environ.get('GITHUB_SHA'),'run_id':os.environ.get('GITHUB_RUN_ID'),'gpu_utility_present':bool(shutil.which('nvidia-smi'))}
    # Only report existence of already configured named credentials, never contents.
    REPORT['existing_nvidia_credential_present']=bool(os.environ.pop('NVIDIA_HOSTED_CREDENTIAL',''))
    previous_artifact()
    url='https://github.com/soedinglab/MMseqs2/releases/download/18-8cc5c/mmseqs-linux-avx2.tar.gz'
    with urllib.request.urlopen(url,timeout=60) as response: data=limited_read(response,25_000_000)
    if hashlib.sha256(data).hexdigest()!=MM_SHA: raise RuntimeError('Pinned MMseqs2 archive digest mismatch')
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as archive: archive.extractall('pairwise_tools',filter='data')
    exe=str(pathlib.Path('pairwise_tools/mmseqs/bin/mmseqs').resolve())
    REPORT['mmseqs_version']=command([exe,'version'],'version').strip()
    REPORT['mmseqs_binary_sha256']=hashlib.sha256(pathlib.Path(exe).read_bytes()).hexdigest()
    q=SOURCE/'public_controls_CDR_IMGT.fasta'; t=SOURCE/'public_TNF_CDR_IMGT.fasta'
    queries=fasta_records(q); targets=fasta_records(t)
    db=OUT/'native_db'; db.mkdir()
    qdb=db/'q'; tdb=db/'t'; pref=db/'all_pairs_pref'; aln=db/'all_pairs_aln'
    command([exe,'createdb',q,qdb],'create_query')
    command([exe,'createdb',t,tdb],'create_target')
    target_index=pathlib.Path(str(tdb)+'.index').read_bytes()
    # Official MMseqs2 all-vs-all amino-acid technique: every query index points
    # to the complete target-key list. This bypasses only the k-mer prefilter.
    pref.write_bytes(target_index)
    qkeys=[line.split()[0] for line in pathlib.Path(str(qdb)+'.index').read_text().splitlines()]
    pathlib.Path(str(pref)+'.index').write_text(''.join(k+'\t0\t'+str(len(target_index))+'\n' for k in qkeys))
    pathlib.Path(str(pref)+'.dbtype').write_bytes(struct.pack('<I',7))
    command([exe,'align',qdb,tdb,pref,aln,'--threads','2','-a','--alignment-mode','3','--seq-id-mode','0','--cov-mode','2','-c','0','--min-seq-id','0','-e','1000000','--comp-bias-corr','0'],'native_all_pairs_align')
    out=OUT/'all_pairs_native.tsv'
    command([exe,'convertalis',qdb,tdb,aln,out,'--format-output',','.join(FIELDS)],'convert_all_pairs')
    exhaustive=parse_rows(out)
    prior={name:parse_rows(SOURCE/('public_reference_'+name+'.tsv')) for name in ('default','unmasked')}
    write_json(OUT/'all_pairs_integer_audit.json',exhaustive)
    expected={(a,b) for a in queries for b in targets}; actual={(r['query'],r['target']) for r in exhaustive}
    if actual-expected: raise RuntimeError('Unexpected public sequence pair')
    self_found={r['query'] for r in exhaustive if r['query']==r['target'] and r['coverage_exact']==1 and r['identity_exact']==1}
    if self_found!=set(targets): raise RuntimeError('Self-control recovery failed')
    risks={(r['query'],r['target']) for r in exhaustive if r['risk_80_70']}
    REPORT['query_count']=len(queries); REPORT['target_count']=len(targets); REPORT['enumerated_pair_count']=len(expected); REPORT['reported_alignment_count']=len(exhaustive)
    REPORT['unreported_pairs_not_certified']=[list(x) for x in sorted(expected-actual)]
    REPORT['self_control_recovery']={'recovered':len(self_found),'expected':len(targets)}
    REPORT['all_pair_risk_hits']=[list(x) for x in sorted(risks)]
    comparisons={}
    for name,rows in prior.items():
        old={(r['query'],r['target']) for r in rows}; oldrisk={(r['query'],r['target']) for r in rows if r['risk_80_70']}
        comparisons[name]={'previous_rows':len(rows),'previous_risk_pairs':len(oldrisk),'newly_reported_pairs':[list(x) for x in sorted(actual-old)],'newly_risk_flagged_pairs':[list(x) for x in sorted(risks-oldrisk)],'previous_risk_pairs_not_flagged_now':[list(x) for x in sorted(oldrisk-risks)]}
    REPORT['comparison_with_original_search']=comparisons
    write_json(OUT/'comparison.json',comparisons)
    REPORT['status']='PUBLIC_PAIRWISE_AUDIT_COMPLETED_PRIVATE_CANDIDATES_NOT_SCREENED'
    (OUT/'README_zh.md').write_text('# TNF公开CDR逐对比对补充审计\n\n本次使用已核验公开参考审计归档，按MMseqs2官方方式绕过k-mer预过滤，枚举所有公开query/target配对，再运行原生align和convertalis。不是搜索所有可能比对路径，也不是组委会完整算法复现。\n\n全部输入是公开参考/范围对照；没有接收、上传或筛查R08候选，没有生成新序列或预测复合物，没有发送托管推理请求。已知抗TNF阳性序列只作为排除参考。\n\nsummary.json列出枚举配对数、实际输出行数、与两种原搜索的差异及80%/70%整数风险标记。新输出行不等于新增不合格候选；无命中也不是官方新颖性认证。\n\n现有NVIDIA凭据只检查是否配置，不读取到日志、不输出内容、不请求推理、不使用额度。\n',encoding='utf-8')

try:
    shutil.copy2(__file__,OUT/pathlib.Path(__file__).name)
    run()
except Exception as exc:
    REPORT['status']='FAILED_WITH_EVIDENCE'; REPORT['errors'].append(type(exc).__name__+': '+str(exc))
    (LOG/'failure.txt').write_text(traceback.format_exc())
finally:
    REPORT['finished_utc']=datetime.now(timezone.utc).isoformat()
    write_json(OUT/'summary.json',REPORT)
    write_json(OUT/'SHA256SUMS.json',{str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'})
    print('PUBLIC_PAIRWISE_SUMMARY='+json.dumps(REPORT,ensure_ascii=False))
if REPORT['status']=='FAILED_WITH_EVIDENCE': raise SystemExit(1)
