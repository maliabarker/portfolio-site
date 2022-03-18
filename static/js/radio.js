function radioCheck() {
    if (document.getElementById('ds').checked) {
        console.log('ds clicked')
        document.getElementById('ifds').style.display = 'block'; 
        document.getElementById('iflive_app').style.display = 'none';
    } else if(document.getElementById('live_app').checked) {
        console.log('wd clicked')
        document.getElementById('iflive_app').style.display = 'block'; 
        document.getElementById('ifds').style.display = 'none';
    } }