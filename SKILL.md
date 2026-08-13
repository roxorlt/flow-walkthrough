---
name: flow-walkthrough
description: 三栏流程联动原型——左侧流程图节点可点击，右侧同步展示对应原型页面，中间自动切换手机框/后台宽窗口。触发：流程联动原型、点流程节点看页面、评审演示页、需求走查 demo、过流程用的演示、流程图和原型联动、flow walkthrough。不适用：只要流程图（用 flow-canvas）、只要原型页面无流程联动诉求。
---

# flow-walkthrough 流程联动原型

把 flow-canvas 产出的流程图 SVG 和一组原型页面组装成单文件三栏联动 HTML：左侧可缩放拖拽的流程画布（点节点）、中间设备框（自动在手机框 / 后台宽窗口间切换）、右侧节点标注。用于需求评审时"过流程"演示。

## 输入（三档，按可得材料降级）

必需：flow-canvas 产出的 SVG（根元素须带 `data-flowspec="1"`；没有流程图时先调 flow-canvas 生成）。
页面来源按可得性取其一：

1. **调用方已有原型 HTML**：从中提取各页面/状态片段作为页面输入（最优）
2. **只有需求文档（PRD）**：按 PRD 的页面与状态描述，用默认灰度线框风格生成简易页面片段（可用模板内置的 `wt-titlebar / wt-body / wt-input / wt-btn / wt-card / wt-badge / wt-dimtext` 组件类）
3. **两者都没有**：生成中性占位页，仅演示联动骨架

## 执行流程

1. **自动做节点-页面关联**：读流程图节点（id 与文案）与页面材料，按语义匹配生成 walkmap JSON（契约见 `contract/walkmap-v1.md`：`pages` 页面清单含 frame 类型 phone/wide，`nodes` 为节点 → 页面 + 标注）。后台类节点（双边线灰底）映射到 `frame: "wide"` 的页面。
2. **产出关联确认表**：在生成最终页面前，把映射以 markdown 表格展示给用户确认——列：流程节点 / 匹配到的页面 / 匹配依据 / 置信度（低置信度行明确标注）。用户确认或修正后再进入下一步。**不要跳过这一步直接交付**。
3. **构建**：
   ```
   python3 scripts/build.py walkmap.json -o out.html
   python3 scripts/build.py walkmap.json --check     # 仅校验映射与契约
   ```
4. 构建器会校验：SVG 契约版本、页面文件存在、映射完整性（SVG 节点无映射 / 映射节点不在 SVG 都会警告）、产物无 emoji。有 error 必须修复；warning 逐条向用户说明。

## 样式

默认灰度线框（模板内置 CSS 变量）。调用方声明了自己的样式规范时，通过 walkmap 的 `css_vars` 覆盖（如 `{"--wt-accent": "#2f6fed"}`）；未声明则用默认。产物禁 emoji（构建器硬校验）。

## 页面内联动 API

页面片段内可调用 `goNode('节点id')` 驱动整体联动（如登录按钮点击后跳到下一个流程节点），实现"手机内按钮走通全流程"的演示效果。

## 环境降级

无 python3 时：参照 `templates/walkthrough.html` 手工完成占位符替换（`__TITLE__ / __SVG__ / __PAGES_PHONE__ / __PAGES_WIDE__ / __NODES_JSON__ / __PAGE_FRAME_JSON__ / __DEFAULT__ / __CSS_VARS__`），质量降级并告知用户（无自动校验）。

## 自检

安装后运行 `python3 scripts/selftest.py`（13 项断言，含 golden 走查构建、画布全屏与坏映射报错检查），全部 PASS 才算可用。
