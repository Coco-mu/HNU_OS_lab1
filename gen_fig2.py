# -*- coding: utf-8 -*-
"""重画实验一图 1-2：构建与运行链路。按文字宽度自适应框宽，避免文字溢出。"""

W, H = 760, 340
PAD = 24


def text_w(s, size=10.5):
    """粗略估算字符串渲染宽度：中文按 1em，英文按 0.56em"""
    w = 0.0
    for ch in s:
        w += size * (1.0 if ord(ch) > 0x2E80 else 0.56)
    return w


BOXES = [
    ('src/*.c  *.S', '源码'),
    ('aarch64-none-elf-gcc', '交叉编译'),
    ('*.o', '目标文件'),
    ('GNU ld', '−T aarch64-qemu.ld'),
    ('build/miniEuler', '裸机 ELF'),
    ('qemu-system-aarch64', '−kernel 运行'),
]
FILLS = ['#EAF2FB', '#FFF6E5', '#EAF2FB', '#FFF6E5', '#E7F4EA', '#F3EAF7']
MIN_W = 72
GAP = 12
BOX_H = 54
TOP = 110


def main():
    widths = [max(MIN_W, round(text_w(t) + PAD)) for t, _ in BOXES]
    total = sum(widths) + GAP * (len(BOXES) - 1)
    x0 = (W - total) / 2

    out = []
    out.append(
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d">' % (W, H, W, H))
    out.append(
        '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#4A5568"/></marker></defs>')
    out.append(
        '<g font-family="\'PingFang SC\',\'Hiragino Sans GB\','
        '\'Microsoft YaHei\',sans-serif">')
    out.append('<rect x="0" y="0" width="%d" height="%d" fill="#FFFFFF"/>' % (W, H))

    # 标题
    out.append('<rect x="24" y="30" width="4" height="18" fill="#1F5FA8"/>')
    out.append('<text x="36" y="45" font-size="16" fill="#1B1B1B" '
               'font-weight="600">图 1-2  构建与运行链路（实验一）</text>')
    out.append('<text x="36" y="65" font-size="11.5" fill="#5A6672">'
               '一次 cmake --build 实际发生的事情</text>')
    out.append('<line x1="24" y1="78" x2="%d" y2="78" stroke="#D5DBE2" stroke-width="1"/>'
               % (W - 24))

    x = x0
    for i, ((txt, label), bw) in enumerate(zip(BOXES, widths)):
        cx = x + bw / 2
        out.append('<rect x="%.1f" y="%d" width="%d" height="%d" rx="7" fill="%s" '
                   'stroke="#1F5FA8" stroke-width="1.4"/>'
                   % (x, TOP, bw, BOX_H, FILLS[i]))
        # 框内主文字：字号按可用宽度收缩，最小 8.5
        size = 10.5
        while text_w(txt, size) > bw - 10 and size > 8.0:
            size -= 0.5
        out.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="#1B1B1B" '
                   'text-anchor="middle" font-weight="600">%s</text>'
                   % (cx, TOP + BOX_H / 2 + size * 0.36, size, txt))
        # 框下标签
        out.append('<text x="%.1f" y="%d" font-size="10" fill="#5A6672" '
                   'text-anchor="middle">%s</text>' % (cx, TOP + BOX_H + 22, label))
        # 箭头
        if i < len(BOXES) - 1:
            ax1 = x + bw + 1
            ax2 = x + bw + GAP - 2
            out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#4A5568" '
                       'stroke-width="1.5" marker-end="url(#ar)"/>'
                       % (ax1, TOP + BOX_H / 2, ax2, TOP + BOX_H / 2))
        x += bw + GAP

    # 底部两条说明条
    for i, (txt, y) in enumerate([
            ('工具链 = Homebrew GCC 交叉编译器（aarch64-none-elf-*）+ GNU ld', 218),
            ('链接脚本 aarch64-qemu.ld 决定入口地址 0x40000000、代码段/数据段布局与栈顶符号', 268)]):
        out.append('<rect x="24" y="%d" width="%d" height="34" rx="6" '
                   'fill="#F7F9FB" stroke="#D5DBE2" stroke-width="1"/>' % (y, W - 48))
        out.append('<text x="%d" y="%d" font-size="11" fill="#2D3748" '
                   'text-anchor="middle">%s</text>' % (W // 2, y + 22, txt))

    out.append('</g></svg>')

    path = '实验截图/示意图2_构建与运行链路.svg'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(''.join(out))
    print('已写', path)
    print('各框宽度:', widths, '总宽', total)


if __name__ == '__main__':
    main()
