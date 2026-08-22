# -*- coding: utf-8 -*-
"""BMF _02 도표 템플릿 셀 채움 (범용)

사용법:
  python3 fill_cells.py <template.hwpx> <cellmap.json> <output.hwpx> [--hwpx-scripts <hwpx스킬 scripts 경로>]

cellmap.json 형식:
{
  "header": "본문 : ... 절기: ... 작성자: ...",   # 표 밖 헤더 문단 (선택)
  "main_idea": ["살", "피", "심"],                 # 좌측 세로 셀 r0c0 (선택, 글자별 문단)
  "cells": { "0,4": ["문단1", "문단2"], "3,1": ["창"], ... },  # "행,열": 문단 리스트
  "content_cells": ["0,4", "8,2", ...]             # 본문 7.5pt 서식(charPr 60)을 적용할 셀 (선택)
}

동작: 템플릿을 unpack → header.xml에 본문용 charPr 60(7.5pt 일반) 자동 추가 →
각 셀의 기존 첫 문단을 프로토타입 삼아 스타일 보존 복제 → 텍스트 치환 → pack → validate.
표 구조(행·열·병합·크기)는 변경하지 않는다.

중요: 템플릿 빈 셀의 잔존 서식은 9.5pt 볼드라서 본문을 그대로 넣으면 셀이 넘쳐 겹친다.
정의행·ABIT·귀납·네장면 문장 셀·본문읽기·주제문 선포문은 반드시 content_cells에 넣어
7.5pt를 적용할 것. 라벨·개념·선포문 1~3·정과 행은 템플릿 서식 유지.
"""
import sys, json, copy, subprocess, tempfile, os, shutil

NS = {'hp': 'http://www.hancom.co.kr/hwpml/2011/paragraph'}
HH = 'http://www.hancom.co.kr/hwpml/2011/head'


def main():
    from lxml import etree
    tpl, cmap_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    hwpx_scripts = None
    if '--hwpx-scripts' in sys.argv:
        hwpx_scripts = sys.argv[sys.argv.index('--hwpx-scripts') + 1]

    cmap = json.load(open(cmap_path, encoding='utf-8'))
    work = tempfile.mkdtemp()

    # unpack (zip 직접 해제 — hwpx는 zip 컨테이너)
    import zipfile
    with zipfile.ZipFile(tpl) as z:
        z.extractall(work)

    # header.xml: 본문용 charPr 60 (7.5pt 일반, charPr 17 복제) 자동 추가
    hpath = os.path.join(work, 'Contents', 'header.xml')
    ht = etree.parse(hpath)
    hns = {'hh': HH}
    props = ht.find('.//hh:charProperties', hns)
    if not any(cp.get('id') == '60' for cp in props.findall('hh:charPr', hns)):
        base = next(cp for cp in props.findall('hh:charPr', hns) if cp.get('id') == '17')
        ncp = copy.deepcopy(base)
        ncp.set('id', '60')
        ncp.set('height', '750')
        b = ncp.find('hh:bold', hns)
        if b is not None:
            ncp.remove(b)
        props.append(ncp)
        props.set('itemCnt', str(len(props.findall('hh:charPr', hns))))
        ht.write(hpath, xml_declaration=True, encoding='UTF-8')

    sec_path = os.path.join(work, 'Contents', 'section0.xml')
    tree = etree.parse(sec_path)
    root = tree.getroot()
    tbl = tree.findall('.//hp:tbl', NS)[0]
    pid = [2000000000]

    content_cells = set(cmap.get('content_cells', []))

    def set_cell(r, c, lines, charpr=None):
        for tc in tbl.findall('.//hp:tc', NS):
            addr = tc.find('hp:cellAddr', NS)
            if int(addr.get('rowAddr')) == r and int(addr.get('colAddr')) == c:
                sub = tc.find('hp:subList', NS)
                ps = sub.findall('hp:p', NS)
                proto = ps[0]
                for p in ps:
                    sub.remove(p)
                for line in lines:
                    np = copy.deepcopy(proto)
                    pid[0] += 1
                    np.set('id', str(pid[0]))
                    runs = np.findall('hp:run', NS)
                    first = runs[0]
                    for extra in runs[1:]:
                        np.remove(extra)
                    if charpr:
                        first.set('charPrIDRef', charpr)
                    ts = first.findall('hp:t', NS)
                    for t in ts[1:]:
                        first.remove(t)
                    if ts:
                        ts[0].text = line
                    else:
                        etree.SubElement(first, '{%s}t' % NS['hp']).text = line
                    sub.append(np)
                return
        print(f'경고: 셀 없음 r{r},c{c}', file=sys.stderr)

    if cmap.get('header'):
        for t in root.iter('{%s}t' % NS['hp']):
            if t.text and t.text.startswith('본문'):
                t.text = cmap['header']
                break

    if cmap.get('main_idea'):
        set_cell(0, 0, cmap['main_idea'])

    for key, lines in cmap.get('cells', {}).items():
        r, c = (int(x) for x in key.split(','))
        set_cell(r, c, lines, '60' if key in content_cells else None)

    tree.write(sec_path, xml_declaration=True, encoding='UTF-8')

    # pack: mimetype 먼저(ZIP_STORED), 나머지 DEFLATED
    if os.path.exists(out):
        os.remove(out)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        mt = os.path.join(work, 'mimetype')
        if os.path.exists(mt):
            z.write(mt, 'mimetype', compress_type=zipfile.ZIP_STORED)
        for base, _, files in os.walk(work):
            for f in files:
                full = os.path.join(base, f)
                rel = os.path.relpath(full, work)
                if rel == 'mimetype':
                    continue
                z.write(full, rel)
    shutil.rmtree(work)

    if hwpx_scripts:
        subprocess.run([sys.executable, os.path.join(hwpx_scripts, 'validate.py'), out], check=True)
    print(f'생성 완료: {out}')


if __name__ == '__main__':
    main()
