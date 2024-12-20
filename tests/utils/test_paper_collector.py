import datetime
from unittest.mock import MagicMock, patch

from research_town.utils.paper_collector import (
    get_paper_by_arxiv_id,
    get_paper_content_from_html,
    get_paper_introduction,
    get_recent_papers,
    get_references,
    get_related_papers,
)


@patch('arxiv.Client')
def test_get_recent_paper(mock_client: MagicMock) -> None:
    # Create mock client instance and configure mock papers
    mock_client_instance = MagicMock()
    mock_client.return_value = mock_client_instance

    # Mock paper data
    mock_paper_1 = MagicMock()
    mock_paper_1.title = 'Paper 1'
    mock_paper_1.entry_id = 'http://example.com/1'
    mock_paper_1.summary = 'Summary 1'
    mock_paper_1.primary_category = 'cs'
    mock_paper_1.published = datetime.datetime(2023, 7, 1)

    mock_paper_2 = MagicMock()
    mock_paper_2.title = 'Paper 2'
    mock_paper_2.entry_id = 'http://example.com/2'
    mock_paper_2.summary = 'Summary 2'
    mock_paper_2.primary_category = 'cs'
    mock_paper_2.published = datetime.datetime(2023, 7, 2)

    # Set return value for client.results
    mock_client_instance.results.return_value = [mock_paper_1, mock_paper_2]

    # Call the function you're testing
    result_papers = get_recent_papers(max_results=2, domain='cs.AI')

    # Assertions
    assert len(result_papers) == 2
    assert result_papers[0].title == 'Paper 1'
    assert result_papers[1].title == 'Paper 2'
    assert result_papers[0].url == 'http://example.com/1'
    assert result_papers[1].url == 'http://example.com/2'

    # Check if mock client was called
    mock_client.assert_called_once()


@patch('arxiv.Client')
def test_get_related_papers(mock_client: MagicMock) -> None:
    # Create mock client instance and configure mock papers
    mock_client_instance = MagicMock()
    mock_client.return_value = mock_client_instance

    # Mock paper data
    mock_paper_1 = MagicMock()
    mock_paper_1.title = 'Paper 1'
    mock_paper_1.entry_id = 'http://example.com/1'
    mock_paper_1.summary = 'Summary 1'
    mock_paper_1.primary_category = 'cs'
    mock_paper_1.published = datetime.datetime(2023, 7, 1)

    mock_paper_2 = MagicMock()
    mock_paper_2.title = 'Paper 2'
    mock_paper_2.entry_id = 'http://example.com/2'
    mock_paper_2.summary = 'Summary 2'
    mock_paper_2.primary_category = 'cs'
    mock_paper_2.published = datetime.datetime(2023, 7, 2)

    # Set return value for client.results
    mock_client_instance.results.return_value = [mock_paper_1, mock_paper_2]

    # Call the function you're testing
    result_papers = get_related_papers(num_results=2, query='test', domain='cs.AI')

    # Assertions
    assert len(result_papers) == 2
    assert result_papers[0].title == 'Paper 1'
    assert result_papers[1].title == 'Paper 2'
    assert result_papers[0].url == 'http://example.com/1'
    assert result_papers[1].url == 'http://example.com/2'

    # Check if mock client was called
    mock_client.assert_called_once()


def test_get_paper_content_from_html() -> None:
    sections = get_paper_content_from_html('https://arxiv.org/html/2403.05534v1')
    assert sections is not None
    assert '1 Introduction' in sections
    assert len(sections['1 Introduction']) > 0


def test_get_paper_introduction() -> None:
    test_url1 = 'https://arxiv.org/pdf/2409.16928'
    test_url2 = 'https://openreview.net/pdf?id=NnMEadcdyD'
    test_url3 = 'https://arxiv.org/abs/2409.17012'
    intro1 = get_paper_introduction(test_url1)
    intro2 = get_paper_introduction(test_url2)
    intro3 = get_paper_introduction(test_url3)
    assert intro1 is not None
    assert intro2 is not None
    assert intro3 is not None

    assert 'Introduction' in intro1
    assert 'Introduction' in intro2
    assert 'Introduction' in intro3


def test_get_paper_by_arxiv_id() -> None:
    result = get_paper_by_arxiv_id('2409.16928')
    assert result is not None


@patch('requests.get')
def test_get_references(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': [
            {'citedPaper': {'arxiv_id': '1234.5678', 'title': 'Cited Paper 1'}},
            {'citedPaper': {'arxiv_id': '2345.6789', 'title': 'Cited Paper 2'}},
        ]
    }
    mock_get.return_value = mock_response

    # Call the function
    references = get_references('1234.5678')

    # Assertions
    assert len(references) == 2
    assert references[0]['title'] == 'Cited Paper 1'
    assert references[1]['title'] == 'Cited Paper 2'
    mock_get.assert_called_once()
