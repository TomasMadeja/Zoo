import yaml
from pathlib import Path

SRC = [

]

INTR = [

]

DST = [

]

def extract(_in):
    with Path(_in).open() as _f:
        yl = yaml.load(_f.read())
    x = sorted(yl['Items'], key=lambda x:float(x['Percent'].replace('%', '')))
    x.reverse()
    return [i['Description'] for i in x]

def _match_ip(_ip, matches):
    if '.' in _ip:
        _ip = _ip.split('.')
    else:
        _ip = _ip.split(':')
    
    if len(matches) > len(_ip):
        return False

    for i in range(len(matches)):
        if matches[i] != _ip[i]:
            return False
    return True


def match_ip(_ip, matches):
    res = False
    for match in matches:
        res = _match_ip(_ip, match) or res
    return res


def _build_map_entry(_from, _to4, _to6,
        inter, inter_i, inter6, inter6_i):
    r=[]
    i = 0
    i4 = 0
    i6 = 0
    while i < len(_from):
        if '.' in _from[i]:
            if i4 < len(_to4):
                _new = _to4[i4]
                i4 += 1
            else:
                _new = inter[inter_i]
                inter_i += 1
        else:
            if i6 < len(_to6):
                _new = _to6[i6]
                i6 += 1
            else:
                _new = inter6[inter6_i]
                inter6_i += 1
        entry = {
            'ip' : {
                'old' : _from[i],
                'new' : _new
            }
        }
        r.append(entry)
        i+=1
    return r, inter, inter_i, inter6, inter6_i


def build_map(_labels, dst4, inter, src4, dst6, inter6, src6):
    r, inter, inter_i, inter6, inter6_i = _build_map_entry(_labels['ip.destination'], dst4, dst6, inter, 0, inter6, 0)
    _r, inter, inter_i, inter6, inter6_i = _build_map_entry(_labels['ip.source'], src4, src6, inter, inter_i, inter6, inter6_i)
    r += _r
    _r, inter, inter_i, inter6, inter6_i = _build_map_entry(_labels['ip.intermediate'], [], [], inter, inter_i, inter6, inter6_i)
    r += _r
    return r


def prepare_background_ips(ips):
    src = []
    intr = []
    dst = []

    for ip in ips:
        if match_ip(ip, SRC):
            src.append(ip)
        elif match_ip(ip, DST):
            dst.append(ip)
        else:
            intr.append(ip)
    return dst, intr, src

def build_config(
        annotated_unit_path,
        ip_man=[],
        timestamp_generation='tcp_avg_shift',
        postprocess=[],
        generation_alt='timestamp_dynamic_shift',
        random_threshold=None,
        test_output_dir='../TMTestDir'
    ):
    cfg = {
        'atk.file' : annotated_unit_path,
        'read.write' : 'sequence',
        'export.filetype' : 'xlsx',
        'test.output.dir.path' : test_output_dir,
        'timestamp' : {
            'generation' : timestamp_generation,
            'postprocess' : [
                {'function' : i} for i in postprocess
            ],
            'generation_alt' : generation_alt,
            'random.threshold' : random_threshold
        },
        'ip.map' : [
            {
                'ip' : {
                    'old' : old_ip,
                    'new' : new_ip
                }
            } for old_ip, new_ip in ip_man
        ]
    }
    return cfg

def handle(ips_file, ips6_file, label_file, output):
    ips = extract(str(Path(ips_file)))
    dst, intr, src = prepare_background_ips(ips)
    ips = extract(str(Path(ips_file)))
    dst6, intr6, src6 = prepare_background_ips(ips)

    with Path(label_file).open() as _f:
        labels_yaml = yaml.load(_f.read())
    labels_ip = labels_yaml['ip']
    ip_map = build_map(labels_ip, dst, intr, src, dst6, intr6, src6)

    cfg = build_config('TODO')
    cfg['ip.map'] = ip_map

    with Path(output).open('w') as _f:
        _f.write(yaml.dump(cfg))

SRC = [
    ['18']
]

INTR = [

]

DST = [
    ['172']
]

handle(
    r"C:\Users\tomas.madeja\Desktop\ips.yaml",
    r"C:\Users\tomas.madeja\Desktop\ip6s.yaml",
    r"C:\Users\tomas.madeja\Downloads\normalized\round4\normalized\normalized_wannacry_ransomware.yaml",
    r"C:\Users\tomas.madeja\Downloads\normalized\round4\normalized\cfg_wannacry_ransomware.yaml"
)


