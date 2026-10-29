#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重新生成 图 1-1 裸机启动流程（实验一），改正 main 的输出方式与结尾空转循环。"""
import os

W = 720
H = 730
BX, BW = 180, 360          # 主链方块
BH = 46

C_BLUE = '#1F5FA8'
C_TEXT = '#1B1B1B'
C_SUB = '#5A6672'
F_TITLE = 16
F_SUB = 11.5
F_BOX = 12.5
F_SMALL = 10.5

boxes = [
    # (y, h, [lines], fill)
    (96, BH, ['QEMU 加载镜像：-kernel build/miniEuler'], '#FFF6E5'),
    (172, 58, ['0x40000000  OsElxState   ← start.S / .text.bspinit',
               'MRS x6, CurrentEL'], '#EAF2FB'),
    (260, BH, ['CMP w6, #4   →   BEQ Start'], '#EAF2FB'),
    (336, BH, ['Start：SP = __os_sys_sp_end &amp; ~0xF'], '#EAF2FB'),
    (412, BH, ['B OsEnterMain   ← prt_reset_vector.S / .text.startup'], '#EAF2FB'),
    (488, 58, ['BL main   →   main() 直接写 UARTDR（0x09000000）',
               '循环 18 次输出 "AArch64 Bare Metal"'], '#EAF7EF'),
    (574, BH, ['main 返回  →  MSR DAIF, #0x1C0（屏蔽中断）'], '#EAF7EF'),
    (650, BH, ['EXITLOOP：B EXITLOOP（原地空转，实验结束）'], '#F4F6F8'),
]


def esc(s):
    return s


parts = []
parts.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H))
parts.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
             'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#4A5568"/></marker></defs>')
parts.append('<g font-family="\'PingFang SC\',\'Hiragino Sans GB\',\'Microsoft YaHei\',sans-serif">')
parts.append('<rect x="0" y="0" width="%d" height="%d" fill="#FFFFFF"/>' % (W, H))

# 标题区
parts.append('<rect x="24" y="30" width="4" height="18" fill="%s"/>' % C_BLUE)
parts.append('<text x="36" y="45" font-size="%d" fill="%s" font-weight="600">图 1-1  裸机启动流程（实验一）</text>'
             % (F_TITLE, C_TEXT))
parts.append('<text x="36" y="65" font-size="%s" fill="%s">从 QEMU 载入 ELF 到串口输出第一条字符串；'
             'start.S 判异常级别并设栈，prt_reset_vector.S 调 main、返回后屏蔽中断</text>' % (F_SUB, C_SUB))
parts.append('<line x1="24" y1="78" x2="696" y2="78" stroke="#D5DBE2" stroke-width="1"/>')

# 主链方块
for y, h, lines, fill in boxes:
    parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="7" fill="%s" stroke="%s" stroke-width="1.4"/>'
                 % (BX, y, BW, h, fill, C_BLUE))
    if len(lines) == 1:
        cy = y + h / 2 + 4.5
        parts.append('<text x="%d" y="%.3f" font-size="%s" fill="%s" text-anchor="middle">%s</text>'
                     % (BX + BW // 2, cy, F_BOX, C_TEXT, lines[0]))
    else:
        cy = y + h / 2 - 7
        for k, ln in enumerate(lines):
            parts.append('<text x="%d" y="%.3f" font-size="%s" fill="%s" text-anchor="middle">%s</text>'
                         % (BX + BW // 2, cy + k * 16.5, F_BOX, C_TEXT, ln))

# 竖箭头
for i in range(len(boxes) - 1):
    y0 = boxes[i][0] + boxes[i][1] + 2
    y1 = boxes[i + 1][0] - 2
    parts.append('<line x1="360" y1="%d" x2="360" y2="%d" stroke="#4A5568" stroke-width="1.5" '
                 'marker-end="url(#ar)"/>' % (y0, y1))

# 左分支 OsEl2Entry
parts.append('<rect x="6" y="260" width="160" height="46" rx="7" fill="#FDEDEA" stroke="%s" stroke-width="1.4"/>'
             % C_BLUE)
parts.append('<text x="86" y="279.425" font-size="%s" fill="%s" text-anchor="middle">Z=0 → OsEl2Entry</text>'
             % (F_SMALL, C_TEXT))
parts.append('<text x="86" y="293.925" font-size="%s" fill="%s" text-anchor="middle">B .   挂死</text>'
             % (F_SMALL, C_TEXT))
parts.append('<line x1="180" y1="283" x2="168" y2="283" stroke="#4A5568" stroke-width="1.5" marker-end="url(#ar)"/>')
parts.append('<text x="174" y="274" font-size="11" fill="%s" text-anchor="middle">否</text>' % C_SUB)
parts.append('<text x="370" y="328" font-size="11" fill="%s" text-anchor="start">是</text>' % C_SUB)

# 右侧注释框
parts.append('<rect x="572" y="172" width="124" height="200" rx="7" fill="#F4F6F8" stroke="#B9C3CE" '
             'stroke-width="1.4" stroke-dasharray="4 3"/>')
notes = ['QEMU virt 上电', '默认 EL1', '', 'CurrentEL', '= 0b0100', '→ x6 = 4', '→ Z = 1']
for k, t in enumerate(notes):
    parts.append('<text x="634" y="%.3f" font-size="%s" fill="%s" text-anchor="middle">%s</text>'
                 % (232.175 + k * 14.5, F_SMALL, C_TEXT, t))

parts.append('</g></svg>')

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '实验截图', '示意图1_裸机启动流程.svg')
with open(out, 'w', encoding='utf-8') as f:
    f.write(''.join(parts))
print('已写入', out, len(''.join(parts)), 'bytes')
