@def website_title = "personal website"
@def website_descr = "personal website"
@def website_url = "https://JasonPekos.github.io/"

@def author = "JasonPekos"

@def mintoclevel = 2

@def ignore = ["node_modules/", "franklin", "franklin.pub"]

\newcommand{\R}{\mathbb R} \newcommand{\scal}[1]{\langle #1 \rangle}

\newcommand{\collaps}[2]{
~~~<button type="button" class="collapsible">~~~ #1 ~~~</button><div class="collapsiblecontent">~~~ #2 ~~~</div>~~~
}

\newcommand{\projectbox}[3]{"""
<div class='grid'>
  <p><a href='#2'>#3</a> #1 </p>
</div>
"""}
