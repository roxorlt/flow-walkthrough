# walkmap/1 契约

flow-walkthrough 的输入格式。上游依赖 flow-canvas 的 flowspec/1 SVG 契约（`data-flowspec="1"`、节点 `data-node="{id}"`、`#sel-ring`）。契约破坏性变更时主版本 +1。

```json
{
  "spec": "walkmap/1",
  "title": "走查标题",
  "svg": "相对本文件的 SVG 路径",
  "default_node": "C",
  "css_vars": { "--wt-accent": "#555555" },
  "pages": [
    { "id": "p-home", "frame": "phone", "file": "pages/home.html" },
    { "id": "p-admin", "frame": "wide",  "file": "pages/admin.html" }
  ],
  "nodes": {
    "A": { "page": "p-home", "title": "节点标题", "anno": [["标注小标题", "标注正文"]] }
  }
}
```

- `pages[].frame`：`phone`（375px 手机框）｜`wide`（690px 后台/浏览器宽窗口），切换节点时自动切换设备框
- `pages[].file`：页面 HTML 片段（body 内片段，不含 html/head），可使用模板内置的 `wt-*` 组件类与 `goNode(id)` API
- `nodes`：仅需覆盖 SVG 中带 `data-node` 的节点；多个节点可指向同一页面；缺失映射的 SVG 节点构建时给警告
- `css_vars` 可选：覆盖模板 `:root` 的 `--wt-*` 样式变量；缺省为灰度线框
- 产物为单文件 HTML，零运行时依赖、离线可用
