function openPage(pageName, elmnt) {
    var i, tabcontent, tablink;
    tabcontent = document.getElementsByClassName("bb_pd_tab");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("bb_pd_spec_rev");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].style.backgroundColor = "#cdc9c9";
      tablinks[i].style.color = "black";
      tablinks[i].style.padding = "8px 30px";
    }
    document.getElementById(pageName).style.display = "block";
    elmnt.style.backgroundColor = "#F5F5F5";
    elmnt.style.padding = "8px 60px";
    elmnt.style.color = "black";
  }
  document.getElementById("defaultOpen").click();

  
  function openpPage(pageName, elmnt) {
    var i, tabcontent, tablink;
    tabcontent = document.getElementsByClassName("bb_pd_tab");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("bb_pd_spec_rev");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].style.backgroundColor = "#cdc9c9";
      tablinks[i].style.color = "black";
    }
    document.getElementById(pageName).style.display = "block";
    elmnt.style.backgroundColor = "#F5F5F5";
    elmnt.style.color = "black";
  }
  document.getElementById("defaultOpen").click();
  