import os
import re

root = r"C:\edki\classroom"

ignore = ("index.html","generate_site.py",".DS_Store")

ignore_dirs = (
"_files",
"media",
"images",
"assets",
"__pycache__",
".git"
)

style = """
<style>

body{
font-family:Segoe UI,Arial;
margin:0;
background:#f4f6fb;
padding:25px;
transition:.3s;
}

.dark body{
background:#1e1e1e;
color:white;
}

a{
text-decoration:none;
color:inherit;
}

.topbar{
display:flex;
gap:10px;
flex-wrap:wrap;
margin-bottom:25px;
}

.btn{
padding:8px 14px;
border:none;
border-radius:8px;
background:#1976d2;
color:white;
cursor:pointer;
font-size:14px;
}

.btn:hover{
background:#0d47a1;
}

.search{
padding:10px;
width:240px;
border-radius:8px;
border:1px solid #ccc;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fill,minmax(240px,1fr));
gap:20px;
}

.card{
background:white;
border-radius:12px;
padding:18px;
box-shadow:0 4px 12px rgba(0,0,0,.1);
transition:.2s;
}

.dark .card{
background:#2c2c2c;
}

.card:hover{
transform:translateY(-4px);
}

.cardlink{
display:block;
}

.icon{
font-size:28px;
margin-bottom:10px;
}

.title{
font-weight:600;
word-break:break-word;
}

.progress{
margin-top:8px;
font-size:13px;
display:flex;
align-items:center;
gap:10px;
}

.star{
cursor:pointer;
font-size:18px;
}

.bar{
height:8px;
background:#ddd;
border-radius:4px;
margin-bottom:18px;
}

.bar-fill{
height:8px;
background:#4caf50;
border-radius:4px;
width:0%;
}

</style>
"""

script = """
<script>

function toggleTheme(){

if(document.documentElement.classList.contains("dark")){
document.documentElement.classList.remove("dark")
localStorage.setItem("theme","light")
}else{
document.documentElement.classList.add("dark")
localStorage.setItem("theme","dark")
}

}

function searchFiles(){

let input=document.getElementById("search").value.toLowerCase()
let cards=document.querySelectorAll(".card")

cards.forEach(c=>{
if(c.innerText.toLowerCase().includes(input))
c.style.display=""
else
c.style.display="none"
})

}

function toggleLearned(id){

let box=document.getElementById(id)

if(box.checked)
localStorage.setItem("done_"+id,"1")
else
localStorage.removeItem("done_"+id)

updateProgress()

}

function toggleStar(id){

let star=document.getElementById("star_"+id)

if(localStorage.getItem("star_"+id)){
localStorage.removeItem("star_"+id)
star.innerText="☆"
}else{
localStorage.setItem("star_"+id,"1")
star.innerText="⭐"
}

}

function loadState(){

document.querySelectorAll(".learnbox").forEach(box=>{
if(localStorage.getItem("done_"+box.id))
box.checked=true
})

document.querySelectorAll(".star").forEach(s=>{
let id=s.dataset.id
if(localStorage.getItem("star_"+id))
s.innerText="⭐"
})

updateProgress()

}

function updateProgress(){

let boxes=document.querySelectorAll(".learnbox")

let done=0
boxes.forEach(b=>{
if(localStorage.getItem("done_"+b.id))
done++
})

let percent=0
if(boxes.length>0)
percent=Math.round(done/boxes.length*100)

let bar=document.getElementById("progressbar")
if(bar) bar.style.width=percent+"%"

let label=document.getElementById("progresslabel")
if(label) label.innerText="Прогрес: "+percent+"%"

}

window.onload=loadState

</script>
"""

def clean_name(name):
    return name.replace("_"," ").replace("%20"," ")

def safe_id(name):
    return re.sub(r'[^a-zA-Z0-9_]', '', name.replace(" ","_"))

for current_path, dirs, files in os.walk(root):

    cards=""

    if current_path!=root:
        cards += """
<a class="cardlink" href="../index.html">
<div class="card">
<div class="icon">⬅️</div>
<div class="title">Назад</div>
</div>
</a>
"""

    for d in sorted(dirs):

        skip=False
        for x in ignore_dirs:
            if d.endswith(x) or d==x:
                skip=True
                break

        if skip:
            continue

        cards += f"""
<a class="cardlink" href="{d}/index.html">
<div class="card">
<div class="icon">📂</div>
<div class="title">{clean_name(d)}</div>
</div>
</a>
"""

    for f in sorted(files):

        if f in ignore or f.endswith(".py"):
            continue

        icon="📄"

        if f.endswith(".pdf"):
            icon="📕"
        elif f.endswith(".docx"):
            icon="📘"
        elif f.endswith(".pptx"):
            icon="📊"
        elif f.endswith(".html"):
            icon="🌐"

        file_id=safe_id(f)

        cards += f"""
<div class="card">

<a class="cardlink" href="{f}" target="_blank">

<div class="icon">{icon}</div>
<div class="title">{clean_name(f)}</div>

</a>

<div class="progress">

<label>
<input type="checkbox" class="learnbox" id="{file_id}" onclick="toggleLearned('{file_id}')">
вивчено
</label>

<span class="star" id="star_{file_id}" data-id="{file_id}" onclick="toggleStar('{file_id}')">☆</span>

</div>

</div>
"""

    base=os.path.relpath("C:/edki",current_path)

    portal_link=f"{base}/main.html"
    classroom_link=f"{base}/classroom/index.html"
    moodle_link=f"{base}/moodle/index.html"
    edki_link=f"{base}/edki/index.html"

    progress_block=""

    if current_path!=root:
        progress_block="""
<div id="progresslabel">Прогрес: 0%</div>

<div class="bar">
<div id="progressbar" class="bar-fill"></div>
</div>
"""

    html=f"""
<!DOCTYPE html>
<html lang="uk">

<head>

<meta charset="UTF-8">
<title>{os.path.basename(current_path)}</title>

<script>
if(localStorage.getItem("theme")==="dark")
document.documentElement.classList.add("dark")
</script>

{style}

</head>

<body>

<div class="topbar">

<a class="btn" href="{portal_link}">🏠 Портал</a>
<a class="btn" href="{classroom_link}">📚 Classroom</a>
<a class="btn" href="{moodle_link}">🎓 Moodle</a>
<a class="btn" href="{edki_link}">📂 ЄДКІ</a>

<button class="btn" onclick="toggleTheme()">🌙 Темна тема</button>

<input id="search" class="search" onkeyup="searchFiles()" placeholder="Пошук...">

</div>

<h2>{clean_name(os.path.basename(current_path))}</h2>

{progress_block}

<div class="grid">

{cards}

</div>

{script}

</body>
</html>
"""

    output=os.path.join(current_path,"index.html")

    with open(output,"w",encoding="utf-8") as f:
        f.write(html)

print("Готово.")