# hfun_gridfig — emit a glyph-grid figure ("gridfig") from committed assets.
#
# Usage in markdown:
#   {{gridfig wake-boids/boids_paths.txt ink}}          static figure
#   {{gridfig wake-boids/boids_anim ink inspect freeze}} animated: inlines the
#       poster wake-boids/boids_anim.txt and attaches whichever source file
#       exists beside it (.frames.txt / .topk.json / .gibbs.json) as data-src
#       for /assets/scripts/ascii-player.js to hydrate. Pages with animated
#       figures include that script once at the bottom.
#
# Flags: ink, inspect, freeze, inline (embed the source in the page instead
# of fetching — for the homepage hero), interval=ms, seed=n, id=x, class=x,
# label=aria_label_with_underscores.
#
# INK_MAP is the single source of the site's typographic-colour rules: it
# colours static posters here at build time and is stamped onto animated
# figures as data-ink-map for the player's generic interpreter. First match
# wins; "X-Y" is a range, anything else a literal set; "*" in the class
# expands to the matched character, uppercased.
const INK_MAP = [
    ("A-G", "b* hd"),   # boid heads wear their series colour, bold
    ("a-g", "b*"),      # fresh trails wear it plain
    ("@^v<>", "acc"),   # boat marks wear the accent
    ("H-Z", "acc"),
    (":", "mut"),       # ageing trails step down through the greys
    (".·", "fnt"),
]

const SOURCE_SUFFIXES = (".frames.txt", ".topk.json", ".gibbs.json")

ink_class(ch::Char) = begin
    for (spec, cls) in INK_MAP
        hit = (length(spec) == 3 && spec[2] == '-') ?
              (spec[1] <= ch <= spec[3]) : occursin(ch, spec)
        hit && return replace(cls, "*" => uppercase(ch))
    end
    nothing
end

esc_html(ch::Char) = ch == '&' ? "&amp;" : ch == '<' ? "&lt;" :
                     ch == '>' ? "&gt;" : string(ch)

function ink_html(txt)
    io = IOBuffer()
    for ch in txt
        cls = ch == '\n' ? nothing : ink_class(ch)
        if cls === nothing
            write(io, esc_html(ch))
        else
            write(io, "<span class=\"", cls, "\">", esc_html(ch), "</span>")
        end
    end
    String(take!(io))
end

ink_map_json() = "[" * join(["[\"$spec\",\"$cls\"]" for (spec, cls) in INK_MAP], ",") * "]"

function hfun_gridfig(params)
    name = params[1]
    flags = Dict{String,String}()
    for p in params[2:end]
        kv = split(p, "="; limit=2)
        flags[kv[1]] = length(kv) == 2 ? kv[2] : "true"
    end

    if endswith(name, ".txt")                       # forced static
        poster, srcfile = joinpath("_assets", name), nothing
    else
        poster = joinpath("_assets", name * ".txt")
        hits = filter(s -> isfile(joinpath("_assets", name * s)), SOURCE_SUFFIXES)
        isempty(hits) && error("gridfig: no source found beside $poster")
        srcfile = name * first(hits)
    end
    txt = read(poster, String)
    ink = haskey(flags, "ink")
    body = ink ? ink_html(txt) :
                 replace(txt, "&" => "&amp;", "<" => "&lt;", ">" => "&gt;")

    attrs = ["class=\"ascii-fig" *
             (haskey(flags, "class") ? " " * flags["class"] : "") * "\""]
    haskey(flags, "id") && push!(attrs, "id=\"$(flags["id"])\"")
    haskey(flags, "label") && push!(attrs,
        "role=\"img\" aria-label=\"$(replace(flags["label"], "_" => " "))\"")
    extra = ""
    if srcfile !== nothing
        if haskey(flags, "inline")
            sid = get(flags, "id", replace(name, "/" => "-")) * "-src"
            raw = read(joinpath("_assets", srcfile), String)
            extra = "<script type=\"application/json\" id=\"$sid\">" * raw * "</script>"
            push!(attrs, "data-src=\"#$sid\"")
        else
            push!(attrs, "data-src=\"/assets/$srcfile\"")
        end
        ink && push!(attrs, "data-ink-map='" * ink_map_json() * "'")
        for k in ("interval", "seed")
            haskey(flags, k) && push!(attrs, "data-$k=\"$(flags[k])\"")
        end
        for k in ("inspect", "freeze")
            haskey(flags, k) && push!(attrs, "data-$k")
        end
    end
    return "<pre " * join(attrs, " ") * ">" * body * "</pre>" * extra
end
