#!/usr/bin/env bash
# MVP Guardian 一键部署脚本
# 把本仓库的技能文件部署到本机已安装的 AI 工具技能目录。
#
# 用法：
#   bash scripts/deploy.sh          # 实际部署
#   bash scripts/deploy.sh --dry    # 演练，只打印不写入
#
# 设计原则：仓库是唯一真源，本脚本只做「仓库 -> 本机」单向同步，永不反向写回。

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY=0
[[ "${1:-}" == "--dry" ]] && DRY=1

run() {
  if [[ $DRY -eq 1 ]]; then
    echo "  [dry] $*"
  else
    eval "$@"
  fi
}

echo "仓库目录: $REPO_DIR"
[[ $DRY -eq 1 ]] && echo "模式: 演练（不会写入任何文件）"
echo

# ---------- WorkBuddy ----------
WB_SKILLS="${HOME}/.workbuddy/skills"
if [[ -d "${HOME}/.workbuddy" ]]; then
  echo "[1/4] WorkBuddy 技能 -> ${WB_SKILLS}/mvp-guardian"
  run "mkdir -p '${WB_SKILLS}/mvp-guardian/references'"
  run "cp '${REPO_DIR}/SKILL.md' '${WB_SKILLS}/mvp-guardian/SKILL.md'"
  run "cp '${REPO_DIR}/references/mvp-principles.md' '${WB_SKILLS}/mvp-guardian/references/mvp-principles.md'"
else
  echo "[1/4] 跳过 WorkBuddy（未检测到 ~/.workbuddy 目录）"
fi

# ---------- Codex ----------
CX_SKILLS="${HOME}/.codex/skills/mvp-guardian"
CX_PROMPTS="${HOME}/.codex/prompts"
if [[ -d "${HOME}/.codex" ]]; then
  echo "[2/4] Codex 技能 -> ${CX_SKILLS}"
  run "mkdir -p '${CX_SKILLS}/references' '${CX_SKILLS}/agents'"
  run "cp '${REPO_DIR}/codex/SKILL.md' '${CX_SKILLS}/SKILL.md'"
  run "cp '${REPO_DIR}/references/mvp-principles.md' '${CX_SKILLS}/references/mvp-principles.md'"
  run "cp '${REPO_DIR}/codex/agents/openai.yaml' '${CX_SKILLS}/agents/openai.yaml'"

  echo "[3/4] Codex /mvp 命令 -> ${CX_PROMPTS}/mvp.md"
  run "mkdir -p '${CX_PROMPTS}'"
  run "cp '${REPO_DIR}/codex/prompts/mvp.md' '${CX_PROMPTS}/mvp.md'"
else
  echo "[2/4] 跳过 Codex（未检测到 ~/.codex 目录）"
  echo "[3/4] 跳过 Codex 命令"
fi

# ---------- 校验 ----------
echo "[4/4] 校验部署结果"
if [[ $DRY -eq 0 ]]; then
  ok=0
  for f in "${WB_SKILLS}/mvp-guardian/SKILL.md" \
           "${CX_SKILLS}/SKILL.md" \
           "${CX_PROMPTS}/mvp.md"; do
    if [[ -f "$f" ]]; then
      echo "  OK   $f"
      ok=$((ok + 1))
    else
      echo "  MISS $f"
    fi
  done
  echo "  已部署 ${ok} 个文件"
else
  echo "  [dry] 跳过校验"
fi

echo
echo "完成。触发热词：mvp / 启动mvp / mvp检查 / 新功能 / 开始开发；Codex 中可用 /mvp。"
