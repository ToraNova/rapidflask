
function removeAllChild(id){
	var targetElem = document.getElementById(id);
	while (targetElem.firstChild) {
		targetElem.removeChild(targetElem.firstChild);
	}
}
