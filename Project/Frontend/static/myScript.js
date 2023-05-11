var addsongtoplay = "";
var currartist = "";
var songplayer = null;
var isPlaying = false;


function playSong(link) {
    event.preventDefault();
    if (!isPlaying) {
        songplayer = new Audio(link);
        songplayer.play();
        isPlaying = true;
      } else {
        songplayer.pause();
        songplayer.currentTime = 0;
        isPlaying = false;
      }
}
function addtofav(a,b,e1) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/addtofav/"+a+"/"+b, true);
    xhr.send();
    event.preventDefault();
    var heartIcon = e1.querySelector('#heart-icona');
    heartIcon.className = "bi bi-heart-fill";
    heartIcon.style.cssText = "color: rgb(95, 182, 55) !important;";
    heartIcon.id = "heart-icond";
    heartIcon.title = "remove from favourites";
    heartIcon.addEventListener('mouseover', function() {
        heartIcon.style.cssText = "color: rgb(95, 182, 55) !important;";
    });
    heartIcon.addEventListener('mouseout', function() {
        heartIcon.style.cssText = "color: rgb(95, 182, 55) !important;";
    });
    e1.onclick = function() {
        removefromfavs(a,b,e1);
    };
}

function removefromfav(a,b,e1) {
    event.preventDefault();
    songremfav.style.display = 'block';
    setTimeout(function() {
        songremfav.style.display = 'none';
    }, 1500);
    var songcont = e1.closest('.songcont');
    songcont.classList.add("disabled");
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/removefromfav/"+a+"/"+b, true);
    xhr.send();
}

function removefromfavs(a,b,e1) {
    event.preventDefault();
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/removefromfav/"+a+"/"+b, true);
    xhr.send();
    var heartIcon = e1.querySelector('#heart-icond');
    heartIcon.className = "bi bi-heart" ;
    heartIcon.style.cssText = "color: rgb(179, 170, 154) !important;";
    heartIcon.id = "heart-icona";
    heartIcon.title = "add to favourites";
    heartIcon.addEventListener('mouseover', function() {
        heartIcon.style.cssText = "color: rgb(95, 182, 55) !important;";
        heartIcon.style.filter = "brightness(60%)";
    });
    heartIcon.addEventListener('mouseout', function() {
        heartIcon.style.cssText = "color: rgb(179, 170, 154) !important;";
        heartIcon.style.filter = "none";
    });
    heartIcon.classList.add('.bi.bi-heart');
    e1.onclick = function() {
        addtofav(a,b,e1);
    };
}

function showcrbox(a){
    event.preventDefault();
    if(a==1){
        crpl.style.display='flex';
        crpl.style.transform='scale(1)';
        libcontainer.style.filter='blur(4px)';
    }
    if(a==0){
        crpl.style.display='none';
        crpl.style.transform='scale(0)';
        libcontainer.style.filter='none';
    }
}
function selpl(a,b){
    event.preventDefault();
    if(a==1){
        plcont.style.display='flex';
        container.style.filter='blur(4px)';
        addsongtoplay=b;
    }
    if(a==0){
        plcont.style.display='none';
        container.style.filter='none';
    }
}
function addtoplaylist(a){
    event.preventDefault();
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/addtoplaylist/"+a+"/"+addsongtoplay, true);
    xhr.send();
    plcont.style.display='none';
    container.style.filter='none';
}
function removefromplaylist(a,b,e){
    event.preventDefault();
    var xhr = new XMLHttpRequest();
    var songcont = e.closest('.songcont');
    songcont.classList.add("disabled");
    xhr.open("GET", "/removefromplaylist/"+a+"/"+b, true);
    xhr.send();
}
function deleteplaylist(a,e){
    event.preventDefault();
    var xhr = new XMLHttpRequest();
    var songcont = e.closest('.songcont');
    songcont.style.display='none';
    xhr.open("GET", "/deleteplaylist/"+a, true);
    xhr.send();
}
function unfollow(a,e){
    event.preventDefault();
    var xhr = new XMLHttpRequest();
    var songcont = e.closest('.songcont');
    songcont.classList.add("disabled");
    xhr.open("GET", "/unfollow/"+a, true);
    xhr.send();
}

function follow(e){
    event.preventDefault();
    var xhr = new XMLHttpRequest();
        Follow.classList.remove("follow");
        Follow.classList.add("unfollow1");
        xhr.open("GET", "/follow", true);
        xhr.send();
        var element = document.getElementById("Follow");
        element.innerHTML = "Unfollow";
        e.onclick = function() {
            ufollow(e);
        };
}
function ufollow(e){
    event.preventDefault();
    var xhr = new XMLHttpRequest();
    Unfollow1.classList.remove("unfollow1");
        Unfollow1.classList.add("follow");
        xhr.open("GET", "/unfollowart", true);
        xhr.send();
        var element = document.getElementById("Unfollow1");
        element.innerHTML = "Follow";
        e.onclick = function() {
            follow(e);
        };
}