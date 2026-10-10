// 시냅스 랩 랜딩 페이지 인터랙션: 헤더·리빌·카운터·탭·폼·상담 위젯
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  /* 헤더 고정 + 퀵바 + 맨 위로 */
  const header = $('#header'), quickbar = $('#quickbar'), totop = $('#totop');
  const onScroll = () => {
    const y = window.scrollY;
    header.classList.toggle('is-stuck', y > 40);
    quickbar.classList.toggle('is-on', y > window.innerHeight * 0.6);
    totop.classList.toggle('is-on', y > 600);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  totop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  /* 모바일 메뉴 */
  const burger = $('#burger'), mnav = $('#mobileNav');
  burger.addEventListener('click', () => mnav.classList.toggle('is-open'));
  $$('a', mnav).forEach(a => a.addEventListener('click', () => mnav.classList.remove('is-open')));

  /* 스크롤 리빌 */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: 0.15 });
  $$('.reveal').forEach(el => io.observe(el));
  $$('.steps .step').forEach((el, i) => el.style.setProperty('--i', i));

  /* 숫자 카운터 */
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target, to = +el.dataset.to, t0 = performance.now(), dur = 1600;
    const tick = t => {
      const p = Math.min(1, (t - t0) / dur), ease = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(to * ease).toLocaleString();
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    cio.unobserve(el);
  }), { threshold: 0.5 });
  $$('.count').forEach(el => cio.observe(el));

  /* 분야 탭 */
  $$('#fieldTabs .tab').forEach(btn => btn.addEventListener('click', () => {
    $$('#fieldTabs .tab').forEach(b => b.classList.toggle('is-on', b === btn));
    $$('.field-panel').forEach(p => p.classList.toggle('is-on', p.dataset.panel === btn.dataset.tab));
  }));

  /* 층별 호버 */
  $$('.floor').forEach(f => f.addEventListener('mouseenter', () => {
    $$('.floor').forEach(x => x.classList.toggle('is-on', x === f));
  }));

  /* 문의 폼 2단계 */
  const cform = $('#cform');
  const goStep = n => {
    $$('.cform__panel', cform).forEach(p => p.classList.toggle('is-on', p.dataset.step == n));
    $$('.cform__steps span', cform).forEach(s => s.classList.toggle('is-on', s.dataset.s == n));
  };
  $('#toStep2').addEventListener('click', () => {
    const req = $$('[data-step="1"] [required]', cform);
    const bad = req.find(i => !i.value.trim());
    if (bad) { bad.focus(); bad.classList.add('is-bad'); setTimeout(() => bad.classList.remove('is-bad'), 1200); return; }
    goStep(2);
  });
  $('#toStep1').addEventListener('click', () => goStep(1));
  cform.addEventListener('submit', e => {
    e.preventDefault();
    if (!$('[name=agree]', cform).checked) { alert('개인정보처리방침에 동의해 주세요.'); return; }
    const fd = new FormData(cform);
    console.log('문의 내용', Object.fromEntries(fd));
    alert('문의가 접수되었습니다. 영업일 기준 1일 이내에 연락드리겠습니다.');
    cform.reset(); goStep(1);
  });

  /* 퀵바 폼 */
  $('#qform').addEventListener('submit', e => {
    e.preventDefault();
    alert('빠른 문의가 접수되었습니다. 곧 연락드리겠습니다.');
    e.target.reset();
  });

  /* AI 상담 위젯 */
  const box = $('#chatBox'), body = $('#chatBody'), cf = $('#chatForm');
  const answers = {
    '제작 기간': '기업 소개형은 4~6주, 쇼핑몰·플랫폼형은 8~12주 정도예요. 원고·사진 준비 상태에 따라 달라집니다.',
    '제작 비용': '페이지 수와 기능(예약·결제·게시판), 촬영 포함 여부로 정해져요. 예상 범위를 알려주시면 그 안에서 구성을 제안드릴게요.',
    '진행 방식': '상담 → 기획 → 디자인(3단계 컨펌) → 개발 → 검수 → 런칭 → 24개월 사후관리 순으로 진행돼요.'
  };
  const push = (txt, me) => {
    const d = document.createElement('div');
    d.className = 'msg ' + (me ? 'msg--me' : 'msg--bot');
    d.textContent = txt; body.appendChild(d); body.scrollTop = body.scrollHeight;
  };
  const reply = q => {
    push(q, true);
    const key = Object.keys(answers).find(k => q.includes(k));
    setTimeout(() => push(key ? answers[key] : '자세한 상담은 아래 제작 문의 폼이나 전화로 남겨주시면 담당자가 바로 연락드려요.'), 500);
  };
  $('#chatFab').addEventListener('click', () => box.classList.toggle('is-open'));
  $('#chatClose').addEventListener('click', () => box.classList.remove('is-open'));
  $$('.chat__quick button').forEach(b => b.addEventListener('click', () => reply(b.dataset.q)));
  cf.addEventListener('submit', e => {
    e.preventDefault();
    const inp = $('input', cf); if (!inp.value.trim()) return;
    reply(inp.value.trim()); inp.value = '';
  });
})();

/* 셀프 견적 계산기 + 패키지 버튼 + 무료 진단 */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const form = $('#calcForm'), total = $('#calcTotal');
  if (!form) return;
  const picked = () => $$('input:checked', form);
  const calc = () => {
    const sum = picked().reduce((a, i) => a + Number(i.value), 0);
    total.textContent = sum.toLocaleString();
  };
  form.addEventListener('change', calc); calc();

  const memo = $('#memo'), contact = $('#contact');
  $('#calcSend').addEventListener('click', () => {
    const items = picked().map(i => i.dataset.label).join(', ');
    memo.value = '[셀프 견적] ' + items + ' → 예상 ' + total.textContent + '만 원~';
    contact.scrollIntoView({ behavior: 'smooth' });
  });
  $$('.plan .btn').forEach(b => b.addEventListener('click', () => {
    memo.value = '[' + b.dataset.plan + ' 패키지] 문의드립니다.';
  }));
  $('#diagForm').addEventListener('submit', e => {
    e.preventDefault();
    alert('무료 진단 신청이 접수되었습니다. 48시간 안에 리포트를 보내드리겠습니다.');
    e.target.reset();
  });
})();

/* 서비스 카드 문의 버튼 → 문의 폼 메모 자동 입력 */
document.querySelectorAll('.svc__link[data-svc]').forEach(a => a.addEventListener('click', () => {
  const m = document.getElementById('memo'); if (m) m.value = '[' + a.dataset.svc + '] 문의드립니다.';
}));
