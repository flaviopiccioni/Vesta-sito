/* Slider delle schermate del portale proprietario: i pallini seguono lo scorrimento e lo comandano; avanza da solo finché l'utente non interagisce. */
(function(){
  document.querySelectorAll('.pslider').forEach(function(sl){
    var tr=sl.querySelector('.ps-track'),dots=[].slice.call(sl.querySelectorAll('.ps-dots a')),n=dots.length,cur=0,auto=true;
    function go(i){cur=(i+n)%n;tr.scrollTo({left:tr.clientWidth*cur,behavior:'smooth'});}
    function mark(){var i=Math.round(tr.scrollLeft/tr.clientWidth);dots.forEach(function(d,j){d.classList.toggle('on',j===i)});cur=i;}
    dots.forEach(function(d,i){d.addEventListener('click',function(e){e.preventDefault();auto=false;go(i);});});
    tr.addEventListener('scroll',function(){window.requestAnimationFrame(mark);},{passive:true});
    ['pointerdown','wheel','touchstart','keydown'].forEach(function(ev){sl.addEventListener(ev,function(){auto=false;},{passive:true});});
    mark();
    if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches){setInterval(function(){if(auto&&!document.hidden)go(cur+1);},5000);}
  });
})();
