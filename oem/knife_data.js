/* ============================================================================
   OEM 刀具配置器 —— 数据层
   （blade / handle 两段由 import_knife_assets.py 从 oem_assets 的出图生成；
     下面这份是手写的占位数据，真实图到位后会被自动替换）
   ============================================================================
   坐标系（所有形状共用，这是「衔接处不错位」的唯一保证）：

     原点 (0,0) = 枢轴 / 护手线 × 刀身中轴线的交点
     X 正方向  = 手柄方向（刀刃在负 X，刀尖朝左）
     Y 正方向  = 向上       单位 = mm

             刀尖 ◄── 刀刃 ──┤枢轴/护手线├── 手柄 ──►
       Y=+  ┌────────────────┼──────────────────┐
       Y=0  ─────────────────┼──────────────────┼──►  刀身中轴
       Y=-  └────────────────┼──────────────────┘
                             X=0                X=+

   网页视图映射（导入脚本按全局包围盒自动算）：
     viewX = view.ox + mmX * view.s ；viewY = view.oy - mmY * view.s
   ============================================================================ */

window.KNIFE_DATA = {

  /* 视图映射：mm → SVG viewBox 0 0 1000 300 */
  view: { ox: 460, oy: 152, s: 3.2, w: 1000, h: 300 },

  /* 衔接与组合规则（导入时按这套值校验并在报告里报警）：
     tangLen        刀刃柄舌从护手线向右伸出多少 mm（要够长，手柄才盖得住）
     tangH          柄舌半高 mm（太厚会从手柄边缘露出来）
     handleStart    手柄前端从 X=? 开始（负值 = 略微包过护手线）
     pocketClearance 折叠刀收刀时柄内腔要留的余量 mm
     折叠规则：刀长 bladeLen + pocketClearance <= 手柄内腔 pocketLen，否则折不进去 */
  joint: { tangLen: 60, tangH: 12, handleStart: -5, pocketClearance: 8 },

  /* ---- 刀刃：mount = folding(折叠) / fixed(直刀)；bladeLen = 枢轴到刀尖 mm ---- */
  blade: [
        {
            "key": "drop-point",
            "label": "Drop point",
            "cn": "水滴头",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 95,
            "needsArt": true,
            "d": "M 156 150 C 200 112 260 102 340 100 L 460 102 L 560 102 L 560 196 L 460 196 C 340 197 210 186 156 150 Z"
        },
        {
            "key": "straight-back",
            "label": "Straight back",
            "cn": "直背型",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 95,
            "needsArt": true,
            "d": "M 156 118 C 200 106 300 102 460 104 L 560 104 L 560 196 L 460 196 C 330 198 220 190 156 118 Z"
        },
        {
            "key": "upswept",
            "label": "Upswept",
            "cn": "上翘型",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 140 100 C 200 108 300 108 460 106 L 560 106 L 560 196 L 460 196 C 340 200 230 188 140 100 Z"
        },
        {
            "key": "california-clip",
            "label": "California clip",
            "cn": "加州刨削式",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 140 146 L 320 98 L 460 100 L 560 100 L 560 196 L 460 196 C 330 198 200 180 140 146 Z"
        },
        {
            "key": "american-tanto",
            "label": "American tanto",
            "cn": "美式T头",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 140 140 L 300 94 L 460 98 L 560 98 L 560 196 L 460 196 C 330 198 210 178 140 140 Z"
        },
        {
            "key": "japanese-tanto",
            "label": "Japanese tanto",
            "cn": "日式T头",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 146 144 C 200 96 260 88 320 92 L 460 96 L 560 96 L 560 196 L 460 196 C 330 198 210 182 146 144 Z"
        },
        {
            "key": "sheepsfoot",
            "label": "Sheepsfoot",
            "cn": "羊蹄型",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 90,
            "needsArt": true,
            "d": "M 172 104 C 250 100 350 100 460 102 L 560 102 L 560 196 L 460 196 C 330 198 210 194 172 104 Z"
        },
        {
            "key": "wharncliffe",
            "label": "Wharncliffe",
            "cn": "鸟嘴型",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 95,
            "needsArt": true,
            "d": "M 150 170 L 420 102 L 460 102 L 560 102 L 560 196 L 460 196 C 340 198 200 192 150 170 Z"
        },
        {
            "key": "spear-point",
            "label": "Spear point",
            "cn": "矛头",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 140 150 C 200 110 290 100 380 99 L 460 100 L 560 100 L 560 196 L 460 196 C 370 195 240 192 140 150 Z"
        },
        {
            "key": "recurve",
            "label": "Recurve / S-blade",
            "cn": "反曲型 / S刃",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 98,
            "needsArt": true,
            "d": "M 150 140 C 220 108 320 104 460 106 L 560 106 L 560 196 L 460 196 C 370 192 300 198 240 190 C 200 184 170 168 150 140 Z"
        },
        {
            "key": "utility",
            "label": "Utility",
            "cn": "实用型",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 88,
            "needsArt": true,
            "d": "M 178 146 C 230 116 330 108 460 108 L 560 108 L 560 192 L 460 192 C 330 194 220 184 178 146 Z"
        },
        {
            "key": "pen-blade",
            "label": "Pen blade",
            "cn": "削笔刀型",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 80,
            "needsArt": true,
            "d": "M 204 148 C 260 120 340 112 460 112 L 560 112 L 560 188 L 460 188 C 340 190 260 182 204 148 Z"
        },
        {
            "key": "horn-cliffe",
            "label": "Horncliffe",
            "cn": "霍式刀（霍恩克利夫型）",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 95,
            "needsArt": true,
            "d": "M 148 126 C 210 100 320 98 460 100 L 560 100 L 560 196 L 460 196 C 320 198 200 186 148 126 Z"
        },
        {
            "key": "modified-tanto",
            "label": "Modified tanto",
            "cn": "改进式T头",
            "tier": 1,
            "mount": "folding",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 150 120 C 210 104 280 96 360 94 L 460 100 L 560 100 L 560 196 L 460 196 C 340 198 210 176 150 120 Z"
        },
        {
            "key": "turkish-clip",
            "label": "Turkish clip",
            "cn": "土耳其刨削式",
            "tier": 2,
            "mount": "folding",
            "bladeLen": 105,
            "needsArt": true,
            "d": "M 132 156 C 200 102 300 92 420 98 L 460 99 L 560 99 L 560 196 L 460 196 C 330 198 190 190 132 156 Z"
        },
        {
            "key": "texas-toothpick",
            "label": "Texas toothpick",
            "cn": "德州牙签式",
            "tier": 2,
            "mount": "folding",
            "bladeLen": 105,
            "needsArt": true,
            "d": "M 124 150 C 210 118 330 110 460 110 L 560 110 L 560 186 L 460 186 C 330 188 200 182 124 150 Z"
        },
        {
            "key": "reverse-tanto",
            "label": "Reverse tanto",
            "cn": "反式T头",
            "tier": 2,
            "mount": "folding",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 156 108 L 330 104 L 460 104 L 560 104 L 560 196 L 460 196 C 340 198 240 178 156 108 Z"
        },
        {
            "key": "swedge-false-edge",
            "label": "Swedge / false edge",
            "cn": "背部假刃",
            "tier": 2,
            "mount": "folding",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 148 150 L 250 106 L 330 100 L 460 102 L 560 102 L 560 196 L 460 196 C 330 198 200 186 148 150 Z"
        },
        {
            "key": "skinner",
            "label": "Skinner",
            "cn": "剥皮刀型",
            "tier": 2,
            "mount": "fixed",
            "bladeLen": 95,
            "needsArt": true,
            "d": "M 156 136 C 200 104 280 96 460 98 L 560 98 L 560 196 L 460 196 C 320 202 190 190 156 136 Z"
        },
        {
            "key": "gut-hook",
            "label": "Gut hook",
            "cn": "肠线勾刃尖",
            "tier": 2,
            "mount": "fixed",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 150 152 C 200 122 250 106 296 98 C 312 95 324 100 326 112 C 310 116 300 126 303 138 C 307 152 322 156 338 148 C 366 136 412 126 460 122 L 560 120 L 560 196 L 460 196 C 330 198 200 186 150 152 Z"
        },
        {
            "key": "bowie",
            "label": "Bowie",
            "cn": "大刀式",
            "tier": 2,
            "mount": "fixed",
            "bladeLen": 125,
            "needsArt": true,
            "d": "M 62 144 L 240 100 L 380 96 L 460 100 L 560 100 L 560 200 L 460 200 C 320 202 180 190 62 144 Z"
        },
        {
            "key": "kukri",
            "label": "Kukri",
            "cn": "库克里型",
            "tier": 2,
            "mount": "fixed",
            "bladeLen": 120,
            "needsArt": true,
            "d": "M 76 150 C 120 110 200 104 300 118 C 380 128 430 140 460 148 L 560 148 L 560 205 L 460 205 C 400 200 330 186 260 162 C 180 134 120 140 76 150 Z"
        },
        {
            "key": "horn-recurve",
            "label": "Horn recurve",
            "cn": "霍式反曲 / 引刀式",
            "tier": 2,
            "mount": "fixed",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 140 124 C 190 98 260 94 340 96 L 460 100 L 560 100 L 560 196 L 460 196 C 330 198 200 180 140 124 Z"
        },
        {
            "key": "frog-spear",
            "label": "Frog spear",
            "cn": "蛙矛式",
            "tier": 2,
            "mount": "fixed",
            "bladeLen": 100,
            "needsArt": true,
            "d": "M 130 150 C 200 112 300 104 400 102 L 460 102 L 560 102 L 560 196 L 460 196 C 360 194 240 190 130 150 Z"
        }
    ],

  /* ---- 手柄：pocketLen = 枢轴到柄尾的内腔可用长度 mm ---- */
  handle: [
    { key: "straight", label: "Straight",        mount: "folding", pocketLen: 128,
      d: "M 462 102 L 886 108 C 934 110 948 124 946 152 C 944 180 930 194 886 196 L 565 199 L 462 203 Z",
      rivets: [[600,152],[700,152],[800,152]], engrave: [700,186] },
    { key: "curved",   label: "Dropped / curved", mount: "folding", pocketLen: 122,
      d: "M 462 102 L 780 106 C 852 116 906 152 926 196 C 932 208 918 214 906 208 C 872 172 838 156 786 150 L 570 200 L 462 203 Z",
      rivets: [[600,180],[690,168],[780,148]], engrave: [640,138] },
    { key: "groove",   label: "Finger groove (short)", mount: "folding", pocketLen: 105,
      d: "M 462 102 L 886 108 C 934 110 948 124 946 152 C 944 180 930 194 886 196 L 720 200 C 690 200 676 190 668 176 C 656 154 634 144 610 144 C 592 144 580 152 574 166 L 566 200 L 462 203 Z",
      rivets: [[660,152],[740,152],[820,152]], engrave: [770,184] },
    { key: "stag",     label: "Stag (fixed blade)", mount: "fixed", pocketLen: 140,
      d: "M 462 96 L 880 104 C 936 108 954 126 952 152 C 950 178 934 196 880 200 L 565 203 L 462 206 Z",
      rivets: [[600,158],[700,155],[800,153]], engrave: [700,140] }
  ],

  /* ---- 柄材：fill 可以是 SVG pattern id，也可以是纹理图 ---- */
  materials: [
    { key: "wood",    label: "Rosewood",      sw: "#6b3f22", fill: "url(#p-wood)" },
    { key: "g10b",    label: "Black G10",     sw: "#23272c", fill: "url(#p-g10b)" },
    { key: "g10o",    label: "Orange G10",    sw: "#b8531a", fill: "url(#p-g10o)" },
    { key: "micarta", label: "Green Micarta", sw: "#4b5341", fill: "url(#p-micarta)" },
    { key: "carbon",  label: "Carbon fibre",  sw: "#1b1e22", fill: "url(#p-carbon)" },
    { key: "maroon",  label: "Maroon pakka",  sw: "#5c2230", fill: "url(#p-maroon)" }
  ],

  /* ---- 钢种：B2B 采购关心的就是这几个 ---- */
  steels: [
    { key: "5cr",  label: "5Cr15MoV",     note: "budget kitchen / utility" },
    { key: "8cr",  label: "8Cr14MoV",     note: "balanced, most popular" },
    { key: "440c", label: "440C",         note: "high corrosion resistance" },
    { key: "d2",   label: "D2 (Cr12MoV)", note: "high wear resistance" },
    { key: "dam",  label: "Damascus",     note: "pattern-welded, premium" }
  ],

  /* ---- 表面处理 ---- */
  finishes: [
    { key: "satin",  label: "Satin brushed",   grad: "url(#g-satin)",    light: false },
    { key: "mirror", label: "Mirror polish",   grad: "url(#g-mirror)",   light: false },
    { key: "stone",  label: "Stonewash",       grad: "url(#g-stone)",    light: false },
    { key: "black",  label: "Black titanium",  grad: "url(#g-black)",    light: true },
    { key: "dam",    label: "Etched Damascus", grad: "url(#g-damascus)", light: true }
  ],

  /* ---- 刻字 ---- */
  engraving: [
    { key: "none",   label: "No engraving" },
    { key: "blade",  label: "Logo on blade" },
    { key: "handle", label: "Logo on handle" },
    { key: "both",   label: "Blade + handle" }
  ]
};
