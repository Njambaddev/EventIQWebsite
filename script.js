// Nav background darkens on scroll
const nav=document.querySelector('nav');
if(nav){
  window.addEventListener('scroll',()=>{nav.style.background=window.scrollY>60?'rgba(13,13,13,0.97)':'rgba(13,13,13,0.88)';});
}

// Scroll-reveal with per-group stagger (repeats on scroll up/down)
(function(){
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if(!('IntersectionObserver' in window)) return;
  const sel='.hero-content>*,.hero-badge,.sound-card,.event-type-card,.mixer-copy>*,.mixer-img,.testimonial-inner>*,.cta-band>*,.sound-header,.events-header,.outsource-note,.js-reveal';
  const obs=new IntersectionObserver((entries)=>{
    entries.forEach(en=>{
      const el=en.target;
      if(en.isIntersecting){
        const sibs=[...el.parentElement.children].filter(c=>c.matches(sel));
        const idx=Math.max(sibs.indexOf(el),0);
        el.style.transitionDelay=(idx*0.07)+'s';
        el.classList.add('in-view');
      }else{
        el.style.transitionDelay='0s';
        el.classList.remove('in-view');
      }
    });
  },{threshold:0.12,rootMargin:'0px 0px -40px 0px'});
  document.querySelectorAll(sel).forEach(el=>obs.observe(el));
})();

// Homepage quick quote (email-only) -> email to Event IQ
(function(){
  const form=document.getElementById('quoteForm');
  if(!form) return;
  form.addEventListener('submit',e=>{
    e.preventDefault();
    const email=(document.getElementById('quoteEmail').value||'').trim();
    const subject=encodeURIComponent('Sound System Quote Request — Event IQ');
    const body=encodeURIComponent(
      'Hello Event IQ,\n\nI would like a quote for professional sound at my event.\n\n'+
      'My email: '+email+'\n'+
      'Event type: \n'+
      'Event date: \n'+
      'Venue / location: \n'+
      'Expected number of guests: \n\n'+
      'Thank you.'
    );
    window.location.href='mailto:njamba.dev@gmail.com?subject='+subject+'&body='+body;
  });
})();

// Contact page full enquiry form -> email to Event IQ
(function(){
  const form=document.getElementById('contactForm');
  if(!form) return;
  const val=id=>{const el=document.getElementById(id);return el?el.value.trim():'';};
  form.addEventListener('submit',e=>{
    e.preventDefault();
    const name=val('cfName'),email=val('cfEmail'),phone=val('cfPhone'),
          type=val('cfType'),date=val('cfDate'),venue=val('cfVenue'),
          venueType=val('cfVenueType'),guests=val('cfGuests'),msg=val('cfMessage');
    const subject=encodeURIComponent('Sound Booking Enquiry — '+(name||'Event IQ')+(type?(' / '+type):''));
    const body=encodeURIComponent(
      'Hello Event IQ,\n\nI would like to enquire about professional sound for my event.\n\n'+
      'Name: '+name+'\n'+
      'Email: '+email+'\n'+
      'Phone: '+phone+'\n'+
      'Event type: '+type+'\n'+
      'Event date: '+date+'\n'+
      'Venue / location: '+venue+'\n'+
      'Venue setting: '+venueType+'\n'+
      'Expected guests: '+guests+'\n\n'+
      'Message:\n'+(msg||'(none)')+'\n\n'+
      'Thank you.'
    );
    window.location.href='mailto:njamba.dev@gmail.com?subject='+subject+'&body='+body;
  });
})();
