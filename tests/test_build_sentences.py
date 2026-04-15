import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from build_sentences import *

def test_build_sentence():
    result = build_sentence("Hello", "world")
    assert result == "Hello world"

def test_capitalize_sentence():
    result = capitalize_sentence("hello world")
    assert result == "Hello world"

def test_add_period():
    result = add_period("Hello world")
    assert result == "Hello world."

def test_add_period_already_has_period():
    result = add_period("Hello world.")
    assert result == "Hello world."

def test_capitalize_sentence_empty():
    result = capitalize_sentence("")
    assert result == ""

def test_full_sentence():
    result = build_full_sentence("hello", "world")
    assert result == "Hello world."
