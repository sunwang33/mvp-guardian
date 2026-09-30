#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从根目录 SKILL.md（WorkBuddy 主本）生成 Codex 侧两份文件。

用法：
    python scripts/build_codex.py

生成：
    codex/SKILL.md   —— Codex 技能（frontmatter 用 Codex 规范：quoted description + metadata.short-description）
    codex/AGENTS.md  —— 项目级注入版（仅正文，无 frontmatter）

这样做的目的：Codex 两份文件永远由主本派生，杜绝手工同步造成的口径漂移。
版本号与描述**直接从主本 frontmatter 读取**——升版本时不需要改本脚本。

注意：字符串一律用显式换行常量和列表 join，避免反斜杠转义被 shell/编辑器吃掉。
"""

import io
import os
import sys

NL = chr(10)
SHORT_DESC = '"辅助并监督 vibe coding 遵循 MVP 思路"'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_main(path):
    """读取主本，返回 (description, body)。"""
    text = io.open(path, encoding='utf-8').read()
    parts = text.split('---' + NL, 2)
    if len(parts) < 3:
        sys.exit('错误：SKILL.md 未找到合法的 frontmatter 分隔符')
    frontmatter, body = parts[1], parts[2]

    desc = None
    for line in frontmatter.splitlines():
        if line.startswith('description:'):
            desc = line[len('description:'):].strip()
            break
    if not desc:
        sys.exit('错误：主本 frontmatter 缺少 description')
    if '"' in desc:
        sys.exit('错误：description 含双引号，无法直接用作 Codex 规范里的 quoted description')
    return desc, body


def to_codex_body(body):
    """把 WorkBuddy 主本正文改写成 Codex / AGENTS.md 口吻（只动标题与首句）。"""
    body = body.replace(
        '# MVP Guardian（MVP 守门员）',
        '# MVP 守门员（MVP Guardian）',
        1)
    body = body.replace(
        '本 skill 是 vibe coding 时的 MVP 辅助与监督员，核心信念来自实践总结：',
        '在 vibe coding 过程中遵循以下 MVP 守门员规则。适用于新产品开发，也适用于给已有产品加拓展功能。核心信念：',
        1)
    return body


def main():
    main_path = os.path.join(ROOT, 'SKILL.md')
    desc, body = read_main(main_path)
    body = to_codex_body(body)

    fm_lines = [
        '---',
        'name: mvp-guardian',
        'description: "' + desc + '"',
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

    # 自检：标题口吻已切换
    assert '# MVP 守门员（MVP Guardian）' in codex_skill, '正文标题未切换为 Codex 口吻'

    title = ''
    for line in lines:
        if line.startswith('# MVP 守门员（MVP Guardian）'):
            title = line
            break
    print('已生成 codex/SKILL.md（%d 行）与 codex/AGENTS.md（%d 行）'
          % (len(codex_skill.splitlines()), len(body.splitlines())))
    print('主本标题：%s' % (title or '(未识别)'))
    print('frontmatter 自检通过')


if __name__ == '__main__':
    main()
