"""Performance benchmarks for output format plugins.

These benchmarks measure the generation speed of each plugin
with various link list sizes to track performance regressions.
"""

import pytest

from minibook.plugins import (
    AsciiDocPlugin,
    HTMLPlugin,
    JSONPlugin,
    MarkdownPlugin,
    RSTPlugin,
)


class TestPluginBenchmarks:
    """Performance benchmarks for all output format plugins."""

    @pytest.mark.parametrize(
        "plugin_info",
        [
            (HTMLPlugin, "html"),
            (MarkdownPlugin, "md"),
            (JSONPlugin, "json"),
            (RSTPlugin, "rst"),
            (AsciiDocPlugin, "adoc"),
        ],
    )
    @pytest.mark.parametrize(
        "link_fixture",
        ["small_link_list", "medium_link_list", "large_link_list", "extra_large_link_list"],
    )
    def test_generation(self, benchmark, tmp_path, plugin_info, link_fixture, request):
        """Benchmark plugin generation with varying link list sizes."""
        plugin_class, extension = plugin_info
        plugin = plugin_class()
        output_file = tmp_path / f"output.{extension}"
        links = request.getfixturevalue(link_fixture)

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=links,
            output_file=output_file,
        )
