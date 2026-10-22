/* Vector Translation site: theme toggle, reveal on scroll, and the hero mark.
   The hero draws the two octahedra of brand/src/mark.py and turns them slowly about the vertical axis.
   The top vertex lies on that axis, so the arrow between the copies holds still while the solids turn. */
(function () {
  var root = document.documentElement;

  function current() {
    var a = root.getAttribute('data-theme');
    if (a) return a;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  var tog = document.querySelector('.theme-toggle');
  if (tog) tog.addEventListener('click', function () {
    var next = current() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('vt-theme', next); } catch (e) {}
  });

  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  var svg = document.getElementById('hero-mark');
  if (!svg) return;
  var NS = 'http://www.w3.org/2000/svg';
  var DIST = 11, EL = 22 * Math.PI / 180, AZ0 = 15 * Math.PI / 180;
  var SHIFT = [0.55, 0.28];
  var V = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
  var E = [], F = [];
  for (var i = 0; i < 6; i++) for (var j = i + 1; j < 6; j++) {
    var d = 0; for (var k = 0; k < 3; k++) d += (V[i][k] - V[j][k]) * (V[i][k] - V[j][k]);
    if (Math.abs(d - 2) < 1e-9) E.push([i, j]);
  }
  [1, -1].forEach(function (a) { [1, -1].forEach(function (b) { [1, -1].forEach(function (c) {
    var n = [a, b, c], fv = [];
    for (var q = 0; q < 6; q++) if (n[0] * V[q][0] + n[1] * V[q][1] + n[2] * V[q][2] === 1) fv.push(q);
    F.push([n, fv]);
  }); }); });

  function turn(p, spin) {
    var x = p[0], y = p[1], z = p[2];
    var x1 = x * Math.cos(spin) + z * Math.sin(spin), z1 = -x * Math.sin(spin) + z * Math.cos(spin);
    var y2 = y * Math.cos(EL) - z1 * Math.sin(EL), z2 = y * Math.sin(EL) + z1 * Math.cos(EL);
    return [x1, y2, z2];
  }

  // fixed scale and offset, from the static pose, so the figure does not breathe as it turns
  var BOX = [6, 6, 94, 94];
  function proj(spin) {
    var R = V.map(function (v) { return turn(v, spin); });
    var P = R.map(function (v) { return [v[0] * DIST / (DIST + v[2]), -v[1] * DIST / (DIST + v[2])]; });
    var vis = E.map(function () { return false; });
    F.forEach(function (f) {
      var nr = turn(f[0], spin), fv = f[1], c = [0, 0, 0];
      fv.forEach(function (q) { for (var k = 0; k < 3; k++) c[k] += R[q][k] / 3; });
      if (nr[0] * c[0] + nr[1] * c[1] + nr[2] * (c[2] + DIST) < 0) {
        E.forEach(function (e, n) { if (fv.indexOf(e[0]) >= 0 && fv.indexOf(e[1]) >= 0) vis[n] = true; });
      }
    });
    return { R: R, P: P, vis: vis };
  }
  var p0 = proj(AZ0);
  var xs = p0.P.map(function (p) { return p[0]; }), ys = p0.P.map(function (p) { return p[1]; });
  var w = Math.max.apply(null, xs) - Math.min.apply(null, xs), h = Math.max.apply(null, ys) - Math.min.apply(null, ys);
  var dx = SHIFT[0] * w, dy = SHIFT[1] * w;
  var sc = Math.min((BOX[2] - BOX[0]) / (w + dx), (BOX[3] - BOX[1]) / (h + dy)) * 0.94;
  var ox = (BOX[0] + BOX[2]) / 2 - (Math.min.apply(null, xs) + (w + dx) / 2) * sc;
  var oy = (BOX[1] + BOX[3]) / 2 - (Math.min.apply(null, ys) + (h + dy) / 2) * sc;

  function line(cls, sw) {
    var l = document.createElementNS(NS, 'line');
    l.setAttribute('class', cls); l.setAttribute('stroke-width', sw); l.setAttribute('stroke-linecap', 'round');
    return l;
  }
  var gS = document.createElementNS(NS, 'g'), gBh = document.createElementNS(NS, 'g'), gA = document.createElementNS(NS, 'g'), gB = document.createElementNS(NS, 'g');
  [gS, gBh, gA, gB].forEach(function (g) { svg.appendChild(g); });
  var LS = E.map(function () { return gS.appendChild(line('s', 0.55)); });
  var LB = E.map(function () { return gB.appendChild(line('b', 1.15)); });
  var LBh = E.map(function () { return gBh.appendChild(line('bh', 0.45)); });

  function draw(spin) {
    var g = proj(spin);
    var A = g.P.map(function (p) { return [p[0] * sc + ox, p[1] * sc + oy]; });
    var B = A.map(function (p) { return [p[0] + dx * sc, p[1] + dy * sc]; });
    E.forEach(function (e, n) {
      var a = A[e[0]], b = A[e[1]];
      LS[n].setAttribute('x1', a[0].toFixed(2)); LS[n].setAttribute('y1', a[1].toFixed(2));
      LS[n].setAttribute('x2', b[0].toFixed(2)); LS[n].setAttribute('y2', b[1].toFixed(2));
      LS[n].setAttribute('class', g.vis[n] ? 's' : 'sh');
      LS[n].setAttribute('stroke-width', g.vis[n] ? 0.55 : 0.38);
      var c = B[e[0]], d = B[e[1]];
      [LB[n], LBh[n]].forEach(function (L) {
        L.setAttribute('x1', c[0].toFixed(2)); L.setAttribute('y1', c[1].toFixed(2));
        L.setAttribute('x2', d[0].toFixed(2)); L.setAttribute('y2', d[1].toFixed(2));
      });
      LB[n].style.display = g.vis[n] ? '' : 'none';
      LBh[n].style.display = g.vis[n] ? 'none' : '';
    });
    return [A[2], B[2]];
  }

  // the arrow: top vertex of the source to the top vertex of the translated copy
  var ends = draw(AZ0), a = ends[0], b = ends[1];
  var ang = Math.atan2(b[1] - a[1], b[0] - a[0]), hd = 3.4;
  var base = [b[0] - hd * Math.cos(ang), b[1] - hd * Math.sin(ang)];
  var shaft = line('a', 0.85);
  shaft.setAttribute('x1', a[0]); shaft.setAttribute('y1', a[1]); shaft.setAttribute('x2', base[0]); shaft.setAttribute('y2', base[1]);
  var head = document.createElementNS(NS, 'path');
  head.setAttribute('class', 'a');
  head.setAttribute('stroke-width', '0.5'); head.setAttribute('stroke-linejoin', 'round');
  head.setAttribute('d', 'M' + b[0] + ',' + b[1] + ' L' + (base[0] + hd * .55 * Math.sin(ang)) + ',' + (base[1] - hd * .55 * Math.cos(ang)) +
    ' L' + (base[0] - hd * .55 * Math.sin(ang)) + ',' + (base[1] + hd * .55 * Math.cos(ang)) + ' Z');
  gA.appendChild(shaft); gA.appendChild(head);

  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (still) return;
  var t0 = null, visible = true;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(svg);
  }
  function frame(t) {
    if (t0 === null) t0 = t;
    if (visible && !document.hidden) draw(AZ0 + (t - t0) / 1000 * 0.16);   // about 40 seconds a turn
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
