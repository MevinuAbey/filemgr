import pytest
from pathlib import Path
from project import check_path, check_action, parse_arguments

def test_check_path(tmp_path):
    # Test when path is a valid existing directory
    assert check_path(tmp_path) == True
    
    # Test when path doesn't exist
    fake_path = tmp_path / "fake_folder"
    assert check_path(fake_path) == False
    
    # Test when None return false
    assert check_path(None) == False
    
    # Test when the path to a file instead of a directory
    mock_file = tmp_path / "test.txt"
    mock_file.touch()
    assert check_path(mock_file) == False

def test_check_action():
    # test check_action function correctly returns the action if it is provided with action
    assert check_action("backup") == "backup"
    assert check_action("organize") == "organize"
    assert check_action("rename") == "rename"

def test_parse_arguments(monkeypatch):
    # Test with arguments
    test_args = ['project.py', '-p', 'my_test_folder', '-a', 'backup']
    monkeypatch.setattr('sys.argv', test_args)

    path, action = parse_arguments()
    assert str(path) == 'my_test_folder'
    assert action == 'backup'

    # Test without arguments
    blank_args = ['project.py']
    monkeypatch.setattr('sys.argv', blank_args)

    path, action = parse_arguments()
    assert path is None
    assert action is None
