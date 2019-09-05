
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
