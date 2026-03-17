import argparse
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Commit:
    date: str
    sha: str
    subject: str
    files: List[str]


AREA_RULES: List[Tuple[str, str]] = [
    ("bioinformatics-analysis/sample/", "样本"),
    ("bioinformatics-analysis/patient/", "患者"),
    ("bioinformatics-analysis/task/", "任务"),
    ("bioinformatics-analysis/cohort/", "队列分析"),
    ("bioinformatics-analysis/reference_genome/", "参考基因组"),
    ("bioinformatics-analysis/flow/", "流程"),
    ("bioinformatics-analysis/middlewares/", "中间件/安全"),
    ("bioinformatics-analysis/bioinformatics/settings/", "配置/环境"),
    ("bioinformatics-analysis/docs/db/", "数据库脚本"),
    ("bioinformatics-analysis/docs/", "文档"),
    ("bioinformatics-analysis/", "后端主体"),
    ("init/", "初始化/部署"),
]


def run_git(repo: str, args: List[str]) -> str:
    p = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if p.returncode != 0:
        msg = (p.stderr or p.stdout or "").strip()
        raise SystemExit(f"git 执行失败：{' '.join(args)}\n{msg}")
    return p.stdout


def classify_area(path: str) -> str:
    for prefix, area in AREA_RULES:
        if path.startswith(prefix):
            return area
    return "其他"


def parse_log_numstat(raw: str) -> List[Commit]:
    rs = "\x1e"
    fs = "\x1f"
    commits: List[Commit] = []
    for block in raw.split(rs):
        block = block.strip("\n")
        if not block:
            continue
        lines = block.splitlines()
        header = lines[0]
        parts = header.split(fs)
        if len(parts) < 3:
            continue
        date, sha, subject = parts[0].strip(), parts[1].strip(), parts[2].strip()
        files: List[str] = []
        for ln in lines[1:]:
            ln = ln.strip()
            if not ln:
                continue
            cols = ln.split("\t")
            if len(cols) >= 3:
                files.append(cols[2])
        commits.append(Commit(date=date, sha=sha, subject=subject, files=sorted(set(files))))
    return commits


def commit_type(subject: str) -> str:
    s = subject.strip().lower()
    for t in ("feat", "fix", "refactor", "perf", "build", "chore", "docs", "test"):
        if s.startswith(f"{t}:") or s.startswith(f"{t}("):
            return t
    return "other"


def to_markdown(
    commits: List[Commit],
    since: str,
    until: Optional[str],
    branch: str,
) -> str:
    by_area: Dict[str, List[Commit]] = defaultdict(list)
    file_counter = Counter()
    area_counter = Counter()
    type_counter = Counter()

    db_files = set()
    migration_files = set()
    api_touch = set()

    for c in commits:
        type_counter[commit_type(c.subject)] += 1

        touched_areas = set()
        for f in c.files:
            file_counter[f] += 1
            area = classify_area(f)
            touched_areas.add(area)

            if f.startswith("bioinformatics-analysis/docs/db/") and f.endswith(".sql"):
                db_files.add(f)
            if "/migrations/" in f and f.endswith(".py"):
                migration_files.add(f)
            if f.endswith(("urls.py", "views.py", "serializers.py")):
                api_touch.add(f)

        if not touched_areas:
            by_area["其他"].append(c)
            area_counter["其他"] += 1
        else:
            for a in sorted(touched_areas):
                by_area[a].append(c)
                area_counter[a] += 1

    lines: List[str] = []
    lines.append("# 需求/变更汇总（按 Git 提交提取）")
    lines.append("")
    lines.append(f"- 分支/引用：`{branch}`")
    lines.append(f"- 时间范围：`{since}` ~ `{until or 'now'}`")
    lines.append(f"- 提交数：{len(commits)}")
    lines.append("")

    lines.append("## 概览")
    lines.append("")
    lines.append("- 按模块（提交触达次数，1 个提交可能计入多个模块）：")
    for area, cnt in area_counter.most_common():
        lines.append(f"  - {area}: {cnt}")
    lines.append("- 按类型（基于 Conventional Commit 前缀粗分）：")
    for t, cnt in type_counter.most_common():
        lines.append(f"  - {t}: {cnt}")
    lines.append("")

    if db_files or migration_files:
        lines.append("## 数据库相关")
        lines.append("")
        if migration_files:
            lines.append("- 迁移文件：")
            for f in sorted(migration_files):
                lines.append(f"  - {f}")
        if db_files:
            lines.append("- SQL 脚本：")
            for f in sorted(db_files):
                lines.append(f"  - {f}")
        lines.append("")

    if api_touch:
        lines.append("## 可能涉及接口/行为变更的文件（需人工确认）")
        lines.append("")
        for f in sorted(api_touch):
            lines.append(f"- {f}")
        lines.append("")

    lines.append("## 按模块明细")
    lines.append("")
    for area in sorted(by_area.keys()):
        lines.append(f"### {area}")
        lines.append("")
        for c in sorted(by_area[area], key=lambda x: (x.date, x.sha)):
            lines.append(f"- {c.date} {c.sha} {c.subject}")
        lines.append("")

    lines.append("## Top 变更文件（按提交触达次数）")
    lines.append("")
    for f, cnt in file_counter.most_common(30):
        lines.append(f"- {cnt} {f}")
    lines.append("")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", help="仓库路径（默认当前目录）")
    ap.add_argument("--branch", default="HEAD", help="分支/引用（默认 HEAD）")
    ap.add_argument("--since", default="2025-12-01", help="起始日期（YYYY-MM-DD）")
    ap.add_argument("--until", default=None, help="结束日期（YYYY-MM-DD，可选）")
    ap.add_argument("--out", default=None, help="输出 Markdown 文件路径（可选）")
    args = ap.parse_args()

    fmt = "%x1e%ad%x1f%h%x1f%s"
    git_args = [
        "log",
        args.branch,
        f"--since={args.since}",
        "--date=short",
        f"--pretty=format:{fmt}",
        "--numstat",
        "--no-merges",
    ]
    if args.until:
        git_args.insert(2, f"--until={args.until}")

    raw = run_git(args.repo, git_args)
    commits = parse_log_numstat(raw)
    md = to_markdown(commits, args.since, args.until, args.branch)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
        print(args.out)
    else:
        print(md)


if __name__ == "__main__":
    main()

