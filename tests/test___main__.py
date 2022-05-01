import pytest
import pytest_mock
from unittest import mock
from unittest.mock import patch
from h2p_parser import __main__ as main


@pytest.fixture
def mock_inq(request):
    method = request.param[0]
    result = request.param[1]
    mock_method = mock.MagicMock()
    mock_method().execute.return_value = result
    with patch(f'h2p_parser.__main__.inquirer.{method}', mock_method):
        yield mock_method


# Test prompt_action()
@pytest.mark.parametrize('mock_inq', [['select', 'Convert']], indirect=True)
def test_prompt_action(mock_inq):
    with mock_inq:
        result = main.prompt_action()
        assert result == 'Convert'


# Test prompt_action() exit mode
@pytest.mark.parametrize('mock_inq', [['select', None]], indirect=True)
def test_prompt_action_exit(mock_inq):
    with mock_inq:
        # This should exit with code 0
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main.prompt_action()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0


# Test prompt file input
@pytest.mark.parametrize('mock_inq', [['filepath', "path/to/file"]], indirect=True)
def test_prompt_f_input(mock_inq):
    with mock_inq:
        result = main.prompt_f_input()
        assert result == "path/to/file"


# Test prompt file input
@pytest.mark.parametrize('mock_inq', [['filepath', "path/to/file"]], indirect=True)
def test_prompt_f_output(mock_inq):
    with mock_inq:
        result = main.prompt_f_output()
        assert result == "path/to/file"


@pytest.mark.parametrize('arg_in, arg_out, arg_delim, expected', [
    (None, None, None, None),
    ('path', None, None, None),
    ('path', 'path', None, None),
    ('path', 'path', '|', None),
])
def test_action_convert(mocker, arg_in, arg_out, arg_delim, expected):
    mock_text = mock.MagicMock()
    mock_text().execute.return_value = arg_delim
    with patch('h2p_parser.__main__.prompt_f_input', return_value=arg_in) as mock_f_input:
        with patch('h2p_parser.__main__.prompt_f_output', return_value=arg_out) as mock_f_output:
            with patch('h2p_parser.__main__.inquirer.text', mock_text):
                with patch('h2p_parser.__main__.convert_h2p') as mock_conv:
                    assert main.action_convert() == expected
                    if arg_in is None:
                        assert mock_f_input.call_count == 1
                        assert mock_f_output.call_count + mock_text().execute.call_count == 0
                    elif arg_out is None:
                        assert mock_f_input.call_count == 1
                        assert mock_f_output.call_count == 1
                        assert mock_text().execute.call_count == 0
                    elif arg_delim is None:
                        assert mock_f_input.call_count == 1
                        assert mock_f_output.call_count == 1
                        assert mock_text().execute.call_count == 1
                    else:
                        assert mock_f_input.call_count == 1
                        assert mock_f_output.call_count == 1
                        assert mock_text().execute.call_count == 1
                        assert mock_conv.call_count == 1


def test_convert_h2p():
    with patch('h2p_parser.__main__.converter.bin_delim_to_json') as mock_conv:
        main.convert_h2p("path/to/file", "path/to/file", "|")
        assert mock_conv.call_count == 1
