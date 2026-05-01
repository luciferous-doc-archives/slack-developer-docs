import pytest

from utils.path import url_to_file_path


class TestUrlToFilePath:
    """url_to_file_path() 関数の単体テスト"""

    @pytest.mark.parametrize(
        "url,all_urls,expected",
        [
            # シナリオ1: 単一ファイル（プレフィックスなし）
            (
                "/api.md",
                ["/api.md"],
                "api.md",
            ),
            (
                "/guide.md",
                ["/guide.md"],
                "guide.md",
            ),
            # シナリオ2: ディレクトリ化（プレフィックスあり）
            (
                "/api/v1.md",
                ["/api/v1.md", "/api/v1/methods.md"],
                "api/v1/index.md",
            ),
            (
                "/guide/python.md",
                ["/guide/python.md", "/guide/python/setup.md"],
                "guide/python/index.md",
            ),
            # シナリオ3: ルート直下の `.md`
            (
                "/setup.md",
                ["/setup.md"],
                "setup.md",
            ),
            # シナリオ4: プレフィックス部分一致なし
            (
                "/api.md",
                ["/api.md", "/api2.md"],
                "api.md",
            ),
            # シナリオ5: 深いパス階層
            (
                "/a/b/c/d.md",
                ["/a/b/c/d.md", "/a/b/c/d/e.md"],
                "a/b/c/d/index.md",
            ),
            # シナリオ6: 複数の `.md` ファイル混在
            (
                "/guide/python.md",
                ["/guide.md", "/guide/python.md", "/guide/python/setup.md"],
                "guide/python/index.md",
            ),
            # シナリオ7: `.md` ファイルが複数存在するが、プレフィックスは異なる
            (
                "/api.md",
                ["/api.md", "/guide.md"],
                "api.md",
            ),
            # シナリオ8: 同じステムを持つ複数のファイルがある場合
            (
                "/docs/reference.md",
                ["/docs/reference.md", "/docs/reference/api.md", "/docs/reference/cli.md"],
                "docs/reference/index.md",
            ),
        ],
        ids=[
            "single_file_no_prefix",
            "single_file_guide",
            "directory_api_v1",
            "directory_guide_python",
            "root_level_md",
            "partial_match_no_prefix",
            "deep_path_hierarchy",
            "multiple_md_files_mixed",
            "different_prefixes",
            "multiple_files_same_stem",
        ],
    )
    def test_url_to_file_path(self, url: str, all_urls: list[str], expected: str):
        """url_to_file_path() の各シナリオをテスト"""
        result = url_to_file_path(url=url, all_urls=all_urls)
        assert result == expected
