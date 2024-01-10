from core.utils.searcher import Searcher


def test_search():
    searcher = Searcher()
    results = searcher.search('SSIS 337')
    print(results)
    assert not results
