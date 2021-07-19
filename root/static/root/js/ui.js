function isContentFilled(){
    let bodyHeight = document.body.scrollHeight
    let contentHeight = document.getElementsByClassName('footer')[0].scrollHeight +
        document.getElementsByClassName('navbar')[0].scrollHeight + document.getElementById('content-container').scrollHeight
    if (document.getElementsByClassName('viewport-header').length > 0 ) {
        return true
    }
    return bodyHeight <= contentHeight;
}

function sethref(doc){
    doc.href = "?exp=" + doc.getElementsByClassName('card-footer')[0].innerText
}

function setFooter() {
    if (isContentFilled()){
        document.getElementsByClassName('footer')[0].style.position='relative'
    } else {
        document.getElementsByClassName('footer')[0].style.position='absolute'
    }
}