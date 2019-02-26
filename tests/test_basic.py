alignment_file = 'PF17947.sto'


def tests_dir():
    """Return None is no tests dir."""
    import os
    cwd = os.getcwd()
    basename = os.path.basename(cwd)
    if basename == 'tests':
        return cwd
    else:
        tests_dir = os.path.join(cwd, 'tests')
        if os.path.exists(tests_dir):
            return tests_dir


def test_pcdhit():
    import os
    import lilbio
    import pcdhit
    from lilbio.funcs import uppercase_only
    source = os.path.join(tests_dir(), alignment_file)
    records = lilbio.parse(source, 'stockholm', func=uppercase_only)
    filtered_records = pcdhit.filter(records, 0.7)
    assert len(list(filtered_records)) == 61
