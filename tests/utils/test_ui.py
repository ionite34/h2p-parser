import pytest
import pytest_mock
from unittest import mock
from unittest.mock import patch
from h2p_parser.utils.ui import *


@pytest.fixture(scope='function')
def mock_inq(request):
    method = request.param[0]
    result = request.param[1]
    mock_method = mock.MagicMock()
    mock_method().execute.return_value = result
    with patch(f'h2p_parser.utils.ui.inquirer.{method}', mock_method):
        yield mock_method


@pytest.mark.parametrize('mock_inq', [('checkbox', 'use-cache')], indirect=True)
def test_prompt_parsing_choices(mock_inq):
    with mock_inq:
        result = prompt_parsing_choices()
        assert result == 'use-cache'


@pytest.mark.parametrize('mock_inq', [['select', None]], indirect=True)
def test_menu_main_exit(mock_inq):
    with mock_inq:
        # This should exit with code 0
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            menu_main()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0
