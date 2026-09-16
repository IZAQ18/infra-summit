'use strict';
const video=document.querySelector('video');
document.querySelectorAll('[data-time]').forEach(button=>button.addEventListener('click',()=>{video.currentTime=Number(button.dataset.time);video.play().catch(()=>{});}));
const select=document.querySelector('#seed'),status=document.querySelector('#load-status');
const fields=[['contact_throughout_hold','Both jaws during hold'],['uninterrupted_carry','Uninterrupted carry'],['supported_lower','Supported lowering'],['released','Released'],['stable','Stable endpoint']];
fetch('evidence/contact-seeds.json').then(r=>{if(!r.ok)throw Error('Evidence unavailable');return r.json();}).then(data=>{
  select.textContent='';
  data.results.forEach((r,i)=>{
    const pass=r.scripted_pick_place_passed,seed=r.configuration.seed;
    const option=document.createElement('option');option.value=String(i);option.textContent=`Seed ${seed} — ${pass?'PASS':'FAIL'}`;select.append(option);
    const tr=document.createElement('tr');
    [String(seed),pass?'PASS':'FAIL',`${(r.final_xy_error_m*1000).toFixed(2)} mm`].forEach((value,j)=>{const td=document.createElement('td');td.textContent=value;if(j===1)td.className=pass?'pass':'fail';tr.append(td);});
    document.querySelector('#trial-rows').append(tr);
  });
  function show(){const r=data.results[Number(select.value)];const pass=r.scripted_pick_place_passed;const title=document.querySelector('#trial-title');title.textContent=`Seed ${r.configuration.seed}: ${pass?'PASS':'FAIL'}`;title.className=pass?'pass':'fail';document.querySelector('#error').textContent=`${(r.final_xy_error_m*1000).toFixed(2)} mm`;document.querySelector('#lift').textContent=`${(r.min_sustained_lift_m*1000).toFixed(2)} mm`;const ul=document.querySelector('#checks');ul.textContent='';for(const[key,label]of fields){const li=document.createElement('li'),strong=document.createElement('strong');strong.textContent=r[key]?'PASS':'FAIL';strong.className=r[key]?'pass':'fail';li.append(strong,document.createTextNode(label));ul.append(li);}document.querySelector('#trial-detail').hidden=false;}
  select.disabled=false;select.addEventListener('change',show);show();status.textContent='Loaded all 10 committed trial reports. Select any pass or failure.';
}).catch(()=>{status.textContent='Could not load trial reports. Use the raw JSON download below or the source repository.';});
