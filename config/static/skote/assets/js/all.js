function d() {dark_mode=localStorage.getItem("global_dark_mode");if(dark_mode===null){localStorage.setItem("global_dark_mode","light");return d();}document.body.setAttribute("data-sidebar",dark_mode);document.body.setAttribute("data-layout-mode",dark_mode);icon=document.getElementById("icon_dark_mode");if(dark_mode==="dark"){icon.setAttribute('class','bx bxs-sun');}else{icon.setAttribute('class','bx bxs-moon');}}
!function (a) {"use strict";d();a('[data-bs-toggle="dark-mode"]').on("click",function(e){dark_mode=localStorage.getItem('global_dark_mode');if(dark_mode==='dark'){localStorage.setItem('global_dark_mode','light');}else{localStorage.setItem('global_dark_mode','dark');}d();});}(jQuery);