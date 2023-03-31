function active_tab(pageName, elmnt){
    tabcontent = document.getElementsByClassName("li_tabs");
    contentPage = document.getElementsByClassName("bb_ua_thirdDiv");
    for(i=0; i < tabcontent.length; i++){
        tabcontent[i].classList.remove("uaTab_active");
    }

    for(j=0; j < contentPage.length; j++) {
        contentPage[j].style.display = "none";
    }

    elmnt.classList.add("uaTab_active");
    document.getElementById(pageName).style.display = "block";
}

function ShowHideDiv(chkBox, divIds) {
    var dvPass = document.getElementById(divIds);
    dvPass.style.display = chkBox.checked ? "block" : "none";
}