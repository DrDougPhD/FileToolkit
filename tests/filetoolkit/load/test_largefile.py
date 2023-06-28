def test_import():
    from filetoolkit import load
    assert callable(load.readlargefile)
