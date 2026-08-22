#!/bin/bash
# setup_font.sh
# NanumSquare 폰트를 /tmp/nanum-fonts/ 에 설치한다.
# 이미 존재하면 스킵.

FONT_DIR="${1:-/tmp/nanum-fonts}"
FONT_FILE="$FONT_DIR/NanumSquareR.ttf"

if [ -f "$FONT_FILE" ]; then
  echo "✅ NanumSquare 폰트 이미 존재: $FONT_DIR"
  exit 0
fi

echo "📥 NanumSquare 폰트 다운로드 중..."
mkdir -p "$FONT_DIR"

# Ubuntu 미러에서 deb 패키지 다운로드 후 압축 해제
DEB_URL="http://archive.ubuntu.com/ubuntu/pool/universe/f/fonts-nanum/fonts-nanum_20200506-1_all.deb"
DEB_FILE="$FONT_DIR/fonts-nanum.deb"

wget -q "$DEB_URL" -O "$DEB_FILE"

if [ $? -ne 0 ]; then
  echo "❌ 다운로드 실패. 네트워크 연결을 확인하세요."
  exit 1
fi

# deb에서 ttf 추출
TMP_EXTRACT="$FONT_DIR/extract"
mkdir -p "$TMP_EXTRACT"
dpkg-deb -x "$DEB_FILE" "$TMP_EXTRACT"

# NanumSquare ttf 파일을 FONT_DIR로 복사
cp "$TMP_EXTRACT"/usr/share/fonts/truetype/nanum/NanumSquare*.ttf "$FONT_DIR/" 2>/dev/null

# 정리
rm -f "$DEB_FILE"
rm -rf "$TMP_EXTRACT"

if [ -f "$FONT_FILE" ]; then
  echo "✅ NanumSquare 폰트 준비 완료: $FONT_DIR"
  ls "$FONT_DIR"/*.ttf
else
  echo "❌ 폰트 추출 실패"
  exit 1
fi
