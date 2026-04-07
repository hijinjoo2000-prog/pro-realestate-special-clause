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
        background: #f0f4f8; border: 1.5px solid #4a90d9; border-radius: 10px;
        padding: 18px; font-size: 14px; line-height: 2; white-space: pre-wrap; word-break: break-all;
    }
    .section-title {
        font-size: 16px; font-weight: 700; color: #2c3e50;
        border-left: 4px solid #3498db; padding-left: 8px; margin: 16px 0 8px 0;
    }
    div[data-testid="stButton"] > button {
        font-size: 16px; font-weight: 700; padding: 10px 20px; border-radius: 8px;
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

doc_type = st.radio(
    "📄 작성 문서 선택",
    ["📋 본 계약서 특약", "📝 계약금일부금 약정서"],
    horizontal=True
)
is_prov = doc_type.startswith("📝")

st.divider()

if not is_prov:
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

st.markdown(f'<div class="section-title">🧱 그룹 2: 변수 입력 폼 {"(약정서 전용)" if is_prov else ""}</div>', unsafe_allow_html=True)

# Define all 23 variables globally to avoid NameErrors
구역명 = 진행단계 = 소재지 = 종전자산 = 비례율 = 권리가액 = 조합원번호 = 신청주택형 = ""
전세보증금 = 근저당원금 = 상환일 = 총매매금액 = 총계약금 = 기지급금액 = 기지급일자 = ""
작성예정일 = 중도금 = 잔금 = 매도인 = 매수인 = 수령인 = 계좌번호 = 멸실기한 = ""

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**🏗️ 물건 기본 및 당사자**")
    구역명   = st.text_input("📍 구역명", placeholder="예: 노량진8")
    if not is_prov: 진행단계 = st.text_input("📍 해당 구역 진행단계", placeholder="예: 21.12.29 관리처분인가...")
    소재지   = st.text_input("🏠 대상물건 소재지", placeholder="예: 노량진동 234-5외 1필지")
    신청주택형 = st.text_input("🏢 신청 주택형", placeholder="예: 84㎡")
    if not is_prov: 조합원번호 = st.text_input("🔢 조합원번호", placeholder="예: 854")
    매도인   = st.text_input("👤 매도인 성명 전원", placeholder="예: 김진영, 신혜경")
    매수인   = st.text_input("👥 매수인 성명 전원", placeholder="예: 권정환, 윤선미")

with c2:
    st.markdown("**📊 재개발 가액 및 금액합의**")
    if not is_prov:
        종전자산   = st.text_input("📉 종전자산평가액", placeholder="예: 415,466,490원")
        비례율     = st.text_input("📊 비례율", placeholder="예: 100.87%")
        권리가액   = st.text_input("📈 권리가액", placeholder="예: 419,081,048원")
    총매매금액 = st.text_input("💵 총 매매금액", placeholder="예: 2,260,000,000원")
    총계약금   = st.text_input("💰 총 계약금액", placeholder="예: 220,000,000원")
    기지급금액 = st.text_input("💸 기지급 계약금액", placeholder="예: 5천만원")
    기지급일자 = st.text_input("📅 송금일자", placeholder="예: 2025.11.3.")
    전세보증금 = st.text_input("🤝 조건부 전세보증금", placeholder="예: 10 (=10억)")

with c3:
    st.markdown("**📆 조건 및 계좌 일정**")
    근저당원금 = st.text_input("🏦 근저당 설정 원금", placeholder="예: 7 (=7억)")
    상환일   = st.text_input("📆 근저당 상환일", placeholder="예: 26년1월30일")
    수령인   = st.text_input("👤 대금 일괄 수령인명 (본계약 옵션)", placeholder="예: 김진영")
    계좌번호 = st.text_input("💳 계약금 수령 계좌번호", placeholder="예: 신한 110-155-7.. 최영민")
    작성예정일 = st.text_input("📝 본계약 작성예정일", placeholder="예: 25년 11월13일이내")
    중도금   = st.text_input("⏳ 중도금액 및 지급일", placeholder="예: 880,000,000원 / 2025.12...")
    잔금     = st.text_input("🏁 잔금액 및 지급일", placeholder="예: 700,000,000원 / 2026.2.27...")
    if not is_prov:
        멸실기한 = st.text_input("⏰ 멸실 등기 최대 기한", placeholder="예: 2026.01.29")

st.divider()

# Option variables init
opt_main_1 = opt_main_2 = opt_main_3 = opt_main_4 = False
opt_main_5 = opt_main_6 = opt_main_7 = opt_main_8 = False
opt_prov_1 = opt_prov_2 = opt_prov_3 = False
opt_prov_4 = opt_prov_5 = opt_prov_6 = False

if not is_prov:
    st.markdown('<div class="section-title">☑️ 선택 옵션 특약 (상황에 따라 체크)</div>', unsafe_allow_html=True)
    c4, c5 = st.columns(2)
    with c4:
        opt_main_1 = st.checkbox("계약금의 일부금 배액배상", value=False)
        opt_main_2 = st.checkbox("기지급 계약금 명시", value=False)
        opt_main_3 = st.checkbox("조건부 임대차(전세)", value=False)
        opt_main_4 = st.checkbox("이사비/이주비 수령", value=False)
    with c5:
        opt_main_5 = st.checkbox("수익 및 관리 책임", value=False)
        opt_main_6 = st.checkbox("대금 수령인 지정", value=False)
        opt_main_7 = st.checkbox("이주비 이자 정산", value=False)
        opt_main_8 = st.checkbox("멸실 등기 대응", value=False)
else:
    st.markdown('<div class="section-title">✅ 약정서용 옵션 특약 (상황에 따라 체크)</div>', unsafe_allow_html=True)
    c4, c5 = st.columns(2)
    with c4:
        opt_prov_1 = st.checkbox("임대차 조건부", value=True)
        opt_prov_2 = st.checkbox("근저당 조건부", value=True)
        opt_prov_3 = st.checkbox("투기과열지구 매수자 선등기", value=True)
    with c5:
        opt_prov_4 = st.checkbox("무근저당 확인 및 말소", value=True)
        opt_prov_5 = st.checkbox("대출실행 협조", value=True)
        opt_prov_6 = st.checkbox("이주비대출 미접수 확인", value=True)

st.divider()

# ─────────────────────────────────── 특약 생성 ───────────────────────────────

def gen_clauses():
    jeon = val(종전자산, "money")
    bire = val(비례율, "pct")
    gwon = val(권리가액, "money")
    htype = val(신청주택형, "area")
    jo_num = val(조합원번호)

    footer_cancel = "\n\n*계약금 일부 입금 후, 일방 해제 시\n매도인의 일방적 해제 시에는 계약금일부 입금금액의 배액을 상환하기로 하며,\n매수인의 일방적 해제 시에는 계약금일부 입금금액을 포기하기로 한다.\n"

    jeonse_val = val(전세보증금, "eok")
    loan_prin = val(근저당원금, "eok")
    
    # Calculate 120%
    loan_p_raw = 근저당원금.replace(",", "").replace(" ", "").replace("억", "")
    if loan_p_raw.replace(".", "").isdigit():
        loan_m = float(loan_p_raw) * 1.2
        loan_max = f"{loan_m:g}억" if loan_m % 1 != 0 else f"{int(loan_m)}억"
    else:
        loan_max = "[   ]"
        
    repay_dt = val(상환일)
    area_val = val(구역명)

    if is_prov:
        header = f"< 부동산 매매계약 약정서 >\n부동산표시 : {val(소재지)} ({area_val} 구역 내 매물)\n매도인: {val(매도인)}\n매수인: {val(매수인)}\n\n■매매금액: {val(총매매금액, 'money')}\n감정가액: 약 {jeon} (현재비례율: {bire})\n권리가액: {gwon}\n\n■계약금: {val(총계약금, 'money')} 중 금일 {val(기지급금액)} 송금\n-지급일: {val(기지급일자)}\n계약서작성일시: {val(작성예정일)}\n\n■중도금: {val(중도금)}\n\n■임대차: 주전세 {jeonse_val}\n\n■잔금: {val(잔금)}\n\n*매도인 입금계좌:\n{val(계좌번호)}\n\n*특약사항*\n"
        
        prov_clauses = [
            "현시설상태에서의 계약이다.",
            "등기부등본, 건축물대장, 분양통지서 상 조합원번호, 소유자 통장을 통해 소유자 확인과 권리관계 확인하고 계약을 진행함.",
            f"본계약은 {area_val} 재정비 촉진지구 입주권 승계를 위한 계약으로, 해당매물은 분양신청 완료된 매물로, {htype} 신청한 매물임을 매도인이 확인해 주고 하는 계약이다.\n(매도자는 계약일에 분양신청 접수증을 지참하기로 한다.)",
            f"매도인은(세대주및세대원포함){area_val}에 해당물건 하나만 있음을 확인하고 만약 해당물건 외에 다른 물건이 있어 입주권에 경합발생시 해당물건의 입주권을 우선으로 한다.\n만약 위 사항으로 인해 매수자에게 손해가 발생할 경우 매도자는 그에 따른 손해배상을 매수자에게 해주기로 한다."
        ]
        
        if opt_prov_1:
            prov_clauses.append(f"본계약은 잔금과 동시에 매도인이 전세로 본 매매 물건에 임대차 하기로 하는 조건부 계약이다. (이주시까지 전세보증금 {jeonse_val}) 전세보증금 {jeonse_val}은 잔금에서 공제한다. \n새로운 임차인에게 전대차 하는 경우, 임대차 보증금은 현 매도인이 책임지고 반환한다.(잔금일에 매수자는 임대인으로 매도자는 임차인으로 변경되는 전세계약서를 작성하기로 한다.)")
        if opt_prov_2:
            prov_clauses.append(f"본계약은 잔금과 동시에 매도인이 근저당 (원금 {loan_prin}, 설정액 120% {loan_max})을 설정하는 조건의 계약으로 원금 {loan_prin}은 잔금에서 공제하며, 근저당 설정 원금 {loan_prin}은 {repay_dt}까지 상환하기로 한다. 만약 약속한 날짜까지 상환이 안될 경우 약속한 날로부터 이자가 발생하며 이자율은 연 10%로 하기로 한다.")
        if opt_prov_3:
            s_bal = val(잔금).split('원')[0] + '원' if '원' in val(잔금) else val(잔금)
            prov_clauses.append(f"현재 {area_val}은 투기과열지구로, 관리처분인가일 이후에 잔금을 치룰 경우에는 입주권승계가 제한된다. 현 상황을 고려하여 해당 잔금일을 {s_bal}로 정하였음에도 불구하고 잔금일 이전에 {area_val} 관리처분인가가 날 경우에는 남아있는 잔금 금액 만큼 근저당을 추가로 설정하고 매수자가 등기먼저 넘겨받기로 하며, 이 때에도 근저당 설정비는 매수자가 반반 부담하기로 한다.")
        if opt_prov_4: prov_clauses.append("현 등기부상 설정된 근저당은 없는 상태이며, 계약일 이후 해당물건에 해가되는 각종 추가 등기사항 발생 시, 매도인 책임하에 반드시 상환 말소하기로 한다.")
        if opt_prov_5: prov_clauses.append("매도인은 매수인이 잔금시 대출실행하는 것에 협조하기로 한다.")
        if opt_prov_6: prov_clauses.append("현재 이주비 대출은 신청접수하지 않은 상태로, 매도자는 감정평가금액의 [   ]%까지 이주비신청이 된다는 사실을 조합에 확인해주고 하는 계약이다.")
            
        prov_clauses.append(f"현재 {area_val}은 투기과열지구로서 매도인 및 매수인은 정비사업의 5년 내지 10년 재당첨제한에 대한 설명을 듣고 인지하였으며, 재당첨금지에 해당하여 현금청산 시 단, 유책의 당사자가 각각 책임지기로 한다.")
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

    else:
        # 본계약서 모드
        clauses = [
            "매도인과 매수인은 위 인쇄된 계약내용[제 1조-제9조]에 대해 설명을 듣고 인지 후 계약을 체결함.",
            "현 시설 상태에서의 매매계약이며 계약 당사자는 등기사항전부증명서, 건축물대장, 토지대장, 토지이용계획확인서 등이 이상이 없음을 확인하고 체결하는 계약임.",
            f"({area_val})구역 조합이 매도인에게 통지한 \"개별 추정분담금 정보제공통지\" 서류상 본 물건 종전자산가액은 {jeon}, 비례율 {bire}, 권리가액 {gwon} 임을 상호 확인하였으며, 신청한 주택형은 {htype}임을 매도인이 확인해주고 계약을 체결한다.(관리처분인가 내역서 사본 참조)\n   (*조합원번호: {jo_num} / *감정평가 {jeon} 권리가액 {gwon} 나옴.)",
            f"매수인은 대상부동산이 {area_val} 재개발추진지역({val(진행단계)})임을 인지하고, 당해 재개발 사업진행과 조합원에 대한 의무, 권리사항 및 아파트 분양여부에 대하여 조합에 확인하고, 충분히 숙지하고 본 계약을 체결한다.",
            f"매도인은(세대원 포함) {area_val} 내에 본건 외 다른 물건이 없음을 확약하며, 경합 발생 시 본 물건을 우선으로 한다. 위반 시 계약은 무조건 해제되며 매도인은 매수인에게 손해배상 책임을 진다.",
            "매수인은 도정법 제72조 6항에 따른 재당첨 제한(5~10년) 규정을 숙지하였으며, 이로 인한 지위 미승계 시 매수인이 모든 책임을 진다.",
            "매도인은 잔금일까지 조합으로부터 통보받은 중요 정보를 즉시 매수인에게 고지하며, 의결권 행사가 필요할 경우 매수인의 의사에 따른다.",
            "매도인은 계약일 이후 잔금 익일까지 근저당 및 기타 제한물권을 추가로 설정하지 않으며 현 등기부 상태를 유지한다.",
            "국가, 조합, 금융권의 사정으로 인한 사업 지연 및 건축비 상승 등 가격 변동성에 대해 중개사에게 책임을 묻지 않는다.",
            "본 계약부동산에 관한 제세공과금은 인도일을 기준으로 하며, 지방세는 지방세법상 납부의무자가 부담한다.",
            "세무에 관한 사항은 세무사에게 의뢰 하기로 한다."
        ]
        
        if opt_main_2: # 기지급 계약금 명시
            money_v = val(기지급금액, 'eok')
            acct_v = val(계좌번호)
            clauses.append(f"계약금 중 금 {money_v}은 {val(기지급일자)} 매도인계좌로 ({acct_v}) 입금했으며, 나머지는 계약서 작성당일 매도인계좌로 입금하면 본 계약은 성립한다. 또한 중도금과 잔금도 동일 계좌로 입금하기로 한다.")
        if opt_main_1: # 배액배상
            clauses.append("계약금의 일부금(예치금) 지급 후 일방의 단순 변심으로 본 계약 체결을 포기할 경우, 매수인은 기지급액을 포기하고 매도인은 수령액의 배액을 상환함으로써 계약을 해제할 수 있다.")
        if opt_main_3: # 조건부 전세
            jeonse = val(전세보증금, 'eok')
            clauses.append(f"잔금과 동시에 매도인이 {jeonse}에 전세로 거주하는 조건부 계약이며, 임대차 기간 중 일체 수리비는 매도인(임차인)이 부담한다.")
        if opt_main_4: # 이사비/이주비 수령
            clauses.append("이주비 대출은 매수인(임대인)이 수령하여 전세금 반환에 사용하며, 실거주에 따른 이사비는 현재 거주자(매도인)가 수령한다.")
        if opt_main_5: # 수익/관리 책임
            clauses.append("이주 전까지 발생하는 월세 수익은 매도인이 수령하되, 해당 기간의 주택 관리 및 임차인 관리는 매도인이 책임진다.")
        if opt_main_6: # 대금 수령인 지정
            acct_val2 = val(계좌번호) if 계좌번호.strip() else "(계좌정보 기재)"
            clauses.append(f"매도인 {val(매도인)}님은 매매대금 전체에 대해 {val(수령인)}님 소유의 통장({acct_val2})으로 받는 것에 동의한다.")
        if opt_main_7: # 이주비 이자 정산
            clauses.append("기본 이주비 이자는 매수자가 부담하며, 사업비 명목의 이주비 이자는 잔금일까지 매도자가, 이후부터는 매수자가 부담한다.")
        if opt_main_8: # 멸실 등기 대응
            clauses.append(f"잔금일까지 멸실등기가 안 될 경우 잔금일을 연기하되, 최대 기한({val(멸실기한)}) 초과 시 근저당 설정 후 등기를 먼저 이전하기로 한다.")
            
        clauses.append("첨부서류: 중개대상물확인설명서, 등기사항증명서, 토지대장, 지적도, 토지이용계획확인원 각 1부.")

        numbered = ""
        for i, c in enumerate(clauses, 1):
            numbered += f"{i}. {c}\n"

        # 계좌번호 최하단 추가
        acct_fin = val(계좌번호)
        if acct_fin != "[    ]":
            numbered += f"\n\n※ 계약금 수령 계좌번호: {acct_fin}"
            
        return numbered

# ─────────────────────────────────── 결과 출력 ───────────────────────────────

result = gen_clauses()

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
    st.download_button(
        label="💾 텍스트 파일로 저장",
        data=edited.encode("utf-8"),
        file_name="재개발특약.txt",
        mime="text/plain",
        use_container_width=True
    )

st.divider()
st.caption("📌 모바일에서 복사하려면: 결과창 텍스트를 길게 눌러 전체선택 → 복사 → 카카오톡 붙여넣기")
