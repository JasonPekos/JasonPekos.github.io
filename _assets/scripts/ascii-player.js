// ascii-player.js — plays glyph-grid figures ("gridfigs").
//
// A gridfig arrives on the page complete: the build inlines its poster (a
// plain-text resting frame) into <pre class="ascii-fig">. This script only
// animates. It hydrates every such pre carrying data-src, which names the
// figure's playback source:
//
//   x.frames.txt   flipbook — header line {v,kind:"flipbook",cols,rows,
//                  frames,interval}, then frames*rows lines of glyphs
//   x.topk.json    shimmer — {v,kind:"topk",cols,rows,k,cells}; each cell
//                  ["glyphs",[probs 0-255 descending]]; a cell resamples
//                  with probability 1 - P(mode) each tick
//   x.gibbs.json   gibbs — {v,kind:"gibbs",...,glyphs,ink,kappa,cells,
//                  field}; each tick resamples `cells` random cells from
//                  P(glyph j | f) ~ exp(-(ink_j - f)^2 / 2 kappa^2)
//
//   data-src="#id" reads the source from an inline
//   <script type="application/json"> instead of fetching.
//
// Other attributes: data-seed, data-interval (ms), data-ink-map (JSON
// char-class -> css-class rules, stamped by the build; this script is a
// generic interpreter of them), data-freeze (click toggles pause),
// data-inspect (a status line under the figure reports the cell under the
// pointer — for a shimmer, its exact posterior).
//
// Manners: one shared clock for all figures; offscreen figures don't tick;
// starting a text selection pauses the figure until the selection is done;
// prefers-reduced-motion disables auto-play entirely (keyboard stepping
// still works). Space pauses, "." steps, "," steps a flipbook backwards.
(function () {
  if (window.__gridfig) return;
  window.__gridfig = true;

  var reduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var figs = [];

  function lcg(seed) {
    var s = seed >>> 0;
    return function () {
      s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
      return s / 4294967296;
    };
  }

  function esc(ch) {
    return ch === '&' ? '&amp;' : ch === '<' ? '&lt;'
         : ch === '>' ? '&gt;' : ch;
  }

  // data-ink-map: [["A-G","b* hd"], ["@^v<>","acc"], ...] — first matching
  // rule wins; "X-Y" is a range, anything else a literal set; "*" in the
  // class expands to the matched character, uppercased.
  function inker(el) {
    var raw = el.getAttribute('data-ink-map');
    if (!raw) return null;
    var rules = JSON.parse(raw);
    function cls(ch) {
      for (var i = 0; i < rules.length; i++) {
        var spec = rules[i][0];
        var hit = (spec.length === 3 && spec[1] === '-')
          ? ch >= spec[0] && ch <= spec[2]
          : spec.indexOf(ch) !== -1;
        if (hit) return rules[i][1].replace('*', ch.toUpperCase());
      }
      return null;
    }
    return function (text) {
      var out = '';
      for (var i = 0; i < text.length; i++) {
        var ch = text[i], c = ch === '\n' ? null : cls(ch);
        out += c ? '<span class="' + c + '">' + esc(ch) + '</span>' : esc(ch);
      }
      return out;
    };
  }

  function parseSource(text) {
    try {
      return JSON.parse(text);                       // topk / gibbs
    } catch (e) {
      var nl = text.indexOf('\n');
      var h = JSON.parse(text.slice(0, nl));         // flipbook header
      var lines = text.slice(nl + 1).split('\n');
      h.frameText = [];
      for (var i = 0; i < h.frames; i++)
        h.frameText.push(lines.slice(i * h.rows, (i + 1) * h.rows).join('\n'));
      return h;
    }
  }

  function pick(rand, weights) {
    var tot = 0, i;
    for (i = 0; i < weights.length; i++) tot += weights[i];
    var u = rand() * tot, acc = 0;
    for (i = 0; i < weights.length; i++) {
      acc += weights[i];
      if (u <= acc) return i;
    }
    return weights.length - 1;
  }

  function entropyNats(probs) {
    var tot = 0, h = 0, i, p;
    for (i = 0; i < probs.length; i++) tot += probs[i];
    for (i = 0; i < probs.length; i++) {
      p = probs[i] / tot;
      if (p > 0) h -= p * Math.log(p);
    }
    return h;
  }

  // ---- playback drivers: state + advance() + text() + inspect(i) --------
  function flipbook(data) {
    return {
      idx: 0,
      advance: function (dir) {
        this.idx = (this.idx + (dir || 1) + data.frames) % data.frames;
      },
      text: function () { return data.frameText[this.idx]; },
      inspect: function (i) {
        return '"' + data.frameText[this.idx]
          .split('\n')[(i / data.cols) | 0][i % data.cols] +
          '" · frame ' + (this.idx + 1) + '/' + data.frames;
      },
      steppable: true,
    };
  }

  function shimmer(data, state, rand) {
    var n = data.rows * data.cols;
    var cells = [];                                  // flattened [glyphs, probs]
    data.cells.forEach(function (row) { row.forEach(function (c) { cells.push(c); }); });
    return {
      advance: function () {
        for (var i = 0; i < n; i++) {
          var probs = cells[i][1];
          if (rand() > 1 - probs[0] / 255) continue; // sure cells never move
          state[i] = cells[i][0][pick(rand, probs)];
        }
      },
      text: function () { return toText(state, data); },
      inspect: function (i) {
        var g = cells[i][0], p = cells[i][1], bits = [];
        for (var k = 0; k < g.length; k++) bits.push('"' + g[k] + '" ' + p[k]);
        return bits.join('  ') + ' · H = ' + entropyNats(p).toFixed(2) + ' nats';
      },
    };
  }

  function gibbs(data, state, rand) {
    var n = data.rows * data.cols;
    var field = new Float64Array(n);
    data.field.forEach(function (row, r) {
      for (var c = 0; c < data.cols; c++)
        field[r * data.cols + c] = parseInt(row.substr(c * 2, 2), 10) / 99;
    });
    var k2 = 2 * data.kappa * data.kappa;
    function draw(i) {
      var w = data.ink.map(function (v) {
        return Math.exp(-(v - field[i]) * (v - field[i]) / k2);
      });
      return data.glyphs[pick(rand, w)];
    }
    return {
      advance: function () {
        for (var k = 0; k < data.cells; k++) {
          var i = (rand() * n) | 0;
          state[i] = draw(i);
        }
      },
      text: function () { return toText(state, data); },
      inspect: function (i) {
        return '"' + state[i] + '" · f = ' + field[i].toFixed(2);
      },
    };
  }

  function toText(state, data) {
    var rows = [];
    for (var r = 0; r < data.rows; r++)
      rows.push(state.slice(r * data.cols, (r + 1) * data.cols).join(''));
    return rows.join('\n');
  }

  // ---- hydration ---------------------------------------------------------
  var DEFAULT_MS = { flipbook: 2000, topk: 120, gibbs: 110 };

  function hydrate(el) {
    var src = el.getAttribute('data-src');
    var text = src[0] === '#'
      ? Promise.resolve(document.getElementById(src.slice(1)).textContent)
      : fetch(src).then(function (r) { return r.text(); });
    text.then(parseSource).then(function (data) {
      if (data.v !== 1) return;                      // future format: stand still
      var state = el.textContent.replace(/\n/g, '').split('');
      var rand = lcg(parseInt(el.getAttribute('data-seed'), 10) || 20260716);
      var drv = data.kind === 'flipbook' ? flipbook(data)
              : data.kind === 'topk' ? shimmer(data, state, rand)
              : gibbs(data, state, rand);
      var ink = inker(el);
      var frameCache = null;
      if (ink && data.kind === 'flipbook')
        frameCache = data.frameText.map(ink);        // colour once, not per tick
      var fig = {
        el: el, data: data, drv: drv, visible: false, hold: false,
        frozen: reduced,
        interval: parseInt(el.getAttribute('data-interval'), 10) ||
                  data.interval || DEFAULT_MS[data.kind],
        next: 0,
        paint: function () {
          if (frameCache) el.innerHTML = frameCache[drv.idx];
          else if (ink) el.innerHTML = ink(drv.text());
          else el.textContent = drv.text();
        },
      };
      wire(el, fig);
      figs.push(fig);
    });
  }

  // ---- interaction -------------------------------------------------------
  function cellAt(el, ev, data) {
    var r = el.getBoundingClientRect();
    var col = Math.floor((ev.clientX - r.left) / (r.width / data.cols));
    var row = Math.floor((ev.clientY - r.top) / (r.height / data.rows));
    return col >= 0 && col < data.cols && row >= 0 && row < data.rows
      ? row * data.cols + col : -1;
  }

  function wire(el, fig) {
    el.setAttribute('tabindex', '0');
    el.addEventListener('keydown', function (e) {
      if (e.key === ' ') {
        fig.frozen = !fig.frozen;
        e.preventDefault();
      } else if (e.key === '.') {
        fig.drv.advance(1); fig.paint();
      } else if (e.key === ',' && fig.drv.steppable) {
        fig.drv.advance(-1); fig.paint();
      }
    });

    el.addEventListener('selectstart', function () { fig.hold = true; });

    if (el.hasAttribute('data-freeze')) {
      var px = 0, py = 0;
      el.addEventListener('pointerdown', function (e) {
        px = e.clientX; py = e.clientY;
      });
      el.addEventListener('pointerup', function (e) {
        if (Math.hypot(e.clientX - px, e.clientY - py) > 6) return;
        fig.frozen = !fig.frozen;
      });
    }

    if (el.hasAttribute('data-inspect')) {
      var hint = ['hover — inspect'];
      if (el.hasAttribute('data-freeze')) hint.push('click — freeze');
      hint.push('space — pause', '"." — step');
      hint = hint.join(' · ');
      var line = document.createElement('samp');
      line.className = 'gridfig-status';
      line.setAttribute('aria-hidden', 'true');
      line.textContent = hint;
      el.insertAdjacentElement('afterend', line);
      el.addEventListener('pointermove', function (ev) {
        var i = cellAt(el, ev, fig.data);
        line.textContent = i < 0 ? hint
          : 'r' + ((i / fig.data.cols) | 0) + ' c' + (i % fig.data.cols) +
            '  ' + fig.drv.inspect(i);
      });
      el.addEventListener('pointerleave', function () {
        line.textContent = hint;
      });
    }
  }

  // ---- the shared clock --------------------------------------------------
  function releaseHolds() {
    var sel = document.getSelection && document.getSelection();
    figs.forEach(function (f) {
      if (f.hold && (!sel || sel.isCollapsed || !f.el.contains(sel.anchorNode)))
        f.hold = false;
    });
  }
  document.addEventListener('selectionchange', releaseHolds);

  var io = 'IntersectionObserver' in window &&
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        e.target.__fig.visible = e.isIntersecting;
      });
    }, { rootMargin: '80px' });

  function loop(now) {
    for (var i = 0; i < figs.length; i++) {
      var f = figs[i];
      if (f.el.__fig !== f) {
        f.el.__fig = f;
        if (io) io.observe(f.el); else f.visible = true;
      }
      if (f.visible && !f.frozen && !f.hold && now >= f.next) {
        f.drv.advance(1);
        f.paint();
        f.next = now + f.interval;
      }
    }
    requestAnimationFrame(loop);
  }

  document.querySelectorAll('pre.ascii-fig[data-src]').forEach(hydrate);
  requestAnimationFrame(loop);
})();
