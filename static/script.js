const imageBtn=document.getElementById('btnSelectHidden')
const selectBtn=document.getElementById('btnSelect')
const convertBtn=document.getElementById('convertBtn')
const confirmAttributesBtn=document.getElementById('attributeConfirmBtn')
const fileName=document.getElementById('fileName')
const sketch= document.getElementById('sketch')
const attributesListSection = document.getElementById('attributesList')
const finalImage = document.getElementById("finalImage")
const arrowImage = document.getElementById("arrowImage");
const imageSection = document.getElementById("imageSectionId");
const tryAnotherBtn = document.getElementById("tryAnotherBtn");
const loader = document.getElementById('loader');

var attr = [];
for (let i=0;i<attributes_list.length;i++){
  attributesListSection.innerHTML+=`
    <div class=${attributes_list[i].value===-1? 'attributeChip':'selectedAttributeChip'} id=${attributes_list[i].id} onClick=handleSelectAttribute('${i}')>
      <p>${attributes_list[i].title}</p>
    </div>
  `
}

const handleSelectAttribute=(index)=>{
  const id=attributes_list[index].id;
  const chip = document.getElementById(id);

  if(attributes_list[index].value==1){
    attributes_list[index].value=-1;
    chip.classList.add('attributeChip');
    chip.classList.remove('selectedAttributeChip');
  }
  else if(attributes_list[index].value==-1){
    attributes_list[index].value=1;
    chip.classList.remove('attributeChip');
    chip.classList.add('selectedAttributeChip');
  }
}

selectBtn.addEventListener('click',()=>{
  imageBtn.click();
})

imageBtn.addEventListener('change',(event)=>{
  if(imageBtn.value){
    fileName.innerHTML=event.target.files[0].name
    const src=URL.createObjectURL(event.target.files[0])
    sketch.src=src
  }
  else{
    fileName.innerHTML='No sketch choosen, yet.'
    sketch.src = "{{ url_for('static', filename='./placeholder.jpg') }}";
  }
})

const prepareAttributeFile = () => {
  attr = [];
  for (let i = 0; i < attributes_list.length; i++) {
    attr.push((attributes_list[i].value).toFixed(1));
  }
  console.log(attr);
  confirmAttributesBtn.style.display = "none";
}

confirmAttributesBtn.addEventListener('click', prepareAttributeFile)

tryAnotherBtn.addEventListener('click', () => {
  convertBtn.style.display = "flex";
  tryAnotherBtn.style.display = "none";
  arrowImage.style.display = "none";
  loader.style.display = "none";
  imageSection.style.display = "none";
  fileName.style.display = "flex";
  selectBtn.style.display = "flex";
  confirmAttributesBtn.style.display = "flex";
  sketch.src = "{{ url_for('static', filename='./placeholder.jpg') }}";
})

convertBtn.addEventListener('click', () => {

  // arrowImage.style.display = "flex";
  loader.style.display = "flex";
  imageSection.style.display = "flex";
  fileName.style.display = "none";
  selectBtn.style.display = "none";
  convertBtn.style.display = "none";
  tryAnotherBtn.style.display = "flex";

  var data = document.getElementById("btnSelectHidden");
  let formData = new FormData();
  formData.append('image', data.files[0]);
  formData.append('attributes',attr)
  fetch('/runModel', {
    method: 'POST',
    body:formData
  }).then(res => {
    console.log("a")
    var image="";
    var reader = res.body.pipeThrough(new TextDecoderStream()).getReader()
    reader.read().then(function processText({ done, value }) {
    // Result objects contain two properties:
    // done  - true if the stream has already given you all its data.
    // value - some data. Always undefined when done is true.
    if (done) {
      // console.log("Stream complete");
      arrowImage.style.display = "flex";
      loader.style.display = "none";
      window.alert('Conversion Completed!');
      finalImage.src = image;
      return;
    }

    if(value.includes("data:image/png;"))
    {
      finalImage.src = image;
      image = value;
    }
    else
    {
      image += value;
    }
    // Read some more, and call this function again
    return reader.read().then(processText);
  });
  }).catch(err => console.error(err));
})