# -*- coding: utf-8 -*-
"""内联关键样式（服务端注入 <head>，不依赖外部样式表）。

为什么需要：如果外链 CSS 没加载 —— 客户手机开省流量/精简模式、网络丢包、或老旧 WebView
拦截 —— 大图会按原始尺寸（1600px）撑开整页，手机上表现为横向溢出、超长的一团乱码。
这段约 300 字节，保证任何情况下页面都不塌：图片不超屏、字体可读、宽表格可横滚。
写在 <link rel=stylesheet> 之前，正常加载时被覆盖，互不冲突。
"""

CSS = (
    "<style>img,svg,video,iframe{max-width:100%;height:auto}"
    'body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;'
    "color:#1c1c1c;background:#fff;word-wrap:break-word;overflow-wrap:anywhere}"
    "h1{font-size:1.6rem}h2{font-size:1.3rem}h3{font-size:1.15rem}"
    "table{max-width:100%;display:block;overflow-x:auto;border-collapse:collapse}"
    "pre{max-width:100%;overflow-x:auto}"
    "header,footer,main,section{padding-left:12px;padding-right:12px;box-sizing:border-box}</style>"
)
