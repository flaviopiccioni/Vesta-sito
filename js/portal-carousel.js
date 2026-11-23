/* Carosello del portale proprietario: un'immagine al centro con titolo e testo sotto, le vicine si intravedono ai lati; frecce, pallini e scorrimento a dito. */
(function(){
  document.querySelectorAll('.pcar').forEach(function(car){
    var tr=car.querySelector('.pc-track'),sl=[].slice.call(tr.children),sec=car.parentNode,dots=[].slice.call(sec.querySelectorAll('.pc-dots a')),cur=0;
    function go(i){i=Math.max(0,Math.min(sl.length-1,i));var s=sl[i];tr.scrollTo({left:s.offsetLeft-(tr.clientWidth-s.clientWidth)/2,behavior:'smooth'});}
    function mark(){var c=tr.scrollLeft+tr.clientWidth/2,best=0,bd=1e9;sl.forEach(function(s,i){var d=Math.abs(s.offsetLeft+s.clientWidth/2-c);if(d<bd){bd=d;best=i;}});cur=best;sl.forEach(function(s,i){s.classList.toggle('on',i===best);});dots.forEach(function(d,i){d.classList.toggle('on',i===best);});car.querySelector('.pc-prev').disabled=best===0;car.querySelector('.pc-next').disabled=best===sl.length-1;}
    car.querySelector('.pc-prev').addEventListener('click',function(){go(cur-1);});
    car.querySelector('.pc-next').addEventListener('click',function(){go(cur+1);});
    dots.forEach(function(d,i){d.addEventListener('click',function(e){e.preventDefault();go(i);});});
    sl.forEach(function(s,i){s.addEventListener('click',function(){if(i!==cur)go(i);});});
    tr.addEventListener('scroll',function(){window.requestAnimationFrame(mark);},{passive:true});
    window.addEventListener('resize',function(){go(cur);});
    mark();
  });
})();
