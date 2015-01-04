"""General pytest template."""
import pytest

import hac.cli


class TestTemp:
    def test_basic_template(self):
        assert hac.cli.parser == []

    def test_basic_template_2(self):
        assert hac.cli.parser == []
