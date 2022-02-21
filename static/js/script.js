function copyTo(id){
    let value = document.getElementById(id).textContent;
    navigator.clipboard.writeText(value);
    window.alert("Copied!");
}
