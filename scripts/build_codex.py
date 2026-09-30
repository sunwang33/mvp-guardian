#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从根目录 SKILL.md（WorkBuddy 主本）生成 Codex 侧两份文件。

用法：
    python scripts/build_codex.py

生成：
    codex/SKILL.md   —— Codex 技能（frontmatter 用 Codex 规范：quoted description + metadata.short-description）
    codex/AGENTS.md  —— 项目级注入版（仅正文，无 frontmatter）

这样做的目的：Codex 两份文件永远由主本派生，杜绝手工同步造成的口径漂移。
注意：字符串一律用显式换行常量和列表 join，避免反斜杠转义被 shell/编辑器吃掉。
"""

import io
import os
import sys

NL = chr(10)

DESC = (
    '"MVP 开发守门员：在 vibe coding 过程中辅助并监督用户遵循 MVP 思路（新产品开发，也给已有产品加拓展功能）。'
    '触发：用户说「mvp」「mvp检查」「新功能」「开始开发」「做一个网站/工具/应用」，或对话出现明确开发意图。'
    'v2.1 硬门槛：阶段门禁链（三问 → mvp-plan 确认 → PRD 确认 → UI 结构确认 → 写码前检查清单），'
    '任何一道未过禁止写生产代码；计划落盘到项目根目录 mvp-plan.md 并维护阶段状态机；'
    '需求模糊时进入 grill 式追问；已有产品的小功能可走增量简化流程。"'
)

SHORT_DESC = '"辅助并监督 vibe coding 遵循 MVP 思路"'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    main_path = os.path.join(ROOT, 'SKILL.md')
    text = io.open(main_path, encoding='utf-8').read()

    # 拆分 frontmatter 与正文（主本前 5 行是 frontmatter）
    parts = text.split('---' + NL, 2)
    if len(parts) < 3:
        sys.exit('错误：SKILL.md 未找到合法的 frontmatter 分隔符')
    body = parts[2]

    # 正文改为「守门员规则」口吻（Codex / AGENTS.md 场景）
    body = body.replace(
        '# MVP Guardian（MVP 守门员）v2.1',
        '# MVP 守门员（MVP Guardian）v2.1',
        1)
    body = body.replace(
        '本 skill 是 vibe coding 时的 MVP 辅助与监督员，核心信念来自实践总结：',
        '在 vibe coding 过程中遵循以下 MVP 守门员规则。适用于新产品开发，也适用于给已有产品加拓展功能。核心信念：',
        1)

    fm_lines = [
        '---',
        'name: mvp-guardian',
        'description: ' + DESC,
        'metadata:',
        '  short-description: ' + SHORT_DESC,
        '---',
        '',
        '',
    ]
    codex_skill = NL.join(fm_lines) + body

    os.makedirs(os.path.join(ROOT, 'codex'), exist_ok=True)
    io.open(os.path.join(ROOT, 'codex', 'SKILL.md'), 'w',
            encoding='utf-8', newline=NL).write(codex_skill)
    io.open(os.path.join(ROOT, 'codex', 'AGENTS.md'), 'w',
            encoding='utf-8', newline=NL).write(body)

    # 自检：frontmatter 结构是否正常（防止再次出现字面量换行）
    lines = codex_skill.splitlines()
    assert lines[0] == '---' and lines[5] == '---', 'frontmatter 结构异常'
    assert lines[3] == 'metadata:' and lines[4].startswith('  short-description:'), \
        'metadata 区块异常：' + repr(lines[3:5])
    for i, line in enumerate(lines[:8], 1):
        assert NL not in line and '/n' not in line, '第 %d 行含异常换行字面量' % i

    print('已生成 codex/SKILL.md（%d 行）与 codex/AGENTS.md（%d 行）'
          % (len(codex_skill.splitlines()), len(body.splitlines())))
    print('frontmatter 自检通过')


if __name__ == '__main__':
    main()
