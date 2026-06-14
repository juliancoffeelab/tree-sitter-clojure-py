from __future__ import annotations

import shlex
import shutil
import subprocess
import sysconfig
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface  # type: ignore


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "custom"

    def initialize(self, _version: str, build_data: dict[str, object]) -> None:
        if self.target_name == "sdist":
            return

        output = self._build_extension()
        force_include = build_data.setdefault("force_include", {})
        if not isinstance(force_include, dict):
            raise TypeError("force_include build data must be a dict")
        force_include[str(output)] = f"tree_sitter_clojure/{output.name}"

    def clean(self, _versions: list[str]) -> None:
        package_dir = Path(self.root, "src", "tree_sitter_clojure")
        for built in package_dir.glob("_binding*.so"):
            built.unlink(missing_ok=True)
        shutil.rmtree(Path(self.root, "build"), ignore_errors=True)

    def _build_extension(self) -> Path:
        root = Path(self.root)
        native_dir = root / "src" / "tree_sitter_clojure" / "native"
        package_dir = root / "src" / "tree_sitter_clojure"
        build_dir = root / "build" / "native"
        build_dir.mkdir(parents=True, exist_ok=True)

        ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")
        include_py = sysconfig.get_config_var("INCLUDEPY")
        if not ext_suffix or not include_py:
            raise RuntimeError(
                "Python build configuration is missing EXT_SUFFIX or INCLUDEPY"
            )

        output = package_dir / f"_binding{ext_suffix}"
        sources = [native_dir / "binding.c", native_dir / "parser.c"]
        objects = []

        compiler = shlex.split(sysconfig.get_config_var("CC") or "cc")
        cflags = shlex.split(sysconfig.get_config_var("CFLAGS") or "")
        ccshared = shlex.split(sysconfig.get_config_var("CCSHARED") or "")
        include_flags = [f"-I{include_py}", f"-I{native_dir}"]

        for source in sources:
            obj = build_dir / f"{source.stem}.o"
            command = (
                compiler
                + cflags
                + ccshared
                + include_flags
                + ["-c", str(source), "-o", str(obj)]
            )
            subprocess.run(command, check=True, cwd=root)
            objects.append(obj)

        linker = shlex.split(sysconfig.get_config_var("LDSHARED") or "cc -shared")
        subprocess.run(
            linker + [str(obj) for obj in objects] + ["-o", str(output)],
            check=True,
            cwd=root,
        )
        return output


build_hook = CustomBuildHook


def get_build_hook() -> type[CustomBuildHook]:
    return CustomBuildHook
