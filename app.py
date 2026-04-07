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

# ─────────────────────────────────── 문서 종류 및 물건 그룹 선택 ──────────────────────────

col_a, col_b = st.columns(2)
with col_a:
    doc_type = st.radio(
        "📄 작성 문서 선택",
        ["📋 본 계약서 특약", "📝 계약금일부금 약정서"],
        horizontal=True
    )
is_prov = doc_type.startswith("📝")

with col_b:
    contract_group = st.selectbox(
        "🏷️ 물건 그룹 선택 (본 계약서 전용)",
        ["물건 그룹 1 (노량진 등)", "물건 그룹 2", "물건 그룹 3"]
    )
    if is_prov:
        contract_group = "약정서 폼 (계약금일부금)"


st.divider()

# 글로벌 변수 초기화 (에러 방지용)
구역명, 소재지, 조합원번호, 신청주택형 = "", "", "", ""
매도인, 매수인, 계좌번호, 전세보증금 = "", "", "", ""
종전자산, 비례율, 권리가액 = "", "", ""
총매매금액, 총계약금, 기지급금액 = "", "", ""
작성예정일, 기지급일자, 근저당원금 = "", "", ""
중도금, 잔금, 상환일, 멸실기한 = "", "", "", ""
진행단계 = ""
opt_jeonse = opt_loan = opt_predunggi = False
opt_noloan_check = opt_loan_coop = opt_eju_loan = False

if not is_prov:
    # --- 본 계약서 모드 ---
    st.markdown('<div class="section-title">✅ 그룹 1: 필수 공통 특약 (기본 적용, 해제 불가)</div>', unsafe_allow_html=True)
    st.info("""
    ✔️ 제1조~제9조 계약내용 인지 및 현 시설 상태 확인 (공부상 이상 없음)  
    ✔️ 개별 추정분담금 내역 및 신청 주택형 서류상 확인  
    ✔️ 재개발 사업 진행단계 인지 및 의무/권리/분양여부 조합 직접 확인 숙지  
    ✔️ 다물권자 확약 및 손해배상 (기존 안전장치)  
    ✔️ 재당첨 제한 고지 및 정보 송달/권리변동 금지  
    ✔️ 제세공과금 기준 및 세무사 의뢰 확인  
    ✔️ 사업 지연/가격 변동성에 대한 중개사 면책
    """)
    st.divider()

    st.markdown('<div class="section-title">🧱 그룹 2: 변수 입력 폼</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**🏗️ 부동의 표시 및 권리관계**")
        구역명   = st.text_input("📍 구역명", placeholder="예: 노량진8")
        진행단계 = st.text_input("📍 해당 구역 진행단계", placeholder="예: 21.12.29 관리처분인가...")
        소재지   = st.text_input("🏠 대상물건 소재지", placeholder="예: 노량진동 234-5외 1필지")
        신청주택형 = st.text_input("🏢 신청 주택형", placeholder="예: 84㎡")
        조합원번호 = st.text_input("🔢 조합원번호", placeholder="예: 854")
    with c2:
        st.markdown("**📊 재개발 가액 정보 & 일정**")
        종전자산   = st.text_input("📉 종전자산평가액", placeholder="예: 415,466,490원")
        비례율     = st.text_input("📊 비례율", placeholder="예: 100.87%")
        권리가액   = st.text_input("📈 권리가액", placeholder="예: 419,081,048원")
        멸실기한   = st.text_input("⏰ 멸실 등기 최대 기한", placeholder="예: 2026.01.29")
        작성예정일 = st.text_input("📝 본계약 작성예정일시", placeholder="예: 25년 11월13일이내 협의")
    with c3:
        st.markdown("**💰 주요 조건 및 금액합의**")
        잔금     = st.text_input("🏁 잔금액 및 지급일", placeholder="예: 700,000,000원 / 2026.2.27.")
        전세보증금 = st.text_input("🤝 조건부 전세보증금", placeholder="예: 10 (=10억)")
        근저당원금 = st.text_input("🏦 근저당 설정원금(억)", placeholder="예: 7 (=7억)")
        상환일   = st.text_input("📆 근저당 상환일", placeholder="예: 26년1월30일")

    st.divider()
    st.markdown('<div class="section-title">☑️ 선택 옵션 특약 (상황에 따라 체크)</div>', unsafe_allow_html=True)
    col_chk1, col_chk2 = st.columns(2)
    with col_chk1:
        opt_jeonse = st.checkbox("임대차 조건부", value=True, key="main_jeonse", help="조건부 전세 (입주시까지 전세보증금 잔금 공제)")
        opt_loan = st.checkbox("근저당 조건부", value=True, key="main_loan", help="조건부 근저당 설정 (매도인이 잔금 전 근저당 설정)")
        opt_predunggi = st.checkbox("투기과열지구 매수자 선등기", value=True, key="main_predunggi")
    with col_chk2:
        opt_noloan_check = st.checkbox("무근저당 확인 및 말소", value=True, key="main_noloan")
        opt_loan_coop = st.checkbox("대출실행 협조", value=True, key="main_loancoop")
        opt_eju_loan = st.checkbox("이주비대출 미접수 확인", value=True, key="main_ejuloan")

else:
    # --- 약정서 모드 ---
    st.markdown('<div class="section-title">🧱 그룹 2: 변수 입력 폼 (약정서 전용)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**🏗️ 물건 기본 및 당사자**")
        구역명   = st.text_input("📍 구역명", placeholder="예: 노량진8")
        소재지   = st.text_input("🏠 대상물건 소재지", placeholder="예: 노량진동 234-5외 1필지")
        매도인   = st.text_input("👤 매도인 성명 전원", placeholder="예: 김진영, 신혜경")
        매수인   = st.text_input("👥 매수인 성명 전원", placeholder="예: 권정환, 윤선미")
        신청주택형 = st.text_input("🏢 신청 주택형", placeholder="예: 84㎡")
    with c2:
        st.markdown("**💰 금액 및 조건부 셋팅**")
        총매매금액 = st.text_input("💵 총 매매금액", placeholder="예: 2,260,000,000원")
        총계약금   = st.text_input("💰 총 계약금액", placeholder="예: 220,000,000원")
        기지급금액 = st.text_input("💸 기지급 계약금액", placeholder="예: 5천만원")
        전세보증금 = st.text_input("🤝 조건부 전세보증금", placeholder="예: 10 (=10억)")
        근저당원금 = st.text_input("🏦 근저당 설정 원금", placeholder="예: 7 (=7억)")
    with c3:
        st.markdown("**📆 계좌 및 일정 등**")
        계좌번호 = st.text_input("💳 계약금 수령 계좌번호", placeholder="예: 신한 110-155-7.. 최영민")
        기지급일자 = st.text_input("📅 송금일자", placeholder="예: 2025.11.3.")
        작성예정일 = st.text_input("📝 본계약 작성예정일", placeholder="예: 25년 11월13일이내")
        중도금   = st.text_input("⏳ 중도금액 및 지급일", placeholder="예: 880,000,000원 / 2025.12...")
        잔금     = st.text_input("🏁 잔금액 및 지급일", placeholder="예: 700,000,000원 / 2026.2.27...")
        상환일   = st.text_input("📆 근저당 상환일", placeholder="예: 26년1월30일")

    st.divider()
    st.markdown('<div class="section-title">✅ 약정서용 옵션 특약 (상황에 따라 체크)</div>', unsafe_allow_html=True)
    col_chk1, col_chk2 = st.columns(2)
    with col_chk1:
        opt_jeonse = st.checkbox("임대차 조건부", value=True, key="prov_jeonse", help="조건부 전세 (입주시까지 전세보증금 잔금 공제)")
        opt_loan = st.checkbox("근저당 조건부", value=True, key="prov_loan", help="조건부 근저당 설정 (매도인이 잔금 전 근저당 설정)")
        opt_predunggi = st.checkbox("투기과열지구 매수자 선등기", value=True, key="prov_predunggi")
    with col_chk2:
        opt_noloan_check = st.checkbox("무근저당 확인 및 말소", value=True, key="prov_noloan")
        opt_loan_coop = st.checkbox("대출실행 협조", value=True, key="prov_loancoop")
        opt_eju_loan = st.checkbox("이주비대출 미접수 확인", value=True, key="prov_ejuloan")

# -----------------------------------------------------------


# ─────────────────────────────────── 특약 생성 ───────────────────────────────


def gen_clauses():
    jeon = val(종전자산, "money")
    bire = f"{round(float(비례율), 2)}%" if 비례율.replace(".", "").isdigit() else (비례율 or "[    ]%")
    gwon = val(권리가액, "money")
    htype = val(신청주택형, "area")
    jo_num = val(조합원번호)

    footer_cancel = (
        "\n\n*계약금 일부 입금 후, 일방 해제 시 \n"
        "매도인의 일방적 해제 시에는 계약금일부 입금금액의 배액을 상환하기로 하며,\n"
        "매수인의 일방적 해제 시에는 계약금일부 입금금액을 포기하기로 한다.\n"
    )

    jeonse_val = val(전세보증금, "eok") if 전세보증금 else "8억"
    loan_prin = f"{근저당원금}억" if 근저당원금 else "7억"
    loan_max  = f"{float(근저당원금)*1.2:.1f}억" if 근저당원금 else "8.4억"
    repay_dt  = 상환일 if 상환일 else "26년1월30일"

    if contract_group == "약정서 폼 (계약금일부금)":
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
            f"■임대차: 주전세 {jeonse_val}\n\n"
            f"■잔금: {val(잔금)}\n\n"
            f"*매도인 입금계좌:\n{val(계좌번호)}\n\n"
            f"*특약사항*\n"
        )
        
        prov_clauses = [
            "현시설상태에서의 계약이다.",
            "등기부등본, 건축물대장, 분양통지서 상 조합원번호, 소유자 통장을 통해 소유자 확인과 권리관계 확인하고 계약을 진행함.",
            f"본계약은 {val(구역명)} 재정비 촉진지구 입주권 승계를 위한 계약으로, 해당매물은 분양신청 완료된 매물로, {htype}타입 신청한 매물임을 매도인이 확인해 주고 하는 계약이다.\n(매도자는 계약일에 분양신청 접수증을 지참하기로 한다.)",
            f"매도인은(세대주및세대원포함){val(구역명)}에 해당물건 하나만 있음을 확인하고 만약 해당물건 외에 다른 물건이 있어 입주권에 경합발생시 해당물건의 입주권을 우선으로 한다.\n만약 위 사항으로 인해 매수자에게 손해가 발생할 경우 매도자는 그에 따른 손해배상을 매수자에게 해주기로 한다."
        ]
        
        if opt_jeonse:
            prov_clauses.append(f"본계약은 잔금과 동시에 매도인이 전세로 본 매매 물건에 임대차 하기로 하는 조건부 계약이다. (이주시까지 전세보증금 {jeonse_val}) 전세보증금 {jeonse_val}은 잔금에서 공제한다. \n새로운 임차인에게 전대차 하는 경우, 임대차 보증금은 현 매도인이 책임지고 반환한다.(잔금일에 매수자는 임대인으로 매도자는 임차인으로 변경되는 전세계약서를 작성하기로 한다.)")
            
        if opt_loan:
            prov_clauses.append(f"본계약은 잔금과 동시에 매도인이 근저당 (원금 {loan_prin}, 설정액 120% {loan_max})을 설정하는 조건의 계약으로 원금 {loan_prin}은 잔금에서 공제하며, 근저당 설정 원금 {loan_prin}은 {repay_dt}까지 상환하기로 한다. 만약 약속한 날짜까지 상환이 안될 경우 약속한 날로부터 이자가 발생하며 이자율은 연 10%로 하기로 한다.")
            
        if opt_predunggi:
            split_balance = val(잔금).split('원')[0] + '원' if '원' in val(잔금) else val(잔금)
            prov_clauses.append(f"현재 {val(구역명)}은 투기과열지구로, 관리처분인가일 이후에 잔금을 치룰 경우에는 입주권승계가 제한된다. 현 상황을 고려하여 해당 잔금일을 {split_balance}로 정하였음에도 불구하고 잔금일 이전에 {val(구역명)} 관리처분인가가 날 경우에는 남아있는 잔금 금액 만큼 근저당을 추가로 설정하고 매수자가 등기먼저 넘겨받기로 하며, 이 때에도 근저당 설정비는 매수자가 반반 부담하기로 한다.")
            
        if opt_noloan_check:
            prov_clauses.append("현 등기부상 설정된 근저당은 없는 상태이며, 계약일 이후 해당물건에 해가되는 각종 추가 등기사항 발생 시, 매도인 책임하에 반드시 상환 말소하기로 한다.")
            
        if opt_loan_coop:
            prov_clauses.append("매도인은 매수인이 잔금시 대출실행하는 것에 협조하기로 한다.")
            
        if opt_eju_loan:
            prov_clauses.append("현재 이주비 대출은 신청접수하지 않은 상태로, 매도자는 감정평가금액의 60%까지 이주비신청이 된다는 사실을 조합에 확인해주고 하는 계약이다.")
            
        prov_clauses.append(f"현재 {val(구역명)}은 투기과열지구로서 매도인 및 매수인은 정비사업의 5년 내지 10년 재당첨제한에 대한 설명을 듣고 인지하였으며, 재당첨금지에 해당하여 현금청산 시 단, 유책의 당사자가 각각 책임지기로 한다.")
        prov_clauses.append("본 약정서에 표시되지 않은 사항은 민법 및 부동산 매매 일반관례에 따른다.")
        
        prov_body = ""
        for i, pc in enumerate(prov_clauses, 1):
            if "\n" in pc:
                parts = pc.split('\n')
                prov_body += f"{i}. {parts[0]}\n"
                for p in parts[1:]:
                    prov_body += f"   {p}\n"
            else:
                prov_body += f"{i}. {pc}\n"
                
        return header + prov_body + footer_cancel

    elif contract_group == "물건 그룹 1 (노량진 등)":
        clauses = [
            "매도인과 매수인은 위 인쇄된 계약내용[제 1조-제9조]에 대해 설명을 듣고 인지 후 계약을 체결함.",
            "현 시설 상태에서의 매매계약이며 계약 당사자는 등기사항전부증명서, 건축물대장, 토지대장, 토지이용계획확인서 등이 이상이 없음을 확인하고 체결하는 계약임.",
            f"({val(구역명)})구역 조합이 매도인에게 통지한 \"개별 추정분담금 정보제공통지\" 서류상 본 물건 종전자산가액은 {jeon}, 비례율 {bire}, 권리가액 {gwon} 임을 상호 확인하였으며, 신청한 주택형은 {htype}임을 매도인이 확인해주고 계약을 체결한다.(관리처분인가 내역서 사본 참조)\n   (*조합원번호: {jo_num} / *감정평가 {jeon} 권리가액 {gwon} 나옴.)",
            f"매수인은 대상부동산이 {val(구역명)} 재개발추진지역({val(진행단계)})임을 인지하고, 당해 재개발 사업진행과 조합원에 대한 의무, 권리사항 및 아파트 분양여부에 대하여 조합에 확인하고, 충분히 숙지하고 본 계약을 체결한다.",
            f"매도인은(세대원 포함) {val(구역명)} 내에 본건 외 다른 물건이 없음을 확약하며, 경합 발생 시 본 물건을 우선으로 한다. 위반 시 계약은 무조건 해제되며 매도인은 매수인에게 손해배상 책임을 진다.",
            "매수인은 도정법 제72조 6항에 따른 재당첨 제한(5~10년) 규정을 숙지하였으며, 이로 인한 지위 미승계 시 매수인이 모든 책임을 진다.",
            "매도인은 잔금일까지 조합으로부터 통보받은 중요 정보를 즉시 매수인에게 고지하며, 의결권 행사가 필요할 경우 매수인의 의사에 따른다.",
            "매도인은 계약일 이후 잔금 익일까지 근저당 및 기타 제한물권을 추가로 설정하지 않으며 현 등기부 상태를 유지한다.",
            "국가, 조합, 금융권의 사정으로 인한 사업 지연 및 건축비 상승 등 가격 변동성에 대해 중개사에게 책임을 묻지 않는다.",
            "본 계약부동산에 관한 제세공과금은 인도일을 기준으로 하며, 지방세는 지방세법상 납부의무자가 부담한다.",
            "세무에 관한 사항은 세무사에게 의뢰 하기로 한다."
        ]
        if opt_jeonse:
            clauses.append(f"본계약은 잔금과 동시에 매도인이 전세로 본 매매 물건에 임대차 하기로 하는 조건부 계약이다. (이주시까지 전세보증금 {jeonse_val}) 전세보증금 {jeonse_val}은 잔금에서 공제한다. \n새로운 임차인에게 전대차 하는 경우, 임대차 보증금은 현 매도인이 책임지고 반환한다.(잔금일에 매수자는 임대인으로 매도자는 임차인으로 변경되는 전세계약서를 작성하기로 한다.)")
        if opt_loan:
            clauses.append(f"본계약은 잔금과 동시에 매도인이 근저당 (원금 {loan_prin}, 설정액 120% {loan_max})을 설정하는 조건의 계약으로 원금 {loan_prin}은 잔금에서 공제하며, 근저당 설정 원금 {loan_prin}은 {repay_dt}까지 상환하기로 한다. 만약 약속한 날짜까지 상환이 안될 경우 약속한 날로부터 이자가 발생하며 이자율은 연 10%로 하기로 한다.")
        if opt_predunggi:
            split_balance = val(잔금).split('원')[0] + '원' if '원' in val(잔금) else val(잔금)
            clauses.append(f"현재 {val(구역명)}은 투기과열지구로, 관리처분인가일 이후에 잔금을 치룰 경우에는 입주권승계가 제한된다. 현 상황을 고려하여 해당 잔금일을 {split_balance}로 정하였음에도 불구하고 잔금일 이전에 {val(구역명)} 관리처분인가가 날 경우에는 남아있는 잔금 금액 만큼 근저당을 추가로 설정하고 매수자가 등기먼저 넘겨받기로 하며, 이 때에도 근저당 설정비는 매수자가 반반 부담하기로 한다.")
        if opt_noloan_check:
            clauses.append("현 등기부상 설정된 근저당은 없는 상태이며, 계약일 이후 해당물건에 해가되는 각종 추가 등기사항 발생 시, 매도인 책임하에 반드시 상환 말소하기로 한다.")
        if opt_loan_coop:
            clauses.append("매도인은 매수인이 잔금시 대출실행하는 것에 협조하기로 한다.")
        if opt_eju_loan:
            clauses.append("현재 이주비 대출은 신청접수하지 않은 상태로, 매도자는 감정평가금액의 60%까지 이주비신청이 된다는 사실을 조합에 확인해주고 하는 계약이다.")
            
        clauses.append(f"현재 {val(구역명)}은 투기과열지구로서 매도인 및 매수인은 정비사업의 5년 내지 10년 재당첨제한에 대한 설명을 듣고 인지하였으며, 재당첨금지에 해당하여 현금청산 시 그 유책의 당사자가 각각 책임지기로 한다.")
        clauses.append("기타사항은 부동산 매매에 관한 일반 관례에 따르기로 한다.")

        numbered = "\n".join(f"{i}. {c}" for i, c in enumerate(clauses, 1))
        return numbered + footer_cancel

    elif contract_group == "물건 그룹 2":
        clauses = [
            "현시설상태에서의 계약이다.",
            f"등기부등본, 건축물대장 등을 통해 소유자 및 권리관계를 확인하고 계약을 진행함.",
            f"본 매물은 {val(구역명)} 구역의 입주권 매물로, 관련된 모든 권리·사항은 현행 법령 및 조합의 정관에 따른다.",
            f"잔금일은 {val(잔금)}로 정하되, 상호 협의 하에 이를 조정할 수 있다.",
            "매도인은 매수인의 잔금 대출 및 등기 이전에 적극 협조하기로 한다.",
            "기타사항은 부동산 매매에 관한 일반 관례에 따르기로 한다."
        ]
        numbered = "\n".join(f"{i}. {c}" for i, c in enumerate(clauses, 1))
        return numbered + footer_cancel

    elif contract_group == "물건 그룹 3":
        clauses = [
            "현시설상태에서의 계약이다.",
            "본 계약은 당사자 간의 원만한 합의에 의해 체결되며, 계약일 이후 발생하는 각종 조세 및 공과금은 잔금일을 기준으로 정산한다.",
            "해당 물건의 부동산 인도 요건 및 기타 특약사항은 본 계약서에 명시된 바에 따르며, 구체적인 내용은 별도로 협의한다.",
            "기타사항은 부동산 매매에 관한 일반 관례 및 민법에 따르기로 한다."
        ]
        numbered = "\n".join(f"{i}. {c}" for i, c in enumerate(clauses, 1))
        return numbered + footer_cancel
    
    return ""



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
