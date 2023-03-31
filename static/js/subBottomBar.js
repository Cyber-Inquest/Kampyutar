// open many page in single tab

function openSubBottomBar(pageName, elmnt) {
  var i, tabcontent, tablink;
  tabcontent = document.getElementsByClassName("admin_subbottomBar");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("abb_li");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "blueviolet";
  }
  document.getElementById(pageName).style.display = "block";
  elmnt.style.backgroundColor = "chocolate";
}
document.getElementById("defaultOpen").click();


// open many page in single tab

function openSBBcontent(pageName, elmnt) {
  var i, tabcontent, tablink;
  tabcontent = document.getElementsByClassName("allProductsContent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("asbb_li");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "brown";
  }
  document.getElementById(pageName).style.display = "block";
  elmnt.style.backgroundColor = "chocolate";
}
document.getElementById("defaultOpen").click();


// image upload js

function showPreview(event) {
  if (event.target.files.length > 0) {
    var src = URL.createObjectURL(event.target.files[0]);
    var preview = document.getElementById("file-ip-1-preview");
    preview.src = src;
    preview.style.display = "block";
  }
}