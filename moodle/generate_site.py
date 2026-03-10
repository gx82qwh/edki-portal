import os
import re

root = r"C:\edki\moodle"

ignore = ("index.html","generate_site.py",".DS_Store")

style = """
<style>

body{
font-family:Segoe UI, Arial;
margin:0;
background:#f4f6fb;
transition:0.3s;
padding:20px;
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
position:sticky;
top:0;
background:white;
padding:12px;
display:flex;
gap:10px;
align-items:center;
flex-wrap:wrap;
box-shadow:0 2px 8px rgba(0,0,0,0.1);
z-index:100;
}

.dark .topbar{
background:#2c2c2c;
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
width:260px;
border-radius:8px;
border:1px solid #ccc;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fill,minmax(220px,1fr));
gap:18px;
margin-top:20px;
}

.card{
display:block;
background:white;
padding:18px;
border-radius:10px;
box-shadow:0 4px 10px rgba(0,0,0,0.1);
transition:0.2s;
}

.dark .card{
background:#2c2c2c;
}

.card:hover{
transform:translateY(-3px);
}

.icon{
font-size:28px;
margin-bottom:8px;
}

.title{
font-weight:600;
word-break:break-word;
}

.progress{
margin-top:10px;
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
margin-top:10px;
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

let cards=document.getElementsByClassName("card")

for(let i=0;i<cards.length;i++){

let text=cards[i].innerText.toLowerCase()

if(text.includes(input))
cards[i].style.display=""
else
cards[i].style.display="none"

}

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

def get_icon(filename):

    ext = filename.lower().split(".")[-1]

    icons = {
        "pdf":"📕",
        "docx":"📘",
        "pptx":"📊",
        "xlsx":"📗",
        "xls":"📗",
        "txt":"📝",
        "zip":"🗜️",
        "rar":"🗜️",
        "html":"🌐"
    }

    if ext in ["png","jpg","jpeg","webp"]:
        return "🖼️"

    return icons.get(ext,"📄")


def clean_name(name):
    return name.replace("_"," ").replace("%20"," ")


def safe_id(name):
    return re.sub(r'[^a-zA-Z0-9_]', '', name.replace(" ","_"))


for current_path, dirs, files in os.walk(root):

    cards=""

    if current_path!=root:
        cards += """
<a class="card" href="../index.html">
<div class="icon">⬅️</div>
<div class="title">Назад</div>
</a>
"""

    dirs.sort()

    for d in dirs:

        if d.endswith("_files"):
            continue

        cards += f"""
<a class="card" href="{d}/index.html">
<div class="icon">📂</div>
<div class="title">{clean_name(d)}</div>
</a>
"""

    files.sort()

    for f in files:

        if f in ignore or f.endswith(".py"):
            continue

        icon=get_icon(f)
        file_id=safe_id(f)

        cards += f"""
<div class="card">

<a href="{f}" target="_blank">

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

    base = os.path.relpath("C:/edki", current_path)

    portal_link = f"{base}/main.html"
    classroom_link = f"{base}/classroom/index.html"
    moodle_link = f"{base}/moodle/index.html"
    edki_link = f"{base}/edki/index.html"

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
if(localStorage.getItem("theme")==="dark"){{
document.documentElement.classList.add("dark")
}}
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

<input id="search" class="search" onkeyup="searchFiles()" placeholder="Пошук по папці...">

</div>

<h1>{clean_name(os.path.basename(current_path))}</h1>

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