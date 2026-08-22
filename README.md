# bethel-ministry 플러그인 마켓플레이스

1사단 58포병대대 벧엘교회 군선교사 김병국 목사의 사역용 Claude Code 플러그인을 담은 개인 마켓플레이스 저장소입니다.

이 저장소를 마켓플레이스로 등록하면 로컬 Claude Code에서 `bethel-ministry` 플러그인을 설치·업데이트할 수 있습니다.

## 등록 및 설치 (로컬 Claude Code)

```
/plugin marketplace add <github-username>/<repo-name>
/plugin install bethel-ministry@bethel-ministry-marketplace
```

## 업데이트

플러그인 내용을 수정한 뒤 커밋·푸시하고, `plugins/bethel-ministry/.claude-plugin/plugin.json`과
`.claude-plugin/marketplace.json`의 `version` 필드를 함께 올려주세요. 이후 로컬 Claude Code에서:

```
/plugin marketplace update bethel-ministry-marketplace
/plugin update bethel-ministry@bethel-ministry-marketplace
```

## 참고: Cowork 세션과의 관계

이 저장소는 로컬 Claude Code(맥북 등)에서 플러그인을 설치·갱신하는 용도입니다. Cowork(클라우드 세션)는
현재 외부 GitHub 마켓플레이스를 직접 구독하는 기능을 지원하지 않으므로, Cowork 세션에서 스킬을 수정한
결과물(.skill 파일)은 이 저장소에도 수동으로 반영(커밋)해야 두 환경의 내용이 일치합니다.

## 구조

```
.
├── .claude-plugin/
│   └── marketplace.json       # 마켓플레이스 등록 정보 (플러그인 목록)
└── plugins/
    └── bethel-ministry/
        ├── .claude-plugin/
        │   └── plugin.json    # 플러그인 자체 정보
        ├── skills/             # 개별 스킬 (SKILL.md + references/)
        └── README.md
```
