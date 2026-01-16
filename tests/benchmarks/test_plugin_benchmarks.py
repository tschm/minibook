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


class TestHTMLPluginBenchmarks:
    """Benchmarks for HTML plugin generation."""

    def test_html_small(self, benchmark, temp_output_dir, small_link_list):
        """Benchmark HTML generation with 10 links."""
        plugin = HTMLPlugin()
        output_file = temp_output_dir / "output.html"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=small_link_list,
            output_file=output_file,
        )

    def test_html_medium(self, benchmark, temp_output_dir, medium_link_list):
        """Benchmark HTML generation with 50 links."""
        plugin = HTMLPlugin()
        output_file = temp_output_dir / "output.html"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=medium_link_list,
            output_file=output_file,
        )

    def test_html_large(self, benchmark, temp_output_dir, large_link_list):
        """Benchmark HTML generation with 200 links."""
        plugin = HTMLPlugin()
        output_file = temp_output_dir / "output.html"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=large_link_list,
            output_file=output_file,
        )


class TestMarkdownPluginBenchmarks:
    """Benchmarks for Markdown plugin generation."""

    def test_markdown_small(self, benchmark, temp_output_dir, small_link_list):
        """Benchmark Markdown generation with 10 links."""
        plugin = MarkdownPlugin()
        output_file = temp_output_dir / "output.md"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=small_link_list,
            output_file=output_file,
        )

    def test_markdown_medium(self, benchmark, temp_output_dir, medium_link_list):
        """Benchmark Markdown generation with 50 links."""
        plugin = MarkdownPlugin()
        output_file = temp_output_dir / "output.md"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=medium_link_list,
            output_file=output_file,
        )

    def test_markdown_large(self, benchmark, temp_output_dir, large_link_list):
        """Benchmark Markdown generation with 200 links."""
        plugin = MarkdownPlugin()
        output_file = temp_output_dir / "output.md"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=large_link_list,
            output_file=output_file,
        )


class TestJSONPluginBenchmarks:
    """Benchmarks for JSON plugin generation."""

    def test_json_small(self, benchmark, temp_output_dir, small_link_list):
        """Benchmark JSON generation with 10 links."""
        plugin = JSONPlugin()
        output_file = temp_output_dir / "output.json"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=small_link_list,
            output_file=output_file,
        )

    def test_json_medium(self, benchmark, temp_output_dir, medium_link_list):
        """Benchmark JSON generation with 50 links."""
        plugin = JSONPlugin()
        output_file = temp_output_dir / "output.json"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=medium_link_list,
            output_file=output_file,
        )

    def test_json_large(self, benchmark, temp_output_dir, large_link_list):
        """Benchmark JSON generation with 200 links."""
        plugin = JSONPlugin()
        output_file = temp_output_dir / "output.json"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=large_link_list,
            output_file=output_file,
        )


class TestRSTPluginBenchmarks:
    """Benchmarks for RST plugin generation."""

    def test_rst_small(self, benchmark, temp_output_dir, small_link_list):
        """Benchmark RST generation with 10 links."""
        plugin = RSTPlugin()
        output_file = temp_output_dir / "output.rst"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=small_link_list,
            output_file=output_file,
        )

    def test_rst_medium(self, benchmark, temp_output_dir, medium_link_list):
        """Benchmark RST generation with 50 links."""
        plugin = RSTPlugin()
        output_file = temp_output_dir / "output.rst"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=medium_link_list,
            output_file=output_file,
        )

    def test_rst_large(self, benchmark, temp_output_dir, large_link_list):
        """Benchmark RST generation with 200 links."""
        plugin = RSTPlugin()
        output_file = temp_output_dir / "output.rst"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=large_link_list,
            output_file=output_file,
        )


class TestAsciiDocPluginBenchmarks:
    """Benchmarks for AsciiDoc plugin generation."""

    def test_asciidoc_small(self, benchmark, temp_output_dir, small_link_list):
        """Benchmark AsciiDoc generation with 10 links."""
        plugin = AsciiDocPlugin()
        output_file = temp_output_dir / "output.adoc"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=small_link_list,
            output_file=output_file,
        )

    def test_asciidoc_medium(self, benchmark, temp_output_dir, medium_link_list):
        """Benchmark AsciiDoc generation with 50 links."""
        plugin = AsciiDocPlugin()
        output_file = temp_output_dir / "output.adoc"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=medium_link_list,
            output_file=output_file,
        )

    def test_asciidoc_large(self, benchmark, temp_output_dir, large_link_list):
        """Benchmark AsciiDoc generation with 200 links."""
        plugin = AsciiDocPlugin()
        output_file = temp_output_dir / "output.adoc"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=large_link_list,
            output_file=output_file,
        )


class TestScalabilityBenchmarks:
    """Benchmarks for testing scalability with extra large datasets."""

    def test_markdown_extra_large(self, benchmark, temp_output_dir, extra_large_link_list):
        """Benchmark Markdown generation with 500 links."""
        plugin = MarkdownPlugin()
        output_file = temp_output_dir / "output.md"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=extra_large_link_list,
            output_file=output_file,
        )

    def test_json_extra_large(self, benchmark, temp_output_dir, extra_large_link_list):
        """Benchmark JSON generation with 500 links."""
        plugin = JSONPlugin()
        output_file = temp_output_dir / "output.json"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=extra_large_link_list,
            output_file=output_file,
        )

    def test_rst_extra_large(self, benchmark, temp_output_dir, extra_large_link_list):
        """Benchmark RST generation with 500 links."""
        plugin = RSTPlugin()
        output_file = temp_output_dir / "output.rst"

        benchmark(
            plugin.generate,
            title="Benchmark Test",
            links=extra_large_link_list,
            output_file=output_file,
        )
