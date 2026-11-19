// Ilustrações vetoriais próprias (SVG, viewBox 600x600).
// Animação: atributo data-a="tipo:amplitude:velocidade:fase"
//   float (px), sway (graus), spin (graus/s), pulse (escala), blink, drift (px x)
// transform-origin vem do style (transform-box: fill-box).

const O = (o) => `style="transform-box:fill-box;transform-origin:${o}"`;

function tentacle(x, y, len, curl, w, color, phase, amp = 6) {
  const p = `M${x},${y} C${x - curl},${y + len * 0.35} ${x + curl},${y + len * 0.65} ${x - curl * 0.4},${y + len}`;
  return `<path d="${p}" stroke="${color}" stroke-width="${w}" fill="none" stroke-linecap="round" data-a="sway:${amp}:1.4:${phase}" ${O("50% 0%")}/>`;
}

const ART = {
  // ---------------------------------------------------------------- 1. COBRA
  snake: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="sk" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#e9c46a"/><stop offset="1" stop-color="#b5832e"/>
      </linearGradient>
      <radialGradient id="glw"><stop offset="0" stop-color="#c8f04a" stop-opacity=".35"/><stop offset="1" stop-color="#c8f04a" stop-opacity="0"/></radialGradient>
    </defs>
    <circle cx="300" cy="320" r="270" fill="url(#glw)"/>
    <g data-a="float:10:0.8:0">
      <path d="M120,470 C40,400 160,330 280,380 C400,430 520,390 470,300 C430,230 300,270 260,220 C220,170 290,110 360,130"
        stroke="#7a5418" stroke-width="66" fill="none" stroke-linecap="round"/>
      <path d="M120,470 C40,400 160,330 280,380 C400,430 520,390 470,300 C430,230 300,270 260,220 C220,170 290,110 360,130"
        stroke="url(#sk)" stroke-width="56" fill="none" stroke-linecap="round"/>
      <path d="M120,470 C40,400 160,330 280,380 C400,430 520,390 470,300 C430,230 300,270 260,220 C220,170 290,110 360,130"
        stroke="#6b4512" stroke-width="30" fill="none" stroke-dasharray="22 34" stroke-linecap="round" opacity=".75"/>
      <path d="M120,470 C40,400 160,330 280,380 C400,430 520,390 470,300 C430,230 300,270 260,220 C220,170 290,110 360,130"
        stroke="#fff3c4" stroke-width="6" fill="none" opacity=".35" transform="translate(-6,-10)"/>
      <g data-a="sway:6:1.1:0" ${O("0% 50%")}>
        <path d="M340,95 C380,80 450,95 462,130 C474,165 420,182 370,168 C340,160 320,120 340,95Z" fill="url(#sk)" stroke="#7a5418" stroke-width="6"/>
        <ellipse cx="418" cy="118" rx="11" ry="12" fill="#1a1205" data-a="blink" ${O("50% 50%")}/>
        <circle cx="422" cy="114" r="3.5" fill="#fff"/>
        <path d="M462,140 l40,6 m-40,-6 l38,-12" stroke="#ff4d4d" stroke-width="6" stroke-linecap="round" data-a="pulse:0.5:3:0" ${O("0% 50%")}/>
      </g>
    </g>
  </svg>`,

  island: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1fa6b8"/><stop offset="1" stop-color="#075566"/></linearGradient>
      <linearGradient id="isl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3fae4f"/><stop offset="1" stop-color="#1d6b2c"/></linearGradient>
    </defs>
    <circle cx="300" cy="300" r="280" fill="url(#sea)"/>
    <g data-a="drift:14:0.6:0">
      <path d="M40,420 q30,-14 60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0" stroke="#bff6ff" stroke-width="7" fill="none" opacity=".5"/>
      <path d="M60,480 q30,-14 60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0" stroke="#bff6ff" stroke-width="6" fill="none" opacity=".35"/>
    </g>
    <path d="M110,400 C140,300 200,220 290,200 C380,185 460,260 495,400 Z" fill="url(#isl)"/>
    <path d="M110,400 C200,380 400,380 495,400 C470,420 140,420 110,400Z" fill="#e8d39b"/>
    ${[160, 215, 270, 330, 390, 440].map((x, i) => `
      <g data-a="sway:3:1:${i}" ${O("50% 100%")}>
        <rect x="${x - 5}" y="${300 - (i % 3) * 25}" width="10" height="${70 + (i % 3) * 20}" fill="#5b3a1a"/>
        <circle cx="${x}" cy="${290 - (i % 3) * 25}" r="${34 - (i % 2) * 6}" fill="${i % 2 ? "#2e8b3e" : "#49c05a"}"/>
      </g>`).join("")}
    <path d="M200,375 c20,-18 40,10 60,-6 s40,8 55,-4" stroke="#e9c46a" stroke-width="12" fill="none" stroke-linecap="round" data-a="float:4:2:0"/>
    <g data-a="pulse:0.06:2:0" ${O("50% 100%")}>
      <rect x="455" y="250" width="10" height="120" fill="#4a3b2a"/>
      <circle cx="460" cy="235" r="52" fill="#fff" stroke="#e63946" stroke-width="12"/>
      <path d="M432,207 L488,263" stroke="#e63946" stroke-width="12"/>
      <text x="460" y="247" text-anchor="middle" font-size="40">🚫</text>
    </g>
  </svg>`,

  // ---------------------------------------------------------- 2. ÁGUA-VIVA
  jellyfish: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="bell" cx=".5" cy=".3" r=".75">
        <stop offset="0" stop-color="#ffd6f4" stop-opacity=".95"/><stop offset=".6" stop-color="#ff7ad9" stop-opacity=".55"/><stop offset="1" stop-color="#7a3cff" stop-opacity=".25"/>
      </radialGradient>
      <radialGradient id="jg"><stop offset="0" stop-color="#ff7ad9" stop-opacity=".45"/><stop offset="1" stop-color="#ff7ad9" stop-opacity="0"/></radialGradient>
      <filter id="soft"><feGaussianBlur stdDeviation="3"/></filter>
    </defs>
    <circle cx="300" cy="250" r="260" fill="url(#jg)"/>
    <g data-a="float:22:0.7:0">
      ${[0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => tentacle(185 + i * 29, 285, 210 + (i % 3) * 30, 26, 6, i % 2 ? "#ffb3ec" : "#9ee9ff", i * 0.7, 9)).join("")}
      ${[0, 1, 2, 3].map((i) => tentacle(240 + i * 40, 290, 140, 18, 16, "#ff9fe4", i, 5)).join("")}
      <g data-a="pulse:0.05:1.4:0" ${O("50% 100%")}>
        <path d="M160,290 C160,140 440,140 440,290 C400,310 200,310 160,290Z" fill="url(#bell)" stroke="#ffd6f4" stroke-width="4"/>
        <ellipse cx="300" cy="240" rx="58" ry="40" fill="#ff3b6b" opacity=".85" filter="url(#soft)"/>
        <ellipse cx="300" cy="240" rx="34" ry="22" fill="#ff8a3d"/>
        <path d="M200,200 C220,160 270,145 300,145" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" opacity=".6"/>
      </g>
    </g>
    ${[[90, 120], [500, 160], [120, 470], [480, 450], [60, 300], [540, 320]].map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="${4 + (i % 3) * 3}" fill="#fff" opacity=".7" data-a="float:14:1.1:${i}"/>`).join("")}
  </svg>`,

  // ---------------------------------------------------------- 3. TARDÍGRADO
  tardigrade: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="tb" cx=".45" cy=".35" r=".8"><stop offset="0" stop-color="#ffe9c9"/><stop offset=".7" stop-color="#e3b98a"/><stop offset="1" stop-color="#a87a52"/></radialGradient>
      <radialGradient id="tglow"><stop offset="0" stop-color="#ffd34d" stop-opacity=".3"/><stop offset="1" stop-color="#ffd34d" stop-opacity="0"/></radialGradient>
    </defs>
    <circle cx="300" cy="300" r="280" fill="url(#tglow)"/>
    ${[[80, 90], [520, 120], [110, 500], [500, 520], [300, 60], [40, 320], [560, 300]].map(([x, y], i) => `<text x="${x}" y="${y}" font-size="${18 + (i % 3) * 8}" fill="#fff" opacity=".8" data-a="pulse:0.4:${1 + i * 0.2}:${i}" ${O("50% 50%")}>✦</text>`).join("")}
    <g data-a="float:16:0.6:0">
      <g data-a="sway:4:0.5:0" ${O("50% 50%")}>
        ${[150, 230, 320, 410].map((x, i) => `
          <g data-a="sway:12:2.2:${i * 1.3}" ${O("50% 0%")}>
            <path d="M${x},360 q-8,60 4,82" stroke="#c99a6c" stroke-width="40" stroke-linecap="round" fill="none"/>
            <path d="M${x - 14},440 l-10,16 M${x},444 l0,18 M${x + 14},440 l10,16" stroke="#5a3b20" stroke-width="5" stroke-linecap="round"/>
          </g>`).join("")}
        <path d="M110,300 C110,190 220,170 300,175 C400,180 500,200 500,300 C500,370 420,390 300,390 C180,390 110,370 110,300Z" fill="url(#tb)" stroke="#8a6040" stroke-width="5"/>
        ${[200, 270, 340, 410].map((x) => `<path d="M${x},185 C${x - 18},260 ${x - 18},330 ${x},385" stroke="#b88a60" stroke-width="4" fill="none" opacity=".6"/>`).join("")}
        <g>
          <ellipse cx="485" cy="295" rx="48" ry="50" fill="url(#tb)" stroke="#8a6040" stroke-width="5"/>
          <ellipse cx="528" cy="300" rx="18" ry="14" fill="#c99a6c" stroke="#8a6040" stroke-width="4"/>
          <circle cx="528" cy="300" r="6" fill="#5a3b20"/>
          <circle cx="478" cy="272" r="7" fill="#2a1a0c" data-a="blink" ${O("50% 50%")}/>
        </g>
      </g>
    </g>
  </svg>`,

  tun: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="tb2" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#fff0d6"/><stop offset=".7" stop-color="#d9ac7c"/><stop offset="1" stop-color="#8f6440"/></radialGradient>
      <radialGradient id="tg2"><stop offset="0" stop-color="#6ec1ff" stop-opacity=".35"/><stop offset="1" stop-color="#6ec1ff" stop-opacity="0"/></radialGradient>
    </defs>
    <circle cx="300" cy="300" r="270" fill="url(#tg2)"/>
    <g data-a="spin:12" ${O("50% 50%")}>
      <ellipse cx="300" cy="300" rx="170" ry="140" fill="url(#tb2)" stroke="#8a6040" stroke-width="6"/>
      ${[-80, -30, 20, 70].map((d) => `<path d="M${300 + d},170 C${280 + d},240 ${280 + d},360 ${300 + d},430" stroke="#b88a60" stroke-width="5" fill="none" opacity=".7"/>`).join("")}
      <path d="M190,250 C230,230 260,260 250,290" stroke="#8a6040" stroke-width="5" fill="none"/>
    </g>
    <text x="300" y="560" text-anchor="middle" font-family="Inter Display" font-weight="900" font-size="56" fill="#fff" opacity=".9">💤 modo \"tun\"</text>
  </svg>`,

  // --------------------------------------------------------------- 4. POLVO
  octopus: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="oc" cx=".4" cy=".3" r=".9"><stop offset="0" stop-color="#ffb08a"/><stop offset=".6" stop-color="#ff6b4a"/><stop offset="1" stop-color="#b8283f"/></radialGradient>
      <radialGradient id="og"><stop offset="0" stop-color="#ff9d3d" stop-opacity=".35"/><stop offset="1" stop-color="#ff9d3d" stop-opacity="0"/></radialGradient>
    </defs>
    <circle cx="300" cy="300" r="280" fill="url(#og)"/>
    <g data-a="float:14:0.7:0">
      ${[
        [215, 300, -1], [245, 315, -1], [275, 322, -1], [305, 325, 1], [335, 322, 1], [365, 315, 1], [395, 300, 1], [300, 310, 0],
      ].map(([x, y, dir], i) => {
        const ex = x + dir * 150, ey = y + 210 - Math.abs(dir) * 30;
        const d = `M${x},${y} C${x + dir * 20},${y + 120} ${ex - dir * 90},${ey + 30} ${ex},${ey - 40}`;
        return `<g data-a="sway:${7 + (i % 3) * 3}:1.2:${i * 0.8}" ${O("50% 0%")}>
          <path d="${d}" stroke="#b8283f" stroke-width="38" fill="none" stroke-linecap="round"/>
          <path d="${d}" stroke="url(#oc)" stroke-width="30" fill="none" stroke-linecap="round"/>
          <path d="${d}" stroke="#ffd9c4" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="2 22" opacity=".9"/>
        </g>`;
      }).join("")}
      <g data-a="pulse:0.03:1.2:0" ${O("50% 100%")}>
        <path d="M180,300 C150,180 220,70 300,70 C380,70 450,180 420,300 C380,330 220,330 180,300Z" fill="url(#oc)" stroke="#b8283f" stroke-width="6"/>
        <circle cx="250" cy="250" r="30" fill="#fff"/><circle cx="350" cy="250" r="30" fill="#fff"/>
        <g data-a="blink" ${O("50% 50%")}><rect x="236" y="244" width="30" height="14" rx="7" fill="#1a0a0a"/><rect x="336" y="244" width="30" height="14" rx="7" fill="#1a0a0a"/></g>
        <circle cx="230" cy="140" r="14" fill="#ffd9c4" opacity=".5"/><circle cx="270" cy="115" r="9" fill="#ffd9c4" opacity=".5"/>
      </g>
    </g>
  </svg>`,

  // --------------------------------------------------- 5. PIRÂMIDES + LUA
  pyramid: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1446"/><stop offset=".7" stop-color="#d9752b"/><stop offset="1" stop-color="#ffc35a"/></linearGradient>
      <linearGradient id="pyL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd27a"/><stop offset="1" stop-color="#e6a23c"/></linearGradient>
      <clipPath id="cc"><circle cx="300" cy="300" r="280"/></clipPath>
    </defs>
    <g clip-path="url(#cc)">
      <rect width="600" height="600" fill="url(#sky)"/>
      ${[[80, 80], [150, 150], [470, 70], [530, 170], [380, 120], [60, 220]].map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="${2 + (i % 2) * 2}" fill="#fff" data-a="pulse:0.6:${1.2 + i * 0.3}:${i}" ${O("50% 50%")}/>`).join("")}
      <g data-a="float:6:0.5:0"><circle cx="440" cy="150" r="62" fill="#f4f1de"/><circle cx="420" cy="135" r="12" fill="#d8d3b8"/><circle cx="460" cy="175" r="9" fill="#d8d3b8"/><circle cx="455" cy="125" r="6" fill="#d8d3b8"/></g>
      <g data-a="drift:40:0.25:0"><g transform="translate(130,190) rotate(35)"><text font-size="60">🚀</text></g></g>
      <path d="M60,470 L230,250 L330,470Z" fill="url(#pyL)"/><path d="M230,250 L330,470 L380,470Z" fill="#b97a26"/>
      <path d="M270,470 L400,300 L480,470Z" fill="url(#pyL)"/><path d="M400,300 L480,470 L520,470Z" fill="#b97a26"/>
      <path d="M440,470 L500,390 L540,470Z" fill="#f0b955"/>
      <rect y="465" width="600" height="140" fill="#e8b45c"/>
      <path d="M0,500 q150,-30 300,0 t300,0 v100 h-600Z" fill="#d89a3f"/>
    </g>
  </svg>`,

  // -------------------------------------------------------------- 6. TUBARÃO
  shark: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="shb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6d8ba3"/><stop offset=".55" stop-color="#4a6a84"/><stop offset=".56" stop-color="#e8f1f5"/><stop offset="1" stop-color="#cfdde4"/></linearGradient>
      <radialGradient id="shg"><stop offset="0" stop-color="#5ff0d2" stop-opacity=".3"/><stop offset="1" stop-color="#5ff0d2" stop-opacity="0"/></radialGradient>
    </defs>
    <circle cx="300" cy="300" r="280" fill="url(#shg)"/>
    ${[[120, 480], [160, 420], [470, 140], [500, 90], [90, 160]].map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="${8 + (i % 3) * 5}" fill="none" stroke="#bff" stroke-width="3" opacity=".6" data-a="float:20:0.8:${i}"/>`).join("")}
    <g data-a="float:14:0.6:0"><g data-a="sway:3:0.6:1" ${O("50% 50%")}>
      <g data-a="sway:14:1.8:0" ${O("100% 50%")}>
        <path d="M120,300 L40,210 L70,300 L40,390Z" fill="#4a6a84"/>
      </g>
      <path d="M290,215 L320,120 L370,225Z" fill="#4a6a84"/>
      <path d="M110,300 C170,230 330,200 450,240 C510,260 560,285 565,300 C560,320 510,345 450,355 C330,380 170,360 110,300Z" fill="url(#shb)" stroke="#2f4a5e" stroke-width="5"/>
      <path d="M330,350 L300,430 L390,355Z" fill="#4a6a84"/>
      ${[0, 1, 2, 3].map((i) => `<path d="M${400 - i * 14},265 q-8,25 0,50" stroke="#2f4a5e" stroke-width="4" fill="none"/>`).join("")}
      <circle cx="490" cy="282" r="9" fill="#0b1620" data-a="blink" ${O("50% 50%")}/>
      <path d="M470,318 q35,10 70,-6" stroke="#2f4a5e" stroke-width="5" fill="none"/>
      <path d="M478,320 l6,10 l6,-8 l6,10 l6,-9 l6,9 l6,-10" stroke="#fff" stroke-width="3" fill="none"/>
    </g></g>
  </svg>`,

  // ------------------------------------------------------------------ 7. MEL
  honey: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="hn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd166"/><stop offset="1" stop-color="#e08a00"/></linearGradient>
      <radialGradient id="hg"><stop offset="0" stop-color="#ffb627" stop-opacity=".4"/><stop offset="1" stop-color="#ffb627" stop-opacity="0"/></radialGradient>
      <pattern id="hex" width="52" height="45" patternUnits="userSpaceOnUse"><path d="M13,0 h26 l13,22.5 l-13,22.5 h-26 l-13,-22.5Z" fill="none" stroke="#ffb627" stroke-width="3" opacity=".25"/></pattern>
    </defs>
    <circle cx="300" cy="300" r="280" fill="url(#hg)"/>
    <circle cx="300" cy="300" r="280" fill="url(#hex)"/>
    <g data-a="float:8:0.6:0">
      <rect x="170" y="150" width="260" height="56" rx="16" fill="#8a4b14"/>
      <rect x="185" y="135" width="230" height="30" rx="12" fill="#a65d1c"/>
      <path d="M160,215 C150,260 145,420 170,470 C200,515 400,515 430,470 C455,420 450,260 440,215Z" fill="#fff" opacity=".22" stroke="#fff6dd" stroke-width="6"/>
      <path d="M163,260 C152,330 150,430 172,468 C202,510 398,510 428,468 C450,430 448,330 437,260 C380,280 220,240 163,260Z" fill="url(#hn)"/>
      <rect x="205" y="320" width="190" height="100" rx="18" fill="#fff6dd"/>
      <text x="300" y="388" text-anchor="middle" font-family="Inter Display" font-weight="900" font-size="58" fill="#8a4b14">MEL</text>
      <path d="M185,250 C180,320 180,400 190,440" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" opacity=".5"/>
      <g data-a="pulse:0.25:1.2:0" ${O("50% 0%")}><path d="M230,206 C230,240 222,250 222,262 a8,8 0 0,0 16,0 C238,250 232,240 232,206Z" fill="#ffb627"/></g>
    </g>
    <g data-a="drift:30:0.7:0"><g data-a="float:18:1.5:0"><text x="440" y="150" font-size="64">🐝</text></g></g>
    <g data-a="drift:26:0.6:2"><g data-a="float:14:1.3:1"><text x="70" y="420" font-size="52">🐝</text></g></g>
  </svg>`,

  // --------------------------------------------------------- 8. FORMIGA ZUMBI
  ant: (sprout = false) => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="ag"><stop offset="0" stop-color="#d6ff3d" stop-opacity=".28"/><stop offset="1" stop-color="#d6ff3d" stop-opacity="0"/></radialGradient>
      <linearGradient id="lf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5fbf3a"/><stop offset="1" stop-color="#2d7a1f"/></linearGradient>
    </defs>
    <circle cx="300" cy="300" r="280" fill="url(#ag)"/>
    <g data-a="sway:3:0.5:0" ${O("0% 100%")}>
      <path d="M40,560 C120,420 300,340 560,330 C470,470 250,560 40,560Z" fill="url(#lf)"/>
      <path d="M40,560 C200,460 380,380 560,330" stroke="#bfe89a" stroke-width="7" fill="none"/>
      ${[0, 1, 2, 3].map((i) => `<path d="M${150 + i * 90},${500 - i * 45} q20,30 50,40" stroke="#bfe89a" stroke-width="4" fill="none" opacity=".7"/>`).join("")}
    </g>
    <g transform="translate(70,0)" data-a="${sprout ? "float:2:0.5:0" : "float:6:2.4:0"}">
      ${[0, 1, 2].map((i) => `<g data-a="sway:${sprout ? 1 : 14}:3:${i}" ${O("50% 0%")}><path d="M${200 + i * 40},360 l${-30 + i * 10},60 l-14,20" stroke="#2a1608" stroke-width="7" fill="none" stroke-linecap="round"/></g>`).join("")}
      ${[0, 1, 2].map((i) => `<g data-a="sway:${sprout ? 1 : 14}:3:${i + 1.5}" ${O("50% 0%")}><path d="M${205 + i * 40},360 l${20 + i * 6},58 l14,18" stroke="#3a2212" stroke-width="7" fill="none" stroke-linecap="round"/></g>`).join("")}
      <ellipse cx="150" cy="330" rx="62" ry="44" fill="#4a2814"/>
      <ellipse cx="135" cy="315" rx="20" ry="10" fill="#7a4a2a" opacity=".6"/>
      <ellipse cx="240" cy="340" rx="44" ry="26" fill="#3a1e0e"/>
      <circle cx="320" cy="325" r="38" fill="#4a2814"/>
      <circle cx="334" cy="315" r="8" fill="#d6ff3d" data-a="pulse:0.4:2:0" ${O("50% 50%")}/>
      <path d="M350,345 l26,16 m-26,-6 l22,22" stroke="#2a1608" stroke-width="6" stroke-linecap="round"/>
      <path d="M318,290 C320,240 350,230 370,250 M330,292 C350,260 390,265 395,280" stroke="#2a1608" stroke-width="5" fill="none" stroke-linecap="round"/>
      ${sprout ? `
        <g data-a="sway:4:0.8:0" ${O("50% 100%")}>
          <path d="M318,292 C300,220 340,160 320,70" stroke="#e8d9a8" stroke-width="12" fill="none" stroke-linecap="round"/>
          <ellipse cx="320" cy="78" rx="24" ry="34" fill="#ff8a3d"/>
          <ellipse cx="314" cy="68" rx="8" ry="12" fill="#ffd0a8" opacity=".7"/>
        </g>
        ${[0, 1, 2, 3, 4, 5, 6, 7].map((i) => `<circle cx="${250 + i * 22}" cy="${120 + (i % 3) * 40}" r="${4 + (i % 2) * 2}" fill="#ffd34d" data-a="float:30:0.6:${i}" opacity=".9"/>`).join("")}` : `
        <path d="M300,300 C292,270 304,255 296,232" stroke="#e8d9a8" stroke-width="7" fill="none" stroke-linecap="round" data-a="sway:6:1:0" ${O("50% 100%")}/>`}
    </g>
  </svg>`,
  sprout: () => ART.ant(true),

  // ------------------------------------------------------ 9. ESTRELA DE NÊUTRONS
  neutron: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="ns" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#cfe0ff"/><stop offset="1" stop-color="#5b7bff"/></radialGradient>
      <radialGradient id="nglow"><stop offset="0" stop-color="#8fb6ff" stop-opacity=".75"/><stop offset=".4" stop-color="#6b5bff" stop-opacity=".25"/><stop offset="1" stop-color="#6b5bff" stop-opacity="0"/></radialGradient>
      <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff6bd5" stop-opacity="0"/><stop offset=".5" stop-color="#ffd6f6" stop-opacity=".9"/><stop offset="1" stop-color="#ff6bd5" stop-opacity="0"/></linearGradient>
    </defs>
    ${[[60, 80], [540, 60], [90, 520], [520, 540], [300, 30], [30, 300], [570, 320], [200, 560], [420, 40]].map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="${1.5 + (i % 3)}" fill="#fff" data-a="pulse:0.7:${1 + i * 0.25}:${i}" ${O("50% 50%")}/>`).join("")}
    <circle cx="300" cy="300" r="250" fill="url(#nglow)" data-a="pulse:0.08:2:0" ${O("50% 50%")}/>
    <g data-a="spin:40" ${O("50% 50%")}>
      <rect x="282" y="-20" width="36" height="640" fill="url(#beam)" transform="rotate(25 300 300)"/>
      ${[70, 110, 150].map((r) => `<ellipse cx="300" cy="300" rx="${r}" ry="${r * 1.9}" fill="none" stroke="#8fb6ff" stroke-width="2.5" opacity=".45" transform="rotate(25 300 300)"/>`).join("")}
      ${[70, 110, 150].map((r) => `<ellipse cx="300" cy="300" rx="${r}" ry="${r * 1.9}" fill="none" stroke="#8fb6ff" stroke-width="2.5" opacity=".45" transform="rotate(205 300 300) scale(-1 1) translate(-600 0)"/>`).join("")}
    </g>
    <circle cx="300" cy="300" r="72" fill="url(#ns)"/>
    <circle cx="300" cy="300" r="72" fill="none" stroke="#fff" stroke-width="3" opacity=".7"/>
  </svg>`,

  // --------------------------------------------------------------- 10. VOMBATE
  wombat: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="wb" cx=".45" cy=".35" r=".8"><stop offset="0" stop-color="#b08a6a"/><stop offset=".7" stop-color="#7d5a3e"/><stop offset="1" stop-color="#5a3e28"/></radialGradient>
      <radialGradient id="wg"><stop offset="0" stop-color="#ffb38a" stop-opacity=".3"/><stop offset="1" stop-color="#ffb38a" stop-opacity="0"/></radialGradient>
    </defs>
    <circle cx="300" cy="300" r="280" fill="url(#wg)"/>
    <ellipse cx="300" cy="500" rx="230" ry="26" fill="#000" opacity=".25"/>
    <g data-a="pulse:0.02:1.1:0" ${O("50% 100%")}>
      <rect x="150" y="430" width="50" height="70" rx="22" fill="#5a3e28"/><rect x="400" y="430" width="50" height="70" rx="22" fill="#5a3e28"/>
      <path d="M90,360 C90,250 190,200 300,200 C420,200 510,250 510,370 C510,450 430,490 300,490 C170,490 90,450 90,360Z" fill="url(#wb)"/>
      <g data-a="sway:5:0.9:0" ${O("50% 100%")}>
        <circle cx="205" cy="165" r="38" fill="#7d5a3e"/><circle cx="205" cy="168" r="20" fill="#d9a88a"/>
        <circle cx="395" cy="165" r="38" fill="#7d5a3e"/><circle cx="395" cy="168" r="20" fill="#d9a88a"/>
        <ellipse cx="300" cy="260" rx="135" ry="110" fill="url(#wb)"/>
        <g data-a="blink" ${O("50% 50%")}><circle cx="245" cy="245" r="14" fill="#1a0f08"/><circle cx="355" cy="245" r="14" fill="#1a0f08"/></g>
        <circle cx="250" cy="240" r="4" fill="#fff"/><circle cx="360" cy="240" r="4" fill="#fff"/>
        <ellipse cx="300" cy="300" rx="52" ry="38" fill="#3a2618"/>
        <ellipse cx="288" cy="290" rx="14" ry="8" fill="#6a4a36"/>
        <circle cx="210" cy="300" r="16" fill="#ff9d8a" opacity=".5"/><circle cx="390" cy="300" r="16" fill="#ff9d8a" opacity=".5"/>
      </g>
    </g>
  </svg>`,

  cube: () => `
  <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
    <defs><radialGradient id="cg"><stop offset="0" stop-color="#9ee6a8" stop-opacity=".3"/><stop offset="1" stop-color="#9ee6a8" stop-opacity="0"/></radialGradient></defs>
    <circle cx="300" cy="300" r="280" fill="url(#cg)"/>
    ${[[180, 360, 0], [300, 360, 1], [420, 360, 2], [240, 255, 3], [360, 255, 4], [300, 150, 5]].map(([x, y, i]) => `
      <g data-a="float:${6 + i}:1:${i}">
        <path d="M${x},${y - 55} l55,-28 l55,28 l-55,28Z" transform="translate(-55,0)" fill="#9a6e4c"/>
        <path d="M${x - 55},${y - 55} l55,28 v70 l-55,-28Z" fill="#6e4a30"/>
        <path d="M${x + 55},${y - 55} l-55,28 v70 l55,-28Z" fill="#82593a"/>
      </g>`).join("")}
    <text x="300" y="545" text-anchor="middle" font-family="Inter Display" font-weight="900" font-size="54" fill="#fff" opacity=".9">📐 quinas perfeitas</text>
  </svg>`,
};

if (typeof module !== "undefined") module.exports = { ART };
