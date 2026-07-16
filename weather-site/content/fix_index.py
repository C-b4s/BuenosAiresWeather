import os

with open('#index.org#', 'r', encoding='utf-8') as f:
    lines = f.readlines()

nav_html = """
#+BEGIN_export html
<nav>
  <ul>
    <li><a href="#procesamiento-robos">Procesamiento de Robos</a></li>
    <li><a href="#ieee-754">IEEE 754</a></li>
    <li><a href="#buenos-aires-weather">Buenos Aires Weather</a></li>
  </ul>
</nav>
#+END_export

"""

sections_html = """
#+BEGIN_export html
<section id="procesamiento-robos">
#+END_export

#+INCLUDE: "procesamiento_robos.org" :lines "16-"

#+BEGIN_export html
</section>

<section id="ieee-754">
#+END_export

#+INCLUDE: "ieee754.org" :lines "18-"

#+BEGIN_export html
</section>

<section id="buenos-aires-weather">
#+END_export

#+INCLUDE: "buenos_aires_weather.org" :lines "16-"

#+BEGIN_export html
</section>

<script>
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
</script>
#+END_export
"""

new_lines = []
for line in lines:
    new_lines.append(line)
    if line.strip().startswith('#+cite_export:'):
        new_lines.append(nav_html)

new_lines.append("\n" + sections_html)

with open('index.org', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
