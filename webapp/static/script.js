function openAbout(){
document.getElementById("aboutModal").style.display="block"
}

function closeAbout(){
document.getElementById("aboutModal").style.display="none"
}


async function detectDefect(){

const fileInput = document.getElementById("imageInput")

if(fileInput.files.length === 0){
alert("Please upload an image")
return
}

const file = fileInput.files[0]

/* Show uploaded image */

const preview = document.getElementById("inputPreview")
preview.src = URL.createObjectURL(file)
preview.style.display = "block"

const formData = new FormData()
formData.append("file", file)

const response = await fetch("/detect",{
method:"POST",
body:formData
})

const data = await response.json()

document.getElementById("result").innerText =
"Result: " + data.result

/* Show detected result image */

const resultImage = document.getElementById("resultImage")

resultImage.src = data.image + "?t=" + new Date().getTime()

resultImage.style.display = "block"

const resultText = document.getElementById("result")

resultText.innerText = "Result: " + data.result

if(data.result.includes("Good")){
resultText.style.color = "green"
}
else{
resultText.style.color = "red"
}

}