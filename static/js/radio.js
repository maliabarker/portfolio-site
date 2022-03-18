function radioCheck() {
    if (document.getElementById('ds').checked) {
        document.getElementById('ifds').style.display = 'block'; 
        document.getElementById('iflive_app').style.display = 'none';
    } else if(document.getElementById('live_app').checked) {
        document.getElementById('iflive_app').style.display = 'block'; 
        document.getElementById('ifds').style.display = 'none';
    } }