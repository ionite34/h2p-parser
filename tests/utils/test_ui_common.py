import pytest
import pytest_mock
from unittest import mock
from unittest.mock import patch
from h2p_parser.utils.ui_common import *


@pytest.fixture
def mock_inq(request):
    method = request.param[0]
    result = request.param[1]
    mock_method = mock.MagicMock()
    mock_method().execute.return_value = result
    with patch(f'h2p_parser.utils.ui_common.inquirer.{method}', mock_method):
        yield mock_method


# Test prompt directory input
@pytest.mark.parametrize('mock_inq', [['filepath', "path/to/dir"]], indirect=True)
def test_prompt_d_input(mock_inq):
    with mock_inq:
        result = prompt_d_input()
        assert result == "path/to/dir"


# Test prompt file input
@pytest.mark.parametrize('mock_inq', [['filepath', "path/to/file"]], indirect=True)
def test_prompt_f_input(mock_inq):
    with mock_inq:
        result = prompt_f_input()
        assert result == "path/to/file"


# Test prompt file output
@pytest.mark.parametrize('mock_inq', [['filepath', "path/to/file"]], indirect=True)
def test_prompt_f_output(mock_inq):
    with mock_inq:
        result = prompt_f_output()
        assert result == "path/to/file"


def test_pr_sep():
    with patch('h2p_parser.utils.ui_common.cp') as mock_cp:
        pr_sep()
        mock_cp.assert_called_once()
