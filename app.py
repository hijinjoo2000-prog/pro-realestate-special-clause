import streamlit as st

st.set_page_config(
    page_title="PRO 재개발 특약 생성기",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    .main { padding: 10px 20px; }
    .stTextArea textarea { font-size: 14px; line-height: 1.8; }
    .copy-box {
        background: #f0f4f8;
        border: 1.5px solid #4a90d9;
        border-radius: 10px;
        padding: 18px;
        font-size: 14px;
        line-height: 2;
        white-space: pre-wrap;
        word-break: break-all;
    }
    .section-title {
        font-size: 16px;
        font-weight: 700;
        color: #2c3e50;
        border-left: 4px solid #3498db;
        padding-left: 8px;
        margin: 16px 0 8px 0;
    }
    div[data-testid="stButton"] > button {
        font-size: 16px;
        font-weight: 700;
        padding: 10px 20px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────── 유틸 함수 ────────────────────────────────

def fmt_money(v):
    v = v.strip().replace(",", "").replace("원", "").replace(" ", "")
    if not v: return "[    ]"
    try:
        n = int(float(v))
        return f"{n:,}원"
    except:
        return v + "원" if "원" not in v else v

def fmt_eok(v):
    v = v.strip().replace(" ", "").replace(",", "").replace("원", "").replace("억", "")
    if not v: return "[    ]"
    try:
        n = float(v)
        return f"{n:.0f}억원" if n == int(n) else f"{n}억원"
    except:
        return v + "억원"

def fmt_pct(v):
    v = v.strip()
    if not v: return "[    ]"
    if "%" not in v: v += "%"
    return v

def fmt_area(v):
    v = v.strip()
    if not v: return "[    ]"
    if "㎡" not in v and "평" not in v: v += "㎡"
    return v

def val(v, fmt=None):
    if not v or not v.strip(): return "[    ]"
    if fmt == "money": return fmt_money(v)
    if fmt == "eok": return fmt_eok(v)
    if fmt == "pct": return fmt_pct(v)
    if fmt == "area": return fmt_area(v)
    return v.strip()

# ─────────────────────────────────── 헤더 ────────────────────────────────────

st.title("🏠 PRO 재개발 특약 생성기")
st.caption("계약서 특약 / 가계약 약정서를 자동 생성합니다 — 모바일·PC 어디서나 사용 가능")

# ─────────────────────────────────── 문서 종류 선택 ──────────────────────────

doc_type = st.radio(
    "📄 작성 문서 선택",
    ["📋 계약서 특약 작성폼", "📝 계약금일부금 특약 작성폼(약정서)"],
    horizontal=True
)
is_prov = doc_type.startswith("📝")

st.divider()

# ─────────────────────────────────── 입력 폼 ─────────────────────────────────

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">🏗️ 물건 기본 정보</div>', unsafe_allow_html=True)
    구역명 = st.text_input("구역명", placeholder="예: 노량진8")
    진행단계 = st.text_input("해당 구역 진행단계", placeholder="예: 21.12.29 관리처분인가, 현 이주철거완료")
    소재지 = st.text_input("대상물건 소재지", placeholder="예: 노량진동 234-5외 1필지") if is_prov else ""
    종전자산 = st.text_input("종전자산평가액(감정가액)", placeholder="예: 415466490")
    비례율 = st.text_input("비례율", placeholder="예: 100.87")
    권리가액 = st.text_input("권리가액", placeholder="예: 419081048")
    조합원번호 = st.text_input("조합원번호", placeholder="예: 854")
    신청주택형 = st.text_input("신청 주택형", placeholder="예: 84")

with col2:
    st.markdown('<div class="section-title">👥 당사자 및 금액 정보</div>', unsafe_allow_html=True)
    매도인 = st.text_input("매도인 전원 성명", placeholder="예: 김진영, 신혜경")
    매수인 = st.text_input("매수인 전원 성명", placeholder="예: 권정환, 윤선미") if is_prov else ""
    수령인 = st.text_input("대금 일괄 수령인명", placeholder="예: 김진영")
    계좌번호 = st.text_input("계약금 수령 계좌번호", placeholder="예: 신한은행 110-155-784945 김진영")
    기지급금액 = st.text_input("기지급 계약금액", placeholder="예: 5000만원")
    기지급일자 = st.text_input("기지급 송금일자", placeholder="예: 2025.11.3.")

    if is_prov:
        총매매금액 = st.text_input("총 매매금액", placeholder="예: 2260000000")
        총계약금 = st.text_input("총 계약금액", placeholder="예: 220000000")
        작성예정일 = st.text_input("계약서 작성예정일", placeholder="예: 25년 11월 13일 이내 협의")
        중도금 = st.text_input("중도금액 및 지급일", placeholder="예: 880,000,000원 / 2025.12.3.")
        잔금 = st.text_input("잔금액 및 지급일", placeholder="예: 700,000,000원 / 2026.2.27.")
    else:
        총매매금액 = 총계약금 = 작성예정일 = 중도금 = 잔금 = ""

st.divider()

# ─────────────────────────────────── 선택 옵션 ───────────────────────────────

st.markdown('<div class="section-title">☑️ 선택 특약 옵션</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    opt_ilbugeom = st.checkbox("계약금의 일부금 배액배상")
    opt_gijigeum = st.checkbox("기지급 계약금 명시")
with c2:
    전세보증금 = st.text_input("조건부 전세보증금 (억)", placeholder="예: 4.6", key="jeonse")
    opt_jeonse = st.checkbox("조건부 임대차(전세)")
    opt_isabi = st.checkbox("이사비/이주비 수령")
with c3:
    opt_su익 = st.checkbox("수익 및 관리 책임")
    opt_daegeum = st.checkbox("대금 수령인 지정")
    opt_ijubi = st.checkbox("이주비 이자 정산")
with c4:
    멸실최대기한 = st.text_input("멸실 등기 최대 기한", placeholder="예: 2026.01.29", key="myeol")
    opt_myeolsil = st.checkbox("멸실 등기 대응")

st.divider()

# ─────────────────────────────────── 특약 생성 ───────────────────────────────

def gen_clauses():
    clauses = []

    # 공통 필수
    clauses.append("매도인과 매수인은 위 인쇄된 계약내용[제 1조-제9조]에 대해 설명을 듣고 인지 후 계약을 체결함.")
    clauses.append("현 시설 상태에서의 매매계약이며 계약 당사자는 등기사항전부증명서, 건축물대장, 토지대장, 토지이용계획확인서 등이 이상이 없음을 확인하고 체결하는 계약임.")

    jeon = val(종전자산, "money")
    bire = val(비례율, "pct")
    gwon = val(권리가액, "money")
    htype = val(신청주택형, "area")
    jo_num = val(조합원번호)

    clauses.append(
        f"({val(구역명)})구역 조합이 매도인에게 통지한 \"개별 추정분담금 정보제공통지\" 서류상 본 물건 종전자산가액은 {jeon}, "
        f"비례율 {bire}, 권리가액 {gwon} 임을 상호 확인하였으며, 신청한 주택형은 {htype}임을 매도인이 확인해주고 계약을 체결한다.(관리처분인가 내역서 사본 참조)\n"
        f"   (*조합원번호: {jo_num} / *감정평가 {jeon} 권리가액 {gwon} 나옴.)"
    )

    clauses.append(
        f"매수인은 대상부동산이 {val(구역명)} 재개발추진지역({val(진행단계)})임을 인지하고, "
        f"당해 재개발 사업진행과 조합원에 대한 의무, 권리사항 및 아파트 분양여부에 대하여 조합에 확인하고, 충분히 숙지하고 본 계약을 체결한다."
    )

    clauses.append(
        f"매도인은(세대원 포함) {val(구역명)} 내에 본건 외 다른 물건이 없음을 확약하며, "
        f"경합 발생 시 본 물건을 우선으로 한다. 위반 시 계약은 무조건 해제되며 매도인은 매수인에게 손해배상 책임을 진다."
    )

    clauses.append("매수인은 도정법 제72조 6항에 따른 재당첨 제한(5~10년) 규정을 숙지하였으며, 이로 인한 지위 미승계 시 매수인이 모든 책임을 진다.")
    clauses.append("매도인은 잔금일까지 조합으로부터 통보받은 중요 정보를 즉시 매수인에게 고지하며, 의결권 행사가 필요할 경우 매수인의 의사에 따른다.")
    clauses.append("매도인은 계약일 이후 잔금 익일까지 근저당 및 기타 제한물권을 추가로 설정하지 않으며 현 등기부 상태를 유지한다.")
    clauses.append("국가, 조합, 금융권의 사정으로 인한 사업 지연 및 건축비 상승 등 가격 변동성에 대해 중개사에게 책임을 묻지 않는다.")
    clauses.append("본 계약부동산에 관한 제세공과금은 인도일을 기준으로 하며, 지방세는 지방세법상 납부의무자가 부담한다.")
    clauses.append("세무에 관한 사항은 세무사에게 의뢰하기로 한다.")

    # 선택 특약
    if opt_gijigeum:
        clauses.append(
            f"계약금 중 금 {val(기지급금액)}은 {val(기지급일자)} 매도인계좌로 ({val(계좌번호)}) 입금했으며, "
            f"나머지는 계약서 작성당일 매도인계좌로 입금하면 본 계약은 성립한다. 또한 중도금과 잔금도 동일 계좌로 입금하기로 한다."
        )

    if opt_ilbugeom:
        clauses.append(
            "계약금의 일부금(예치금) 지급 후 일방의 단순 변심으로 본 계약 체결을 포기할 경우, "
            "매수인은 기지급액을 포기하고 매도인은 수령액의 배액을 상환함으로써 계약을 해제할 수 있다."
        )

    if opt_jeonse:
        clauses.append(
            f"잔금과 동시에 매도인이 {val(전세보증금, 'eok')}에 전세로 거주하는 조건부 계약이며, "
            f"임대차 기간 중 일체 수리비는 매도인(임차인)이 부담한다."
        )

    if opt_isabi:
        clauses.append("이주비 대출은 매수인(임대인)이 수령하여 전세금 반환에 사용하며, 실거주에 따른 이사비는 현재 거주자(매도인)가 수령한다.")

    if opt_su익:
        clauses.append("이주 전까지 발생하는 월세 수익은 매도인이 수령하되, 해당 기간의 주택 관리 및 임차인 관리는 매도인이 책임진다.")

    if opt_daegeum:
        acnt = val(계좌번호) if val(계좌번호) != "[    ]" else "(계좌정보 기재)"
        clauses.append(f"매도인 {val(매도인)}님은 매매대금 전체에 대해 {val(수령인)}님 소유의 통장({acnt})으로 받는 것에 동의한다.")

    if opt_ijubi:
        clauses.append("기본 이주비 이자는 매수자가 부담하며, 사업비 명목의 이주비 이자는 잔금일까지 매도자가, 이후부터는 매수자가 부담한다.")

    if opt_myeolsil:
        clauses.append(
            f"잔금일까지 멸실등기가 안 될 경우 잔금일을 연기하되, "
            f"최대 기한({val(멸실최대기한)}) 초과 시 근저당 설정 후 등기를 먼저 이전하기로 한다."
        )

    clauses.append("첨부서류: 중개대상물확인설명서, 등기사항증명서, 토지대장, 지적도, 토지이용계획확인원 각 1부.")

    numbered = "\n".join(f"{i}. {c}" for i, c in enumerate(clauses, 1))

    acnt_line = f"\n\n※ 계약금 수령 계좌번호: {val(계좌번호)}" if val(계좌번호) != "[    ]" else ""

    if is_prov:
        header = (
            f"< 부동산 매매계약 약정서 >\n"
            f"부동산표시 : {val(소재지)} ({val(구역명)} 구역 내 매물)\n"
            f"매도인: {val(매도인)}\n"
            f"매수인: {val(매수인)}\n\n"
            f"■매매금액: {val(총매매금액, 'money')}\n"
            f"감정가액: 약 {jeon} (현재비례율: {bire})\n"
            f"권리가액: {gwon}\n\n"
            f"■계약금: {val(총계약금, 'money')} 중 금일 {val(기지급금액)} 송금\n"
            f"-지급일: {val(기지급일자)}\n"
            f"계약서작성일시: {val(작성예정일)}\n\n"
            f"■중도금: {val(중도금)}\n\n"
            f"■임대차: 주전세 {val(전세보증금, 'eok')}\n\n"
            f"■잔금: {val(잔금)}\n\n"
            f"*매도인 입금계좌:\n{val(계좌번호)}\n\n\n"
            f"*특약사항*\n"
        )
        footer = (
            "\n\n*계약금 일부 입금 후, 일방 해제 시\n"
            "매도인의 일방적 해제 시에는 계약금일부 입금금액의 배액을 상환하기로 하며,\n"
            "매수인의 일방적 해제 시에는 계약금일부 입금금액을 포기하기로 한다.\n"
        )
        return header + numbered + footer
    else:
        return numbered + acnt_line


result = gen_clauses()

# ─────────────────────────────────── 결과 출력 ───────────────────────────────

st.markdown('<div class="section-title">📋 생성된 특약 문구</div>', unsafe_allow_html=True)

edited = st.text_area(
    label="결과 (직접 수정 가능)",
    value=result,
    height=500,
    label_visibility="collapsed"
)

cola, colb = st.columns(2)

with cola:
    if st.button("📋 전체 복사 (클립보드)", use_container_width=True, type="primary"):
        st.code(edited, language=None)
        st.info("⬆️ 위 내용을 길게 눌러 복사 후 카카오톡에 붙여넣기하세요!")

with colb:
    # 다운로드 버튼 (메모장/파일로 저장)
    st.download_button(
        label="💾 텍스트 파일로 저장",
        data=edited.encode("utf-8"),
        file_name="재개발특약.txt",
        mime="text/plain",
        use_container_width=True
    )

st.divider()
st.caption("📌 모바일에서 복사하려면: 결과창 텍스트를 길게 눌러 전체선택 → 복사 → 카카오톡 붙여넣기")
