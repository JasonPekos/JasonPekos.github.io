@def website_title = "personal website"
@def website_descr = "personal website"
@def website_url = "https://JasonPekos.github.io/"

@def author = "JasonPekos"

@def mintoclevel = 2

@def ignore = ["node_modules/", "franklin", "franklin.pub", "bandit-mmm/", "bandit-mmm-codex/"]

<!-- theme: pages opt in to a template-rendered masthead with
     @def showmasthead = true (+ title / kicker / dek / metaline vars) -->
@def showmasthead = false

\newcommand{\R}{\mathbb R} \newcommand{\scal}[1]{\langle #1 \rangle}

<!-- \collaps renders as a native <details> element -->
\newcommand{\collaps}[2]{
~~~<details><summary>~~~ #1 ~~~</summary>~~~
#2
~~~</details>~~~
}

\newcommand{\projectbox}[3]{"""
<div class='grid'>
  <p><a href='#2'>#3</a> #1 </p>
</div>
"""}
