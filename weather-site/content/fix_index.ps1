$lines = Get-Content '#index.org#'
$nav = @"

#+BEGIN_export html
<nav>
  <ul>
    <li><a href="#procesamiento-robos">Procesamiento de Robos</a></li>
    <li><a href="#ieee-754">IEEE 754</a></li>
    <li><a href="#buenos-aires-weather">Buenos Aires Weather</a></li>
  </ul>
</nav>
#+END_export
"@

$sections = @"

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
"@

$newLines = @()
foreach ($line in $lines) {
    $newLines += $line
    if ($line.Trim() -match "^#\+cite_export:") {
        $newLines += $nav
    }
}
$newLines += $sections

Set-Content -Path 'index.org' -Value $newLines -Encoding UTF8
